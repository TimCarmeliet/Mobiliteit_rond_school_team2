
import tkinter as tk
from tkinter import ttk
from main_controller import Controller as ctrl
from model_sql import database as db

# ── CO₂ per km per vervoersmiddel (g/km) ────────────────────────────────────
CO2_FACTOR = {
    "Fiets":    0,
    "Bus":      50,
    "Auto":     120,
    "Te voet":  0,
}
ONBEKEND_FACTOR = 80  # default voor onbekende types


def _factor(transport_type: str) -> float:
    return CO2_FACTOR.get(transport_type, ONBEKEND_FACTOR)


def bereken_co2_data(filter_klas=None, filter_min_afstand=None, filter_transport=None) -> list:
    """
    Berekent CO₂ per verplaatsing door student-afstanden en transporttype te combineren.
    Geeft gefilterde lijst van dicts terug.
    Geen SQL JOINs – puur Python combinaties van enkelvoudige queries.
    """
    studenten   = {s["id"]: s for s in db.student_read_all()}
    transporten = {t["id"]: t["type"] for t in db.transport_read_all()}
    logs        = db.query_all_logs_with_date()

    resultaten = []
    for log in logs:
        s  = studenten.get(log["student_id"])
        if s is None:
            continue
        transport_type = transporten.get(log["transport_id"], "Onbekend")
        afstand        = s["afstand"]
        co2_gram       = round(_factor(transport_type) * afstand, 1)

        # Filters toepassen
        if filter_klas and s["klas"] != filter_klas:
            continue
        if filter_min_afstand and afstand < filter_min_afstand:
            continue
        if filter_transport and transport_type != filter_transport:
            continue

        resultaten.append({
            "log_id":    log["id"],
            "student":   s["naam"],
            "klas":      s["klas"],
            "transport": transport_type,
            "afstand":   afstand,
            "datum":     log["datum"],
            "co2_gram":  co2_gram,
        })

    return resultaten


# ════════════════════════════════════════════════════════════════════════════
#  VIEW
# ════════════════════════════════════════════════════════════════════════════

KLEUREN = ["#27ae60", "#3498db", "#e74c3c", "#f39c12", "#9b59b6"]


class Co2Tab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f6fa")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ── Filterrij ────────────────────────────────────────────────────────
        filter_frame = tk.LabelFrame(self, text="Filters",
                                     bg="#f5f6fa", font=("Segoe UI", 9, "bold"),
                                     padx=8, pady=6)
        filter_frame.pack(fill="x", padx=12, pady=(10, 4))

        # Klas-filter
        tk.Label(filter_frame, text="Klas:", bg="#f5f6fa",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        self.klas_var = tk.StringVar(value="Alle")
        self.klas_cb = ttk.Combobox(filter_frame, textvariable=self.klas_var,
                                    width=10, state="readonly")
        self.klas_cb.grid(row=0, column=1, padx=(4, 14))

        # Afstandsfilter
        tk.Label(filter_frame, text="Min. afstand:", bg="#f5f6fa",
                 font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w")
        self.afstand_var = tk.StringVar(value="Alle")
        ttk.Combobox(filter_frame, textvariable=self.afstand_var,
                     values=["Alle", "> 5 km", "> 10 km"],
                     width=10, state="readonly").grid(row=0, column=3, padx=(4, 14))

        # Transport-filter
        tk.Label(filter_frame, text="Vervoer:", bg="#f5f6fa",
                 font=("Segoe UI", 9)).grid(row=0, column=4, sticky="w")
        self.transport_var = tk.StringVar(value="Alle")
        self.transport_cb = ttk.Combobox(filter_frame, textvariable=self.transport_var,
                                         width=12, state="readonly")
        self.transport_cb.grid(row=0, column=5, padx=(4, 14))

        tk.Button(filter_frame, text="🔍 Filteren", command=self._filteren,
                  bg="#8e44ad", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=10, pady=3).grid(row=0, column=6)

        # ── Tabel ─────────────────────────────────────────────────────────────
        lf_tabel = tk.LabelFrame(self, text="CO₂-verbruik per verplaatsing",
                                 bg="#f5f6fa", font=("Segoe UI", 9, "bold"))
        lf_tabel.pack(fill="both", expand=True, padx=12, pady=4)

        cols = ("Student", "Klas", "Vervoer", "Afstand (km)", "Datum", "CO₂ (g)")
        self.tree = ttk.Treeview(lf_tabel, columns=cols, show="headings", height=14)
        widths = {"Student": 140, "Klas": 70, "Vervoer": 90,
                  "Afstand (km)": 90, "Datum": 90, "CO₂ (g)": 80}
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=widths[c], anchor="center")
        sb = ttk.Scrollbar(lf_tabel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # ── Grafiek: totaal CO₂ per vervoersmiddel ────────────────────────────
        lf_grafiek = tk.LabelFrame(self, text="Totaal CO₂ per vervoersmiddel (g)",
                                   bg="#f5f6fa", font=("Segoe UI", 9, "bold"))
        lf_grafiek.pack(fill="x", padx=12, pady=(4, 10))
        self.canvas_co2 = tk.Canvas(lf_grafiek, bg="white", height=180)
        self.canvas_co2.pack(fill="x", padx=4, pady=4)

    # ── Refresh / filter ──────────────────────────────────────────────────────

    def _laad_filter_opties(self):
        klassen    = sorted({s["klas"] for s in ctrl.haal_alle_studenten()})
        transporten = [t["type"] for t in ctrl.haal_alle_transporten()]
        self.klas_cb["values"]      = ["Alle"] + klassen
        self.transport_cb["values"] = ["Alle"] + transporten

    def _filteren(self):
        klas      = self.klas_var.get() if self.klas_var.get() != "Alle" else None
        afstand_s = self.afstand_var.get()
        min_afstand = None
        if afstand_s == "> 5 km":
            min_afstand = 5.0
        elif afstand_s == "> 10 km":
            min_afstand = 10.0
        transport = self.transport_var.get() if self.transport_var.get() != "Alle" else None
        self._vul_tabel(klas, min_afstand, transport)

    def _vul_tabel(self, klas=None, min_afstand=None, transport=None):
        data = bereken_co2_data(klas, min_afstand, transport)

        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=(
                row["student"], row["klas"], row["transport"],
                row["afstand"], row["datum"], row["co2_gram"]
            ))

        # Totaal CO₂ per vervoersmiddel voor grafiek
        totalen: dict[str, float] = {}
        for row in data:
            totalen[row["transport"]] = totalen.get(row["transport"], 0) + row["co2_gram"]

        self._teken_co2_grafiek(totalen)

    def _teken_co2_grafiek(self, totalen: dict):
        canvas = self.canvas_co2
        canvas.delete("all")
        canvas.update_idletasks()
        breedte = canvas.winfo_width() or 700
        hoogte  = 180
        marge_l, marge_r, marge_b, marge_t = 70, 20, 40, 30

        items = sorted(totalen.items())
        if not items:
            canvas.create_text(breedte // 2, hoogte // 2,
                               text="Geen data", font=("Segoe UI", 10))
            return

        max_val = max(v for _, v in items) or 1
        stap    = (breedte - marge_l - marge_r) / len(items)
        balk_b  = max(20, stap - 16)
        grafiek_h = hoogte - marge_t - marge_b

        canvas.create_text(breedte // 2, 14,
                           text="Totale CO₂-uitstoot (g) per vervoersmiddel",
                           font=("Segoe UI", 9, "bold"), fill="#2c3e50")

        for i, (label, val) in enumerate(items):
            x_mid = marge_l + stap * i + stap / 2
            hoogte_balk = grafiek_h * val / max_val
            x1, x2 = x_mid - balk_b / 2, x_mid + balk_b / 2
            y1, y2 = hoogte - marge_b - hoogte_balk, hoogte - marge_b
            kleur = KLEUREN[i % len(KLEUREN)]
            canvas.create_rectangle(x1, y1, x2, y2, fill=kleur, outline="white")
            canvas.create_text(x_mid, y1 - 10,
                               text=f"{val:.0f}g", font=("Segoe UI", 8, "bold"), fill="#2c3e50")
            canvas.create_text(x_mid, hoogte - marge_b + 14,
                               text=label, font=("Segoe UI", 8), fill="#2c3e50")

    def refresh(self):
        self._laad_filter_opties()
        self._vul_tabel()

