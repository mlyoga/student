import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io
import datetime
import os
import pytesseract
from utils.ocr import extract_text_from_image
from utils.resume_generator import generate_resume
from utils.recommender import recommend_events
from utils.database import save_achievement, get_achievements
from utils.auth import authenticate_user

# ✅ Automatically Set Tesseract Path Based on OS
if os.name == "nt":  # Windows
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # Linux
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# 🎉 Streamlit App Title
st.title("📜 Student Achievement Tracker")

# 🔑 Initialize Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# 🔐 User Authentication
if not st.session_state.authenticated:
    st.header("🔑 Login")
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid username or password.")
    st.stop()

# 📌 Sidebar Navigation
st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
page = st.sidebar.radio(
    "📌 Navigate",
    ["🏠 Home", "📄 Resume Generator", "🎟 Event Recommendations", "📂 Digital Portfolio"]
)

# 🏠 **Home Page - Upload Certificates**
if page == "🏠 Home":
    st.header("🎉 Upload Certificates")
    uploaded_file = st.file_uploader("📂 Upload a certificate", type=["jpg", "png", "pdf"])

    if uploaded_file:
        extracted_texts = []
        try:
            if uploaded_file.type.startswith("image/"):
                image = Image.open(uploaded_file)
                st.image(image, caption="🖼 Uploaded Certificate", use_container_width=True)
                extracted_texts.append(extract_text_from_image(image))

            elif uploaded_file.type == "application/pdf":
                images = extract_images_from_pdf(uploaded_file)
                for idx, image in enumerate(images):
                    st.image(image, caption=f"📄 Page {idx + 1}", use_container_width=True)
                    extracted_texts.append(extract_text_from_image(image))
            
            for idx, text in enumerate(extracted_texts):
                st.write(f"📝 **Extracted Text {idx + 1}:**", text)
                if st.button(f"➕ Save Certificate {idx + 1}", key=f"save_{idx}"):
                    save_achievement(st.session_state.username, f"Certificate {idx + 1}", text)
                    st.success(f"✅ Certificate {idx + 1} Saved!")
        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")

# 📄 **Resume Generator**
elif page == "📄 Resume Generator":
    st.header("📑 Resume Generator")

    # 📝 User Inputs
    name = st.text_input("Full Name")
    dob = st.date_input("📅 Date of Birth", min_value=datetime.date(1995, 1, 1))
    email = st.text_input("📧 Email")
    phone = st.text_input("📞 Phone Number")
    address = st.text_area("🏠 Address")
    skills = st.text_area("🛠 Skills (comma-separated)")
    education = st.text_area("🎓 Education Details")
    experience = st.text_area("💼 Work Experience")
    projects = st.text_area("🚀 Projects (comma-separated)")
    user_achievements = st.text_area("🏆 Achievements (comma-separated)")

    # 🎖 Fetch Saved Achievements
    saved_achievements = get_achievements(st.session_state.username)
    all_achievements_list = []

    if saved_achievements:
        all_achievements_list.extend(
            [ach["text"] for ach in saved_achievements if isinstance(ach, dict) and "text" in ach]
        )

    if user_achievements.strip():
        all_achievements_list.extend(user_achievements.split(","))

    all_achievements = "\n".join([f"• {ach.strip()}" for ach in all_achievements_list]) if all_achievements_list else "No achievements added yet."

    if st.button("📜 Generate Resume"):
        resume_pdf = generate_resume(
            name=name,
            dob=dob,
            email=email,
            phone=phone,
            address=address,
            skills=skills,
            education=education,
            experience=experience,
            projects=projects,
            achievements=all_achievements
        )

        if isinstance(resume_pdf, io.BytesIO):  # Ensure correct object type
            st.write("📃 **Generated Resume:**")
            st.download_button(
                label="📥 Download Resume",
                data=resume_pdf.getvalue(),
                file_name="resume.pdf",
                mime="application/pdf"
            )
        else:
            st.error("⚠️ Resume generation failed. Please check the input.")

# 📟 **Digital Portfolio - My Details & Achievements**
elif page == "📂 Digital Portfolio":
    st.header("📂 My Digital Portfolio")
    
    # 🔹 User Details Section
    st.subheader("👤 My Details")
    st.write(f"**👤 Name:** {st.session_state.username}")
    st.write(f"**📧 Email:** [Your Email Here]")
    st.write(f"**📞 Phone:** [Your Phone Number Here]")
    st.write(f"**🏠 Address:** [Your Address Here]")

    # 🎓 **Education & Work**
    st.subheader("🎓 Education & Work")
    st.write("📚 **Education:** [Your Education Details Here]")
    st.write("💼 **Work Experience:** [Your Work Experience Details Here]")

    # 🏆 **Achievements**
    st.subheader("🏆 Achievements")
    achievements = get_achievements(st.session_state.username)
    if achievements:
        for idx, achievement in enumerate(achievements):
            if isinstance(achievement, dict) and "text" in achievement:
                st.write(f"📌 **{idx + 1}:** {achievement['text']}")
    else:
        st.warning("⚠️ No achievements added yet.")

    # 🚀 **Projects**
    st.subheader("🚀 Projects")
    st.write("📌 **Project 1:** [Your Project Details Here]")
    st.write("📌 **Project 2:** [Your Project Details Here]")

    # 📜 **Certificates**
    st.subheader("📜 Certificates")
    st.write("🏅 **Certificate 1:** [Certificate Name Here]")
    st.write("🏅 **Certificate 2:** [Certificate Name Here]")

    # 📥 **Resume Download**
    st.subheader("📥 My Resume")
    st.write("Download your resume from the **Resume Generator** section.")

