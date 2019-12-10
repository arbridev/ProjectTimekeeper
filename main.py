## external imports

import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import sys
import datetime

## setup

appDir = os.path.dirname(os.path.realpath(__file__))
projectsDir = os.path.join(appDir, "projects")

os.chdir(appDir)
sys.path.insert(1, os.getcwd())

## internal imports

from appui import App
from excel import ExcelHandler

## app setup

app = App()
app.setup()

root = app.master

handler = ExcelHandler()

## helper functions

def newProject():
    projectTitle = simpledialog.askstring("Input", "Project name:", parent=root)
    if projectTitle != '':
        changeProjectTitle(projectTitle, projectLbl)
        path = os.path.join(projectsDir, projectTitle + ".xlsx")
        handler.newWorkbook(path)
        handler.inputScaffold()

def openProject(projectLbl):
    filename = filedialog.askopenfilename(initialdir=os.path.join(appDir, 'projects'), title="Select File", filetypes=(("excel", "*.xlsx"), ("all files", "*.*")))
    if filename != '':
        changeProjectTitle(filename, projectLbl)
        handler.openWorkbook(filename)

def changeProjectTitle(title, projectLbl):
    projectLbl.destroy()
    projectLbl = tk.Label(projectTitleFrm, text=title, fg="black", bg="red")
    projectLbl.pack()

def startTask(taskEntry):
    cell = handler.getNextEmptyCellDown()
    previousCell = handler.getCellAbove(cell)
    if type(previousCell.value) is int:
        cell.value = int(previousCell.value) + 1
    else:
        cell.value = 1
    cell = handler.getCellBeside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.getCellBeside(cell)
    cell.value = 'START'
    cell = handler.getCellBeside(cell)
    cell.value = taskEntry.get("1.0", tk.END)
    handler.saveWorkbook()

def endTask(taskEntry):
    cell = handler.getNextEmptyCellDown()
    previousCell = handler.getCellAbove(cell)
    if type(previousCell.value) is int:
        cell.value = int(previousCell.value) + 1
    else:
        cell.value = 1
    cell = handler.getCellBeside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.getCellBeside(cell)
    cell.value = 'END'
    cell = handler.getCellBeside(cell)
    cell.value = taskEntry.get("1.0", tk.END)
    handler.saveWorkbook()

## main execution

projectTitle = 'NO PROJECT SELECTED'

projectTitleFrm = tk.Frame(root, bg="gray")
projectTitleFrm.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.0)

projectLbl = tk.Label(projectTitleFrm, text=projectTitle, fg="black", bg="red")
projectLbl.pack()

tasksframe = tk.Frame(root, bg="white")
tasksframe.place(relwidth=0.8, relheight=0.7, relx=0.2, rely=0.1)

buttonPanel = tk.Frame(root, bg="gray")
buttonPanel.place(relwidth=0.2, relheight=1.0, relx=0.0, rely=0.0)

newProjectBtn = tk.Button(buttonPanel, text="New Project", padx=10, pady=5, fg="black", bg="blue", command=lambda: newProject())
newProjectBtn.pack()

openProjectBtn = tk.Button(buttonPanel, text="Open Project", padx=10, pady=5, fg="black", bg="blue", command=lambda: openProject(projectLbl))
openProjectBtn.pack()

taskButtonSection = tk.Frame(buttonPanel, bg="gray")
taskButtonSection.place(relwidth=1.0, relheight=0.2, relx=0.0, rely=0.8)

taskPanel = tk.Frame(root, bg="gray", padx=10, pady=5)
taskPanel.place(relwidth=0.8, relheight=0.2, relx=0.2, rely=0.8)
tk.Label(taskPanel, text="Task:").pack()
taskEntry = tk.Text(taskPanel)
taskEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

startTaskBtn = tk.Button(taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42", command=lambda: startTask(taskEntry))
startTaskBtn.pack()

endTaskBtn = tk.Button(taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42", command=lambda: endTask(taskEntry))
endTaskBtn.pack()

root.mainloop()

handler.close()