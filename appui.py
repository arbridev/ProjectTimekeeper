import tkinter as tk
import datetime
from task import Task

class App(tk.Frame):

    project_title_frm = None
    project_lbl = None
    tasksframe = None
    tasklist = None
    button_panel = None
    new_project_btn = None
    open_project_btn = None
    task_button_section = None
    taskpanel = None
    start_task_btn = None
    end_task_btn = None

    __lightgray = "#AAAAAA"
    __bggray = "#E9E9E9"
    __darkgray = "#333339"
    __blue = "#000080"
    __red = "#800000"

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.setup()

    def setup(self):
        root = self.master
        
        # prevent window resizing
        root.resizable(False, False)

        s_width = root.winfo_screenwidth()
        s_height = root.winfo_screenheight()

        w_width = s_width/2
        w_height = s_height/2

        canvas = tk.Canvas(root, height=w_height, width=w_width, bg=self.__bggray)
        canvas.pack()

        # calculate x and y coordinates for the Tk root window
        x = (s_width/2) - (w_width/2)
        y = (s_height/2) - (w_height/2)

        # set the dimensions of the screen 
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y))

        root.title('Project Timekeeper')

        projectTitle = 'NO PROJECT SELECTED'

        self.project_title_frm = tk.Frame(root, bg=self.__bggray)
        self.project_title_frm.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.0)
        
        self.project_lbl = tk.Label(self.project_title_frm, text=projectTitle, fg="black", bg=self.__bggray)
        self.project_lbl.pack(expand=True)

        self.tasksframe = tk.Frame(root, bg="white")
        self.tasksframe.place(relwidth=0.76, relheight=0.5, relx=0.22, rely=0.1)

        self.tasklist = tk.Listbox(self.tasksframe)
        self.tasklist.pack(expand=True, fill=tk.BOTH)

        self.button_panel = tk.Frame(root, bg=self.__bggray)
        self.button_panel.place(relwidth=0.2, relheight=1.0, relx=0.0, rely=0.0)
        
        self.set_new_project_btn(None)
        
        self.set_open_project_btn(None)

        self.task_button_section = tk.Frame(self.button_panel, bg=self.__bggray)
        self.task_button_section.place(relwidth=1.0, relheight=0.4, relx=0.0, rely=0.6)
        
        self.taskpanel = tk.Frame(root, bg=self.__bggray, padx=10, pady=5)
        self.taskpanel.place(relwidth=0.8, relheight=0.35, relx=0.2, rely=0.6)
        tk.Label(self.taskpanel, text="TASK DESCRIPTION:", bg=self.__bggray).pack()
        self.taskEntry = tk.Text(self.taskpanel)
        self.taskEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        
        self.set_start_task_btn(None)
        
        self.set_end_task_btn(None)
    
    def change_project_title(self, title):
        self.project_lbl.destroy()
        self.project_lbl = tk.Label(self.project_title_frm, text=title, fg="black", bg=self.__bggray)
        self.project_lbl.pack(expand=True)

    def set_commands(self, newproject, openproject, starttask, endtask):
        self.set_new_project_btn(newproject)
        self.set_open_project_btn(openproject)
        self.set_start_task_btn(starttask)
        self.set_end_task_btn(endtask)

    def set_new_project_btn(self, newproject: tk.Button):
        if newproject != None:
            self.new_project_btn.destroy()
        self.new_project_btn = tk.Button(self.button_panel, text="New Project", padx=10, pady=5, fg="black", bg=self.__lightgray, command=newproject)
        self.new_project_btn.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.05)

    def set_open_project_btn(self, openproject):
        if openproject != None:
            self.open_project_btn.destroy()
        self.open_project_btn = tk.Button(self.button_panel, text="Open Project", padx=10, pady=5, fg="black", bg=self.__lightgray, command=openproject)
        self.open_project_btn.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.15)

    def set_start_task_btn(self, starttask, disabled=False):
        color = self.__blue
        if starttask != None:
            self.start_task_btn.destroy()
        state = tk.NORMAL
        if disabled == True:
            state = tk.DISABLED
            color = self.__darkgray
        self.start_task_btn = tk.Button(self.task_button_section, text="Start", padx=10, pady=5, fg="white", bg=color, command=starttask, state=state)
        self.start_task_btn.place(relwidth=0.8, relheight=0.3, relx=0.1, rely=0.2)

    def set_end_task_btn(self, endtask, disabled=False):
        color = self.__red
        if endtask != None:
            self.end_task_btn.destroy()
        state = tk.NORMAL
        if disabled == True:
            state = tk.DISABLED
            color = self.__darkgray
        self.end_task_btn = tk.Button(self.task_button_section, text="End", padx=10, pady=5, fg="white", bg=color, command=endtask, state=state)
        self.end_task_btn.place(relwidth=0.8, relheight=0.3, relx=0.1, rely=0.5)

    def present_tasks(self, tasks):
        self.clear_tasks()
        index = 1
        for task in tasks:
            text = f'{task.id} - Start: '
            if task.start != None:
                text += f'{task.start.strftime("%H:%M:%S")}'
            text += ' | End: '
            if task.end != None:
                text += f'{task.end.strftime("%H:%M:%S")}'
            text += ' | Desc: '
            if task.description != None:
                truncdesc = (task.description[:30] + '..') if len(task.description) > 30 else task.description
                text += f'{truncdesc}'
            text += ' | Duration: '
            if task.start != None and task.end != None:
                delta = task.end - task.start
                text += str(self.format_timedelta(delta))
            self.tasklist.insert(index, text)
            index += 1

    def clear_tasks(self):
        self.tasklist.delete(0, last=self.tasklist.size())

    def format_timedelta(self, timedelta):
        return self.chop_microseconds(timedelta)

    def chop_microseconds(self, timedelta):
        return timedelta - datetime.timedelta(microseconds=timedelta.microseconds)
            

    
