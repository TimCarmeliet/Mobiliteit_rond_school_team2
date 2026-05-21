from datetime import datetime


class Controller:
    def __init__(self, model):
        self.model = model

    def _to_int(self, value, field_name):
        try:
            return int(value)
        except (TypeError, ValueError):
            return f"ERROR: {field_name} moet een getal zijn"

    def _student_exists(self, student_id):
        return any(student[0] == student_id for student in self.model.get_students())

    def _transport_exists(self, transport_id):
        return any(transport[0] == transport_id for transport in self.model.get_transport())

    # STUDENTS
    def add_student(self, naam, klas, afstand):
        if not naam or not klas or not afstand:
            return "ERROR: Vul alle velden in"

        try:
            afstand = float(afstand)
        except ValueError:
            return "ERROR: Afstand moet een getal zijn"

        if afstand < 0:
            return "ERROR: Afstand mag niet negatief zijn"

        self.model.add_student(naam, klas, afstand)
        return "Student succesvol toegevoegd"

    def get_students(self):
        return self.model.get_students()

    def get_all_students(self):
        rows = self.model.get_students()
        return [(r[0], r[1], r[2], f"{r[3]} km") for r in rows]

    def update_student(self, student_id, naam, klas, afstand):
        student_id = self._to_int(student_id, "Student id")
        if isinstance(student_id, str):
            return student_id

        if not self._student_exists(student_id):
            return "ERROR: Student bestaat niet"

        if not naam or not klas or not afstand:
            return "ERROR: Vul alle velden in"

        try:
            afstand = float(afstand)
        except ValueError:
            return "ERROR: Afstand moet een getal zijn"

        if afstand < 0:
            return "ERROR: Afstand mag niet negatief zijn"

        self.model.update_student(student_id, naam, klas, afstand)
        return "Student succesvol aangepast"

    def delete_student(self, student_id):
        student_id = self._to_int(student_id, "Student id")
        if isinstance(student_id, str):
            return student_id

        if not self._student_exists(student_id):
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
        transport_id = self._to_int(transport_id, "Transport id")
        if isinstance(transport_id, str):
            return transport_id

        if not self._transport_exists(transport_id):
            return "ERROR: Transport bestaat niet"

        self.model.delete_transport(transport_id)
        return "Transport verwijderd"

    # MOBILITY
    def add_mobility(self, student_id, transport_id, datum):
        if not student_id or not transport_id or not datum:
            return "ERROR: Vul alle mobility gegevens in"

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

        self.model.add_mobility(student_id, transport_id, datum)
        return "Mobility log toegevoegd"

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

    # ANALYSES
    def get_analysis(self):
        return {
            "transport": self.model.count_transport(),
            "avg_distance": self.model.avg_distance()
        }