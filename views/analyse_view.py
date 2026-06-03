import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.handy_view import maak_kader, maak_tabel

# kleuren
blauw = "#185FA5"
grijs = "#eee"


def toon_analyse(view):
    view.clear_content()
    view.analyse_content = tk.Frame(view.root, bg=grijs)
    view.analyse_content.pack(fill="both", expand=True)

    analyse_data = view.controller.get_analysis()
    transporten = view.controller.get_transport()
    transport_namen = {transport[0]: transport[1] for transport in transporten}

    # ── frame links: aantal per vervoersmiddel (tabel) ──
    frame = maak_kader(view.analyse_content, titel="Gebruik per vervoertype", header_kleur=blauw)
    frame.pack_configure(side="left", padx=(20, 10), pady=20, fill="y", anchor="nw")

    tabel_data = [
        (transport_namen.get(transport_id, "Onbekend"), aantal)
        for transport_id, aantal in analyse_data["transport"]
    ]
    tabel = maak_tabel(frame, kolommen=["Vervoer", "Aantal verplaatsingen"], data=tabel_data)
    tabel.column("Vervoer", width=150, anchor="w")
    tabel.column("Aantal verplaatsingen", width=150, anchor="center")

    # ── frame midden: gemiddelde afstand (tabel) ──
    frame2 = maak_kader(view.analyse_content, titel="Gemiddelde afstand tot school", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(0, 10), pady=20, fill="y", anchor="nw")

    gem_alle = round(analyse_data["avg_distance"], 2) if analyse_data["avg_distance"] else 0
    tabel2_data = [("Alle studenten", f"{gem_alle} km")]
    for transport_type, gemiddelde in analyse_data["avg_distance_per_transport"]:
        tabel2_data.append((transport_type, f"{gemiddelde} km"))

    tabel2 = maak_tabel(frame2, kolommen=["Categorie", "Gem. afstand"], data=tabel2_data)
    tabel2.column("Categorie", width=150, anchor="w")
    tabel2.column("Gem. afstand", width=120, anchor="center")

    # ── frame rechts: balkdiagram gemiddelde afstand per vervoersmiddel ──
    frame3 = maak_kader(view.analyse_content, titel="Grafiek gemiddelde afstand", header_kleur=blauw)
    frame3.pack_configure(side="left", padx=(0, 20), pady=20, fill="both", expand=True, anchor="nw")

    grafiek_frame = tk.Frame(frame3, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # data voor de grafiek - makkelijk aanpasbaar hier
    labels = [rij[0] for rij in analyse_data["avg_distance_per_transport"]]
    waarden = [rij[1] for rij in analyse_data["avg_distance_per_transport"]]

    if labels and waarden:
        # kleuren per balk - makkelijk aanpasbaar
        kleuren = ["#185FA5", "#2f7d32", "#b3261e", "#f0a500"]

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("white")

        balken = ax.bar(labels, waarden, color=kleuren[:len(labels)])

        # waarde boven elke balk tonen
        for balk in balken:
            hoogte = balk.get_height()
            ax.text(
                balk.get_x() + balk.get_width() / 2,
                hoogte + 0.1,
                f"{hoogte} km",
                ha="center", va="bottom", fontsize=9, fontweight="bold"
            )

        ax.set_title("Gem. afstand per vervoersmiddel (km)", fontsize=11, fontweight="bold")
        ax.set_xlabel("Vervoersmiddel")
        ax.set_ylabel("Afstand (km)")
        ax.set_ylim(0, max(waarden) + 2)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        tk.Label(grafiek_frame, text="Geen data beschikbaar", bg="white", font=("Arial", 10)).pack(pady=20)