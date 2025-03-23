import cv2
import pytesseract
from PIL import Image
import os

# Set Tesseract path if needed (uncomment and modify below line for Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def main():
    # Image paths (update these paths based on your actual file location)
    images = ["/mnt/data/sih.jpg", "/mnt/data/cit.jpg"]

    for img_path in images:
        if os.path.exists(img_path):
            print(f"\nExtracted Text from {os.path.basename(img_path)}:\n")
            extracted_text = extract_text(img_path)
            print(extracted_text)
        else:
            print(f"File not found: {img_path}")

if __name__ == "__main__":
    main()
