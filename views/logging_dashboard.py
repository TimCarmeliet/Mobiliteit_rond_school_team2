import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from views.handy_view import maak_kader, maak_tabel


blauw = "#185FA5"
groen = "#2f7d32"
rood = "#b3261e"
grijs = "#eee"
donker_grijs = "#333333"


def toon_logging_dashboard(view, parent):
    data = view.controller.get_logging_analysis()

    linker_frame = tk.Frame(parent, bg=grijs)
    linker_frame.pack(side="left", fill="y", padx=10, pady=10)

    frame_user = maak_kader(linker_frame, titel="Acties per gebruiker", header_kleur=blauw)
    frame_user.pack(anchor="nw", pady=(0, 10))
    tabel_user = maak_tabel(
        frame_user,
        kolommen=["Gebruiker", "Aantal acties"],
        data=data["by_user"],
    )
    tabel_user.column("Gebruiker", width=140, anchor="w")
    tabel_user.column("Aantal acties", width=100, anchor="center")

    frame_type = maak_kader(linker_frame, titel="Acties per type", header_kleur=blauw)
    frame_type.pack(anchor="nw")
    tabel_type = maak_tabel(
        frame_type,
        kolommen=["Actietype", "Aantal"],
        data=data["by_type"],
    )
    tabel_type.column("Actietype", width=120, anchor="w")
    tabel_type.column("Aantal", width=90, anchor="center")

    rechter_frame = tk.Frame(parent, bg=grijs)
    rechter_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_grafiek = maak_kader(rechter_frame, titel="Visualisatie acties per type", header_kleur=blauw)
    frame_grafiek.pack(fill="both", expand=True)

    grafiek_frame = tk.Frame(frame_grafiek, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    if not data["by_type"]:
        tk.Label(
            grafiek_frame,
            text="Nog geen logdata beschikbaar.",
            bg="white",
            fg=donker_grijs,
            font=("Arial", 11),
        ).pack(pady=40)
        return

    labels = [row[0] for row in data["by_type"]]
    waarden = [row[1] for row in data["by_type"]]
    kleuren = [blauw, groen, rood, "#f0a500", "#777777"]

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor("white")
    balken = ax.bar(labels, waarden, color=kleuren[:len(labels)])

    for balk in balken:
        hoogte = balk.get_height()
        ax.text(
            balk.get_x() + balk.get_width() / 2,
            hoogte + 0.2,
            str(int(hoogte)),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title("Aantal acties per type", fontsize=12, fontweight="bold")
    ax.set_xlabel("Actietype")
    ax.set_ylabel("Aantal")
    ax.set_ylim(0, max(waarden) + 2)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
