from datetime import datetime


class Controller:
    def __init__(self, model):
        self.model = model
    # STUDENTS

    def add_student(self, naam, klas, afstand):

        # controle lege velden
        if not naam or not klas or not afstand:
            return "ERROR: Vul alle velden in"

        # afstand moet een getal zijn
        try:
            afstand = float(afstand)
        except:
            return "ERROR: Afstand moet een getal zijn"

        # afstand mag niet negatief zijn
        if afstand < 0:
            return "ERROR: Afstand mag niet negatief zijn"

        # student toevoegen
        self.model.add_student(naam, klas, afstand)

        return "Student succesvol toegevoegd"

    def get_students(self):
        return self.model.get_students()


    def get_all_students(self):
        rows = self.model.get_students()
        return [(r[0], r[1], r[2], f"{r[3]} km") for r in rows]

    def update_student(self, student_id, naam, klas, afstand):
        self.model.update_student(student_id, naam, klas, float(afstand))

    def delete_student(self, student_id):

        # controle of student bestaat
        students = self.model.get_students()

        bestaat = False

        for s in students:
            if s[0] == student_id:
                bestaat = True

        if not bestaat:
            return "ERROR: Student bestaat niet"

        self.model.delete_student(student_id)

        return "Student verwijderd"

    # TRANSPORT

    def add_transport(self, transport_type):

        if not transport_type:
            return "ERROR: Geef een transporttype op"

        self.model.add_transport(transport_type)

        return "Transport toegevoegd"

    def get_transport(self):
        return self.model.get_transport()

    def delete_transport(self, transport_id):
        self.model.delete_transport(transport_id)

    # MOBILITY

    def add_mobility(self, student_id, transport_id, datum):

        # controle lege velden
        if not student_id or not transport_id or not datum:
            return "ERROR: Vul alle mobility gegevens in"

        # datum validatie
        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except:
            return "ERROR: Datum moet YYYY-MM-DD zijn"

        # mobility toevoegen
        self.model.add_mobility(student_id, transport_id, datum)

        return "Mobility log toegevoegd"

    def get_mobility(self):
        return self.model.get_mobility()

    # ANALYSES

    def get_analysis(self):

        transport_data = self.model.count_transport()
        avg_distance = self.model.avg_distance()
        classes = self.model.students_per_class()

        return {
            "transport": self.model.count_transport(),
            "avg_distance": self.model.avg_distance()
        }
