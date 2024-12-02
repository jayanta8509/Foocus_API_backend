from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"]}})

API_URL_Generate = "https://4hwuq3qhogdp5p-7860.proxy.runpod.net/v2/generation/text-to-image-with-ip"

API_URL_UPSCALE = "https://4hwuq3qhogdp5p-7860.proxy.runpod.net/v2/generation/image-upscale-vary"

# def transform_url(url):
#     return url.replace('http://127.0.0.1:7860', 'https://267p1sqnhuz2pn-7860.proxy.runpod.net')


@app.route('/generate-image', methods=['POST'])
def generate_image():
    prompt = request.form.get('prompt')
    aspect_ratios_selection = request.form.get('aspect_ratios_selection')
    num_images = int(request.form.get('num_images'))
    guidance_scale = float(request.form.get('guidance_scale'))
    cn_stop = float(request.form.get('cn_stop'))
    cn_weight = float(request.form.get('cn_weight'))

    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
        
    image_file = request.files['image']
    cn_img = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare payload for external API
    payload = {
        "prompt": prompt,
        "negative_prompt": "",
        "style_selections": [
            "Fooocus V2",
            "Fooocus Enhance",
            "Fooocus Sharp"
        ],
        "performance_selection": "Speed",
        "aspect_ratios_selection": aspect_ratios_selection,
        "image_number": num_images,
        "image_seed": -1,
        "sharpness": 2,
        "guidance_scale": guidance_scale,
        "base_model_name": "juggernautXL_v8Rundiffusion.safetensors",
        "refiner_model_name": "None",
        "refiner_switch": 0.5,
        "loras": [
            {
            "enabled": True,
            "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
            "weight": 0.1
            },
            {
            "enabled": True,
            "model_name": "None",
            "weight": 1
            },
            {
            "enabled": True,
            "model_name": "None",
            "weight": 1
            },
            {
            "enabled": True,
            "model_name": "None",
            "weight": 1
            },
            {
            "enabled": True,
            "model_name": "None",
            "weight": 1
            }
        ],
        "advanced_params": {
            "adaptive_cfg": 7,
            "adm_scaler_end": 0.3,
            "adm_scaler_negative": 0.8,
            "adm_scaler_positive": 1.5,
            "black_out_nsfw": False,
            "canny_high_threshold": 128,
            "canny_low_threshold": 64,
            "clip_skip": 2,
            "controlnet_softness": 0.25,
            "debugging_cn_preprocessor": False,
            "debugging_dino": False,
            "debugging_enhance_masks_checkbox": False,
            "debugging_inpaint_preprocessor": False,
            "dino_erode_or_dilate": 0,
            "disable_intermediate_results": False,
            "disable_preview": False,
            "disable_seed_increment": False,
            "freeu_b1": 1.01,
            "freeu_b2": 1.02,
            "freeu_enabled": False,
            "freeu_s1": 0.99,
            "freeu_s2": 0.95,
            "inpaint_advanced_masking_checkbox": True,
            "inpaint_disable_initial_latent": False,
            "inpaint_engine": "v2.6",
            "inpaint_erode_or_dilate": 0,
            "inpaint_respective_field": 1,
            "inpaint_strength": 1,
            "invert_mask_checkbox": False,
            "mixing_image_prompt_and_inpaint": False,
            "mixing_image_prompt_and_vary_upscale": False,
            "overwrite_height": -1,
            "overwrite_step": -1,
            "overwrite_switch": -1,
            "overwrite_upscale_strength": -1,
            "overwrite_vary_strength": -1,
            "overwrite_width": -1,
            "refiner_swap_method": "joint",
            "sampler_name": "dpmpp_2m_sde_gpu",
            "scheduler_name": "karras",
            "skipping_cn_preprocessor": False,
            "vae_name": "Default (model)"
        },
        "save_meta": True,
        "meta_scheme": "fooocus",
        "save_extension": "png",
        "save_name": "",
        "read_wildcards_in_order": False,
        "require_base64": False,
        "async_process": False,
        "webhook_url": "",
        "image_prompts": [
            {
            "cn_img": cn_img,
            "cn_stop":cn_stop,
            "cn_weight": cn_weight,
            "cn_type": "ImagePrompt"
            }
        ]
}

    try:
        response = requests.post(API_URL_Generate, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # # Transform URLs in response
        # for item in data:
        #     if item.get('url'):
        #         item['url'] = transform_url(item['url'])
                
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500



@app.route('/image-upscale', methods=['POST'])
def upscale():

    prompt = request.form.get('prompt')
    aspect_ratios_selection = request.form.get('aspect_ratios_selection') #1152*896
    num_images = int(request.form.get('num_images'))
    guidance_scale = float(request.form.get('guidance_scale'))
    uov_method = request.form.get('uov_method') # Upscale (2x)
    upscale_value = float(request.form.get('upscale_value')) # 1


    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
        
    image_file = request.files['image']
    input_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare payload for external API
    payload = {
            "prompt": prompt,
            "negative_prompt": "",
            "style_selections": [
                "Fooocus V2",
                "Fooocus Enhance",
                "Fooocus Sharp"
            ],
            "performance_selection": "Speed",
            "aspect_ratios_selection": aspect_ratios_selection,
            "image_number": num_images,
            "image_seed": -1,
            "sharpness": 2,
            "guidance_scale": guidance_scale,
            "base_model_name": "juggernautXL_v8Rundiffusion.safetensors",
            "refiner_model_name": "None",
            "refiner_switch": 0.5,
            "loras": [
                {
                "enabled": True,
                "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
                "weight": 0.1
                },
                {
                "enabled": True,
                "model_name": "None",
                "weight": 1
                },
                {
                "enabled": True,
                "model_name": "None",
                "weight": 1
                },
                {
                "enabled": True,
                "model_name": "None",
                "weight": 1
                },
                {
                "enabled": True,
                "model_name": "None",
                "weight": 1
                }
            ],
            "advanced_params": {
                "adaptive_cfg": 7,
                "adm_scaler_end": 0.3,
                "adm_scaler_negative": 0.8,
                "adm_scaler_positive": 1.5,
                "black_out_nsfw": False,
                "canny_high_threshold": 128,
                "canny_low_threshold": 64,
                "clip_skip": 2,
                "controlnet_softness": 0.25,
                "debugging_cn_preprocessor": False,
                "debugging_dino": False,
                "debugging_enhance_masks_checkbox": False,
                "debugging_inpaint_preprocessor": False,
                "dino_erode_or_dilate": 0,
                "disable_intermediate_results": False,
                "disable_preview": False,
                "disable_seed_increment": False,
                "freeu_b1": 1.01,
                "freeu_b2": 1.02,
                "freeu_enabled": False,
                "freeu_s1": 0.99,
                "freeu_s2": 0.95,
                "inpaint_advanced_masking_checkbox": True,
                "inpaint_disable_initial_latent": False,
                "inpaint_engine": "v2.6",
                "inpaint_erode_or_dilate": 0,
                "inpaint_respective_field": 1,
                "inpaint_strength": 1,
                "invert_mask_checkbox": False,
                "mixing_image_prompt_and_inpaint": False,
                "mixing_image_prompt_and_vary_upscale": False,
                "overwrite_height": -1,
                "overwrite_step": -1,
                "overwrite_switch": -1,
                "overwrite_upscale_strength": -1,
                "overwrite_vary_strength": -1,
                "overwrite_width": -1,
                "refiner_swap_method": "joint",
                "sampler_name": "dpmpp_2m_sde_gpu",
                "scheduler_name": "karras",
                "skipping_cn_preprocessor": False,
                "vae_name": "Default (model)"
            },
            "save_meta": True,
            "meta_scheme": "fooocus",
            "save_extension": "png",
            "save_name": "",
            "read_wildcards_in_order": False,
            "require_base64": False,
            "async_process": False,
            "webhook_url": "",
            "uov_method": uov_method,
            "upscale_value": upscale_value,
            "input_image": input_image,
            "image_prompts": []
}
    try:
        response = requests.post(API_URL_UPSCALE, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # # Transform URLs in response
        # for item in data:
        #     if item.get('url'):
        #         item['url'] = transform_url(item['url'])
                
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)