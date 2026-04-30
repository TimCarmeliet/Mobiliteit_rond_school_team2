import tkinter as tk
from tkinter import ttk

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