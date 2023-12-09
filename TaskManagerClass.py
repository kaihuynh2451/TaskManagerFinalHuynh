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
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import heapq

class Task:
    def __init__(self, task, priority, description, category):
        # initializes a task with name, priority, description, category, and the date added
        self.task = task
        self.priority = priority
        self.description = description
        self.category = category
        self.date_added = datetime.now()
        self.prev_task = None
        self.next_task = None

class PriorityQueue:
    # initializes a priority queue using a heap
    def __init__(self):
        self.heap = []

    # pushes a task onto the priority queue
    def push(self, task):
        heapq.heappush(self.heap, (task.priority, task.date_added, task))

    # pops the task with the highest priority from the priority queue
    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[2]

class DoublyLinkedList:

    # initializes a doubly linked list for maintaining the order of tasks
    def __init__(self):
        self.head = None
        self.tail = None

    # appends a task to the doubly linked list
    def append(self, task):
        if not self.head:
            self.head = task
            self.tail = task
        else:
            task.prev_task = self.tail
            self.tail.next_task = task
            self.tail = task

    # removes a task from the doubly linked list
    def remove(self, task):
        if task.prev_task:
            task.prev_task.next_task = task.next_task
        else:
            self.head = task.next_task

        if task.next_task:
            task.next_task.prev_task = task.prev_task
        else:
            self.tail = task.prev_task

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Task Manager")

        # tasks list
        self.task_list = DoublyLinkedList()
        self.priority_queue = PriorityQueue()

        # entry variables
        self.task_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.category_var = tk.StringVar()

        # labels and Entries
        ttk.Label(root, text="Task:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.task_entry = ttk.Entry(root, textvariable=self.task_var, width=40)
        self.task_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(root, text="Priority:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.priority_entry = ttk.Entry(root, textvariable=self.priority_var, width=40)
        self.priority_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.description_entry = ttk.Entry(root, textvariable=self.description_var, width=40)
        self.description_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(root, text="Category:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        # predefined categories dropdown
        self.category_options = ["Work", "Home", "Personal", "Other"]
        self.category_menu = ttk.Combobox(root, textvariable=self.category_var, values=self.category_options)
        self.category_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.category_menu.set("Work")

        # add task button
        add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # edit task button
        edit_button = ttk.Button(root, text="Edit Task", command=self.edit_task)
        edit_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky="e")

        # delete task button
        delete_button = ttk.Button(root, text="Delete Task", command=self.delete_selected_task)
        delete_button.grid(row=5, column=2, columnspan=2, padx=10, pady=10, sticky="e")

        # task treeview
        self.task_treeview = ttk.Treeview(root, columns=("Task", "Priority", "Date Added", "Description", "Category"), show="headings", height=15, selectmode="browse")
        self.task_treeview.grid(row=6, column=0, columnspan=5, padx=10, pady=10, sticky="w")

        self.task_treeview.heading("Task", text="Task", anchor=tk.W)
        self.task_treeview.heading("Priority", text="Priority", anchor=tk.W)
        self.task_treeview.heading("Date Added", text="Date Added", anchor=tk.W)
        self.task_treeview.heading("Description", text="Description", anchor=tk.W)
        self.task_treeview.heading("Category", text="Category", anchor=tk.W)

        # sort options
        ttk.Label(root, text="Sort by:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.sort_option = ttk.Combobox(root, values=["Priority", "Date Added"])
        self.sort_option.grid(row=7, column=1, padx=10, pady=10, sticky="w")
        self.sort_option.set("Priority")

        # sort button
        sort_button = ttk.Button(root, text="Sort", command=self.sort_tasks)
        sort_button.grid(row=7, column=2, columnspan=2, padx=10, pady=10, sticky="w")

        # selecting a task event
        self.task_treeview.bind("<ButtonRelease-1>", self.display_task_details)

        # task details frame
        self.task_details_frame = ttk.Frame(root)
        self.task_details_frame.grid(row=8, column=0, columnspan=5, padx=10, pady=10, sticky="w")

        # task details textbox
        self.task_details_textbox = tk.Text(
            self.task_details_frame, width=60, height=5, wrap="word", state=tk.DISABLED,
            relief="flat", highlightthickness=0, font=("Arial", 12))
        self.task_details_textbox.pack()

    def validate_priority(self, priority):
        try:
            priority_value = int(priority)
            if priority_value <= 0:
                return False
            return True
        except ValueError:
            return False

    def add_task(self):
        # add task to task manager
        task = self.task_var.get()
        priority = self.priority_var.get()
        description = self.description_var.get()
        category = self.category_var.get()

        if task and self.validate_priority(priority):
            date_added = datetime.now()
            new_task = Task(task, priority, description, category)  # Include category
            new_task.date_added = date_added

            # update the doubly linked list
            self.task_list.append(new_task)

            # update the priority queue
            self.priority_queue.push(new_task)

            # update the task treeview
            self.update_task_treeview()

            # clear entry fields
            self.task_var.set("")
            self.priority_var.set("")
            self.description_var.set("")
            self.category_var.set("")
        else:
            messagebox.showwarning("Warning",
                                   "Invalid input. Task name cannot be empty, and priority must be a positive integer!")

    #edit the selected task
    def edit_task(self):
        selected_item = self.task_treeview.selection() # retrieves selected item
        if selected_item: # checks if item is selected
            selected_index = self.task_treeview.index(selected_item)
            if selected_index is not None: # check if invalid
                try:
                    current_task = self.task_list.head
                    for _ in range(selected_index):
                        current_task = current_task.next_task

                    new_task_name = simpledialog.askstring( # prompts to enter new task name
                        "Edit Task", "Enter new task name:", initialvalue=current_task.task
                    )
                    new_description = simpledialog.askstring( # prompts to enter new description
                        "Edit Task", "Enter new description:", initialvalue=current_task.description
                    )

                    if new_task_name is not None and new_task_name.strip() and new_description is not None and new_description.strip(): # check if user input is valid
                        current_task.task = new_task_name # updates with new info
                        current_task.description = new_description
                        self.update_task_treeview() # update displayed details
                        self.display_task_details(None)  # update displayed details
                    else:
                        messagebox.showwarning("Warning", "Invalid input. Task name and description cannot be empty!")

                except IndexError:
                    messagebox.showwarning("Warning", "Invalid task selection")

    # deletes the selected task
    def delete_selected_task(self):
        selected_item = self.task_treeview.selection()
        if selected_item:
            selected_index = self.task_treeview.index(selected_item)
            if selected_index is not None:
                try:
                    current_task = self.task_list.head
                    for _ in range(selected_index):
                        current_task = current_task.next_task

                    confirmation = messagebox.askyesno("Confirmation", # user confirmation before task is deleted
                                                       f"Do you really want to delete the task '{current_task.task}'?")

                    if confirmation: # checks if user confirmed the deletion
                        # remove the task and update the treeview
                        self.task_list.remove(current_task)
                        self.priority_queue.heap.remove((current_task.priority, current_task.date_added, current_task)) # removes the task from priority queue and heap
                        heapq.heapify(self.priority_queue.heap)
                        self.update_task_treeview() # update displayed details
                        self.clear_task_details()

                except IndexError:
                    messagebox.showwarning("Warning", "Invalid task selection")

    def display_task_details(self, event): # displays details of selected task in the GUI
        selected_item = self.task_treeview.selection()
        if selected_item:
            selected_index = self.task_treeview.index(selected_item)
            if selected_index is not None and 0 <= selected_index: # check if index is valid
                try: # traverse the task linked list to find the selected task
                    current_task = self.task_list.head
                    for _ in range(selected_index):
                        current_task = current_task.next_task
                    self.show_task_details(current_task) # displays details in the box
                except IndexError:
                    messagebox.showwarning("Warning", "Invalid task selection")

    # displays the details of teh selected task in a box
    def show_task_details(self, task_details): # formatted text
        task_text = f"Task: {task_details.task}\nPriority: {task_details.priority}\nDate Added: {task_details.date_added.strftime('%m-%d %H:%M:%S')}"
        if task_details.description: # includes description of task
            task_text += f"\nDescription: {task_details.description}"
        task_text += f"\nCategory: {task_details.category}" # includes category of task
        self.task_details_textbox.config(state=tk.NORMAL)
        self.task_details_textbox.delete("1.0", tk.END)
        self.task_details_textbox.insert(tk.END, task_text)
        self.task_details_textbox.config(state=tk.DISABLED)

    def update_task_treeview(self):
        self.task_treeview.delete(*self.task_treeview.get_children())
        for task in self.priority_queue.heap:
            task_details = task[2]
            self.task_treeview.insert("", "end", values=(task_details.task, task_details.priority,
                                                         task_details.date_added.strftime('%m-%d %H:%M:%S'), task_details.description, task_details.category))

    # sorts the tasks based on priority or date added
    def sort_tasks(self):
        sort_option = self.sort_option.get()
        try: # sorts task based on selected option
            if sort_option == "Priority":
                self.priority_queue.heap.sort(key=lambda x: (x[0], x[1]))
            elif sort_option == "Date Added":
                self.priority_queue.heap.sort(key=lambda x: (x[1], x[0]))
            self.update_task_treeview() # updates GUI
        except (ValueError, TypeError) as e:
            messagebox.showwarning("Warning", f"Error sorting tasks: {e}")

    def clear_task_details(self):
        self.task_details_textbox.config(state=tk.NORMAL)
        self.task_details_textbox.delete("1.0", tk.END)
        self.task_details_textbox.config(state=tk.DISABLED)
