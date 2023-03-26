import streamlit as st
from PIL import Image
import requests

# Set page tab display
st.set_page_config(
   page_title="CompVis - Computer Vision for Industrial Safety and Attendance",
   page_icon="👷‍♂️",
   layout="wide",
   initial_sidebar_state="expanded",
)

# API URL
url = 'http://localhost:8000'

# App title and description
st.title("CompVis - Computer Vision for Industrial Safety and Attendance")
st.markdown(
    "This application uses computer vision to detect and identify faces in videos"
)
# Add image to top of sidebar
st.sidebar.image("/home/daniel/code/dosorio79/code/kolapally/streamlit/img/logo-color.png", use_column_width=True)

# Sidebar links
st.sidebar.markdown("# Navigation")
page_options = ["Face indentification", "Project Info", "About Us"]
page_selection = st.sidebar.radio("", page_options)

# Page content
if page_selection == "Face indentification":
    st.subheader("Upload an image for prediction")
    img_file_buffer = st.file_uploader('')

    if img_file_buffer is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.image(Image.open(img_file_buffer), use_column_width=True)

        with col2:
            with st.spinner("Identifying faces..."):
                img_bytes = img_file_buffer.getvalue()
                res = requests.post(url + "/detect_faces", files={'img': img_bytes})

                if res.status_code == 200:
                    st.image(res.content, use_column_width=True)
                else:
                    st.markdown("**Oops**, something went wrong 😓 Please try again.")
                    print(res.status_code, res.content)

elif page_selection == "Project Info":
    st.subheader("Project Info")
    st.write("This is the page for project info.")

elif page_selection == "About Us":
    st.subheader("About Us")
    st.write("This is the page for information about the development team.")
