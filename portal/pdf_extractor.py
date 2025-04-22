import fitz  # PyMuPDF
import tempfile
import numpy as np
from PIL import Image
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import re

ocr_model = ocr_predictor(pretrained=True)

def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert("RGB")  # Force RGB
        images.append(np.array(img))  # Convert to numpy array here
    return images


def extract_text_blocks_with_doctr(pdf_path):
    np_images = pdf_to_images(pdf_path)

    # Sanity check
    for i, img in enumerate(np_images):
        print(f"Page {i+1}: type={type(img)}, shape={img.shape}, ndim={img.ndim}")

    result = ocr_model(np_images)

    blocks = []
    for page in result.pages:
        for block in page.blocks:
            block_text = " ".join([word.value for line in block.lines for word in line.words])
            if block_text.strip():
                blocks.append(block_text.strip())
    return blocks





def needs_mathpix(text):
    math_keywords = ['\\', '=', '+', '-', '*', '∑', '∫', '^', '_', '{', '}', '/', 'π', 'θ']
    return any(sym in text for sym in math_keywords) or bool(re.search(r'[a-zA-Z]+\d+', text))