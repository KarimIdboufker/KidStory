from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from models.story import generate_story, load_story_model
from models.image import generate_images, load_image_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    app.state.story_model = load_story_model()
    app.state.image_model = load_image_model()
    yield
    # Clean up resources if needed

app = FastAPI(lifespan=lifespan)

@app.post("/generate_story")
async def generate_story_endpoint(data: dict):
    try:
        story_parts = generate_story(
            characters=data["characters"],
            environment=data["setting"],
            action=data["action"],
            ending=data["ending"]
        )
        # Format story parts into pages format expected by frontend
        pages = [{"text": text, "index": i} for i, text in enumerate(story_parts)]
        return {"status": "success", "pages": pages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_images")
async def generate_images_endpoint(data: dict):
    try:
        # Extract story_paragraphs from the data dictionary
        story_paragraphs = data.get("story_paragraphs", [])
        # Add illustration-friendly prefixes to each paragraph
        image_prompts = [
            f"children's book illustration style: {paragraph}" 
            for paragraph in story_paragraphs
        ]
        images = generate_images(image_prompts, app.state.image_model)
        return {"status": "success", "images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "OK"}
