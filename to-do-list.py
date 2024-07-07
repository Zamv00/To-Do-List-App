from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import *
from tkinter.messagebox import *
import time
import json

def new_task():
   try:
       task = entry.get()
       if task:
           pending_tasks_list.insert(END, task)
           entry.delete(0, END)
   except Exception as e:
       print("Error occured: ", e)

def delete_task():
    try:
        if pending_tasks_list.curselection():
            selected_task_index = pending_tasks_list.curselection()[0]
            pending_tasks_list.delete(selected_task_index)
        elif completed_tasks_list.curselection():
            selected_task_index = completed_tasks_list.curselection()[0]
            completed_tasks_list.delete(selected_task_index)

    except Exception as e:
        print("Error occured: ", e)

def mark_completed(event):
    try:
        selected_task_index = pending_tasks_list.curselection()[0]
        task = pending_tasks_list.get(selected_task_index)
        pending_tasks_list.delete(selected_task_index)
        completed_tasks_list.insert(END,task)
    except Exception as e:
        print("Error occured: ", e)

def save_file():
    try:
        file_path = asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All files", "*.")]
        )
        if not file_path:
            return

        pending_tasks = pending_tasks_list.get(0, END)
        completed_tasks = completed_tasks_list.get(0, END)
        data = {
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks
        }
        with open(file_path, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Save", "File saved successfully")
    except Exception as e:
        print("An error has occured: ", e)
        messagebox.showerror("Error", "Failed to save file!")

def load_file():
    try:
        file_path = askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All files", "*.")]
        )
        if not file_path:
            return

        with open(file_path, "r") as f:
            tasks=json.load(f)
            pending_tasks_list.delete(0, END)
            completed_tasks_list.delete(0, END)
            for task in tasks["pending_tasks"]:
                pending_tasks_list.insert(END, task)
            for task in tasks["completed_tasks"]:
                completed_tasks_list.insert(END, task)
    except FileNotFoundError:
        print("File not found")
        messagebox.showwarning("Not Found", "File not found")
    except Exception as e:
        print("An error as occured: ", e)
        messagebox.showerror("Error", "An error has occured in opening the file")



root = Tk()
root.geometry("1000x650")
root.config(bg="#EEDC82")
root.resizable(False, False)
root.title("To Do List")




Label(text="Insert the text of your task here:", font=("Consolas", 11, "bold"), bg="#EEDC82").pack()
entry = Entry(root, width=40, bg="#FFFACD")
entry.pack(pady=5)

frame = Frame(root)
frame.config(bg="#EEDC82")
frame.pack()
tasks_Frame = Frame(root)
tasks_Frame.config(bg="#EEDC82")
tasks_Frame.pack()

menubar = Menu()
root.config(menu=menubar)
file_menu = Menu(menubar, tearoff=FALSE)
menubar.add_cascade(menu=file_menu, label="File")
file_menu.add_command(label="Save", command=save_file, font=("Consolas", 12, "bold"))
file_menu.add_command(label="Open", command=load_file, font=("Consolas", 12, "bold"))


add_task = Button(frame, text="Add Task", command=new_task,font=("Consolas", 12, "bold"), padx=5, bg="white")
add_task.grid(row=0,column=0, padx=5,pady=10)
remove_task = Button(frame, text="Remove Task", command = delete_task, font=("Consolas", 12, "bold"), padx=5, bg="white")
remove_task.grid(row=0, column=1,padx=5,pady=10)




altezza = 24

pending_tasks_list = Listbox(tasks_Frame, width=50, height=altezza, font=("Consolas", 12), selectmode=SINGLE, bg="#FFFACD")
pending_tasks_list.grid(row=0,column=0,padx=(0,20),pady=(10, 0))
pending_tasks_list.bind('<Double-1>', mark_completed)


completed_tasks_list = Listbox(tasks_Frame, width=50, height=altezza, font=("Consolas", 12, "overstrike"), selectmode=SINGLE, bg="#FFFACD")
completed_tasks_list.grid(row=0, column=1,pady=(10, 0))

def on_closing():
    answer = askquestion("Save", "Do you want to save?")
    if answer == "yes":
        save_file()
        root.destroy()
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()