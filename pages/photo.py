import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
from font_hanken_grotesk import HankenGroteskMedium

_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(_DIR, '..', 'photos')
RESOLUTION = (600, 448)
SATURATION = 0.5

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.jfif')


def create_image():
    photos = []
    if os.path.isdir(PHOTOS_DIR):
        photos = [
            f for f in os.listdir(PHOTOS_DIR)
            if f.lower().endswith(SUPPORTED_EXTENSIONS)
        ]

    if not photos:
        img = Image.new('RGB', RESOLUTION, (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(HankenGroteskMedium, 32)
        text = "No photos found"
        _, _, tw, th = font.getbbox(text)
        draw.text(((RESOLUTION[0] - tw) // 2, (RESOLUTION[1] - th) // 2), text, fill=(0, 0, 0), font=font)
        return img

    photo_path = os.path.join(PHOTOS_DIR, random.choice(photos))
    img = Image.open(photo_path).convert('RGB')
    img = ImageOps.pad(img, RESOLUTION, color=(0, 0, 0))
    return img
