import streamlit as st
import cv2
import numpy as np
import dlib
from PIL import Image
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from twilio_turn import get_ice_servers
import av
import threading

# Title of the app
st.title("Face Landmark Color Masking")

# Sidebar for user inputs
st.sidebar.header("Settings")

# Option to choose between webcam and image
input_option = st.sidebar.radio("Choose input source:", ("Example Image", "Image", "Webcam"))

# Sliders for BGR values
b = st.sidebar.slider("Blue", 0, 255, 0)
g = st.sidebar.slider("Green", 0, 255, 0)
r = st.sidebar.slider("Red", 0, 255, 0)

# Initialize dlib's face detector and landmark predictor
try:
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('assets/shape_predictor_68_face_landmarks.dat')
except Exception as e:
    st.error(f"Error loading dlib models: {e}")
    st.stop()

# Function to process the image
def imageProcess(imgOrg, points, b, g, r):
    mask = np.zeros_like(imgOrg)
    mask = cv2.fillPoly(mask, [points], (255, 255, 255))

    coloredMask = np.zeros_like(mask)
    coloredMask[:] = b, g, r

    imgMask = cv2.bitwise_and(coloredMask, mask)
    imgMask = cv2.GaussianBlur(imgMask, (7, 7), 10)
    imgOrgGray = cv2.cvtColor(imgOrg, cv2.COLOR_BGR2GRAY)
    imgOrgGray = cv2.cvtColor(imgOrgGray, cv2.COLOR_GRAY2BGR)
    imgMask = cv2.addWeighted(imgOrgGray, 1, imgMask, 0.3, 0)

    return imgMask

def faceProcess(imgCol, input_option):
    if input_option == "Webcam":
        imgCol = cv2.resize(imgCol, (0, 0), None, 1, 1)
    else:
        h, w = imgCol.shape[:2]
        aspect_ratio = w / h
        height = 500
        width = int(height * aspect_ratio)
        imgCol = cv2.resize(imgCol, (width, height), interpolation=cv2.INTER_AREA)
        imgCol = cv2.cvtColor(imgCol, cv2.COLOR_BGR2RGB)
    imgOrg = imgCol.copy()
    imgGray = cv2.cvtColor(imgCol, cv2.COLOR_RGB2GRAY)

    # Initialize img_lips with the original image
    imgLips = imgOrg.copy()

    faces = detector(imgGray)

    for face in faces:
        landmarks = predictor(imgGray, face)
        landmarkPoints = []

        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarkPoints.append([x, y])

        landmarkPoints = np.array(landmarkPoints)
        imgLips = imageProcess(imgOrg, landmarkPoints[48:60], r, g, b)

    return imgLips

# Webcam feed using streamlit-webrtc
def callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")
    img_processed = faceProcess(img, "Webcam")
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Function to start WebRTC
def start_webrtc():
    webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": get_ice_servers()},
        video_frame_callback=callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

# Webcam or Image input
if input_option == "Webcam":
    st.write("Using Webcam")
    start_webrtc()

elif input_option == "Image":
    st.write("Using Image")
    st.write("Please upload a frontal face view image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        imgCol = np.array(Image.open(uploaded_file))
        imgLips = faceProcess(imgCol, input_option)
        st.image(imgLips, caption="Processed Image", use_container_width=True)
    else:
        st.warning("Please upload an image.")
else:
    st.write("Using Example Image")
    imgCol = np.array(Image.open("assets/3.jpeg"))
    imgLips = faceProcess(imgCol, input_option)
    st.image(imgLips, caption="Processed Image", use_container_width=True)