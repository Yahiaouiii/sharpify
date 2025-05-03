# backend/model.py
import os
import torch
from collections import OrderedDict
from PIL import Image
from torchvision.transforms import ToTensor, ToPILImage
import numpy as np
import cv2

# Path to the model weights
MODEL_PATH = "models/RRDB_ESRGAN_x4.pth"

def load_model():
   
    # Import the RRDBNet architecture from BasicSR
    from basicsr.archs.rrdbnet_arch import RRDBNet

    # Instantiate the network
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3,
        num_feat=64, num_block=23,
        num_grow_ch=32, scale=4
    )

    # Load the checkpoint
    ckpt = torch.load(MODEL_PATH, map_location='cpu')

    # Extract the state dict from potential nested keys
    if 'params_ema' in ckpt:
        state_dict = ckpt['params_ema']
    elif 'network_g' in ckpt:
        state_dict = ckpt['network_g']
    elif 'params' in ckpt:
        state_dict = ckpt['params']
    elif 'state_dict' in ckpt:
        state_dict = ckpt['state_dict']
    else:
        state_dict = ckpt  # assume entire dict IS the state_dict

    # Strip "module." prefixes if present
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[len('module.'):] if k.startswith('module.') else k
        new_state_dict[name] = v

    # Load weights non-strictly to ignore any mismatch
    missing, unexpected = model.load_state_dict(new_state_dict, strict=False)
    print(f">>> Loaded ESRGAN weights with {len(missing)} missing and {len(unexpected)} unexpected keys")

    model.eval()
    return model

# Keep a single copy of the loaded model in memory
_esrgan_model = None
def get_model():
    global _esrgan_model
    if _esrgan_model is None:
        _esrgan_model = load_model()
    return _esrgan_model

def upscale_image(pil_img: Image.Image) -> Image.Image:
    """
    Upscale a PIL image using RRDB-ESRGAN ×4 and return a new PIL image
    with correct color (RGB) and gamma correction.
    """
    model = get_model()

    # 1. Ensure RGB and convert to numpy
    pil_img = pil_img.convert("RGB")
    img = np.array(pil_img).astype(np.float32) / 255.0  # HWC, RGB, [0,1]

    # 2. sRGB → linear
    img = np.power(img, 2.2)

    # 3. HWC → CHW
    img = np.transpose(img, (2, 0, 1))

    # 4. To Tensor
    img_tensor = torch.from_numpy(img).unsqueeze(0).float()

    # 5. Inference
    with torch.no_grad():
        output = model(img_tensor).squeeze(0).clamp(0, 1)

    # 6. CHW → HWC
    output = output.cpu().numpy()
    output = np.transpose(output, (1, 2, 0))  # still RGB

    # 7. linear → sRGB
    output = np.power(output, 1.0 / 2.2)
    output = np.clip(output, 0.0, 1.0)

    # 8. Back to uint8 PIL
    output = (output * 255.0).round().astype(np.uint8)
    return Image.fromarray(output)





