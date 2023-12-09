"""
/***************************************************************
* Name : TaskManagerFinal
* Author: Kai Huynh
* Created : 11/1/2023
* Course: CIS 152 - Data Structure
* Version: 17.0.5
* OS: Windows 11
* IDE: Pycharm 2022
* Copyright : This is my own original work
* based onspecifications issued by our instructor
* Description : The Simple Task Manager program, is a program developed with Python, that has options for adding tasks,
* sorting tasks based on date added or priority, and deleting tasks. All of these remain responsive, updating in real time
* through a user-friendly GUI. Not only can users add, delete, and sort tasks from the GUI, tasks are also updated real-time,
* allowing users to edit the name, and the description of the tasks.
*            Input: Task Name, Priority, Task Description, Task Category
*            Ouput: Outputs Task List
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified. I have not given other fellow student(s) access
* to my program.
***************************************************************
"""
import tkinter as tk
from TaskManagerClass import TaskManager

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()


    
