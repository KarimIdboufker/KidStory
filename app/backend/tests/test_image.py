import pytest
from models.image import generate_images, load_image_model
from PIL import Image

def test_load_image_model():
    model = load_image_model()
    assert model is not None

def test_generate_images():
    test_data = {
        "characters": ["Alice", "Bob"],
        "setting": "magical forest",
        "action": "searching for treasure",
        "ending": "they found a magical gem"
    }
    
    model = load_image_model()
    images = generate_images(test_data, model)
    
    assert isinstance(images, list)
    assert len(images) == 4  # Should generate 4 images
    for img in images:
        assert isinstance(img, Image.Image)

if __name__ == "__main__":
    model = load_image_model()
    generate_images({
        "characters": ["Alice", "Bob"],
        "setting": "forest",
        "action": "running",
        "ending": "happy"
    }, model)