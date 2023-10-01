import json
import sys

from datetime import datetime
from datetime import timedelta

file_path = 'study_data.json'


def start_new_session():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'sessions': []}

    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    new_session = {
        'start_time': current_time,
        'end_time': None,
        'breaks': []
    }

    data['sessions'].append(new_session)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print('New study session added successfully.')

def end_last_session():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('No study sessions found.')
        return

    sessions = data.get('sessions', [])
    if not sessions:
        print('No study sessions found.')
        return

    # Find the last study session and set its end time to the current time
    last_session = sessions[-1]
    if last_session['end_time']:
        print('The last session is already ended.')
        return

    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    last_session['end_time'] = current_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print('Last study session ended successfully.')

def add_start_break_to_last_session():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('No study sessions found.')
        return

    sessions = data.get('sessions', [])
    if not sessions:
        print('No study sessions found.')
        return

    # Find the last study session and check if it's already ended
    last_session = sessions[-1]
    if last_session['end_time']:
        print('The last session is already ended.')
        return

    # Check if a break is already started for the last session
    if last_session['breaks'] and not last_session['breaks'][-1].get('end_time'):
        print('A break is already started for the last session.')
        return

    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # Create a new break and add the start time
    new_break = {
        'start_time': current_time,
        'end_time': None
    }

    last_session['breaks'].append(new_break)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print('Start time for a break added to the last study session.')


def end_last_break_to_last_session():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('No study sessions found.')
        return

    sessions = data.get('sessions', [])
    if not sessions:
        print('No study sessions found.')
        return

    # Find the last study session and check if it's already ended
    last_session = sessions[-1]
    if last_session['end_time']:
        print('The last session is already ended.')
        return

    # Check if a break is not started for the last session
    if not last_session['breaks']:
        print('No break started for the last session.')
        return

    # Check if the last break is already ended
    last_break = last_session['breaks'][-1]
    if last_break['end_time']:
        print('The last break is already ended.')
        return

    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # Set the end time for the last break
    last_break['end_time'] = current_time

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print('End time for the last break added to the last study session.')

def print_session_durations():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('No study sessions found.')
        return

    sessions = data.get('sessions', [])
    if not sessions:
        print('No study sessions found.')
        return

    print('Session Durations:')
    for session in sessions:
        start_time = datetime.fromisoformat(session['start_time'])
        end_time = datetime.fromisoformat(session['end_time'])

        session_duration = end_time - start_time

        print(f'{start_time.strftime("%m/%d")} - {end_time.strftime("%m/%d")}')
        print(f'Duration: {str(session_duration)}')

        if session['breaks']:
            total_break_duration = timedelta()  # Initialize total_break_duration to a timedelta object

            for b in session['breaks']:
                if b.get('end_time'):
                    break_duration = datetime.fromisoformat(b['end_time']) - datetime.fromisoformat(b['start_time'])
                    total_break_duration += break_duration

            session_duration_without_breaks = session_duration - total_break_duration
            print(f'Total Duration: {str(session_duration_without_breaks)}')
        else:
            print('No breaks for this session.')
        print()

def print_session_durations1():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('No study sessions found.')
        return

    sessions = data.get('sessions', [])
    if not sessions:
        print('No study sessions found.')
        return

    print('{:<12} {:<12} {:<12} {:<12} {:<12}'.format('Date', 'Start Time', 'End Time', 'Total Duration', 'Duration'))
    print('-' * 65)

    for session in sessions:
        start_time = datetime.fromisoformat(session['start_time'])
        end_time = datetime.fromisoformat(session['end_time'])

        session_duration = end_time - start_time
        total_duration = session_duration

        if session['breaks']:
            total_break_duration = timedelta()  # Initialize total_break_duration to a timedelta object

            for b in session['breaks']:
                if b.get('end_time'):
                    break_duration = datetime.fromisoformat(b['end_time']) - datetime.fromisoformat(b['start_time'])
                    total_break_duration += break_duration

            total_duration = session_duration - total_break_duration



        print('{:<12} {:<12} {:<12} {:<12} {:<12}'.format(start_time.strftime('%m/%d'),
                                                         start_time.strftime('%H:%M'),
                                                         end_time.strftime('%H:%M'),
                                                         format_timedelta(session_duration),
                                                         format_timedelta(total_duration)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <function>")
        sys.exit(1)

    function_to_run = sys.argv[1]

    if function_to_run == "end_last_session":
        end_last_session()
    elif function_to_run == "start_new_session":
        start_new_session()
    elif function_to_run == "start_break":
        add_start_break_to_last_session()
    elif function_to_run == "end_break":
        end_last_break_to_last_session()
    elif function_to_run == "print":
        print_session_durations1()
    else:
        print("Invalid function. Available functions: start_new_session, end_last_session, start_break, end_break, print")

#start_new_session()
#add_start_break_to_last_session()
#end_last_break_to_last_session()
#end_last_session()
#print_session_durations()
