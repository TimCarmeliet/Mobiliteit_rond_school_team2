import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.handy_view import maak_kader, maak_tabel

# kleuren
blauw = "#185FA5"
grijs = "#eee"

# ── GRAFIEK INSTELLINGEN - makkelijk aanpasbaar ──────────────────────────────
# Verander GRAFIEK_TYPE naar "balk" of "taart" om de grafiek te wisselen
GRAFIEK_TYPE = "balk"

# kleuren per vervoersmiddel (wordt gebruikt in beide grafiektypes)
GRAFIEK_KLEUREN = ["#185FA5", "#2f7d32", "#b3261e", "#f0a500"]

# grootte van de grafiek (breedte, hoogte in inches)
GRAFIEK_GROOTTE = (5, 4)
# ─────────────────────────────────────────────────────────────────────────────


def _maak_grafiek(ax, labels, waarden):
    # balkdiagram
    if GRAFIEK_TYPE == "balk":
        balken = ax.bar(labels, waarden, color=GRAFIEK_KLEUREN[:len(labels)])
        for balk in balken:
            hoogte = balk.get_height()
            ax.text(
                balk.get_x() + balk.get_width() / 2,
                hoogte + 0.3,
                str(int(hoogte)),
                ha="center", va="bottom", fontsize=10, fontweight="bold"
            )
        ax.set_xlabel("Vervoersmiddel")
        ax.set_ylabel("Aantal verplaatsingen")
        ax.set_ylim(0, max(waarden) + 20)

    # taartdiagram
    elif GRAFIEK_TYPE == "taart":
        ax.pie(
            waarden,
            labels=labels,
            colors=GRAFIEK_KLEUREN[:len(labels)],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")

    ax.set_title("Verdeling vervoersmiddelen", fontsize=12, fontweight="bold")


def toon_dashboard(view):
    view.clear_content()
    view.dashboard_content = tk.Frame(view.root, bg=grijs)
    view.dashboard_content.pack(fill="both", expand=True)

    # haal data op via de controller
    verdeling = view.controller.get_transport_verdeling()
    labels = [rij[0] for rij in verdeling]
    waarden = [rij[1] for rij in verdeling]
    totaal = sum(waarden)

    # ── frame links: grafiek ──
    frame = maak_kader(view.dashboard_content, titel="Verdeling vervoersmiddelen", header_kleur=blauw)
    frame.pack_configure(side="left", padx=20, pady=20, fill="both", expand=True)

    grafiek_frame = tk.Frame(frame, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    fig, ax = plt.subplots(figsize=GRAFIEK_GROOTTE)
    fig.patch.set_facecolor("white")
    _maak_grafiek(ax, labels, waarden)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # ── frame rechts: legende + cijfers ──
    frame2 = maak_kader(view.dashboard_content, titel="Overzicht in cijfers", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(0, 20), pady=20, anchor="nw")

    # legende bovenaan
    legende_frame = tk.Frame(frame2, bg="white", padx=10, pady=8)
    legende_frame.pack(fill="x")

    for i, label in enumerate(labels):
        kleur = GRAFIEK_KLEUREN[i % len(GRAFIEK_KLEUREN)]
        rij = tk.Frame(legende_frame, bg="white")
        rij.pack(anchor="w", pady=2)
        # kleurvakje
        tk.Label(rij, bg=kleur, width=2, relief="flat").pack(side="left", padx=(0, 6))
        tk.Label(rij, text=label, bg="white", font=("Arial", 9), anchor="w").pack(side="left")

    # scheidingslijn
    tk.Frame(frame2, height=1, bg="#cccccc").pack(fill="x", padx=10)

    # tabel met cijfers
    tabel_data = [
        (rij[0], rij[1], f"{round(rij[1] / totaal * 100, 1)}%")
        for rij in verdeling
    ]
    tabel = maak_tabel(frame2, kolommen=["Vervoersmiddel", "Aantal", "Percentage"], data=tabel_data)
    tabel.column("Vervoersmiddel", width=130)
    tabel.column("Aantal", width=80, anchor="center")
    tabel.column("Percentage", width=90, anchor="center")