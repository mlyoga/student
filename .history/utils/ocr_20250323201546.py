import cv2
import pytesseract
from PIL import Image
import os

# Set Tesseract path if not automatically detected (for Windows users)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extracts text from a given image using Tesseract OCR."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to load image: {image_path}")

        # Convert to grayscale (improves OCR accuracy)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding for better text detection
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Extract text
        text = pytesseract.image_to_string(gray)
        return text.strip()

    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

if __name__ == "__main__":
    image_path = "certificate.jpg"  # Update this with your image path
    extracted_text = extract_text_from_image(image_path)

    if extracted_text:
        print("\nExtracted Text:\n" + "-"*40)
        print(extracted_text)
        print("-"*40)
    else:
        print("No text detected.")
