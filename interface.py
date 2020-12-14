from tkinter import *
import os
from PIL import Image, ImageTk
import glob
from functools import partial
import tkinter.font as tkFont


window = Tk()
window.title("Face Shape Detection and Sunglass Selection")
#window.geometry("600x430") #Width x Height
fontStyle = tkFont.Font(family="Times New Roman", size = 35, weight = "bold")

main_frame = Frame(window)
manual_frame = Frame(window)

#f4 = Frame(root)

for frame in (main_frame, manual_frame):
    frame.grid(row=0, column=0, sticky='news')
    #frame.pack(expand = True, fill = 'both')


def raise_frame(frame):
    frame.tkraise()

def predict():
    os.system("python faceshape_interface.py")


head_label = Label(main_frame,text = "Face Shape Detection \n and\n Sunglass Selection", font = fontStyle)
#head_label.config(font=("Courier", 44))
head_label.grid(row= 1, column=1, columnspan=2)

#-----------MAIN_FRAME---------
# img1 = PhotoImage(file = "p-1.png")
# img1 = img1.zoom(25) #with 250, I ended up running out of memory
# img1 = img1.subsample(59) #mechanically, here it is adjusted to 59 instead of 590
width = 250
height = 250
img_1 = Image.open("p-1.png")
img_1 = img_1.resize((width,height), Image.ANTIALIAS)
img_1 =  ImageTk.PhotoImage(img_1)

btn_predict = Button(main_frame, text = "Detect Face Shape",image = img_1, compound = TOP, command = predict)

img_2 = Image.open("q.jpg")
img_2 = img_2.resize((width,height), Image.ANTIALIAS)
img_2 =  ImageTk.PhotoImage(img_2)
btn_tryall = Button(main_frame, text = "Select Manually",image = img_2, compound = TOP, command = lambda:raise_frame(manual_frame))


width = 100
height = 40
exit = Image.open("exit.png")
exit = exit.resize((width,height), Image.ANTIALIAS)
exit =  ImageTk.PhotoImage(exit)
btn_exit = Button(main_frame, text = "Exit",image = exit, command=window.destroy)


btn_predict.grid(row = 2, column = 1, padx=(30, 0), pady=(20, 0))
btn_tryall.grid(row = 2, column = 2, padx=(20, 0), pady=(20, 0))

btn_exit.grid(row = 3, column=2, padx=(200, 0), pady=(30, 0))


#------------manual_frame------------

def selection(n):
    message = n
    print(message)
    if message == 'No':
        os.system("python main_project.py -m" + message)
    else:
        os.system("python FACESHAPE_GUI.py -m"+message)



head_label = Label(manual_frame, text = "Manual Selection", font = fontStyle)
head_label.config(font=("Courier", 44))
head_label.grid(row= 0, column=0, columnspan=8)

folder_list = []

x=1
y=0
for folder_name in glob.glob('Sunglass/*'): #assuming gif
        
    txt = folder_name
    n = txt.split("\\")
    message = n[1]
    #print(message)
    filename = message + ".png"
    #print(filename)
    load=Image.open(filename)
    load = load.resize((200, 200), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Button(manual_frame, text = message, image = render, compound="top", command = partial(selection, message))
        
        #print(img)
    img.image = render
    img.grid(row = x, column = y, padx=(10, 0))
#print(y)
    y = y + 1
    if y == 3:
        x = x + 1
        y = 0

    folder_list.append(load)

width = 200
height = 200
img = Image.open("q.jpg")
img = img.resize((width,height), Image.ANTIALIAS)
img1 =  ImageTk.PhotoImage(img)
message = 'No'
btn_predict = Button(manual_frame, text = "Try All",image = img1, compound = TOP, command = partial(selection, message))
btn_predict.grid(row = x, column = y, padx=(10, 0))


fontStyle = tkFont.Font(family="Times New Roman", size = 20, weight = "bold")
btn_exit = Button(manual_frame, text = "Back", height = 1, width = 4, font = fontStyle, command=lambda:raise_frame(main_frame))

btn_exit.grid(row = 2, column= 2)

raise_frame(main_frame)

window.mainloop()

