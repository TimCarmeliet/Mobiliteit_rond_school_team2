import tkinter as tk
from handy_view import maak_kader, maak_tabel
from tkinter import messagebox, ttk

# kleur
blauw = "#185FA5"
rood = "#b3261e"
groen = "#2f7d32"
grijs = "#eee"
donker_grijs = "#333333"
class mainView:

    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.geometry("1200x600")
        self.root.title("Mobiliteit rond de school")
        



        self.topnav = tk.Frame(root, bg="#333", height=40)
        self.topnav.pack(side="top", fill="x")

        self.styleButton = {"bg": "#555", "fg": "white", "activebackground": "#777", "activeforeground": "white", "bd": 0, "padx": 20, "pady": 10}

        tk.Button(self.topnav, text="student",command=self.student, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="vervoer", command=self.vervoer, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="dashboard", command=self.dashboard, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="verplaatsing", command=self.verplaatsing, **self.styleButton).pack(side="left")
        tk.Button(self.topnav, text="analyse", command=self.analyse, **self.styleButton).pack(side="left")

            
        self.student_content = tk.Frame(self.root, bg="#eee")
        self.vervoer_content = tk.Frame(self.root, bg="#eee")
        self.dashboard_content = tk.Frame(self.root, bg="#eee")
        self.verplaatsing_content = tk.Frame(self.root, bg="#eee")
        self.analyse_content = tk.Frame(self.root, bg="#eee")

        self.student()

    def clear_content(self):
        self.student_content.forget()
        self.vervoer_content.forget()
        self.dashboard_content.forget()
        self.verplaatsing_content.forget()
        self.analyse_content.forget()

    def vervoer(self):
        
        self.clear_content()
        self.vervoer_content = tk.Frame(self.root, bg="#eee")
        self.vervoer_content.pack(fill="both", expand=True)

        tk.Label(self.vervoer_content, text="Vervoer pagina", font=("Arial", 24)).pack(pady=20)

    def vervoer(self):
        self.clear_content()
        self.vervoer_content = tk.Frame(self.root, bg=grijs)
        self.vervoer_content.pack(fill="both", expand=True)
        data = self.controller.get_transport()
        geselecteerde_transport_id = tk.StringVar()

        # frame vervoer beheren
        # geen aanpassen knop - projectfiche zegt enkel toevoegen en verwijderen
        frame = maak_kader(self.vervoer_content, titel="Vervoer beheren", header_kleur=blauw)
        frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

        form = tk.Frame(frame, bg="white", padx=16, pady=14)
        form.pack(fill="x")

        tk.Label(form, text="Vervoersmiddel", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
        vervoerTypeinput = tk.Entry(form, width=28, font=("Arial", 10), relief="solid", bd=1)
        vervoerTypeinput.grid(row=1, column=0, sticky="ew", pady=(3, 14))

        form.columnconfigure(0, weight=1)

        knoppen = tk.Frame(form, bg="white")
        knoppen.grid(row=2, column=0, sticky="ew")

        def formulier_leegmaken():
            geselecteerde_transport_id.set("")
            vervoerTypeinput.delete(0, "end")
            tabel.selection_remove(tabel.selection())

        def vervoer_toevoegen():
            transport_type = vervoerTypeinput.get().strip()
            if not transport_type:
                messagebox.showwarning("Vervoer", "Vul een vervoersmiddel in.")
                return
            self.controller.add_transport(transport_type)
            self.vervoer()

        def vervoer_verwijderen():
            if not geselecteerde_transport_id.get():
                messagebox.showwarning("Vervoer", "Selecteer eerst een vervoersmiddel uit de tabel.")
                return
            self.controller.delete_transport(geselecteerde_transport_id.get())
            self.vervoer()

        knopstijl = {"fg": "white", "activeforeground": "white", "bd": 0, "padx": 12, "pady": 7, "font": ("Arial", 9, "bold"), "cursor": "hand2"}
        tk.Button(knoppen, text="Toevoegen", command=vervoer_toevoegen, bg=blauw, activebackground=blauw, **knopstijl).pack(side="left", padx=(0, 10))
        tk.Button(knoppen, text="Verwijderen", command=vervoer_verwijderen, bg=rood, activebackground=rood, **knopstijl).pack(side="left")

        tk.Button(form, text="Leegmaken", command=formulier_leegmaken, bg="#e7e7e7", fg=donker_grijs, activebackground="#d8d8d8", bd=0, padx=10, pady=6, cursor="hand2").grid(row=3, column=0, sticky="ew", pady=(10, 0))

        # frame overzicht vervoersmiddelen
        frame2 = maak_kader(self.vervoer_content, titel=f"Overzicht vervoersmiddelen ({len(data)})", header_kleur=blauw)
        frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

        tabel = maak_tabel(frame2, kolommen=["ID", "Type"], data=data)
        tabel.column("ID", width=50, anchor="center")
        tabel.column("Type", width=200)

        # klik op rij -> vult het formulier in
        def on_select(event):
            geselecteerd = tabel.selection()
            if geselecteerd:
                rij = tabel.item(geselecteerd[0])["values"]
                geselecteerde_transport_id.set(rij[0])
                vervoerTypeinput.delete(0, "end")
                vervoerTypeinput.insert(0, rij[1])

        tabel.bind("<<TreeviewSelect>>", on_select)

    def student(self):
        self.clear_content()
        self.student_content = tk.Frame(self.root, bg="#eee")
        self.student_content.pack(fill="both", expand=True)
        data = self.controller.get_all_students()
        geselecteerde_student_id = tk.StringVar()

        # frame student bewerken
        frame = maak_kader(self.student_content, titel="Student bewerken", verticalSpace=20, horizontalSpace=20, header_kleur=blauw)
        frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

        form = tk.Frame(frame, bg="white", padx=16, pady=14)
        form.pack(fill="x")

        tk.Label(form, text="Naam", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
        studentNaaminput = tk.Entry(form, width=28, font=("Arial", 10), relief="solid", bd=1)
        studentNaaminput.grid(row=1, column=0, sticky="ew", pady=(3, 12))

        tk.Label(form, text="Klas", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=2, column=0, sticky="w")
        studentKlasinput = tk.Entry(form, width=28, font=("Arial", 10), relief="solid", bd=1)
        studentKlasinput.grid(row=3, column=0, sticky="ew", pady=(3, 12))

        tk.Label(form, text="Afstand tot school (km)", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=4, column=0, sticky="w")
        studentAfstandinput = tk.Entry(form, width=28, font=("Arial", 10), relief="solid", bd=1)
        studentAfstandinput.grid(row=5, column=0, sticky="ew", pady=(3, 14))

        form.columnconfigure(0, weight=1)

        knoppen = tk.Frame(form, bg="white")
        knoppen.grid(row=6, column=0, sticky="ew")

        def input_waarden():
            naam = studentNaaminput.get().strip()
            klas = studentKlasinput.get().strip()
            afstand = studentAfstandinput.get().strip().replace(",", ".").replace(" km", "")

            if not naam or not klas or not afstand:
                messagebox.showwarning("Student", "Vul naam, klas en afstand in.")
                return None

            try:
                float(afstand)
            except ValueError:
                messagebox.showwarning("Student", "Afstand moet een getal zijn, bijvoorbeeld 4.5.")
                return None

            return naam, klas, afstand

        def formulier_leegmaken():
            geselecteerde_student_id.set("")
            studentNaaminput.delete(0, "end")
            studentKlasinput.delete(0, "end")
            studentAfstandinput.delete(0, "end")
            tabel.selection_remove(tabel.selection())

        def student_toevoegen():
            waarden = input_waarden()
            if waarden is None:
                return
            self.controller.add_student(*waarden)
            self.student()

        def student_aanpassen():
            waarden = input_waarden()
            if waarden is None:
                return
            if not geselecteerde_student_id.get():
                messagebox.showwarning("Student", "Selecteer eerst een student uit de tabel.")
                return
            self.controller.update_student(geselecteerde_student_id.get(), *waarden)
            self.student()

        def student_verwijderen():
            if not geselecteerde_student_id.get():
                messagebox.showwarning("Student", "Selecteer eerst een student uit de tabel.")
                return
            self.controller.delete_student(geselecteerde_student_id.get())
            self.student()

        knopstijl = {"fg": "white","activeforeground": "white","bd": 0,"padx": 12,"pady": 7,"font": ("Arial", 9, "bold"),"cursor": "hand2"}
        tk.Button(knoppen, text="Toevoegen", command=student_toevoegen, bg=blauw, activebackground=blauw, **knopstijl).pack(side="left", padx=(0, 10))
        tk.Button(knoppen, text="Aanpassen", command=student_aanpassen, bg=groen, activebackground="#2f7d32", **knopstijl).pack(side="left", padx=(0, 10))
        tk.Button(knoppen, text="Verwijderen", command=student_verwijderen, bg=rood, activebackground="#b3261e", **knopstijl).pack(side="left")

        tk.Button(form, text="Leegmaken", command=formulier_leegmaken, bg="#e7e7e7", fg=donker_grijs, activebackground="#d8d8d8", bd=0, padx=10, pady=6, cursor="hand2").grid(row=7, column=0, sticky="ew", pady=(10, 0))


        # frame2 overzicht studenten
        frame2 = maak_kader(self.student_content, titel=f"Overzicht studenten ({len(data)})", header_kleur=blauw)
        frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

        tabel = maak_tabel(frame2, 
            kolommen=["ID", "Naam", "Klas", "Afstand"],
            data=data
        )
        tabel.column("ID", width=50, anchor="center")
        tabel.column("Naam", width=210)
        tabel.column("Klas", width=90, anchor="center")
        tabel.column("Afstand", width=110, anchor="e")

        # klik op rij -> vult het formulier in
        def on_select(event):
            geselecteerd = tabel.selection()
            if geselecteerd:
                rij = tabel.item(geselecteerd[0])["values"]
                geselecteerde_student_id.set(rij[0])
                studentNaaminput.delete(0, "end")
                studentNaaminput.insert(0, rij[1])
                studentKlasinput.delete(0, "end")
                studentKlasinput.insert(0, rij[2])
                studentAfstandinput.delete(0, "end")
                studentAfstandinput.insert(0, str(rij[3]).replace(" km", ""))

        tabel.bind("<<TreeviewSelect>>", on_select)



    def dashboard(self):

        self.clear_content()
        self.dashboard_content = tk.Frame(self.root, bg="#eee")
        self.dashboard_content.pack(fill="both", expand=True)

        tk.Label(self.dashboard_content, text="Dashboard pagina", font=("Arial", 24)).pack(pady=20)
    
    def verplaatsing(self):

        self.clear_content()
        self.verplaatsing_content = tk.Frame(self.root, bg="#eee")
        self.verplaatsing_content.pack(fill="both", expand=True)

        tk.Label(self.verplaatsing_content, text="Verplaatsing pagina", font=("Arial", 24)).pack(pady=20)

    def verplaatsing(self):
        self.clear_content()
        self.verplaatsing_content = tk.Frame(self.root, bg=grijs)
        self.verplaatsing_content.pack(fill="both", expand=True)

        # haal studenten en transport op voor de dropdowns
        studenten = self.controller.get_students()
        transport = self.controller.get_transport()
        logs = self.controller.get_mobility()
        geselecteerde_log_id = tk.StringVar()

        # dropdown opties: "id - naam"
        student_opties = [f"{s[0]} - {s[1]}" for s in studenten]
        transport_opties = [f"{t[0]} - {t[1]}" for t in transport]

        # frame verplaatsing beheren
        frame = maak_kader(self.verplaatsing_content, titel="Verplaatsing beheren", header_kleur=blauw)
        frame.pack_configure(side="left", fill="y", padx=(20, 10), pady=20, anchor="nw")

        form = tk.Frame(frame, bg="white", padx=16, pady=14)
        form.pack(fill="x")

        tk.Label(form, text="Student", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
        student_var = tk.StringVar()
        student_dropdown = ttk.Combobox(form, textvariable=student_var, values=student_opties, width=26, state="readonly")
        student_dropdown.grid(row=1, column=0, sticky="ew", pady=(3, 12))

        tk.Label(form, text="Vervoersmiddel", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=2, column=0, sticky="w")
        transport_var = tk.StringVar()
        transport_dropdown = ttk.Combobox(form, textvariable=transport_var, values=transport_opties, width=26, state="readonly")
        transport_dropdown.grid(row=3, column=0, sticky="ew", pady=(3, 12))

        tk.Label(form, text="Datum (YYYY-MM-DD)", bg="white", fg=donker_grijs, font=("Arial", 10, "bold"), anchor="w").grid(row=4, column=0, sticky="w")
        datumInput = tk.Entry(form, width=28, font=("Arial", 10), relief="solid", bd=1)
        datumInput.grid(row=5, column=0, sticky="ew", pady=(3, 14))

        form.columnconfigure(0, weight=1)

        knoppen = tk.Frame(form, bg="white")
        knoppen.grid(row=6, column=0, sticky="ew")

        def input_waarden():
            student_keuze = student_var.get()
            transport_keuze = transport_var.get()
            datum = datumInput.get().strip()

            if not student_keuze or not transport_keuze or not datum:
                messagebox.showwarning("Verplaatsing", "Vul alle velden in.")
                return None

            # haal het id op uit de "id - naam" string
            student_id = student_keuze.split(" - ")[0]
            transport_id = transport_keuze.split(" - ")[0]

            return student_id, transport_id, datum

        def formulier_leegmaken():
            geselecteerde_log_id.set("")
            student_var.set("")
            transport_var.set("")
            datumInput.delete(0, "end")
            tabel.selection_remove(tabel.selection())

        def verplaatsing_toevoegen():
            waarden = input_waarden()
            if waarden is None:
                return
            resultaat = self.controller.add_mobility(*waarden)
            if resultaat.startswith("ERROR"):
                messagebox.showwarning("Verplaatsing", resultaat)
                return
            self.verplaatsing()

        def verplaatsing_aanpassen():
            waarden = input_waarden()
            if waarden is None:
                return
            if not geselecteerde_log_id.get():
                messagebox.showwarning("Verplaatsing", "Selecteer eerst een verplaatsing uit de tabel.")
                return
            resultaat = self.controller.update_mobility(geselecteerde_log_id.get(), *waarden)
            if resultaat.startswith("ERROR"):
                messagebox.showwarning("Verplaatsing", resultaat)
                return
            self.verplaatsing()

        def verplaatsing_verwijderen():
            if not geselecteerde_log_id.get():
                messagebox.showwarning("Verplaatsing", "Selecteer eerst een verplaatsing uit de tabel.")
                return
            self.controller.delete_mobility(geselecteerde_log_id.get())
            self.verplaatsing()

        knopstijl = {"fg": "white", "activeforeground": "white", "bd": 0, "padx": 12, "pady": 7, "font": ("Arial", 9, "bold"), "cursor": "hand2"}
        tk.Button(knoppen, text="Toevoegen", command=verplaatsing_toevoegen, bg=blauw, activebackground=blauw, **knopstijl).pack(side="left", padx=(0, 10))
        tk.Button(knoppen, text="Aanpassen", command=verplaatsing_aanpassen, bg=groen, activebackground=groen, **knopstijl).pack(side="left", padx=(0, 10))
        tk.Button(knoppen, text="Verwijderen", command=verplaatsing_verwijderen, bg=rood, activebackground=rood, **knopstijl).pack(side="left")

        tk.Button(form, text="Leegmaken", command=formulier_leegmaken, bg="#e7e7e7", fg=donker_grijs, activebackground="#d8d8d8", bd=0, padx=10, pady=6, cursor="hand2").grid(row=7, column=0, sticky="ew", pady=(10, 0))

        # frame overzicht verplaatsingen
        frame2 = maak_kader(self.verplaatsing_content, titel=f"Overzicht verplaatsingen ({len(logs)})", header_kleur=blauw)
        frame2.pack_configure(side="left", padx=(10, 20), pady=20, fill="both", expand=True, anchor="nw")

        tabel = maak_tabel(frame2, kolommen=["ID", "Student ID", "Transport ID", "Datum"], data=logs)
        tabel.column("ID", width=50, anchor="center")
        tabel.column("Student ID", width=100, anchor="center")
        tabel.column("Transport ID", width=100, anchor="center")
        tabel.column("Datum", width=120, anchor="center")

        # klik op rij -> vult het formulier in
        def on_select(event):
            geselecteerd = tabel.selection()
            if geselecteerd:
                rij = tabel.item(geselecteerd[0])["values"]
                geselecteerde_log_id.set(rij[0])

                # zet dropdown op juiste student
                for optie in student_opties:
                    if optie.startswith(str(rij[1]) + " - "):
                        student_var.set(optie)
                        break

                # zet dropdown op juist transport
                for optie in transport_opties:
                    if optie.startswith(str(rij[2]) + " - "):
                        transport_var.set(optie)
                        break

                datumInput.delete(0, "end")
                datumInput.insert(0, rij[3])

        tabel.bind("<<TreeviewSelect>>", on_select)
    
    def analyse(self):

        self.clear_content()
        self.analyse_content = tk.Frame(self.root, bg="#eee")
        self.analyse_content.pack(fill="both", expand=True)

        tk.Label(self.analyse_content, text="Analyse pagina", font=("Arial", 24)).pack(pady=20)