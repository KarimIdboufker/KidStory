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
        story = generate_story(data, app.state.story_model)
        return {"status": "success", "pages": story}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_images")
async def generate_images_endpoint(data: dict):
    try:
        images = generate_images(data, app.state.image_model)
        return {"status": "success", "images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "OK"}
