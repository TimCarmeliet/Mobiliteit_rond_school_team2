"""
view/tab_logs.py
----------------
Tabblad voor het registreren en beheren van verplaatsingen (CRUD).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from main_controller import controller as ctrl


class LogsTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f6fa")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        form = tk.LabelFrame(self, text="Verplaatsing registreren / aanpassen",
                             bg="#f5f6fa", font=("Segoe UI", 10, "bold"), padx=10, pady=8)
        form.pack(fill="x", padx=14, pady=(12, 4))

        # Student dropdown
        tk.Label(form, text="Student", bg="#f5f6fa", font=("Segoe UI", 9)).grid(
            row=0, column=0, sticky="w", padx=(0, 4))
        self.student_var = tk.StringVar()
        self.student_cb = ttk.Combobox(form, textvariable=self.student_var, width=28,
                                       state="readonly", font=("Segoe UI", 9))
        self.student_cb.grid(row=0, column=1, padx=(0, 14))

        # Transport dropdown
        tk.Label(form, text="Vervoer", bg="#f5f6fa", font=("Segoe UI", 9)).grid(
            row=0, column=2, sticky="w", padx=(0, 4))
        self.transport_var = tk.StringVar()
        self.transport_cb = ttk.Combobox(form, textvariable=self.transport_var, width=16,
                                         state="readonly", font=("Segoe UI", 9))
        self.transport_cb.grid(row=0, column=3, padx=(0, 14))

        # Datum
        tk.Label(form, text="Datum (JJJJ-MM-DD)", bg="#f5f6fa", font=("Segoe UI", 9)).grid(
            row=0, column=4, sticky="w", padx=(0, 4))
        self.datum_entry = tk.Entry(form, width=14, font=("Segoe UI", 9))
        self.datum_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.datum_entry.grid(row=0, column=5)

        btn_frame = tk.Frame(form, bg="#f5f6fa")
        btn_frame.grid(row=1, column=0, columnspan=6, pady=(8, 2), sticky="w")

        self._btn(btn_frame, "➕ Registreren",  "#27ae60", self._registreren).pack(side="left", padx=(0, 6))
        self._btn(btn_frame, "✏️ Aanpassen",    "#2980b9", self._aanpassen).pack(side="left", padx=(0, 6))
        self._btn(btn_frame, "🗑️ Verwijderen",  "#e74c3c", self._verwijderen).pack(side="left", padx=(0, 6))
        self._btn(btn_frame, "🔄 Wissen",       "#95a5a6", self._wis_form).pack(side="left")

        # Tabel
        tbl_frame = tk.LabelFrame(self, text="Alle verplaatsingen",
                                  bg="#f5f6fa", font=("Segoe UI", 10, "bold"))
        tbl_frame.pack(fill="both", expand=True, padx=14, pady=8)

        cols = ("ID", "Student", "Klas", "Vervoer", "Datum")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=18)
        widths = {"ID": 45, "Student": 160, "Klas": 80, "Vervoer": 100, "Datum": 100}
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=widths[c], anchor="center")
        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        self._selected_id: int | None = None
        self._student_map: dict[str, int] = {}
        self._transport_map: dict[str, int] = {}

    @staticmethod
    def _btn(parent, text, color, cmd):
        return tk.Button(parent, text=text, bg=color, fg="white",
                         font=("Segoe UI", 9, "bold"), relief="flat",
                         padx=10, pady=4, cursor="hand2", command=cmd)

    def _laad_dropdowns(self):
        studenten = ctrl.haal_alle_studenten()
        self._student_map = {f"{s['naam']} ({s['klas']})": s["id"] for s in studenten}
        self.student_cb["values"] = list(self._student_map.keys())

        transporten = ctrl.haal_alle_transporten()
        self._transport_map = {t["type"]: t["id"] for t in transporten}
        self.transport_cb["values"] = list(self._transport_map.keys())

    def _wis_form(self):
        self.student_var.set("")
        self.transport_var.set("")
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self._selected_id = None

    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        self._selected_id = int(vals[0])
        # Vul form in
        student_label = next(
            (k for k, v in self._student_map.items() if f"{vals[1]} ({vals[2]})" in k), "")
        self.student_var.set(student_label)
        self.transport_var.set(vals[3])
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, vals[4])

    def _registreren(self):
        student_label = self.student_var.get()
        transport_label = self.transport_var.get()
        if not student_label or not transport_label:
            messagebox.showwarning("Invoer", "Selecteer een student en een vervoersmiddel.")
            return
        ok, msg = ctrl.registreer_verplaatsing(
            self._student_map[student_label],
            self._transport_map[transport_label],
            self.datum_entry.get()
        )
        if ok:
            messagebox.showinfo("Succes", "Verplaatsing geregistreerd!")
            self._wis_form()
            self.refresh()
        else:
            messagebox.showerror("Fout", msg)

    def _aanpassen(self):
        if self._selected_id is None:
            messagebox.showwarning("Selecteer", "Selecteer eerst een verplaatsing.")
            return
        student_label = self.student_var.get()
        transport_label = self.transport_var.get()
        if not student_label or not transport_label:
            messagebox.showwarning("Invoer", "Selecteer een student en vervoersmiddel.")
            return
        ok, msg = ctrl.pas_log_aan(
            self._selected_id,
            self._student_map[student_label],
            self._transport_map[transport_label],
            self.datum_entry.get()
        )
        if ok:
            messagebox.showinfo("Succes", "Verplaatsing aangepast!")
            self._wis_form()
            self.refresh()
        else:
            messagebox.showerror("Fout", msg)

    def _verwijderen(self):
        if self._selected_id is None:
            messagebox.showwarning("Selecteer", "Selecteer eerst een verplaatsing.")
            return
        if not messagebox.askyesno("Bevestig", "Verplaatsing verwijderen?"):
            return
        ctrl.verwijder_log(self._selected_id)
        messagebox.showinfo("Succes", "Verplaatsing verwijderd.")
        self._wis_form()
        self.refresh()

    def refresh(self):
        self._laad_dropdowns()
        self.tree.delete(*self.tree.get_children())
        for log in ctrl.haal_alle_logs():
            self.tree.insert("", "end", values=(
                log["id"], log["student"], log["klas"], log["transport"], log["datum"]
            ))
