# Christopher Brown 000968168

import sys
from distance import store_distance_table
from package import store_package_table
from truck import Truck
import datetime


# This is the first option for the user to choose from.
# Time Complexity, O(1)
def choice_1():
    print()
    print("Please select an option:")
    print("1 = Final Delivery Time")
    print("2 = Choose a your own time")
    print("3 = Results")
    print("4 = Quit")
    selection = input("Enter option: ")
    return selection

# After the user picks something from choice_1 they can select another option from this.
# Time Complexity, O(1)
def choice_2():
    print()
    print("Select an option:")
    print("1 = Print all packages")
    print("2 = Look up Package ID")
    print("3 = Select a new time")
    print("4 = Quit")
    selection = input("Enter Option: ")
    return selection


def main():

    # Tables are parsed for information and stored for use throughout the program.
    distance_dict, distances_list = store_distance_table('WGUPS Distance Table.csv')
    package_hash = store_package_table('WGUPS Package File.csv')

    # Trucks are created and assigned to variables. The trucks leave at staggered times to account for delays.
    # Time Complexity O(1), Space Complexity O(1)
    a = Truck("1")
    b = Truck("2", 9, 5, 0)
    c = Truck("3", 10, 20, 0)

    # Corrects the package with the wrong address. The address changes happens at 10:20 so I set it to "arrive" at 10:20
    # Time Complexity O(1), Space Complexity O(1)
    updated_package = package_hash.get(9)
    updated_package[0] = 'Arriving at 10:20 AM'
    updated_package[3] = '410 S State St'
    updated_package[4] = 'Salt Lake City'
    updated_package[5] = 'UT'
    updated_package[6] = '84111'
    updated_package[9] = 'Wrong address. Update at 10:20 AM'
    package_hash.add(9, updated_package)

    # Sorts and loads all of the packages on each truck.
    a.order_and_load(package_hash, distance_dict, distances_list)
    b.order_and_load(package_hash, distance_dict, distances_list)
    c.order_and_load(package_hash, distance_dict, distances_list)

    # True returns the truck back to the hub after delivering all of the packages. A is returned so the driver can
    # get on Truck C and deliver the remaining packages.
    a.deliver(package_hash, distance_dict, distances_list, True)
    b.deliver(package_hash, distance_dict, distances_list)
    c.deliver(package_hash, distance_dict, distances_list)

    # User interface. This section allows the user to look up packages at any time. If they select final they see the
    # packages at their final state. They can also input their own time to see package status's at a custom time.
    # Results displays the final mileage and final time for they delivery system.
    # Time Complexity, the while loop is infinite (goes until a user hits 4), so Big O can not be analyzed.
    print("Welcome to WGUPS Delivery System")

    selection_1 = None
    selection_2 = None
    while selection_1 is not "4" and selection_2 is not "4":
        selection_1 = choice_1()
        if selection_1 is "1":
            selection_2 = choice_2()
            if selection_2 is "1":
                package_hash.lookup_all_final()
            elif selection_2 is "2":
                id_num = int(input("Enter Package ID number: "))
                if 1 <= id_num <= 40:
                    package_hash.lookup_single_final(id_num)
                else:
                    print("Invalid Package ID... Try again...")
            elif selection_2 is "3":
                print("Choose a new time")
            elif selection_2 is "4":
                sys.exit(0)
            else:
                print("Invalid value, try again")
        elif selection_1 is "2":
            print()
            hour = int(input('Enter a hour in 24 hour format. Ex) 13 = 1PM '))
            minute = int(input('Enter a minute '))
            second = int(input('Enter a second '))
            user_time = datetime.time(hour, minute, second)
            selection_2 = choice_2()
            if selection_2 is "1":
                package_hash.lookup_all_time(user_time)
            elif selection_2 is "2":
                id_num = int(input("Enter Package ID number: "))
                if 1 <= id_num <= 40:
                    package_hash.lookup_single_time(id_num, user_time)
                else:
                    print("Invalid Package ID... Try again...")
            elif selection_2 is "3":
                print("Choose a new time")
            elif selection_2 is "4":
                sys.exit(0)
            else:
                print("Invalid value, try again")
        elif selection_1 is "3":
            print()
            print("----1----")
            a_total_time = a.time.end_time - a.time.start_time
            a_total_miles = (a_total_time.total_seconds() / 3600) * a.speed
            print("Truck 1 ", a_total_miles, "Miles Total")
            print("Start =", a.time.start_time.strftime("%H:%M:%S %p"))
            print("End =", a.time.end_time.strftime("%H:%M:%S %p"))
            print("Total = ", a_total_time)

            print("----2----")
            b_total_time = b.time.end_time - b.time.start_time
            b_total_miles = (b_total_time.total_seconds() / 3600) * b.speed
            print("Truck 2 ", b_total_miles, "Miles Total")
            print("Start =", b.time.start_time.strftime("%H:%M:%S %p"))
            print("End =", b.time.end_time.strftime("%H:%M:%S %p"))
            print("Total = ", b_total_time)

            print("----3----")
            c_total_time = c.time.end_time - c.time.start_time
            c_total_miles = (c_total_time.total_seconds() / 3600) * c.speed
            print("Truck 3 ", c_total_miles, "Miles Total")
            print("Start =", c.time.start_time.strftime("%H:%M:%S %p"))
            print("End =", c.time.end_time.strftime("%H:%M:%S %p"))
            print("Total = ", c_total_time)

            total_miles = a_total_miles + b_total_miles + c_total_miles
            final_times = a.time.end_time, b.time.end_time, c.time.end_time
            last_delivery = max(final_times).strftime("%H:%M:%S %p")

            print("----FINAL RESULTS----")
            print("Final Miles = ", total_miles)
            print("Last Delivery = ", last_delivery)

        elif selection_1 is "4":
            sys.exit(0)
        else:
            print("Invalid value entered. Try again...")


# if the file is being executed, main is called.
if __name__ == "__main__":
    main()
