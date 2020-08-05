# Christopher Brown 000968168

import re
from hash_table import HashTable
from read import package_to_list


# Iterates through each package in the table and adds the package to the hash table. The package status is added to
# the hash table for easy recall. The package status will show times when the package arrives at the hub, is put on the
# truck, and is delivered.
# Time Complexity O(n), Space Complexity O(n)
def store_package_table(package_file):
    # packages with delivery addresses
    package_hash = HashTable()
    for item in package_to_list(package_file):
        # Delivery Status is initialized to In Hub
        current_location = 'At Hub'
        if 'Delayed' in item[7]:
            # findall would be bound by a constant so this line is O(1)
            match = re.findall(r'\d{1,2}:\d{2}\s\w{2}', item[7])
            current_location = 'Arriving at ' + match[0]
        package_value = [current_location, 'Not On Truck', 'Not Delivered']
        for index in range(1, 8):
            package_value.append(item[index])
        # sets the package ID as a key and a list of delivery status, address, city, state, zip, deadline, and
        # notes as a value.
        package_hash.add(int(item[0]), package_value)
    return package_hash
