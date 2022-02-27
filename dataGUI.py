import sqlite3
import openpyxl
import PySide6.QtWidgets
import sys
import GUIWindow
import numbers
from tkinter import *

with sqlite3.connect("project1db.sqlite") as db:
    cursor = db.cursor  # cursor conneccts to the database


def update_data_from_API():
    pass


window = Tk()
window.geometry("450x180")

#
label1 = Label(text="update the data")
label1.place(x=30, y=40)
label1.config(bg='lightgreen', padx=0)
#
label2 = Label(text="data visual graph")
label2.place(x=30, y=80)
label2.config(bg='lightgreen', padx=0)

# buttons
updateButton = Button(text="update", command=update_data_from_API)
updateButton.place(x=150, y=120, width=75, height=35)

window.mainloop()
