from tkinter.ttk import Style


def stylize(style: Style):
    style = style()
    style.configure("TButton", font=("Arial", 12, "normal"))
    style.configure("TRadiobutton", font=("Arial", 12, "normal"))
    style.configure("TSpinbox", font=("Arial", 12, "normal"))
    style.configure("green.TButton", foreground="green", font=("Arial", 14, "bold"))
    style.configure("blue.TButton", foreground="blue", font=("Arial", 14, "bold"))
    style.configure("red.TButton", foreground="red", font=("Arial", 14, "bold"))
    style.configure("Treeview", font=("Arial", 12, "normal"))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("TNotebook.Tab", font=("Arial", 12, "normal"), padding=4)
    style.configure(
        "cicilan.TCheckbutton", font=("Arial", 12, "normal"), background="white"
    )
    style.configure("pilihsemua.TCheckbutton", font=("Arial", 12, "normal"))
