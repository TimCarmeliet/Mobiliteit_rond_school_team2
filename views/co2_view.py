import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.handy_view import maak_kader, maak_tabel

# ── CONFIGURATIE (Makkelijk aanpasbaar) ──────────────────────────────────────
CO2_FACTOR = {
    "fiets": 0,
    "bus": 50,
    "auto": 120,
    "te voet": 0
}
DEFAULT_FACTOR = 80  # voor onbekende types

KLEUREN = ["#2f7d32", "#185FA5", "#b3261e", "#f0a500", "#9b59b6"]
blauw = "#185FA5"
grijs = "#eee"
donker_grijs = "#333333"


def bereken_co2_data(controller, filter_klas="Alle", filter_afstand="Alle", filter_transport="Alle"):
    """
    Berekent de CO2-uitstoot per verplaatsing en past de filters toe.
    Er worden GEEN SQL JOINs gebruikt, alle matching gebeurt in Python.
    """
    raw_data = controller.get_co2_data()
    resultaten = []

    for row in raw_data:
        afstand = row["afstand"]
        klas = row["klas"]
        transport = row["transport"]

        # 1. Klas filteren
        if filter_klas != "Alle" and klas != filter_klas:
            continue

        # 2. Afstand filteren
        if filter_afstand == "> 5 km" and afstand <= 5.0:
            continue
        if filter_afstand == "> 10 km" and afstand <= 10.0:
            continue

        # 3. Vervoer filteren
        if filter_transport != "Alle" and transport.lower() != filter_transport.lower():
            continue

        # CO2 berekenen: afstand (km) * factor (g/km)
        factor = CO2_FACTOR.get(transport.lower(), DEFAULT_FACTOR)
        co2_gram = round(afstand * factor, 1)

        resultaten.append({
            "student": row["student"],
            "klas": klas,
            "transport": transport,
            "afstand": afstand,
            "datum": row["datum"],
            "co2_gram": co2_gram
        })

    return resultaten


def toon_co2_dashboard(view, parent):
    """
    Bouwt het CO2-analyse tabblad op.
    Boven: filters voor klas, afstand en vervoer.
    Onder links: tabel met de ritten en de berekende CO2-uitstoot.
    Onder rechts: balkdiagram met de totale CO2-uitstoot per vervoersmiddel.
    """
    # Hoofdcontainer voor het tabblad
    main_frame = tk.Frame(parent, bg=grijs)
    main_frame.pack(fill="both", expand=True)

    # ── BOVEN: Filterbalk ────────────────────────────────────────────────────
    filter_frame = tk.LabelFrame(
        main_frame,
        text="Filters",
        bg="white",
        fg=donker_grijs,
        font=("Arial", 9, "bold"),
        padx=10,
        pady=8
    )
    filter_frame.pack(fill="x", padx=20, pady=(15, 5))

    # 1. Klas dropdown
    tk.Label(filter_frame, text="Klas:", bg="white", font=("Arial", 9, "bold"), fg=donker_grijs).grid(row=0, column=0, padx=(5, 5), sticky="w")
    klas_var = tk.StringVar(value="Alle")
    klas_cb = ttk.Combobox(filter_frame, textvariable=klas_var, state="readonly", width=12)
    klas_cb.grid(row=0, column=1, padx=(0, 15))

    # Dynamisch klassen ophalen
    students = view.controller.get_students()
    klassen = sorted({s[2] for s in students})
    klas_cb["values"] = ["Alle"] + klassen

    # 2. Afstand dropdown
    tk.Label(filter_frame, text="Afstand:", bg="white", font=("Arial", 9, "bold"), fg=donker_grijs).grid(row=0, column=2, padx=(5, 5), sticky="w")
    afstand_var = tk.StringVar(value="Alle")
    afstand_cb = ttk.Combobox(filter_frame, textvariable=afstand_var, values=["Alle", "> 5 km", "> 10 km"], state="readonly", width=12)
    afstand_cb.grid(row=0, column=3, padx=(0, 15))

    # 3. Vervoer dropdown
    tk.Label(filter_frame, text="Vervoer:", bg="white", font=("Arial", 9, "bold"), fg=donker_grijs).grid(row=0, column=4, padx=(5, 5), sticky="w")
    transport_var = tk.StringVar(value="Alle")
    transport_cb = ttk.Combobox(filter_frame, textvariable=transport_var, state="readonly", width=15)
    transport_cb.grid(row=0, column=5, padx=(0, 15))

    # Dynamisch transporttypes ophalen
    transports = view.controller.get_transport()
    transport_typen = [t[1] for t in transports]
    transport_cb["values"] = ["Alle"] + transport_typen

    # ── ONDERSTE DEEL: Tabel (links) en Grafiek (rechts) ─────────────────────
    data_frame = tk.Frame(main_frame, bg=grijs)
    data_frame.pack(fill="both", expand=True)

    # Links: Tabel-kader
    tabel_kader = maak_kader(data_frame, titel="CO₂-uitstoot per verplaatsing", header_kleur=blauw)
    tabel_kader.pack_configure(side="left", padx=20, pady=10, fill="both", expand=True)

    tabel_container = tk.Frame(tabel_kader, bg="white")
    tabel_container.pack(fill="both", expand=True, padx=5, pady=5)

    # Rechts: Grafiek-kader
    grafiek_kader = maak_kader(data_frame, titel="Totale CO₂ per vervoersmiddel", header_kleur=blauw)
    grafiek_kader.pack_configure(side="left", padx=(0, 20), pady=10, fill="both", expand=True)

    grafiek_container = tk.Frame(grafiek_kader, bg="white")
    grafiek_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Globale variabele om de huidige tabel-instantie bij te houden voor hertekenen
    huidige_tabel = [None]

    def update_analyse():
        # Verwijder oude grafiek
        for widget in grafiek_container.winfo_children():
            widget.destroy()

        # Data berekenen op basis van gekozen filters
        gefilterde_data = bereken_co2_data(
            view.controller,
            filter_klas=klas_var.get(),
            filter_afstand=afstand_var.get(),
            filter_transport=transport_var.get()
        )


        # 1. Tabel vullen
        tabel_rijen = [
            (r["student"], r["klas"], r["transport"], f"{r['afstand']:.1f} km", r["datum"], f"{r['co2_gram']:.1f} g")
            for r in gefilterde_data
        ]

        # Als er al een tabel staat, vernietig die dan eerst
        if huidige_tabel[0] is not None:
            huidige_tabel[0].destroy()

        # Maak nieuwe tabel aan
        kolommen = ["Student", "Klas", "Vervoer", "Afstand", "Datum", "CO₂"]
        tabel = maak_tabel(tabel_container, kolommen=kolommen, data=tabel_rijen)
        tabel.column("Student", width=120)
        tabel.column("Klas", width=60, anchor="center")
        tabel.column("Vervoer", width=80, anchor="center")
        tabel.column("Afstand", width=80, anchor="center")
        tabel.column("Datum", width=95, anchor="center")
        tabel.column("CO₂", width=80, anchor="center")
        huidige_tabel[0] = tabel

        # 2. Grafiek tekenen
        co2_per_type = {}
        for r in gefilterde_data:
            t = r["transport"]
            co2_per_type[t] = co2_per_type.get(t, 0.0) + r["co2_gram"]

        if not co2_per_type:
            tk.Label(
                grafiek_container,
                text="Geen data beschikbaar voor deze filters.",
                bg="white",
                font=("Arial", 11),
                fg=donker_grijs
            ).pack(pady=40)
            return

        labels = sorted(co2_per_type.keys())
        waarden = [co2_per_type[l] for l in labels]

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("white")

        balken = ax.bar(labels, waarden, color=KLEUREN[:len(labels)])

        # Waarden op de balken schrijven
        for balk in balken:
            hoogte = balk.get_height()
            ax.text(
                balk.get_x() + balk.get_width() / 2,
                hoogte + 0.5,
                f"{hoogte:.0f} g",
                ha="center", va="bottom", fontsize=9, fontweight="bold", color=donker_grijs
            )

        ax.set_title("Totale CO₂-uitstoot (gram)", fontsize=11, fontweight="bold")
        ax.set_xlabel("Vervoersmiddel", fontsize=9)
        ax.set_ylabel("CO₂-uitstoot (g)", fontsize=9)
        ax.set_ylim(0, max(waarden) + max(waarden) * 0.15 + 5)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=grafiek_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Koppel dropdown selectie direct aan het updaten van de analyse
    klas_cb.bind("<<ComboboxSelected>>", lambda e: update_analyse())
    afstand_cb.bind("<<ComboboxSelected>>", lambda e: update_analyse())
    transport_cb.bind("<<ComboboxSelected>>", lambda e: update_analyse())

    # Eerste keer laden
    update_analyse()
