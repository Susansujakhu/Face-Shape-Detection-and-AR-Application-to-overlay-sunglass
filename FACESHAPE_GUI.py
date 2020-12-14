import argparse
from tkinter import *
import glob
import tkinter.font as tkFont
# pip install pillow
from PIL import Image, ImageTk
import tkinter.messagebox
from functools import partial
import os


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--message", required=True,
    help="name of the user")
args = vars(ap.parse_args())
message = format(args["message"])

#print(message)


if '@' in message:
    msg = message
    msg = msg.split('@')
    message = msg[0]
    profile_image ="Results/" + msg[1]
    
else:
    profile_image = message + '.png'
    
image_list = []


def click(n):
    #print(n)
    txt = n
    print(txt)
    x = txt.split("/")
    x = x[1].split("\\")
    message = x[0] + "/" + x[1]
    print(message)
    os.system("python main_project.py -m" + message)


def gall_main(n, which_frame = 'frame_shape'):
    

    x, y= 2, 0 #row,column
    i = 1
    print(which_frame)
    for filename in glob.glob('Sunglass/'+ message +'/*.png'): #assuming gif
        
        if(i<=n):    
            load=Image.open(filename)
            load = load.resize((170, 170), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)
            if(which_frame == 'frame_shape'):
                img = Button(frame_shape, text = "Try", bg = 'white', image = render, compound="top", command = partial(click, filename), relief = RAISED)
            else:
                img = Button(frame_seemore, text = "Try", bg = 'white', image = render, compound="top", command = partial(click, filename), relief = RAISED)
            img.image = render
            img.grid(row = x, column = y, padx = (30, 20), pady = (30, 0))
        #print(y)
            y = y + 1
            if y == 3:
                x = x + 1
                y = 0
    
            image_list.append(load)
            i+=1



def raise_frame(frame):
    frame.tkraise()
    

    
def display_image(image_path, resize_width = 170, resize_height = 170):
    load = Image.open(image_path)
    load = load.resize((resize_width, resize_height), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    return render

root = Tk()
root.title("Gallery")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
w_width = screen_width / 2
w_height = screen_height / 2
#print(w_height, w_width)

x = w_width - (w_width / 2)  
y = w_height - (w_height / 1.2)

root.geometry('699x540''+%d+%d' %(x, y))
#root['background'] = 'green'

#root.configure(bg = 'green')

#root.geometry("{0}x{1}+0+0".format(683, 500))

fontStyle = tkFont.Font(family="Times New Roman", size = 20, weight = "bold")
recommendation_fontstyle = tkFont.Font(family="Times New Roman", size = 16, weight = "bold")
button_fontstyle = tkFont.Font(family="Times New Roman", size = 15, weight = "bold")
message_fontStyle = tkFont.Font(family="Times New Roman", size = 35, weight = "bold")

frame_shape = Frame(root)
frame_seemore = Frame(root)
#f4 = Frame(root)

for frame in (frame_shape,frame_seemore):
    frame.grid(row=0, column=0, sticky='news')
    #frame.pack(expand = True, fill = 'both')

#first frame
shape_image_path = profile_image
faceshape_img = display_image(shape_image_path, 170, 170) 

label_shape = Label(frame_shape, image = faceshape_img)
#.image = display_image(shape_image_path)
label_shape.grid(row = 0, column = 0, padx = (30, 0), pady =(30, 0))
label_faceshape = Label(frame_shape, text = '\nFace Shape:', font = fontStyle)
label_shape = Label(frame_shape, text = message.upper(), font = message_fontStyle).grid(row = 0, column = 2, pady = (25, 0))
label_faceshape.grid(row = 0, column = 1, padx = (5, 0), pady = 0)

#Label(frame_shape, text = 'OVAL', font = fontStyle).grid(row = 0, column = 2)

label_recommendation = Label(frame_shape, text = 'Recommendations', font = recommendation_fontstyle)
label_recommendation.grid(row = 1, column = 0, pady = (30, 0))


gall_main(3)

btn_see_more = Button(frame_shape, text = '...see all...', font = button_fontstyle, command = lambda:raise_frame(frame_seemore))
btn_see_more.grid(row = 3, column = 2, pady = (10, 0), padx = (50, 0))


#second frame
Button(frame_seemore, text='Back', command = lambda:raise_frame(frame_shape)).grid(row = 6, column = 0)
gall_main(6, 'frame_seemore')



raise_frame(frame_shape)
root.mainloop()


