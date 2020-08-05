# Christopher Brown 000968168


import datetime


# Stores today's date and 8:00 AM as the start time. The date isn't currently necessary but I include the date so if the
# program is updated in the future with multiple dates for deliveries I will be closer to having a correct solution.
# Time Complexity O(1), Space Complexity O(1)
def start_time():
    today = datetime.date.today()
    t = datetime.datetime(today.year, today.month, today.day, 8, 0, 0)
    return t


# Each truck has a time that changes independently from the others.
class Time:

    # Time Complexity O(1), Space Complexity O(1)
    def __init__(self, start=start_time()):
        self.start_time = start
        self.current_time = self.start_time
        self.end_time = 0

    # This advances a trucks time by adding the hours, minutes, and seconds to the current time.
    # Time Complexity O(1), Space Complexity O(1)
    def advance_time(self, cur_time, hrs, mins, secs):
        time_change = datetime.timedelta(hours=hrs, minutes=mins, seconds=secs)
        self.current_time = cur_time + time_change
        return self.current_time

