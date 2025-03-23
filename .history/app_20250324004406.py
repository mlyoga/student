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
        saved_certificates = []  # Store extracted text for saving

        if uploaded_file.type.startswith("image/"):
            image = Image.open(uploaded_file)
            st.image(image, caption="🖼 Uploaded Certificate", use_container_width=True)
            extracted_texts.append(extract_text_from_image(image))

        elif uploaded_file.type == "application/pdf":
            images = extract_images_from_pdf(uploaded_file)
            for idx, image in enumerate(images):
                st.image(image, caption=f"📄 Page {idx + 1}", use_container_width=True)
                extracted_texts.append(extract_text_from_image(image))

        # Display extracted text and save
        for idx, text in enumerate(extracted_texts):
            if text.strip():  # Ensure extracted text is valid
                st.write(f"📝 **Extracted Text {idx + 1}:** {text}")
                saved_certificates.append({"text": text})

        if st.button("➕ Save Certificates"):
            for cert in saved_certificates:
                save_achievement(st.session_state.username, f"Certificate {len(saved_certificates)}", cert["text"])
            st.success("✅ All Certificates Saved! Check Portfolio to View.")

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
    user_achievements = st.text_area("🏆 Achievements (comma-separated)")

    # 🎖 Fetch Saved Achievements
    saved_achievements = get_achievements(st.session_state.username)

    # ✅ Merge and Format Achievements Correctly
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
            achievements=all_achievements  # 🔥 Fix: Pass Achievements Properly
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

    st.subheader("🏆 Achievements")
    achievements = get_achievements(st.session_state.username)
    if achievements:
        for idx, achievement in enumerate(achievements):
            if isinstance(achievement, dict) and "text" in achievement:
                st.write(f"📌 **Achievement {idx + 1}:** {achievement['text']}")
    else:
        st.warning("⚠️ No achievements added yet.")

    # 📜 **Certificates Section**
    st.subheader("📜 Certificates")
    certificates = get_achievements(st.session_state.username)
    if certificates:
        for idx, cert in enumerate(certificates):
            if isinstance(cert, dict) and "text" in cert:
                st.write(f"🏅 **Certificate {idx + 1}:** {cert['text']}")
    else:
        st.warning("⚠️ No certificates uploaded yet.")

