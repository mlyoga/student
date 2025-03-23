from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
import io

def wrap_text(text, width=80):
    """Wrap text to fit within the page width."""
    return "\n".join(textwrap.wrap(text, width))

def generate_resume(name, dob, email, phone, address, skills, education, experience, projects, achievements):
    """
    Generate a professional PDF resume with improved formatting and text wrapping.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # Header (Name & Contact Details)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, name)

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"🎂 DOB: {dob}")
    pdf.drawString(100, 715, f"📧 Email: {email}")
    pdf.drawString(100, 700, f"📞 Phone: {phone}")
    pdf.drawString(100, 685, f"🏠 Address: {wrap_text(address, 60)}")

    # Sections Formatting with bullet points
    y = 660
    sections = [
        ("Skills", skills.split(",")),  
        ("Education", education.split(",")),  
        ("Experience", experience.split(",")),  
        ("Projects", projects.split(",")),  
    ]

    pdf.setFont("Helvetica-Bold", 14)
    
    for title, content in sections:
        pdf.drawString(100, y, f"{title}:")
        y -= 20
        pdf.setFont("Helvetica", 12)

        for item in content:
            pdf.drawString(110, y, f"• {wrap_text(item.strip(), 80)}")
            y -= 20  
            if y < 50:  
                pdf.showPage()
                y = 750
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, y, f"{title} (contd.):")
                y -= 20
                pdf.setFont("Helvetica", 12)

        y -= 10
        pdf.setFont("Helvetica-Bold", 14)

    # Achievements Section
    pdf.drawString(100, y, "Achievements:")
    y -= 20

    pdf.setFont("Helvetica", 12)
    for ach in achievements:
        pdf.drawString(110, y, f"🏆 {ach['category']}: {wrap_text(ach['details'], 80)}")
        y -= 20
        if y < 50:  
            pdf.showPage()
            y = 750
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(100, y, "Achievements (contd.):")
            y -= 20
            pdf.setFont("Helvetica", 12)

    pdf.save()
    buffer.seek(0)
    return buffer

