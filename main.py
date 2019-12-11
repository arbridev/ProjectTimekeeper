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
handler = ExcelHandler()

## helper functions

def newProject():
    projectTitle = simpledialog.askstring("Input", "Project name:", parent=app.master)
    if projectTitle != '':
        app.changeProjectTitle(projectTitle)
        path = os.path.join(projectsDir, projectTitle + ".xlsx")
        handler.newWorkbook(path)
        handler.inputScaffold()
        handler.adjustColumn("B", 20)
        handler.adjustColumn("C", 20)
        handler.adjustColumn("D", 40)
        handler.saveWorkbook()

def openProject():
    filename = filedialog.askopenfilename(initialdir=os.path.join(appDir, 'projects'), title="Select File", filetypes=(("excel", "*.xlsx"), ("all files", "*.*")))
    if filename != '':
        app.changeProjectTitle(filename)
        handler.openWorkbook(filename)

def startTask():
    cell = handler.getNextEmptyCellDown()
    previousCell = handler.getCellAbove(cell)
    if type(previousCell.value) is int:
        cell.value = int(previousCell.value) + 1
    else:
        cell.value = 1
    cell = handler.getCellBeside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.getCellBeside(cell)
    cell = handler.getCellBeside(cell)
    cell.value = app.taskEntry.get("1.0", tk.END)
    handler.saveWorkbook()

def endTask():
    cell = handler.getLastFillCellDown()
    previousCell = handler.getCellAbove(cell)
    if type(previousCell.value) is int:
        cell.value = int(previousCell.value) + 1
    else:
        cell.value = 1
    cell = handler.getCellBeside(cell)
    cell = handler.getCellBeside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.getCellBeside(cell)
    cell.value = app.taskEntry.get("1.0", tk.END)
    # handler.adjustCell(cell, verticalAlignment="center")
    cell = handler.getCellBeside(cell)
    cellRow = str(cell.row)
    cell.value = datetime.time()
    cell.value = f"=C{cellRow}-B{cellRow}"
    handler.adjustRow(cell.row, 20)
    handler.saveWorkbook()

## main execution

app.setCommands(newProject, openProject, startTask, endTask)

app.mainloop()

handler.close()