"""Utility functions for working with catalog information.

Author: Aiden Aquino
Date:  12/6/23
"""

import json
import textwrap
from copy import deepcopy


def parse_credits(credits):
    """Return a tuple of ints representing the possible credit values.

    Examples:
    >>> parse_credits("3")
    (3,)
    >>> parse_credits("1-4")
    (1, 2, 3, 4)

    Args:
        credits (str): The credits string.

    Returns:
        tuple: An ordered tuple of all possible credit values.
    """
    # Split the string based off the -
    split_string = credits.split("-")
    # Save the string tup
    string_tup = ()

    # If there is a range of nums, convert to range and then to tup
    if len(split_string) == 2:
        string_tup = tuple(range(int(split_string[0]), int(split_string[1]) + 1))
        return string_tup
    # If there is only one possible credit, return a tuple with only one num in it
    elif len(split_string) == 1:
        return (int(split_string[0]), )


def json_to_catalog(json_dict):
    """Convert from the json catalog format to the correct internal format.

    This will return an exact copy of the provided dictionary except for the
    following:

    * The lists of prerequisite course ids will be converted to sets.
    * The credit strings will be converted to integer tuples (using
    the parse_credits function)

    Args:
        json_dict (dict): A catalog dictionary as ready by the json module.

    Returns:
        dict: A catalog dictionary in the correct internal format.

    """
    placeholder_dict = deepcopy(json_dict)
    # for every course in the dict
    for course in placeholder_dict:
        placeholder_dict[course] = placeholder_dict[course]

        # update the credit strings
        placeholder_dict[course]["credits"] = parse_credits(placeholder_dict[course]["credits"])

        # Update the pre-reqs
        reqs_set = set()
        for pre_req in placeholder_dict[course]["prerequisites"]:
            reqs_set.add(pre_req)

        placeholder_dict[course]["prerequisites"] = reqs_set

    # Return
    return placeholder_dict


def load_catalog(filename):
    """Read course information from an JSON file and return a dictionary.

    Args:
        filename (str): The filename of the JSON file.

    Returns:
        dict: A dictionary containing course information.
    """
    with open(filename) as file:
        json_loaded_dict = json.load(file)
        final_dict = json_to_catalog(json_loaded_dict)
        return final_dict


def get_dependencies(course_id, catalog):
    """Get the all dependencies for a course.

    This function will return the prerequisites for the course, plus
    all prerequisites for those prerequisites, and so on.

    Args:
        course_id (str): The ID of the course.
        catalog (dict): The dictionary containing course information.

    Returns:
        set: A set of course dependencies.

    """
    pre_reqs = catalog[course_id]["prerequisites"]
    if pre_reqs == {} or pre_reqs == set():
        return set()

    dependencies = set()
    # Add the pre_req and it's dependencies
    for req in pre_reqs:
        dependencies.add(req)

        for sub_reqs in get_dependencies(req, catalog):
            dependencies.add(sub_reqs)

    return dependencies


def format_course_info(course_id, catalog, width=40):
    """Format course information for display.

    The resulting string will have five fields: Name, Description,
    Credits, Prerequisites, and Dependencies.  Each field will be
    separated by a blank line and each will be wrapped to the maximum
    allowable number of characters. The string will not end in a newline.

    Args:
        course_id (str): The ID of the course.
        catalog (dict): The dictionary containing course information.
        width (int, optional): The width for text wrapping. Defaults to 40.

    Returns:
        str: Formatted course information.

    """
    final_str = ""
    course = catalog[course_id]

    # Add Name
    name_str = "Name: " + course["name"]
    for line in textwrap.wrap(name_str, width):
        final_str += line + "\n"
    final_str += "\n"

    # Add Description
    desc_str = "Description: " + course["description"]

    for line in textwrap.wrap(desc_str, width):
        final_str += line + "\n"
    final_str += "\n"

    # Add Credits
    creds = course["credits"]
    creds_str = ""
    if len(creds) > 1:
        creds_str += "Credits: " + f"{creds[0]}-{creds[-1]}"
    elif len(creds) == 1:
        creds_str += "Credits: " + f"{creds[0]}"

    for line in textwrap.wrap(creds_str, width):
        final_str += line + "\n"
    final_str += "\n"

    # Add Prerequisites
    reqs_str = "Prerequisites: "

    iterations = 0
    for pre_req in course["prerequisites"]:
        if iterations != len(course["prerequisites"]) - 1:
            reqs_str += pre_req + ", "
        else:
            reqs_str += pre_req
        iterations += 1

    for line in textwrap.wrap(reqs_str, width):
        final_str += line + "\n"
    final_str += "\n"

    # Add Dependencies
    depnds_str = "Dependencies: "
    course_depnds = list(sorted(get_dependencies(course_id, catalog)))

    iterations = 0
    for depnd in course_depnds:
        if iterations != len(course_depnds) - 1:
            depnds_str += depnd + ", "
        else:
            depnds_str += depnd

        iterations += 1

    for line in textwrap.wrap(depnds_str, width):
        final_str += line + "\n"

    return final_str.strip()


def total_credits(schedule, catalog):
    """Calculate the range of total credits in a schedule.

    Args:
        schedule (list): The course schedule.
        catalog (dict): The dictionary containing course information.

    Returns:
        tuple: A two entry tuple where the first entry is the minimum
            total credits for the schedule and the second is the maximum total
            credits.
    """
    # Save Max and Min
    num_max = 0
    num_min = 0

    # Run through each semester
    for semester in schedule:
        # Run through each course in the semester
        for course in semester:
            # convert credits into a list for iteration
            course_credits = list(catalog[course]["credits"])

            # If there is more than one set amount of credits, add max and min
            if len(course_credits) > 1:
                num_min += course_credits[0]
                num_max += course_credits[-1]
            # If there is only one possible credit, add that to the max and min
            elif len(course_credits) == 1:
                num_min += course_credits[0]
                num_max += course_credits[0]

    return (num_min, num_max)


def available_classes(schedule, semester, catalog):
    """Get the available classes for a semester based on the current schedule.

    A course is available for the indicated semester if it is not
    already present somewhere in the schedule, and all of the
    prerequisites have been fulfilled in some previous semester.

    Args:
        schedule (list): The current course schedule.
        semester (int): The semester for which to find available classes.
        catalog (dict): The dictionary containing course information.

    Returns:
        set: A set of available classes for the specified semester.

    """
    classes = set()
    for course in catalog:
        course_reqs = catalog[course]["prerequisites"]
        if (course_reqs == set() or course_reqs == {}) and not check_semester(course, schedule)[0]:
            classes.add(course)
        else:
            reqs_achieved = 0
            for req in course_reqs:
                for sem_set in schedule:
                    if req in sem_set and schedule.index(sem_set) < semester:
                        reqs_achieved += 1
            if reqs_achieved == len(course_reqs) and not check_semester(course, schedule)[0]:
                classes.add(course)

    return classes


def check_semester(course, schedule):
    """Checks each semester to see if the course is in the semester.

    Args:
        course (str): course to be looked for in schedule
        schedule (list): schedule course would be in

    Returns:
        bool: True for if course is in the schedule, False if the opposite
    """
    semester_in = 0
    for semester in schedule:
        if course in semester:
            return True, semester_in
        semester_in += 1

    return False, semester_in


def check_prerequisites(schedule, catalog):
    """Check for courses in a schedule with unmet prerequisites.

    Args:
        schedule (list): The course schedule.
        catalog (dict): The dictionary containing course information.

    Returns:
        set: A set of courses with unmet prerequisites.
    """
    invalid_classes = set()

    current_semester = 0
    for semester in schedule:
        for course in semester:
            course_cat = catalog[course]["prerequisites"]
            if len(course_cat) != 0:
                for req in course_cat:
                    sem_check = check_semester(req, schedule)
                    if not sem_check[0] or current_semester <= sem_check[1]:
                        invalid_classes.add(course)
                        break
        current_semester += 1

    return invalid_classes
