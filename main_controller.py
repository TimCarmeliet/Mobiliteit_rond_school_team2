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
            "transport": transport_data,
            "avg_distance": avg_distance,
            "classes": classes
        }

    # EXTRA ANALYSE 1
    # Student met grootste afstand

    def longest_distance_student(self):

        students = self.model.get_students()

        if not students:
            return None

        longest = max(students, key=lambda s: s[3])

        return longest

    # EXTRA ANALYSE 2
    # Percentage vervoersmiddelen

    def transport_percentages(self):

        transport_data = self.model.count_transport()

        totaal = 0

        for item in transport_data:
            totaal += item[1]

        percentages = []

        for item in transport_data:

            transport_id = item[0]
            aantal = item[1]

            if totaal > 0:
                percentage = round((aantal / totaal) * 100, 2)
            else:
                percentage = 0

            percentages.append((transport_id, percentage))

        return percentages

    # EXTRA ANALYSE 3
    # Filter studenten per klas

    def students_per_class_filter(self, klas_naam):

        students = self.model.get_students()

        filtered = []

        for s in students:

            if s[2] == klas_naam:
                filtered.append(s)

        return filtered

    # EXTRA ANALYSE 4
    # Gemiddelde afstand per klas

    def average_distance_per_class(self):

        students = self.model.get_students()

        klas_data = {}

        for s in students:

            klas = s[2]
            afstand = s[3]

            if klas not in klas_data:
                klas_data[klas] = []

            klas_data[klas].append(afstand)

        result = []

        for klas in klas_data:

            gemiddelde = sum(klas_data[klas]) / len(klas_data[klas])

            result.append((klas, round(gemiddelde, 2)))

        return result