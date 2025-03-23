import pytesseract
from PIL import Image

# Set the correct Tesseract path (Windows example)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

