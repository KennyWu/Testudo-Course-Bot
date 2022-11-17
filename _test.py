import pytest
from RetrieveData import Retrieve


def test_one():
    """Tests the dictionary values is None with newly initalized Retrieve Object"""
    retrieve = Retrieve()
    assert retrieve.course_selection == None


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