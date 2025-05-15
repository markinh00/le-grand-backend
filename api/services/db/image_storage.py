import os
import uuid
from urllib.parse import urlparse

from fastapi import UploadFile


IMAGE_DIR = os.getenv("IMAGE_DIR")

protected_img = [
    "572cb3da-e0d7-4849-afca-3bb7c4be24f6.jpeg",
    "75804a10-0407-478d-9cc0-384960dd55a0.jpg",
    "ca00107e-4498-4e6a-9567-bc6ebed9a2f5.jpg",
    "fc99b584-0b45-4b3f-aa7b-f1ed50e40031.jpg",
    "cee3f6f9-4fc3-4c82-a22d-aaf4828b9cc7.jpg",
    "845b25f1-a7bf-4d89-aab8-17a068b51943.jpg",
    "default-placeholder.png"
]

def upload_image(img_file: UploadFile) -> str | None:
    try:
        os.makedirs(IMAGE_DIR, exist_ok=True)

        file_extension = os.path.splitext(img_file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        image_path = os.path.join(IMAGE_DIR, unique_filename)

        content = img_file.file.read()

        with open(image_path, "wb") as f:
            f.write(content)

        return f"http://localhost:8000/image/{unique_filename}"
    except Exception as e:
        print(e)
        return None


def delete_image(image_url: str) -> bool:
    try:
        path = urlparse(image_url).path
        filename = os.path.basename(path)

        image_path = os.path.join(IMAGE_DIR, filename)

        if not os.path.exists(image_path):
                print(f"File not found: {image_path}")
                return False

        if not filename in protected_img:
            os.remove(image_path)
        return True
    except Exception as e:
        print(e)
        return False

