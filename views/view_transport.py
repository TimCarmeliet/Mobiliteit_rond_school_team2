import tkinter as tk
from tkinter import messagebox
from views.handy_view import maak_kader, maak_tabel

# kleuren
blauw = "#185FA5"
rood = "#b3261e"
grijs = "#eee"
donker_grijs = "#333333"



def toon_vervoer_pagina(view):
    view.clear_content()
    view.vervoer_content = tk.Frame(view.root, bg=grijs)
    view.vervoer_content.pack(fill="both", expand=True)

    data = view.controller.get_transport()
    geselecteerde_transport_id = tk.StringVar()

    # frame vervoer beheren
    frame = maak_kader(view.vervoer_content, titel="Vervoer beheren", header_kleur=blauw)
    frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

    form = tk.Frame(frame, bg="white", padx=16, pady=14)
    form.pack(fill="x")

    tk.Label(form, text="Vervoersmiddel", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
    vervoerTypeinput = tk.Entry(form, width=28, font=("Arial", 10), relief="solid", bd=1)
    vervoerTypeinput.grid(row=1, column=0, sticky="ew", pady=(3, 14))

    form.columnconfigure(0, weight=1)

    knoppen = tk.Frame(form, bg="white")
    knoppen.grid(row=2, column=0, sticky="ew")

    def formulier_leegmaken():
        geselecteerde_transport_id.set("")
        vervoerTypeinput.delete(0, "end")
        tabel.selection_remove(tabel.selection())

    def vervoer_toevoegen():
        transport_type = vervoerTypeinput.get().strip()
        if not transport_type:
            messagebox.showwarning("Vervoer", "Vul een vervoersmiddel in.")
            return
        view.controller.add_transport(transport_type)
        view.vervoer()

    def vervoer_verwijderen():
        if not geselecteerde_transport_id.get():
            messagebox.showwarning("Vervoer", "Selecteer eerst een vervoersmiddel uit de tabel.")
            return
        view.controller.delete_transport(geselecteerde_transport_id.get())
        view.vervoer()

    knopstijl = {"fg": "white", "activeforeground": "white", "bd": 0, "padx": 12, "pady": 7, "font": ("Arial", 9, "bold"), "cursor": "hand2"}
    tk.Button(knoppen, text="Toevoegen", command=vervoer_toevoegen, bg=blauw, activebackground=blauw, **knopstijl).pack(side="left", padx=(0, 10))
    tk.Button(knoppen, text="Verwijderen", command=vervoer_verwijderen, bg=rood, activebackground=rood, **knopstijl).pack(side="left")

    tk.Button(form, text="Leegmaken", command=formulier_leegmaken, bg="#e7e7e7", fg=donker_grijs, activebackground="#d8d8d8", bd=0, padx=10, pady=6, cursor="hand2").grid(row=3, column=0, sticky="ew", pady=(10, 0))

    # frame overzicht vervoersmiddelen
    frame2 = maak_kader(view.vervoer_content, titel=f"Overzicht vervoersmiddelen ({len(data)})", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

    tabel = maak_tabel(frame2, kolommen=["ID", "Type"], data=data)
    tabel.column("ID", width=50, anchor="center")
    tabel.column("Type", width=200)

    # klik op rij -> vult het formulier in
    def on_select(event):
        geselecteerd = tabel.selection()
        if geselecteerd:
            rij = tabel.item(geselecteerd[0])["values"]
            geselecteerde_transport_id.set(rij[0])
            vervoerTypeinput.delete(0, "end")
            vervoerTypeinput.insert(0, rij[1])

    tabel.bind("<<TreeviewSelect>>", on_select)