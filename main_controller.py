from datetime import datetime


class Controller:
    def __init__(self, model):
        self.model = model

    # STUDENTS
    def add_student(self, naam, klas, afstand):
        if naam and klas and afstand:
            self.model.add_student(naam, klas, float(afstand))

    def get_students(self):
        return self.model.get_students()


    def get_all_students(self):
        rows = self.model.get_students()
        return [(r[0], r[1], r[2], f"{r[3]} km") for r in rows]

    def update_student(self, student_id, naam, klas, afstand):
        self.model.update_student(student_id, naam, klas, float(afstand))

    def delete_student(self, student_id):
        self.model.delete_student(student_id)

    # TRANSPORT
    def add_transport(self, t):
        if t:
            self.model.add_transport(t)

    def get_transport(self):
        return self.model.get_transport()

    def delete_transport(self, transport_id):
        self.model.delete_transport(transport_id)

    # MOBILITY
    def add_mobility(self, student_id, transport_id, datum):
        self.model.add_mobility(student_id, transport_id, datum)

    def get_mobility(self):
        return self.model.get_mobility()
    
    def update_mobility(self, log_id, student_id, transport_id, datum):
        self.model.update_mobility(int(log_id), int(student_id), int(transport_id), datum)
        return "Verplaatsing aangepast"

    def delete_mobility(self, log_id):
        self.model.delete_mobility(int(log_id))
        return "Verplaatsing verwijderd"
    
    # ANALYSE
    def get_transport_verdeling(self):
        return self.model.get_transport_verdeling()

    def get_analysis(self):
        return {
            "transport": self.model.count_transport(),
            "avg_distance": self.model.avg_distance()
        }