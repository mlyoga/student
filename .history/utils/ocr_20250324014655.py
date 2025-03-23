import pytesseract
from PIL import Image
import os

# ✅ Dynamically Set Tesseract Path Based on OS
if os.name == "nt":  # Windows
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # Linux/MacOS (Streamlit Cloud, Ubuntu)
    tesseract_paths = ["/usr/bin/tesseract", "/usr/local/bin/tesseract"]
    tesseract_path = None
    for path in tesseract_paths:
        if os.path.exists(path):
            tesseract_path = path
            break

if not tesseract_path or not os.path.exists(tesseract_path):
    raise FileNotFoundError("⚠ Tesseract is not installed! Please install `tesseract-ocr`.")

pytesseract.pytesseract.tesseract_cmd = tesseract_path

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
        print(f"⚠ Image not found at {image_path}")

