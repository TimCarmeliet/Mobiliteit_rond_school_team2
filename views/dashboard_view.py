
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.handy_view import maak_kader, maak_tabel




# kleuren
blauw = "#185FA5"
grijs = "#eee"

# ── GRAFIEK INSTELLINGEN - makkelijk aanpasbaar 
# Verander GRAFIEK_TYPE naar "balk" of "taart" om de grafiek te wisselen
GRAFIEK_TYPE = "balk"

# kleuren per vervoersmiddel (wordt gebruikt in beide grafiektypes)
GRAFIEK_KLEUREN = ["#185FA5", "#2f7d32", "#b3261e", "#f0a500"]

# grootte van de grafiek (breedte, hoogte in inches)
GRAFIEK_GROOTTE = (5, 4)



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

    # ──  Vervoersmiddelen (bestaande functionaliteit) 
    tab_vervoer = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_vervoer, text="Vervoersmiddelen")
    _toon_vervoer_tab(view, tab_vervoer)

    # ──  Overzicht per klas ──
    tab_klas = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_klas, text="Overzicht per klas")
    _toon_klas_dashboard(view, tab_klas)

    # ──Afstand analyse ─
    tab_afstand = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_afstand, text="Afstand analyse")
    _toon_afstand_dashboard(view, tab_afstand)



    # ── Grafiek per leerling ─
    tab_leerling = tk.Frame(notebook, bg=grijs)
    notebook.add(tab_leerling, text="Grafiek per leerling")
    _toon_leerling_dashboard(view, tab_leerling)




# ── Tab 1: Vervoersmiddelen ───────────────────────────────────────────────────

def _toon_vervoer_tab(view, parent):
    """
    Toont de grafiek en tabel voor de verdeling van vervoersmiddelen.
    Dit is de originele dashboardinhoud, nu in een tabblad geplaatst.
    'parent' is het tabblad-frame waarin alles wordt opgebouwd.
    """
    # Verdelingsdata ophalen via de controller
    verdeling = view.controller.get_transport_verdeling()
    labels = [rij[0] for rij in verdeling]
    waarden = [rij[1] for rij in verdeling]
    totaal = sum(waarden)

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





# ── Tab 3: Afstand analyse ───────────────────────────────────────────────────

def _toon_afstand_dashboard(view, parent):
    """
    Toont de gemiddelde afstandsanalyse.
    Links: tabel met gemiddelde afstand per vervoersmiddel + algemeen gemiddelde.
    Rechts: balkdiagram met gemiddelde afstand per vervoersmiddel en een referentielijn.
    """
    # ── CONFIGURATIE (Makkelijk aanpasbaar) ──────────────────────────────────
    TITEL_TABEL = "Gemiddelde afstand per vervoer"
    TITEL_GRAFIEK = "Gemiddelde afstand tot school"
    LABEL_X = "Vervoersmiddel"
    LABEL_Y = "Afstand (km)"
    REFERENTIE_LIJN_KLEUR = "#d63031"  # Rood voor de stippellijn
    REFERENTIE_LIJN_STIJL = "--"

    # Kleuren per vervoerstype (of fallback als het type niet bestaat)
    KLEUR_MAP = {
        "fiets":   "#185FA5",
        "bus":     "#2f7d32",
        "auto":    "#b3261e",
        "te voet": "#f0a500"
    }
    FALLBACK_KLEUREN = ["#9b59b6", "#1abc9c", "#e67e22", "#2ecc71"]
    # ─────────────────────────────────────────────────────────────────────────

    donker_grijs = "#333333"

    # Gegevens ophalen via de controller
    overall_avg = view.controller.get_avg_distance_overall()
    per_transport = view.controller.get_avg_distance_per_transport()

    # ── LINKS: Informatie en Tabel ───────────────────────────────────────────
    linker_frame = tk.Frame(parent, bg=grijs)
    linker_frame.pack(side="left", fill="y", padx=20, pady=20)

    # Kader voor de tabel
    frame_tabel = maak_kader(linker_frame, titel=TITEL_TABEL, header_kleur=blauw)
    frame_tabel.pack(anchor="nw", fill="x")

    # Boven de tabel tonen we de algemene gemiddelde afstand in een opvallend label
    info_frame = tk.Frame(frame_tabel, bg="white", padx=10, pady=10)
    info_frame.pack(fill="x", before=None)

    lbl_titel = tk.Label(
        info_frame,
        text="Algemeen gemiddelde (alle studenten):",
        font=("Arial", 10, "bold"),
        bg="white",
        fg=donker_grijs
    )
    lbl_titel.pack(anchor="w")

    lbl_waarde = tk.Label(
        info_frame,
        text=f"{overall_avg:.2f} km",
        font=("Arial", 16, "bold"),
        bg="white",
        fg=blauw
    )
    lbl_waarde.pack(anchor="w", pady=(2, 10))

    # Tabeldata opbouwen
    tabel_rijen = [
        (t_type.capitalize(), f"{avg:.2f} km")
        for t_type, avg in per_transport
    ]

    tabel = maak_tabel(
        frame_tabel,
        kolommen=["Vervoersmiddel", "Gem. afstand"],
        data=tabel_rijen
    )
    tabel.column("Vervoersmiddel", width=150, anchor="w")
    tabel.column("Gem. afstand", width=120, anchor="center")

    # ── RECHTS: Grafiek (staafdiagram) ───────────────────────────────────────
    rechter_frame = tk.Frame(parent, bg=grijs)
    rechter_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)

    frame_grafiek = maak_kader(rechter_frame, titel=TITEL_GRAFIEK, header_kleur=blauw)
    frame_grafiek.pack(fill="both", expand=True)

    grafiek_frame = tk.Frame(frame_grafiek, bg="white")
    grafiek_frame.pack(fill="both", expand=True, padx=10, pady=10)

    if not per_transport:
        tk.Label(
            grafiek_frame,
            text="Geen data beschikbaar.",
            bg="white",
            font=("Arial", 11),
            fg=donker_grijs
        ).pack(pady=40)
    else:
        labels = [t_type.capitalize() for t_type, _ in per_transport]
        waarden = [avg for _, avg in per_transport]

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("white")

        # Kleuren toewijzen op basis van vervoersmiddel
        balk_kleuren = [
            KLEUR_MAP.get(t_type.lower(), FALLBACK_KLEUREN[i % len(FALLBACK_KLEUREN)])
            for i, (t_type, _) in enumerate(per_transport)
        ]

        balken = ax.bar(labels, waarden, color=balk_kleuren)

        # Waarde boven elke balk tonen
        for balk in balken:
            hoogte = balk.get_height()
            ax.text(
                balk.get_x() + balk.get_width() / 2,
                hoogte + 0.1,
                f"{hoogte:.2f} km",
                ha="center", va="bottom", fontsize=9, fontweight="bold", color=donker_grijs
            )

        # Horizontale referentielijn toevoegen voor de algemene gemiddelde afstand
        ax.axhline(
            overall_avg,
            color=REFERENTIE_LIJN_KLEUR,
            linestyle=REFERENTIE_LIJN_STIJL,
            linewidth=1.5,
            label=f"Algemeen gem. ({overall_avg:.2f} km)"
        )

        ax.set_title("Gemiddelde afstand tot school per vervoersmiddel", fontsize=11, fontweight="bold")
        ax.set_xlabel(LABEL_X, fontsize=9)
        ax.set_ylabel(LABEL_Y, fontsize=9)
        ax.set_ylim(0, max(max(waarden) + 1.5, overall_avg + 1.5))
        ax.legend(loc="upper right")
        fig.tight_layout()

        # Grafiek inbedden in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=grafiek_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def _toon_leerling_dashboard(view, parent):
    """
    Toont een grafiek per geselecteerde leerling.
    Bevat:
      - Dropdown voor leerlingselectie
      - Dropdown voor grafiektype (Cirkeldiagram / Balkdiagram)
      - Matplotlib grafiek die de verdeling van vervoersmiddelen toont.
    """
    donker_grijs = "#333333"

    main_frame = tk.Frame(parent, bg=grijs)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Boven: Selectie-frame
    selectie_frame = tk.LabelFrame(
        main_frame,
        text="Opties",
        bg="white",
        fg=donker_grijs,
        font=("Arial", 9, "bold"),
        padx=10,
        pady=8
    )
    selectie_frame.pack(fill="x", pady=(0, 15))

    # Leerling dropdown
    tk.Label(selectie_frame, text="Leerling:", bg="white", font=("Arial", 9, "bold"), fg=donker_grijs).grid(row=0, column=0, padx=(5, 5), sticky="w")
    
    students = view.controller.get_students()  # lijst van (id, naam, klas, afstand)
    student_namen = sorted([s[1] for s in students])
    
    leerling_var = tk.StringVar()
    leerling_cb = ttk.Combobox(selectie_frame, textvariable=leerling_var, values=student_namen, state="readonly", width=30)
    leerling_cb.grid(row=0, column=1, padx=(0, 20))
    if student_namen:
        leerling_cb.set(student_namen[0])

    # Grafiektype dropdown
    tk.Label(selectie_frame, text="Grafiektype:", bg="white", font=("Arial", 9, "bold"), fg=donker_grijs).grid(row=0, column=2, padx=(5, 5), sticky="w")
    type_var = tk.StringVar(value="Cirkeldiagram")
    type_cb = ttk.Combobox(selectie_frame, textvariable=type_var, values=["Cirkeldiagram", "Balkdiagram"], state="readonly", width=15)
    type_cb.grid(row=0, column=3, padx=(0, 20))

    # Grafiek container
    grafiek_kader = maak_kader(main_frame, titel="Vervoersverdeling leerling", header_kleur=blauw)
    grafiek_kader.pack(fill="both", expand=True)
    
    grafiek_container = tk.Frame(grafiek_kader, bg="white")
    grafiek_container.pack(fill="both", expand=True, padx=10, pady=10)

    def update_grafiek(*args):
        # Oude widgets verwijderen
        for widget in grafiek_container.winfo_children():
            widget.destroy()

        naam = leerling_var.get()
        if not naam:
            return

        # Vervoersdata van de geselecteerde leerling tellen
        logs = view.controller.get_mobility_overview() # (id, naam, type, datum)
        verplaatsingen = [log[2] for log in logs if log[1] == naam]

        if not verplaatsingen:
            tk.Label(
                grafiek_container,
                text=f"Geen verplaatsingsgegevens gevonden voor {naam}.",
                bg="white",
                font=("Arial", 11),
                fg=donker_grijs
            ).pack(pady=40)
            return

        # Telling
        telling = {}
        for v in verplaatsingen:
            telling[v] = telling.get(v, 0) + 1

        labels = sorted(telling.keys())
        waarden = [telling[l] for l in labels]

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("white")

        grafiek_type = type_var.get()
        kleuren = ["#185FA5", "#2f7d32", "#b3261e", "#f0a500", "#9b59b6"]

        if grafiek_type == "Balkdiagram":
            balken = ax.bar(labels, waarden, color=kleuren[:len(labels)])
            # Waarde boven elke balk tonen
            for balk in balken:
                hoogte = balk.get_height()
                ax.text(
                    balk.get_x() + balk.get_width() / 2,
                    hoogte + 0.1,
                    str(int(hoogte)),
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color=donker_grijs
                )
            ax.set_xlabel("Vervoersmiddel", fontsize=9)
            ax.set_ylabel("Aantal verplaatsingen", fontsize=9)
            ax.set_ylim(0, max(waarden) + max(waarden)*0.15 + 1)
        else:  # Cirkeldiagram / Taartdiagram
            ax.pie(
                waarden,
                labels=labels,
                colors=kleuren[:len(labels)],
                autopct="%1.1f%%",
                startangle=90,
                textprops={'fontsize': 10, 'color': donker_grijs}
            )
            ax.axis("equal")

        ax.set_title(f"Vervoerskeuze van {naam}", fontsize=12, fontweight="bold", pad=15)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=grafiek_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Binden aan dropdown selecties
    leerling_cb.bind("<<ComboboxSelected>>", update_grafiek)
    type_cb.bind("<<ComboboxSelected>>", update_grafiek)

    # Initieel inladen
    update_grafiek()

