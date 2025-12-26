import pytest
#This test is a compilation of my pytest learning journey.
import logging
import utils
logger = logging.getLogger(__name__)
logger.info("Logger initialized in test_assert.py")
def test_zero_div():
    with pytest.raises(ZeroDivisionError):
        a = 10/0

def test_pass_assertion():
    print("Pytest won't print this message unless we run with -s option")
    try:
        assert 0+1 ==1
        logger.info("test_pass: Assertion passed as 0+1 equals 1")
        utils.insert_test_result("v1.0","test_assert.test_pass_assertion","PASS")
    except AssertionError as e:
        logger.error("test_pass: Assertion failed as 0+1 does not equal 1")
        utils.insert_test_result("v1.0","test_assert.py","FAIL","test_pass_assertion",str(e))
        logger.error(e)
        raise
   
 
@pytest.mark.functional #This is a marker for "funcational tests" and we can run all the tests with this marker using pytest -m functional
def test_fail():
    assert 0+1 == 4

@pytest.mark.skip(reason = "skipping this test")
def test_skip():
    assert 0+1 == 1
    
@pytest.mark.xfail(reason = "we can define the expected failure here so that it does not fail the test suite")
def test_xfail():
    assert 0+0 ==3

@pytest.mark.skipif(True, reason ="The feature will be skipped if the condition is true")
def test_skipif():
	assert 0+1 == 1