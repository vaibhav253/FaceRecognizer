'''import MySQLdb
#connection to mySQL server
class connection():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="images")'''
import cv2
import numpy as np
import sqlite3
import os
#connection to the dataset
connection = sqlite3.connect('Images.db')
if not os.path.exists('./Frames'):
    os.makedirs('./Frames')
cur = connection.cursor()
#if you are running for the first time than the next two line must be run for first time of running

#sql = 'DROP TABLE IF EXISTS PersonInfo;CREATE TABLE PersonInfo (id integer unique primary key autoincrement,name text);'
#cur.executescript(sql)
#User input
File_name = input("Enter your name: ")
cur.execute('INSERT INTO PersonInfo (name) VALUES (?)', (File_name,))
#connection.db.commit()

#load the cascade
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
#uname = input("Enter your name: ")
#c.execute('INSERT INTO PersonInfo (name) VALUES (?)', (uname,))
id = cur.lastrowid
count = 0
while True:
  #detection of the face
  ret, FaceDetaction = cap.read()
  gray = cv2.cvtColor(FaceDetaction, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  #saving the frames.
  for (x,y,w,h) in faces:
    count = count+1
    cv2.imwrite("./Frames/"+str(id)+"."+str(count)+".jpg",gray[y:y+h,x:x+w])
    #it will shows the rectangle on the face
    cv2.rectangle(FaceDetaction, (x,y), (x+w, y+h), (0,255,0), 2)
    cv2.waitKey(100)

  cv2.imshow('FaceDetaction',FaceDetaction)
  cv2.waitKey(1);

  #if escap key pressed than it will be closed.
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break
  elif count > 20:
    break
cap.release()
connection.commit()
connection.close()
cv2.destroyAllWindows()