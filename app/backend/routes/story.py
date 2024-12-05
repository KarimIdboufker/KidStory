from fastapi import APIRouter
from models.story import generate_story

router = APIRouter()

@router.post("/story")
async def generate_story_route(data: dict):
    return generate_story(data)
