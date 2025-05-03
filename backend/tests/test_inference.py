# backend/tests/test_inference.py
import io
import pytest
from PIL import Image
import requests  # or use flask testing client

# If testing locally, one might use the requests library against a running server.
# Alternatively, use Flask's test_client. Here we use requests for simplicity.

@pytest.fixture(scope="module")
def test_image_bytes():
    # Create a small test image (e.g., 16x16 black image)
    img = Image.new('RGB', (16, 16), color='blue')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def test_upscale_endpoint(test_image_bytes):
    # Assume the Flask server is running on localhost:5000
    url = "http://localhost:5000/upscale"
    files = {'image': ('test.png', test_image_bytes, 'image/png')}
    response = requests.post(url, files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert 'image' in data
    b64_str = data['image']
    # The response should be a base64 string; check a bit of it
    assert b64_str.startswith('iVBOR')  # PNG files start with 'iVBORw0KG...'
