import pytesseract
import re
from PIL import Image

# Set the correct Tesseract path (Windows example)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image):
    """
    Extracts text from an image and identifies certificate details:
    - Certificate Name
    - Date
    - Organization
    - Location
    """
    extracted_text = pytesseract.image_to_string(image)

    # Regular expressions for pattern matching
    date_pattern = r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b"
    org_pattern = r"(?i)\b(organized|issued|certified by|conducted by)\s*[:\-]?\s*([A-Za-z\s&]+)"
    location_pattern = r"\b(?:[A-Z][a-z]+\s*){1,3},?\s*(?:[A-Z]{2,3})?\b"
    
    # Extracting fields
    date_match = re.findall(date_pattern, extracted_text)
    org_match = re.search(org_pattern, extracted_text)
    location_match = re.findall(location_pattern, extracted_text)

    # Identifying the certificate name (Assuming the first prominent capitalized phrase is the title)
    lines = extracted_text.split("\n")
    certificate_name = next((line.strip() for line in lines if line.isupper() and len(line.split()) > 1), "Unknown Certificate")

    # Extract results
    certificate_details = {
        "Certificate Name": certificate_name,
        "Date": date_match[0] if date_match else "Not Found",
        "Organization": org_match.group(2) if org_match else "Not Found",
        "Location": location_match[0] if location_match else "Not Found"
    }

    return certificate_details
