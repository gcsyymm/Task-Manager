import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x400")

        # Load tasks from file
        self.tasks = self.load_tasks()

        # GUI Elements
        self.task_listbox = tk.Listbox(self.root, width=80, height=15)
        self.task_listbox.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.complete_button = tk.Button(self.root, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the task list in the Listbox."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else "✗"
            self.task_listbox.insert(tk.END, f"{status} {task['title']} - {task['description']} (Due: {task['due_date']})")

    def add_task(self):
        """Add a new task."""
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if not title:
            return
        description = simpledialog.askstring("Add Task", "Enter task description:")
        due_date = simpledialog.askstring("Add Task", "Enter due date (e.g., 2023-12-31):")
        if title and due_date:
            self.tasks.append({
                "title": title,
                "description": description,
                "due_date": due_date,
                "completed": False
            })
            self.save_tasks()
            self.refresh_task_list()

    def mark_completed(self):
        """Mark the selected task as completed."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]["completed"] = True
            self.save_tasks()
            self.refresh_task_list()

    def delete_task(self):
        """Delete the selected task."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.save_tasks()
            self.refresh_task_list()

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                return json.load(file)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()