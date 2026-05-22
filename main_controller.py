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
        log_id = self._to_int(log_id, "Log id")
        if isinstance(log_id, str):
            return log_id

        student_id = self._to_int(student_id, "Student id")
        if isinstance(student_id, str):
            return student_id

        transport_id = self._to_int(transport_id, "Transport id")
        if isinstance(transport_id, str):
            return transport_id

        if not self._student_exists(student_id):
            return "ERROR: Student bestaat niet"

        if not self._transport_exists(transport_id):
            return "ERROR: Transport bestaat niet"

        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            return "ERROR: Datum moet YYYY-MM-DD zijn"

        self.model.update_mobility(log_id, student_id, transport_id, datum)
        return "Verplaatsing aangepast"

    def delete_mobility(self, log_id):
        log_id = self._to_int(log_id, "Log id")
        if isinstance(log_id, str):
            return log_id

        self.model.delete_mobility(log_id)
        return "Verplaatsing verwijderd"

    # ANALYSE
    def get_analysis(self):
        return {
            "transport": self.model.count_transport(),
            "avg_distance": self.model.avg_distance()
        }