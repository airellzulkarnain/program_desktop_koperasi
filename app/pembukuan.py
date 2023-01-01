import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from database import get_db


def pembukuan(parent: ttk.Notebook):
    main_frame = ttk.Frame(parent)
    
    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)
    main_frame.rowconfigure(3, weight=1)
    main_frame.rowconfigure(4, weight=1)
    main_frame.rowconfigure(5, weight=1)
    main_frame.rowconfigure(6, weight=1)

    return main_frame
