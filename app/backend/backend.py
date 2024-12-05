from fastapi import FastAPI
from models.story import generate_story
from models.image import generate_images

app = FastAPI()

@app.post("/generate_story")
async def generate_story_endpoint(data: dict):
    return generate_story(data)

@app.post("/generate_images")
async def generate_images_endpoint(data: dict):
    return generate_images(data)

@app.get("/health")
async def health_check():
    return {"status": "OK"}
