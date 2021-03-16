import os
import subprocess
import threading as td
import time
import tkinter as tk
from win10toast import ToastNotifier
from tkinter import filedialog
import psutil

toaster = ToastNotifier()
if os.path.exists("last.txt"):
    last_opened_file = open("last.txt", "r")
    last = last_opened_file.read()
    last_opened_file.close()
else:
    last = ""
    open("last.txt", "a")

stop_threads = False
root = tk.Tk()
root.title(f"Code Editor - {os.path.basename(last)}")
root.configure(background='white')


def cpu_rams():
    global cpu
    cpu = psutil.cpu_percent(4) / 100


def graf_stop():
    global stop_threads
    canvas.config(width=500)
    info.place_forget()
    stop_threads = True
    button5.place_forget()
    button2.place(x=81, y=0)


def graf():
    if os.path.exists("last.txt"):
        file = open("last.txt")
        last = file.read()
        file.close()
        if last == "" or last == " ":
            toaster.show_toast("Hey",
                    "You can't run empty file. Open file and try again",
                    icon_path="vsc.ico",
                    duration=3)
        else:
            global info
            global thread1
            global stop_threads
            canvas.config(width=750)
            info = tk.Frame(root, width=250, height=500, bg="white")
            info.place(x=500)
            thread1 = td.Thread(target=idk)
            thread1.start()
            stop_threads = False
            subprocess.Popen(f"cmd /K {last}")
    


def idk():
    global button5
    button2.place_forget()
    button5 = tk.Button(root, width=10, height=1, text="Run", command=graf_stop)
    button5.place(x=81, y=0)
    while True:
        global stop_threads
        ram = psutil.virtual_memory()[2] / 100
        relly = 1 - ram
        cpu = psutil.cpu_percent() / 100
        relyy = 1 - cpu
        graf1 = tk.Frame(info, bg="lime")
        graf1.place(x=0, rely=relyy, relheight=cpu, relwidth=0.15)
        graf2 = tk.Frame(info, bg="blue")
        graf2.place(x=40, rely=relly, relheight=ram, relwidth=0.15)
        clear = tk.Frame(info, bg="white")
        time.sleep(0.5)
        clear.place(x=0, y=0, relheight=1, relwidth=1)
        if stop_threads:
            break


def file_menu():
    global files
    global save_py
    global open_file
    save_py = tk.Button(root, text="Save as", height=1, width=10, command=py)
    save_py.place(x=0, y=50)
    open_file = tk.Button(root, text="Open file", height=1, width=10, command=open_saved)
    open_file.place(x=0, y=25)
    button1.place_forget()
    files = tk.Button(root, text="File", height=1, width=10, command=file_close)
    files.place(x=0, y=0)



def py():
    global name
    global button4
    name = tk.Entry(root, border=2)
    name.place(x=75, width=300, y=250)
    button4 = tk.Button(root, text="Save as", height=1, width=10, command=py_save)
    button4.place(y=247, x=375)


def open_saved():
    code_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files", "*.*"),("files","")))
    file = open(code_file)
    insert_code = file.read()
    file.close()
    code.insert(1.0, chars=insert_code)
    file = open("last.txt","w")
    file.write(code_file)
    file.close()


def py_save():
    global last
    file = open(f"{name.get()}", "w")
    file.write(code.get(1.0, "end-1c"))
    file.close()
    root.title(f"Code Editor - {name.get()}")
    file = open("last.txt", "w")
    file.write(f"{name.get()}")
    file.close()
    last = f"{name.get()}"


def file_close():
    files.place_forget()
    save_py.place_forget()
    open_file.place_forget()
    button1.place(x=0, y=0)
    try:
        button4.place_forget()
        name.place_forget()
    except:
        pass


def build():
    if os.path.exists("last.txt"):
        file = open("last.txt")
        last = file.read()
        file.close()
        if last == "" or last == " ":
            toaster.show_toast("Hey",
                    "You can't build empty file. Open file and try again",
                    icon_path="vsc.ico",
                    duration=3)
        else:
            subprocess.Popen(f"cmd /K pyinstaller {last} --clean")


canvas = tk.Canvas(root, height=500, width=500, bg="white", bd=0, highlightbackground="white")
canvas.pack()
button1 = tk.Button(root, width=10, height=1, text="File", command=file_menu)
button1.place(x=0, y=0)
button2 = tk.Button(root, width=10, height=1, text="Run", command=graf)
button2.place(x=81, y=0)
button3 = tk.Button(root, width=10, height=1, text="Build", command=build)
button3.place(x=162, y=0)
if last is "":
    code = tk.Text(root)
    code.place(x=0, y=25, relheight=0.95, width=500)
else:
    code = tk.Text(root)
    code.place(x=0, y=25, relheight=0.95, width=500)
    try:
        file = open(last)
        code_written = file.read()
        file.close()
    except FileNotFoundError:
        code_written = ""
    code.insert(1.0, chars=code_written)
tk.mainloop()
