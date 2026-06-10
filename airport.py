class Airport:
    """
        Data model for an airport record

        Maps to the Airport table in FlightManagement.db
        AirportID is the 3-letter IATA code, used as PK
        Timezone stored as UTC offset string, e.g. UTC+1
    """

    def __init__(self):
        """
            Default empty values
        """
        self.airportID = ''
        self.airportName = ''
        self.city = ''
        self.country = ''
        self.timezone = ''

    def set_airport_id(self, airportID):
        """
            Set IATA code, used as PK
        """
        self.airportID = airportID

    def set_airport_name(self, airportName):
        """
            Set full official airport name
        """
        self.airportName = airportName

    def set_city(self, city):
        """
            Set city served by this airport
        """
        self.city = city

    def set_country(self, country):
        """
            Set country the airport is in
        """
        self.country = country

    def set_timezone(self, timezone):
        """
            Set UTC offset string, e.g. UTC+1, UTC-5
        """
        self.timezone = timezone

    def get_airport_id(self):
        """
            Return IATA code
        """
        return self.airportID

    def get_airport_name(self):
        """
            Return full airport name
        """
        return self.airportName

    def get_city(self):
        """
            Return city
        """
        return self.city

    def get_country(self):
        """
            Return country
        """
        return self.country

    def get_timezone(self):
        """
            Return UTC offset string
        """
        return self.timezone

    def __str__(self):
        """
            Newline-separated string for DB insertion

            Order matches Airport table column order
        """
        return (self.airportID + "\n" + self.airportName + "\n" +
                self.city + "\n" + self.country + "\n" + self.timezone)