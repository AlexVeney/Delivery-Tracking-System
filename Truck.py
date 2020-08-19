from datetime import datetime, timedelta
from Helper import Helper


class Truck:
    PACKAGE_CAPACITY = 16
    TRAVEL_SPEED = 18
    delivery_log = []

    def __init__(self, truck_number, driver):
        self.truck_number = truck_number
        self.packages_on_truck = []
        self.num_of_packages = 0
        self.miles_traveled = 0.0
        self.driver = driver
        self.current_location = 0   # truck starts at hub (location 0)
        self.clock = datetime.now()

    # Big O Notation -> Linear O(N)
    def load_truck_at_hub(self, packages_at_hub, packages_to_load):
        """
            Load all packages in truck's current loading sequence to truck
                Each package is loaded using the package id list (packages_to_load) and the package hash table (packages_at_hub)
                Package id is used to retrieve package object
                Special instruction: Package 9's address is corrected at 10:20 so it does not leave the hub until then
                    Truck's clock is changed to 10:20 during second loading sequence to simulate time change
                    Package 9's data elements are modified to reflect new address
                Truck's status is displayed to console along with current time
        """
        for i in range(len(packages_to_load)):
            package_number = str(packages_to_load[i])
            package = packages_at_hub.get_from_table(package_number)

            if package_number == "9":
                # set clock to 10:20 am
                self.clock = self.clock.replace(hour=10, minute=20, second=0)
                package.address = "410 S State St"
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zip = "84111"
                print("\n*****Package 9 address corrected to: 410 S State St., Salt Lake City, UT 84111***** @ "
                      + str(self.clock.strftime("%-I:%M:%S")))

            self.load_package(package)

        print("\n[ Truck " + str(self.truck_number) + " ] left the hub @ " + str(self.clock.strftime("%-I:%M:%S")))

    # Big O Notation -> Constant O(1)
    def load_package(self, package):
        """
        Load single package onto truck
            Package delivery status modified to show it is loaded onto a truck (2 = 'In Transit')
            Checks to make sure # of packages on truck is lower than the truck capacity
            Package is NOT loaded if truck is full, user is notified by message displayed to console
            Number of packages on truck is incremented by 1
            Package is appended to Truck's packages_on_truck list
        """
        if package.delivery_status == "At the hub":
            package.set_delivery_status(2)
            if self.num_of_packages < Truck.PACKAGE_CAPACITY:
                self.packages_on_truck.append(package)
                self.num_of_packages += 1
                print("Package " + package.ID + " loaded onto [ Truck " + str(self.truck_number) + " ]")
            else:
                print("\n Truck " + str(self.truck_number) + " is full")
        else:
            print("\nPackage " + package.ID + " is in transit or already delivered")

    # Big O Notation -> Linear O(N)
    def deliver_package(self, package, address_street, address_distance, packages):
        """
            Deliver package, adjust the truck's time and mileage, and record package statuses
                Check package delivery status attribute to make sure it is 'In Transit"
                Remove package from truck's 'packages_on_truck' list and Decrement 'number_of_packages' on truck by 1
                Calculate the distance needed to travel to deliver package - calculate_travel_distance()
                Add distance needed to travel to truck's total mileage
                Calculate the time needed to travel distance - calculate_travel_time()
                Record deliver time by setting package.actual_delivery_time to current time
                Display package id, destination address, distance, travel time and truck num to console
                Change truck's location to the destination addresses's location code
                Update package's status to show its been delivered (3 = "Delivered")
                Add snapshot of the status of all packages to status_log - Helper.add_to_status_log()
        """
        # ensure package is not at the hub
        if package.delivery_status == "In transit":
            # remove package from truck
            self.packages_on_truck.remove(package)

            # decrease truck's package count
            self.num_of_packages -= 1

            # calculate travel distance
            distance = self.calculate_travel_distance(package.address, address_street, address_distance)

            # updates truck's total mileage
            self.miles_traveled = float('%.1f' % (self.miles_traveled + distance))

            # calculate travel time
            travel_time = self.calculate_travel_time(distance)

            # update trucks time to delivery time
            self.clock += timedelta(minutes=travel_time)

            # set package's delivery time
            package.actual_delivery_time = self.clock.strftime("%-I:%M:%S")

            print("\n\n DESTINATION: " + package.address +
                  " DISTANCE: " + str(distance) + " miles " +
                  " TRAVEL TIME: " + str(travel_time) + " minutes")

            print("Package " + package.ID + " delivered and unloaded from [ TRUCK " + str(self.truck_number) + " ] at "
                  + str(package.actual_delivery_time))

            # Change truck's current location
            self.current_location = address_street[package.address]

            # change package's delivery status to 'delivered'
            package.set_delivery_status(3)

            # set Helper.clock time
            Helper.clock = self.clock

            Helper.add_to_status_log(self.clock, packages)
        else:
            print("\n   Package " + package.ID + " is not on truck " + str(self.truck_number))

    # Big O Notation -> Constant O(1)
    def calculate_travel_distance(self, destination_address, address_street, address_distance):
        """
        Determine the travel distance from current location to desired destination
            Find the distance from current and destination location by retrieving distance from address_distance list
            Return distance (float)
        """
        # Current location number
        current_location = self.current_location

        # Destination location number
        destination_location = address_street[destination_address]

        # Exit if location is not found
        if destination_location is None:
            print("Error: Location is not found")
            SystemExit

        # Get distance from matrix
        if address_distance[current_location][destination_location] != '':
            distance = float(address_distance[current_location][destination_location])
        else:
            distance = float(address_distance[destination_location][current_location])

        return distance

    # Big O Notation -> Constant O(1)
    @staticmethod
    def calculate_travel_time(distance):
        """
            Determine the travel time based on distance from current location to destination location
                Obtain distance_per_min by dividing avg mph / 60 (minutes)
                Multiply the distance_per_min and distance to get travel time
                Return travel time (int)
        """
        distance_per_min = Truck.TRAVEL_SPEED / 60.0
        travel_time = int(distance / distance_per_min)

        return travel_time

    # Big O Notation -> Constant O(1)
    def return_to_hub(self, address_street, address_distance):
        """
        Return truck to the hub from last delivery address, add time and add mileage
            Use calculate_travel_distance(), calculate_travel_time() to record truck movement to hub
            Display truck's status to console
        """
        # Get distance from current location to hub
        hub_address = "4001 South 700 East"
        distance_to_hub = self.calculate_travel_distance(hub_address, address_street, address_distance)

        # set truck's current location to the hub
        self.current_location = 0

        # add travel distance to hub to truck's total mileage
        self.miles_traveled += distance_to_hub

        # add travel time to
        travel_time_to_hub = Truck.calculate_travel_time(distance_to_hub)

        # update trucks time
        self.clock += timedelta(minutes=travel_time_to_hub)

        print("\n[ Truck " + str(self.truck_number) + " ] returned to the hub @ " + str(self.clock.strftime("%-I:%M:%S")))

    # Big O Notation -> Cubic (N^3)
    @staticmethod
    def start_delivery_route(truck1, num_truckloads_truck1, truck2, num_truckloads_truck2, packages, loading_sequence,
                             address_street, address_distance):
        """
        Deliver packages in delivery route
            While loop attempts to deliver packages if num_of_remaining_truckloads > 0
            If truckloads remain for a truck, the loading sequence is used to load the packages in the truckload list
                - load_truck_at_hub()
            While loop delivers packages until both Truck1 and Truck2 have no packages
            If statement is used to check if one truck is empty. if so the other truck delivers the remaining packages
            Group of If statements decide which package should be delivered next using package_selection()
                (greedy algorithm) and referencing the truck's time
            Time is simulated by adding travel_time to a copy of each truck's time and determining
                which delivery occurs first. Only the delivery that occurs first is completed
            If statement following package deliveries checks to see if truck is empty, if so truck returns to hub
                - return_to_hub() , number_of_remaining_truckloads is decremented by 1 and truck loads for empty truck is
                decremented by 1
        """

        load_id_truck1 = 0
        load_id_truck2 = 0
        num_of_remaining_truckloads = num_truckloads_truck1 + num_truckloads_truck2

        # Block - 0(N^3)
        # loops through all truck loads at the hub
        while num_of_remaining_truckloads > 0:

            # O(N)
            # load truck1 and truck2 with appropriate loading seq
            if num_truckloads_truck1 > 0:
                truck1.load_truck_at_hub(packages, loading_sequence[0][load_id_truck1])
                load_id_truck1 += 1
            if num_truckloads_truck2 > 0:
                truck2.load_truck_at_hub(packages, loading_sequence[1][load_id_truck2])
                load_id_truck2 += 1

            # Block - O(N^2)
            # deliver the packages in loading sequence
            while truck1.num_of_packages > 0 or truck2.num_of_packages > 0:

                if truck1.num_of_packages == 0 and truck2.num_of_packages != 0:
                    next_package = truck2.package_selection(address_street, address_distance)
                    truck2.deliver_package(next_package, address_street, address_distance, packages)

                    if truck2.num_of_packages == 0:
                        truck2.return_to_hub(address_street, address_distance)

                elif truck2.num_of_packages == 0 and truck1.num_of_packages != 0:
                    next_package = truck1.package_selection(address_street, address_distance)
                    truck1.deliver_package(next_package, address_street, address_distance, packages)

                    if truck1.num_of_packages == 0:
                        truck1.return_to_hub(address_street, address_distance)
                else:
                    # O(N)
                    next_package_1 = truck1.package_selection(address_street, address_distance)
                    next_package_2 = truck2.package_selection(address_street, address_distance)

                    distance1 = truck1.calculate_travel_distance(next_package_1.address, address_street,
                                                                 address_distance)
                    distance2 = truck2.calculate_travel_distance(next_package_2.address, address_street,
                                                                 address_distance)

                    time1 = truck1.clock + timedelta(minutes=Truck.calculate_travel_time(distance1))
                    time2 = truck2.clock + timedelta(minutes=Truck.calculate_travel_time(distance2))

                    if time1 < time2:
                        truck1.deliver_package(next_package_1, address_street, address_distance, packages)
                        if truck1.num_of_packages == 0:
                            truck1.return_to_hub(address_street, address_distance)
                    elif time2 < time1:
                        truck2.deliver_package(next_package_2, address_street, address_distance, packages)
                        if truck2.num_of_packages == 0:
                            truck2.return_to_hub(address_street, address_distance)
                    else:
                        truck1.deliver_package(next_package_1, address_street, address_distance, packages)
                        if truck1.num_of_packages == 0:
                            truck1.return_to_hub(address_street, address_distance)

                        truck2.deliver_package(next_package_2, address_street, address_distance, packages)
                        if truck2.num_of_packages == 0:
                            truck2.return_to_hub(address_street, address_distance)

                # after delivery of all packages in truck's current load the num of remaining loads decrease
            if truck1.num_of_packages == 0:
                num_truckloads_truck1 -= 1
                num_of_remaining_truckloads -= 1

            if truck2.num_of_packages == 0:
                num_truckloads_truck2 -= 1
                num_of_remaining_truckloads -= 1

    # Big O Notation -> Linear O(N)
    def package_selection(self, address_street, address_distance):
        """
        Select package with shortest distance delivery distance
            Set 'remaining_packages' to a copy of the truck's current list for readability
            Set 'initial_distance' for comparison to the travel distance needed to deliver package at index 0 of
                'remaining_packages'
            'shortest_distance' by default is the same as the 'initial_distance' because no other distance has
                been compared
            For loop iterates through 'remaining_packages' list calculating travel distance for current package then
                comparing 'shortest_distance' to 'current_package_distance' - calculate_travel_distance()
            If 'current_package_distance' is less than the 'shortest_distance' the 'shortest distance' is set to
                'current_package_distance' and 'package_selected' is set to the current package
            Return the final 'package_selected'
        """
        if self.num_of_packages == 0:
            return None

        remaining_packages = self.packages_on_truck
        initial_distance = self.calculate_travel_distance(remaining_packages[0].address, address_street,
                                                          address_distance)
        shortest_distance = initial_distance
        package_selected = remaining_packages[0]
        for package in remaining_packages:
            current_package_distance = self.calculate_travel_distance(package.address, address_street, address_distance)

            if current_package_distance < shortest_distance:
                shortest_distance = current_package_distance
                package_selected = package

        return package_selected
























