import tkinter as tk
from tkinter import messagebox

from views.handy_view import maak_kader, maak_tabel


blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"


def toon_student(view, tooltip_class):
    view.clear_content()
    view.student_content = tk.Frame(view.root, bg="#eee")
    view.student_content.pack(fill="both", expand=True)
    data = view.controller.get_all_students()
    geselecteerde_student_id = tk.StringVar()

    # frame student bewerken
    frame = maak_kader(
        view.student_content,
        titel="Student bewerken",
        verticalSpace=20,
        horizontalSpace=20,
        header_kleur=blauw,
    )
    frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

    form = tk.Frame(frame, bg="white", padx=18, pady=16)
    form.pack(fill="x")

    label_stijl = {
        "bg": "white",
        "fg": donker_grijs,
        "font": ("Arial", 10, "bold"),
        "anchor": "w",
    }
    input_stijl = {
        "width": 30,
        "font": ("Arial", 10),
        "relief": "solid",
        "bd": 1,
        "highlightthickness": 1,
        "highlightbackground": "#d0d7de",
        "highlightcolor": blauw,
        "insertbackground": donker_grijs,
    }

    tk.Label(form, text="Naam", **label_stijl).grid(row=0, column=0, sticky="w")
    studentNaaminput = tk.Entry(form, **input_stijl)
    studentNaaminput.grid(row=1, column=0, sticky="ew", pady=(3, 12))

    tk.Label(form, text="Klas", **label_stijl).grid(row=2, column=0, sticky="w")
    studentKlasinput = tk.Entry(form, **input_stijl)
    studentKlasinput.grid(row=3, column=0, sticky="ew", pady=(3, 12))

    tk.Label(form, text="Afstand tot school (km)", **label_stijl).grid(row=4, column=0, sticky="w")
    studentAfstandinput = tk.Entry(form, **input_stijl)
    studentAfstandinput.grid(row=5, column=0, sticky="ew", pady=(3, 16))

    form.columnconfigure(0, weight=1)

    knoppen = tk.Frame(form, bg="white")
    knoppen.grid(row=6, column=0, sticky="ew")

    def input_waarden():
        naam = studentNaaminput.get().strip()
        klas = studentKlasinput.get().strip()
        afstand = studentAfstandinput.get().strip().replace(",", ".").replace(" km", "")

        if not naam or not klas or not afstand:
            messagebox.showwarning("Student", "Vul naam, klas en afstand in.")
            return None

        try:
            float(afstand)
        except ValueError:
            messagebox.showwarning("Student", "Afstand moet een getal zijn, bijvoorbeeld 4.5.")
            return None

        return naam, klas, afstand

    def formulier_leegmaken():
        geselecteerde_student_id.set("")
        studentNaaminput.delete(0, "end")
        studentKlasinput.delete(0, "end")
        studentAfstandinput.delete(0, "end")
        tabel.selection_remove(tabel.selection())
        update_selectie_knoppen()

    def student_toevoegen():
        waarden = input_waarden()
        if waarden is None:
            return
        view.controller.add_student(*waarden)
        view.student()

    def student_aanpassen():
        waarden = input_waarden()
        if waarden is None:
            return
        if not geselecteerde_student_id.get():
            messagebox.showwarning("Student", "Selecteer eerst een student uit de tabel.")
            return
        view.controller.update_student(geselecteerde_student_id.get(), *waarden)
        view.student()

    def student_verwijderen():
        if not geselecteerde_student_id.get():
            messagebox.showwarning("Student", "Selecteer eerst een student uit de tabel.")
            return
        view.controller.delete_student(geselecteerde_student_id.get())
        view.student()

    knopstijl = {
        "fg": "white",
        "activeforeground": "white",
        "disabledforeground": "white",
        "bd": 0,
        "padx": 12,
        "pady": 8,
        "font": ("Arial", 9, "bold"),
        "cursor": "hand2",
    }
    tk.Button(
        knoppen,
        text="Toevoegen",
        command=student_toevoegen,
        bg=blauw,
        activebackground=blauw,
        **knopstijl,
    ).pack(side="left", padx=(0, 10))
    aanpassen_knop = tk.Button(knoppen, text="Aanpassen", command=student_aanpassen, **knopstijl)
    aanpassen_knop.pack(side="left", padx=(0, 10))
    verwijderen_knop = tk.Button(knoppen, text="Verwijderen", command=student_verwijderen, **knopstijl)
    verwijderen_knop.pack(side="left")

    aanpassen_tooltip = tooltip_class(
        aanpassen_knop,
        "Klik eerst op een leerling in het overzicht om te kunnen aanpassen.",
    )
    verwijderen_tooltip = tooltip_class(
        verwijderen_knop,
        "Klik eerst op een leerling in het overzicht om te kunnen verwijderen.",
    )

    def update_selectie_knoppen():
        heeft_selectie = bool(geselecteerde_student_id.get())
        if heeft_selectie:
            aanpassen_knop.config(state="normal", bg=groen, activebackground=groen, cursor="hand2")
            verwijderen_knop.config(state="normal", bg=rood, activebackground=rood, cursor="hand2")
            aanpassen_tooltip.set_actief(False)
            verwijderen_tooltip.set_actief(False)
        else:
            aanpassen_knop.config(state="normal", bg=licht_grijs, activebackground=licht_grijs, cursor="hand2")
            verwijderen_knop.config(state="normal", bg=licht_grijs, activebackground=licht_grijs, cursor="hand2")
            aanpassen_tooltip.set_actief(True)
            verwijderen_tooltip.set_actief(True)

    update_selectie_knoppen()

    tk.Button(
        form,
        text="Leegmaken",
        command=formulier_leegmaken,
        bg="#e7e7e7",
        fg=donker_grijs,
        activebackground=licht_grijs,
        bd=0,
        padx=10,
        pady=7,
        cursor="hand2",
    ).grid(row=7, column=0, sticky="ew", pady=(12, 0))

    # frame2 overzicht studenten
    frame2 = maak_kader(view.student_content, titel=f"Overzicht studenten ({len(data)})", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

    tabel = maak_tabel(
        frame2,
        kolommen=["ID", "Naam", "Klas", "Afstand"],
        data=data,
    )
    tabel.column("ID", width=50, anchor="center")
    tabel.column("Naam", width=210)
    tabel.column("Klas", width=90, anchor="center")
    tabel.column("Afstand", width=110, anchor="e")

    # klik op rij -> vult het formulier in
    def on_select(event):
        geselecteerd = tabel.selection()
        if geselecteerd:
            rij = tabel.item(geselecteerd[0])["values"]
            geselecteerde_student_id.set(rij[0])
            studentNaaminput.delete(0, "end")
            studentNaaminput.insert(0, rij[1])
            studentKlasinput.delete(0, "end")
            studentKlasinput.insert(0, rij[2])
            studentAfstandinput.delete(0, "end")
            studentAfstandinput.insert(0, str(rij[3]).replace(" km", ""))
        else:
            geselecteerde_student_id.set("")
        update_selectie_knoppen()

    tabel.bind("<<TreeviewSelect>>", on_select)
