import argparse
from tkinter import *
import glob
# pip install pillow
from PIL import Image, ImageTk
import tkinter.messagebox
from functools import partial
import os
'''
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--message", required=True,
    help="name of the user")
args = vars(ap.parse_args())
message = format(args["message"])

'''
message = 'No'
print(message)
image_list = []

def click(n):
    #print(n)
    txt = n

    x = txt.split("/")
    x = x[1].split("\\")
    message = x[0] + "/" + x[1]
    print(message)
    os.system("python main_project.py -m" + message)

   
#class Window(Frame):
#    def __init__(self, master=None):
#        Frame.__init__(self, master)
#        self.grid(row = 5, column = 5)
        #self.pack(fill=BOTH, expand=1)
def gall_main():
    x,y = 0,0 #row,column
    for filename in glob.glob('Sunglass/'+ message +'/*.png'): #assuming gif
            
        load=Image.open(filename)
        load = load.resize((250, 250), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Button(root, text = "Try", image = render, compound="top", command = partial(click, filename))
            
            #print(img)
        img.image = render
        img.grid(row = x, column = y)
    #print(y)
        y = y + 1
        if y == 5:
            x = x + 1
            y = 0

        image_list.append(load)



        
root = Tk()
gall_main()
#app = Window(root)
root.wm_title("Gallery window")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# use the next line if you also want to get rid of the titlebar

root.geometry("%dx%d+0+0" % (w, h))
root.configure(bg = 'red')
#root.attributes('-fullscreen', True)

#root.geometry("200x120")
root.mainloop()