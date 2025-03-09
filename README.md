<p class="demoTitle">Lips Detection and Coloring</p>
<p>This project detects faces using dlib's facial landmark predictor and applies a customizable color mask to the lips region in an image or webcam feed. Users can adjust the mask color in real-time using trackbars for Blue, Green, and Red (BGR) values.</p>
<h2>Features</h2>
<ul data-spread="false">
<li>
<p>Face detection using dlib's <code>frontal_face_detector</code>.</p>
</li>
<li>
<p>68 facial landmarks prediction with <code>shape_predictor_68_face_landmarks.dat</code>.</p>
</li>
<li>
<p>Customizable lip color overlay using OpenCV.</p>
</li>
<li>
<p>Real-time color adjustment via trackbars.</p>
</li>
<li>
<p>Supports both webcam and static image inputs.</p>
</li>
<li>
<p>Streamlit-based web application for easy interaction.</p>
</li>
</ul>
<h2>Installation</h2>
<h3>Prerequisites</h3>
<p>Ensure you have Python installed along with the following dependencies:</p>
<pre><code>pip install opencv-python numpy dlib streamlit streamlit-webrtc av twilio_turn</code></pre>
<h3>Download the Required Model</h3>
<p>Download <code>shape_predictor_68_face_landmarks.dat</code> from <a>dlib's official source</a> and place it inside the <code>assets/</code> directory.</p>
<h2>Usage</h2>
<h3>Running with an Image</h3>
<pre><code>python main.py</code></pre>
<p>Make sure to place your image in the <code>assets/</code> directory and update the filename in <code>main.py</code> accordingly.</p>
<h3>Running with a Webcam</h3>
<p>To enable webcam mode, set <code>webcam = True</code> inside <code>main.py</code> and run:</p>
<pre><code>python main.py</code></pre>
<h3>Running as a Streamlit App</h3>
<p>To launch the Streamlit web application, run:</p>
<pre><code>streamlit run streamlit_app.py</code></pre>
<p>This will open an interactive web-based interface where you can choose between an example image, uploading your own image, or using a webcam.</p>
<h2>File Structure</h2>
<pre>.<br />├── assets/<br />│ ├── shape_predictor_68_face_landmarks.dat # Facial landmark model<br />│ ├── 2.jpeg # Sample image<br />│ ├── 1.png # Another sample image<br />│ <br />├── main.py # Main script<br />├── streamlit_app.py # Streamlit application<br />├── twilio_turn.py # Twilio TURN server configuration<br />├── README.md # Project documentation</pre>
<h2>How It Works</h2>
<ol start="1" data-spread="false">
<li>
<p>The program detects faces using dlib's frontal face detector.</p>
</li>
<li>
<p>It extracts facial landmarks and isolates the lip region.</p>
</li>
<li>
<p>A colored mask is applied to the lips based on user-defined BGR values.</p>
</li>
<li>
<p>The processed image is displayed in real-time with an option to adjust colors dynamically.</p>
</li>
<li>
<p>The Streamlit app provides a web-based UI to choose input sources and apply lip color filters.</p>
</li>
</ol>
<h2>Controls</h2>
<ul data-spread="false">
<li>
<p>Adjust the <strong>BGR trackbars</strong> to change lip color.</p>
</li>
<li>
<p>Press <code>Esc</code> to exit the application.</p>
</li>
<li>
<p>In Streamlit, use sliders to modify colors and switch between image and webcam modes.</p>
</li>
</ul>
<p>&nbsp;</p>
