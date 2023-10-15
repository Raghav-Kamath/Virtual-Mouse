import mediapipe as mp
import cv2
import numpy as np
import time
from math import sqrt
import win32api
import pyautogui
 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
click_distance_threshold = 30 # adjust this to control the distance threshold for a click
click_cooldown = 1 # adjust this to control the cooldown period in seconds
last_click_time = 0 # Initialize Click time

count=0
# Initialize frame times
prev_frame_time = 0
new_frame_time = 0

last_x = 0
last_y = 0
last_update_time = 0
cursor_speed = 0.5 # adjust this to control the cursor movement speed

video = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands: 
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, imageWidth, _ = image.shape
 
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )

        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                indexfingertip_x = handLandmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * imageWidth
                indexfingertip_y = handLandmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * imageHeight
                thumbfingertip_x = handLandmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * imageWidth
                thumbfingertip_y = handLandmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * imageHeight

                try:
                    Distance_x = sqrt((indexfingertip_x - thumbfingertip_x) ** 2 + (indexfingertip_x - thumbfingertip_x) ** 2)
                    Distance_y = sqrt((indexfingertip_y - thumbfingertip_y) ** 2 + (indexfingertip_y - thumbfingertip_y) ** 2)                           
                    distance = sqrt(Distance_x ** 2 + Distance_y ** 2)

                    if distance < click_distance_threshold:
                        current_time = time.time()
                        if current_time - last_click_time > click_cooldown:
                            last_click_time = current_time
                            count+=1
                            print("Times Clicked :",count)
                            pyautogui.click()

                    current_time = time.time()
                    if last_update_time == 0:
                        last_update_time = current_time
                    time_diff = current_time - last_update_time

                    if time_diff > 0.02: # adjust this to control the update frequency
                        new_x = int((last_x + indexfingertip_x) / 2)
                        new_y = int((last_y + indexfingertip_y) / 2)
                        win32api.SetCursorPos((new_x*4,new_y*5))
                        last_x = new_x
                        last_y = new_y
                        last_update_time = current_time
                except:
                    pass

        # Calculating the FPS to display on screen
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        # Converting the FPS into integer
        fps = int(fps)
        fps = str(fps)
        cv2.putText(image, "FPS : "+ fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "Press Q to Exit", (int(imageWidth*0.72), 30), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.25, color=(0, 0, 0), thickness=4,lineType=cv2.LINE_AA)
        cv2.putText(image, "Press Q to Exit", (int(imageWidth*0.72), 30), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.25, color=(255, 255, 255), thickness=1,lineType=cv2.LINE_AA)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
 
video.release()
cv2.destroyAllWindows()