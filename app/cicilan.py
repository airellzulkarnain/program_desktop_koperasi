import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import Session
from database import get_db


def cicilan(parent: ttk.Notebook):
    main_frame = ttk.Frame(parent)
    main_frame.grid(column=1, row=1, sticky=tk.NSEW)

    ttk.Label(main_frame, text='TEST').grid(column=1, row=1)
    return main_frame
