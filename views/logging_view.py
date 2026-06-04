import tkinter as tk
from tkinter import messagebox, simpledialog

from views.handy_view import maak_kader, maak_tabel


blauw = "#185FA5"
groen = "#2f7d32"
rood = "#b3261e"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"


def toon_logging(view):
    view.clear_content()
    view.logging_content = tk.Frame(view.root, bg=grijs)
    view.logging_content.pack(fill="both", expand=True)

    data = view.controller.get_action_logs()
    analyse = view.controller.get_logging_analysis()

    linker_frame = maak_kader(
        view.logging_content,
        titel="Logging beheren",
        verticalSpace=20,
        horizontalSpace=20,
        header_kleur=blauw,
    )
    linker_frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

    form = tk.Frame(linker_frame, bg="white", padx=18, pady=16)
    form.pack(fill="x")

    huidige_gebruiker = view.controller.get_current_user_id()
    status_tekst = huidige_gebruiker if huidige_gebruiker else "Niet ingelogd"

    tk.Label(
        form,
        text=f"Huidige gebruiker: {status_tekst}",
        bg="white",
        fg=donker_grijs,
        font=("Arial", 10, "bold"),
        anchor="w",
    ).pack(fill="x", pady=(0, 14))

    knop_stijl = {
        "fg": "white",
        "activeforeground": "white",
        "bd": 0,
        "padx": 12,
        "pady": 8,
        "font": ("Arial", 9, "bold"),
        "cursor": "hand2",
    }

    def inloggen():
        user_id = simpledialog.askstring(
            "Logging",
            "Geef je user_id in:",
            parent=view.root,
        )
        if user_id is None:
            return

        melding = view.controller.start_logging(user_id)
        if not view._toon_melding("Logging", melding):
            return
        view.logging()

    def uitloggen():
        melding = view.controller.stop_logging()
        if not view._toon_melding("Logging", melding):
            return
        view.logging()

    tk.Button(
        form,
        text="Inloggen",
        command=inloggen,
        bg=groen,
        activebackground=groen,
        **knop_stijl,
    ).pack(fill="x", pady=(0, 8))

    tk.Button(
        form,
        text="Uitloggen",
        command=uitloggen,
        bg=rood if huidige_gebruiker else licht_grijs,
        activebackground=rood if huidige_gebruiker else licht_grijs,
        **knop_stijl,
    ).pack(fill="x")

    frame_actief = maak_kader(
        view.logging_content,
        titel="Meest actieve gebruiker(s)",
        verticalSpace=20,
        horizontalSpace=20,
        header_kleur=blauw,
    )
    frame_actief.pack_configure(side="left", fill="y", padx=(10, 10), pady=20, anchor="nw")

    tabel_actief = maak_tabel(
        frame_actief,
        kolommen=["Gebruiker", "Aantal acties"],
        data=analyse["most_active"],
    )
    tabel_actief.column("Gebruiker", width=140, anchor="w")
    tabel_actief.column("Aantal acties", width=100, anchor="center")

    rechter_frame = maak_kader(
        view.logging_content,
        titel=f"Overzicht logs ({len(data)})",
        verticalSpace=20,
        horizontalSpace=20,
        header_kleur=blauw,
    )
    rechter_frame.pack_configure(side="left", fill="both", expand=True, padx=(10, 20), pady=20, anchor="nw")

    tabel = maak_tabel(
        rechter_frame,
        kolommen=["ID", "Gebruiker", "Actietype", "Tijdstip"],
        data=data,
    )
    tabel.column("ID", width=60, anchor="center")
    tabel.column("Gebruiker", width=130, anchor="w")
    tabel.column("Actietype", width=100, anchor="center")
    tabel.column("Tijdstip", width=160, anchor="center")
