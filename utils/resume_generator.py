from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io

def generate_resume(name, dob, email, phone, address, skills, education, experience, projects, achievements):
    """
    Generate a structured PDF resume with proper text wrapping and page handling.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title - Name
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 50, name)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, height - 70, f"DOB: {dob}")
    pdf.drawString(100, height - 85, f"Email: {email}")
    pdf.drawString(100, height - 100, f"Phone: {phone}")
    pdf.drawString(100, height - 115, f"Address: {address}")

    y_position = height - 140

    def add_section(title, content):
        """Helper function to add sections with automatic line wrapping and pagination."""
        nonlocal y_position
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, y_position, title)
        y_position -= 20
        pdf.setFont("Helvetica", 12)

        lines = simpleSplit(content, "Helvetica", 12, 400)  # Wrap text
        for line in lines:
            if y_position < 50:  # Check for page overflow
                pdf.showPage()
                y_position = height - 50
                pdf.setFont("Helvetica", 12)
            pdf.drawString(100, y_position, line)
            y_position -= 15

        y_position -= 10  # Extra spacing

    # Adding sections
    add_section("Skills:", skills)
    add_section("Education:", education)
    add_section("Experience:", experience)
    add_section("Projects:", projects)

    # Achievements Section
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, y_position, "Achievements:")
    y_position -= 20
    pdf.setFont("Helvetica", 12)

    if not achievements.strip():
        pdf.drawString(100, y_position, "No achievements added yet.")
        y_position -= 20
    else:
        for ach in achievements.split("\n"):
            text = f"🏅 {ach.strip()}"  # Add bullet point
            lines = simpleSplit(text, "Helvetica", 12, 400)

            for line in lines:
                if y_position < 50:  # New page if needed
                    pdf.showPage()
                    y_position = height - 50
                    pdf.setFont("Helvetica", 12)
                pdf.drawString(100, y_position, line)
                y_position -= 15

            y_position -= 10  # Extra spacing

    pdf.save()
    buffer.seek(0)
    return buffer

