from diffusers import StableDiffusionPipeline
import torch

# Load Waifu Diffusion model


def load_image_model():
    
    model = "hakurei/waifu-diffusion"
    pipeline = StableDiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16).to("cuda")
    print(f"Loading image model: {model}...")
    print("Image model loaded")
    return pipeline


def generate_images(data, model):

    prompts = [
        f"{data['characters'][0]} and {data['characters'][1]} in a {data['setting']} setting.",
        f"{data['characters'][0]} and {data['characters'][1]} {data['action']}.",
        f"An exciting moment of {data['action']} in a {data['setting']} setting.",
        f"Ending scene with {data['characters'][0]} and {data['characters'][1]}: {data['ending']}."
    ]

    images = []
    for prompt in prompts:
        image = model(prompt).images[0]  # Generate one image per prompt
        images.append(image)

    return images
