import argparse
from tkinter import *
import glob
from PIL import Image, ImageTk
import numpy as np #for mathematical calculations
import cv2 #for face detection and other image operations
#import dlib #for detection of facial landmarks ex:nose,jawline,eyes


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--message", required=True,
    help="name of the user")
args = vars(ap.parse_args())
message = format(args["message"])

#message  = 'Oval/1.png'
#print(message)

root = Tk()
root.title("Sunglass Tester")




#root.geometry('950x500')

if message == 'No':
    i_list = glob.glob("Sunglass/**/*.png")
else:
    check = '.'
    if check in message:
        i_list = glob.glob("Sunglass/" + message)
    else:            
        
        i_list = glob.glob("Sunglass/" + message +"/*.png")
        

lent = len(i_list)
img_list = [j for j in range(lent)]

for l in range(lent):
    img = Image.open(i_list[l])
    img = img.resize((250, 100), Image.ANTIALIAS) ## The (250, 100) is (width, height)
    img_list[l] = ImageTk.PhotoImage(img)

i_no = 0

label = Label(image=img_list[0])
label.grid(row=1, column=0, columnspan=3)



def forward(image_no):
    global i_no
    global label
    global btn_forward
    global btn_back



    label.grid_forget()
    label = Label(image=img_list[image_no])
    btn_forward = Button(root, text=">>", command=lambda:forward(image_no+1))
    btn_back = Button(root, text="<<", command=lambda:forward(image_no-1))

    if image_no == lent-1:
        btn_forward = Button(root, text=">>",state=DISABLED)
    if image_no == 0:
        btn_back = Button(root, text="<<", state=DISABLED)

    label.grid(row= 1, column=0, columnspan=3)
    btn_back.grid(row= 2 , column = 0)
    btn_forward.grid(row= 2 , column = 2)
    i_no = image_no


btn_back = Button(root, text = "<<", command =forward, state=DISABLED)
btn_exit = Button(root, text = "Exit", command=root.destroy)
btn_forward = Button(root, text = ">>", command = lambda: forward(1))
#btn_predict = Button(root,text = "Predict Face Shape", command = lambda: predict())

btn_back.grid(row = 2 , column = 0)
btn_exit.grid(row = 2 , column = 1)
btn_forward.grid(row = 2 , column = 2)
#btn_predict.grid(row = 1, column = 3, columnspan = 2)



width, height = 600, 300
#url = 'http://192.168.254.186:8080/video'
cap = cv2.VideoCapture(1)
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
lmain.grid(row=0, column=0,columnspan=5)

# xml files describing our haar cascade classifiers
faceCascadeFilePath ="Cascade files/haarcascade_frontalface_default.xml"
noseCascadeFilePath ="Cascade files/haarcascade_mcs_nose_default.xml"
    # build our cv2 Cascade Classifiers
faceCascade = cv2.CascadeClassifier(faceCascadeFilePath)
noseCascade = cv2.CascadeClassifier(noseCascadeFilePath)
eye_cascade = cv2.CascadeClassifier('Cascade files/haarcascade_eye.xml')

if faceCascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

if noseCascade.empty():
    raise IOError('Unable to load the nose cascade classifier xml file')

if eye_cascade.empty():
    raise IOError('Unable to load the eye cascade classifier xml file')



def show_frame():

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # Create greyscale image from the video feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in input video stream
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

   # Iterate over each face found
    for (x, y, w, h) in faces:
        # Un-comment the next line for debug (draw box around all faces)
        face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)


        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Load our overlay image: sunglass.png
        i = i_list[i_no]
        imgsunglass = cv2.imread(i, -1)   #read unchanged image with transparancy
        #print(imgsunglass)

        # Creating the mask for the sunglass
        orig_mask = imgsunglass[:,:,3]
        # Create the inverted mask for the sunglass
        orig_mask_inv = cv2.bitwise_not(orig_mask)

        # Convert sunglass image to BGR and save the original image size (used later when re-sizing the image)
        imgsunglass = imgsunglass[:,:,0:3]
        origsunglassHeight, origsunglassWidth = imgsunglass.shape[:2] # take sunglass height and width

        eyes = eye_cascade.detectMultiScale(roi_gray,scaleFactor = 1.5, minNeighbors = 5)
        ley = 0
        for (ex,ey,ew,eh) in eyes:
            if ex < w/2: #left eye
                #cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
                lex, ley, lew, leh = ex, ey, ew, eh

            else:   #right eye
                #cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (255,0,0), 2)
                rex, rey, rew, reh = ex, ey, ew, eh

        #-----------------------------------------------------------------------------
        # Detect a nose within the region bounded by each face (the ROI)
        nose = noseCascade.detectMultiScale(roi_gray)
        for (nx,ny,nw,nh) in nose:
            # Un-comment the next line for debug (draw box around the nose)
            #print("ley = ", ley, "ny = ", ny)
            if (ley > ny or ny < 50):
                break
            #cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,0,255),2)
            
            # The sunglass should be three times the width of the nose
            sunglassWidth =  2.5 * nw
            print(sunglassWidth)
            sunglassHeight = (sunglassWidth * origsunglassHeight / origsunglassWidth)
            # Center the Sunglass on the Top of the nose
            x1 = int(nx - (sunglassWidth/3))
            x2 = int(nx + nw + (sunglassWidth / 3)+7)
            y1 = int(ny - (sunglassHeight/2)-10)
            y2 = int(ny + (sunglassHeight/2)-5)

            # Check for clipping
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > w:
                x2 = w
            if y2 > h:
                y2 = h

            # Re-calculate the width and height of the sunglass image
            sunglassWidth = x2 - x1
            sunglassHeight = y2 - y1

            # Re-size the original image and the masks to the sunglass sizes
            # calcualted above
            sunglass = cv2.resize(imgsunglass, (sunglassWidth,sunglassHeight), interpolation = cv2.INTER_CUBIC)
            mask = cv2.resize(orig_mask, (sunglassWidth,sunglassHeight), interpolation = cv2.INTER_CUBIC)
            mask_inv = cv2.resize(orig_mask_inv, (sunglassWidth,sunglassHeight), interpolation = cv2.INTER_AREA)

            # take ROI for Sunglass from background equal to size of Sunglass image
            roi = roi_color[y1:y2, x1:x2]

            # roi_bg contains the original image only where the sunglass is not in the region that is the size of the Sunglass.

            roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

            # roi_fg contains the image of the Sunglass only where the sunglass is
            roi_fg = cv2.bitwise_and(sunglass,sunglass,mask = mask)

            # join the roi_bg and roi_fg
            dst = cv2.add(roi_bg,roi_fg)
            # place the joined image, saved to dst back over the original image
            roi_color[y1:y2, x1:x2] = dst


    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(100, show_frame)
    
show_frame()

root.mainloop()
cap.release()
