from pix2tex.cli import LatexOCR
from PIL import Image
import io

# Load model once
ocr_model = LatexOCR()

def extract_latex_from_image(image_bytes):
    """Extracts LaTeX from image bytes using Pix2Tex."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    try:
        result = ocr_model(image)
        return result
    except Exception as e:
        print(f"Pix2Tex OCR failed: {e}")
        return ""
