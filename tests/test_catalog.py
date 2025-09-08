"""Unit tests for catalog_utils.

Author:
Version:
"""

import catalog_utils


def test_parse_credits():
    assert catalog_utils.parse_credits("3") == (3,)
    assert catalog_utils.parse_credits("1-4") == (1, 2, 3, 4)
    assert catalog_utils.parse_credits("3-5") == (3, 4, 5)


def test_json_to_catalog():
    catalog = catalog_utils.json_to_catalog({
        "JAPN 101": {
            "name": "Elementary Japanese I",
            "credits": "4",
            "description": "The fundamentals of Japanese through listening, speaking, reading, and writing.",
            "prerequisites": []
        },
        "JAPN 102": {
            "name": "Elementary Japanese II",
            "credits": "4",
            "description": "The fundamentals of Japanese through listening, speaking, reading, and writing. Practice in pronunciation and development of comprehension.",
            "prerequisites": [
                "JAPN 101"
            ]
        },
        "JAPN 231": {
            "name": "Intermediate Japanese I",
            "credits": "3-4",
            "description": "A thorough review of grammar, vocabulary building, conversation, composition, and reading.",
            "prerequisites": [
                "JAPN 102"
            ]
        }
    })

    end_catalog = {
        "JAPN 101": {
            "name": "Elementary Japanese I",
            "credits": (4, ),
            "description": "The fundamentals of Japanese through listening, speaking, reading, and writing.",
            "prerequisites": set()
        },
        "JAPN 102": {
            "name": "Elementary Japanese II",
            "credits": (4, ),
            "description": "The fundamentals of Japanese through listening, speaking, reading, and writing. Practice in pronunciation and development of comprehension.",
            "prerequisites": {
                "JAPN 101"
            }
        },
        "JAPN 231": {
            "name": "Intermediate Japanese I",
            "credits": (3, 4),
            "description": "A thorough review of grammar, vocabulary building, conversation, composition, and reading.",
            "prerequisites": {
                "JAPN 102"
            }
        }
    }

    assert catalog == end_catalog


def test_load_catalog():
    japn_catalog = {
        "JAPN 101": {
            "name": "Elementary Japanese I",
            "credits": (4,),
            "description": "The fundamentals of Japanese through listening, speaking, reading, and writing.",
            "prerequisites": set()
        },
        "JAPN 102": {
            "name": "Elementary Japanese II",
            "credits": (4,),
            "description": "The fundamentals of Japanese through listening, speaking, reading, and writing. Practice in pronunciation and development of comprehension.",
            "prerequisites": {
                "JAPN 101"
            }
        },
        "JAPN 231": {
            "name": "Intermediate Japanese I",
            "credits": (3, 4),
            "description": "A thorough review of grammar, vocabulary building, conversation, composition, and reading.",
            "prerequisites": {
                "JAPN 102"
            }
        }
    }

    assert catalog_utils.load_catalog("japn_catalog.json") == japn_catalog


def test_get_dependencies():
    classes_catalog = {
        "CS 261": {
            "name": "Societal and Ethical Issues in Computing",
            "credits": "3",
            "description": "",
            "prerequisites": {}
        },
        "CS 330": {
            "name": "Societal and Ethical Issues in Computing",
            "credits": "3",
            "description": "",
            "prerequisites": {}
        },
        "CS 361": {
            "name": "Computer Systems II",
            "credits": "3",
            "description": "",
            "prerequisites": {"CS 330", "CS 261"}
        },
        "CS 222": {
            "name": "Computer Systems II",
            "credits": "3",
            "description": "",
            "prerequisites": {"CS 361"}
        }
    }
    answer = {"CS 361", "CS 330", "CS 261"}
    assert catalog_utils.get_dependencies("CS 222", classes_catalog) == answer

    classes_catalog = {
        "CS 261": {
            "name": "Societal and Ethical Issues in Computing",
            "credits": "3",
            "description": "",
            "prerequisites": set()
        },
        "CS 330": {
            "name": "Societal and Ethical Issues in Computing",
            "credits": "3",
            "description": "",
            "prerequisites": set()
        },
        "CS 361": {
            "name": "Computer Systems II",
            "credits": "3",
            "description": "",
            "prerequisites": set()
        },
        "CS 222": {
            "name": "Computer Systems II",
            "credits": "3",
            "description": "",
            "prerequisites": set()
        }
    }
    assert catalog_utils.get_dependencies("CS 361", classes_catalog) == set()


def test_total_credits():
    catalog = catalog_utils.load_catalog('cs_catalog.json')
    sched = [{'ALGEBRA'}, {'CS 149'}, {'CS 227', 'CS 159'}]
    assert catalog_utils.total_credits(sched, catalog) == (9, 12)

    catalog = catalog_utils.load_catalog('cs_catalog.json')
    sched = [{'ALGEBRA'}, {'CS 240'}, {'CS 227'}]
    assert catalog_utils.total_credits(sched, catalog) == (6, 9)


def test_available_classes():
    # catalog = catalog_utils.load_catalog("japn_catalog.json")
    # available = catalog_utils.available_classes([{'JAPN 102'}, set(), set()], 0, catalog)
    # assert available == {"JAPN 101"}

    # catalog = catalog_utils.load_catalog("japn_catalog.json")
    # available = catalog_utils.available_classes([{'JAPN 102'}, set(), set()], 1, catalog)
    # assert available == {"JAPN 101", "JAPN 231"}

    catalog = catalog_utils.load_catalog("japn_catalog.json")
    available = catalog_utils.available_classes([set(), {'JAPN 102'}, set()], 0, catalog)
    assert available == {'JAPN 101'}


def test_check_prerequisites():
    # catalog = catalog_utils.load_catalog("japn_catalog.json")
    # sched = [{'JAPN 231'}, set(), {'JAPN 101'}, set(), {'JAPN 101'}]
    # problem = catalog_utils.check_prerequisites(sched, catalog)
    # assert problem == {"JAPN 231"}

    catalog = catalog_utils.load_catalog("japn_catalog.json")
    sched = [{'JAPN 231', 'JAPN 102'}, set(), {'JAPN 231'}]
    problem = catalog_utils.check_prerequisites(sched, catalog)
    assert problem == {'JAPN 231', 'JAPN 102'}


# We're providing tests for format_course_info() because these
# kinds of tests are particularly annoying to write.

def test_format_course_info():
    catalog = catalog_utils.load_catalog("japn_catalog.json")

    # Test the default width...
    actual = catalog_utils.format_course_info("JAPN 231", catalog)
    expect = """Name: Intermediate Japanese I

Description: A thorough review of
grammar, vocabulary building,
conversation, composition, and reading.

Credits: 3-4

Prerequisites: JAPN 102

Dependencies: JAPN 101, JAPN 102"""
    assert actual == expect

    #  Test an alternate width...
    actual = catalog_utils.format_course_info("JAPN 231", catalog, width=80)
    expect = """Name: Intermediate Japanese I

Description: A thorough review of grammar, vocabulary building, conversation,
composition, and reading.

Credits: 3-4

Prerequisites: JAPN 102

Dependencies: JAPN 101, JAPN 102"""
    assert actual == expect

    #  Test a different course and a different width...
    actual = catalog_utils.format_course_info("JAPN 101", catalog, width=50)
    expect = """Name: Elementary Japanese I

Description: The fundamentals of Japanese through
listening, speaking, reading, and writing.

Credits: 4

Prerequisites:

Dependencies:"""
    assert actual == expect
