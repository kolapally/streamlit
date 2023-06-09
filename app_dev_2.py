import streamlit as st
from PIL import Image
import requests
import subprocess
import os
# Set page tab display
st.set_page_config(
   page_title="CompVis - Computer Vision for Industrial Safety",
   page_icon="👷‍♂️",
   layout="wide",
   initial_sidebar_state="expanded",
)

# API URL
url = 'https://compvimgwithvideo-2ohawdromq-ew.a.run.app'

# App title and description
st.title("CompVis - Computer Vision for Industrial Safety and Attendance")
st.markdown(
    "This application uses computer vision to detect and identify faces in videos"
)
st.markdown(
    "👷‍♂️ work in progress: our app is currently down. We are migrating the backend and updating the API... See it in action in this demo video "
)

st.markdown('https://drive.google.com/file/d/1nbOl3mUyAyEcyQH7v04KyAABqTwXVLKO/view?usp=drive_link')



# Add image to top of sidebar
st.sidebar.image("img/logo-color.png", use_column_width=True)

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
                res = requests.post(url + "/detect_image", files={'img': img_bytes})

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
                video_path = os.path.join(os.getcwd(),'output.mp4')
                if os.path.exists(video_path):
                    os.remove(video_path)

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
    st.write("Have you ever visited an industry facility where employees use ID cards to mark attendence?")
    st.text("")
    st.write("During emergency evacuations, it can be very hard to monitor the employees who are safe and those who are still inside the facility.")
    st.text("")
    st.write("Additionally, during assembly point checks, the process of manually verifying the presence of each employee can be time consuming and prone to errors.")
    st.text("")
    st.text("")
    st.text("")
    st.write("To solve this, we use advanced computer vision and person detection techniques to accurately monitor the employees who are outside the facility during emegencies.")
    st.text("")
    st.text("")
    st.write("Our system also helps to detect employeeat enterance to know who was present in workplace during emergency.")
    st.text("")
    st.text("")
    st.write("To make the project more engaging, we considered the iconic fire drill scene from TV series (THE OFFICE).")
    st.write("Model trained on 6 charachters from the series and made to predict the faces with lables.")

elif page_selection == "About Us":
    st.subheader("About Us")
    st.title("Kolapally Sai kalyan")
    st.title("Daniel Osório")
    st.title("Merle Marie Buchmann")
    st.title("Kranthi Maddishetty")
