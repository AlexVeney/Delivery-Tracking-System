# Alexandra Veney
import csv
from datetime import time, datetime
from Hash import Hash
from Helper import Helper
from Truck import Truck

NUM_OF_PACKAGES = 40

route_started = False


packages = Hash(NUM_OF_PACKAGES)    # hash object to store packages

packages.create_package_list("Package File.csv")    # create package list from package file

# Big O Notation -> Linear O(N)
with open("Distance Table.csv") as d_file:
    """
    Read in delivery addresses and travel distances from csv files ('Package File' and 'Distance Table')

        Utilizes csv class to read first line from Distance Table which contains the addresses
        Address and location code info stored in dict {location code:street address)
        Distance info stored in tuple  (location, row of distances)
    """
    reader = csv.reader(d_file, delimiter=',')

    # holds row of addresses from file
    addresses = next(reader)

    # get street addresses
    address_street = dict()
    for i in range(len(addresses)):
        address_street.update({addresses[i]: i})

    # get distance between addresses
    address_distance = list()
    for row in reader:
        address_distance.insert(reader.line_num, row)


# Big O Notation -> Polynomial O(N^4)
menu_selection = "0"
while menu_selection != "5":
    """
    Display menu options until user chooses to end program
        While loop runs until user selects quit option (menu_selection = 5)
               "1 : Start delivery route" - Deliver packages, displays deliveries as they occur
               "2 : Get status of package by package id" - Get and displays status of single package
               "3 : Get status of packages at specific time" - Get and displays status of packages at a specific time
               "4 : Get status of all packages" - Get and displays status of all packages after delivery route completion
               "5 : End delivery route"
        Helper functions from the Helper class provide the logic for each menu_selection
        Truck loads (lists) manually created to efficiently load truck while taking into account special instructions
        All truck loads are stored in a 2D list for each retrieval within start_delivery_route()
        Helper.clock datetime initialized to beginning of day 08:00:00
        Delivery of all packages orchestrated - Truck.start_delivery_route()
    """
    menu_selection = Helper.display_menu(route_started)

    # delivery route starts if user selects 1 and the route has not started yet
    if menu_selection == "1" and not route_started:
        route_started = True
        print("\n[Delivery Route Started]")

        truck1 = Truck(1, "Driver 1")
        truck2 = Truck(2, "Driver 2")

        # Assign packages to truck for each visit to hub
        truck1_first_load = [4, 13, 14, 15, 16, 17, 19, 20, 21, 34, 39, 40]
        truck2_first_load = [1, 2, 3, 5, 7, 8, 18, 22, 27, 29, 30, 33, 35, 36, 37, 38]
        truck1_second_load = [6, 10, 11, 12, 25, 26, 28, 31, 32]
        truck2_second_load = [9, 23, 24]

        # Consolidate lists
        loading_sequence = [[truck1_first_load, truck1_second_load], [truck2_first_load, truck2_second_load]]

        # Number of loading seqs for truck 1
        num_truckloads_truck1 = len(loading_sequence[0])

        # Number of loading seqs for truck 2
        num_truckloads_truck2 = len(loading_sequence[1])

        # initialize clock to keep current time
        Helper.clock = datetime.now()
        Helper.clock = Helper.clock.replace(hour=8, minute=0, second=0)

        # set truck clock to current time
        truck1.clock = Helper.clock
        truck2.clock = Helper.clock

        # O(2^N)
        # begin deliver route for the day
        Truck.start_delivery_route(truck1, num_truckloads_truck1, truck2, num_truckloads_truck2, packages,
                                   loading_sequence, address_street, address_distance)

        #  display each truck's mileage, route total mileage and route completion time
        print("\nTruck 1s mileage: " + str(truck1.miles_traveled))
        print("\nTruck 2s mileage: " + str(truck2.miles_traveled))
        print("\nTotal miles traveled: " + str(truck1.miles_traveled + truck2.miles_traveled))
        Helper.clock = Helper.determine_current_time(truck1.clock, truck2.clock)
        print("Delivery route end time: " + str(Helper.clock.strftime("%-I:%M:%S")))

    elif menu_selection == "1" and route_started:
        print("\n[ * Route already started, to get status select menu option 2, 3 or 4 * ]\n")

    elif menu_selection == "2":
        # Get status based on package ID
        Helper.get_package_status(packages)

    elif menu_selection == "3":
        # Get status on packages based on time
        Helper.get_status_based_on_time()

    elif menu_selection == "4":
        # Get status on all packages after delivery completion
        Helper.get_status_of_all_packages(packages)

    elif menu_selection != "5":
        print("\n[ X : Invalid Menu Selection]")

print("\n[Delivery Route Program Ended]")


