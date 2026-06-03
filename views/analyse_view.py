"""
analyse_view.py
===============
Toont de analysefunctionaliteiten in een tabblad-scherm (ttk.Notebook).

════════════════════════════════════════════════════════
HOE EEN NIEUWE ANALYSE TOEVOEGEN?
  1. Schrijf een bouwfunctie _bouw_mijn_analyse(tab, controller)
  2. Voeg een regel toe aan de lijst ANALYSE_TABS onderaan dit bestand:
         ("Naam van tabblad", _bouw_mijn_analyse)
════════════════════════════════════════════════════════

Huidige tabbladen:
  1. Overzicht per klas   – aantal studenten, gem. afstand, vervoersverdeling
  2. Gebruik per vervoer  – hoeveel verplaatsingen per transporttype
"""

import tkinter as tk
from tkinter import ttk
from views.handy_view import maak_kader, maak_tabel

# ── Kleuren (consistent met de rest van de applicatie) ────────────────────────
blauw       = "#185FA5"
grijs       = "#eee"
donker_grijs = "#333333"


# ── Hoofdfunctie (aangeroepen vanuit main_view.py) ────────────────────────────

def toon_analyse(view):
    """
    Bouwt het volledige analysescherm op met een ttk.Notebook.
    Elk tabblad roept zijn eigen bouwfunctie aan.
    """
    view.clear_content()
    view.analyse_content = tk.Frame(view.root, bg=grijs)
    view.analyse_content.pack(fill="both", expand=True)

    notebook = ttk.Notebook(view.analyse_content)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    # Maak elk tabblad aan op basis van ANALYSE_TABS (zie onderaan dit bestand)
    for tabblad_naam, bouw_functie in ANALYSE_TABS:
        tab = tk.Frame(notebook, bg=grijs)
        notebook.add(tab, text=tabblad_naam)
        bouw_functie(tab, view.controller)


# ── Tab 1: Overzicht per klas ─────────────────────────────────────────────────
#
# Toont:
#   • Tabel A – klas | aantal studenten | gem. afstand (km)
#   • Tabel B – klas | vervoersmiddel | aantal verplaatsingen | %
#
# ─────────────────────────────────────────────────────────────────────────────

# Kolombreedtes voor Tabel A (pas hier aan om de weergave te wijzigen)
_KLAS_KOLOMMEN = {
    "Klas":              80,
    "Aantal studenten": 130,
    "Gem. afstand (km)": 140,
}

# Kolombreedtes voor Tabel B
_VERVOER_KOLOMMEN = {
    "Klas":                    80,
    "Vervoersmiddel":         140,
    "Aantal verplaatsingen":  160,
    "% van klas":              90,
}


def _bouw_overzicht_per_klas(tab, controller):
    """
    Bouwt de inhoud van het 'Overzicht per klas'-tabblad.

    Stap 1: data ophalen via de controller
    Stap 2: data omzetten naar tabelrijen
    Stap 3: Tabel A opbouwen (klas-samenvatting)
    Stap 4: Tabel B opbouwen (vervoersverdeling per klas)
    """
    # ── Stap 1: data ophalen ──────────────────────────────────────────────────
    # get_overzicht_per_klas() geeft een lijst van dicts:
    # [{ klas, aantal, gem_afstand, vervoer: {type: n} }, ...]
    data = controller.get_overzicht_per_klas()

    # ── Stap 2a: rijen voor Tabel A ───────────────────────────────────────────
    # Elke rij = (klas, aantal studenten, gem. afstand)
    tabel_a_rijen = [
        (rij["klas"], rij["aantal"], f'{rij["gem_afstand"]:.2f} km')
        for rij in data
    ]

    # ── Stap 2b: rijen voor Tabel B ───────────────────────────────────────────
    # Per klas, per vervoersmiddel: één rij met het aantal en het percentage.
    # Het percentage toont hoe groot het aandeel van dat vervoer is binnen de klas.
    tabel_b_rijen = []
    for rij in data:
        totaal_verplaatsingen = sum(rij["vervoer"].values()) or 1  # voorkom deling door nul
        for vervoer_type, aantal in sorted(rij["vervoer"].items()):
            percentage = round(aantal / totaal_verplaatsingen * 100, 1)
            tabel_b_rijen.append((rij["klas"], vervoer_type, aantal, f"{percentage}%"))

    # ── Stap 3: Tabel A – klas-samenvatting ──────────────────────────────────
    frame_a = maak_kader(tab, titel="Aantal studenten & gemiddelde afstand per klas", header_kleur=blauw)
    frame_a.pack_configure(side="left", padx=(20, 10), pady=20, anchor="nw")

    kolommen_a = list(_KLAS_KOLOMMEN.keys())
    tabel_a = maak_tabel(frame_a, kolommen=kolommen_a, data=tabel_a_rijen)
    for kol, breedte in _KLAS_KOLOMMEN.items():
        tabel_a.column(kol, width=breedte, anchor="center")

    # ── Stap 4: Tabel B – vervoersverdeling per klas ──────────────────────────
    frame_b = maak_kader(tab, titel="Verdeling vervoersmiddelen per klas", header_kleur=blauw)
    frame_b.pack_configure(side="left", padx=(10, 20), pady=20, anchor="nw")

    kolommen_b = list(_VERVOER_KOLOMMEN.keys())
    tabel_b = maak_tabel(frame_b, kolommen=kolommen_b, data=tabel_b_rijen)
    for kol, breedte in _VERVOER_KOLOMMEN.items():
        tabel_b.column(kol, width=breedte, anchor="center")


# ── Tab 2: Gebruik per vervoer ────────────────────────────────────────────────
#
# Toont: vervoersmiddel | aantal verplaatsingen | % van totaal
#
# ─────────────────────────────────────────────────────────────────────────────

# Kolombreedtes (pas hier aan om de weergave te wijzigen)
_VERVOER_GEBRUIK_KOLOMMEN = {
    "Vervoersmiddel":         150,
    "Aantal verplaatsingen":  160,
    "% van totaal":           100,
}


def _bouw_gebruik_per_vervoer(tab, controller):
    """
    Bouwt de inhoud van het 'Gebruik per vervoer'-tabblad.
    Toont hoeveel verplaatsingen er per transporttype geregistreerd zijn.
    """
    # Data ophalen: lijst van (transport_type, aantal)
    verdeling = controller.get_transport_verdeling()

    totaal = sum(v for _, v in verdeling) or 1  # voorkom deling door nul

    # Rijen opbouwen: type, aantal, percentage van totaal
    rijen = [
        (transport_type, aantal, f"{round(aantal / totaal * 100, 1)}%")
        for transport_type, aantal in verdeling
    ]

    frame = maak_kader(tab, titel="Verplaatsingen per vervoersmiddel", header_kleur=blauw)
    frame.pack_configure(side="left", padx=20, pady=20, anchor="nw")

    kolommen = list(_VERVOER_GEBRUIK_KOLOMMEN.keys())
    tabel = maak_tabel(frame, kolommen=kolommen, data=rijen)
    for kol, breedte in _VERVOER_GEBRUIK_KOLOMMEN.items():
        tabel.column(kol, width=breedte, anchor="center")


# ════════════════════════════════════════════════════════════════════════════
# ANALYSE_TABS: de volgorde en inhoud van de tabbladen.
#
# Wil je een tab toevoegen?  → voeg een tuple ("Naam", bouwfunctie) toe.
# Wil je een tab verwijderen? → verwijder de bijhorende tuple.
# Wil je volgorde aanpassen? → verplaats de tuples.
# ════════════════════════════════════════════════════════════════════════════
ANALYSE_TABS = [
    ("Overzicht per klas",  _bouw_overzicht_per_klas),
    ("Gebruik per vervoer", _bouw_gebruik_per_vervoer),
]
