# Christopher Brown 000968168

# Distance functions.
from datetime import datetime
from read import distance_to_list
from operator import itemgetter


# Finds a specific mileage from the distances_list and returns the distance in miles between two addresses
# Time Complexity, O(1)
def distance_between(adr1, adr2, distance_dictionary, distances_list):
    miles = (distances_list[distance_dictionary[adr1]][distance_dictionary[adr2]])
    if miles is '':
        miles = (distances_list[distance_dictionary[adr2]][distance_dictionary[adr1]])
    return float(miles)


# Creates a dictionary and a list to store the distances between addresses as found in the distance table.
# All of the distances are appended to the list.
# # Time Complexity, O(N^2)
def store_distance_table(distance_file):
    # Delivery addresses with distances
    distance_dictionary = {}
    distances_list = []
    for index, item in enumerate(distance_to_list(distance_file)):
        location = item[1]
        # Adds the location to a dictionary with a corresponding index to help search the distances
        distance_dictionary[location] = index
        distance = []
        for i in range(2, len(item)):
            distance.append(item[i])
        # Adds a row of full of distances
        distances_list.append(distance)
    return distance_dictionary, distances_list


# Returns a tuple with the package_id and the shortest distance in miles from the current location to a location in the
# package hash that is currently at the hub and is not yet loaded onto a truck.
# Time Complexity O(n^2), Space Complexity O(n)
def shortest_distance(current_location, package_hash, distance_dict, distances_list):
    ordered_distance = []

    for package in package_hash.map:
        package_id = package[0][0]
        route = package[0][1][1]
        at_hub = package[0][1][0]

        # If the hash map says it is on the truck with a time then skip over the package
        if route == 'Not On Truck' and at_hub == 'At Hub':
            # This takes O(n)
            address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
            distance = distance_between(current_location, address, distance_dict, distances_list)
            id_distance = (package_id, distance)
            ordered_distance.append(id_distance)
    # Sorts the list according to the shortest distance. This sort takes O(n log n), Space Complexity O(n)
    ordered_distance.sort(key=itemgetter(1))
    i = 0
    if len(ordered_distance) > 1 and current_location == address:
        return ordered_distance[i]
    elif len(ordered_distance) <= 1:
        ordered_distance = (ordered_distance[i][0], 'Empty')
        return ordered_distance
    return ordered_distance[i]


# Returns a tuple with the package_id and the shortest distance in miles from the current location to a location in the
# package hash that is currently at the hub and is not yet loaded onto a truck. The package must also have a deadline
# that is not EOD.
# Time Complexity, O(n^2), Space Complexity O(n)
def shortest_early_distance(current_location, package_hash, distance_dict, distances_list, early_deliveries):
    ordered_distance = []
    for package_id in early_deliveries:
        # This line takes O(n)
        at_hub = package_hash.get(package_id)[0]

        route = package_hash.get(package_id)[1]
        deadline = package_hash.get(package_id)[7]
        if route == 'Not On Truck' and at_hub == 'At Hub':
            deadline = datetime.strptime(deadline, '%I:%M %p').time()
            address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
            distance = distance_between(current_location, address, distance_dict, distances_list)
            id_distance_deadline = [package_id, distance, deadline]
            ordered_distance.append(id_distance_deadline)
    # Sort them in order of distance first. This takes O(n log n), space complexity O(n)
    ordered_distance.sort(key=itemgetter(1))

    # Then compare to the earliest deadline and sort them in the shortest order
    earliest = datetime.time(datetime.max)
    for item in ordered_distance:
        package_time = ordered_distance[ordered_distance.index(item)][2]
        if package_time < earliest:
            ordered_distance.insert(0, ordered_distance.pop(ordered_distance.index(item)))
            earliest = package_time
    for item in ordered_distance:
        package_id = ordered_distance[ordered_distance.index(item)][0]
        ordered_distance[ordered_distance.index(item)] = package_id

    if len(ordered_distance) >= 1:
        return ordered_distance[0]
    else:
        return 'Empty'


# Finds the shortest distance for packages that are already on the truck but need to be reorganized. This will only
# resort the packages due by the end of day.
# Time Complexity, O(N^2), Space Complexity O(n)
def shortest_loaded(current_location, package_hash, distance_dict, distances_list, loaded_packages):
    ordered_distance = []
    for package_id in loaded_packages:
        # This line takes O(n)
        deadline = package_hash.get(package_id)[7]
        if deadline == 'EOD':
            address = ' ' + package_hash.get(package_id)[3] + '\n(' + package_hash.get(package_id)[6] + ')'
            distance = distance_between(current_location, address, distance_dict, distances_list)
            id_distance = (package_id, distance)
            ordered_distance.append(id_distance)
    # This line takes O(n log n), space complexity O(n)
    ordered_distance.sort(key=itemgetter(1))

    return ordered_distance[0][0]
