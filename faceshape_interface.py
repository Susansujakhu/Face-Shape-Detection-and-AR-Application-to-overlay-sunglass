import argparse
from tkinter import *
import glob
from PIL import Image, ImageTk
import numpy as np #for mathematical calculations
import cv2 #for face detection and other image operations

import dlib #for detection of facial landmarks ex:nose,jawline,eyes
import imutils

import time
import os


root = Tk()
root.title("Sunglass Tester")

#root.geometry('950x500')

width, height = 600, 500
#url = 'http://192.168.254.186:8080/video'

cap = cv2.VideoCapture(1)
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
lmain.grid(row=0, column=1,columnspan=5)

# xml files describing our haar cascade classifiers
faceCascadeFilePath ="Cascade files/haarcascade_frontalface_default.xml"

#download file path = http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
predictor_path = "shape_predictor_81_face_landmarks.dat/shape_predictor_81_face_landmarks.dat"

faceCascade = cv2.CascadeClassifier(faceCascadeFilePath)
#create the landmark predictor
predictor = dlib.shape_predictor(predictor_path)

if faceCascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

counter = 6
def show_frame():
    global counter
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    fx, fy, fw, fh = 170, 80, 450, 360
    cv2.rectangle(frame ,(fx ,fy) ,(fw ,fh) ,(0,0,255), 2)
    cv2.putText(frame, "Place your Face inside the red Box", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    #resizing the image to 000 cols nd 500 rows
    #image = imutils.resize(image, width=600)
    #making another copy

    #convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
    #message to pass in next window if no face detected
    message = "No"
    
    for (x,y,w,h) in faces:

        #draw a rectangle around the faces
        if x < fx or y < fy or (x + w) > fw or (y + h) > fh:
            break

        #cv2.putText(frame, "Press 'c' to continue...", (300,440 ),fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=1,color=(0,255,0), thickness=2)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        #converting the opencv rectangle coordinates to Dlib rectangle
        dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
        #detecting landmarks
        detected_landmarks = predictor(frame, dlib_rect).parts()
        #converting to np matrix
        landmarks = np.matrix([[p.x,p.y] for p in detected_landmarks])
        #landmarks array contains indices of landmarks.

        #copying the image so that original is saved
        landmark = frame.copy()
        
        
        for idx, point in enumerate(landmarks):
                pos = (point[0,0], point[0,1] )
                #annotate the positions
                cv2.putText(landmark,str(idx),pos,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.4,color=(0,0,255) )
                #draw points on the landmark positions
                cv2.circle(landmark, pos, 3, color=(0,255,255))

        #cv2.imshow("Landmarks", landmark)

#making another copy  for showing final results
        #results = frame.copy()


    #Forehead length
        linepointleft = (landmarks[75,0],landmarks[75,1])
        #print("linepointleft", linepointleft)
        linepointright = (landmarks[79,0],landmarks[79,1]+5)
        #print("linepointright", linepointright)
        line1 = np.subtract(linepointright, linepointleft)[0]

        #print("line1",line1)
        cv2.line(landmark, linepointleft, linepointright, color=(0,255,0), thickness = 2)
        #cv2.putText(landmark,' Line 1',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
        cv2.circle(landmark, linepointleft, 5, color=(255,0,0), thickness=-1)
        cv2.circle(landmark, linepointright, 5, color=(255,0,0), thickness=-1)

    #Distance between cheek bones
        #drawing line 2 with circles
        linepointleft = (landmarks[1,0],landmarks[1,1])
        linepointright = (landmarks[15,0],landmarks[15,1])
        line2 = np.subtract(linepointright,linepointleft)[0]
        cv2.line(landmark, linepointleft,linepointright,color=(0,255,0), thickness = 2)
        #cv2.putText(landmark,' Line 2',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
        cv2.circle(landmark, linepointleft, 5, color=(255,0,0), thickness=-1)
        cv2.circle(landmark, linepointright, 5, color=(255,0,0), thickness=-1)

    #Distance between Jaw lines
        #drawing line 3 with circles
        linepointleft = (landmarks[4,0],landmarks[4,1])
        linepointright = (landmarks[12,0],landmarks[12,1])
        line3 = np.subtract(linepointright,linepointleft)[0]
        
        cv2.line(landmark, linepointleft,linepointright,color=(0,255,0), thickness = 2)
        #cv2.putText(landmark,' Line 3',linepointleft,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
        cv2.circle(landmark, linepointleft, 5, color=(255,0,0), thickness=-1)
        cv2.circle(landmark, linepointright, 5, color=(255,0,0), thickness=-1)

    #Face Length
        #drawing line 4 with circles
        linepointbottom = (landmarks[8,0],landmarks[8,1])
        linepointtop = (landmarks[71,0],landmarks[71,1])
        #linepointtop = (landmarks[8,0],y)
        line4 = np.subtract(linepointbottom,linepointtop)[1]
        cv2.line(landmark,linepointtop,linepointbottom,color=(0,255,0), thickness = 2)
        #cv2.putText(landmark,' Line 4',linepointbottom,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
        cv2.circle(landmark, linepointtop, 5, color=(255,0,0), thickness=-1)
        cv2.circle(landmark, linepointbottom, 5, color=(255,0,0), thickness=-1)


        similarity1 = line4/line2
        
        similarity2 = abs(line3 - line1)

        #print(similarity1)
        #we use length for angle calculation
        
        ax,ay = landmarks[4,0],landmarks[4,1]
        
        bx,by = landmarks[12,0],landmarks[12,1]
        
        
        #cx,cy = landmarks[6,0],landmarks[6,1]
        #dx,dy = landmarks[7,0],landmarks[7,1]
        res = int((bx+ax)/2), int((by+ay)/2)
        cv2.circle(landmark, res, 5, color=(255,0,0), thickness=-1)
        linepointbottom = (landmarks[8,0],landmarks[8,1])
        line5 = np.subtract(res, linepointbottom)[0]
        
        #print(similarity1)
        #print('line2:' + str(line2))
        #print('line4:' + str(line4))
        #print('line5:' + str(line5))
        #print(similarity1)
        cv2.line(landmark, linepointleft,linepointright,color=(0,255,0), thickness = 2)
        for i in range(1):
          if similarity1<1.25:
           # print(angle)
            if line5 <= 0:
              #print('squared shape.Jawlines are more angular')
              message = "Square"         
              #cv2.putText(image,'Square Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
              break
            else:
              #print('round shape.Jawlines are not that angular')
              message = "Round"
              #cv2.putText(image,'Round Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
              break
          else:
            if similarity2 < 10 and similarity1 > 1.35:
              #print('rectangular. face length is largest and jawline are angular ')
              message = "Oblong"
              #cv2.putText(image,'Oblong/Rectangular Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
              break;
            else:
              #print('oblong. face length is largest and jawlines are not angular')
              message = "Oval"
              #cv2.putText(image,'Oval Face detected',(50,300 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
              break;




        #output = np.concatenate((landmark,results), axis=1)
        output = landmark
    #cv2.putText(frame, message + " Face Detected", (50,400 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
    
    if message != "No":
        root.after(1000)    

        counter = counter - 1
        cv2.putText(frame, str(counter), (310,220 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=5,color=(0,255,0), thickness=2)
        cv2.putText(frame, message + " Face Detected", (150,400 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,255), thickness=2)
     
    
        #print(counter)
        if counter == 0:
            #cv2.putText(frame, message + " Face Detected", (50,400 ),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,255,0), thickness=2)
            output = output[80:360, 170:450]
            output_name = time.strftime("%d-%m-%Y-%H-%M-%S")+'.jpg'
            #cv2.imwrite(output_name ,landmark)
            cv2.imwrite('Results/'+ output_name ,output)
            cap.release()
            root.destroy()
            message = message + "@" + output_name
            os.system("python FACESHAPE_GUI.py -m"+message)
           # os.system("python main_project.py -m"+message)
           
    else:
        counter = 6
    
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(100, show_frame)


show_frame()

root.mainloop()
cap.release()
