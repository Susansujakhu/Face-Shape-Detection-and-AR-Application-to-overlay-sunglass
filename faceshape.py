#importing the libraries
import tkinter as tk

import numpy as np #for mathematical calculations
import cv2 #for face detection and other image operations
import dlib #for detection of facial landmarks ex:nose,jawline,eyes
import imutils
import tkinter
import time
import os
from PIL import Image, ImageTk
'''
cap = cv2.VideoCapture(1)
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(0)

'''
#haarcascade for detecting faces
# link = https://github.com/opencv/opencv/tree/master/data/haarcascades
face_cascade_path = "Cascade files/haarcascade_frontalface_default.xml"
#.dat file for detecting facial landmarks
#download file path = http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
predictor_path = "shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"

#create the haar cascade for detecting face
faceCascade = cv2.CascadeClassifier(face_cascade_path)


#create the landmark predictor
predictor = dlib.shape_predictor(predictor_path)

#read the image
image = cv2.imread('round.jpg')
#ret, image = cap.read()
fx, fy, fw, fh = 170, 80, 450, 360
cv2.rectangle(image ,(fx ,fy) ,(fw ,fh) ,(0,0,255), 2)
cv2.putText(image, "Place your Face inside the red Box", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
cv2.putText(image, "Exit = 'q'", (30,70 ),fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=1,color=(0,255,0), thickness=1)
#resizing the image to 000 cols nd 500 rows
#image = imutils.resize(image, width=600)
#making another copy

#convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#apply a Gaussian blur with a 3 x 3 kernel to help remove high frequency noise
#gauss = cv2.GaussianBlur(gray,(3,3), 0)

#Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.05,
    minNeighbors=5,
    minSize=(100,100),
    flags=cv2.CASCADE_SCALE_IMAGE
    )
#Detect faces in the image
#print("found {0} faces!".format(len(faces)) )
message = "No"
for (x,y,w,h) in faces:

    #draw a rectangle around the faces
    #if x < fx or y < fy or (x + w) > fw or (y + h) > fh:
     #   break

    #cv2.putText(image, "Press 'c' to continue...", (300,440 ),fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=1,color=(0,255,0), thickness=2)
    #cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
    #converting the opencv rectangle coordinates to Dlib rectangle
    dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
    #detecting landmarks
    detected_landmarks = predictor(image, dlib_rect).parts()
    #converting to np matrix
    landmarks = np.matrix([[p.x,p.y] for p in detected_landmarks])
    #landmarks array contains indices of landmarks.

    #copying the image so we can we side by side
    landmark = image.copy()
    for idx, point in enumerate(landmarks):
            pos = (point[0,0], point[0,1] )
            #annotate the positions
            cv2.putText(landmark,str(idx),pos,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.4,color=(0,0,255) )
            #draw points on the landmark positions
            cv2.circle(landmark, pos, 3, color=(0,255,255))

    #cv2.imshow("Landmarks", landmark)

#making another copy  for showing final results
    results = image.copy()

    linepointleft = (landmarks[17,0],landmarks[17,1])
    #print("linepointleft", linepointleft)
    linepointright = (landmarks[26,0],landmarks[26,1])
    #print("linepointright", linepointright)
    line1 = np.subtract(linepointright, linepointleft)[0]
    line1 = line1 + 20
    print("line1",line1)
    cv2.line(results, linepointleft, linepointright, color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 0',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointleft, 5, color=(255,0,0), thickness=-1)
    cv2.circle(results, linepointright, 5, color=(255,0,0), thickness=-1)


    #drawing line 2 with circles
    linepointleft = (landmarks[1,0],landmarks[1,1])
    linepointright = (landmarks[15,0],landmarks[15,1])
    line2 = np.subtract(linepointright,linepointleft)[0]
    cv2.line(results, linepointleft,linepointright,color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 2',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointleft, 5, color=(255,0,0), thickness=-1)
    cv2.circle(results, linepointright, 5, color=(255,0,0), thickness=-1)

    #drawing line 3 with circles
    linepointleft = (landmarks[4,0],landmarks[4,1])
    linepointright = (landmarks[12,0],landmarks[12,1])
    line3 = np.subtract(linepointright,linepointleft)[0]
    cv2.line(results, linepointleft,linepointright,color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 3',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointleft, 5, color=(255,0,0), thickness=-1)
    cv2.circle(results, linepointright, 5, color=(255,0,0), thickness=-1)

    #drawing line 4 with circles
    linepointbottom = (landmarks[8,0],landmarks[8,1])
    linepointtop = (landmarks[8,0],y)
    line4 = np.subtract(linepointbottom,linepointtop)[1]
    cv2.line(results,linepointtop,linepointbottom,color=(0,255,0), thickness = 2)
    cv2.putText(results,' Line 4',linepointbottom,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
    cv2.circle(results, linepointtop, 5, color=(255,0,0), thickness=-1)
    cv2.circle(results, linepointbottom, 5, color=(255,0,0), thickness=-1)
    #print(line1,line2,line3,line4)

    # similarity = np.std([line1,line2,line3])
    # #print("similarity=",similarity)
    # ovalsimilarity = np.std([line2,line4])
    # #print('diam=',ovalsimilarity)

    similarity1 = np.std([line2, line4])

    similarity2 = np.std([line1, line3])

    similarity3 = np.std([line1, line2, line3])

    #we use arcustangens for angle calculation
    ax,ay = landmarks[3,0],landmarks[3,1]
    bx,by = landmarks[4,0],landmarks[4,1]
    cx,cy = landmarks[5,0],landmarks[5,1]
    dx,dy = landmarks[6,0],landmarks[6,1]
    import math
    from math import degrees
    alpha0 = math.atan2(cy-ay,cx-ax)
    alpha1 = math.atan2(dy-by,dx-bx)
    alpha = alpha1-alpha0
    angle = abs(degrees(alpha))
    angle = 180-angle


    for i in range(1):
      if similarity1<20:
       # print(angle)
        if similarity3<7 and angle < 160 :
          #print('squared shape.Jawlines are more angular')
          message = "Square"
          
          #cv2.putText(image,'Square Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
          break
        else:
          #print('round shape.Jawlines are not that angular')
          message = "Round"
          #cv2.putText(image,'Round Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
          break
      if line4 > line2:
        if angle<160:
          #print('rectangular. face length is largest and jawline are angular ')
          message = "Oblong"
          #cv2.putText(image,'Oblong/Rectangular Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
          break;
        else:
          #print('oblong. face length is largest and jawlines are not angular')
          message = "Oval"
          #cv2.putText(image,'Oval Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
          break;

      if similarity2<20 and angle<160:
        message = "Diamond"
        print('diamond shape. ')
        break
    output = np.concatenate((landmark,results), axis=1)
cv2.putText(image, message + " Face Detected", (50,400 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
cv2.imshow('img',image)

if cv2.waitKey(1) & 0xFF == ord('q'):
    break

if cv2.waitKey(1) and message != "No":
    cv2.imwrite('Results/'+time.strftime("%d-%m-%Y-%H-%M-%S")+'.jpg',output)
    cap.release()
    os.system("python main_project.py -m"+message)
