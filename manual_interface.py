from tkinter import *
import os
from PIL import Image, ImageTk
import argparse
import glob
import tkinter.messagebox
from functools import partial

window = Tk()
window.title("Select Manually")
window.geometry("680x550") #Width x Height

def selection(n):
    message = n
    print(message)
    if message == 'No':
        os.system("python main_project.py -m" + message)
    else:
        os.system("python FACESHAPE_GUI.py -m"+message)



head_label = Label(text = "Sunglass Tester")
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
    img = Button(window, text = message, image = render, compound="top", command = partial(selection, message))
        
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
btn_predict = Button(window, text = "Try All",image = img1, compound = TOP, command = partial(selection, message))
btn_predict.grid(row = x, column = y, padx=(10, 0))

window.mainloop()

