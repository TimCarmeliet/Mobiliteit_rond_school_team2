import tkinter as tk

def maak_kader(parent, titel, verticalSpace=20, horizontalSpace=20, header_kleur="#185FA5"):
    # buitenste frame/de rand
    frame = tk.Frame(parent, bd=1, relief="solid", bg="white")
    frame.pack(padx=verticalSpace, pady=horizontalSpace, anchor="nw")

    # header (gekleurde balk)
    header = tk.Label(frame, text=titel, bg=header_kleur, fg="white",font=("Arial", 11, "bold"), padx=10, pady=6)
    header.pack(fill="x")

    # scheidingslijn
    tk.Frame(frame, height=1, bg="#cccccc").pack(fill="x")

    return frame