import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import sys

## setup
appDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(appDir)
sys.path.insert(1, os.getcwd())

## internal imports
from appui import App

## app setup

app = App()
app.setup()
        
root = app.master

## helper functions

def newProject():
    projectTitle = simpledialog.askstring("Input", "Project name:", parent=root)
    if projectTitle != '':
        changeProjectTitle(projectTitle, projectLbl)

def openProject(projectLbl):
    filename = filedialog.askopenfilename(initialdir=os.path.join(appDir, 'projects'), title="Select File", filetypes=(("excel", "*.xlsx"), ("all files", "*.*")))
    if filename != '':
        changeProjectTitle(filename, projectLbl)

def changeProjectTitle(title, projectLbl):
    projectLbl.destroy()
    projectLbl = tk.Label(projectTitleFrm, text=title, fg="black", bg="red")
    projectLbl.pack()

def startTask():
    print('startTask')

def endTask():
    print('endTask')

## main execution

projectTitle = 'NO PROJECT SELECTED'

projectTitleFrm = tk.Frame(root, bg="gray")
projectTitleFrm.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.0)

projectLbl = tk.Label(projectTitleFrm, text=projectTitle, fg="black", bg="red")
projectLbl.pack()

tasksframe = tk.Frame(root, bg="white")
tasksframe.place(relwidth=0.8, relheight=0.7, relx=0.2, rely=0.1)

buttonPanel = tk.Frame(root, bg="green")
buttonPanel.place(relwidth=0.2, relheight=1.0, relx=0.0, rely=0.0)

newProjectBtn = tk.Button(buttonPanel, text="New Project", padx=10, pady=5, fg="black", bg="blue", command=lambda: newProject())
newProjectBtn.pack()

openProjectBtn = tk.Button(buttonPanel, text="Open Project", padx=10, pady=5, fg="black", bg="blue", command=lambda: openProject(projectLbl))
openProjectBtn.pack()

taskButtonSection = tk.Frame(buttonPanel, bg="red")
taskButtonSection.place(relwidth=1.0, relheight=0.2, relx=0.0, rely=0.8)

startTaskBtn = tk.Button(taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42", command=startTask)
startTaskBtn.pack()

endTaskBtn = tk.Button(taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42", command=endTask)
endTaskBtn.pack()

root.mainloop()