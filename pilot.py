class Pilot:
    """
        Data model for a pilot record

        Maps to the Pilot table in FlightManagement.db
        Getters, setters and a __str__ for DB insertion
    """

    def __init__(self):
        """
            Default empty values
        """
        self.pilotID = 0
        self.name = ''
        self.rank = ''
        self.flightTime = 0

    def set_pilot_id(self, pilotID):
        """
            Set pilot ID
        """
        self.pilotID = pilotID

    def set_name(self, name):
        """
            Set pilot full name
        """
        self.name = name

    def set_rank(self, rank):
        """
            Set rank, e.g. Captain, First Officer
        """
        self.rank = rank

    def set_flight_time(self, flightTime):
        """
            Set total flight hours logged
        """
        self.flightTime = flightTime

    def get_pilot_id(self):
        """
            Retur pilot ID
        """
        return self.pilotID

    def get_name(self):
        """
            Return name
        """
        return self.name

    def get_rank(self):
        """
            Return rank
        """
        return self.rank

    def get_flight_time(self):
        """
            Return total flight time
        """
        return self.flightTime

    def __str__(self):
        """
            Newline-separated string for DB insertion

            Order matches Pilot table column order
        """
        return (str(self.pilotID) + "\n" +
                self.name    + "\n" +
                self.rank    + "\n" +
                str(self.flightTime))