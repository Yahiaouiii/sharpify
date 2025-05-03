# backend/cartoonify.py
import cv2
import numpy as np
from PIL import Image

def cartoonify_image(pil_img: Image.Image) -> Image.Image:
    img = np.array(pil_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Apply bilateral filter to smooth colors
    color = cv2.bilateralFilter(img, d=9, sigmaColor=200, sigmaSpace=200)

    # Convert to grayscale and apply median blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)

    # Detect edges and combine with color image
    edges = cv2.adaptiveThreshold(blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)

    # Convert edges to color
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Combine edges with smoothed color image
    cartoon = cv2.bitwise_and(color, edges_colored)

    # Convert back to RGB and PIL
    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cartoon_rgb)
