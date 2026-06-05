
import tkinter as tk
from tkinter import messagebox, ttk          # messagebox = pop-upvensters, ttk = Combobox
from views.handy_view import Tooltip, maak_kader, maak_tabel

# Kleurconstanten
blauw       = "#185FA5"   
rood        = "#b3261e"   
groen       = "#2f7d32"   
grijs       = "#eee"      
donker_grijs = "#333333"  
licht_grijs = "#d8d8d8"   


def toon_afwezigheid(view):

    # Verwijder de inhoud van het vorige scherm
    view.clear_content()

    # Maak een leeg frame aan dat het volledige venster vult
    view.afwezigheid_content = tk.Frame(view.root, bg=grijs)
    view.afwezigheid_content.pack(fill="both", expand=True)

    # Data ophalen via de controlle
    # dropdownmenu's en de tabel al gevuld zijn bij het openen.

    # Alle registraties ophalen met studentnaam (voor de rechtertabel)
    data = view.controller.get_attendance_overview()

    # Alle studenten ophalen 
    students = view.controller.get_students()

    student_opties = [f"{s[1]} ({s[2]})" for s in students]

    student_id_per_optie = {f"{s[1]} ({s[2]})": s[0] for s in students}

    student_optie_per_id = {s[0]: f"{s[1]} ({s[2]})" for s in students}

    # De drie geldige waarden voor het statusveld
    status_opties = ["aanwezig", "afwezig", "laat"]

    # Hier slaan we het ID op van de rij die de gebruiker aanklikt.
    # Zolang de gebruiker niets selecteert, blijft dit leeg ("").
    geselecteerde_id = tk.StringVar()

    frame = maak_kader(
        view.afwezigheid_content,
        titel="Aanwezigheid bewerken",
        verticalSpace=20,
        horizontalSpace=20,
        header_kleur=blauw,
    )
    frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

    # Binnenste frame voor de velden en knoppen (wit, met padding)
    form = tk.Frame(frame, bg="white", padx=18, pady=16)
    form.pack(fill="x")

    combobox_stijl = {"width": 30, "font": ("Arial", 10)}

    # Invoerveld 1: Student
    # Label boven het veld
    tk.Label(form, text="Student", **view._label_stijl()).grid(row=0, column=0, sticky="w")
    # Combobox met state="readonly" = de gebruiker kan alleen kiezen,
    # niet zelf typen. Dit voorkomt foute invoer.
    studentInput = ttk.Combobox(form, values=student_opties, state="readonly", **combobox_stijl)
    studentInput.grid(row=1, column=0, sticky="ew", pady=(3, 12))

    # Invoerveld 2: Datum
    # meerdere datumformaten en zet ze altijd om naar YYYY-MM-DD.
    tk.Label(form, text="Datum (bv. 15-01-2026 of 2026-01-15)", **view._label_stijl()).grid(row=2, column=0, sticky="w")
    datumInput = tk.Entry(form, **view._input_stijl())
    datumInput.grid(row=3, column=0, sticky="ew", pady=(3, 12))

    # Invoerveld 3: Status
    # Combobox met vaste keuzes: aanwezig / afwezig / laat
    tk.Label(form, text="Status", **view._label_stijl()).grid(row=4, column=0, sticky="w")
    statusInput = ttk.Combobox(form, values=status_opties, state="readonly", **combobox_stijl)
    statusInput.grid(row=5, column=0, sticky="ew", pady=(3, 16))

    # Zorg dat kolom 0 de volledige breedte mag innemen
    form.columnconfigure(0, weight=1)

    # Frame voor de drie actieknoppen (Toevoegen / Aanpassen / Verwijderen)
    knoppen = tk.Frame(form, bg="white")
    knoppen.grid(row=6, column=0, sticky="ew")

    # HULPFUNCTIES (binnenfuncties van toon_afwezigheid)
    # Python laat toe om functies te definiëren BINNEN een andere functie.
    # Deze functies hebben toegang tot alle variabelen
    # hierboven (studentInput, datumInput, geselecteerde_id, ...).
    # Ze worden pas uitgevoerd als de gebruiker op een knop drukt.

    def input_waarden():
        # Leest de drie velden uit en geeft ze terug als tuple.
        # Geeft None terug als een veld leeg is, zodat we de
        # actie kunnen stoppen voor de databank aangesproken wordt.
        student_id = student_id_per_optie.get(studentInput.get(), "")
        datum = datumInput.get().strip()
        status = statusInput.get().strip()

        if not student_id or not datum or not status:
            # Toon een pop-upwaarschuwing als een veld leeg is
            messagebox.showwarning(
                "Aanwezigheid",
                "Kies een student, vul een datum in en kies een status."
            )
            return None

        return student_id, datum, status

    def formulier_leegmaken():
        # Zet alle velden terug naar leeg en hef de tabelrij-selectie op.
        # Dit roept update_knoppen() aan zodat de knoppen ook terugkeren
        geselecteerde_id.set("")
        studentInput.set("")
        datumInput.delete(0, "end")
        statusInput.set("")
        tabel.selection_remove(tabel.selection())
        update_knoppen()

    def aanwezigheid_toevoegen():
        # Stap 1: lees de invoervelden uit
        waarden = input_waarden()
        if waarden is None:
            return  # stop als een veld leeg is

        # Stap 2: stuur de data naar de controller (die valideert en opslaat)
        melding = view.controller.add_attendance(*waarden)

        # Stap 3: toon een foutmelding als de controller een probleem meldde
        if not view._toon_melding("Aanwezigheid", melding):
            return

        # Stap 4: herlaad het scherm zodat de nieuwe rij in de tabel verschijnt
        view.afwezigheid()

    def aanwezigheid_aanpassen():
        # Controleer of de gebruiker een rij heeft geselecteerd
        if not geselecteerde_id.get():
            messagebox.showwarning("Aanwezigheid", "Selecteer eerst een record uit de tabel.")
            return

        waarden = input_waarden()
        if waarden is None:
            return

        # Stuur het id + nieuwe waarden naar de controller om te updaten
        melding = view.controller.update_attendance(geselecteerde_id.get(), *waarden)
        if not view._toon_melding("Aanwezigheid", melding):
            return

        view.afwezigheid()  # scherm herladen

    def aanwezigheid_verwijderen():
        # Controleer of de gebruiker een rij heeft geselecteerd
        if not geselecteerde_id.get():
            messagebox.showwarning("Aanwezigheid", "Selecteer eerst een record uit de tabel.")
            return

        # Stuur het id naar de controller om het record te verwijderen
        melding = view.controller.delete_attendance(geselecteerde_id.get())
        if not view._toon_melding("Aanwezigheid", melding):
            return

        view.afwezigheid()  # scherm herladen

    # KNOPPEN AANMAKEN

    # Toevoegen-knop: altijd blauw en actief
    tk.Button(
        knoppen, text="Toevoegen", command=aanwezigheid_toevoegen,
        bg=blauw, activebackground=blauw, **view._knop_stijl(),
    ).pack(side="left", padx=(0, 10))

    # Aanpassen-knop
    aanpassen_knop = tk.Button(
        knoppen, text="Aanpassen", command=aanwezigheid_aanpassen, **view._knop_stijl()
    )
    aanpassen_knop.pack(side="left", padx=(0, 10))

    # Verwijderen-knop
    verwijderen_knop = tk.Button(
        knoppen, text="Verwijderen", command=aanwezigheid_verwijderen, **view._knop_stijl()
    )
    verwijderen_knop.pack(side="left")

    aanpassen_tooltip = Tooltip(
        aanpassen_knop, "Klik eerst op een record in het overzicht om te kunnen aanpassen."
    )
    verwijderen_tooltip = Tooltip(
        verwijderen_knop, "Klik eerst op een record in het overzicht om te kunnen verwijderen."
    )

    def update_knoppen():
        # Wordt aangeroepen telkens als de selectie verandert.
        # Pas de kleur van Aanpassen en Verwijderen aan:
        #   - geen selectie → grijs (inactief uiterlijk)
        #   - rij geselecteerd → groen/rood (actief uiterlijk)
        # De tooltips worden ook aan/uit gezet op hetzelfde moment.
        heeft_selectie = bool(geselecteerde_id.get())
        if heeft_selectie:
            aanpassen_knop.config(bg=groen, activebackground=groen)
            verwijderen_knop.config(bg=rood, activebackground=rood)
            aanpassen_tooltip.set_actief(False)   # tooltip verbergen
            verwijderen_tooltip.set_actief(False)
        else:
            aanpassen_knop.config(bg=licht_grijs, activebackground=licht_grijs)
            verwijderen_knop.config(bg=licht_grijs, activebackground=licht_grijs)
            aanpassen_tooltip.set_actief(True)    # tooltip tonen
            verwijderen_tooltip.set_actief(True)

    # Roep update_knoppen meteen aan zodat de knoppen correct zijn bij opstart
    update_knoppen()

    # Leegmaken-knop: onderaan het formulier, voert geen databank-actie uit
    tk.Button(
        form, text="Leegmaken", command=formulier_leegmaken,
        bg="#e7e7e7", fg=donker_grijs, activebackground=licht_grijs,
        bd=0, padx=10, pady=7, cursor="hand2",
    ).grid(row=7, column=0, sticky="ew", pady=(12, 0))

    # RECHTER KANT: OVERZICHTSTABEL
    # maak_kader aan de rechterkant, met fill="both" en expand=True
    # zodat de tabel de resterende ruimte van het venster vult.
    frame2 = maak_kader(
        view.afwezigheid_content,
        titel=f"Overzicht aanwezigheid ({len(data)})",
        header_kleur=blauw
    )
    frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

    # Treeview-tabel met vijf kolommen.
    # 'data' bevat tuples van de vorm: (id, naam, klas, datum, status)
    # Dit zijn de resultaten van get_attendance_overview() (met JOIN op naam).
    tabel = maak_tabel(
        frame2,
        kolommen=["ID", "Student", "Klas", "Datum", "Status"],
        data=data,
    )
    # Kolombreedte en uitlijning instellen per kolom
    tabel.column("ID",     width=50,  anchor="center")
    tabel.column("Student", width=150)
    tabel.column("Klas",   width=80,  anchor="center")
    tabel.column("Datum",  width=110, anchor="center")
    tabel.column("Status", width=90,  anchor="center")

    # Aparte opzoektabel met de records (id, student_id, datum, status).
    # We hebben deze nodig in on_select om het formulier in te vullen:
    # de tabel toont namen, maar het formulier werkt intern met student_id.
    attendance_per_id = {record[0]: record for record in view.controller.get_attendance()}

    def on_select(event):
        # Wordt automatisch opgeroepen door Tkinter zodra de gebruiker
        # op een rij in de tabel klikt (via tabel.bind hieronder).
        geselecteerd = tabel.selection()   # geeft een tuple met geselecteerde rij-ids

        if geselecteerd:
            # Haal de zichtbare waarden op van de aangeklikte rij
            rij = tabel.item(geselecteerd[0])["values"]

            # Sla het database-id op zodat aanpassen/verwijderen weet welk record
            geselecteerde_id.set(rij[0])

            # Zoek het ruwe record op (met student_id) zodat we het formulier
            # correct kunnen invullen (Combobox heeft het id nodig, niet de naam)
            record = attendance_per_id.get(int(rij[0]))
            if record:
                # record[0] = id, record[1] = student_id, record[2] = datum, record[3] = status
                studentInput.set(student_optie_per_id.get(record[1], ""))
                datumInput.delete(0, "end")
                datumInput.insert(0, record[2])
                statusInput.set(record[3])
        else:
            # Gebruiker heeft de selectie opgeheven
            geselecteerde_id.set("")

        # Herbereken de knopkleuren op basis van de nieuwe selectiestatus
        update_knoppen()

    # Koppel on_select aan het <<TreeviewSelect>>-event van de tabel.
    # Tkinter roept on_select automatisch op bij elke klik op een rij.
    tabel.bind("<<TreeviewSelect>>", on_select)
