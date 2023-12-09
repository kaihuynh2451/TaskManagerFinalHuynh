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
from datetime import datetime
import unittest
from tkinter import Tk
from TaskManagerClass import Task, TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.task_manager = TaskManager(self.root)

    def tearDown(self):
        self.root.update_idletasks()
        self.root.destroy()
        self.root = None

    def test_add_task(self):
        # creates a task and add it directly
        task = Task("Test Task", "1", "Test Description", "Work")
        self.task_manager.task_var.set(task.task)
        self.task_manager.priority_var.set(task.priority)
        self.task_manager.description_var.set(task.description)
        self.task_manager.category_var.set(task.category)

        self.task_manager.add_task()

        # checks if the task has been added
        self.assertGreaterEqual(len(self.task_manager.priority_queue.heap), 1)

        # access the first element in the heap
        if self.task_manager.priority_queue.heap:
            task_details = self.task_manager.priority_queue.heap[0][2]

            self.assertEqual(task_details.task, task.task)
            self.assertEqual(task_details.priority, task.priority)
            self.assertEqual(task_details.description, task.description)

    def test_edit_task(self):
        # adds a task first
        self.task_manager.task_var.set("Test Task")
        self.task_manager.priority_var.set("1")
        self.task_manager.description_var.set("Test Description")
        self.task_manager.category_var.set("Work")
        self.task_manager.add_task()

        # selects the item in the treeview before calling edit_task
        selected_item = self.task_manager.task_treeview.selection()
        if selected_item:
            self.task_manager.task_treeview.focus(selected_item[0])
            self.task_manager.task_treeview.selection_set(selected_item[0])

            # editing the task
            self.task_manager.task_var.set("Updated Task")
            self.task_manager.description_var.set("Updated Description")
            self.task_manager.edit_task()

            # checks if the task has been edited
            if self.task_manager.priority_queue.heap:
                task_details = self.task_manager.priority_queue.heap[0][2]
                self.assertEqual("Updated Task", task_details.task)
                self.assertEqual("Updated Description", task_details.description)

    def test_sort_tasks(self):
        root = Tk()
        task_manager = TaskManager(root)

        # add tasks with different priorities
        task_manager.task_var.set("Task 1")
        task_manager.priority_var.set("3")
        task_manager.description_var.set("Description 1")
        task_manager.category_var.set("Work")
        task_manager.add_task()

        task_manager.task_var.set("Task 2")
        task_manager.priority_var.set("1")
        task_manager.description_var.set("Description 2")
        task_manager.category_var.set("Work")
        task_manager.add_task()

        task_manager.task_var.set("Task 3")
        task_manager.priority_var.set("2")
        task_manager.description_var.set("Description 3")
        task_manager.category_var.set("Work")
        task_manager.add_task()

        # sort tasks by priority
        task_manager.sort_option.set("Priority")
        task_manager.sort_tasks()

        # update the task treeview
        task_manager.update_task_treeview()

        # checks if tasks are sorted by priority
        if task_manager.priority_queue.heap:
            priorities = [task[2].priority for task in task_manager.priority_queue.heap]
            expected_priorities = ["1", "2", "3"]
            self.assertListEqual(priorities, expected_priorities)

        root.destroy()

    def test_delete_selected_task(self):
        # add a task first
        self.task_manager.task_var.set("Test Task")
        self.task_manager.priority_var.set("1")
        self.task_manager.description_var.set("Test Description")
        self.task_manager.category_var.set("Work")
        self.task_manager.add_task()

        # delete the task
        self.task_manager.task_treeview.selection_set(self.task_manager.task_treeview.get_children()[0])
        self.task_manager.delete_selected_task()

        # check if the task has been deleted
        deleted_task_found = any(task[2].task == "Test Task" for task in self.task_manager.priority_queue.heap)

        self.assertFalse(deleted_task_found)
        self.assertEqual(len(self.task_manager.priority_queue.heap), 0)

    def test_display_task_details(self):
        # add a task first
        self.task_manager.task_var.set("Test Task")
        self.task_manager.priority_var.set("1")
        self.task_manager.description_var.set("Test Description")
        self.task_manager.category_var.set("Work")
        self.task_manager.add_task()

        # display task details
        self.task_manager.display_task_details(None)

        # manual inspection of the GUI output, I attempted to have an actual Unit Test but it would not work properly.
        # therefore manual inspection was used instead.
        self.root.mainloop()

    def test_clear_task_details(self):
        # add a task first
        self.task_manager.task_var.set("Test Task")
        self.task_manager.priority_var.set("1")
        self.task_manager.description_var.set("Test Description")
        self.task_manager.category_var.set("Work")
        self.task_manager.add_task()

        # clear task details
        self.task_manager.clear_task_details()

        # check if the task details textbox is empty
        displayed_text = self.task_manager.task_details_textbox.get("1.0", "end-1c")
        self.assertEqual(displayed_text, "")

if __name__ == "__main__":
    unittest.main()
