import pytesseract
from PIL import Image

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)
