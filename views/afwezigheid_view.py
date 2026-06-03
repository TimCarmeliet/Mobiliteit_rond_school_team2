"""
afwezigheid_view.py  –  Uitbreiding Viggo
==========================================
Dit bestand bevat het scherm voor het beheren van aanwezigheidsregistraties.

Structuur van het scherm:
  - Links: invoerformulier (CRUD: toevoegen, aanpassen, verwijderen)
  - Rechts: overzichtstabel van alle registraties

Elke registratie bevat:
  - Student (gekozen uit dropdownmenu)
  - Datum  (formaat YYYY-MM-DD)
  - Status (aanwezig / afwezig / laat)
"""

import tkinter as tk
from tkinter import messagebox, ttk
from views.handy_view import Tooltip, maak_kader, maak_tabel

# Kleuren consistent met de rest van de applicatie
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"


def toon_afwezigheid(view):
    """
    Bouwt het volledige scherm voor aanwezigheidsbeheer op.

    'view' is de mainView instantie. Via view.controller kunnen we de
    businesslogica aanroepen. Via view.afwezigheid() herladen we de pagina
    na een wijziging (zelfde patroon als de andere schermen in dit project).
    """
    view.clear_content()

    # Maak het hoofdframe aan voor dit scherm
    view.afwezigheid_content = tk.Frame(view.root, bg=grijs)
    view.afwezigheid_content.pack(fill="both", expand=True)

    # ── Data ophalen ──────────────────────────────────────────────────────────
    # Alle registraties (met studentnaam) voor het overzicht
    data = view.controller.get_attendance_overview()

    # Alle studenten voor het dropdownmenu
    students = view.controller.get_students()

    # Opzoektabellen: we koppelen de leesbare naam aan een intern id
    student_opties = [f"{s[1]} ({s[2]})" for s in students]  # bv. "Jan Peeters (6ADB)"
    student_id_per_optie = {f"{s[1]} ({s[2]})": s[0] for s in students}
    student_optie_per_id = {s[0]: f"{s[1]} ({s[2]})" for s in students}

    # De drie geldige statuswaarden
    status_opties = ["aanwezig", "afwezig", "laat"]

    # Variabele die het id van de geselecteerde rij bijhoudt
    geselecteerde_id = tk.StringVar()

    # ── LINKS: invoerformulier ────────────────────────────────────────────────
    frame = maak_kader(
        view.afwezigheid_content,
        titel="Aanwezigheid bewerken",
        verticalSpace=20,
        horizontalSpace=20,
        header_kleur=blauw,
    )
    frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

    form = tk.Frame(frame, bg="white", padx=18, pady=16)
    form.pack(fill="x")

    combobox_stijl = {"width": 30, "font": ("Arial", 10)}

    # Dropdownmenu: kies een student
    tk.Label(form, text="Student", **view._label_stijl()).grid(row=0, column=0, sticky="w")
    studentInput = ttk.Combobox(form, values=student_opties, state="readonly", **combobox_stijl)
    studentInput.grid(row=1, column=0, sticky="ew", pady=(3, 12))

    # Tekstveld: datum invoeren – meerdere formaten worden aanvaard
    tk.Label(form, text="Datum (bv. 15-01-2026 of 2026-01-15)", **view._label_stijl()).grid(row=2, column=0, sticky="w")
    datumInput = tk.Entry(form, **view._input_stijl())
    datumInput.grid(row=3, column=0, sticky="ew", pady=(3, 12))

    # Dropdownmenu: kies de aanwezigheidsstatus
    tk.Label(form, text="Status", **view._label_stijl()).grid(row=4, column=0, sticky="w")
    statusInput = ttk.Combobox(form, values=status_opties, state="readonly", **combobox_stijl)
    statusInput.grid(row=5, column=0, sticky="ew", pady=(3, 16))

    form.columnconfigure(0, weight=1)

    # Knoppen-rij: Toevoegen / Aanpassen / Verwijderen
    knoppen = tk.Frame(form, bg="white")
    knoppen.grid(row=6, column=0, sticky="ew")

    # ── Hulpfuncties voor de knoppen ──────────────────────────────────────────

    def input_waarden():
        """
        Lees de drie invoervelden uit en geef ze terug als tuple.
        Toont een waarschuwing en geeft None terug als een veld leeg is.
        """
        student_id = student_id_per_optie.get(studentInput.get(), "")
        datum = datumInput.get().strip()
        status = statusInput.get().strip()

        if not student_id or not datum or not status:
            messagebox.showwarning(
                "Aanwezigheid",
                "Kies een student, vul een datum in en kies een status."
            )
            return None

        return student_id, datum, status

    def formulier_leegmaken():
        """Reset alle invoervelden en hef de tabelrij-selectie op."""
        geselecteerde_id.set("")
        studentInput.set("")
        datumInput.delete(0, "end")
        statusInput.set("")
        tabel.selection_remove(tabel.selection())
        update_knoppen()

    def aanwezigheid_toevoegen():
        """Stuur de invoer naar de controller om een nieuw record toe te voegen."""
        waarden = input_waarden()
        if waarden is None:
            return
        melding = view.controller.add_attendance(*waarden)
        if not view._toon_melding("Aanwezigheid", melding):
            return
        view.afwezigheid()  # pagina herladen zodat de tabel bijgewerkt is

    def aanwezigheid_aanpassen():
        """Stuur de invoer naar de controller om het geselecteerde record aan te passen."""
        if not geselecteerde_id.get():
            messagebox.showwarning("Aanwezigheid", "Selecteer eerst een record uit de tabel.")
            return
        waarden = input_waarden()
        if waarden is None:
            return
        melding = view.controller.update_attendance(geselecteerde_id.get(), *waarden)
        if not view._toon_melding("Aanwezigheid", melding):
            return
        view.afwezigheid()

    def aanwezigheid_verwijderen():
        """Verwijder het geselecteerde record via de controller."""
        if not geselecteerde_id.get():
            messagebox.showwarning("Aanwezigheid", "Selecteer eerst een record uit de tabel.")
            return
        melding = view.controller.delete_attendance(geselecteerde_id.get())
        if not view._toon_melding("Aanwezigheid", melding):
            return
        view.afwezigheid()

    # Toevoegen-knop: altijd actief (blauw)
    tk.Button(
        knoppen, text="Toevoegen", command=aanwezigheid_toevoegen,
        bg=blauw, activebackground=blauw, **view._knop_stijl(),
    ).pack(side="left", padx=(0, 10))

    # Aanpassen en Verwijderen worden grijs totdat een rij geselecteerd is
    aanpassen_knop = tk.Button(
        knoppen, text="Aanpassen", command=aanwezigheid_aanpassen, **view._knop_stijl()
    )
    aanpassen_knop.pack(side="left", padx=(0, 10))

    verwijderen_knop = tk.Button(
        knoppen, text="Verwijderen", command=aanwezigheid_verwijderen, **view._knop_stijl()
    )
    verwijderen_knop.pack(side="left")

    # Tooltips verschijnen als de gebruiker over een grijze knop beweegt
    aanpassen_tooltip = Tooltip(
        aanpassen_knop, "Klik eerst op een record in het overzicht om te kunnen aanpassen."
    )
    verwijderen_tooltip = Tooltip(
        verwijderen_knop, "Klik eerst op een record in het overzicht om te kunnen verwijderen."
    )

    def update_knoppen():
        """
        Pas de kleur van de Aanpassen- en Verwijderen-knoppen aan.
        Grijs = geen selectie, groen/rood = record geselecteerd.
        """
        heeft_selectie = bool(geselecteerde_id.get())
        if heeft_selectie:
            aanpassen_knop.config(bg=groen, activebackground=groen)
            verwijderen_knop.config(bg=rood, activebackground=rood)
            aanpassen_tooltip.set_actief(False)
            verwijderen_tooltip.set_actief(False)
        else:
            aanpassen_knop.config(bg=licht_grijs, activebackground=licht_grijs)
            verwijderen_knop.config(bg=licht_grijs, activebackground=licht_grijs)
            aanpassen_tooltip.set_actief(True)
            verwijderen_tooltip.set_actief(True)

    update_knoppen()

    # Leegmaken-knop: reset het formulier zonder een actie op de databank
    tk.Button(
        form, text="Leegmaken", command=formulier_leegmaken,
        bg="#e7e7e7", fg=donker_grijs, activebackground=licht_grijs,
        bd=0, padx=10, pady=7, cursor="hand2",
    ).grid(row=7, column=0, sticky="ew", pady=(12, 0))

    # ── RECHTS: overzichtstabel ───────────────────────────────────────────────
    frame2 = maak_kader(
        view.afwezigheid_content,
        titel=f"Overzicht aanwezigheid ({len(data)})",
        header_kleur=blauw
    )
    frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

    # Tabel toont: id, studentnaam, klas, datum, status
    tabel = maak_tabel(
        frame2,
        kolommen=["ID", "Student", "Klas", "Datum", "Status"],
        data=data,
    )
    tabel.column("ID", width=50, anchor="center")
    tabel.column("Student", width=150)
    tabel.column("Klas", width=80, anchor="center")
    tabel.column("Datum", width=110, anchor="center")
    tabel.column("Status", width=90, anchor="center")

    # Ruwe attendance-records (met student_id i.p.v. naam) voor het formulier
    # get_attendance() geeft: (id, student_id, datum, status)
    attendance_per_id = {record[0]: record for record in view.controller.get_attendance()}

    def on_select(event):
        """
        Wordt aangeroepen als de gebruiker op een rij in de tabel klikt.
        Vult het formulier automatisch in met de gegevens van die rij,
        zodat de gebruiker ze kan aanpassen of verwijderen.
        """
        geselecteerd = tabel.selection()
        if geselecteerd:
            rij = tabel.item(geselecteerd[0])["values"]
            geselecteerde_id.set(rij[0])  # sla het id op

            # haal het ruwe record op om het formulier correct in te vullen
            record = attendance_per_id.get(int(rij[0]))
            if record:
                # record = (id, student_id, datum, status)
                studentInput.set(student_optie_per_id.get(record[1], ""))
                datumInput.delete(0, "end")
                datumInput.insert(0, record[2])
                statusInput.set(record[3])
        else:
            geselecteerde_id.set("")

        update_knoppen()

    tabel.bind("<<TreeviewSelect>>", on_select)
