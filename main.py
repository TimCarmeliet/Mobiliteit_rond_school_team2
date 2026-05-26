import tkinter as tk
#import pandas as pd
from main_model import Model
from main_controller import Controller
from main_view import mainView
from tab_logs import LogsTab
from tab_analyse import AnalyseTab

if __name__ == "__main__":
    root = tk.Tk()

    model = Model()
    controller = Controller(model)
    view = LogsTab(root, controller)

    root.mainloop()
    