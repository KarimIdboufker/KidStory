from fastapi import APIRouter
from models.image import generate_images

router = APIRouter()

@router.post("/images")
async def generate_images_route(data: dict):
    return generate_images(data)
