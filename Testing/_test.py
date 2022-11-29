import pytest
from Retrieval import Retrieve


def test_one():
    """Tests the dictionary values is empty with newly initalized Retrieve Object"""
    retrieve = Retrieve()
    print(retrieve.course_selection)
    assert retrieve.course_selection == {}


def test_two():
    """Test that the retrieve object will hold the correct dictionary values when updated"""
    test_dict = {'CMSC216': {110, 120, 130, 140},
                 'CMSC132': {110, 120, 130, 140}}
    retrieve = Retrieve(semester="202301")
    retrieve.course_selection = test_dict
    assert retrieve.course_selection == {'CMSC216': {
        110, 120, 130, 140}, 'CMSC132': {110, 120, 130, 140}}


def test_three():
    """Test adding new key value pair to the dictionary"""
    test_dict = {'CMSC216': {110, 120, 130, 140},
                 'CMSC132': {110, 120, 130, 140}}
    retrieve = Retrieve(semester=202301)
    retrieve.course_selection = test_dict
    assert retrieve.add(course='CMSC417') == False
    assert retrieve.add(course='CMSC417', section={"0101"}) == True
    assert retrieve.course_selection == {'CMSC216': {110, 120, 130, 140}, 'CMSC132': {
        110, 120, 130, 140}, 'CMSC417': {"0101"}}


def test_four():
    """Tests adding new sections to existing classes"""
    test_dict = {'CMSC216': {'0101', '0102', '0103'},
                 'CMSC132': {110, 120, 130, 140}}
    retrieve = Retrieve(semester=202301)
    retrieve.course_selection = test_dict
    assert retrieve.add(course='CMSC216', section={'0104', '0105'}) == True
    assert retrieve.course_selection == {'CMSC216': {'0101', '0102', '0103', '0104', '0105'},
                                         'CMSC132': {110, 120, 130, 140}}


def test_five():
    """Tests for if a class doesn't exist"""
    test_dict = {'CMSC216': {110, 120, 130, 140},
                 'CMSC132': {110, 120, 130, 140}}
    retrieve = Retrieve(semester=202301)
    retrieve.course_selection = test_dict
    assert retrieve.add(course='CS0-1', section={100, 200, 300, 400}) == False


def test_six():
    """Tests for invalid sections"""
    test_dict = {'CMSC216': {110, 120, 130, 140},
                 'CMSC132': {110, 120, 130, 140}}
    retrieve = Retrieve(semester=202301)
    retrieve.course_selection = test_dict
    assert retrieve.add(course='CMSC216', section={'0000', '0101'}) == False


def test_seven():
    """Tests that deleting works as on deleting whole courses"""
    test_dict = {'CMSC216': {110, 120, 130, 140},
                 'CMSC132': {110, 120, 130, 140}}
    retrieve = Retrieve(semester=202301)
    retrieve.course_selection = test_dict
    assert retrieve.delete('CMSC132') == True
    assert retrieve.course_selection == {'CMSC216': {110, 120, 130, 140}}


def test_eight():
    """Tests deleting specific sections"""
    test_dict = {'CMSC216': {'101', '102', '103', '104'},
                 'CMSC132': {'101', '102', '103', '104'}}
    retrieve = Retrieve(semester=202301)
    retrieve.course_selection = test_dict
    assert retrieve.delete('CMSC132', {'101', '102', '200'}) == True
    assert retrieve.course_selection == {'CMSC216': {'101', '102', '103', '104'},
                                         'CMSC132': {'103', '104'}}


def test_nine():
    """Not actual inseration test due to variables always changing,
     just testing retrieve - use py.test _test.py -s
     """
    retrieve = Retrieve(semester=202301)
    assert retrieve.add('CMSC132', {'0101', '0102', '0103'}) == True
    assert retrieve.add('MATH240', {'0121', '0122', '0131'}) == True
    data = retrieve.retrieve()
    for course in data:
        print("COURSE: " + course)
        for section in data[course]:
            print("  - Section " + section)
            print("    - Time: " + data[course][section][0])
            print("    - Opening: " + data[course][section][1])
            print("    - Waitlist: " + data[course][section][2])
