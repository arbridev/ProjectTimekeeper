## external imports

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import sys
import datetime

## setup

appDir = os.path.dirname(os.path.realpath(__file__))
projectsdir = os.path.join(appDir, "projects")

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

def new_project():
    project_title = simpledialog.askstring("Input", "Project name:", parent=app.master)
    if project_title != '' and project_title != None:
        path = os.path.join(projectsdir, project_title + ".xlsx")
        handler.new_workbook(path)
        app.change_project_title(os.path.basename(path))
        handler.input_scaffold()
        handler.adjust_column("B", 20)
        handler.adjust_column("C", 20)
        handler.adjust_column("D", 40)
        handler.save_workbook()
        app.present_tasks(load_tasks())
        set_ui_state()

def open_project():
    filename = filedialog.askopenfilename(
        initialdir=os.path.join(appDir, 'projects'), 
        title="Select File", 
        filetypes=(("excel", "*.xlsx"), ("all files", "*.*")))
    if filename != '':
        app.change_project_title(os.path.basename(filename))
        handler.open_workbook(filename)
        app.present_tasks(load_tasks())
        set_ui_state()
        set_project_total()

def start_task():
    if handler.filepath == '':
        messagebox.showwarning("Warning","No project selected")
        return
    startcell = handler.get_next_empty_cell_down()
    cell = startcell
    previouscell = handler.get_cell_above(cell)
    if type(previouscell.value) is int:
        cell.value = previouscell.value + 1
    else:
        cell.value = 1
    cell = handler.get_cell_beside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.get_cell_beside(cell)
    cell = handler.get_cell_beside(cell)
    cell.value = app.taskEntry.get("1.0", tk.END)
    insert_divisory_date(startcell, previouscell)
    handler.save_workbook()
    app.present_tasks(load_tasks())
    set_ui_state()

def end_task():
    if handler.filepath == '':
        messagebox.showwarning("Warning","No project selected")
        return
    cell = handler.get_last_filled_cell_vertically()
    cell = handler.get_cell_beside(cell)
    cell = handler.get_cell_beside(cell)
    cell.value = datetime.datetime.now()
    cell = handler.get_cell_beside(cell)
    cell.value = app.taskEntry.get("1.0", tk.END)
    # handler.adjustCell(cell, verticalAlignment="center")
    cell = handler.get_cell_beside(cell)
    cellRow = str(cell.row)
    cell.value = datetime.time()
    cell.value = f"=C{cellRow}-B{cellRow}"
    handler.adjust_row(cell.row, 20)
    handler.save_workbook()
    set_day_total()
    set_project_total()
    app.present_tasks(load_tasks())
    set_ui_state()

def insert_divisory_date(cell, previouscell):
    if previouscell.is_date == False:
        if previouscell.value == 'Id':
            newrow = cell.row
            handler.insert_row(newrow)
            input_divisory_date(newrow)
            return
        lastdatecell = cell.offset(row=-1, column=2)
        newdatecell = cell.offset(column=1)
        lastdate = None
        if lastdatecell.is_date:
            lastdate = lastdatecell.value.date()
        newdate = newdatecell.value.date()
        if newdate != lastdate:
            newrow = cell.row
            handler.insert_row(newrow)
            input_divisory_date(newrow)

def input_divisory_date(row):
    merge_range = f'A{str(row)}:E{str(row)}'
    handler.merge_cells(range_string=merge_range)
    handler.input_date(datetime.datetime.now().date(), f'A{str(row)}')

def load_tasks():
    tasks = []
    cell = handler.get_last_filled_cell_vertically()
    if cell.row < 2:
        return tasks
    while type(cell.value) is int:
        cell = handler.get_cell_above(cell)
    cell = handler.get_cell_below(cell)
    while cell.value != None:
        taskcell = cell
        taskId = taskcell.value
        taskcell = handler.get_cell_beside(taskcell)
        taskstart = taskcell.value
        taskcell = handler.get_cell_beside(taskcell)
        taskend = taskcell.value
        taskcell = handler.get_cell_beside(taskcell)
        taskdesc = taskcell.value
        task = Task(taskId, start=taskstart, end=taskend, description=taskdesc)
        tasks.append(task)
        cell = handler.get_cell_below(cell)
    return tasks

def set_ui_state(disabletasks=False):
    start_btn_disabled = False
    end_btn_disabled = False
    if disabletasks == True:
        app.set_start_task_btn(start_task, disabled=True)
        app.set_end_task_btn(end_task, disabled=True)
        return
    cell = handler.get_last_filled_cell_vertically()
    cell = handler.get_cell_beside(cell)
    enddatecell = handler.get_cell_beside(cell) # last end date cell
    if enddatecell.value == None:
        start_btn_disabled = True
        end_btn_disabled = False
    else:
        start_btn_disabled = False
        end_btn_disabled = True
    app.set_start_task_btn(start_task, disabled=start_btn_disabled)
    app.set_end_task_btn(end_task, disabled=end_btn_disabled)

def set_day_total():
    lastcell = handler.get_last_filled_cell_vertically()
    targetcell = lastcell
    while targetcell.is_date == False:
        targetcell = handler.get_cell_above(targetcell)
    topcellcoord = handler.get_cell_below(targetcell).offset(column=4).coordinate
    bottomcellcoord = lastcell.offset(column=4).coordinate
    formulae = '=Sum(' + topcellcoord + ':' + bottomcellcoord + ')'
    totalcell = targetcell.offset(column=5)
    totalcell.value = datetime.time()
    totalcell.value = formulae
    handler.save_workbook()

def set_project_total():
    column = handler.get_column('F')
    lastcell = column[len(column)-1]
    bottomcellcoord = lastcell.coordinate
    formulae = '=Sum(F2:' + bottomcellcoord + ')'
    totalcell = handler.get_cell('F1')
    totalcell.value = datetime.time()
    totalcell.value = formulae
    handler.apply_bold(totalcell)
    handler.apply_center(totalcell)
    handler.save_workbook()


## main execution

app.set_commands(new_project, open_project, start_task, end_task)

set_ui_state(disabletasks=True)

app.mainloop()

handler.close()