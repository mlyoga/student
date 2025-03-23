import cv2
import pytesseract
import re

# Set Tesseract path if needed (Windows users only)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extracts text from a certificate image using Tesseract OCR."""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to load image: {image_path}")

        # Convert to grayscale (improves OCR accuracy)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding for better text extraction
        processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Extract text using Tesseract
        extracted_text = pytesseract.image_to_string(processed_img)
        return extracted_text.strip()

    except Exception as e:
        return f"Error processing {image_path}: {str(e)}"

def extract_certificate_details(image_path):
    """Extracts key certificate details such as recipient, event name, organization, platform, and partners."""
    text = extract_text_from_image(image_path)

    details = {
        "Recipient": None,
        "Event": None,
        "Organization": None,
        "Platform": None,
        "Partners": None
    }

    # Define keyword patterns
    recipient_pattern = r"(?i)awarded to\s*([\w\s]+)"
    event_pattern = r"(?i)for\s*([\w\s]+)"
    organization_pattern = r"(?i)organized by\s*([\w\s]+)"
    platform_pattern = r"(?i)platform\s*([\w\s]+)"
    partners_pattern = r"(?i)in partnership with\s*([\w\s,]+)"

    # Extract information using regex
    recipient_match = re.search(recipient_pattern, text)
    event_match = re.search(event_pattern, text)
    organization_match = re.search(organization_pattern, text)
    platform_match = re.search(platform_pattern, text)
    partners_match = re.search(partners_pattern, text)

    if recipient_match:
        details["Recipient"] = recipient_match.group(1).strip()
    if event_match:
        details["Event"] = event_match.group(1).strip()
    if organization_match:
        details["Organization"] = organization_match.group(1).strip()
    if platform_match:
        details["Platform"] = platform_match.group(1).strip()
    if partners_match:
        details["Partners"] = partners_match.group(1).strip()

    return details

def main():
    """Test the OCR on a sample certificate image."""
    image_path = "/mnt/data/certificate.jpg"  # Update with actual path

    print(f"\nProcessing: {image_path}")
    details = extract_certificate_details(image_path)

    print("\nExtracted Certificate Details:")
    print("-" * 40)
    for key, value in details.items():
        print(f"{key}: {value if value else 'Not found'}")
    print("-" * 40)

if __name__ == "__main__":
    main()
