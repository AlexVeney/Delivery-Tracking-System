from datetime import time, datetime
import copy


class Helper:

    clock = datetime.now()
    status_log = []

    # Big O Notation -> Constant O(1)
    @staticmethod
    def display_menu(route_started):
        """
        Display menu to user, prompt for input and display messages to guide user input
            Checks for invalid menu_selection input from user
        """

        menu_selection = input("\n******************************************"
                               "\nWGUPS DLD Menu\n"
                               "1 : Start delivery route\n"
                               "2 : Get status of package by package id\n"
                               "3 : Get status of packages at specific time\n"
                               "4 : Get status of all packages\n"
                               "5 : End delivery route\n"
                               "******************************************\n"
                               "Enter menu selection: ")

        return menu_selection

    # Big O Notation -> Linear O(N)
    @staticmethod
    def get_status_of_all_packages(packages):
        """
        Displays status of all packages after delivery route completes
            For loop iterates over Hash table that holds packages to retrieve package - get_from_table()
            The package's corresponding data elements are displayed to console - Helper.display_package_details()
        """
        print("\n******************************************")
        for i in range(len(packages.table)):
            package_num = i + 1
            package = packages.get_from_table(package_num)
            Helper.display_package_details(package)

    # Big O Notation -> Constant O(1)
    @staticmethod
    def get_package_status(packages):
        """
        Displays status of single package to console
            User is prompted to enter package id
            Package is retrieved from package hash table - get_from_table()
            The package's corresponding data elements are displayed to console - Helper.display_package_details()
        """
        package_id = input("Enter package ID: ")
        package = packages.get_from_table(package_id)
        Helper.display_package_details(package)

    # Big O Notation -> Linear O(N)
    @staticmethod
    def add_to_status_log(time1, packages):
        """
        Snapshot of package hash table is added to status-log list
            A snapshot(deepcopy) of the package hash table is created at 'time1'(datetime) during program execution
            (time1: snapshot) tuple is added to status-log list
        """
        snapshot = copy.deepcopy(packages.table)
        tuple1 = (time1, snapshot)
        Helper.status_log.append(tuple1)

    # Big O Notation -> Linear O(N)
    @staticmethod
    def get_status_based_on_time():
        """
        Get and display status of all packages to console based on time
            Prompts and retrieves input from user that is used to retrieve snapshot of package hash table
            Proper status-log is retrieved from Helper.status_log - Helper.find_log()
            Package data elements from all packages are displayed to console - Helper.display_package_details()
        """
        entered_time = input("Enter time in format HH:MM:SS :")
        # find log based on time
        log = Helper.find_log(entered_time)

        print("\n******************************************")
        for i in range(len(log)):
            Helper.display_package_details(log[i][1])

    # Big O Notation -> Linear O(N)
    @staticmethod
    def find_log(user_input):
        """
        Find log that contains up to date package statuses based on user_input (datetime)
            Splits user_input(string) into hour minute and second to create a datetime object representing the entered time
            Iterates through status_log list comparing entered time to status_log timestamp
            Retrieves and returns log
        """
        hour, minute, second = user_input.split(':')
        status_clock = Helper.clock.replace(hour=int(hour), minute=int(minute), second=int(second))
        for i in range(len(Helper.status_log)):
            last_log_index = len(Helper.status_log) - 1
            if i == last_log_index:
                return Helper.status_log[i][1]
            elif status_clock >= Helper.status_log[i][0] and status_clock < Helper.status_log[i+1][0]:
                return Helper.status_log[i][1]

    # Big O Notation -> Constant O(1)
    # Display package data elements to console
    @staticmethod
    def display_package_details(package):
        print("\n**** Package " + str(package.ID) + " ****")
        print(" ID: " + str(package.ID) + " ADDRESS: " + package.address +
              " " + package.city + " " + package.state + "  " + package.zip + " DEADLINE: " +
              package.delivery_deadline + " WEIGHT:  " + package.weight + " STATUS:  " + package.delivery_status)

        if package.delivery_status == "Delivered":
            print(" DELIVERY TIME: " + package.actual_delivery_time)

    # Big O Notation -> Constant O(1)
    # Determine delivery route end-time based on latest truck time
    @staticmethod
    def determine_current_time(time1, time2):
        if time1 > time2:
            return time1
        else:
            return time2
