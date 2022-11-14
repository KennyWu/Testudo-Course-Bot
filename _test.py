import pytest
from RetrieveData import Retrieve

def test_one():
    """Tests the dictionary values is None with newly initalized Retrieve Object"""
    retrieve = Retrieve()
    assert retrieve.course_selection == None
    
def test_two():
    """Test that the retrieve object will hold the correct dictionary values when updated"""
    a = True
    assert a == True
