import os
import subprocess
import threading as td
import time
import ctypes
import tkinter as tk
from win10toast import ToastNotifier
from tkinter import filedialog
import psutil
import pathlib
import keyboard
root = tk.Tk()
toaster = ToastNotifier()
if os.path.exists(".code-editor"):
    pass
else:
    os.mkdir(".code-editor")
if os.path.exists(".code-editor/last.txt"):
    last_opened_file = open(".code-editor/last.txt", "r")
    last = last_opened_file.read()
    last_opened_file.close()
else:
    last = ""
    open(".code-editor/last.txt", "a")
try:
        file = open(last)
        root.title(f"Code Editor - {os.path.basename(last)}")
        file.close()
except FileNotFoundError:
        root.title(f"Code Editor - ")
stop_threads = False
root.configure(background='white')
root.resizable(False, False)


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
    if os.path.exists(".code-editor/last.txt"):
        file = open(".code-editor/last.txt")
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
            file = open(".code-editor/project.txt")
            what = file.read()
            file.close()
            if "C++" == what:
                if os.path.exists("a.exe"):
                    subprocess.Popen("cmd /k a.exe")
                else:
                    pass
            if "C" == what:
                if os.path.exists("a.exe"):
                    subprocess.Popen("cmd /k a.exe")
                else:
                    pass
            elif "Python" == what:
                subprocess.Popen(f"cmd /K python {last}")
    


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
    global new_file
    save_py = tk.Button(root, text="Save as", height=1, width=10, command=py)
    save_py.place(x=0, y=75)
    open_file = tk.Button(root, text="Open file", height=1, width=10, command=open_saved)
    open_file.place(x=0, y=50)
    new_file = tk.Button(root, text="New File", height=1, width=10, command=new)
    new_file.place(x=0, y=25)
    button1.place_forget()
    files = tk.Button(root, text="File", height=1, width=10, command=file_close)
    files.place(x=0, y=0)


def new_files():
    file_name = name.get()
    root.title(f"Code Editor - {name.get()}")
    file = open(file_name, "a")
    file.close()
    file = open(file_name)
    insert_code = file.read()
    code.delete(1.0, "end")
    code.insert(1.0, chars=insert_code)
    file.close()
    file = open(".code-editor/last.txt","w")
    file_path = pathlib.Path(name.get()).absolute()
    file.write(str(file_path))
    file.close()
    if ".cpp" in os.path.basename(file_path):
        file = open(".code-editor/project.txt", "w")
        file.write("C++")
        file.close()
    elif ".py" in os.path.basename(file_path):
        file = open(".code-editor/project.txt", "w")
        file.write("Python")
        file.close()
    elif ".c" in os.path.basename(file_path):
        file = open(".code-editor/project.txt", "w")
        file.write("C")
        file.close()
def py():
    global name
    global button4
    name = tk.Entry(root, border=2)
    name.place(x=75, width=300, y=250)
    button4 = tk.Button(root, text="Save as", height=1, width=10, command=py_save)
    button4.place(y=247, x=375)


def new():
    global name
    global button4
    name = tk.Entry(root, border=2)
    name.place(x=75, width=300, y=250)
    button4 = tk.Button(root, text="Create File", height=1, width=10, command=new_files)
    button4.place(y=247, x=375)


def open_saved():
    code_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files", "*.*"),("files","")))
    file = open(code_file)
    insert_code = file.read()
    file.close()
    code.delete(1.0, "end")
    code.insert(1.0, chars=insert_code)
    file = open(".code-editor/last.txt","w")
    file.write(code_file)
    file.close()
    if ".cpp" in os.path.basename(code_file):
        file = open(".code-editor/project.txt", "w")
        file.write("C++")
        file.close()
    elif ".py" in os.path.basename(code_file):
        file = open(".code-editor/project.txt", "w")
        file.write("Python")
        file.close()
    elif ".c" in os.path.basename(code_file):
        file = open(".code-editor/project.txt", "w")
        file.write("C")
        file.close()


def py_save():
    global last
    file = open(f"{name.get()}", "w")
    file.write(code.get(1.0, "end-1c"))
    file.close()
    root.title(f"Code Editor - {name.get()}")
    file = open(".code-editor/last.txt", "w")
    file_path = pathlib.Path(name.get()).absolute()
    file.write(f"{file_path}")
    file.close()
    last = f"{file_path}"
    file = open(".code-editor/project.txt", "w")
    if ".cpp" in name.get():
        file.write("C++")
        file.close()
    elif ".py" in name.get():
        file.write("Python")
        file.close()
    elif ".c" in name.get():
        file.write("C")
        file.close()


def file_close():
    files.place_forget()
    save_py.place_forget()
    open_file.place_forget()
    new_file.place_forget()
    button1.place(x=0, y=0)
    try:
        button4.place_forget()
        name.place_forget()
    except:
        pass


def build():
    if os.path.exists(".code-editor/last.txt"):
        file = open(".code-editor/last.txt")
        last = file.read()
        file.close()
        file = open(".code-editor/project.txt")
        what = file.read()
        file.close()
        if last == "" or last == " ":
            toaster.show_toast("Hey",
                    "You can't build empty file. Open file and try again",
                    icon_path="vsc.ico",
                    duration=3)
        if "C" == what:
            file = open(".code-editor/c_compiler.txt", "a")
            file.close()
            file = open(".code-editor/c_compiler.txt")
            if "yes" == file.read():
                compiler_cpp = 6
                time.sleep(0)
            else:
                file.close()
                compiler_cpp = ctypes.windll.user32.MessageBoxW(0, "Do you have C compiler? And do you have it in PATH?", "C compiler", 4)
                if 6 == int(compiler_cpp):
                    file = open(".code-editor/c_compiler.txt", "w")
                    file.write("yes")
                    file.close()
                else:
                    pass
                file = open(".code-editor/project.txt")
                if 6 == int(compiler_cpp):
                    subprocess.Popen(f"gcc {last}")
            subprocess.Popen(f"gcc {last}")
        if "C++" == what:
            file = open(".code-editor/cpp_compiler.txt", "a")
            file.close()
            file = open(".code-editor/cpp_compiler.txt")
            if "yes" == file.read():
                compiler_cpp = 6
                time.sleep(0)
            else:
                file.close()
                compiler_cpp = ctypes.windll.user32.MessageBoxW(0, "Do you have C++ compiler? And do you have it in PATH?", "C++ compiler", 4)
                if 6 == int(compiler_cpp):
                    file = open(".code-editor/cpp_compiler.txt", "w")
                    file.write("yes")
                    file.close()
                else:
                    pass
                file = open(".code-editor/project.txt")
                if 6 == int(compiler_cpp):
                    subprocess.Popen(f"g++ {last}")
            subprocess.Popen(f"g++ {last}")
        if "Python" in what:
            file = open(".code-editor/pyinstaller.txt", "a")
            file.close()
            file = open(".code-editor/pyinstaller.txt")
            if "yes" == file.read():
                compiler_cpp = 6
                time.sleep(0)
            else:
                file.close()
                compiler_cpp = ctypes.windll.user32.MessageBoxW(0, "Do you have Pyinstaller? And do you have it in PATH?", "Pyinstaller", 4)
                if 6 == int(compiler_cpp):
                    file = open(".code-editor/pyinstaller.txt", "w")
                    file.write("yes")
                    file.close()
                else:
                    pass
                file = open(".code-editor/project.txt")
                if 6 == int(compiler_cpp):
                    subprocess.Popen(f"cmd /K pyinstaller {last} --clean")
            subprocess.Popen(f"cmd /K pyinstaller {last} --clean")


def key_save():
    global last
    file = open(f"{last}", "w")
    file.write(code.get(1.0, "end-1c"))
    file.close()
    root.title(f"Code Editor - {os.path.basename(last)}")
    file = open(".code-editor/last.txt", "w")
    file_path = pathlib.Path(last).absolute()
    file.write(f"{file_path}")
    file.close()
    last = f"{file_path}"
    file = open(".code-editor/project.txt", "w")
    toaster.show_toast("File",
                    "File was saved successfully",
                    icon_path="vsc.ico",
                    duration=3)
    if ".cpp" in os.path.basename(last):
        file.write("C++")
        file.close()
    elif ".py" in os.path.basename(last):
        file.write("Python")
        file.close()
    elif ".c" in os.path.basename(last):
        file.write("C")
        file.close()
canvas = tk.Canvas(root, height=513, width=513, bg="white", bd=0, highlightbackground="white")
canvas.pack()
button1 = tk.Button(root, width=10, height=1, text="File", command=file_menu)
button1.place(x=0, y=0)
button2 = tk.Button(root, width=10, height=1, text="Run", command=graf)
button2.place(x=81, y=0)
button3 = tk.Button(root, width=10, height=1, text="Build", command=build)
button3.place(x=162, y=0)
scrollbar = tk.Scrollbar(root)
scrollbar.place(x=500, height=475, y=25)
scrollbar2 = tk.Scrollbar(root, orient='horizontal')
scrollbar2.place(x=0, width=500, y=500)
if last is "":
    code = tk.Text(root, yscrollcommand=scrollbar.set, wrap="none", xscrollcommand=scrollbar2.set, font=("Calibri", 10))
    code.place(x=0, y=25, height=475, width=500)
else:
    code = tk.Text(root, yscrollcommand=scrollbar.set, wrap="none", xscrollcommand=scrollbar2.set, font=("Ubuntu", 12))
    code.place(x=0, y=25, height=475, width=500)
    try:
        file = open(last)
        code_written = file.read()
        file.close()
    except FileNotFoundError:
        code_written = ""
    code.insert(1.0, chars=code_written)
scrollbar.config(command=code.yview)
scrollbar2.config(command=code.xview)
keyboard.add_hotkey('ctrl+s', lambda: key_save())
tk.mainloop()
