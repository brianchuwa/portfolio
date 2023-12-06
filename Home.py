import uuid
from pathlib import Path
import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Brian Chuwa",
    page_icon="👨‍💻",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
# profile_pic = current_dir / "assets" / "brian_chuwa_hero_image.png"
profile_pic_filename = "assets/brian_chuwa_hero_image.png"


# --- GENERAL SETTINGS ---
NAME = "Brian Chuwa"
DESCRIPTION = """
I am a results-driven, experienced finance professional, self-taught data analyst, and web developer passionate about digital transformation.
"""
EMAIL = "hello@brian.co.tz"
SOCIAL_MEDIA = {
    "YouTube": "https://www.youtube.com/@brianchuwa ",
    "LinkedIn": "https://www.linkedin.com/in/brianchuwa/ ",
    "GitHub": "https://github.com/brianchuwa",
    "Twitter": "https://twitter.com/BrianChuwa",
}

# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
# with open(resume_file, "rb") as pdf_file:
#     PDFbyte = pdf_file.read()
# profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
   # st.image(profile_pic, width=230)
   # Check if the file exists
    if os.path.exists(profile_pic_filename):
        # Open the image file
        with open(profile_pic_filename, "rb") as f:
            profile_pic = f.read()

        # Display the image in Streamlit app
        st.image(profile_pic, width=230)
    else:
        st.warning(f"Profile picture not found at {profile_pic_filename}")

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.link_button(
        "Download CV", "https://docs.google.com/document/d/1DyarOjcOpVzlzrz18FCFQ7YdLIX_XlXLgjv8t1Ok_Ls/export?format=pdf")
    st.write("📤", EMAIL)

# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")

st.divider()

# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience & Qulifications")
st.write(
    """
- ✔️ 7 Years experience extracting actionable insights from data
- ✔️ 7 Years experience working as financial analyst and investment adviser
- ✔️ Strong hands on experience and knowledge in Python and Google Sheets
- ✔️ Good understanding of statistical principles and their respective applications
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write('\n')
st.write('\n')
st.subheader("Hard Skills")
st.write(
    """
- 👩‍💻 Programming: Python (Pandas, Streamlit), HTML, CSS
- 📊 Data Visulization: Looker Studio, PowerBi, MS Excel, Google Sheets
- 📚 Modeling: Logistic regression, linear regression
- 🗄️ Databases: MySQL, SqLite
- 🖋️ Workspaces: Microsoft 365, Google Workspace
"""
)
st.write('\n')

st.divider()

st.write('\n')
st.write('\n')
st.subheader("Contact Me")
contact_form = """
<form action="https://formsubmit.co/hello@brian.co.tz" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)


st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
# Custom footer
st.markdown('<div id="made-by">Made by Brian Chuwa</div>',
            unsafe_allow_html=True)


hidden_variable = str(uuid.uuid4())
st.session_state.hidden_variable = hidden_variable
st.write(hidden_variable)
