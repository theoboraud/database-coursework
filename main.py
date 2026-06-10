from db_operations import DBOperations


def print_menu():
    """
Main menu, grouped by section

    Numbers are unique across the whole menu
    Section headers are visual only
    """
    print("\n ================================")
    print("   Flight Management System")
    print(" ================================")
    print()
    print("  --- Flights ---")
    print("  1.  View all flights")
    print("  2.  View flights by criteria")
    print("  3.  Search flight by ID")
    print("  4.  Add a new flight")
    print("  5.  Update flight information")
    print("  6.  Delete a flight")
    print()
    print("  --- Pilots ---")
    print("  7.  View all pilots")
    print("  8.  View pilot schedule")
    print("  9.  Add a pilot")
    print("  10. Assign pilot to flight")
    print("  11. Flights per pilot")
    print()
    print("  --- Airports ---")
    print("  12. View all airports")
    print("  13. View / update airport information")
    print("  14. Add an airport")
    print("  15. Flights per airport")
    print()
    print("  --- Initialisation ---")
    print("  16. Set up tables")
    print()
    print("  0.  Exit")
    print()


def handle_input(choice, db_ops):
    """
Route menu choice to the right DBOperations method

    Returns False on exit (0), True otherwise to keep the loop going

    Parameters:
        choice  -- integer entered by the user
        db_ops  -- DBOperations instance to call methods on
    """
    dispatch = {
        1:  db_ops.select_all_flights,
        2:  db_ops.view_flights_by_criteria,
        3:  db_ops.search_flight,
        4:  db_ops.add_flight,
        5:  db_ops.update_flight,
        6:  db_ops.delete_flight,
        7:  db_ops.select_all_pilots,
        8:  db_ops.view_pilot_schedule,
        9:  db_ops.add_pilot,
        10: db_ops.assign_pilot,
        11: db_ops.summary_flights_by_pilot,
        12: db_ops.select_all_airports,
        13: db_ops.view_update_airport_information,
        14: db_ops.add_airport,
        15: db_ops.summary_flights_by_airport,
        16: db_ops.create_tables,
    }

    if choice == 0:
        print("  Exiting...")
        return False
    elif choice in dispatch:
        dispatch[choice]()
    else:
        print("  Invalid choice. Please try again.")

    return True


# Entry point — runs until the user exits
while True:
    print_menu()
    try:
        choice = int(input("  Enter your choice: "))
        print()
    except ValueError:
        print("  Please enter a number.")
        continue
    db_ops = DBOperations()
    if not handle_input(choice, db_ops):
        break