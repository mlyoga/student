import streamlit as st
import time
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
    st.error(f"⚠️ Tesseract not found at {pytesseract.pytesseract.tesseract_cmd}. Please install it.")
    st.stop()

# 🌟 Custom CSS for Beautiful Login UI
st.markdown("""
    <style>
        .login-container {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            width: 350px;
            margin: auto;
            text-align: center;
        }
        .login-title {
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }
        .login-subtext {
            font-size: 16px;
            color: #666;
            margin-bottom: 20px;
        }
        input {
            border-radius: 8px !important;
            padding: 10px;
            width: 100%;
            margin-bottom: 15px;
        }
        button {
            background-color: #007BFF !important;
            color: white !important;
            font-weight: bold;
            padding: 10px;
            width: 100%;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# 🔑 Authentication System
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# 🔐 Beautiful Login UI
if not st.session_state.authenticated:
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<p class='login-title'>🔑 Welcome Back!</p>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtext'>Please enter your credentials to access your portfolio.</p>", unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", placeholder="Enter your password", type="password")

        if st.button("🚀 Login"):
            with st.spinner("Authenticating..."):
                time.sleep(1)  # Simulating authentication delay
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    st.experimental_rerun()  # Redirect after login
                else:
                    st.error("❌ Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# 📌 Sidebar Navigation
st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
page = st.sidebar.radio(
    "📌 Navigate",
    ["🏠 Home", "📄 Resume Generator", "🎟 Event Recommendations", "📂 Digital Portfolio"]
)

# 🖼 Extract Images from PDF
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
        st.warning("⚠️ No achievements added yet.")

    # 📜 Certificates (Displays Uploaded Ones!)
    st.subheader("📜 Certificates")
    saved_certificates = get_achievements(st.session_state.username)
    if saved_certificates:
        for idx, cert in enumerate(saved_certificates):
            if isinstance(cert, dict) and "text" in cert:
                st.write(f"🏅 **Certificate {idx + 1}:** {cert['text']}")
    else:
        st.warning("⚠️ No certificates uploaded yet.")

    if st.button("💾 Save Profile"):
        st.success("✅ Profile Updated Successfully!")

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
                    st.experimental_rerun()  # ✅ Ensures certificates appear instantly in Portfolio

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")
