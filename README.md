Lips Detection and Coloring

This project detects faces using dlib's facial landmark predictor and applies a customizable color mask to the lips region in an image or webcam feed. Users can adjust the mask color in real-time using trackbars for Blue, Green, and Red (BGR) values.

Features

Face detection using dlib's frontal_face_detector.

68 facial landmarks prediction with shape_predictor_68_face_landmarks.dat.

Customizable lip color overlay using OpenCV.

Real-time color adjustment via trackbars.

Supports both webcam and static image inputs.

Installation

Prerequisites

Ensure you have Python installed along with the following dependencies:

pip install opencv-python numpy dlib

Download the Required Model

Download shape_predictor_68_face_landmarks.dat from dlib's official source and place it inside the assets/ directory.

Usage

Running with an Image

python main.py

Make sure to place your image in the assets/ directory and update the filename in main.py accordingly.

Running with a Webcam

To enable webcam mode, set webcam = True inside main.py and run:

python main.py

File Structure

.
├── assets/
│   ├── shape_predictor_68_face_landmarks.dat  # Facial landmark model
│   ├── 3.jpeg  # Sample image
├── main.py  # Main script
├── README.md  # Project documentation

How It Works

The program detects faces using dlib's frontal face detector.

It extracts facial landmarks and isolates the lip region.

A colored mask is applied to the lips based on user-defined BGR values.

The processed image is displayed in real-time with an option to adjust colors dynamically.

Controls

Adjust the BGR trackbars to change lip color.

Press Esc to exit the application.
