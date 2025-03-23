from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_resume(name, dob, email, phone, address, skills, education, experience, projects, achievements):
    """
    Generate a PDF resume using user details and achievements.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, f"{name}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Email: {email}")
    pdf.drawString(100, 715, f"Phone: {phone}")
    pdf.drawString(100, 700, f"Address: {address}")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 680, "Skills:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 665, skills)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 645, "Education:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 630, education)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 610, "Experience:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 595, experience)

    # Add achievements
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 575, "Achievements:")

    y = 560
    for ach in achievements:
        if isinstance(ach, dict):  # Ensure it is a dictionary
            title = ach.get("title", "Untitled Achievement")  # Default if title is missing
            description = ach.get("description", "No description available.")  # Default if description is missing
            text = f"🏅 {title}: {description}"
        else:
            text = f"🏅 {ach}"  # Handle unexpected formats

        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, y, text)
        y -= 20

        # Check if the page is full, then create a new page
        if y < 50:
            pdf.showPage()
            y = 750  # Reset position for new page

    pdf.save()
    buffer.seek(0)
    return buffer
