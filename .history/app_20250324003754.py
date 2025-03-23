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

# 🎨 Set Streamlit Page Config
st.set_page_config(page_title="Student Portfolio", page_icon="📜", layout="wide")

# ✅ Set Tesseract Path Based on OS
if os.name == "nt":  # Windows
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # Linux
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ✅ Check if Tesseract Exists
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    st.error(f"⚠ Tesseract not found at {pytesseract.pytesseract.tesseract_cmd}. Please install it.")
    st.stop()

# 🎉 App Title
st.title("📜 Student Digital Portfolio & Resume Generator")

# 🔑 Authentication System
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated:
    st.header("🔑 Login")
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("✅ Logged in successfully!")
            st.rerun()  # ✅ Redirect after login
        else:
            st.error("❌ Invalid username or password.")
    st.stop()

# 📌 Sidebar Navigation
st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
page = st.sidebar.radio(
    "📌 Navigate",
    ["🏠 Home", "📄 Resume Generator", "🎟 Event Recommendations", "📂 Digital Portfolio"]
)

# 🖼 Function to Extract Images from PDF
def extract_images_from_pdf(pdf_file):
    images = []
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            for img in page.get_images(full=True):
                base_image = pdf_document.extract_image(img[0])
                images.append(Image.open(io.BytesIO(base_image["image"])))
    except Exception as e:
        st.error(f"⚠ Error extracting images from PDF: {e}")
    return images

# 📂 **Digital Portfolio (With Certificates)**
if page == "📂 Digital Portfolio":
    st.header("📂 My Digital Portfolio")

    st.subheader("👤 My Details")
    name = st.text_input("👤 Name", value=st.session_state.username)
    email = st.text_input("📧 Email", value="your.email@example.com")
    phone = st.text_input("📞 Phone", value="Your Phone Number")
    address = st.text_area("🏠 Address", value="Your Address")

    st.subheader("🎓 Education & Work")
    education = st.text_area("📚 Education", value="Your Education Details")
    work_experience = st.text_area("💼 Work Experience", value="Your Work Experience Details")

    st.subheader("🏆 Achievements")
    achievements = get_achievements(st.session_state.username)
    if achievements:
        for idx, achievement in enumerate(achievements):
            if isinstance(achievement, dict) and "text" in achievement:
                st.write(f"📌 **{idx + 1}:** {achievement['text']}")
    else:
        st.warning("⚠ No achievements added yet.")

    # 📜 Certificates (Displays Uploaded Ones!)
    st.subheader("📜 Certificates")
    saved_certificates = get_achievements(st.session_state.username)
    if saved_certificates:
        for idx, cert in enumerate(saved_certificates):
            if isinstance(cert, dict) and "text" in cert:
                st.write(f"🏅 **Certificate {idx + 1}:** {cert['text']}")
    else:
        st.warning("⚠ No certificates uploaded yet.")

    if st.button("💾 Save Profile"):
        st.success("✅ Profile Updated Successfully!")

# 📄 **Resume Generator**
elif page == "📄 Resume Generator":
    st.header("📑 Resume Generator")

    name = st.text_input("👤 Full Name")
    dob = st.date_input("📅 Date of Birth", min_value=datetime.date(1995, 1, 1))
    email = st.text_input("📧 Email")
    phone = st.text_input("📞 Phone Number")
    address = st.text_area("🏠 Address")
    skills = st.text_area("🛠 Skills (comma-separated)")
    education = st.text_area("🎓 Education Details")
    experience = st.text_area("💼 Work Experience")
    user_achievements = st.text_area("🏆 Achievements (comma-separated)")

    saved_achievements = get_achievements(st.session_state.username)
    all_achievements = "\n".join(
        [f"• {ach['text']}" for ach in saved_achievements if isinstance(ach, dict) and "text" in ach]
    ) if saved_achievements else "No achievements added yet."

    if st.button("📜 Generate Resume"):
        resume_pdf = generate_resume(
            name, dob, email, phone, address, skills, education, experience, all_achievements
        )

        if isinstance(resume_pdf, io.BytesIO):
            st.download_button(label="📥 Download Resume", data=resume_pdf.getvalue(), file_name="resume.pdf", mime="application/pdf")
        else:
            st.error("⚠ Resume generation failed.")

# 🎟 **Event Recommendations**
elif page == "🎟 Event Recommendations":
    st.header("🎭 Recommended Events for You")
    interests = st.text_input("🎯 Enter your interests (comma-separated)")

    if st.button("🔍 Get Recommendations"):
        if interests.strip():
            recommended_events = recommend_events(interests)
            if recommended_events:
                for event in recommended_events:
                    st.write(f"📍 {event}")
            else:
                st.warning("⚠ No matching events found.")
        else:
            st.warning("⚠ Please enter at least one interest.")

# 🏠 **Home - Upload Certificates (Saves to Portfolio)**
elif page == "🏠 Home":
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
                st.write(f"📝 **Extracted Text {idx + 1}:** {text}")
                if st.button(f"➕ Save Certificate {idx + 1}", key=f"save_{idx}"):
                    save_achievement(st.session_state.username, f"Certificate {idx + 1}", text)
                    st.success(f"✅ Certificate {idx + 1} Saved! Refresh Portfolio to View.")
                    st.rerun()  # ✅ Certificates appear instantly in Portfolio

        except Exception as e:
            st.error(f"⚠ Error processing file: {e}")


