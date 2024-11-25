import cv2
import mediapipe as mp
import pyautogui
from threading import RLock

class Hands:
  def __init__(self, videoCaptureIndex):
    self.capturing = False
    self.videoCaptureIndex = videoCaptureIndex
    self.capture_hands = mp.solutions.hands.Hands()
    # Grabbing the Holistic Model from Mediapipe and
    # Initializing the Model
    self.mp_holistic = mp.solutions.holistic
    self.holistic_model = self.mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) 
    # Initializing the drawing utils for drawing the facial landmarks on image
    self.mp_drawing = mp.solutions.drawing_utils
    self.screen_width, self.screen_height = pyautogui.size()
    
  def stopCaptureHandsGestures(self):
    self.capturing = False
      
  def startCaptureHandsGestures(self, lock: RLock):
    self.capturing = True
    capture = cv2.VideoCapture(self.videoCaptureIndex)
    capture.set(3, 1024)
    capture.set(4, 800)

    while self.capturing:
        _, image = capture.read()
        # resizing the frame for better view
        # image = cv2.resize(image, (800, 600))

        image_height, image_width, _ = image.shape
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output_hands = self.capture_hands.process(rgb_image)
        all_hands = output_hands.multi_hand_landmarks
        if all_hands:
            for hand in all_hands:
                self.mp_drawing.draw_landmarks(image, hand, self.mp_holistic.HAND_CONNECTIONS)
                one_hand_landmarks = hand.landmark
                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)
                    # print(x, y)
                    if id == self.mp_holistic.HandLandmark.INDEX_FINGER_TIP:
                        mouse_x = int(self.screen_width / image_width * x)
                        mouse_y = int(self.screen_height / image_height * y)
                        cv2.circle(image, (x, y), 10, (0, 255, 255))
                        pyautogui.moveTo(mouse_x, mouse_y)
                        x1 = x
                        y1 = y
                    if id == self.mp_holistic.HandLandmark.THUMB_TIP:
                        x2 = x
                        y2 = y
                        cv2.circle(image, (x, y), 10, (0, 255, 255))
                x_dist = x2- x1
                y_dist = y2- y1
                if (x_dist < 10):
                    pass
                    pyautogui.mouseDown()
                elif (y_dist < 30):
                    pyautogui.click()
                    pass
                else:
                    pyautogui.mouseUp()
                    pass
                print(f"x_dist({x_dist})\n")
                print(f"y_dist({y_dist})\n")
        cv2.imshow("Hand movement video capture", image)
        key = cv2.waitKey(100)
        if key == 27:
            break
    
    capture.release()
    cv2.destroyAllWindows()