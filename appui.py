import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

    def setup(self):
        root = self.master
        # prevent window resizing
        root.resizable(False, False)

        sWidth = root.winfo_screenwidth()
        sHeight = root.winfo_screenheight()

        wWidth = sWidth/2
        wHeight = sHeight/2

        canvas = tk.Canvas(root, height=wHeight, width=wWidth, bg="gray")
        canvas.pack()

        # calculate x and y coordinates for the Tk root window
        x = (sWidth/2) - (wWidth/2)
        y = (sHeight/2) - (wHeight/2)

        # set the dimensions of the screen 
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (wWidth, wHeight, x, y))

        root.title('Work Timekeeper')