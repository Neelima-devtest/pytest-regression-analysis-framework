import pytest
import logging
from app.calc_app import add, subtract, multiply, divide

logger = logging.getLogger(__name__)
logger.info("Logger initialized in test_csv_data.py")

#If we want to use "parametrize" to get data from csv file and use it in the test function, we can add a marker like below
#@pytest.mark.parametrize("test_id,description,a,b,expected",get_test_data("tests/data.csv","add"),ids = lambda val: str(val))
#def test_add(test_id, description, a,b,expected):
#    result = a+b
#    assert result == expected, f"Testid {test_id} with description {description} failed as the expected value is {expected} but actual value is {result}"
    
#The above line can be replaced with the below line if we want to use fixture to get the data from csv file
#The fixture is defined in conftest.py file
#And we dont have to import the fixture in this file, pytest will automatically find it in conftest.py file

#CREATE TABLE test_results ( id INT AUTO_INCREMENT PRIMARY KEY, app_version VARCHAR(20), test_name VARCHAR(255), status VARCHAR(10), fail_function VARCHAR(255), fail_error TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

logger.setLevel(logging.INFO)

#Now we will use fixture to run the addition tests
#In parametrized, each row in the csv file will be treated as a separate test case by pytest.

@pytest.mark.addition
def test_add(add_case):
    test_id, description, a, b, expected = add_case
    logger.info(f"Executing testid {test_id} with description '{description}'")
    assert add(a, b) == expected, (
        f"Failure message : {test_id} with description '{description}' failed as the expected value is {expected} "
        f"but actual value is {add(a, b)}"
    )
    logger.info(
        f"Testid {test_id} with description '{description}' passed as the expected value is {expected} "
        f"and actual value is {add(a, b)}"
    )
        
@pytest.mark.subtraction
def test_subtract(sub_case):
    test_id, description, a, b, expected = sub_case
    logger.info(f"Executing testid {test_id} with description '{description}'")
    assert subtract(a, b) == expected, (
        f"Failure message : {test_id} with description {description} failed as the expected value is {expected} "
        f"but actual value is {subtract(a, b)}"
    )
    logger.info(
        f"Test case succeeded {test_id} : {description} with expected {expected} and value {subtract(a, b)}"
    )