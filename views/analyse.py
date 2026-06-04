import tkinter as tk

from views.handy_view import maak_kader, maak_tabel


blauw = "#185FA5"
grijs = "#eee"
donker_grijs = "#333333"


def _format_getal(waarde, suffix=""):
    if waarde is None:
        return "Geen data"
    return f"{round(waarde, 2)}{suffix}"


def toon_analyse(view):
    view.clear_content()

    view.analyse_content = tk.Frame(view.root, bg=grijs)
    view.analyse_content.pack(fill="both", expand=True)

    analyse_data = view.controller.get_analysis()
    actieve_analyse = tk.StringVar(value="vervoer")

    analyse_nav = tk.Frame(view.analyse_content, bg=grijs)
    analyse_nav.pack(side="top", fill="x", pady=(10, 0))

    nav_center = tk.Frame(analyse_nav, bg=grijs)
    nav_center.pack(expand=True)

    analyse_frame = tk.Frame(view.analyse_content, bg=grijs)
    analyse_frame.pack(fill="both", expand=True, padx=20, pady=20)

    knoppen = {}

    knop_stijl = {
        "fg": "white",
        "activeforeground": "white",
        "bd": 0,
        "relief": "flat",
        "padx": 18,
        "pady": 9,
        "font": ("Arial", 9, "bold"),
        "cursor": "hand2",
    }

    def maak_analyse_leeg():
        for widget in analyse_frame.winfo_children():
            widget.destroy()

    def update_knoppen():
        for naam, knop in knoppen.items():
            if naam == actieve_analyse.get():
                knop.config(bg=blauw, activebackground=blauw)
            else:
                knop.config(bg="#d9d9d9", activebackground="#cfcfcf")

    def toon_vervoer():
        actieve_analyse.set("vervoer")
        update_knoppen()
        maak_analyse_leeg()

        frame = maak_kader(
            analyse_frame,
            titel="Aantal per vervoersmiddel",
            verticalSpace=0,
            horizontalSpace=0,
            header_kleur=blauw,
        )
        frame.pack(fill="both", expand=True)

        tabel = maak_tabel(
            frame,
            kolommen=["Vervoer", "Aantal verplaatsingen"],
            data=analyse_data["transport"],
        )

        tabel.column("Vervoer", width=220, anchor="w")
        tabel.column("Aantal verplaatsingen", width=150, anchor="center")

    def toon_afstand():
        actieve_analyse.set("afstand")
        update_knoppen()
        maak_analyse_leeg()

        frame = maak_kader(
            analyse_frame,
            titel="Gemiddelde afstand",
            verticalSpace=0,
            horizontalSpace=0,
            header_kleur=blauw,
        )
        frame.pack(fill="both", expand=True)

        totaal_tekst = _format_getal(analyse_data["avg_distance"], " km")

        tk.Label(
            frame,
            text=f"Gemiddelde afstand alle studenten: {totaal_tekst}",
            bg="white",
            fg=donker_grijs,
            font=("Arial", 11, "bold"),
            anchor="w",
            padx=10,
            pady=10,
        ).pack(fill="x")

        tabel = maak_tabel(
            frame,
            kolommen=["Vervoer", "Gemiddelde afstand"],
            data=analyse_data["avg_distance_by_transport"],
        )

        tabel.column("Vervoer", width=220, anchor="w")
        tabel.column("Gemiddelde afstand", width=150, anchor="center")

    def toon_klassen():
        actieve_analyse.set("klassen")
        update_knoppen()
        maak_analyse_leeg()

        frame = maak_kader(
            analyse_frame,
            titel="Overzicht per klas",
            verticalSpace=0,
            horizontalSpace=0,
            header_kleur=blauw,
        )
        frame.pack(fill="both", expand=True)

        tabel = maak_tabel(
            frame,
            kolommen=[
                "Klas",
                "Aantal studenten",
                "Gemiddelde afstand",
                "Vervoersmiddelen",
            ],
            data=analyse_data["classes"],
        )

        tabel.column("Klas", width=80, anchor="center")
        tabel.column("Aantal studenten", width=120, anchor="center")
        tabel.column("Gemiddelde afstand", width=140, anchor="center")
        tabel.column("Vervoersmiddelen", width=300, anchor="w")

    def toon_per_leerling():
        actieve_analyse.set("leerling")
        update_knoppen()
        maak_analyse_leeg()

        frame = maak_kader(
            analyse_frame,
            titel="Aantal verschillende vervoersmiddelen per leerling",
            verticalSpace=0,
            horizontalSpace=0,
            header_kleur=blauw,
        )
        frame.pack(fill="both", expand=True)

        # Samenvatting boven de tabel tonen
        summary_frame = tk.Frame(frame, bg="white", padx=10, pady=10)
        summary_frame.pack(fill="x", before=None)

        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for _, aantal in analyse_data["transport_per_student"]:
            counts[aantal] = counts.get(aantal, 0) + 1

        summary_text = (
            f"Aantal leerlingen per aantal gebruikte vervoersmiddelen:\n"
            f"   • 1 vervoersmiddel: {counts.get(1, 0)} leerlingen\n"
            f"   • 2 vervoersmiddelen: {counts.get(2, 0)} leerlingen\n"
            f"   • 3 vervoersmiddelen: {counts.get(3, 0)} leerlingen\n"
            f"   • 4 vervoersmiddelen: {counts.get(4, 0)} leerlingen"
        )

        tk.Label(
            summary_frame,
            text=summary_text,
            bg="white",
            fg=donker_grijs,
            font=("Arial", 10, "bold"),
            justify="left",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        tabel = maak_tabel(
            frame,
            kolommen=["Leerling", "Aantal vervoer"],
            data=analyse_data["transport_per_student"],
        )

        tabel.column("Leerling", width=220, anchor="w")
        tabel.column("Aantal vervoer", width=180, anchor="center")

    knoppen["vervoer"] = tk.Button(
        nav_center,
        text="Vervoersmiddelen",
        command=toon_vervoer,
        **knop_stijl,
    )
    knoppen["vervoer"].pack(side="left")

    knoppen["afstand"] = tk.Button(
        nav_center,
        text="Afstand",
        command=toon_afstand,
        **knop_stijl,
    )
    knoppen["afstand"].pack(side="left")

    knoppen["klassen"] = tk.Button(
        nav_center,
        text="Klassen",
        command=toon_klassen,
        **knop_stijl,
    )
    knoppen["klassen"].pack(side="left")

    knoppen["leerling"] = tk.Button(
        nav_center,
        text="Per leerling",
        command=toon_per_leerling,
        **knop_stijl,
    )
    knoppen["leerling"].pack(side="left")

    toon_vervoer()
