import mimetypes
import os
from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse


IMAGE_DIR = os.getenv("IMAGE_DIR")

router = APIRouter(prefix="/image", tags=["Image"])

@router.get("/{img_id}")
def get_image_by_id(img_id: str):
    image_path = f'{IMAGE_DIR}/{img_id}'

    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="image not found"
        )

    mime_type, _ = mimetypes.guess_type(image_path)
    return FileResponse(image_path, media_type=mime_type or "application/octet-stream")