import tkinter as tk

def maak_kader(parent, titel, attributen, methoden, header_kleur="#185FA5"):
    # buitenste frame = de rand
    frame = tk.Frame(parent, bd=1, relief="solid", bg="white")
    frame.pack(padx=20, pady=20, anchor="nw")

    # header (gekleurde balk)
    header = tk.Label(frame, text=titel, bg=header_kleur, fg="white",
                      font=("Arial", 11, "bold"), padx=10, pady=6)
    header.pack(fill="x")

    # scheidingslijn
    tk.Frame(frame, height=1, bg="#cccccc").pack(fill="x")

    # attributen
    for attribuut in attributen:
        tk.Label(frame, text=attribuut, bg="white", fg="#333333",
                 font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")


    # methoden
    for methode in methoden:
        tk.Label(frame, text=methode, bg="white", fg="#333333",
                 font=("Courier", 10), anchor="w", padx=10, pady=2).pack(fill="x")

    return frame


root = tk.Tk()
root.title("Klassendiagram")
root.configure(bg="#f0f0f0")

maak_kader(
    root,
    titel="Controller",
    attributen=[
        "- model : Model",
        "- view  : View",
    ],
    methoden=[
        "+ add_student(naam, klas, afstand)",
        "+ get_all_students() : list",
        "+ delete_student(id)",
        "+ get_avg_distance()",
    ],
    header_kleur="#185FA5"   # blauw
)

maak_kader(
    root,
    titel="Model",
    attributen=[
        "- db_path : str",
        "- connection : Connection",
    ],
    methoden=[
        "+ execute_query(...)",
        "+ fetch_all(...)",
        "+ fetch_one(...)",
    ],
    header_kleur="#0F6E56"   # groen
)

root.mainloop()