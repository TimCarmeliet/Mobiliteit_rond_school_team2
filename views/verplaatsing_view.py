import tkinter as tk
from tkinter import messagebox, ttk
from views.handy_view import Tooltip, maak_kader, maak_tabel

# kleur
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
licht_grijs = "#d8d8d8"

def toon_verplaatsing(view):
        view.clear_content()
        view.verplaatsing_content = tk.Frame(view.root, bg=grijs)
        view.verplaatsing_content.pack(fill="both", expand=True)

        data = view.controller.get_mobility_overview()
        students = view.controller.get_students()
        transporten = view.controller.get_transport()
        geselecteerde_mobility_id = tk.StringVar()

        student_opties = [f"{student[1]} ({student[2]})" for student in students]
        transport_opties = [transport[1] for transport in transporten]
        student_id_per_optie = {
            f"{student[1]} ({student[2]})": student[0] for student in students
        }
        transport_id_per_optie = {transport[1]: transport[0] for transport in transporten}
        student_optie_per_id = {
            student[0]: f"{student[1]} ({student[2]})" for student in students
        }
        transport_optie_per_id = {transport[0]: transport[1] for transport in transporten}
        mobility_per_id = {
            mobility[0]: mobility for mobility in view.controller.get_mobility()
        }

        frame = maak_kader(
            view.verplaatsing_content,
            titel="Verplaatsing bewerken",
            verticalSpace=20,
            horizontalSpace=20,
            header_kleur=blauw,
        )
        frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

        form = tk.Frame(frame, bg="white", padx=18, pady=16)
        form.pack(fill="x")

        combobox_stijl = {"width": 30, "font": ("Arial", 10)}

        tk.Label(form, text="Student", **view._label_stijl()).grid(row=0, column=0, sticky="w")
        studentInput = ttk.Combobox(form, values=student_opties, state="readonly", **combobox_stijl)
        studentInput.grid(row=1, column=0, sticky="ew", pady=(3, 12))

        tk.Label(form, text="Vervoer", **view._label_stijl()).grid(row=2, column=0, sticky="w")
        transportInput = ttk.Combobox(form, values=transport_opties, state="readonly", **combobox_stijl)
        transportInput.grid(row=3, column=0, sticky="ew", pady=(3, 12))

        tk.Label(form, text="Datum (YYYY-MM-DD)", **view._label_stijl()).grid(row=4, column=0, sticky="w")
        datumInput = tk.Entry(form, **view._input_stijl())
        datumInput.grid(row=5, column=0, sticky="ew", pady=(3, 16))
        form.columnconfigure(0, weight=1)

        knoppen = tk.Frame(form, bg="white")
        knoppen.grid(row=6, column=0, sticky="ew")

        def input_waarden():
            student_id = student_id_per_optie.get(studentInput.get(), "")
            transport_id = transport_id_per_optie.get(transportInput.get(), "")
            datum = datumInput.get().strip()

            if not student_id or not transport_id or not datum:
                messagebox.showwarning("Verplaatsing", "Kies een student, kies vervoer en vul een datum in.")
                return None

            return student_id, transport_id, datum

        def verplaatsing_leegmaken():
            geselecteerde_mobility_id.set("")
            studentInput.set("")
            transportInput.set("")
            datumInput.delete(0, "end")
            tabel.selection_remove(tabel.selection())
            update_verplaatsing_knoppen()

        def verplaatsing_toevoegen():
            waarden = input_waarden()
            if waarden is None:
                return

            melding = view.controller.add_mobility(*waarden)
            if not view._toon_melding("Verplaatsing", melding):
                return
            view.verplaatsing()

        def verplaatsing_aanpassen():
            waarden = input_waarden()
            if waarden is None:
                return

            if not geselecteerde_mobility_id.get():
                messagebox.showwarning("Verplaatsing", "Selecteer eerst een verplaatsing uit de tabel.")
                return

            melding = view.controller.update_mobility(geselecteerde_mobility_id.get(), *waarden)
            if not view._toon_melding("Verplaatsing", melding):
                return
            view.verplaatsing()

        def verplaatsing_verwijderen():
            if not geselecteerde_mobility_id.get():
                messagebox.showwarning("Verplaatsing", "Selecteer eerst een verplaatsing uit de tabel.")
                return

            melding = view.controller.delete_mobility(geselecteerde_mobility_id.get())
            if not view._toon_melding("Verplaatsing", melding):
                return
            view.verplaatsing()

        tk.Button(
            knoppen,
            text="Toevoegen",
            command=verplaatsing_toevoegen,
            bg=blauw,
            activebackground=blauw,
            **view._knop_stijl(),
        ).pack(side="left", padx=(0, 10))
        aanpassen_knop = tk.Button(knoppen, text="Aanpassen", command=verplaatsing_aanpassen, **view._knop_stijl())
        aanpassen_knop.pack(side="left", padx=(0, 10))
        verwijderen_knop = tk.Button(knoppen, text="Verwijderen", command=verplaatsing_verwijderen, **view._knop_stijl())
        verwijderen_knop.pack(side="left")

        aanpassen_tooltip = Tooltip(aanpassen_knop, "Klik eerst op een verplaatsing in het overzicht om te kunnen aanpassen.")
        verwijderen_tooltip = Tooltip(verwijderen_knop, "Klik eerst op een verplaatsing in het overzicht om te kunnen verwijderen.")

        def update_verplaatsing_knoppen():
            heeft_selectie = bool(geselecteerde_mobility_id.get())
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

        update_verplaatsing_knoppen()

        tk.Button(
            form,
            text="Leegmaken",
            command=verplaatsing_leegmaken,
            bg="#e7e7e7",
            fg=donker_grijs,
            activebackground=licht_grijs,
            bd=0,
            padx=10,
            pady=7,
            cursor="hand2",
        ).grid(row=7, column=0, sticky="ew", pady=(12, 0))

        frame2 = maak_kader(view.verplaatsing_content, titel=f"Overzicht verplaatsingen ({len(data)})", header_kleur=blauw)
        frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

        # Zoekbalk voor verplaatsingen
        filter_bar = tk.Frame(frame2, bg="white", padx=10, pady=5)
        filter_bar.pack(fill="x", side="top", pady=(5, 0))

        tk.Label(filter_bar, text="Zoeken (naam):", bg="white", fg=donker_grijs, font=("Arial", 9, "bold")).pack(side="left", padx=(0, 5))
        zoek_var = tk.StringVar()
        zoek_entry = tk.Entry(filter_bar, textvariable=zoek_var, font=("Arial", 9), relief="solid", bd=1, width=20)
        zoek_entry.pack(side="left")

        tabel = maak_tabel(
            frame2,
            kolommen=["ID", "Student", "Vervoer", "Datum"],
            data=data,
        )
        tabel.column("ID", width=60, anchor="center")
        tabel.column("Student", width=100, anchor="center")
        tabel.column("Vervoer", width=100, anchor="center")
        tabel.column("Datum", width=130, anchor="center")

        def update_tabel(*args):
            zoek = zoek_var.get().strip().lower()
            tabel.delete(*tabel.get_children())
            
            gefilterde_data = data
            if zoek:
                gefilterde_data = [row for row in data if zoek in row[1].lower()]
                
            for i, row in enumerate(gefilterde_data):
                tag = "even" if i % 2 == 0 else "odd"
                tabel.insert("", "end", values=row, tags=(tag,))

        zoek_var.trace_add("write", update_tabel)

        def on_select(event):
            geselecteerd = tabel.selection()
            if geselecteerd:
                rij = tabel.item(geselecteerd[0])["values"]
                geselecteerde_mobility_id.set(rij[0])
                mobility = mobility_per_id.get(int(rij[0]))
                if mobility:
                    studentInput.set(student_optie_per_id.get(mobility[1], ""))
                    transportInput.set(transport_optie_per_id.get(mobility[2], ""))
                datumInput.delete(0, "end")
                datumInput.insert(0, rij[3])
            else:
                geselecteerde_mobility_id.set("")
            update_verplaatsing_knoppen()

        tabel.bind("<<TreeviewSelect>>", on_select)
