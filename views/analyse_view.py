import tkinter as tk
from views.handy_view import maak_kader, maak_tabel


# kleuren
blauw = "#185FA5"
grijs = "#eee"

# ── Hoofdfunctie (aangeroepen vanuit main_view.py) ────────────────────────────

def toon_analyse(view):
    """
    Bouwt het volledige analysescherm op met een ttk.Notebook.
    Elk tabblad roept zijn eigen bouwfunctie aan.
    """
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

    # ── frame rechts: gemiddelde afstand (tabel) ──
    frame2 = maak_kader(view.analyse_content, titel="Gemiddelde afstand tot school", header_kleur=blauw)
    frame2.pack_configure(side="left", padx=(0, 20), pady=20, fill="y", anchor="nw")

    gem_alle = round(analyse_data["avg_distance"], 2) if analyse_data["avg_distance"] else 0
    tabel2_data = [("Alle studenten", f"{gem_alle} km")]
    for transport_type, gemiddelde in analyse_data["avg_distance_per_transport"]:
        tabel2_data.append((transport_type, f"{gemiddelde} km"))

    tabel2 = maak_tabel(frame2, kolommen=["Categorie", "Gem. afstand"], data=tabel2_data)
    tabel2.column("Categorie", width=150, anchor="w")
    tabel2.column("Gem. afstand", width=120, anchor="center")

