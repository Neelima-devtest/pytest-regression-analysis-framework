import pytest
import utils
import socket
from datetime import datetime
import time

APP_VERSION = "v1.0"
OLD_VERSION = "v1.1"
START_TIME = None
TOTAL_SESSION_DURATION = None
RUN_ID = None


def generate_run_id():
    hostname = socket.gethostname()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}"
RUN_ID = generate_run_id()

@pytest.fixture(scope="session")
def test_data_addition():
    return utils.load_test_data("tests/data.csv", "add")

@pytest.fixture(scope="session")
def test_data_subtraction():
    return utils.load_test_data("tests/data.csv", "sub")

@pytest.fixture(scope="session")
def test_data_multiplication():
    return utils.load_test_data("tests/data.csv", "mul")

@pytest.fixture(scope="session")
def test_data_division():
    return utils.load_test_data("tests/data.csv", "div")

@pytest.fixture(params=utils.load_test_data("tests/data.csv", "add"), ids=lambda r: str(r[0]))
def add_case(request):
    return request.param

@pytest.fixture(params=utils.load_test_data("tests/data.csv", "sub"), ids=lambda r: str(r[0]))
def sub_case(request):
    return request.param
    

def pytest_runtest_logreport(report):
    #This is a hook. pytest calls this automatically thrice for each testcase.
    #report.when has three values based on three different stages of a test i.e setup, call, teardown
    #We want to push the result to DB only for test_call phase. So we ignore the others.
    
    #Trivia - How does pytest recognise a hook?
    #Based on the function name. There are predefined function names for hooks. If we change the name or arguments, it doesnt work.
    
    if report.when != "call":
        return
    
    test_name = report.nodeid
    status = "PASS" if report.passed else "FAIL"
    fail_func = None
    fail_err = None
    if report.failed:
        fail_func = report.nodeid
        # Use longrepr for failure representation (string, traceback, etc.)
        fail_err = str(getattr(report, "longrepr", ""))
        
    utils.insert_test_result(APP_VERSION, test_name, status, fail_func, fail_err,RUN_ID,report.duration)

def pytest_sessionstart(session):
    #This hook is called at the start of the test session.
    #We can use it to perform any setup or initialization.
    global START_TIME
    START_TIME = time.monotonic()
    
def pytest_sessionfinish(session, exitstatus):
    #This hook is called at the end of the test session.
    #We can use it to perform any cleanup or final reporting.
    
    old = utils.fetch_results_by_version(OLD_VERSION)
    new = utils.fetch_results_by_version(APP_VERSION)

    result = utils.compare_versions(old, new)

    global TOTAL_SESSION_DURATION
    TOTAL_SESSION_DURATION = round(time.monotonic() - START_TIME, 2)
    utils.generate_html_report(result,RUN_ID, TOTAL_SESSION_DURATION)
    # Rule - Fail on regressions or missing new tests
    if result["regressions"] or result["missing_tests_new"]:
        pytest.exit("Regression OR Missing New Tests Detected !!! {loudly crying face}", returncode=1)
        






