import pytesseract
from PIL import Image
import os

# ✅ Set the correct Tesseract path (Windows Example)
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# ✅ Check if Tesseract exists
if not os.path.exists(tesseract_path):
    raise FileNotFoundError(f"Tesseract not found at {tesseract_path}. Please install it.")

# ✅ Function to Extract Text
def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {e}"

# ✅ Test the function (Optional)
if __name__ == "__main__":
    image_path = "test_image.png"  # Change to your image path
    if os.path.exists(image_path):
        img = Image.open(image_path)
        extracted_text = extract_text_from_image(img)
        print("Extracted Text:", extracted_text)
    else:
        print(f"Image not found at {image_path}")
