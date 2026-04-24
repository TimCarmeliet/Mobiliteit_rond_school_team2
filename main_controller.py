class Controller:
    def __init__(self, model):
        self.model = model

    # STUDENTS
    def add_student(self, naam, klas, afstand):
        if naam and klas and afstand:
            self.model.add_student(naam, klas, float(afstand))

    def get_students(self):
        return self.model.get_students()

    def delete_student(self, student_id):
        self.model.delete_student(student_id)

    # TRANSPORT
    def add_transport(self, t):
        if t:
            self.model.add_transport(t)

    def get_transport(self):
        return self.model.get_transport()

    # MOBILITY
    def add_mobility(self, student_id, transport_id, datum):
        self.model.add_mobility(student_id, transport_id, datum)

    def get_mobility(self):
        return self.model.get_mobility()

    # ANALYSE
    def get_analysis(self):
        return {
            "transport": self.model.count_transport(),
            "avg_distance": self.model.avg_distance()
        }