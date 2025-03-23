import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io
import datetime
from utils.ocr import extract_text_from_image
from utils.resume_generator import generate_resume
from utils.recommender import recommend_events
from utils.database import save_achievement, get_achievements
from utils.auth import authenticate_user

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
    ["🏠 Home", "📄 Resume Generator", "🎟 Event Recommendations", "📂 Portfolio"]
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
        st.error(f"⚠️ Error extracting images from PDF: {e}")
    return images

# 🏠 **Home Page - Upload Certificates**
if page == "🏠 Home":
    st.header("🎉 Upload Certificates")
    uploaded_file = st.file_uploader("📂 Upload a certificate", type=["jpg", "png", "pdf"])

    if uploaded_file:
        extracted_texts = []

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

    if st.button("📜 Generate Resume"):
        achievements = get_achievements(st.session_state.username) or []resume_pdf = generate_resume(name, dob, email, phone, address, skills, education, experience, projects, achievements)
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

# 🎟 **Event Recommendations**
elif page == "🎟 Event Recommendations":
    st.header("🎭 Recommended Events for You")
    interests = st.text_input("🎯 Enter your interests (comma-separated)")

    if st.button("🔍 Get Recommendations"):
        events = recommend_events(interests)
        if events:
            for event in events:
                st.write(f"🎯 {event}")
        else:
            st.warning("⚠️ No events found matching your interests.")

# 📂 **Portfolio**
elif page == "📂 Portfolio":
    st.header("📂 Your Portfolio")
    st.write("🚀 Showcase your achievements, certificates, and projects here.")

    achievements = get_achievements(st.session_state.username)
    if achievements:
        for idx, achievement in enumerate(achievements):
            st.write(f"📌 **Achievement {idx + 1}:** {achievement}")
    else:
        st.warning("⚠️ No achievements added yet.")



