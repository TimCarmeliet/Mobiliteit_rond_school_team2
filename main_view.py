import tkinter as tk
from handy_view import maak_kader

# kleur
blauw = "#185FA5"
grijs = "#eee"
donker_grijs = "#333333"
class mainView:

    def __init__(self, root):
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
        #frame student bewerken
        frame = maak_kader(self.student_content, titel="Student", verticalSpace=20, horizontalSpace=10, header_kleur=blauw)
        #inhoud
        tk.Label(frame, text="naam", bg="white", fg=donker_grijs,font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")
        studentNaaminput = tk.Entry(frame).pack(fill="x", padx=10, pady=5)
        tk.Label(frame, text="klas", bg="white", fg=donker_grijs,font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")
        studentKlasinput = tk.Entry(frame).pack(fill="x", padx=10, pady=5)
        tk.Label(frame, text="Afstand tot school (km)", bg="white", fg=donker_grijs,font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")
        studentAfstandinput = tk.Entry(frame).pack(fill="x", padx=10, pady=5)
        tk.Button(frame, text="Voevoegen", bg=blauw, fg="white", activebackground=blauw, activeforeground="white", bd=0, padx=10, pady=5).pack(side="left",pady=10)
        tk.Button(frame, text="aanpassen", bg=blauw, fg="white", activebackground=blauw, activeforeground="white", bd=0, padx=10, pady=5).pack(side="left",pady=10)
        tk.Button(frame, text="Verwijderen", bg=blauw, fg="white", activebackground=blauw, activeforeground="white", bd=0, padx=10, pady=5).pack(side="left", pady=10)
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