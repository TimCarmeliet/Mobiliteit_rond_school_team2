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

    def get_overzicht_per_klas(self):
        """
        Combineert twee model-queries tot één volledig overzicht per klas.

        Bevat per klas:
          - 'klas'       : naam van de klas
          - 'aantal'     : aantal studenten in die klas
          - 'gem_afstand': gemiddelde afstand tot school (in km)
          - 'vervoer'    : dict met vervoersverdeling { type: aantal_verplaatsingen }

        Bouwt op:
          - model.get_studenten_per_klas()  -> (klas, aantal, gem_afstand)
          - model.get_vervoer_per_klas()    -> { klas: { type: n } }
        """
        studenten = self.model.get_studenten_per_klas()
        vervoer = self.model.get_vervoer_per_klas()

        resultaat = []
        for klas, aantal, gem_afstand in studenten:
            resultaat.append({
                "klas": klas,
                "aantal": aantal,
                "gem_afstand": gem_afstand or 0,
                # als er geen verplaatsingen zijn voor deze klas, geef lege dict
                "vervoer": vervoer.get(klas, {}),
            })

        return resultaat

    def get_analysis(self):
        return {
            "transport": self.model.count_transport(),
            "avg_distance": self.model.avg_distance()
        }

    # ── ATTENDANCE / AFWEZIGHEID (uitbreiding Viggo) ─────────────────────────

    def _attendance_exists(self, attendance_id):
        """Controleer of een aanwezigheidsrecord met dit id bestaat in de databank."""
        return any(record[0] == attendance_id for record in self.model.get_attendance())

    def add_attendance(self, student_id, datum, status):
        """
        Voeg een nieuw aanwezigheidsrecord toe.
        Valideert eerst alle invoervelden via _validate_attendance().
        Geeft een foutmelding terug als de validatie mislukt, anders een succesbericht.
        """
        controle = self._validate_attendance(student_id, datum, status)
        if isinstance(controle, str):
            return controle  # foutmelding doorsturen naar de view

        student_id, datum, status = controle
        self.model.add_attendance(student_id, datum, status)
        return "Aanwezigheid succesvol toegevoegd"

    def get_attendance(self):
        """Haal alle aanwezigheidsrecords op als ruwe data (voor intern gebruik)."""
        return self.model.get_attendance()

    def get_attendance_overview(self):
        """Haal aanwezigheidsrecords op met studentnamen, voor weergave in de tabel."""
        return self.model.get_attendance_overview()

    def update_attendance(self, attendance_id, student_id, datum, status):
        """
        Pas een bestaand aanwezigheidsrecord aan.
        Valideert het id en alle velden voordat het model wordt aangeroepen.
        """
        # zet het id om naar een geheel getal
        attendance_id = self._to_int(attendance_id, "Aanwezigheid id")
        if isinstance(attendance_id, str):
            return attendance_id

        # controleer of dit record bestaat
        if not self._attendance_exists(attendance_id):
            return "ERROR: Aanwezigheidsrecord bestaat niet"

        controle = self._validate_attendance(student_id, datum, status)
        if isinstance(controle, str):
            return controle

        student_id, datum, status = controle
        self.model.update_attendance(attendance_id, student_id, datum, status)
        return "Aanwezigheid succesvol aangepast"

    def delete_attendance(self, attendance_id):
        """Verwijder een aanwezigheidsrecord uit de databank."""
        attendance_id = self._to_int(attendance_id, "Aanwezigheid id")
        if isinstance(attendance_id, str):
            return attendance_id

        if not self._attendance_exists(attendance_id):
            return "ERROR: Aanwezigheidsrecord bestaat niet"

        self.model.delete_attendance(attendance_id)
        return "Aanwezigheid verwijderd"

    # ── Datum-instellingen ────────────────────────────────────────────────────
    # Voeg hier extra formaten toe als je meer invoervormen wil ondersteunen.
    # De datum wordt altijd opgeslagen als YYYY-MM-DD (eerste formaat in de lijst).
    DATUM_FORMATEN = [
        "%Y-%m-%d",   # 2026-01-15  (ISO, intern opslagformaat)
        "%d-%m-%Y",   # 15-01-2026  (Belgisch met koppeltekens)
        "%d/%m/%Y",   # 15/01/2026  (Belgisch met slashes)
        "%d.%m.%Y",   # 15.01.2026  (Belgisch met punten)
    ]

    def _parse_datum(self, datum_tekst):
        """
        Probeert de ingevoerde datum te herkennen via alle formaten in DATUM_FORMATEN.
        Geeft een datetime-object terug bij succes, of None als geen formaat past.
        """
        for formaat in self.DATUM_FORMATEN:
            try:
                return datetime.strptime(datum_tekst.strip(), formaat)
            except ValueError:
                continue
        return None

    def _validate_attendance(self, student_id, datum, status):
        """
        Valideer de invoer voor een aanwezigheidsrecord.

        Geeft een foutmelding (string) terug bij ongeldige invoer,
        of een tuple (student_id, datum_als_YYYY-MM-DD, status) bij correcte invoer.
        """
        # controleer of alle velden ingevuld zijn
        if not student_id or not datum or not status:
            return "ERROR: Vul alle velden in"

        # student_id moet een geheel getal zijn
        student_id = self._to_int(student_id, "Student id")
        if isinstance(student_id, str):
            return student_id

        # de student moet bestaan in de databank
        if not self._student_exists(student_id):
            return "ERROR: Student bestaat niet"

        # datum proberen te herkennen via alle ondersteunde formaten
        datum_obj = self._parse_datum(datum)
        if datum_obj is None:
            # toon een duidelijke foutmelding met voorbeelden van geldige formaten
            voorbeelden = " of ".join(
                datetime(2026, 1, 15).strftime(f) for f in self.DATUM_FORMATEN
            )
            return f"ERROR: Ongeldig datumformaat. Gebruik bv. {voorbeelden}"

        # datum altijd opslaan als YYYY-MM-DD (ongeacht wat de gebruiker intikte)
        datum_opgeslagen = datum_obj.strftime("%Y-%m-%d")

        # status moet een van de drie geldige waarden zijn
        geldige_statussen = ["aanwezig", "afwezig", "laat"]
        if status.lower() not in geldige_statussen:
            return f"ERROR: Status moet zijn: {', '.join(geldige_statussen)}"

        # alles is geldig: geef de gecleande waarden terug
        return student_id, datum_opgeslagen, status.lower()

    # ── ANALYSES AFWEZIGHEID ──────────────────────────────────────────────────

    def get_afwezigheid_per_klas(self):
        """Geeft het aantal aanwezig/afwezig/laat terug per klas als dictionary."""
        return self.model.get_afwezigheid_per_klas()

    def get_aanwezigheid_percentage_per_klas(self):
        """Geeft het aanwezigheidspercentage per klas terug als lijst van tuples."""
        return self.model.get_aanwezigheid_percentage_per_klas()

    def get_vervoer_vs_aanwezigheid(self):
        """Geeft de relatie tussen vervoersmiddel en aanwezigheid terug als dictionary."""
        return self.model.get_vervoer_vs_aanwezigheid()
