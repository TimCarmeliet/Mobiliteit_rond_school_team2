import tkinter as tk
from tkinter import ttk


class Tooltip:
    def __init__(self, widget, tekst):
        self.widget = widget
        self.tekst = tekst
        self.venster = None
        self.actief = True
        widget.bind("<Enter>", self.toon)
        widget.bind("<Leave>", self.verberg)

    def toon(self, event=None):
        if self.venster or not self.actief:
            return

        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self.venster = tk.Toplevel(self.widget)
        self.venster.wm_overrideredirect(True)
        self.venster.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.venster,
            text=self.tekst,
            bg="#222222",
            fg="white",
            padx=8,
            pady=5,
            font=("Arial", 9),
            relief="solid",
            bd=1,
        )
        label.pack()

    def verberg(self, event=None):
        if self.venster:
            self.venster.destroy()
            self.venster = None

    def set_actief(self, actief):
        self.actief = actief
        if not actief:
            self.verberg()


def maak_kader(parent, titel, verticalSpace=20, horizontalSpace=20, header_kleur="#185FA5"):
    # buitenste frame/de rand
    frame = tk.Frame(parent, bd=1, relief="solid", bg="white")
    frame.pack(padx=verticalSpace, pady=horizontalSpace, anchor="nw")

    # header (gekleurde balk)
    header = tk.Label(frame, text=titel, bg=header_kleur, fg="white",font=("Arial", 11, "bold"), padx=10, pady=6)
    header.pack(fill="x")

    # scheidingslijn
    tk.Frame(frame, height=1, bg="#cccccc").pack(fill="x")

    return frame



def maak_tabel(parent, kolommen, data):
    tabel = ttk.Treeview(parent, columns=kolommen, show="headings", height=10)
    for kolom in kolommen:
        tabel.heading(kolom, text=kolom)
        tabel.column(kolom, width=120, anchor="w")
    for i, rij in enumerate(data):
        tag = "even" if i % 2 == 0 else "odd"
        tabel.insert("", "end", values=rij, tags=(tag,))
    tabel.tag_configure("even", background="#ffffff")
    tabel.tag_configure("odd", background="#f5f5f5")
    tabel.pack(fill="both", expand=True, padx=10, pady=10)
    return tabel
