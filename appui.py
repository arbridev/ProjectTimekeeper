import tkinter as tk
import datetime
from task import Task

class App(tk.Frame):

    projectTitleFrm = None
    projectLbl = None
    tasksframe = None
    taskList = None
    buttonPanel = None
    newProjectBtn = None
    openProjectBtn = None
    taskButtonSection = None
    taskPanel = None
    startTaskBtn = None
    endTaskBtn = None

    __lightGray = "#AAAAAA"

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.setup()

    def setup(self):
        root = self.master
        
        # prevent window resizing
        root.resizable(False, False)

        sWidth = root.winfo_screenwidth()
        sHeight = root.winfo_screenheight()

        wWidth = sWidth/2
        wHeight = sHeight/2

        canvas = tk.Canvas(root, height=wHeight, width=wWidth, bg=self.__lightGray)
        canvas.pack()

        # calculate x and y coordinates for the Tk root window
        x = (sWidth/2) - (wWidth/2)
        y = (sHeight/2) - (wHeight/2)

        # set the dimensions of the screen 
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (wWidth, wHeight, x, y))

        root.title('Work Timekeeper')

        projectTitle = 'NO PROJECT SELECTED'

        self.projectTitleFrm = tk.Frame(root, bg=self.__lightGray)
        self.projectTitleFrm.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.0)

        self.projectLbl = tk.Label(self.projectTitleFrm, text=projectTitle, fg="black", bg="red")
        self.projectLbl.pack()

        self.tasksframe = tk.Frame(root, bg="white")
        self.tasksframe.place(relwidth=0.76, relheight=0.7, relx=0.22, rely=0.1)

        self.taskList = tk.Listbox(self.tasksframe)
        self.taskList.pack(expand=True, fill=tk.BOTH)

        self.buttonPanel = tk.Frame(root, bg=self.__lightGray)
        self.buttonPanel.place(relwidth=0.2, relheight=1.0, relx=0.0, rely=0.0)
        
        self.setNewProjectBtn(None)
        
        self.setOpenProjectBtn(None)

        self.taskButtonSection = tk.Frame(self.buttonPanel, bg=self.__lightGray)
        self.taskButtonSection.place(relwidth=1.0, relheight=0.2, relx=0.0, rely=0.8)

        self.taskPanel = tk.Frame(root, bg=self.__lightGray, padx=10, pady=5)
        self.taskPanel.place(relwidth=0.8, relheight=0.2, relx=0.2, rely=0.8)
        tk.Label(self.taskPanel, text="TASK DESCRIPTION:", bg=self.__lightGray).pack()
        self.taskEntry = tk.Text(self.taskPanel)
        self.taskEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        
        self.setStartTaskBtn(None)
        
        self.setEndTaskBtn(None)
    
    def changeProjectTitle(self, title):
        self.projectLbl.destroy()
        self.projectLbl = tk.Label(self.projectTitleFrm, text=title, fg="black", bg="red")
        self.projectLbl.pack()

    def setCommands(self, newProject, openProject, startTask, endTask):
        self.setNewProjectBtn(newProject)
        self.setOpenProjectBtn(openProject)
        self.setStartTaskBtn(startTask)
        self.setEndTaskBtn(endTask)

    def setNewProjectBtn(self, newProject):
        if newProject != None:
            self.newProjectBtn.destroy()
        self.newProjectBtn = tk.Button(self.buttonPanel, text="New Project", padx=10, pady=5, fg="white", bg="blue", command=newProject)
        self.newProjectBtn.pack(fill=tk.X)

    def setOpenProjectBtn(self, openProject):
        if openProject != None:
            self.openProjectBtn.destroy()
        self.openProjectBtn = tk.Button(self.buttonPanel, text="Open Project", padx=10, pady=5, fg="white", bg="blue", command=openProject)
        self.openProjectBtn.pack(fill=tk.X)

    def setStartTaskBtn(self, startTask, disabled=False):
        if startTask != None:
            self.startTaskBtn.destroy()
        state = tk.NORMAL
        if disabled == True:
            state = tk.DISABLED
        self.startTaskBtn = tk.Button(self.taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42", command=startTask, state=state)
        self.startTaskBtn.pack(fill=tk.X)

    def setEndTaskBtn(self, endTask, disabled=False):
        if endTask != None:
            self.endTaskBtn.destroy()
        state = tk.NORMAL
        if disabled == True:
            state = tk.DISABLED
        self.endTaskBtn = tk.Button(self.taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42", command=endTask, state=state)
        self.endTaskBtn.pack(fill=tk.X)

    def presentTasks(self, tasks):
        self.clearTasks()
        index = 1
        for task in tasks:
            print(task)
            text = f'{task.id} - Start: '
            if task.start != None:
                text += f'{task.start.strftime("%H:%M:%S")}'
            text += ' | End: '
            if task.end != None:
                text += f'{task.end.strftime("%H:%M:%S")}'
            text += ' | Desc: '
            if task.description != None:
                truncDesc = (task.description[:30] + '..') if len(task.description) > 30 else task.description
                text += f'{truncDesc}'
            text += ' | Duration: '
            if task.start != None and task.end != None:
                delta = task.end - task.start
                text += str(self.formatTimedelta(delta))
            self.taskList.insert(index, text)
            index += 1

    def clearTasks(self):
        self.taskList.delete(0, last=self.taskList.size())

    def formatTimedelta(self, timedelta):
        return self.chop_microseconds(timedelta)

    def chop_microseconds(self, timedelta):
        return timedelta - datetime.timedelta(microseconds=timedelta.microseconds)
            

    
