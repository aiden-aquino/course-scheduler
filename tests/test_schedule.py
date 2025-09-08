"""Unit tests for schedule_utils.

Author: Aiden Aquino
Version: 11/26/2023
"""
import schedule_utils


def test_schedule_to_json():
    schedule = [set(), set(), set()]
    assert schedule_utils.schedule_to_json(schedule) == [[], [], []]

    schedule = [{"A Class"}, set(), {"A Nother Class"}]
    assert schedule_utils.schedule_to_json(schedule) == [["A Class"], [], ["A Nother Class"]]

    schedule = [set(), {"Class One", "Class Two"}, set()]
    assert schedule_utils.schedule_to_json(schedule) == [[], ["Class One", "Class Two"], []]

    schedule = [{'AA 100', 'AA 200', 'AA 300', 'BB 100', 'BB 200', 'ZZZ 500'}, {'CC 200', 'DD 100', 'DD 200', 'CC 100', 'YYY 500', 'CC 300'}]
    assert schedule_utils.schedule_to_json(schedule) == [['AA 100', 'AA 200', 'AA 300', 'BB 100', 'BB 200', 'ZZZ 500'], ['CC 100', 'CC 200', 'CC 300', 'DD 100', 'DD 200', 'YYY 500']]


def test_json_to_schedule():
    schedule = [[], [], []]
    assert schedule_utils.json_to_schedule(schedule) == [set(), set(), set()]

    schedule = [["A Class"], [], ["Another Class"]]
    assert schedule_utils.json_to_schedule(schedule) == [{"A Class"}, set(), {"Another Class"}]

    schedule = [[], ["Class One", "Class Two"], []]
    assert schedule_utils.json_to_schedule(schedule) == [set(), {"Class One", "Class Two"}, set()]


def test_save_load_schedule():
    # One strategy for testing save and load is to:
    #
    # * Create a schedule by hand.
    # * Use save_schedule() to save that schedule.
    # * Use load_schedule() to load the resulting file.
    # * Assert that the loaded data matches the saved data.
    #
    # This strategy has the disadvantage of not testing the two methods
    # in isolation, which is generally the goal of unit testing. But it
    # is easier to implement, because no additional files are required.
    schedule = [set(), set(), set()]
    schedule_utils.save_schedule(schedule, "afile.json")
    print(schedule)
    assert schedule_utils.load_schedule("afile.json") == schedule

    schedule = [set(), {"CS 149", "One Other Class"}, set()]
    schedule_utils.save_schedule(schedule, "anotherfile.json")
    assert schedule_utils.load_schedule("anotherfile.json") == schedule

    schedule = [{"Class_One"}, set(), {"Class_Two"}]
    schedule_utils.save_schedule(schedule, "oneotherfile.json")
    assert schedule_utils.load_schedule("oneotherfile.json") == schedule


def test_get_duplicates():
    schedule = [{"Class_One"}, set(), {"Class_Two"}]
    assert schedule_utils.get_duplicates(schedule) == set()

    schedule = [{"Class_One", "Class_Two"}, set(), {"Class_Two"}]
    assert schedule_utils.get_duplicates(schedule) == {"Class_Two"}

    schedule = [{"Class_One", "Class_Two"}, {"Class_Three"}, {"Class_Three"}]
    assert schedule_utils.get_duplicates(schedule) == {"Class_Three"}

    schedule = [{'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}, {'CS 50', 'CS 40', 'CS 20', 'CS 10', 'CS 30', 'CS 60'}]
    assert schedule_utils.get_duplicates(schedule) == {'CS 50', 'CS 20', 'CS 10', 'CS 40', 'CS 30', 'CS 60'}
