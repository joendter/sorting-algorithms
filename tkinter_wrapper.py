import tkinter as tk
from tkinter import filedialog
import os
import webbrowser
import main


def execute_code():
    selected_option = var.get()
    file_path = filedialog.askopenfilename(title="Array to sort", filetypes=[("Text files", "*.txt")],
                                           defaultextension=".txt", initialdir=os.getcwd())
    print(file_path)
    if file_path == "":
        file_path = "testdata1.txt"
    if not main.Array.fromFile(main.debugarray,filepath=file_path):
        return
    if selected_option == 1:
        openPDF("GnomeSort.pdf")
        main.example_sort(datapath=file_path)
    elif selected_option == 2:
        openPDF("BubbleSort.pdf")
        main.example_sort(1,datapath=file_path)
    elif selected_option == 3:
        openPDF("SelectionSort.pdf")
        main.example_sort(2,datapath=file_path)
    elif selected_option == 4:
        openPDF("MiracleSort.pdf")
        main.example_sort(3,datapath=file_path)
    elif selected_option == 5:
        openPDF("BogoSort.pdf")
        main.example_sort(4,datapath=file_path)
    else:
        print("No algorithm selected")


def openPDF(filename):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    webbrowser.open(file_path)


root = tk.Tk()
root.title("Select Sorting algorithm")
root.geometry("400x400")

var = tk.IntVar()

tk.Radiobutton(root, text="Gnome Sort", variable=var, value=1).pack(anchor=tk.W)
tk.Radiobutton(root, text="Bubble Sort", variable=var, value=2).pack(anchor=tk.W)
tk.Radiobutton(root, text="Selection Sort", variable=var, value=3).pack(anchor=tk.W)
tk.Radiobutton(root, text="Miracle Sort", variable=var, value=4).pack(anchor=tk.W)
tk.Radiobutton(root, text="Bogosort", variable=var, value=5).pack(anchor=tk.W)

tk.Button(root, text="Run sorting algorithm", command=execute_code).pack()

root.mainloop()