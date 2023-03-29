import streamlit as st
from PIL import Image
import requests
import subprocess
import ffmpeg
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
st.sidebar.image("/home/kolapally/code/kolapally/streamlit/img/logo-color.png", use_column_width=True)

# Sidebar links
st.sidebar.markdown("# Navigation")
page_options = ["Image Detection",'Video Detection', "Project Info", "About Us"]
page_selection = st.sidebar.radio("", page_options)

# Page content
if page_selection == "Image Detection":
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

if page_selection == "Video Detection":
    st.subheader("Upload a video for prediction")
    video_file_buffer = st.file_uploader('')

    if video_file_buffer is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.video(video_file_buffer)

        with col2:
            with st.spinner("Labeling faces ..."):
                # img_bytes = img_file_buffer.getvalue()
                res = requests.post(url + "/detect_video", files={'video': video_file_buffer})

                if res.status_code == 200:
                    video_bytes = res.content
                    with open('myvideo.mp4', 'wb') as f:
                        f.write(video_bytes)
                    subprocess.run(['ffmpeg', '-i', 'myvideo.mp4', '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'copy', 'output.mp4'])
                    with open('output.mp4', 'rb') as f:
                        video_bytes = f.read()
                    st.video(video_bytes)
                else:
                    st.markdown("**Oops**, something went wrong 😓 Please try again.")
                    print(res.status_code, res.content)

elif page_selection == "Project Info":
    st.subheader("Project Info")
    st.write("This is the page for project info.")

elif page_selection == "About Us":
    st.subheader("About Us")
    st.write("This is the page for information about the development team.")
