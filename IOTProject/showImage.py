# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:30:08 2019

@author: Lab-722
"""

import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk
import requests
from io import BytesIO

def showPIL(pilImage):
    print("ShowPIL")
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()
url = "http://images6.fanpop.com/image/photos/43000000/Frozen-2-Japanese-Character-Poster-Elsa-frozen-2-43046128-678-960.jpg"
#url = "https://heroichollywood.com/wp-content/uploads/2019/08/Frozen-2-Elsa.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
#pilImage = Image.open("elsa.jpg")
#showPIL(img)