import cv2
import pytesseract
import os

# Set Tesseract path if needed (Windows users only)
# Uncomment and modify this line if Tesseract is not found automatically
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_path):
    """Extracts text from an image using Tesseract OCR."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to load image: {image_path}")

        # Convert to grayscale (improves OCR accuracy)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Optional: Apply thresholding for better text detection
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Extract text
        text = pytesseract.image_to_string(gray)
        return text.strip()

    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

def main():
    """Main function to extract text from a list of images."""
    print("\nOCR module loaded successfully.")
    print("Functions available:", dir())

    # Image paths (update these paths based on your actual file location)
    images = ["/mnt/data/sih.jpg", "/mnt/data/cit.jpg"]

    for img_path in images:
        print(f"\nProcessing: {os.path.basename(img_path)}")
        extracted_text = extract_text(img_path)
        
        if extracted_text:
            print(f"\nExtracted Text:\n{'-'*40}\n{extracted_text}\n{'-'*40}")
        else:
            print("No text detected.")

if __name__ == "__main__":
    main()

