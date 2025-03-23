import easyocr

# ✅ Initialize EasyOCR Reader
reader = easyocr.Reader(["en"])  # Language: English

def extract_text_from_image(image):
    """
    Extract text from an image using EasyOCR.
    :param image: PIL Image object
    :return: Extracted text as a string
    """
    try:
        text = reader.readtext(image, detail=0)  # Extract text without bounding box details
        return " ".join(text)  # Join the text list into a single string
    except Exception as e:
        return f"Error extracting text: {e}"

# ✅ Test the function (Optional)
if __name__ == "__main__":
    image_path = "test_image.png"  # Change to your image path
    try:
        from PIL import Image
        img = Image.open(image_path)
        extracted_text = extract_text_from_image(img)
        print("Extracted Text:", extracted_text)
    except FileNotFoundError:
        print(f"⚠ Image not found at {image_path}")
