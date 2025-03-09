import cv2
import numpy as np
import dlib

# Initialize dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('assets/shape_predictor_68_face_landmarks.dat')

def initialize_trackbars(window_name):
    """
    Creates a window with trackbars for adjusting Blue, Green, and Red values.

    Args:
        window_name (str): Name of the window to create.
    """
    cv2.namedWindow(window_name)
    cv2.resizeWindow(window_name, 640, 240)
    cv2.createTrackbar('Blue', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar('Green', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar('Red', window_name, 0, 255, lambda x: None)

def lips_process(img_org, points, b, g, r):
    """
    Applies a colored mask to the lips region based on the provided points and BGR values.

    Args:
        img_org (numpy.ndarray): The original image.
        points (numpy.ndarray): Array of points defining the lips region.
        b (int): Blue value for the mask.
        g (int): Green value for the mask.
        r (int): Red value for the mask.

    Returns:
        numpy.ndarray: The processed image with the colored mask applied.
    """
    # Create a mask for the lips region
    mask = np.zeros_like(img_org)
    mask = cv2.fillPoly(mask, [points], (255, 255, 255))

    # Create a colored mask using the provided BGR values
    colored_mask = np.zeros_like(mask)
    colored_mask[:] = b, g, r

    # Apply the colored mask to the lips region
    img_mask = cv2.bitwise_and(colored_mask, mask)
    img_mask = cv2.GaussianBlur(img_mask, (7, 7), 10)

    # Convert the original image to grayscale and back to BGR for blending
    img_org_gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)
    img_org_gray = cv2.cvtColor(img_org_gray, cv2.COLOR_GRAY2BGR)

    # Blend the colored mask with the grayscale image
    img_mask = cv2.addWeighted(img_org_gray, 1, img_mask, 0.3, 0)

    return img_mask

def face_process(img_col, webcam):
    """
    Processes the input image to detect faces and apply a colored mask to the lips.

    Args:
        img_col (numpy.ndarray): The input image.
        webcam (bool): Flag to indicate if the input is from a webcam.

    Returns:
        numpy.ndarray: The processed image with the colored mask applied to the lips.
    """
    # Resize the image based on the input source
    if webcam:
        img_col = cv2.resize(img_col, (0, 0), None, 1, 1)
    else:
        h, w = img_col.shape[:2]
        aspect_ratio = w / h
        height = 600
        width = int(height * aspect_ratio)
        img_col = cv2.resize(img_col, (width, height), interpolation=cv2.INTER_AREA)

    # Convert the image to RGB and create a copy
    img_col = cv2.cvtColor(img_col, cv2.COLOR_BGR2RGB)
    img_org = img_col.copy()
    img_gray = cv2.cvtColor(img_col, cv2.COLOR_RGB2GRAY)

    # Initialize img_lips with the original image
    img_lips = img_org.copy()

    # Detect faces in the grayscale image
    faces = detector(img_gray)

    for face in faces:
        # Predict facial landmarks
        landmarks = predictor(img_gray, face)
        landmark_points = []

        # Extract landmark points
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmark_points.append([x, y])

        # Get BGR values from trackbars
        b = cv2.getTrackbarPos('Blue', 'BGR')
        g = cv2.getTrackbarPos('Green', 'BGR')
        r = cv2.getTrackbarPos('Red', 'BGR')

        # Convert landmark points to a NumPy array
        landmark_points = np.array(landmark_points)

        # Apply the colored mask to the lips region
        img_lips = lips_process(img_org, landmark_points[48:60], b, g, r)

    return img_lips

def main(webcam):
    """
    Main function to handle webcam or image input and process the lips region.
    """

    # Initialize video capture (webcam) if enabled
    cap = None
    if webcam:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

    # Initialize trackbars for BGR adjustment
    initialize_trackbars('BGR')

    while True:
        # Capture frame from webcam or load image
        if webcam:
            success, img_col = cap.read()
            if not success:
                print("Error: Failed to capture frame from webcam.")
                break
        else:
            img_col = cv2.imread('assets/3.jpeg', cv2.IMREAD_COLOR)
            if img_col is None:
                print("Error: Could not load image.")
                break

        # Apply the colored mask to the lips region
        img_lips = face_process(img_col, webcam)
        cv2.imshow('BGR', img_lips)

        # Exit on 'Esc' key press
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release resources
    if webcam:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Flag to toggle between webcam and image input
    webcam = False
    main(webcam)