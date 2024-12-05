import pytest
from models.story import generate_story, load_story_model

def test_load_story_model():
    model = load_story_model()
    assert model is not None

def test_generate_story():
    test_data = {
        "characters": ["Alice", "Bob"],
        "setting": "magical forest",
        "action": "searching for treasure",
        "ending": "they found a magical gem"
    }
    
    story = generate_story(test_data)
    assert isinstance(story, str)
    assert len(story) > 0
    # Check if key elements are present in the story
    assert any(char in story for char in test_data["characters"])
    assert test_data["setting"] in story.lower()

if __name__ == "__main__":
    generate_story({
        "characters": ["Alice", "Bob"],
        "setting": "forest",
        "action": "running",
        "ending": "happy"
    })