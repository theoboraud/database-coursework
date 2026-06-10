import sqlite3
from flight_info import FlightInfo
from pilot import Pilot
from airport import Airport


class DBOperations:
    """
Handles all DB interactions for FlightManagement.db

    One method per menu option
    Pattern: open connection, run SQL, commit/fetch, close in finally
    SQL strings kept as class constants for easy editing
    """

    sql_create_pilot = """
        CREATE TABLE IF NOT EXISTS Pilot (
            PilotID       INTEGER     NOT NULL,
            Name          VARCHAR(50) NOT NULL,
            LicenceNumber VARCHAR(20) NOT NULL UNIQUE,
            Rank          VARCHAR(20) NOT NULL,
            FlightTime    INTEGER     NOT NULL DEFAULT 0,
            PRIMARY KEY (PilotID)
        )"""

    sql_create_airport = """
        CREATE TABLE IF NOT EXISTS Airport (
            AirportID   CHAR(3)      NOT NULL,
            AirportName VARCHAR(100) NOT NULL,
            City        VARCHAR(50)  NOT NULL,
            Country     VARCHAR(50)  NOT NULL,
            Timezone    VARCHAR(10)  NOT NULL,
            PRIMARY KEY (AirportID)
        )"""

    sql_create_flight = """
        CREATE TABLE IF NOT EXISTS Flight (
            FlightID             VARCHAR(10) NOT NULL,
            DepartureTime        DATETIME    NOT NULL,
            ArrivalTime          DATETIME    NOT NULL,
            Status               VARCHAR(20) NOT NULL DEFAULT 'Scheduled',
            OriginAirportID      CHAR(3)     NOT NULL REFERENCES Airport(AirportID),
            DestinationAirportID CHAR(3)     NOT NULL REFERENCES Airport(AirportID),
            PilotID              INTEGER     NOT NULL REFERENCES Pilot(PilotID),
            PRIMARY KEY (FlightID)
        )"""

    sql_insert_pilot = """
        INSERT INTO Pilot (PilotID, Name, LicenceNumber, Rank, FlightTime)
        VALUES (?, ?, ?, ?, ?)"""

    sql_insert_airport = """
        INSERT INTO Airport (AirportID, AirportName, City, Country, Timezone)
        VALUES (?, ?, ?, ?, ?)"""

    sql_insert_flight = """
        INSERT INTO Flight (FlightID, DepartureTime, ArrivalTime,
                            Status, OriginAirportID, DestinationAirportID, PilotID)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""

    sql_select_all_flights = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o  ON f.OriginAirportID      = o.AirportID
        JOIN Airport d  ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p    ON f.PilotID              = p.PilotID"""

    sql_select_all_pilots  = "SELECT * FROM Pilot"
    sql_select_all_airports = "SELECT * FROM Airport"

    sql_search_flight = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o  ON f.OriginAirportID      = o.AirportID
        JOIN Airport d  ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p    ON f.PilotID              = p.PilotID
        WHERE f.FlightID = ?"""

    sql_update_flight_status   = "UPDATE Flight SET Status = ? WHERE FlightID = ?"
    sql_update_departure_time  = "UPDATE Flight SET DepartureTime = ? WHERE FlightID = ?"
    sql_assign_pilot           = "UPDATE Flight SET PilotID = ? WHERE FlightID = ?"
    sql_update_airport_timezone = "UPDATE Airport SET Timezone = ? WHERE AirportID = ?"
    sql_delete_flight          = "DELETE FROM Flight WHERE FlightID = ?"

    sql_flights_by_airport = """
        SELECT a.AirportID, a.City, COUNT(f.FlightID) AS TotalFlights
        FROM Airport a
        LEFT JOIN Flight f ON a.AirportID = f.DestinationAirportID
        GROUP BY a.AirportID, a.City
        ORDER BY TotalFlights DESC"""

    sql_flights_by_pilot = """
        SELECT p.PilotID, p.Name, p.Rank, COUNT(f.FlightID) AS TotalFlights
        FROM Pilot p
        LEFT JOIN Flight f ON p.PilotID = f.PilotID
        GROUP BY p.PilotID, p.Name, p.Rank
        ORDER BY TotalFlights DESC"""

    sql_pilot_schedule = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        WHERE f.PilotID = ?
        ORDER BY f.DepartureTime"""

    sql_flights_by_status = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p   ON f.PilotID              = p.PilotID
        WHERE f.Status = ?"""

    sql_flights_by_date = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p   ON f.PilotID              = p.PilotID
        WHERE DATE(f.DepartureTime) = ?"""

    sql_flights_by_city = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p   ON f.PilotID              = p.PilotID
        WHERE d.City = ?"""

    sql_flights_by_origin = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p   ON f.PilotID              = p.PilotID
        WHERE f.OriginAirportID = ?"""

    sql_flights_by_destination = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p   ON f.PilotID              = p.PilotID
        WHERE f.DestinationAirportID = ?"""

    sql_flights_by_arrival_date = """
        SELECT f.FlightID, f.DepartureTime, f.ArrivalTime,
               f.Status, o.AirportID, o.City, d.AirportID, d.City,
               p.Name,
               o.Timezone, d.Timezone
        FROM Flight f
        JOIN Airport o ON f.OriginAirportID      = o.AirportID
        JOIN Airport d ON f.DestinationAirportID = d.AirportID
        JOIN Pilot p   ON f.PilotID              = p.PilotID
        WHERE DATE(f.ArrivalTime) = ?"""

    def __init__(self):
        """
Connect and create tables if missing

        Called every loop iteration
        IF NOT EXISTS makes this safe to call repeatedly
        """
        try:
            self.conn = sqlite3.connect("FlightManagement.db")
            self.cur = self.conn.cursor()
            self.cur.execute(self.sql_create_pilot)
            self.cur.execute(self.sql_create_airport)
            self.cur.execute(self.sql_create_flight)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def get_connection(self):
        """
Open a fresh connection and cursor

        Call at start of any method needing DB access
        Connection is close in the finally block each time
        """
        self.conn = sqlite3.connect("FlightManagement.db")
        self.cur = self.conn.cursor()

    # ----------------------------------------------------------------
    # Timezone helpers
    # ----------------------------------------------------------------

    def parse_utc_offset(self, timezone_str):
        """
Parse UTC offset string to int

        e.g. UTC+1 -> 1, UTC-5 -> -5

        Parameters:
            timezone_str -- UTC+X or UTC-X string
        """
        tz = timezone_str.strip().upper().replace("UTC", "")
        return int(tz) if tz else 0

    def local_to_utc(self, local_time_str, timezone_str):
        """
Convert local time to UTC by subtracting the offset

        Parameters:
            local_time_str -- YYYY-MM-DD HH:MM local time
            timezone_str   -- UTC offset string, e.g. UTC+1
        """
        from datetime import datetime, timedelta
        offset = self.parse_utc_offset(timezone_str)
        local_dt = datetime.strptime(local_time_str, "%Y-%m-%d %H:%M")
        utc_dt = local_dt - timedelta(hours=offset)
        return utc_dt.strftime("%Y-%m-%d %H:%M")

    def utc_to_local(self, utc_time_str, timezone_str):
        """
Convert UTC time to local by adding the offset

        Parameters:
            utc_time_str -- YYYY-MM-DD HH:MM UTC
            timezone_str -- UTC offset string, e.g. UTC+1
        """
        from datetime import datetime, timedelta
        offset = self.parse_utc_offset(timezone_str)
        utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M")
        local_dt = utc_dt + timedelta(hours=offset)
        return local_dt.strftime("%Y-%m-%d %H:%M")

    # ----------------------------------------------------------------
    # Print helpers
    # ----------------------------------------------------------------

    def print_flight_row(self, row):
        """
Print one flight record

        Expects a row from any flight SELECT joining Flight, Airport x2, Pilot
        Column order: FlightID, DepUTC, ArrUTC, Status,
        OriginID, OriginCity, DestID, DestCity, PilotName, OriginTZ, DestTZ
        Times shown as local + UTC in brackets
        """
        utc_dep = row[1]
        utc_arr = row[2]
        origin_tz = row[9] if len(row) > 9 else "UTC+0"
        dest_tz   = row[10] if len(row) > 10 else "UTC+0"
        local_dep = self.utc_to_local(utc_dep, origin_tz)
        local_arr = self.utc_to_local(utc_arr, dest_tz)
        print("-" * 60)
        print(f"  Flight ID     : {row[0]}")
        print(f"  Origin        : {row[5]} ({row[4]})")
        print(f"  Departure     : {local_dep} local ({origin_tz}) [{utc_dep} UTC]")
        print(f"  Destination   : {row[7]} ({row[6]})")
        print(f"  Arrival       : {local_arr} local ({dest_tz}) [{utc_arr} UTC]")
        print(f"  Pilot         : {row[8]}")
        print(f"  Status        : {row[3]}")

    def next_available_id(self, used_ids):
        """
Smallest positive int not in used_ids

        e.g. {1,2,3,5} -> 4, {1,2,3} -> 4, never returns 0

        Parameters:
            used_ids -- set of ints already taken
        """
        i = 1
        while i in used_ids:
            i += 1
        return i

    def print_table(self, headers, rows):
        """
Two-column aligned table with header and separator

        Column widths calculated from widest value so pipes always line up

        Parameters:
            headers -- tuple of two header strings
            rows    -- list of two-element tuples
        """
        col1_w = max(len(str(headers[0])), max((len(str(r[0])) for r in rows), default=0))
        col2_w = max(len(str(headers[1])), max((len(str(r[1])) for r in rows), default=0))
        separator = "  " + "-" * (col1_w + col2_w + 5)
        print(f"  {str(headers[0]):<{col1_w}} | {str(headers[1]):<{col2_w}}")
        print(separator)
        for r in rows:
            print(f"  {str(r[0]):<{col1_w}} | {str(r[1]):<{col2_w}}")
        print(separator)

    # ----------------------------------------------------------------
    # ID / code picker helpers
    # ----------------------------------------------------------------

    def random_flight_id(self, used_ids):
        """
Random flight ID: 2 uppercase letters + 3 digits, not in used_ids

        Keeps trying until unique

        Parameters:
            used_ids -- set of FlightIDs already taken
        """
        import random, string
        while True:
            fid = (random.choice(string.ascii_uppercase) +
                   random.choice(string.ascii_uppercase) +
                   str(random.randint(0, 9)) +
                   str(random.randint(0, 9)) +
                   str(random.randint(0, 9)))
            if fid not in used_ids:
                return fid

    def pick_new_flight_id(self):
        """
Ask for a FlightID not already in use

        Show taken IDs, default is random (2 letters + 3 digits)
        Loop until valid unused ID entered
        """
        self.cur.execute("SELECT FlightID FROM Flight ORDER BY FlightID")
        flights = self.cur.fetchall()
        if flights:
            print("\n Existing flights (already taken IDs):")
            self.print_table(("Flight ID",), [(r[0],) for r in flights]) if False else None
            ids_only = [r[0] for r in flights]
            col_w = max(len(i) for i in ids_only + ["Flight ID"])
            print(f"  {'Flight ID':<{col_w}}")
            print("  " + "-" * (col_w + 2))
            for fid in ids_only:
                print(f"  {fid:<{col_w}}")
            print("  " + "-" * (col_w + 2))
        used_ids = {row[0] for row in flights}
        default = self.random_flight_id(used_ids)
        while True:
            raw = input(f"Enter new Flight ID (e.g. BA101) [default: {default}]: ").strip().upper()
            if raw == "":
                print(f"  No value entered, set to default value: {default}")
                return default
            if len(raw) < 2:
                print("  Flight ID must be at least 2 characters.")
            elif raw in used_ids:
                print(f"  {raw} is already in use. Please choose a different one.")
            else:
                return raw

    def pick_existing_flight_id(self, prompt="Enter Flight ID: "):
        """
Ask for an existing FlightID

        Show the ID list, loop until valid

        Parameters:
            prompt -- input prompt string
        """
        self.cur.execute("SELECT FlightID FROM Flight ORDER BY FlightID")
        flights = self.cur.fetchall()
        if not flights:
            print("No flights found in the database.")
            return None
        ids_only = [r[0] for r in flights]
        col_w = max(len(i) for i in ids_only + ["Flight ID"])
        print("\n Available flights:")
        print(f"  {'Flight ID':<{col_w}}")
        print("  " + "-" * (col_w + 2))
        for fid in ids_only:
            print(f"  {fid:<{col_w}}")
        print("  " + "-" * (col_w + 2))
        valid_ids = set(ids_only)
        while True:
            raw = input(prompt).strip().upper()
            if raw in valid_ids:
                return raw
            print(f"  Invalid ID. Please choose from the list above.")

    def pick_new_pilot_id(self):
        """
Ask for a PilotID not already in use

        Show taken IDs, loop until unused int entered
        """
        self.cur.execute("SELECT PilotID, Name FROM Pilot ORDER BY PilotID")
        pilots = self.cur.fetchall()
        if pilots:
            print("\n Existing pilots (already taken IDs):")
            self.print_table(("ID", "Name"), pilots)
        used_ids = {row[0] for row in pilots}
        default = self.next_available_id(used_ids)
        while True:
            try:
                raw = input(f"Enter new Pilot ID (must not be in the list above) [default: {default}]: ").strip()
                if raw == "":
                    print(f"  No value entered, set to default value: {default}")
                    return default
                pid = int(raw)
                if pid not in used_ids and pid > 0:
                    return pid
                print(f"  ID {pid} is already in use. Please choose a different one.")
            except ValueError:
                print("  Please enter a number.")

    def pick_existing_pilot_id(self):
        """
Ask for an existing PilotID

        Show pilot list, loop until valid
        Blank input picks a random pilot as default
        """
        import random
        self.cur.execute(self.sql_select_all_pilots)
        pilots = self.cur.fetchall()
        if not pilots:
            print("No pilots found in the database.")
            return None
        print("\n Available pilots:")
        self.print_table(("ID", "Name — Rank"), [(r[0], f"{r[1]} — {r[3]}") for r in pilots])
        valid_ids = list({row[0] for row in pilots})
        default = random.choice(valid_ids)
        while True:
            try:
                raw = input(f"Enter Pilot ID [default: random → {default}]: ").strip()
                if raw == "":
                    print(f"  No value entered, set to default value: {default}")
                    return default
                pid = int(raw)
                if pid in valid_ids:
                    return pid
                print(f"  Invalid ID. Please choose from: {sorted(valid_ids)}")
            except ValueError:
                print("  Please enter a number.")

    def pick_new_airport_id(self):
        """
Ask for an AirportID not already in use

        Must be exactly 3 letters, unused IATA code
        """
        self.cur.execute("SELECT AirportID, City FROM Airport ORDER BY AirportID")
        airports = self.cur.fetchall()
        if airports:
            print("\n Existing airports (already taken codes):")
            self.print_table(("ID", "City"), airports)
        used_ids = {row[0] for row in airports}
        while True:
            code = input("Enter new Airport ID / IATA code (3 letters, e.g. LHR): ").strip().upper()
            if len(code) != 3 or not code.isalpha():
                print("  Airport ID must be exactly 3 letters.")
            elif code in used_ids:
                print(f"  {code} is already in use. Please choose a different one.")
            else:
                return code
            # No default for airport ID — IATA codes must be intentional

    def pick_existing_airport_id(self, prompt="Enter Airport ID: ", exclude=None):
        """
Ask for an existing AirportID

        Show airport list, loop until valid
        Blank input picks a random airport as default
        Random default never matches exclude

        Parameters:
            prompt  -- input prompt string
            exclude -- AirportID to disallow, e.g. origin when picking destination
        """
        import random
        self.cur.execute("SELECT AirportID, City, Country FROM Airport ORDER BY AirportID")
        airports = self.cur.fetchall()
        if not airports:
            print("No airports found in the database.")
            return None
        displayed = [r for r in airports if r[0] != exclude]
        print("\n Available airports:")
        self.print_table(("ID", "City, Country"), [(r[0], f"{r[1]}, {r[2]}") for r in displayed])
        valid_ids = list({row[0] for row in airports})
        candidates = [a for a in valid_ids if a != exclude]
        default = random.choice(candidates)
        while True:
            code = input(f"{prompt} [default: random → {default}]: ").strip().upper()
            if code == "":
                print(f"  No value entered, set to default value: {default}")
                return default
            elif code not in valid_ids:
                print("  Invalid ID. Airport ID not recognised. Please enter a valid airport ID.")
            elif code == exclude:
                print("  Invalid ID. The destination airport cannot be the same as the origin airport. Please enter a valid airport ID.")
            else:
                return code

    # ----------------------------------------------------------------
    # Initialisation
    # ----------------------------------------------------------------

    def create_tables(self):
        """
Drop and recreate all three tables

        Flight dropped first as it holds FKs to Airport and Pilot
        Any existing data will be lost
        Also calls insert_sample_data
        """
        try:
            self.get_connection()
            self.cur.execute("DROP TABLE IF EXISTS Flight")
            self.cur.execute("DROP TABLE IF EXISTS Pilot")
            self.cur.execute("DROP TABLE IF EXISTS Airport")
            self.cur.execute(self.sql_create_pilot)
            self.cur.execute(self.sql_create_airport)
            self.cur.execute(self.sql_create_flight)
            self.conn.commit()
            print("\nAll tables created successfully.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()
        self.insert_sample_data()

    def insert_sample_data(self):
        """
Populate all three tables with sample data

        12 pilots, 12 airports, 15 flights via executemany
        Timezones in UTC+/-X format
        """
        try:
            self.get_connection()

            pilots = [
                (1,  "James Carter",   "LIC001", "Captain",        4200),
                (2,  "Sarah Mitchell", "LIC002", "Captain",        3800),
                (3,  "David Nguyen",   "LIC003", "First Officer",  1500),
                (4,  "Emily Clarke",   "LIC004", "First Officer",  1200),
                (5,  "Robert Khan",    "LIC005", "Captain",        5100),
                (6,  "Laura Patel",    "LIC006", "Captain",        4700),
                (7,  "Michael Ross",   "LIC007", "First Officer",  900),
                (8,  "Anna Schmidt",   "LIC008", "Second Officer", 400),
                (9,  "Tom Bradley",    "LIC009", "Captain",        6200),
                (10, "Nina Okafor",    "LIC010", "First Officer",  1100),
                (11, "Carlos Rivera",  "LIC011", "Captain",        3300),
                (12, "Yuki Tanaka",    "LIC012", "Second Officer", 600),
            ]

            airports = [
                ("LHR", "Heathrow Airport",          "London",    "United Kingdom", "UTC+0"),
                ("JFK", "John F. Kennedy Airport",   "New York",  "United States",  "UTC-5"),
                ("DXB", "Dubai International",       "Dubai",     "UAE",            "UTC+4"),
                ("CDG", "Charles de Gaulle Airport", "Paris",     "France",         "UTC+1"),
                ("NRT", "Narita International",      "Tokyo",     "Japan",          "UTC+9"),
                ("SYD", "Kingsford Smith Airport",   "Sydney",    "Australia",      "UTC+11"),
                ("YYZ", "Pearson International",     "Toronto",   "Canada",         "UTC-5"),
                ("SIN", "Changi Airport",            "Singapore", "Singapore",      "UTC+8"),
                ("FRA", "Frankfurt Airport",         "Frankfurt", "Germany",        "UTC+1"),
                ("CPT", "Cape Town International",   "Cape Town", "South Africa",   "UTC+2"),
                ("BOM", "Chhatrapati Shivaji",       "Mumbai",    "India",          "UTC+5"),
                ("MAD", "Adolfo Suarez Airport",     "Madrid",    "Spain",          "UTC+1"),
            ]

            flights = [
                ("BA101", "2025-03-01 08:00", "2025-03-01 10:30", "Scheduled", "LHR", "JFK", 1),
                ("BA202", "2025-03-01 09:00", "2025-03-01 20:00", "Scheduled", "LHR", "DXB", 2),
                ("BA303", "2025-03-02 11:00", "2025-03-02 13:15", "Scheduled", "JFK", "CDG", 3),
                ("BA404", "2025-03-02 14:00", "2025-03-03 06:00", "Delayed",   "LHR", "NRT", 4),
                ("BA505", "2025-03-03 07:00", "2025-03-03 19:30", "Scheduled", "LHR", "SYD", 5),
                ("BA606", "2025-03-03 10:00", "2025-03-03 17:00", "Scheduled", "DXB", "YYZ", 6),
                ("BA707", "2025-03-04 06:00", "2025-03-04 22:00", "Scheduled", "LHR", "SIN", 7),
                ("BA808", "2025-03-04 08:30", "2025-03-04 11:00", "Cancelled", "CDG", "FRA", 8),
                ("BA909", "2025-03-05 12:00", "2025-03-06 04:00", "Scheduled", "LHR", "CPT", 9),
                ("BA110", "2025-03-05 15:00", "2025-03-06 07:00", "Scheduled", "LHR", "BOM", 10),
                ("BA211", "2025-03-06 09:00", "2025-03-06 11:30", "Scheduled", "FRA", "LHR", 11),
                ("BA312", "2025-03-06 13:00", "2025-03-06 16:00", "Delayed",   "MAD", "CDG", 12),
                ("BA413", "2025-03-07 07:00", "2025-03-07 18:30", "Scheduled", "LHR", "DXB", 1),
                ("BA514", "2025-03-07 10:00", "2025-03-07 21:00", "Scheduled", "LHR", "NRT", 2),
                ("BA615", "2025-03-08 08:00", "2025-03-08 20:00", "Scheduled", "JFK", "SIN", 3),
            ]

            self.cur.executemany(self.sql_insert_pilot, pilots)
            self.cur.executemany(self.sql_insert_airport, airports)
            self.cur.executemany(self.sql_insert_flight, flights)
            self.conn.commit()
            print("\nSample data inserted successfully.")
            print(f"  {len(pilots)} pilots, {len(airports)} airports, {len(flights)} flights added.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # ----------------------------------------------------------------
    # Flights
    # ----------------------------------------------------------------

    def select_all_flights(self):
        """
Show all flights

        Double JOIN on Airport (origin + destination) and JOIN on Pilot
        Shows names/cities instead of raw IDs
        """
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all_flights)
            results = self.cur.fetchall()
            if results:
                print(f"\n All Flights ({len(results)} records):")
                for row in results:
                    self.print_flight_row(row)
                print("-" * 50)
            else:
                print("No flights found.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def view_flights_by_criteria(self):
        """
Filter flights by origin, destination, status, or date

        Sub-menu with 5 options
        Origin/dest: pick from airport list
        Status: numbered choice 1/2/3
        Date: pick from list of existing dates
        """
        try:
            self.get_connection()
            print("\n Search by:")
            print("  1. Origin airport")
            print("  2. Destination airport")
            print("  3. Status")
            print("  4. Departure date")
            print("  5. Arrival date")
            choice = input("Enter choice: ")
            print()

            if choice == "1":
                self.cur.execute("SELECT AirportID, AirportName FROM Airport ORDER BY AirportID")
                airports = self.cur.fetchall()
                self.print_table(("ID", "Airport Name"), airports)
                airport_ids = {r[0] for r in airports}
                while True:
                    code = input("Enter Origin Airport ID: ").strip().upper()
                    if code in airport_ids:
                        break
                    print("  Invalid ID. Airport ID not recognised. Please enter a valid airport ID.")
                print()
                self.cur.execute(self.sql_flights_by_origin, (code,))

            elif choice == "2":
                self.cur.execute("SELECT AirportID, AirportName FROM Airport ORDER BY AirportID")
                airports = self.cur.fetchall()
                self.print_table(("ID", "Airport Name"), airports)
                airport_ids = {r[0] for r in airports}
                while True:
                    code = input("Enter Destination Airport ID: ").strip().upper()
                    if code in airport_ids:
                        break
                    print("  Invalid ID. Airport ID not recognised. Please enter a valid airport ID.")
                print()
                self.cur.execute(self.sql_flights_by_destination, (code,))

            elif choice == "3":
                print("  1. Scheduled")
                print("  2. Delayed")
                print("  3. Cancelled")
                status_map = {"1": "Scheduled", "2": "Delayed", "3": "Cancelled"}
                while True:
                    s = input("Enter choice (1/2/3): ").strip()
                    if s in status_map:
                        status = status_map[s]
                        break
                    print("  Invalid choice. Please enter 1, 2 or 3.")
                print()
                self.cur.execute(self.sql_flights_by_status, (status,))

            elif choice == "4":
                self.cur.execute(
                    "SELECT DISTINCT DATE(DepartureTime) FROM Flight ORDER BY DATE(DepartureTime)"
                )
                dep_dates = [r[0] for r in self.cur.fetchall()]
                if not dep_dates:
                    print("No departure dates found.")
                    return
                print("  Available departure dates:")
                for d in dep_dates:
                    print(f"    {d}")
                valid = set(dep_dates)
                while True:
                    date = input("Enter departure date (YYYY-MM-DD): ").strip()
                    if date in valid:
                        break
                    print("  Invalid date. Please choose from the list above.")
                print()
                self.cur.execute(self.sql_flights_by_date, (date,))

            elif choice == "5":
                self.cur.execute(
                    "SELECT DISTINCT DATE(ArrivalTime) FROM Flight ORDER BY DATE(ArrivalTime)"
                )
                arr_dates = [r[0] for r in self.cur.fetchall()]
                if not arr_dates:
                    print("No arrival dates found.")
                    return
                print("  Available arrival dates:")
                for d in arr_dates:
                    print(f"    {d}")
                valid = set(arr_dates)
                while True:
                    date = input("Enter arrival date (YYYY-MM-DD): ").strip()
                    if date in valid:
                        break
                    print("  Invalid date. Please choose from the list above.")
                print()
                self.cur.execute(self.sql_flights_by_arrival_date, (date,))

            else:
                print("Invalid choice.")
                return

            results = self.cur.fetchall()
            if results:
                print(f" {len(results)} flight(s) found:")
                for row in results:
                    self.print_flight_row(row)
                print("-" * 50)
            else:
                print("No flights found matching that criteria.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_flight(self):
        """
Find and show one flight by FlightID

        Double JOIN on Airport + Pilot for full details
        """
        try:
            self.get_connection()
            flight_id = self.pick_existing_flight_id("Enter Flight ID to search: ")
            print()
            self.cur.execute(self.sql_search_flight, (flight_id,))
            result = self.cur.fetchone()
            if result:
                print(" Flight found:")
                self.print_flight_row(result)
                print("-" * 50)
            else:
                print("No flight found with that ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def add_flight(self):
        """
Insert a new flight

        Collects fields in display order: ID, Origin, Dep, Dest, Arr, Pilot, Status
        Origin and destination validate against Airport table
        Times entered as local, stored as UTC
        """
        try:
            self.get_connection()
            flight = FlightInfo()
            # 1. Flight ID
            flight.set_flight_id(self.pick_new_flight_id())

            # 2. Origin
            print()
            flight.set_origin_airport_id(self.pick_existing_airport_id("Enter Origin Airport ID: "))
            self.cur.execute("SELECT Timezone FROM Airport WHERE AirportID = ?", (flight.get_origin_airport_id(),))
            origin_tz = self.cur.fetchone()[0]

            # 3. Departure (local time at origin)
            raw = input(f"Enter Departure Time as local time at {flight.get_origin_airport_id()} ({origin_tz}) (YYYY-MM-DD HH:MM) [default: 2026-06-10 13:00]: ").strip()
            if raw == "":
                raw = "2026-06-10 13:00"
                print(f"  No value entered, set to default value: {raw}")
            flight.set_departure_time(self.local_to_utc(raw, origin_tz))
            print(f"  Stored as UTC: {flight.get_departure_time()}")

            # 4. Destination
            print()
            flight.set_destination_airport_id(
                self.pick_existing_airport_id(
                    "Enter Destination Airport ID: ",
                    exclude=flight.get_origin_airport_id()
                )
            )
            self.cur.execute("SELECT Timezone FROM Airport WHERE AirportID = ?", (flight.get_destination_airport_id(),))
            dest_tz = self.cur.fetchone()[0]

            # 5. Arrival (local time at destination)
            raw = input(f"Enter Arrival Time as local time at {flight.get_destination_airport_id()} ({dest_tz}) (YYYY-MM-DD HH:MM) [default: 2026-06-10 14:00]: ").strip()
            if raw == "":
                raw = "2026-06-10 14:00"
                print(f"  No value entered, set to default value: {raw}")
            flight.set_arrival_time(self.local_to_utc(raw, dest_tz))
            print(f"  Stored as UTC: {flight.get_arrival_time()}")

            # 6. Pilot
            print()
            flight.set_pilot_id(self.pick_existing_pilot_id())

            # 7. Status
            print("  1. Scheduled")
            print("  2. Delayed")
            print("  3. Cancelled")
            status_map = {"1": "Scheduled", "2": "Delayed", "3": "Cancelled"}
            while True:
                s = input("Enter Status (1/2/3) [default: 1 — Scheduled]: ").strip()
                if s == "":
                    s = "1"
                    print("  No value entered, set to default value: Scheduled")
                if s in status_map:
                    flight.set_status(status_map[s])
                    break
                print("  Invalid choice. Please enter 1, 2 or 3.")
            print()

            self.cur.execute(self.sql_insert_flight, (
                flight.get_flight_id(),
                flight.get_departure_time(),
                flight.get_arrival_time(),
                flight.get_status(),
                flight.get_origin_airport_id(),
                flight.get_destination_airport_id(),
                flight.get_pilot_id()
            ))
            self.conn.commit()
            self.cur.execute(self.sql_search_flight, (flight.get_flight_id(),))
            result = self.cur.fetchone()
            print(" Flight added successfully:")
            if result:
                self.print_flight_row(result)
                print("-" * 50)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def update_flight(self):
        """
Update any field on an existing flight

        Displays current details first
        Sub-menu loops until user goes back
        Current value shown as default, Enter keeps it
        """
        try:
            self.get_connection()
            flight_id = self.pick_existing_flight_id("Enter Flight ID to update: ")
            if flight_id is None:
                return
            print()

            while True:
                # Fetch current flight state fresh each iteration
                self.cur.execute(self.sql_search_flight, (flight_id,))
                row = self.cur.fetchone()
                if not row:
                    print("Flight no longer found.")
                    return

                print(" Current flight details:")
                self.print_flight_row(row)
                print()

                # Derive current values for use as defaults
                origin_id  = row[4]
                dest_id    = row[6]
                self.cur.execute("SELECT Timezone FROM Airport WHERE AirportID = ?", (origin_id,))
                origin_tz = self.cur.fetchone()[0]
                self.cur.execute("SELECT Timezone FROM Airport WHERE AirportID = ?", (dest_id,))
                dest_tz = self.cur.fetchone()[0]
                current_utc_dep = row[1]
                current_utc_arr = row[2]
                current_local_dep = self.utc_to_local(current_utc_dep, origin_tz)
                current_local_arr = self.utc_to_local(current_utc_arr, dest_tz)

                print(" What would you like to change?")
                print("  1. Flight ID")
                print("  2. Origin airport")
                print("  3. Departure time")
                print("  4. Destination airport")
                print("  5. Arrival time")
                print("  6. Pilot")
                print("  7. Status")
                print("  8. Back to menu")
                choice = input("\nEnter choice: ").strip()
                print()

                if choice == "1":
                    current = row[0]
                    print(f"  Current Flight ID: {current}")
                    raw = input(f"  Enter new Flight ID [default: {current}]: ").strip().upper()
                    if raw == "":
                        print(f"  No value entered, kept as: {current}")
                    elif raw == current:
                        print(f"  No change made.")
                    else:
                        self.cur.execute("SELECT FlightID FROM Flight WHERE FlightID = ?", (raw,))
                        if self.cur.fetchone():
                            print(f"  {raw} is already in use. No change made.")
                        else:
                            self.cur.execute("UPDATE Flight SET FlightID = ? WHERE FlightID = ?", (raw, flight_id))
                            self.conn.commit()
                            flight_id = raw
                            print(f"  Flight ID updated to: {raw}")

                elif choice == "2":
                    print(f"  Current origin: {origin_id}")
                    new_origin = self.pick_existing_airport_id(
                        "  Enter new origin airport ID: ",
                        exclude=dest_id
                    )
                    print()
                    if new_origin == origin_id:
                        print("  No change made.")
                    else:
                        self.cur.execute("UPDATE Flight SET OriginAirportID = ? WHERE FlightID = ?", (new_origin, flight_id))
                        self.conn.commit()
                        print(f"  Origin updated to: {new_origin}")

                elif choice == "3":
                    print(f"  Current departure: {current_local_dep} local ({origin_tz}) [{current_utc_dep} UTC]")
                    raw = input(f"  Enter new departure as local time at {origin_id} ({origin_tz}) (YYYY-MM-DD HH:MM) [default: {current_local_dep}]: ").strip()
                    if raw == "":
                        raw = current_local_dep
                        print(f"  No value entered, kept as: {raw}")
                    new_utc = self.local_to_utc(raw, origin_tz)
                    self.cur.execute(self.sql_update_departure_time, (new_utc, flight_id))
                    self.conn.commit()
                    print(f"  Stored as UTC: {new_utc}")

                elif choice == "4":
                    print(f"  Current destination: {dest_id}")
                    new_dest = self.pick_existing_airport_id(
                        "  Enter new destination airport ID: ",
                        exclude=origin_id
                    )
                    print()
                    if new_dest == dest_id:
                        print("  No change made.")
                    else:
                        self.cur.execute("UPDATE Flight SET DestinationAirportID = ? WHERE FlightID = ?", (new_dest, flight_id))
                        self.conn.commit()
                        print(f"  Destination updated to: {new_dest}")

                elif choice == "5":
                    print(f"  Current arrival: {current_local_arr} local ({dest_tz}) [{current_utc_arr} UTC]")
                    raw = input(f"  Enter new arrival as local time at {dest_id} ({dest_tz}) (YYYY-MM-DD HH:MM) [default: {current_local_arr}]: ").strip()
                    if raw == "":
                        raw = current_local_arr
                        print(f"  No value entered, kept as: {raw}")
                    new_utc = self.local_to_utc(raw, dest_tz)
                    self.cur.execute("UPDATE Flight SET ArrivalTime = ? WHERE FlightID = ?", (new_utc, flight_id))
                    self.conn.commit()
                    print(f"  Stored as UTC: {new_utc}")

                elif choice == "6":
                    self.cur.execute("SELECT PilotID FROM Flight WHERE FlightID = ?", (flight_id,))
                    current_pilot_id = self.cur.fetchone()[0]
                    print(f"  Current pilot: {row[8]} (ID: {current_pilot_id})")
                    new_pilot = self.pick_existing_pilot_id()
                    print()
                    self.cur.execute(self.sql_assign_pilot, (new_pilot, flight_id))
                    self.conn.commit()
                    print(f"  Pilot updated.")

                elif choice == "7":
                    current = row[3]
                    print(f"  Current status: {current}")
                    print("  1. Scheduled")
                    print("  2. Delayed")
                    print("  3. Cancelled")
                    status_map = {"1": "Scheduled", "2": "Delayed", "3": "Cancelled"}
                    while True:
                        s = input("  Enter choice (1/2/3): ").strip()
                        if s in status_map:
                            new_status = status_map[s]
                            break
                        print("  Invalid choice. Please enter 1, 2 or 3.")
                    print()
                    self.cur.execute(self.sql_update_flight_status, (new_status, flight_id))
                    self.conn.commit()
                    print(f"  Status updated to: {new_status}")

                elif choice == "8":
                    return

                else:
                    print("  Invalid choice.")

                print()

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def delete_flight(self):
        """
Delete a flight by FlightID

        Asks for confirmation first
        rowcount used to confirm deletion
        """
        try:
            self.get_connection()
            flight_id = self.pick_existing_flight_id("Enter Flight ID to delete: ")
            confirm = input(f"\nAre you sure you want to delete Flight {flight_id}? (yes/no): ")
            print()
            if confirm.lower() == "yes":
                self.cur.execute(self.sql_delete_flight, (flight_id,))
                self.conn.commit()
                if self.cur.rowcount != 0:
                    print(f"{self.cur.rowcount} flight(s) deleted.")
                else:
                    print("No flight found with that ID.")
            else:
                print("Delete cancelled.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # ----------------------------------------------------------------
    # Pilots
    # ----------------------------------------------------------------

    def select_all_pilots(self):
        """
Show all pilots
        """
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all_pilots)
            results = self.cur.fetchall()
            if results:
                print(f"\n All Pilots ({len(results)} records):")
                for row in results:
                    print("-" * 50)
                    print(f"  Pilot ID      : {row[0]}")
                    print(f"  Name          : {row[1]}")
                    print(f"  Licence No    : {row[2]}")
                    print(f"  Rank          : {row[3]}")
                    print(f"  Flight Time   : {row[4]}")
                print("-" * 50)
            else:
                print("No pilots found.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def view_pilot_schedule(self):
        """
Show all flights for a given pilot

        Filters by PilotID, double JOIN on Airport
        Ordered by departure time
        """
        try:
            self.get_connection()
            pilot_id = self.pick_existing_pilot_id()
            print()
            self.cur.execute(self.sql_pilot_schedule, (pilot_id,))
            results = self.cur.fetchall()
            if results:
                print(f" Schedule for Pilot {pilot_id} ({len(results)} flight(s)):")
                for row in results:
                    print("-" * 50)
                    print(f"  Flight ID     : {row[0]}")
                    print(f"  Flight Number : {row[1]}")
                    origin_tz = row[8] if len(row) > 8 else "UTC+0"
                    dest_tz   = row[9] if len(row) > 9 else "UTC+0"
                    local_dep = self.utc_to_local(row[1], origin_tz)
                    local_arr = self.utc_to_local(row[2], dest_tz)
                    print(f"  Departure     : {local_dep} local ({origin_tz}) [{row[1]} UTC]")
                    print(f"  Arrival       : {local_arr} local ({dest_tz}) [{row[2]} UTC]")
                    print(f"  Status        : {row[3]}")
                    print(f"  Origin        : {row[5]} ({row[4]})")
                    print(f"  Destination   : {row[7]} ({row[6]})")
                print("-" * 50)
            else:
                print("No flights found for that pilot.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def add_pilot(self):
        """
Insert a new pilot

        PilotID validated as unique before insert
        New pilot displayed on success
        """
        try:
            self.get_connection()
            pilot = Pilot()
            pilot.set_pilot_id(self.pick_new_pilot_id())
            pilot.set_name(input("Enter pilot name: "))
            pilot.set_licence_number(input("Enter licence number: "))
            pilot.set_rank(input("Enter rank (Captain/First Officer/Second Officer): "))
            pilot.set_flight_time(int(input("Enter flight time (hours): ")))
            print()

            self.cur.execute(self.sql_insert_pilot, (
                pilot.get_pilot_id(),
                pilot.get_name(),
                pilot.get_licence_number(),
                pilot.get_rank(),
                pilot.get_flight_time()
            ))
            self.conn.commit()
            print(" Pilot added successfully:")
            print("-" * 50)
            print(f"  Pilot ID      : {pilot.get_pilot_id()}")
            print(f"  Name          : {pilot.get_name()}")
            print(f"  Licence No    : {pilot.get_licence_number()}")
            print(f"  Rank          : {pilot.get_rank()}")
            print(f"  Flight Time   : {pilot.get_flight_time()}")
            print("-" * 50)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def assign_pilot(self):
        """
Assign a pilot to a flight

        Updates PilotID FK in Flight
        Both flight and pilot validated before update
        """
        try:
            self.get_connection()
            flight_id = self.pick_existing_flight_id("Enter Flight ID: ")
            print()
            pilot_id = self.pick_existing_pilot_id()
            print()
            self.cur.execute(self.sql_assign_pilot, (pilot_id, flight_id))
            self.conn.commit()
            if self.cur.rowcount != 0:
                self.cur.execute(self.sql_search_flight, (flight_id,))
                result = self.cur.fetchone()
                print(" Flight information updated:")
                if result:
                    self.print_flight_row(result)
                    print("-" * 60)
            else:
                print("No flight found with that ID.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def summary_flights_by_pilot(self):
        """
Flight count grouped by pilot

        LEFT JOIN so pilots with no flights still show
        Ordered by total DESC
        """
        try:
            self.get_connection()
            self.cur.execute(self.sql_flights_by_pilot)
            results = self.cur.fetchall()
            print("\n Flights per pilot:")
            print("-" * 50)
            print(f"  {'ID':<5} {'Name':<20} {'Rank':<18} {'Total Flights'}")
            print("-" * 50)
            for row in results:
                print(f"  {row[0]:<5} {row[1]:<20} {row[2]:<18} {row[3]}")
            print("-" * 50)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # ----------------------------------------------------------------
    # Airports
    # ----------------------------------------------------------------

    def select_all_airports(self):
        """
Show all airports
        """
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all_airports)
            results = self.cur.fetchall()
            if results:
                print(f"\n All Airports ({len(results)} records):")
                for row in results:
                    print("-" * 50)
                    print(f"  Airport ID   : {row[0]}")
                    print(f"  Airport Name : {row[1]}")
                    print(f"  City         : {row[2]}")
                    print(f"  Country      : {row[3]}")
                    print(f"  Timezone     : {row[4]}")
                print("-" * 50)
            else:
                print("No airports found.")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def print_airport_row(self, row):
        """
Print one airport record

        Expects row from Airport SELECT
        Column order: AirportID, AirportName, City, Country, Timezone
        """
        print("-" * 50)
        print(f"  Airport ID   : {row[0]}")
        print(f"  Airport Name : {row[1]}")
        print(f"  City         : {row[2]}")
        print(f"  Country      : {row[3]}")
        print(f"  Timezone     : {row[4]}")
        print("-" * 50)

    def parse_timezone_input(self, prompt, default=None):
        """
Ask for a UTC offset int and return formatted timezone string

        User enters int, e.g. 1 -> UTC+1, -5 -> UTC-5
        Enter keeps default if provided

        Parameters:
            prompt  -- prompt string
            default -- value to keep on blank input
        """
        while True:
            raw = input(prompt).strip()
            if raw == "" and default is not None:
                print(f"  No value entered, kept as: {default}")
                return default
            try:
                offset = int(raw)
                tz = f"UTC+{offset}" if offset >= 0 else f"UTC{offset}"
                return tz
            except ValueError:
                print("  Invalid input. Please enter a whole number (e.g. 1, -5, 0).")

    def view_update_airport_information(self):
        """
View and update any field on an existing airport

        Display details first, then sub-menu loops until back
        Current value is default, Enter keeps it
        ID rename propagated to Flight FK columns
        """
        try:
            self.get_connection()
            airport_id = self.pick_existing_airport_id("Enter Airport ID: ")
            if airport_id is None:
                return
            print()

            while True:
                self.cur.execute("SELECT * FROM Airport WHERE AirportID = ?", (airport_id,))
                row = self.cur.fetchone()
                if not row:
                    print("Airport no longer found.")
                    return

                print(" Current airport details:")
                self.print_airport_row(row)
                print()

                print(" What would you like to change?")
                print("  1. Airport ID")
                print("  2. Airport Name")
                print("  3. City")
                print("  4. Country")
                print("  5. Timezone")
                print("  6. Back to menu")
                choice = input("\nEnter choice: ").strip()
                print()

                if choice == "1":
                    current = row[0]
                    print(f"  Current Airport ID: {current}")
                    while True:
                        raw = input(f"  Enter new Airport ID (3 letters) [default: {current}]: ").strip().upper()
                        if raw == "":
                            print(f"  No value entered, kept as: {current}")
                            break
                        if len(raw) != 3 or not raw.isalpha():
                            print("  Airport ID must be exactly 3 letters.")
                            continue
                        if raw == current:
                            print("  No change made.")
                            break
                        self.cur.execute("SELECT AirportID FROM Airport WHERE AirportID = ?", (raw,))
                        if self.cur.fetchone():
                            print(f"  {raw} is already in use. Please choose a different one.")
                            continue
                        # Update Airport table and propagate FK to Flight
                        self.cur.execute("UPDATE Airport SET AirportID = ? WHERE AirportID = ?", (raw, airport_id))
                        self.cur.execute("UPDATE Flight SET OriginAirportID = ? WHERE OriginAirportID = ?", (raw, airport_id))
                        self.cur.execute("UPDATE Flight SET DestinationAirportID = ? WHERE DestinationAirportID = ?", (raw, airport_id))
                        self.conn.commit()
                        airport_id = raw
                        print(f"  Airport ID updated to: {raw}")
                        break

                elif choice == "2":
                    current = row[1]
                    print(f"  Current Airport Name: {current}")
                    raw = input(f"  Enter new airport name [default: {current}]: ").strip()
                    if raw == "":
                        print(f"  No value entered, kept as: {current}")
                    else:
                        self.cur.execute("UPDATE Airport SET AirportName = ? WHERE AirportID = ?", (raw, airport_id))
                        self.conn.commit()
                        print(f"  Airport Name updated to: {raw}")

                elif choice == "3":
                    current = row[2]
                    print(f"  Current City: {current}")
                    raw = input(f"  Enter new city [default: {current}]: ").strip()
                    if raw == "":
                        print(f"  No value entered, kept as: {current}")
                    else:
                        self.cur.execute("UPDATE Airport SET City = ? WHERE AirportID = ?", (raw, airport_id))
                        self.conn.commit()
                        print(f"  City updated to: {raw}")

                elif choice == "4":
                    current = row[3]
                    print(f"  Current Country: {current}")
                    raw = input(f"  Enter new country [default: {current}]: ").strip()
                    if raw == "":
                        print(f"  No value entered, kept as: {current}")
                    else:
                        self.cur.execute("UPDATE Airport SET Country = ? WHERE AirportID = ?", (raw, airport_id))
                        self.conn.commit()
                        print(f"  Country updated to: {raw}")

                elif choice == "5":
                    current = row[4]
                    print(f"  Current Timezone: {current}")
                    print("  Enter the UTC offset as a whole number (e.g. 1 for UTC+1, -5 for UTC-5, 0 for UTC+0).")
                    new_tz = self.parse_timezone_input(f"  Enter new UTC offset [press Enter to keep {current}]: ", default=current)
                    if new_tz != current:
                        self.cur.execute(self.sql_update_airport_timezone, (new_tz, airport_id))
                        self.conn.commit()
                        print(f"  Timezone updated to: {new_tz}")

                elif choice == "6":
                    return

                else:
                    print("  Invalid choice.")

                print()

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def add_airport(self):
        """
Insert a new airport

        AirportID must be 3 letters, unique
        New airport displayed on success
        """
        try:
            self.get_connection()
            airport = Airport()
            airport.set_airport_id(self.pick_new_airport_id())
            airport.set_airport_name(input("Enter full airport name: "))
            airport.set_city(input("Enter city name: "))
            airport.set_country(input("Enter country name: "))
            raw = input("Enter timezone (e.g. UTC+1) [default: UTC+0]: ").strip()
            if raw == "":
                raw = "UTC+0"
                print(f"  No value entered, set to default value: {raw}")
            airport.set_timezone(raw)
            print()

            self.cur.execute(self.sql_insert_airport, (
                airport.get_airport_id(),
                airport.get_airport_name(),
                airport.get_city(),
                airport.get_country(),
                airport.get_timezone()
            ))
            self.conn.commit()
            print(" Airport added successfully:")
            print("-" * 50)
            print(f"  Airport ID   : {airport.get_airport_id()}")
            print(f"  Airport Name : {airport.get_airport_name()}")
            print(f"  City         : {airport.get_city()}")
            print(f"  Country      : {airport.get_country()}")
            print(f"  Timezone     : {airport.get_timezone()}")
            print("-" * 50)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def summary_flights_by_airport(self):
        """
Incoming flight count grouped by airport

        LEFT JOIN so airports with no flights still show
        Ordered by total DESC
        """
        try:
            self.get_connection()
            self.cur.execute(self.sql_flights_by_airport)
            results = self.cur.fetchall()
            print("\n Flights per airport (as destination):")
            print("-" * 50)
            print(f"  {'Code':<6} {'City':<20} {'Total Flights'}")
            print("-" * 50)
            for row in results:
                print(f"  {row[0]:<6} {row[1]:<20} {row[2]}")
            print("-" * 50)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()