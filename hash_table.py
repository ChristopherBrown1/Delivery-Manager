# Christopher Brown 000968168

# Class for custom hash table functionality.
from datetime import datetime
import re


class HashTable:

    # Sets the size of the hash table to 40 items and initializes each item to None.
    # Time Complexity O(1), Space Complexity O(1)
    def __init__(self):
        self.size = 40
        self.map = [None] * self.size

    # Calculates the index for the key in the hash map and returns the index.
    # Time Complexity O(1) , Space Complexity O(1)
    def _get_hash(self, key):
        return key % self.size

    # Adds a key and value to the hash table if there is nothing already in that key. If the key is taken
    # it updates the value.
    # Time Complexity O(N), Space Complexity O(1)
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for item in self.map[key_hash]:
                if item[0] == key:
                    # updates the value if the key already exists
                    item[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # Gets the value for a specified key if it exists. If there is a collision it searches through each key and
    # returns the value of the matching key.
    # Time Complexity O(N), Space Complexity O(1)
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Deletes an item from the hash table by searching every key in the table and popping the matching key.
    # Time Complexity O(N), Space Complexity O(1)
    def delete(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    # Iterates through all of the keys in the hash table and appends them to a list.
    # Time Complexity O(N), Space Complexity O(1)
    def get_keys(self):
        keys_list = []
        for item in self.map:
            if item is not None:
                keys_list.append(item[0][0])
        return keys_list

    # prints every item in the map by looping through them.
    # Time Complexity O(N), Space Complexity O(1)
    def print(self):
        print('---------- Hash Map ----------')
        for item in self.map:
            if item is not None:
                print(str(item))

    # Searches and prints all of the packages at their final delivery time.
    # Time Complexity O(N), Space Complexity O(1)
    def lookup_all_final(self):
        print()
        print('---------- All Packages Final Times ----------')
        for item in self.map:
            if item is not None:
                package_num = "Package ID: " + str(item[0][0])
                delivery_time = item[0][1][2]
                address = "to " + item[0][1][3] + " " + item[0][1][4] + " " + item[0][1][5] + " " + item[0][1][6] + "."
                deadline =  "The deadline was " + item[0][1][7] + "."
                print(package_num, delivery_time, address, deadline)

    # Looks up a single package and prints its final delivery time. This returns a package from self.get() which
    # operates in O(N) time.
    # Time Complexity O(N), Space Complexity O(1)
    def lookup_single_final(self, id_num):
        print()
        print('---------- Single Package ----------')
        package_values = self.get(id_num)
        if package_values is not None:
            package_num = "Package ID: " + str(id_num)
            delivery_time = package_values[2]
            address = "to " + package_values[3] + " " + package_values[4] + " " + package_values[5] + " " + package_values[6] + "."
            deadline = "The deadline was " + package_values[7] + "."
            print(package_num, delivery_time, address, deadline)

    # Loops through all packages in the hash table and prints their status at the specified time. The hash table
    # contains status information with times that the package started on its delivery route and was delivered. This
    # information is used to infer where a package was at a given time.
    # Time Complexity O(N), Space Complexity O(1)
    def lookup_all_time(self, user_time):
        print()
        print('---------- All Packages at ' + str(user_time) + ' ----------')
        for item in self.map:
            if item is not None:
                package_num = "Package ID: " + str(item[0][0])
                route = item[0][1][1]
                format = '%I:%M:%S'
                # findall would be bound by a constant so this line is O(1)
                route_time = re.findall(r'\d{1,2}:\d{2}:\d{2}', route)
                route_time = datetime.strptime(route_time[0], format).time()
                delivery_status = item[0][1][2]
                delivery_time = re.findall(r'\d{1,2}:\d{2}:\d{2}', delivery_status)
                delivery_time = datetime.strptime(delivery_time[0], format).time()

                address = "to " + item[0][1][3] + " " + item[0][1][4] + " " + item[0][1][5] + " " + item[0][1][6] + "."
                deadline = "The deadline was " + item[0][1][7] + "."

                if user_time < route_time:
                    deadline = "The deadline is " + item[0][1][7] + "."
                    print(package_num, "At Hub will be loaded at", route_time, "Will be going " + address, deadline)
                elif route_time <= user_time < delivery_time:
                    deadline = "The deadline is " + item[0][1][7] + "."
                    print(package_num, route, "Shipping " + address, deadline)
                elif delivery_time <= user_time:
                    print(package_num, "Delivered at", delivery_time, address, deadline)

    # Gets a single package from the hash table and prints its status at the specified time. The hash table
    # contains status information with times that the package started on its delivery route and was delivered. This
    # information is used to infer where a package was at a given time.
    # Time Complexity O(N), Space Complexity O(1)
    def lookup_single_time(self, id_num, user_time):
        print()
        print('---------- Single Package at ' + str(user_time) + ' ----------')
        package_values = self.get(id_num)
        if package_values is not None:
            package_num = "Package ID: " + str(id_num)
            route = package_values[1]
            format = '%I:%M:%S'
            # findall would be bound by a constant so this line is O(1)
            route_time = re.findall(r'\d{1,2}:\d{2}:\d{2}', route)
            route_time = datetime.strptime(route_time[0], format).time()
            delivery_status = package_values[2]
            delivery_time = re.findall(r'\d{1,2}:\d{2}:\d{2}', delivery_status)
            delivery_time = datetime.strptime(delivery_time[0], format).time()

            address = "to " + package_values[3] + " " + package_values[4] + " " + package_values[5] + " " + package_values[6] + "."
            deadline = "The deadline was " + package_values[7] + "."

            if user_time < route_time:
                deadline = "The deadline is " + package_values[7] + "."
                print(package_num, "At Hub will be loaded at", route_time, "Will be going " + address, deadline)
            elif route_time <= user_time < delivery_time:
                deadline = "The deadline is " + package_values[7] + "."
                print(package_num, route, "Shipping " + address, deadline)
            elif delivery_time <= user_time:
                print(package_num, "Delivered at", delivery_time, address, deadline)