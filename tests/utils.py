from datetime import datetime
import pandas as pd
#import pytest

import mysql.connector
from html import escape


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpassword",
        database="pytest_db"
    )

def insert_test_result(app_version, test_name, status, fail_function=None, fail_error=None, run_id=None, duration=None):
    #docker exec -it pytest-mysql mysql -u root -p
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO test_results (app_version, test_name, status, fail_function, fail_error, run_id, duration)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (app_version, test_name, status, fail_function, fail_error, run_id, duration))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_results_by_version(app_version):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    #query = "SELECT test_name, status FROM test_results WHERE app_version = %s"
    query = """SELECT test_name, COUNT(*) AS total_runs, SUM(STATUS='PASS') AS pass_count, SUM(STATUS='FAIL') AS fail_count
               FROM test_results
               WHERE app_version = %s
               GROUP BY test_name"""
    cursor.execute(query, (app_version,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row["test_name"]: row for row in results}

def compare_versions(old_results, new_results):
    regressions = []
    new_added_tests_fail = []
    new_added_tests_pass = []
    missing_tests_new = []
    flaky_tests = []
    successful_tests = []
    # for test_name, old_status in old_results.items():
    #     new_status = new_results.get(test_name)
    #     if new_status is None and old_status is None:
    #         continue  # Both versions missing the test, ignore
    #     elif new_status is None:
    #         missing_tests_new.append(test_name)
    #     elif old_status is None:
    #         missing_tests_old.append(test_name)
    #     if old_status == "PASS" and (new_status == "FAIL" or new_status is None):
    #         regressions.append(test_name)
    # return {"regressions": regressions, "missing_tests_old": missing_tests_old, "missing_tests_new": missing_tests_new}
    
    missing_tests_old = new_results.keys() - old_results.keys()
    for test in missing_tests_old:
        pass_rate = new_results[test]["pass_count"] / new_results[test]["total_runs"] if new_results[test]["total_runs"] > 0 else 0
        if pass_rate < 0.4:
            new_added_tests_fail.append(test)
        else:
            new_added_tests_pass.append(test)
            
    for test_name, old_data in old_results.items():
        new_data = new_results.get(test_name)
        if new_data is None:
            missing_tests_new.append(test_name)
            continue
        old_pass_rate = old_data["pass_count"] / old_data["total_runs"] if old_data["total_runs"] > 0 else 0
        new_pass_rate = new_data["pass_count"] / new_data["total_runs"] if new_data["total_runs"] > 0 else 0
        
        if 0.8 <= old_pass_rate < 1.0 and new_pass_rate < 0.5:
            regressions.append(test_name)
            
        elif 0.5 <= old_pass_rate < 0.8 and 0.5 <= new_pass_rate < 0.8:
            flaky_tests.append(test_name)
            
        else:
            successful_tests.append(test_name)
            
        
    return {
        "regressions": regressions,
        "missing_tests_new": missing_tests_new,
        "new_added_tests_fail": new_added_tests_fail,
        "new_added_tests_pass": new_added_tests_pass,
        "flaky_tests": flaky_tests,
        "successful_tests": successful_tests
    }
    
# def generateHtmlReport(comparison_result, output_file="report.html"):
#     with open(output_file, "w") as f:
#         f.write("<html><head><title>Test Comparison Report</title>")
#         f.write("<style>")
#         f.write("body { font-family: Arial, sans-serif; }")
#         f.write("h1 { color: #333; }")
#         f.write("h2 { color: #666; }")
#         f.write(".Regressions { color: red; }")
#         f.write(".Missing { color: orange; }")
#         f.write(".Flaky { color: blue; }")
#         f.write(".Successful { color: green; }")
#         f.write("</style></head><body>")
#         f.write("<h1>Test Comparison Report</h1>")
        
#         f.write("<h2>Regressions</h2><ul>")
#         for test in comparison_result["regressions"]:
#             f.write(f"<li>{test}</li>")
#         f.write("</ul>")
        
#         f.write("<h2>Missing Tests in Old Version</h2><ul>")
#         for test in comparison_result["missing_tests_old"]:
#             f.write(f"<li>{test}</li>")
#         f.write("</ul>")
        
#         f.write("<h2>Missing Tests in New Version</h2><ul>")
#         for test in comparison_result["missing_tests_new"]:
#             f.write(f"<li>{test}</li>")
#         f.write("</ul>")
        
#         f.write("<h2>Flaky Tests</h2><ul>")
#         for test in comparison_result["flaky_tests"]:
#             f.write(f"<li>{test}</li>")
#         f.write("</ul>")
        
#         f.write("<h2>Successful Tests</h2><ul>")
#         for test in comparison_result["successful_tests"]:
#             f.write(f"<li>{test}</li>")
#         f.write("</ul>")
        
#         f.write("</body></html>")

def generate_html_report(comparison_result,runid, duration, output_file=None):
    if output_file is None:
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"reports/comparison_report_{date_str}.html"
    parts = []
    parts.append("<html><head><title>Test Comparison Report</title>")
    parts.append("<style>")
    parts.append("body { font-family: Arial, sans-serif; }")
    parts.append("h1 { color: #333; }")
    parts.append("h2 { color: #666; }")
    parts.append(".regressions { color: red; }")
    parts.append(".missing-new { color: orange; }")
    parts.append(".flaky { color: blue; }")
    parts.append(".successful { color: green; }")
    parts.append(".stats { color: purple; }")
    parts.append("</style></head><body>")
    parts.append("<h1>Test Comparison Report</h1>")
    parts.append(f"<h3 class=\"stats\">Run ID: {escape(runid)}</h3>")
    parts.append(f"<h3 class=\"stats\">Total Session Duration: {escape(str(duration))} seconds</h3>")

    def list_section(title, items, cls):
        
        if not items:
            parts.append(f"<h2>{escape(title)}</h2><ul>")
            parts.append("<li>None</li>")
        else:
            parts.append(f"<h2>{escape(title)}</h2><ul class=\"{cls}\">")
            parts.extend(f"<li>{escape(str(item))}</li>" for item in items)
        parts.append("</ul>")

    list_section("Regressions", comparison_result["regressions"], "regressions")
    list_section("Newly added tests - Fail", comparison_result["new_added_tests_fail"], "regressions")
    list_section("Newly added tests - Pass", comparison_result["new_added_tests_pass"], "successful")
    list_section("Missing Tests in New Version", comparison_result["missing_tests_new"], "missing-new")
    list_section("Flaky Tests", comparison_result["flaky_tests"], "flaky")
    list_section("Successful Tests", comparison_result["successful_tests"], "successful")

    parts.append("</body></html>")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

def load_test_data(filepath, operation):
    df = pd.read_csv(filepath)
    filtered_df = df[df["operation"] == operation]
    return list(filtered_df[["test_id","description","a","b","expected"]].itertuples(index=False, name=None))

#get_test_data_output should be like =>
# [
# ("TC001", "Add 2 nums", "5", "2", "7"),
# ("TC002", "Add 2 nums", "10", "20", "30"),
# ("TC003", "Add 2 nums", "0", "0", "10"),
#]