def write_issues(spreadsheet, issues):

    try:
        worksheet = spreadsheet.worksheet("Issues")
    except Exception:
        worksheet = spreadsheet.add_worksheet(
            title="Issues",
            rows=100,
            cols=4
        )

    worksheet.clear()

    headers = [
        "employee",
        "date",
        "issue_type",
        "detail"
    ]

    rows = [
        [
            issue["employee"],
            issue["date"],
            issue["issue_type"],
            issue["detail"]
        ]
        for issue in issues
    ]

    worksheet.update(
        values=[headers] + rows,
        range_name="A1"
    )

    print(f"Successfully uploaded {len(issues)} issues.")


def write_daily_report(spreadsheet, hours_records, issues):

    try:
        worksheet = spreadsheet.worksheet("Daily_Reprt")
    except Exception:
        worksheet = spreadsheet.add_worksheet(
            title="Daily_Report",
            rows=20,
            cols=4,
        )

    worksheet.clear()

    employee_hours = {}

    for record in hours_records:
        employee = record["employee"].strip()
        tracked = float(record["tracked_hours"])

        employee_hours[employee] = (
            employee_hours.get(employee, 0) + tracked
        )

    employee_issues = {}

    for issue in issues:
        employee = issue["employee"]

        employee_issues[employee] = (
            employee_issues.get(employee, 0) + 1
        )

    employees = sorted(
        set(employee_hours) | set(employee_issues)
    )

    rows = []

    for employee in employees:

        total_hours = employee_hours.get(employee, 0)
        issue_count = employee_issues.get(employee, 0)

        status = "Follow-up" if issue_count > 0 else "OK"

        rows.append([
            employee,
            round(total_hours, 2),
            issue_count,
            status
        ])

    headers = [
        "employee",
        "total_tracked_hours",
        "number_of_issues",
        "status"
    ]

    worksheet.update(
        values=[headers] + rows,
        range_name = "A1"
    )

    print(
        f"Successfully uploaded Daily_Report "
        f"for {len(employees)} employees. "
    )