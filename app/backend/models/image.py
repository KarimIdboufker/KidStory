from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
from io import BytesIO
import base64

# Load Waifu Diffusion model (or any other desired model)
def load_image_model():
    model = "hakurei/waifu-diffusion"
    pipeline = StableDiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16).to("cuda")
    print(f"Loading image model: {model}...")
    print("Image model loaded")
    return pipeline

def generate_image_from_paragraph(paragraph, model):
    """
    Generates an image based on a single paragraph.
    """
    # Generate image using the paragraph as a prompt
    image = model(paragraph, safety_checker=True).images[0]
    return image

def generate_images(story_paragraphs, model):
    """
    Generates images for each paragraph in the story and encodes them into base64 format.
    """
    encoded_images = []
    for paragraph in story_paragraphs:
        # Create an illustration-friendly prompt from the paragraph
        prompt = f"children's book illustration, kid-friendly, cute art style: {paragraph}"
        
        # Generate image based on the paragraph
        image = generate_image_from_paragraph(prompt, model)
        
        # Convert the image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Append encoded image to the list
        encoded_images.append(img_str)
    
    return encoded_images

if __name__ == "__main__":
    # Load the image model
    model = load_image_model()
    
    # Example paragraphs from a generated story
    story_paragraphs = [
        "Nael and Naim explored the vast expanse of space in their shiny rocket.",
        "Suddenly, a fierce alien appeared, challenging them to a cosmic duel.",
        "Using their wits, they solved a tricky puzzle to uncover hidden treasure.",
        "Finally, the alien smiled and joined their crew, and they all lived happily ever after."
    ]
    
    # Generate images from the story paragraphs and encode them to base64
    encoded_images = generate_images(story_paragraphs, model)
    
    # Optionally: Save the images locally
    for i, img_str in enumerate(encoded_images):
        image_path = f"generated_image_{i+1}.png"
        img_data = base64.b64decode(img_str)
        with open(image_path, "wb") as img_file:
            img_file.write(img_data)
        print(f"Saved image {i+1} to {image_path}")
    
    print("Generated images are ready for use in the front-end.")
