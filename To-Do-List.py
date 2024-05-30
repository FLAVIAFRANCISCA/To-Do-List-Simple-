import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys

tasks = []
ok_thread = True

def get_entry(event=""):
    text = todo.get()
    try:
        time_str = time.get()
        if ':' in time_str:
            minutes, seconds = map(int, time_str.split(':'))
            duration = minutes * 60 + seconds
        else:
            duration = int(time_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Please enter a valid integer or 'm:ss' format.")
        return
    if duration <= 0:
        messagebox.showerror("Error", "Please enter a positive integer for time.")
        return
    todo.delete(0, tk.END)
    time.delete(0, tk.END)
    todo.focus_set()
    add_list(text, duration)
    update_list()
    success_label.config(text="Task added successfully!", fg="green")

def add_list(text, duration):
    tasks.append([text, duration])
    timer = threading.Timer(duration, time_passed, [text])
    timer.start()

def update_list():
    todolist.delete(0, tk.END)
    for task in tasks:
        todolist.insert(tk.END, "[" + task[0] + "] Time left: " + format_time(task[1]))

def time_passed(task):
    messagebox.showinfo("Notification", "Time for: " + task)
    for t in tasks:
        if t[0] == task:
            tasks.remove(t)
            break
    update_list()
    success_label.config(text="Task completed and removed!", fg="blue")

def delete_task():
    try:
        index = todolist.curselection()[0]
        task = tasks[index][0]
        del tasks[index]
        update_list()
        success_label.config(text=f"Task '{task}' removed!", fg="red")
    except IndexError:
        messagebox.showerror("Error", "Please select a task to delete.")

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return '{:02}:{:02}'.format(minutes, seconds)

def real_time():
    global ok_thread
    while ok_thread:
        for task in tasks:
            task[1] -= 1
        update_list()
        app.update()
        time.sleep(1)

if __name__ == '__main__':
    # application
    app = tk.Tk()
    app.geometry("480x680")
    app.title("Todolist Reminder")
    app.rowconfigure(0, weight=1)
    app.columnconfigure(0, weight=1)

    # style
    style = ttk.Style()
    style.configure("TButton", foreground="#ffffff", background="#6186AC")
    style.configure("TLabel", foreground="#000000", font=("Arial", 12))

    # widgets
    label = ttk.Label(app, text="Enter task to do:")
    label_hour = ttk.Label(app, text="Enter time (seconds or m:ss):")
    todo = ttk.Entry(app, width=30)
    time = ttk.Entry(app, width=15)
    add_button = ttk.Button(app, text='Add task', command=get_entry)
    delete_button = ttk.Button(app, text='Delete task', command=delete_task)
    todolist = tk.Listbox(app, width=50, height=15)
    success_label = ttk.Label(app, text="", font=("Arial", 10))

    # start real-time thread
    real_timer = threading.Thread(target=real_time)
    real_timer.start()

    # binding
    app.bind('<Return>', get_entry)

    # widgets placement
    label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    label_hour.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    todo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    time.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    add_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    delete_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    todolist.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    success_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    app.mainloop()
    ok_thread = False
    sys.exit("FINISHED")
