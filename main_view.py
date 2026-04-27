from email import header
import tkinter as tk

class mainView:

    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
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

        #kader in de window maken
        kader = tk.Frame(self.student_content, bg="white", bd=1, relief="solid")
        kader.pack(padx=20, pady=20, anchor="nw")

        header = tk.Label(kader, text="Student pagina", bg="#333", fg="white",font=("Arial", 11, "bold"), padx=10, pady=6)
        header.pack(fill="x")

        tk.Frame(kader, height=1, bg="#cccccc").pack(fill="x")
        tk.Label(kader, text="attribuut", bg="white", fg="#333333",font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")
        tk.Frame(kader, height=1, bg="#cccccc").pack(fill="x")
        tk.Label(kader, text="attribuut", bg="white", fg="#333333",font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")
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