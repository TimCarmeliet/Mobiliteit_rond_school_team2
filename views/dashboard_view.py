import tkinter as tk
from handy_view import maak_kader, maak_tabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# kleur
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"

def toon_dashboard(view):
    view.clear_content()
    view.dashboard_content = tk.Frame(view.root, bg=grijs)
    view.dashboard_content.pack(fill="both", expand=True)

    # haal de data op via de controller
    verdeling = view.controller.get_transport_verdeling()

    # frame voor de grafiek
    frame = maak_kader(view.dashboard_content, titel="Verdeling vervoersmiddelen", header_kleur=blauw)
    frame.pack_configure(side="left", padx=20, pady=20, fill="both", expand=True)

    grafiek_frame = tk.Frame(frame, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)
    # data klaarmaken voor de grafiek
    labels = [rij[0] for rij in verdeling]
    waarden = [rij[1] for rij in verdeling]

     # balkdiagram maken met matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor("white")

    kleuren = ["#185FA5", "#2f7d32", "#b3261e", "#f0a500"]
    balken = ax.bar(labels, waarden, color=kleuren[:len(labels)])

    # waarde boven elke balk tonen
    for balk in balken:
        hoogte = balk.get_height()
        ax.text(
            balk.get_x() + balk.get_width() / 2,
            hoogte + 0.3,
            str(int(hoogte)),
            ha="center", va="bottom", fontsize=10, fontweight="bold"
        )

    ax.set_title("Aantal verplaatsingen per vervoersmiddel", fontsize=12, fontweight="bold")
    ax.set_xlabel("Vervoersmiddel")
    ax.set_ylabel("Aantal verplaatsingen")
    ax.set_ylim(0, max(waarden) + 20)
    fig.tight_layout()

    # grafiek inbedden in tkinter
    canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # frame voor de tabel naast de grafiek
    frame2 = maak_kader(view.dashboard_content, titel="Overzicht in cijfers", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(0, 20), pady=20, anchor="nw")

    tabel_data = [(rij[0], rij[1], f"{round(rij[1] / sum(waarden) * 100, 1)}%") for rij in verdeling]
    tabel = maak_tabel(frame2, kolommen=["Vervoersmiddel", "Aantal", "Percentage"], data=tabel_data)
    tabel.column("Vervoersmiddel", width=130)
    tabel.column("Aantal", width=80, anchor="center")
    tabel.column("Percentage", width=90, anchor="center")