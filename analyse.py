import tkinter as tk
from tkinter import ttk
from main_controller import Controller as ctrl

class AnalyseTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f6fa")
        self._build_ui()
        self.refresh() 

    def _build_ui(self):
        btn_bar = tk.Frame(self, bg="#dfe6e9")
        btn_bar.pack(fill="x", padx=0, pady=0)

        analyses = [  
            ("📊 Aantal per vervoer",        self._toon_aantal_per_vervoer),
            ("📏 Gemiddelde afstand",         self._toon_gem_afstand),
            ("🏫 Overzicht per klas",         self._toon_per_klas),
            ("⭐ Populairste vervoer/student", self._toon_populairste),
        ]
        for label, cmd in analyses:
            tk.Button(btn_bar, text=label, command=cmd,
                      bg="#2c3e50", fg="w hite", font=("Segoe UI", 9, "bold"),
                      relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=2, pady=4)

        # Resultatenframe
        self.result_frame = tk.LabelFrame(self, text="Resultaten",
                                          bg="#f5f6fa", font=("Segoe UI", 10, "bold"))
        self.result_frame.pack(fill="both", expand=True, padx=14, pady=8)

        self.tree = ttk.Treeview(self.result_frame, show="headings", height=22)
        sb = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    # ── Weergave-helpers ────────────────────────────────────────────────────

    def _reset_tree(self, kolommen: list[str]):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = kolommen
        for col in kolommen:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=max(120, len(col) * 12), anchor="center")

    # ── Analyses ────────────────────────────────────────────────────────────

    def _toon_aantal_per_vervoer(self):
        data = ctrl.analyse_aantal_per_vervoersmiddel()
        self._reset_tree(["Vervoersmiddel", "Aantal verplaatsingen"])
        for row in data:
            self.tree.insert("", "end", values=(row["transport"], row["aantal"]))

    def _toon_gem_afstand(self):
        data = ctrl.analyse_gemiddelde_afstand()
        self._reset_tree(["Categorie", "Gemiddelde afstand (km)"])
        self.tree.insert("", "end", values=("Alle studenten", data["gemiddeld_alle"]))
        for row in data["per_vervoersmiddel"]:
            self.tree.insert("", "end", values=(
                f"  └ {row['transport']}", row["gemiddelde"]))

    def _toon_per_klas(self):
        data = ctrl.analyse_overzicht_per_klas()
        self._reset_tree(["Klas", "Leerlingen", "Gem. afstand (km)", "Vervoersverdeling"])
        for row in data:
            verdeling = " | ".join(f"{k}: {v}" for k, v in sorted(row["transport"].items()))
            self.tree.insert("", "end", values=(
                row["klas"], row["aantal"], row["gem_afstand"], verdeling))

    def _toon_populairste(self):
        """Extra analyse: meest gebruikte vervoersmiddel per student."""
        data = ctrl.analyse_populairste_transport_per_student()
        self._reset_tree(["Student", "Klas", "Meest gebruikt vervoer", "Aantal ritten"])
        for row in data:
            self.tree.insert("", "end", values=(
                row["student"], row["klas"], row["transport"], row["aantal"]))

    def refresh(self):
        self._toon_aantal_per_vervoer()