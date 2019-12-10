import tkinter as tk

class App(tk.Frame):

    projectTitleFrm = None
    projectLbl = None
    tasksframe = None
    buttonPanel = None
    newProjectBtn = None
    openProjectBtn = None
    taskButtonSection = None
    taskPanel = None
    startTaskBtn = None
    endTaskBtn = None

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

        canvas = tk.Canvas(root, height=wHeight, width=wWidth, bg="gray")
        canvas.pack()

        # calculate x and y coordinates for the Tk root window
        x = (sWidth/2) - (wWidth/2)
        y = (sHeight/2) - (wHeight/2)

        # set the dimensions of the screen 
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (wWidth, wHeight, x, y))

        root.title('Work Timekeeper')

        projectTitle = 'NO PROJECT SELECTED'

        self.projectTitleFrm = tk.Frame(root, bg="gray")
        self.projectTitleFrm.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.0)

        self.projectLbl = tk.Label(self.projectTitleFrm, text=projectTitle, fg="black", bg="red")
        self.projectLbl.pack()

        self.tasksframe = tk.Frame(root, bg="white")
        self.tasksframe.place(relwidth=0.8, relheight=0.7, relx=0.2, rely=0.1)

        self.buttonPanel = tk.Frame(root, bg="gray")
        self.buttonPanel.place(relwidth=0.2, relheight=1.0, relx=0.0, rely=0.0)

        # self.newProjectBtn = tk.Button(buttonPanel, text="New Project", padx=10, pady=5, fg="black", bg="blue", command=lambda: newProject())
        self.newProjectBtn = tk.Button(self.buttonPanel, text="New Project", padx=10, pady=5, fg="black", bg="blue")
        self.newProjectBtn.pack()

        # self.openProjectBtn = tk.Button(buttonPanel, text="Open Project", padx=10, pady=5, fg="black", bg="blue", command=lambda: openProject(projectLbl))
        self.openProjectBtn = tk.Button(self.buttonPanel, text="Open Project", padx=10, pady=5, fg="black", bg="blue")
        self.openProjectBtn.pack()

        self.taskButtonSection = tk.Frame(self.buttonPanel, bg="gray")
        self.taskButtonSection.place(relwidth=1.0, relheight=0.2, relx=0.0, rely=0.8)

        self.taskPanel = tk.Frame(root, bg="gray", padx=10, pady=5)
        self.taskPanel.place(relwidth=0.8, relheight=0.2, relx=0.2, rely=0.8)
        tk.Label(self.taskPanel, text="Task:").pack()
        self.taskEntry = tk.Text(self.taskPanel)
        self.taskEntry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        # self.startTaskBtn = tk.Button(taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42", command=lambda: startTask(taskEntry))
        self.startTaskBtn = tk.Button(self.taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42")
        self.startTaskBtn.pack()

        # self.endTaskBtn = tk.Button(taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42", command=lambda: endTask(taskEntry))
        self.endTaskBtn = tk.Button(self.taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42")
        self.endTaskBtn.pack()
    
    def changeProjectTitle(self, title):
        self.projectLbl.destroy()
        self.projectLbl = tk.Label(self.projectTitleFrm, text=title, fg="black", bg="red")
        self.projectLbl.pack()

    def setCommands(self, newProject, openProject, startTask, endTask):
        self.newProjectBtn.destroy()
        self.newProjectBtn = tk.Button(self.buttonPanel, text="New Project", padx=10, pady=5, fg="black", bg="blue", command=newProject)
        self.newProjectBtn.pack()
        
        self.openProjectBtn.destroy()
        self.openProjectBtn = tk.Button(self.buttonPanel, text="Open Project", padx=10, pady=5, fg="black", bg="blue", command=openProject)
        self.openProjectBtn.pack()
        
        self.startTaskBtn.destroy()
        self.startTaskBtn = tk.Button(self.taskButtonSection, text="Start", padx=10, pady=5, fg="white", bg="#263D42", command=startTask)
        self.startTaskBtn.pack()
        
        self.endTaskBtn.destroy()
        self.endTaskBtn = tk.Button(self.taskButtonSection, text="End", padx=10, pady=5, fg="white", bg="#263D42", command=endTask)
        self.endTaskBtn.pack()