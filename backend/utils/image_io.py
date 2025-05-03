# backend/utils/image_io.py
from io import BytesIO
from base64 import b64encode
from PIL import Image

def pil_to_base64(img: Image.Image) -> str:
    """
    Convert a PIL Image to a base64 string (PNG format).
    """
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return b64encode(img_bytes).decode('utf-8')

def base64_to_pil(b64str: str) -> Image.Image:
    """
    Convert a base64 string to a PIL Image.
    """
    img_data = BytesIO(b64encode(b64str.encode('utf-8')))
    img = Image.open(img_data)
    return img
