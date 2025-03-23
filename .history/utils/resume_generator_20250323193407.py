from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_resume(name, email, phone, address, skills, education, experience, achievements):
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
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, y, f"🏅 {ach['category']}: {ach['details']}")
        y -= 20
        if y < 50:  # Ensure it doesn't go off-page
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer
