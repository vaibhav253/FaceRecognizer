import os
import sqlite3
import sys
import time
import cv2
import numpy as np
from PIL import Image
#load inbuilt face recognizer model provide by opencv
recognizer = cv2.face.LBPHFaceRecognizer_create()
dataset_path = './Frames/'
if not os.path.exists('./recognizer'):
    os.makedirs('./recognizer')
#fuction for the factching frames
def getImagesWithID(path):
  path = [os.path.join(path,f) for f in os.listdir(dataset_path)]
  faces = []
  IDs = []
  for path in path:
    faceImg = Image.open(path).convert('L')
    faceNp = np.array(faceImg,'uint8')
    ID = int(os.path.split(path)[-1].split('.')[1])
    faces.append(faceNp)
    IDs.append(ID)
    #cv2.imshow("training",faceNp)
    cv2.waitKey(10)
  return np.array(IDs), faces
#labels and ids
Ids, faces = getImagesWithID(dataset_path)
#train the model
recognizer.train(faces,Ids)
#save the data as YAML file it will store as a list
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()

#connection to the dataset
connection = sqlite3.connect('Images.db')
cur = connection.cursor()
#fatching YAML file
fname = "recognizer/trainingData.yml"
#load the cascade
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
#load the model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(fname)
while True:
  ret, FaceRecogintion = cap.read()
  gray = cv2.cvtColor(FaceRecogintion, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    cv2.rectangle(FaceRecogintion,(x,y),(x+w,y+h),(0,255,0),3)
    #model prediction
    ids,pred = recognizer.predict(gray[y:y+h,x:x+w])
    cur.execute("select name from PersonInfo where id = (?);", (ids,))
    names = cur.fetchall()

    pred_name = names[0][0]
    #Comarision for the name.
    if pred  <50:
      cv2.putText(FaceRecogintion, 'Hello '+ pred_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2, cv2.LINE_AA)
    else:
      cv2.putText(FaceRecogintion, 'New Member', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2,cv2.LINE_AA)
      cv2.imshow('FaceRecogintion', FaceRecogintion)
      time.sleep(10)
      # saving the data for new user.
      #it will gives you choice for the saving new users data. if it is yes than it will redirect to
      # data generation for saving the frames and users name
      usr_input = input("You want to Save Your INFO:-(Y/N): ")
      while (usr_input != 'y') | (usr_input != 'n'):
        if usr_input == 'y':
          import DataGeneration
        elif usr_input == 'n':
          sys.exit()
  cv2.imshow('FaceRecogintion',FaceRecogintion)
  #if escap key pressed than it will be closed.
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break
cap.release()
cv2.destroyAllWindows()