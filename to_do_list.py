# A TO-DO List application is a useful project that helps users manage and organize their tasks efficiently.This project aims to create a command-line or GUI-based application using python,allowing users to create,update,and track their to-do lists.



from tkinter import *
import tkinter.messagebox
import sqlite3 as sql

def add_task():
    input_text = task_field.get()
    if len(input_text) == 0:
        tkinter.messagebox.showwarning("Error", "Please Enter Some Text")
    else:
        tasks.append(input_text)  # Add task to the tasks list
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (input_text,))  # Insert task into DB
        connections.commit()  # Commit DB changes
        update_task()
        task_field.delete(0, "end")

def delete_task():
    try:
        value = list_box.get(list_box.curselection())
        if value in tasks:
            tasks.remove(value)
            update_task()
            cursor.execute("DELETE FROM tasks WHERE title=?", (value,))
            connections.commit()  
    except:
        tkinter.messagebox.showinfo("error", "no tasks are there to delete")

def delete_all():
    message_box = tkinter.messagebox.askyesno("delete all", "are you sure??")
    if message_box == True:
        while len(tasks)!=0:
            tasks.pop()
        cursor.execute("DELETE FROM tasks")
        connections.commit()  
        update_task()

def clear_task():
    list_box.delete(0, "end")

def close():
    print(tasks)
    window.destroy()

def retrieve_data():
    while len(tasks) != 0:
        tasks.pop()
    for row in cursor.execute("SELECT title FROM tasks"):
        tasks.append(row[0])

def mark_completed():
    marked=list_box.curselection()
    temp=marked[0]
    temp_marked=list_box.get(marked)
    temp_marked=temp_marked+"✔"
    list_box.delete(temp)
    list_box.insert(temp,temp_marked)
def update_task():
    clear_task()
    for task in tasks:
        list_box.insert(END, task)

if __name__ == "__main__":
    
    window = Tk()
    window.title("to-do list")
    window.configure(bg="orange")
    window.geometry("600x450")
    window.resizable(0, 0)
    connections = sql.connect("listsOfTasks.db")
    cursor = connections.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks(title TEXT)")

    tasks = []

    frame = Frame(window, bg="#5EE5EE")
    functions_frame = Frame(window, bg="#5EE5EE")
 

    frame.pack(fill="both")
    functions_frame.pack(side="top", expand=True, fill="both")
    

    frame_label = Label(frame, text="To-Do list",font="bold", background="#5EE5EE", foreground="#FF6103")
    frame_label.pack(padx=10, pady=10)

    task_label = Label(functions_frame, text="enter the text:", background="#5EE5EE", foreground="dark orange",font="bold")
    task_label.place(x=20, y=30)
    task_label.pack(padx=10,pady=10)

    task_field = Entry(functions_frame, width=50, bg="white", foreground="#A52A2A")
    task_field.place(x=160, y=40)
    add_button = Button(functions_frame, text="ADD",width=15, bg="green", command=add_task)
    add_button.pack(padx=10,pady=10)
    delete_button = Button(functions_frame, text="DELETE", bg="red", width=15, command=delete_task)
    delete_all_button = Button(functions_frame, text="DELETE ALL", bg="BROWN", width=15, command=delete_all)
    update_button=Button(functions_frame, text="TASK COMPLETED", bg="PINK", width=15, command=mark_completed)
    exit_button = Button(functions_frame, text="EXIT", width=15, command=close)

    add_button.place(x=18, y=80)
    delete_button.place(x=240,y=80)
    delete_all_button.place(x=460,y=80)
    exit_button.place(x=37,y=330)
    update_button.place(x=18,y=110)
    list_box=tkinter.Listbox(functions_frame,width=95,height=9,selectmode="single",bg="#FFFFFF",fg="#000000",selectbackground="#CDB53D",selectforeground="#ffffff")
    list_box.place(x=17,y=140)


    retrieve_data()
    update_task()
    window.mainloop()
    connections.commit()
    cursor.close()