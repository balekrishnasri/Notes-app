import streamlit as st
from PIL import Image
import pytesseract

from auth import login_user, register_user
from ai_utils import generate_summary, format_notes, get_keywords
from pdf_utils import create_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Notes App",
    page_icon="📚",
    layout="wide"
)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

def go(page):
    st.session_state.page = page

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📚 Notes App")

    if st.session_state.user:
        st.success(f"Logged in as {st.session_state.user}")

        if st.button("🏠 Home"):
            go("home")

        if st.button("🚪 Logout"):
            st.session_state.user = None
            go("login")
    else:
        st.info("Please login")

# ---------------- LOGIN ----------------
def login_page():
    st.markdown("## 🔐 Login")

    with st.container():
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.session_state.user = user
                    go("home")
                    st.success("Login successful!")
                else:
                    st.error("Invalid credentials")

        with col2:
            if st.button("Register"):
                if register_user(username, password):
                    st.success("Registered! Now login")
                else:
                    st.error("User already exists")

# ---------------- HOME ----------------
def home_page():
    st.title("📸 Notes Generator")
    st.caption("Upload image → Extract notes → AI summary → Download PDF")

    uploaded_file = st.file_uploader("Upload Notes Image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        col1, col2 = st.columns(2)

        with col1:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", use_container_width=True)

        with col2:
            text = pytesseract.image_to_string(img)

            st.subheader("📄 Extracted Text")
            st.text_area("", text, height=300)

        if st.button("🧠 Generate AI Notes"):
            summary = generate_summary(text)
            keywords = get_keywords(text)
            formatted = format_notes(text, summary, keywords)

            st.session_state.formatted = formatted

            st.success("Notes generated!")

            st.markdown("### 🧠 Summary")
            st.write(summary)

            st.markdown("### 🔑 Keywords")
            st.write(keywords)

        if st.button("📥 Download PDF"):
            if "formatted" in st.session_state:
                path = create_pdf(st.session_state.formatted)

                with open(path, "rb") as f:
                    st.download_button(
                        "Download Notes PDF",
                        f,
                        file_name="Notes.pdf"
                    )
            else:
                st.warning("Generate notes first!")

# ---------------- ROUTER ----------------
def main():
    if st.session_state.user is None:
        login_page()
    else:
        home_page()

if __name__ == "__main__":
    main()