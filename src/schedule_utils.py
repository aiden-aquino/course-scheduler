"""Utility functions for working with course schedules.

A course schedule is a list of sets where each entry in the list
represents an academic term, and the entries in the sets are strings
representing the course ids of courses taken during that term.

Author: Aiden Aquino
Version: 12/6/23
"""

import json


def schedule_to_json(schedule):
    """Convert a course schedule to a format suitable for saving as JSON.

    The provided schedule will not be modified.

    Args:
        schedule (list): A list of sets.

    Returns:
        list: A list of lists.
    """
    converted_schedule = []
    for semester in schedule:
        current_semester = []
        for course in semester:
            current_semester.append(course)
        converted_schedule.append(sorted(current_semester))

    return converted_schedule


def json_to_schedule(schedule_list):
    """Convert a list of lists to a list of sets.

    The elements in each list will be stored in alphabetical order.
    The provided list will not be modified.

    Args:
        schedule_list (list): A list of lists.

    Returns:
        list: A list of sets.

    """
    converted_schedule = []
    for semester in schedule_list:
        current_semester = set()
        for course in semester:
            current_semester.add(course)
        converted_schedule.append(current_semester)

    return converted_schedule


def save_schedule(schedule, filename):
    """Save a course schedule to a JSON file.

    The course schedule is represented as a list of sets, where each
    set contains the course ids (strings) for the corresponding
    semester.

    Within each semester, the course ids will be stored in alphabetical
    order in the resulting JSON file.

    Args:
        schedule (list): The course schedule.
        filename (str): The filename for the JSON file.

    """
    new_sched = []
    for semester in schedule:
        new_sched.append(sorted(semester))

    with open(filename, 'w') as file:
        json.dump(schedule_to_json(new_sched), file, indent=4)


def load_schedule(filename):
    """Load a course schedule from an JSON file.

    The return value will be a list of sets, where each set contains
    the course ids (strings) for the corresponding semester.

    Args:
        filename (str): The filename of the JSON file.

    Returns:
        list: A list of sets representing the course schedule.

    """
    with open(filename) as file:

        loaded_file = json.load(file)
        json_sched = json_to_schedule(loaded_file)
        return json_sched


def get_duplicates(schedule):
    """Get duplicate courses in a schedule.

    The resulting set will be empty if there are no duplicates.

    Args:
        schedule (list): The course schedule.

    Returns:
        set: A set of duplicate courses.
    """
    current_len = 0
    classes_in_course = set()

    classes_dups = set()
    for semester in schedule:
        for course in semester:
            classes_in_course.add(course)
            if len(classes_in_course) == current_len:
                classes_dups.add(course)
            else:
                current_len += 1

    return classes_dups
