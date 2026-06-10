class FlightInfo:
    """
        Data model for a flight record

        Maps to the Flight table in FlightManagement.db
        FlightID is a string PK, same format as old FlightNumber (e.g. BA101)
        OriginAirportID and DestinationAirportID are FKs to Airport
        Old plain Origin string and integer DestinationID have been remove
    """

    def __init__(self):
        """
            Default empty values
        """
        self.flightID = ''
        self.departureTime = ''
        self.arrivalTime = ''
        self.status = ''
        self.originAirportID = ''
        self.destinationAirportID = ''
        self.pilotID = 0

    def set_flight_id(self, flightID):
        """
            Set flight ID string, e.g. BA101
        """
        self.flightID = flightID

    def set_departure_time(self, departureTime):
        """
            Set departure time, format YYYY-MM-DD HH:MM
        """
        self.departureTime = departureTime

    def set_arrival_time(self, arrivalTime):
        """
            Set arrival time, format YYYY-MM-DD HH:MM
        """
        self.arrivalTime = arrivalTime

    def set_status(self, status):
        """
            Set status: Scheduled, Delayed, or Cancelled
        """
        self.status = status

    def set_origin_airport_id(self, originAirportID):
        """
            Set origin IATA code, must exist in Airport table
        """
        self.originAirportID = originAirportID

    def set_destination_airport_id(self, destinationAirportID):
        """
            Set destination IATA code, must exist in Airport table
        """
        self.destinationAirportID = destinationAirportID

    def set_pilot_id(self, pilotID):
        """
            Set assigned pilot ID, must exist in Pilot table
        """
        self.pilotID = pilotID

    def get_flight_id(self):
        """
            Return flight ID string
        """
        return self.flightID

    def get_departure_time(self):
        """
            Return departure time
        """
        return self.departureTime

    def get_arrival_time(self):
        """
            Return arrival time
        """
        return self.arrivalTime

    def get_status(self):
        """
            Return status
        """
        return self.status

    def get_origin_airport_id(self):
        """
            Return origin IATA code
        """
        return self.originAirportID

    def get_destination_airport_id(self):
        """
            Return destination IATA code
        """
        return self.destinationAirportID

    def get_pilot_id(self):
        """
            Return assigned pilot ID
        """
        return self.pilotID

    def __str__(self):
        """
            Newline-separated string for DB insertion

            Order matches Flight table column order
        """
        return (self.flightID + "\n" + self.departureTime + "\n" +
                self.arrivalTime + "\n" + self.status + "\n" +
                self.originAirportID + "\n" + self.destinationAirportID + "\n" +
                str(self.pilotID))