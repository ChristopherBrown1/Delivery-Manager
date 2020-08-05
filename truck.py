# Christopher Brown 000968168


import re
from datetime import datetime, date
from distance import distance_between, shortest_distance, shortest_early_distance, shortest_loaded
from time_class import Time

# Number of trucks that leave at the start time, 8AM.
early_trucks = 0


# truck class. Trucks can drive at 18 mph, they can hold a certain number 16 packages at a time.
class Truck:
    speed = 18.0

    # Initializes the truck class. The truck can carry 16 packages at a time and its starting location is the hub. Each
    # truck has its own package list that it will add and remove packages from when loaded and delivered.
    # Time Complexity O(1), Space Complexity O(1)
    def __init__(self, name, hours=None, mins=None, seconds=None):
        self.name = name
        self.capacity = 16
        self.location = 'HUB'
        self.loaded_package_list = []

        # Truck will start loading and delivery at a custom time if the optional parameters are given. If no optional
        # parameters are given then the truck starts at the start time of 8AM.
        # Time Complexity O(1), Space Complexity O(1)
        if hours is not None and mins is not None and seconds is not None:
            today = date.today()
            truck_start_time = datetime(today.year, today.month, today.day, hours, mins, seconds)
            self.time = Time(truck_start_time)
        else:
            global early_trucks
            early_trucks += 1
            self.time = Time()

    # Delivers the packages that have been loaded onto the truck. It pops off the first package from the list of loaded
    # packages and then updates the address. The time is advanced after each delivery and the delivery time is updated.
    # If the final parameter is true the truck will return to the hub and add the travel time for the truck.
    # Time Complexity O(n), Space Complexity O(1)
    def deliver(self, package_hash, distance_dict, distances_list, truck_to_hub=False):
        if self.loaded_package_list:
            # Capacity is a constant number of 16 so the while loop counts as O(1)
            while self.loaded_package_list:
                address1 = self.location
                if self.location == 'HUB':
                    address1 = ' ' + self.location

                package_id = self.loaded_package_list.pop(0)
                address2 = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
                hours = float(distance_between(address1, address2, distance_dict, distances_list)) / self.speed
                current_time = self.time.advance_time(self.time.current_time, hours, 0, 0)
                value = package_hash.get(package_id)
                value[0] = 'Finished'
                value[2] = 'Delivered at ' + current_time.strftime("%H:%M:%S")
                package_hash.add(package_id, value)
                self.location = address2
                self.time.end_time = current_time

        if truck_to_hub is True:
            address1 = self.location
            address2 = ' HUB'
            hours = float(distance_between(address1, address2, distance_dict, distances_list)) / self.speed
            current_time = self.time.advance_time(self.time.current_time, hours, 0, 0)
            self.location = address2
            self.time.end_time = current_time

        return hours

    # Loads a single package, given the package, id onto the truck and updates the Route start time. 1 is subtracted
    # from the capacity of the truck.
    # Time Complexity O(N), Space Complexity O(1)
    def load(self, package_id, package_hash):
        address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
        self.loaded_package_list.append(package_id)
        value = package_hash.get(package_id)
        value[1] = 'On Truck ' + self.name + ' at ' + self.time.start_time.strftime("%H:%M:%S")
        package_hash.add(package_id, value)
        current_location = address
        self.capacity -= 1
        return current_location

    # Any delayed packages will not be at the hub until arrival time. If the time of the truck is >= the arrival time of
    # the package, the truck can load the package because the package is at the hub. This updates the list of packages
    # available for loading.
    # Time Complexity O(n^2), Space Complexity O(1)
    def _update_packages_at_hub(self, package_hash):
        for package in package_hash.map:
            package_id = package[0][0]
            at_hub = package_hash.get(package_id)[0]
            if at_hub != 'At Hub':
                # findall would be a constant O(1)
                arv_time = re.findall(r'\d{1,2}:\d{2}\s\w{2}', at_hub)
                format = '%I:%M %p'
                arv_time = datetime.strptime(arv_time[0], format).time()
                if self.time.current_time.time() >= arv_time:
                    package[0][1][0] = 'At Hub'

    # Orders the package list closest to farthest then, when called, the delivery function will pop off the packages
    # in order of closest first, Greedy Algorithm. The order and load function goes through several steps to load
    # packages according to the given times and conditions in their notes. These steps are documented below.
    # Time Complexity O(n^2), Space Complexity O(n)
    def order_and_load(self, package_hash, distance_dict, distances_list):
        # If the truck is not at the hub it can not be loaded for delivery.
        if self.location == 'HUB':
            current_location = ' HUB'
            group = False

            # Scans for packages at hub. If a package is delayed it will not be available until time given in note.1
            self._update_packages_at_hub(package_hash)

            # This part finds any packages that need to be on the same truck. It sets group to true so they can be
            # reordered after everything is on the correct truck.
            grouped_packages, is_group = self.same_truck_packages(package_hash)
            if is_group is True:
                group = True

            # Loads all of the packages that have a deadline. Any package that is not 'EOD' will be evenly divided
            # and loaded on the earliest available trucks. Current location is updated if there are early deliveries.
            early_delivery_ids = self.early_deliveries(current_location, package_hash, distance_dict, distances_list)
            if early_delivery_ids:
                current_location = self.load_list(early_delivery_ids, package_hash, grouped_packages)

            # Packages that must be on truck with specific name
            current_location, is_group = self.named_truck_packages(package_hash, current_location)
            if is_group is True:
                group = True

            # Finds the package with the closest address and loads that package onto the truck while there is still
            # space on the truck. Capacity is a constant number of 16 so the while loop starts as O(1)
            while self.capacity >= 1:
                # Finds the closest package to the current location.
                package_id, distance = shortest_distance(current_location, package_hash, distance_dict, distances_list)

                # This condition breaks out of while loop to stop loading packages if the last item in the list has
                # been reached. This will end the loading portion.
                if distance == 'Empty':
                    self.load(package_id, package_hash)
                    break

                # Loads the package if if its not on the truck and if it doesn't have another package it needs to
                # be loaded with.
                route_status = package_hash.get(package_id)[1]
                if route_status == 'Not On Truck':
                    address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
                    note = package_hash.get(package_id)[9]
                    if "Must be delivered with" not in note:
                        self.load(package_id, package_hash)

                    # Finds any other packages in the group and loads them if they aren't already on the truck.
                    else:
                        group_package_ids = re.findall('[0-9]+', note)
                        if self.capacity - len(group_package_ids) - 1 >= 0:
                            group = True
                            self.load(package_id, package_hash)
                            # The packages arent loaded according to their distance so it is reordered later.
                            # The group would be a constant so this for loop starts as O(1)
                            for id in group_package_ids:
                                id = int(id)
                                route_status = package_hash.get(id)[1]
                                if route_status == 'Not On Truck':
                                    self.load(id, package_hash)

                current_location = address

            # If group is true or early deliveries is true the loaded packages are reordered according to distance. The
            # early deliveries are not reordered. The packages that do not have a strict deadline are reordered.
            if is_group is True or early_delivery_ids:
                eod_packages = []
                reordered_eod_packages = []
                loc = ' HUB'
                first_eod = False
                first_eod_index = None
                for i, package_id in enumerate(self.loaded_package_list):
                    deadline = package_hash.get(package_id)[7]
                    # skip reordering any early deadlines packages
                    if deadline == 'EOD':
                        eod_packages.append(package_id)
                        previous_package = self.loaded_package_list[i-1]
                        if previous_package != 'EOD' and first_eod is False:
                            first_eod = True
                            first_eod_index = i
                            loc = ' ' + package_hash.get(previous_package)[3] + '\n(' + package_hash.get(previous_package)[6] + ')'

                # Reorders all of the packages in the truck that are EOD and puts them back in the loaded packages list.
                while len(eod_packages) > 0:
                    shortest = shortest_loaded(loc, package_hash, distance_dict, distances_list, eod_packages)
                    reordered_eod_packages.append(shortest)
                    eod_packages.remove(shortest)
                    loc = ' ' + package_hash.get(shortest)[3] + '\n(' + package_hash.get(shortest)[6] + ')'
                self.loaded_package_list[first_eod_index:len(self.loaded_package_list)] = reordered_eod_packages

        return self.loaded_package_list

    # Finds all of the early deliveries that are not currently on a route or delivered and returns an ordered list,
    # sorted by closest distance. The list is divided into even chunks so that it can be divided among the earliest
    # departing trucks. Ex) If 10 packages have early deadlines and there are 2 trucks leaving at the start time 5
    # packages will go on the first truck and 5 will go on the second truck.
    # Time Complexity O(n^2), Space Complexity O(n)
    def early_deliveries(self, current_location, package_hash, distance_dict, distances_list):
        early_deliveries = []
        for package in package_hash.map:
            package_id = package[0][0]
            package_deadline = package_hash.get(package_id)[7]
            note = package_hash.get(package_id)[9]
            route_status = package_hash.get(package_id)[1]
            if package_deadline != 'EOD' and "Must be delivered with" not in note and route_status == 'Not On Truck':
                early_deliveries.append(package_id)

        early_deliveries = self.chunk(early_deliveries, early_trucks)

        for package in package_hash.map:
            package_id = package[0][0]
            package_deadline = package_hash.get(package_id)[7]
            note = package_hash.get(package_id)[9]
            route_status = package_hash.get(package_id)[1]
            if package_deadline != 'EOD' and "Must be delivered with"in note and route_status == 'Not On Truck':
                early_deliveries.append(package_id)

        # While loop to order early deliveries according to distance.
        reordered_early_deliveries = []
        while len(early_deliveries) > 0:
            early_delivery_id = shortest_early_distance(current_location, package_hash, distance_dict, distances_list, early_deliveries)
            if early_delivery_id != 'Empty':
                reordered_early_deliveries.append(early_delivery_id)
                early_deliveries.remove(early_delivery_id)
                current_location = ' ' + package_hash.get(early_delivery_id)[3] + '\n(' + package_hash.get(early_delivery_id)[6] + ')'
            else:
                break
        return reordered_early_deliveries

    # Loads a given list of packages and any package that is grouped with it.
    # Time Complexity, O(n^2), Space Complexity O(1)
    def load_list(self, package_id_list, package_hash, grouped_packages):
        group = False
        for package_id in package_id_list:
            route_status = package_hash.get(package_id)[1]
            if route_status == 'Not On Truck':
                address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
                if package_id not in grouped_packages:
                    self.load(package_id, package_hash)

                # If there is a group of packages to load it first checks if there is enough room on the truck.
                elif self.capacity - len(grouped_packages) - 1 >= 0:
                    group = True
                    grouped_packages.remove(package_id)
                    self.load(package_id, package_hash)
                    # print(package_id)
                else:
                    print("GROUPED PACKAGES WONT FIT ON THIS TRUCK")

        # Loads the group of packages
        if group is True:
            if self.capacity - len(grouped_packages) - 1 >= 0:
                for id in grouped_packages:
                    grouped_packages.remove(id)
                    route_status = package_hash.get(id)[1]
                    if route_status == 'Not On Truck':
                        address = ' ' + package_hash.get(id)[3] + '\n(' + package_hash.get(id)[6] + ')'
                        self.load(id, package_hash)
        return address

    # Divides the packages between trucks so that the early packages are delivered faster if there are multiple trucks
    # that leave early in the day.
    # Time Complexity, O(N), Space Complexity O(n)
    def chunk(self, early_packages, num_trucks):
        li = []
        # num_trucks is changed to 1 so the packages will always be placed on the
        # next truck if they are designated early deliveries
        if num_trucks < 1:
            num_trucks = 1

        for i in range(0, num_trucks):
            # If the package is already in the list skip it.
            if i not in li:
                # if the package is in a group then put them together
                li.append(early_packages[i::num_trucks])

        # If there are no more early trucks the packages will be put on the next truck.
        global early_trucks
        early_trucks -= 1
        if early_trucks >= 0:
            return li[early_trucks]
        else:
            return li[0]

    # Finds all of the packages that must be on the same truck together.
    # Time Complexity O(n^2), Space Complexity O(1)
    def same_truck_packages(self, package_hash):
        group_ids = []
        is_group = False
        for package in package_hash.map:
            package_id = package[0][0]
            note = package_hash.get(package_id)[9]
            if "Must be delivered with" in note:
                group_ids.append(package_id)
                # findall counts as a constant O(1)
                group_package_ids = re.findall('[0-9]+', note)
                # There would be a defined number of grouped packages
                for id in group_package_ids:
                    id = int(id)
                    route_status = package_hash.get(id)[1]
                    if route_status == 'Not On Truck' and id not in group_ids:
                        is_group = True
                        group_ids.append(id)
        return group_ids, is_group

    # Finds all of the packages that must be on a truck with a specific number.
    # Time Complexity O(n^2), Space Complexity O(1)
    def named_truck_packages(self, package_hash, address):
        is_group = False
        for package in package_hash.map:
            package_id = package[0][0]
            note = package_hash.get(package_id)[9]
            route_status = package_hash.get(package_id)[1]
            if 'Can only be on truck' in note and route_status == 'Not On Truck':
                is_group = True
                truck_number = re.findall('[0-9]+', note)
                truck_number = truck_number[0]
                if self.name == truck_number:
                    address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
                    self.load(package_id, package_hash)
        return address, is_group
