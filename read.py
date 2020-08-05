# Christopher Brown 000968168


import csv

# The two functions are the same except for variable names. I can merge these in the future.
# Function iterates through each line in the file and puts them in a list.
# Time Complexity, O(N), Space Complexity O(1)
def distance_to_list(distance_file):
    distance_list = []
    with open(distance_file, 'r') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            distance_list.append(row)
    return distance_list


# Function iterates through each line in the file and puts them in a list.
# Time Complexity, O(N), Space Complexity O(1)
def package_to_list(package_file):
    package_list = []
    with open(package_file, 'r') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            package_list.append(row)
    return package_list
