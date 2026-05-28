import tkinter as tk
from tkinter import messagebox, ttk

from views.handy_view import Tooltip, maak_kader, maak_tabel
from views.student_view import toon_student
from views.verplaatsing_view import toon_verplaatsing
from views.dashboard_view import toon_dashboard


# kleur
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"


class mainView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Mobiliteit rond de school")

        self.topnav = tk.Frame(root, bg="#333", height=40)
        self.topnav.pack(side="top", fill="x")

        self.styleButton = {
            "bg": "#555",
            "fg": "white",
            "activebackground": "#777",
            "activeforeground": "white",
            "bd": 0,
            "padx": 20,
            "pady": 10,
        }

        tk.Button(self.topnav, text="student", command=self.student, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="vervoer", command=self.vervoer, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="dashboard", command=self.dashboard, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="verplaatsing", command=self.verplaatsing, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="analyse", command=self.analyse, **self.styleButton).pack(side="left")

        self.student_content = tk.Frame(self.root, bg=grijs)
        self.vervoer_content = tk.Frame(self.root, bg=grijs)
        self.dashboard_content = tk.Frame(self.root, bg=grijs)
        self.verplaatsing_content = tk.Frame(self.root, bg=grijs)
        self.analyse_content = tk.Frame(self.root, bg=grijs)

        self.student()

    def clear_content(self):
        self.student_content.forget()
        self.vervoer_content.forget()
        self.dashboard_content.forget()
        self.verplaatsing_content.forget()
        self.analyse_content.forget()

    def _label_stijl(self):
        return {
            "bg": "white",
            "fg": donker_grijs,
            "font": ("Arial", 10, "bold"),
            "anchor": "w",
        }

    def _input_stijl(self):
        return {
            "width": 30,
            "font": ("Arial", 10),
            "relief": "solid",
            "bd": 1,
            "highlightthickness": 1,
            "highlightbackground": "#d0d7de",
            "highlightcolor": blauw,
            "insertbackground": donker_grijs,
        }

    def _knop_stijl(self):
        return {
            "fg": "white",
            "activeforeground": "white",
            "disabledforeground": "white",
            "bd": 0,
            "padx": 12,
            "pady": 8,
            "font": ("Arial", 9, "bold"),
            "cursor": "hand2",
        }

    def _toon_melding(self, titel, melding):
        if melding and melding.startswith("ERROR"):
            messagebox.showwarning(titel, melding.replace("ERROR: ", ""))
            return False
        return True

    def student(self):
        toon_student(self, Tooltip)

    def vervoer(self):
        self.clear_content()
        self.vervoer_content = tk.Frame(self.root, bg=grijs)
        self.vervoer_content.pack(fill="both", expand=True)

        data = self.controller.get_transport()
        geselecteerde_transport_id = tk.StringVar()

        frame = maak_kader(
            self.vervoer_content,
            titel="Vervoer bewerken",
            verticalSpace=20,
            horizontalSpace=20,
            header_kleur=blauw,
        )
        frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

        form = tk.Frame(frame, bg="white", padx=18, pady=16)
        form.pack(fill="x")

        tk.Label(form, text="Transporttype", **self._label_stijl()).grid(row=0, column=0, sticky="w")
        transportTypeInput = tk.Entry(form, **self._input_stijl())
        transportTypeInput.grid(row=1, column=0, sticky="ew", pady=(3, 14))
        form.columnconfigure(0, weight=1)

        knoppen = tk.Frame(form, bg="white")
        knoppen.grid(row=2, column=0, sticky="ew")

        def vervoer_leegmaken():
            geselecteerde_transport_id.set("")
            transportTypeInput.delete(0, "end")
            tabel.selection_remove(tabel.selection())
            update_vervoer_knoppen()

        def vervoer_toevoegen():
            melding = self.controller.add_transport(transportTypeInput.get().strip())
            if not self._toon_melding("Vervoer", melding):
                return
            self.vervoer()

        def vervoer_aanpassen():
            if not geselecteerde_transport_id.get():
                messagebox.showwarning("Vervoer", "Selecteer eerst een transporttype uit de tabel.")
                return

            melding = self.controller.update_transport(
                geselecteerde_transport_id.get(),
                transportTypeInput.get().strip(),
            )
            if not self._toon_melding("Vervoer", melding):
                return
            self.vervoer()

        def vervoer_verwijderen():
            if not geselecteerde_transport_id.get():
                messagebox.showwarning("Vervoer", "Selecteer eerst een transporttype uit de tabel.")
                return

            melding = self.controller.delete_transport(geselecteerde_transport_id.get())
            if not self._toon_melding("Vervoer", melding):
                return
            self.vervoer()

        tk.Button(
            knoppen,
            text="Toevoegen",
            command=vervoer_toevoegen,
            bg=blauw,
            activebackground=blauw,
            **self._knop_stijl(),
        ).pack(side="left", padx=(0, 10))
        aanpassen_knop = tk.Button(knoppen, text="Aanpassen", command=vervoer_aanpassen, **self._knop_stijl())
        aanpassen_knop.pack(side="left", padx=(0, 10))
        verwijderen_knop = tk.Button(knoppen, text="Verwijderen", command=vervoer_verwijderen, **self._knop_stijl())
        verwijderen_knop.pack(side="left")

        aanpassen_tooltip = Tooltip(aanpassen_knop, "Klik eerst op een transporttype in het overzicht om te kunnen aanpassen.")
        verwijderen_tooltip = Tooltip(verwijderen_knop, "Klik eerst op een transporttype in het overzicht om te kunnen verwijderen.")

        def update_vervoer_knoppen():
            heeft_selectie = bool(geselecteerde_transport_id.get())
            if heeft_selectie:
                aanpassen_knop.config(bg=groen, activebackground=groen, cursor="hand2")
                verwijderen_knop.config(bg=rood, activebackground=rood, cursor="hand2")
                aanpassen_tooltip.set_actief(False)
                verwijderen_tooltip.set_actief(False)
            else:
                aanpassen_knop.config(bg=licht_grijs, activebackground=licht_grijs, cursor="hand2")
                verwijderen_knop.config(bg=licht_grijs, activebackground=licht_grijs, cursor="hand2")
                aanpassen_tooltip.set_actief(True)
                verwijderen_tooltip.set_actief(True)

        update_vervoer_knoppen()

        tk.Button(
            form,
            text="Leegmaken",
            command=vervoer_leegmaken,
            bg="#e7e7e7",
            fg=donker_grijs,
            activebackground=licht_grijs,
            bd=0,
            padx=10,
            pady=7,
            cursor="hand2",
        ).grid(row=3, column=0, sticky="ew", pady=(12, 0))

        frame2 = maak_kader(self.vervoer_content, titel=f"Overzicht vervoer ({len(data)})", header_kleur=blauw)
        frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

        tabel = maak_tabel(frame2, kolommen=["ID", "Type"], data=data)
        tabel.column("ID", width=60, anchor="center")
        tabel.column("Type", width=220)

        def on_select(event):
            geselecteerd = tabel.selection()
            if geselecteerd:
                rij = tabel.item(geselecteerd[0])["values"]
                geselecteerde_transport_id.set(rij[0])
                transportTypeInput.delete(0, "end")
                transportTypeInput.insert(0, rij[1])
            else:
                geselecteerde_transport_id.set("")
            update_vervoer_knoppen()

        tabel.bind("<<TreeviewSelect>>", on_select)

    def dashboard(self):
        toon_dashboard(self)

    def verplaatsing(self):
        toon_verplaatsing(self)

    def analyse(self):
        self.clear_content()
        self.analyse_content = tk.Frame(self.root, bg=grijs)
        self.analyse_content.pack(fill="both", expand=True)

        analyse_data = self.controller.get_analysis()
        transporten = self.controller.get_transport()
        transport_namen = {transport[0]: transport[1] for transport in transporten}

        tabel_data = [
            (transport_namen.get(transport_id, "Onbekend"), aantal)
            for transport_id, aantal in analyse_data["transport"]
        ]

        frame = maak_kader(
            self.analyse_content,
            titel="Gebruik per vervoertype",
            verticalSpace=20,
            horizontalSpace=20,
            header_kleur=blauw,
        )
        frame.pack_configure(side="left", padx=(20, 10), pady=20, fill="both", expand=True, anchor="nw")

        tabel = maak_tabel(
            frame,
            kolommen=["Vervoer", "Aantal verplaatsingen"],
            data=tabel_data,
        )
        tabel.column("Vervoer", width=220, anchor="w")
        tabel.column("Aantal verplaatsingen", width=150, anchor="center")
