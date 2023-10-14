import json
from datetime import datetime, timedelta
import sys

# Load the JSON data from the file
with open('/home/trabajo/.ti-sheet') as f:
    data = json.load(f)

def calculate_total_time_per_month(data):
    # Initialize a dictionary to store total time per day
    total_time_per_day = {}

    # Get the current month
    current_month = datetime.utcnow().month

    # Iterate over the work entries
    for entry in data['work']:
        start_time = datetime.fromisoformat(entry['start'][:-1])

        # Check if the entry is within the current month
        if start_time.month == current_month:
            # Calculate the time difference in seconds
            end_time_str = entry.get('end', None)
            if end_time_str:
                end_time = datetime.fromisoformat(end_time_str[:-1])
            else:
                end_time = datetime.utcnow()

            time_difference = (end_time - start_time).total_seconds()

            # Extract the date (year-month-day) from the start time
            date = start_time.date()

            # Add the time difference to the total time for that day
            total_time_per_day[date] = total_time_per_day.get(date, 0) + time_difference

    return total_time_per_day

# Calculate total time for the current month
total_time_per_month = calculate_total_time_per_month(data)
total_time = 0

# Print the total time for each day in the current month
for date, total_time_day in list(total_time_per_month.items())[-int(sys.argv[1]):]:
    total_time += total_time_day
    print(f'{date.strftime("%d")}: {total_time_day/3600:.2f}h')


previous_time = list(total_time_per_month.items())[-(int(sys.argv[1])+1)][1]
last_time = list(total_time_per_month.items())[-1][1]

# The avr needs to include x items and cause we are excluding the last one, we must add one previous to the list
# I dont wanna my avr go down because the day is starting and the time is 0
total_time -= last_time
total_time += previous_time

average_time = total_time / int(sys.argv[1])
print(f'{sys.argv[1]}d: {average_time/3600:.2f}h')
