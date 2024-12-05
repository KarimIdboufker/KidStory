from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import base64
from io import BytesIO

# Load Waifu Diffusion model


def load_image_model():
    
    model = "hakurei/waifu-diffusion"
    pipeline = StableDiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16).to("cuda")
    print(f"Loading image model: {model}...")
    print("Image model loaded")
    return pipeline


def generate_images(data, model):
    prompts = [
        f"children's book illustration, kid-friendly, cute art style: {data['characters'][0]} and {data['characters'][1]} in a {data['setting']} setting",
        f"children's book illustration, kid-friendly, cute art style: {data['characters'][0]} and {data['characters'][1]} {data['action']}",
        f"children's book illustration, kid-friendly, cute art style: a fun scene of {data['action']} in a {data['setting']} setting",
        f"children's book illustration, kid-friendly, cute art style: happy ending with {data['characters'][0]} and {data['characters'][1]}: {data['ending']}"
    ]

    encoded_images = []
    for prompt in prompts:
        # Generate image
        image = model(prompt, safety_checker=True).images[0]
        
        # Convert PIL Image to base64 string
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        encoded_images.append(img_str)

    return encoded_images

if __name__ == "__main__":
    model = load_image_model()
    images = generate_images({
        "characters": ["Nael", "Naim"],
        "setting": "Space",
        "action": "fighting",
        "ending": "happy"
    }, model)
    
    # Save the generated images
    for i, image in enumerate(images):
        image_path = f"generated_image_{i+1}.png"
        image.save(image_path)
        print(f"Saved image {i+1} to {image_path}")
