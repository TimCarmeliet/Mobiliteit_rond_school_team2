import tkinter as tk
import pandas as pd
from main_model import Model
from main_controller import Controller
from main_view import View

if __name__ == "__main__":
    root = tk.Tk()

    model = Model()
    controller = Controller(model)
    view = View(root, controller)

    root.mainloop()
    