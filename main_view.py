import tkinter as tk
from handy_view import maak_kader, maak_tabel
from tkinter import messagebox, ttk
from tab_logs import LogsTab
from analyse import AnalyseTab

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
    
    def analyse(self):

        self.clear_content()
        self.analyse_content = tk.Frame(self.root, bg="#eee")
        self.analyse_content.pack(fill="both", expand=True)

        tk.Label(self.analyse_content, text="Analyse pagina", font=("Arial", 24)).pack(pady=20)