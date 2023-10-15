# Virtual-Mouse

To create a virtual mouse I have used OpenCV and MediaPipe to detect the user's hand. Mediapipe module uses a machine learning model to detect and track the user's hand in real-time. Once the hand is detected, the hand landmarks are extracted using MediaPipe's hand landmark model. These landmarks represent the position of the fingers, thumb, and palm of the hand.
Next, the hand landmarks are mapped to the cursor position using OpenCV. The cursor position is updated based on the position of the hand landmarks(index finger tip) on the screen. This allows the user to control the cursor using hand movements.
To click an item on the screen, the user can perform a gesture of pinching the thumb finger and the index finger. This gesture is detected and the cursor is clicked accordingly.

Clone the repository
Before you run the file you should install the required modules. Open the command prompt in cloned folder and type
```
pip install -r requirements.txt
```
