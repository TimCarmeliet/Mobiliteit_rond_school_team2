import tkinter as tk
from main_model import Model
from main_controller import Controller
from views.main_view import mainView
from analyse import AnalyseTab

def toon_foutmelding(exc_type, value, tb):
    import traceback
    from tkinter import messagebox
    
    # Formatteer de foutmelding en print naar de console
    err_msg = "".join(traceback.format_exception(exc_type, value, tb))
    print(" FOUT GEDETECTEERD:\n", err_msg)
    
    # Vind de exacte plek van de fout
    tb_summary = traceback.extract_tb(tb)
    if tb_summary:
        last_trace = tb_summary[-1]
        bestand = last_trace.filename.split("\\")[-1].split("/")[-1]
        regel = last_trace.lineno
        func = last_trace.name
        user_msg = f"Fout in {bestand} op regel {regel} (in functie '{func}'):\n\n{exc_type.__name__}: {value}"
    else:
        user_msg = f"Er is een fout opgetreden:\n\n{exc_type.__name__}: {value}"
        
    messagebox.showerror("Fout Gevonden", user_msg)

if __name__ == "__main__":
    root = tk.Tk()
    root.report_callback_exception = toon_foutmelding

    model = Model()
    controller = Controller(model)
    view = mainView(root, controller)

    root.mainloop() 
    
