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

    def _mobility_exists(self, mobility_id):
        return any(mobility[0] == mobility_id for mobility in self.model.get_mobility())

    def _transport_type_exists(self, transport_type, ignore_id=None):
        transport_type = transport_type.lower()
        for transport in self.model.get_transport():
            if ignore_id is not None and transport[0] == ignore_id:
                continue
            if transport[1].lower() == transport_type:
                return True
        return False

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
        transport_type = transport_type.strip() if transport_type else ""

        if not transport_type:
            return "ERROR: Geef een transporttype op"

        if self._transport_type_exists(transport_type):
            return "ERROR: Dit transporttype bestaat al"

        self.model.add_transport(transport_type)
        return "Transport toegevoegd"

    def get_transport(self):
        return self.model.get_transport()

    def update_transport(self, transport_id, transport_type):
        transport_id = self._to_int(transport_id, "Transport id")
        if isinstance(transport_id, str):
            return transport_id

        if not self._transport_exists(transport_id):
            return "ERROR: Transport bestaat niet"

        transport_type = transport_type.strip() if transport_type else ""

        if not transport_type:
            return "ERROR: Geef een transporttype op"

        if self._transport_type_exists(transport_type, ignore_id=transport_id):
            return "ERROR: Dit transporttype bestaat al"

        self.model.update_transport(transport_id, transport_type)
        return "Transport aangepast"

    def delete_transport(self, transport_id):
        transport_id = self._to_int(transport_id, "Transport id")
        if isinstance(transport_id, str):
            return transport_id

        if not self._transport_exists(transport_id):
            return "ERROR: Transport bestaat niet"

        if self.model.transport_in_use(transport_id) > 0:
            return "ERROR: Dit transporttype wordt nog gebruikt bij verplaatsingen"

        self.model.delete_transport(transport_id)
        return "Transport verwijderd"

    # MOBILITY
    def add_mobility(self, student_id, transport_id, datum):
        controle = self._validate_mobility(student_id, transport_id, datum)
        if isinstance(controle, str):
            return controle

        student_id, transport_id, datum = controle
        self.model.add_mobility(student_id, transport_id, datum)
        return "Verplaatsing toegevoegd"

    def get_mobility(self):
        return self.model.get_mobility()

    def get_mobility_overview(self):
        return self.model.get_mobility_overview()

    def update_mobility(self, mobility_id, student_id, transport_id, datum):
        mobility_id = self._to_int(mobility_id, "Verplaatsing id")
        if isinstance(mobility_id, str):
            return mobility_id

        if not self._mobility_exists(mobility_id):
            return "ERROR: Verplaatsing bestaat niet"

        controle = self._validate_mobility(student_id, transport_id, datum)
        if isinstance(controle, str):
            return controle

        student_id, transport_id, datum = controle
        self.model.update_mobility(mobility_id, student_id, transport_id, datum)
        return "Verplaatsing aangepast"

    def delete_mobility(self, mobility_id):
        mobility_id = self._to_int(mobility_id, "Verplaatsing id")
        if isinstance(mobility_id, str):
            return mobility_id

        if not self._mobility_exists(mobility_id):
            return "ERROR: Verplaatsing bestaat niet"

        self.model.delete_mobility(mobility_id)
        return "Verplaatsing verwijderd"

    def _validate_mobility(self, student_id, transport_id, datum):
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

        return student_id, transport_id, datum

    # ANALYSES
    def get_transport_verdeling(self):
        return self.model.get_transport_verdeling()

    def get_analysis(self):
        students = self.model.get_students()
        transporten = self.model.get_transport()
        mobility_logs = self.model.get_mobility()

        student_per_id = {student[0]: student for student in students}
        transport_naam_per_id = {transport[0]: transport[1] for transport in transporten}

        transport_tellingen = {transport[0]: 0 for transport in transporten}
        afstanden_per_transport = {transport[0]: [] for transport in transporten}
        vervoersmiddelen_per_klas = {}
        vervoer_per_leerling = {}

        for mobility in mobility_logs:
            student_id = mobility[1]
            transport_id = mobility[2]
            student = student_per_id.get(student_id)

            if transport_id in transport_tellingen:
                transport_tellingen[transport_id] += 1

            if student:
                afstanden_per_transport.setdefault(transport_id, []).append(student[3])
                klas = student[2]
                vervoersmiddelen_per_klas.setdefault(klas, {})
                vervoersmiddelen_per_klas[klas][transport_id] = (
                    vervoersmiddelen_per_klas[klas].get(transport_id, 0) + 1
                )
                vervoer_per_leerling[student_id] = vervoer_per_leerling.get(student_id, 0) + 1

        transport_data = [
            (transport_naam_per_id[transport_id], aantal)
            for transport_id, aantal in transport_tellingen.items()
        ]

        afstand_per_transport = []
        for transport_id, afstanden in afstanden_per_transport.items():
            if afstanden:
                gemiddelde = sum(afstanden) / len(afstanden)
                gemiddelde_tekst = f"{round(gemiddelde, 2)} km"
            else:
                gemiddelde_tekst = "Geen data"

            afstand_per_transport.append(
                (transport_naam_per_id.get(transport_id, "Onbekend"), gemiddelde_tekst)
            )

        klas_data = []
        klassen = sorted({student[2] for student in students})
        for klas in klassen:
            studenten_in_klas = [student for student in students if student[2] == klas]
            aantal_studenten = len(studenten_in_klas)
            gemiddelde = sum(student[3] for student in studenten_in_klas) / aantal_studenten

            verdeling = vervoersmiddelen_per_klas.get(klas, {})
            if verdeling:
                verdeling_tekst = ", ".join(
                    f"{transport_naam_per_id.get(tid, 'Onbekend')}: {aantal}"
                    for tid, aantal in verdeling.items()
                )
            else:
                verdeling_tekst = "Geen verplaatsingen"

            klas_data.append(
                (klas, aantal_studenten, f"{round(gemiddelde, 2)} km", verdeling_tekst)
            )

        leerling_data = [
            (student_per_id[s_id][1], aantal)
            for s_id, aantal in vervoer_per_leerling.items()
            if s_id in student_per_id
        ]
        return {
            "transport": transport_data,
            "avg_distance": self.model.avg_distance(),
            "avg_distance_by_transport": afstand_per_transport,
            "classes": klas_data,
            "transport_per_student": leerling_data,
        }
