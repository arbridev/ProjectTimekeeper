import tkinter as tk
from tkinter import filedialog, Text
import os
import sys

## setup
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, os.getcwd())

## internal imports
from appui import App

## helper functions

def openProject():
    print('openProject')

def startTask():
    print('startTask')

def endTask():
    print('endTask')

## main execution

app = App()
app.setup()
        
root = app.master

tasksframe = tk.Frame(root, bg="white")
tasksframe.place(relwidth=0.8, relheight=0.7, relx=0.2, rely=0.1)

buttonPanel = tk.Frame(root, bg="green")
buttonPanel.place(relwidth=0.2, relheight=1.0, relx=0.0, rely=0.0)

openProjectBtn = tk.Button(buttonPanel, text="Open Project", padx=10, pady=5, fg="black", bg="blue", command=openProject)
openProjectBtn.pack()

taskButtonSection = tk.Frame(buttonPanel, bg="red")
taskButtonSection.place(relwidth=1.0, relheight=0.2, relx=0.0, rely=0.8)

startTaskBtn = tk.Button(taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42", command=startTask)
startTaskBtn.pack()

endTaskBtn = tk.Button(taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42", command=endTask)
endTaskBtn.pack()

root.mainloop()