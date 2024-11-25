
from tf_keras.models import load_model
from threading import RLock
import cv2
import numpy as np

class Eyes:
  def __init__(self, videoCaptureIndex, modelDir):
    self.facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    self.cap = cv2.VideoCapture(videoCaptureIndex)
    # cap.set(3, 640)
    # cap.set(4, 480)
    self.font = cv2.FONT_HERSHEY_COMPLEX

    self.model = load_model(f"{modelDir}/keras_model.h5")

    self.classNames = open(f"{modelDir}/labels.txt", "r").readlines()
    self.inSightFaces = []
    self.see = True

  def watch(self, lock: RLock):
    print("\nWatching...")
    while self.see:
        success, imgOriginal=self.cap.read()
        lock.acquire()
        self.inSightFaces.clear()
        faces = self.facedetect.detectMultiScale(imgOriginal, 1.3, 5)
        for x, y, w, h in faces:
            crop_img = imgOriginal[y:y+h, x:x+w]
            img = cv2.resize(crop_img, (224, 224), interpolation=cv2.INTER_AREA)
            img = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)
            img = (img / 127.5) - 1

            prediction = self.model.predict(img, verbose=0)
            classIndex = np.argmax(prediction)
            # print(str(f"classIndex:{classIndex}"))
            faceName = self.classNames[classIndex]
            name = faceName[2:].replace("\n", "")
            # print('Face name [%s%%]\r'%faceName, end="")
            predictionValue = prediction[0][classIndex]

            self.inSightFaces.append({"name": name, "prediction": predictionValue})

            infoBoxSize = 40
            cv2.rectangle(imgOriginal, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(imgOriginal, (x, y-infoBoxSize), (x+w, y), (0, 255, 0), 2)
            cv2.rectangle(imgOriginal, (x, y+h), (x+w, y+h+infoBoxSize), (0, 255, 0), 2)

            cv2.putText(imgOriginal, name, (x, y-10), self.font, 0.75, (255, 0, 0))
            cv2.putText(imgOriginal, str(round(predictionValue * 100, 2)) + "%", (x, y+h+infoBoxSize-10), self.font, 0.75, (0, 0, 255))
        
        lock.release()
        cv2.imshow("Result", imgOriginal)
        cv2.waitKey(1)
    
  def getInSightFaces(self):
    return self.inSightFaces
  
  def closeEyes(self):
     self.see = False