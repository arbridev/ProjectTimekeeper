## external imports

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
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
from task import Task

## app setup

app = App()
handler = ExcelHandler()

## methods

def newProject():
    projectTitle = simpledialog.askstring("Input", "Project name:", parent=app.master)
    if projectTitle != '' and projectTitle != None:
        path = os.path.join(projectsDir, projectTitle + ".xlsx")
        handler.newWorkbook(path)
        app.changeProjectTitle(path)
        handler.inputScaffold()
        handler.adjustColumn("B", 20)
        handler.adjustColumn("C", 20)
        handler.adjustColumn("D", 40)
        handler.saveWorkbook()
        app.presentTasks(loadTasks())
        setUIState()

def openProject():
    filename = filedialog.askopenfilename(initialdir=os.path.join(appDir, 'projects'), title="Select File", filetypes=(("excel", "*.xlsx"), ("all files", "*.*")))
    if filename != '':
        app.changeProjectTitle(filename)
        handler.openWorkbook(filename)
        app.presentTasks(loadTasks())
        setUIState()

def startTask():
    if handler.filepath == '':
        messagebox.showwarning("Warning","No project selected")
        return
    startCell = handler.getNextEmptyCellDown()
    cell = startCell
    previousCell = handler.getCellAbove(cell)
    if type(previousCell.value) is int:
        cell.value = previousCell.value + 1
    else:
        cell.value = 1
    cell = handler.getCellBeside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.getCellBeside(cell)
    cell = handler.getCellBeside(cell)
    cell.value = app.taskEntry.get("1.0", tk.END)
    insertDivisoryDate(startCell, previousCell)
    handler.saveWorkbook()
    setPreviousDayTotal()
    app.presentTasks(loadTasks())
    setUIState()

def endTask():
    if handler.filepath == '':
        messagebox.showwarning("Warning","No project selected")
        return
    cell = handler.getLastFilledCell()
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
    app.presentTasks(loadTasks())
    setUIState()

def insertDivisoryDate(cell, previousCell):
    if previousCell.is_date == False:
        if previousCell.value == 'Id':
            newRow = cell.row
            handler.insertRow(newRow)
            inputDivisoryDate(newRow)
            return
        lastDateCell = cell.offset(row=-1, column=2)
        newDateCell = cell.offset(column=1)
        lastDate = None
        if lastDateCell.is_date:
            lastDate = lastDateCell.value.date()
        newDate = newDateCell.value.date()
        if newDate != lastDate:
            newRow = cell.row
            handler.insertRow(newRow)
            inputDivisoryDate(newRow)

def inputDivisoryDate(row):
    mergeRange = f'A{str(row)}:E{str(row)}'
    handler.mergeCells(range_string=mergeRange)
    handler.inputDate(datetime.datetime.now().date(), f'A{str(row)}')

def loadTasks():
    tasks = []
    cell = handler.getLastFilledCell()
    if cell.row < 2:
        return tasks
    while type(cell.value) is int:
        cell = handler.getCellAbove(cell)
    cell = handler.getCellBelow(cell)
    while cell.value != None:
        taskCell = cell
        taskId = taskCell.value
        taskCell = handler.getCellBeside(taskCell)
        taskStart = taskCell.value
        taskCell = handler.getCellBeside(taskCell)
        taskEnd = taskCell.value
        taskCell = handler.getCellBeside(taskCell)
        taskDesc = taskCell.value
        task = Task(taskId, start=taskStart, end=taskEnd, description=taskDesc)
        tasks.append(task)
        cell = handler.getCellBelow(cell)
    return tasks

def setUIState(disableTasks=False):
    startBtnDisabled = False
    endBtnDisabled = False
    if disableTasks == True:
        app.setStartTaskBtn(startTask, disabled=True)
        app.setEndTaskBtn(endTask, disabled=True)
        return
    cell = handler.getLastFilledCell()
    cell = handler.getCellBeside(cell)
    endDateCell = handler.getCellBeside(cell) # last end date cell
    if endDateCell.value == None:
        startBtnDisabled = True
        endBtnDisabled = False
    else:
        startBtnDisabled = False
        endBtnDisabled = True
    app.setStartTaskBtn(startTask, disabled=startBtnDisabled)
    app.setEndTaskBtn(endTask, disabled=endBtnDisabled)

def setPreviousDayTotal():
    lastCell = handler.getLastFilledCell()
    lastCell = handler.getCellAbove(lastCell)
    if lastCell.is_date == True:
        sumCells = []
        lastCell = handler.getCellAbove(lastCell)
        while lastCell.is_date == False:
            sumCells.append(lastCell)
            lastCell = handler.getCellAbove(lastCell)
        sumCells.reverse()
        formulae = '=Sum(' + sumCells[0].offset(column=4).coordinate + ':' + sumCells.pop().offset(column=4).coordinate + ')'
        totalCell = lastCell.offset(column=5)
        totalCell.value = datetime.time()
        totalCell.value = formulae
        handler.saveWorkbook()
        


## main execution

app.setCommands(newProject, openProject, startTask, endTask)

setUIState(disableTasks=True)

app.mainloop()

handler.close()