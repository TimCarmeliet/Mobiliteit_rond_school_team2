"""
dashboard_view.py
=================
Toont het hoofddashboard met drie tabbladen via ttk.Notebook:

  Tab 1 – Vervoersmiddelen : bestaande grafiek + tabel
  Tab 2 – Overzicht per klas : tabel + gestapeld balkdiagram vervoer per klas
  Tab 3 – Afwezigheid      : uitbreiding Viggo
             • tabel: aanwezigheidspercentage per klas
             • tabel: vervoersmiddel vs aanwezigheid
             • gestapeld balkdiagram per klas (aanwezig / afwezig / laat)
"""

import tkinter as tk
from tkinter import ttk                                   # voor het Notebook (tabbladen)
from views.handy_view import maak_kader, maak_tabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Kleuren consistent met de rest van de applicatie
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"


def toon_dashboard(view):
    """
    Hoofdfunctie voor het dashboard.
    Maakt een ttk.Notebook aan met twee tabbladen:
      - Tab 1: Vervoersmiddelen (bestaande functionaliteit)
      - Tab 2: Afwezigheid & Aanwezigheid (uitbreiding Viggo)
    """
    view.clear_content()
    view.dashboard_content = tk.Frame(view.root, bg=grijs)
    view.dashboard_content.pack(fill="both", expand=True)

    # Notebook = de widget die tabbladen beheert in Tkinter (ttk.Notebook)
    notebook = ttk.Notebook(view.dashboard_content)
    notebook.pack(fill="both", expand=True, padx=5, pady=5)

    # ── Tab 1: Vervoersmiddelen (bestaande functionaliteit) ───────────────────
    tab_vervoer = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_vervoer, text="Vervoersmiddelen")
    _toon_vervoer_tab(view, tab_vervoer)

    # ── Tab 2: Overzicht per klas ─────────────────────────────────────────────
    tab_klas = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_klas, text="Overzicht per klas")
    _toon_klas_dashboard(view, tab_klas)

    # ── Tab 3: Afwezigheid (uitbreiding Viggo) ────────────────────────────────
    tab_afwezigheid = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_afwezigheid, text="Afwezigheid & Aanwezigheid")
    _toon_afwezigheid_dashboard(view, tab_afwezigheid)


# ── Tab 1: Vervoersmiddelen ───────────────────────────────────────────────────

def _toon_vervoer_tab(view, parent):
    """
    Toont de grafiek en tabel voor de verdeling van vervoersmiddelen.
    Dit is de originele dashboardinhoud, nu in een tabblad geplaatst.
    'parent' is het tabblad-frame waarin alles wordt opgebouwd.
    """
    # Verdelingsdata ophalen via de controller
    verdeling = view.controller.get_transport_verdeling()

    # Frame voor de grafiek (links)
    frame = maak_kader(parent, titel="Verdeling vervoersmiddelen", header_kleur=blauw)
    frame.pack_configure(side="left", padx=20, pady=20, fill="both", expand=True)

    grafiek_frame = tk.Frame(frame, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Data klaarmaken voor matplotlib
    labels = [rij[0] for rij in verdeling]
    waarden = [rij[1] for rij in verdeling]

    if not waarden:
        # geen data beschikbaar: toon een melding in plaats van een lege grafiek
        tk.Label(grafiek_frame, text="Geen verplaatsingsdata beschikbaar.",
                 bg="white", font=("Arial", 11), fg=donker_grijs).pack(pady=30)
    else:
        # Balkdiagram maken met matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("white")

        kleuren = ["#185FA5", "#2f7d32", "#b3261e", "#f0a500"]
        balken = ax.bar(labels, waarden, color=kleuren[:len(labels)])

        # Waarde boven elke balk tonen
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

        # Grafiek inbedden in de Tkinter-widget via de matplotlib-backend
        canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Frame voor de tabel (rechts naast de grafiek)
    frame2 = maak_kader(parent, titel="Overzicht in cijfers", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(0, 20), pady=20, anchor="nw")

    totaal = sum(waarden) if waarden else 1  # vermijd deling door nul
    tabel_data = [
        (rij[0], rij[1], f"{round(rij[1] / totaal * 100, 1)}%")
        for rij in verdeling
    ]
    tabel = maak_tabel(frame2, kolommen=["Vervoersmiddel", "Aantal", "Percentage"], data=tabel_data)
    tabel.column("Vervoersmiddel", width=130)
    tabel.column("Aantal", width=80, anchor="center")
    tabel.column("Percentage", width=90, anchor="center")


# ── Tab 2: Overzicht per klas ─────────────────────────────────────────────────

# Kleuren per vervoerstype voor het gestapeld balkdiagram.
# Pas hier de kleur van een vervoerstype aan als je dat wil.
VERVOER_KLEUREN = {
    "fiets":   "#185FA5",   # blauw
    "bus":     "#2f7d32",   # groen
    "auto":    "#b3261e",   # rood
    "te voet": "#f0a500",   # oranje
}
# Fallback-kleuren voor eventuele extra vervoerstypes
_EXTRA_KLEUREN = ["#9b59b6", "#1abc9c", "#e67e22", "#2ecc71"]


def _toon_klas_dashboard(view, parent):
    """
    Toont het dashboardtabblad 'Overzicht per klas'.

    Links : tabel  – klas | aantal studenten | gem. afstand (km)
    Rechts: grafiek – gestapeld balkdiagram met vervoersverdeling per klas
                      elke kleur = één vervoerstype
                      elke balk  = één klas
    """
    # Data ophalen via de controller
    klas_data = view.controller.get_overzicht_per_klas()

    if not klas_data:
        tk.Label(parent, text="Geen klasdata beschikbaar.",
                 bg=grijs, font=("Arial", 11), fg=donker_grijs).pack(pady=40)
        return

    # ── LINKS: samenvattingstabel ─────────────────────────────────────────────
    linker_frame = tk.Frame(parent, bg=grijs)
    linker_frame.pack(side="left", fill="y", padx=10, pady=10)

    frame_tabel = maak_kader(linker_frame, titel="Samenvatting per klas", header_kleur=blauw)
    frame_tabel.pack(anchor="nw")

    tabel_rijen = [
        (r["klas"], r["aantal"], f'{r["gem_afstand"]:.2f} km')
        for r in klas_data
    ]
    tabel = maak_tabel(
        frame_tabel,
        kolommen=["Klas", "Aantal studenten", "Gem. afstand (km)"],
        data=tabel_rijen,
    )
    tabel.column("Klas",              width=80,  anchor="center")
    tabel.column("Aantal studenten",  width=130, anchor="center")
    tabel.column("Gem. afstand (km)", width=130, anchor="center")

    # ── RECHTS: gestapeld balkdiagram ─────────────────────────────────────────
    rechter_frame = tk.Frame(parent, bg=grijs)
    rechter_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_grafiek = maak_kader(
        rechter_frame, titel="Vervoersverdeling per klas (grafiek)", header_kleur=blauw
    )
    frame_grafiek.pack(fill="both", expand=True)

    grafiek_frame = tk.Frame(frame_grafiek, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Verzamel alle vervoerstypes die voorkomen over alle klassen (gesorteerd)
    alle_types = sorted({v for r in klas_data for v in r["vervoer"].keys()})
    klassen    = [r["klas"] for r in klas_data]
    x          = list(range(len(klassen)))

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("white")

    # Gestapeld balkdiagram: per vervoerstype één laag bovenop de vorige
    bottoms = [0] * len(klassen)   # beginpunt van de volgende laag per klas
    for i, vervoer_type in enumerate(alle_types):
        waarden = [r["vervoer"].get(vervoer_type, 0) for r in klas_data]
        # kleur opzoeken in VERVOER_KLEUREN, anders neem een fallback
        kleur = VERVOER_KLEUREN.get(vervoer_type.lower(),
                                    _EXTRA_KLEUREN[i % len(_EXTRA_KLEUREN)])
        ax.bar(x, waarden, bottom=bottoms, label=vervoer_type.capitalize(), color=kleur)
        # verschuif de bodem voor de volgende laag
        bottoms = [b + w for b, w in zip(bottoms, waarden)]

    ax.set_title("Vervoersverdeling per klas", fontsize=12, fontweight="bold")
    ax.set_xlabel("Klas")
    ax.set_ylabel("Aantal verplaatsingen")
    ax.set_xticks(x)
    ax.set_xticklabels(klassen)
    ax.legend(loc="upper right")
    fig.tight_layout()

    # Grafiek inbedden in Tkinter via de matplotlib-backend
    canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# ── Tab 3: Afwezigheid (uitbreiding Viggo) ────────────────────────────────────

def _toon_afwezigheid_dashboard(view, parent):
    """
    Uitbreiding Viggo: dashboardweergave van aanwezigheidsanalyse.

    Links: twee informatietabellen
      1. Aanwezigheidspercentage per klas
         (klas | aanwezig | afwezig | laat | totaal | % aanwezig)
      2. Relatie vervoersmiddel vs aanwezigheid
         (vervoer | aanwezig | afwezig | laat)

    Rechts: gestapeld balkdiagram per klas
      - Groen  = aanwezig
      - Rood   = afwezig
      - Oranje = laat
    Dit diagram maakt het onmiddellijk zichtbaar hoe de aanwezigheid
    per klas verdeeld is.
    """
    # Data ophalen via de controller (geen directe databanktoegang vanuit de view)
    percentages = view.controller.get_aanwezigheid_percentage_per_klas()
    vervoer_vs = view.controller.get_vervoer_vs_aanwezigheid()
    klas_data = view.controller.get_afwezigheid_per_klas()

    # ── LINKS: tabellen ───────────────────────────────────────────────────────
    linker_frame = tk.Frame(parent, bg=grijs)
    linker_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Tabel 1: aanwezigheidspercentage per klas
    frame1 = maak_kader(linker_frame, titel="% Aanwezigheid per klas", header_kleur=blauw)
    frame1.pack(pady=(0, 10), anchor="nw")

    tabel1_data = [
        (klas, aanwezig, afwezig, laat, totaal, f"{percentage}%")
        for klas, aanwezig, afwezig, laat, totaal, percentage in percentages
    ]
    tabel1 = maak_tabel(
        frame1,
        kolommen=["Klas", "Aanwezig", "Afwezig", "Laat", "Totaal", "% Aanwezig"],
        data=tabel1_data,
    )
    tabel1.column("Klas", width=70, anchor="center")
    tabel1.column("Aanwezig", width=70, anchor="center")
    tabel1.column("Afwezig", width=70, anchor="center")
    tabel1.column("Laat", width=60, anchor="center")
    tabel1.column("Totaal", width=60, anchor="center")
    tabel1.column("% Aanwezig", width=85, anchor="center")

    # Tabel 2: vervoersmiddel vs aanwezigheid
    # Toont hoe aanwezigheid verschilt per type vervoer
    frame2 = maak_kader(linker_frame, titel="Vervoer vs Aanwezigheid", header_kleur=blauw)
    frame2.pack(anchor="nw")

    tabel2_data = [
        (
            transport,
            counts.get("aanwezig", 0),
            counts.get("afwezig", 0),
            counts.get("laat", 0),
        )
        for transport, counts in sorted(vervoer_vs.items())
    ]
    tabel2 = maak_tabel(
        frame2,
        kolommen=["Vervoer", "Aanwezig", "Afwezig", "Laat"],
        data=tabel2_data,
    )
    tabel2.column("Vervoer", width=100, anchor="w")
    tabel2.column("Aanwezig", width=80, anchor="center")
    tabel2.column("Afwezig", width=70, anchor="center")
    tabel2.column("Laat", width=60, anchor="center")

    # ── RECHTS: gestapeld balkdiagram ─────────────────────────────────────────
    rechter_frame = tk.Frame(parent, bg=grijs)
    rechter_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame3 = maak_kader(rechter_frame, titel="Aanwezigheid per klas (grafiek)", header_kleur=blauw)
    frame3.pack(fill="both", expand=True)

    grafiek_frame = tk.Frame(frame3, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    if not klas_data:
        # Als er nog geen aanwezigheidsdata is, toon een duidelijke melding
        tk.Label(
            grafiek_frame,
            text="Nog geen aanwezigheidsdata beschikbaar.\n"
                 "Voeg records toe via het 'Afwezigheid' menu.",
            bg="white", font=("Arial", 11), fg=donker_grijs, justify="center"
        ).pack(pady=40)
        return

    # Data klaarmaken voor het gestapeld balkdiagram
    klassen = sorted(klas_data.keys())
    aanwezig_vals = [klas_data[k].get("aanwezig", 0) for k in klassen]
    afwezig_vals = [klas_data[k].get("afwezig", 0) for k in klassen]
    laat_vals = [klas_data[k].get("laat", 0) for k in klassen]

    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor("white")

    x = list(range(len(klassen)))

    # Gestapeld balkdiagram: aanwezig onderaan, afwezig erboven, laat bovenaan.
    # 'bottom' geeft aan waar de volgende laag begint.
    ax.bar(x, aanwezig_vals, label="Aanwezig", color=groen)
    ax.bar(x, afwezig_vals, bottom=aanwezig_vals, label="Afwezig", color=rood)

    # Bottom van de "laat"-laag = aanwezig + afwezig
    bottom_laat = [a + b for a, b in zip(aanwezig_vals, afwezig_vals)]
    ax.bar(x, laat_vals, bottom=bottom_laat, label="Laat", color="#f0a500")

    ax.set_title("Aanwezigheid per klas", fontsize=12, fontweight="bold")
    ax.set_xlabel("Klas")
    ax.set_ylabel("Aantal registraties")
    ax.set_xticks(x)
    ax.set_xticklabels(klassen)
    ax.legend()
    fig.tight_layout()

    # Grafiek inbedden in Tkinter via de matplotlib FigureCanvasTkAgg-backend
    canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
