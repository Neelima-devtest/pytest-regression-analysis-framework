Goal - A simple end to end framework for regression analysis.

  To run tests in "tests" directory using the the config in "pytest.ini". Every run has a unique runid.
  
  To generate a html report (within reports directory) for every run with all the tests passed or failed in that run.
  
  To generate code coverage reports (within reports directory) with respect to the "app" directory.
  
  For every testcase, push the testcase info to the mysql database.
  
  Database has the columns - app_version, test_name, fail_function, fail_error, run_id, duration (execution time for each testcase).
  
  After the run is complete, compare all the runs of the current version with the previous version in database.
  
  Then, generate a comparison report with runid, total session duration, regressions, flaky tests, newly added tests and successful tests.



How to run?

  From the root directory just execute "pytest", the run parameters is fetched from pytest.ini.
