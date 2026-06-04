import tkinter as tk
from tkinter import messagebox, ttk

from views.handy_view import Tooltip, maak_kader, maak_tabel
from views.student_view import toon_student
from views.verplaatsing_view import toon_verplaatsing
from views.view_transport import toon_vervoer_pagina
from views.dashboard_view import toon_dashboard
from views.analyse_view import toon_analyse



# kleur
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"


class mainView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Mobiliteit rond de school")

        self.topnav = tk.Frame(root, bg="#333", height=40)
        self.topnav.pack(side="top", fill="x")

        self.styleButton = {
            "bg": "#555",
            "fg": "white",
            "activebackground": "#777",
            "activeforeground": "white",
            "bd": 0,
            "padx": 20,
            "pady": 10,
        }

        tk.Button(self.topnav, text="student", command=self.student, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="vervoer", command=self.vervoer, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="dashboard", command=self.dashboard, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="verplaatsing", command=self.verplaatsing, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="analyse", command=self.analyse, **self.styleButton).pack(side="left")
        self.student_content = tk.Frame(self.root, bg=grijs)
        self.vervoer_content = tk.Frame(self.root, bg=grijs)
        self.dashboard_content = tk.Frame(self.root, bg=grijs)
        self.verplaatsing_content = tk.Frame(self.root, bg=grijs)
        self.analyse_content = tk.Frame(self.root, bg=grijs)


        self.student()

    def clear_content(self):
        self.student_content.forget()
        self.vervoer_content.forget()
        self.dashboard_content.forget()
        self.verplaatsing_content.forget()
        self.analyse_content.forget()

    def _label_stijl(self):
        return {
            "bg": "white",
            "fg": donker_grijs,
            "font": ("Arial", 10, "bold"),
            "anchor": "w",
        }

    def _input_stijl(self):
        return {
            "width": 30,
            "font": ("Arial", 10),
            "relief": "solid",
            "bd": 1,
            "highlightthickness": 1,
            "highlightbackground": "#d0d7de",
            "highlightcolor": blauw,
            "insertbackground": donker_grijs,
        }

    def _knop_stijl(self):
        return {
            "fg": "white",
            "activeforeground": "white",
            "disabledforeground": "white",
            "bd": 0,
            "padx": 12,
            "pady": 8,
            "font": ("Arial", 9, "bold"),
            "cursor": "hand2",
        }

    def _toon_melding(self, titel, melding):
        if melding and melding.startswith("ERROR"):
            messagebox.showwarning(titel, melding.replace("ERROR: ", ""))
            return False
        return True

    def student(self):
        toon_student(self, Tooltip)

    def vervoer(self):
        toon_vervoer_pagina(self)

    def dashboard(self):
        toon_dashboard(self)



    def verplaatsing(self):
        toon_verplaatsing(self)

    def analyse(self):
        toon_analyse(self)
