from resume_generator import generate_resume  # Import function

# Sample data for testing
name = "M.L. Yogavarshini"
dob = "15 March 2002"
email = "yogavarshini@example.com"
phone = "+91 9876543210"
address = "Chennai, Tamil Nadu, India"
skills = "Python, Machine Learning, Power Electronics, Fusion 360, Arduino"
education = "B.Tech in Electrical Engineering, Panimalar Engineering College, 2024"
experience = "Intern at AAI, Intern at CMRL"
projects = "SAR Image Colorization, EV Cleaning Vehicle, Aerospace Component Redesign"

# Ensure this section exists!
achievements = [
    {"category": "Hackathon", "details": "Finalist in SIH 2024"},
    {"category": "Research", "details": "Presented a paper on AI in medical imaging"},
    {"category": "Leadership", "details": "Led a team at Karnataka Hackathon 2024"},
]

# Ensure all arguments are passed correctly
resume_pdf = generate_resume(name, dob, email, phone, address, skills, education, experience, projects, achievements)

# Save the PDF file
with open("Resume.pdf", "wb") as f:
    f.write(resume_pdf.getbuffer())

print("Resume generated successfully!")
