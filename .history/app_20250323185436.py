import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io
import os
from utils.ocr import extract_text_from_image
from utils.resume_generator import generate_resume
from utils.recommender import recommend_events
from utils.database import save_achievement, get_achievements, save_rating, get_ratings
from utils.auth import authenticate_user

st.title("📜 Student Achievement Tracker")

# Initialize Session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# User Authentication
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

# Sidebar Navigation
st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
page = st.sidebar.radio("📌 Navigate", ["🏠 Home", "📁 Portfolio", "📄 Resume Generator", "🎟 Event Recommendations"])

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
        st.error(f"⚠️ Error extracting images from PDF: {e}")
    return images

if page == "🏠 Home":
    st.header("🎉 Upload Certificates")
    uploaded_file = st.file_uploader("📂 Upload a certificate", type=["jpg", "png", "pdf"])
    
    if uploaded_file:
        if uploaded_file.type.startswith("image/"):
            image = Image.open(uploaded_file)
            st.image(image, caption="🖼 Uploaded Certificate", use_column_width=True)
            extracted_text = extract_text_from_image(image)
            st.write("📝 Extracted Text:", extracted_text)

            if st.button("➕ Add to Portfolio"):
                save_achievement(st.session_state.username, "Certificate", extracted_text)
                st.success("✅ Added!")
        
        elif uploaded_file.type == "application/pdf":
            images = extract_images_from_pdf(uploaded_file)
            for idx, image in enumerate(images):
                st.image(image, caption=f"📄 Page {idx + 1}", use_column_width=True)
                extracted_text = extract_text_from_image(image)
                st.write(f"📝 Extracted Text from Page {idx + 1}:", extracted_text)

                if st.button(f"➕ Add Page {idx + 1} to Portfolio"):
                    save_achievement(st.session_state.username, f"Certificate Page {idx + 1}", extracted_text)
                    st.success(f"✅ Added!")

elif page == "📄 Resume Generator":
    st.header("📑 Resume Generator")

    st.subheader("📝 Enter Personal Details")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")
    skills = st.text_area("Skills (comma-separated)")
    education = st.text_area("Education Details")
    experience = st.text_area("Work Experience")

    if st.button("📜 Generate Resume"):
        achievements = get_achievements(st.session_state.username)
        resume_pdf = generate_resume(name, email, phone, address, skills, education, experience, achievements)
        
        if resume_pdf:
            resume_bytes = io.BytesIO(resume_pdf)
            st.write("📃 **Generated Resume:**")
            st.download_button(
                label="📥 Download Resume",
                data=resume_bytes,
                file_name="resume.pdf",
                mime="application/pdf"
            )
        else:
            st.error("⚠️ Resume generation failed. Please check the input.")

elif page == "🎟 Event Recommendations":
    st.header("🎭 Recommended Events for You")
    interests = st.text_input("Enter your interests (comma-separated)")
    if st.button("🔍 Get Recommendations"):
        events = recommend_events(interests)
        if events:
            for event in events:
                st.write(f"🎯 {event}")
        else:
            st.warning("⚠️ No events found matching your interests.")
