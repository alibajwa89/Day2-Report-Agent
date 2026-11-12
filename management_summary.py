import json
from collections import defaultdict

from google import genai

MODEL_NAME = "gemini-3.5-flash-lite"

def generate_management_summary(hours_records, issues, api_key):
    employee_hours = defaultdict(float)
    employee_issue_counts = defaultdict(int)

    for record in hours_records:
        employee = record["employee"].strip()

        employee_hours[employee] += float(
            record["tracked_hours"]
        )

    for issue in issues:
        employee = issue["employee"]

        employee_issue_counts[employee] += 1

    employees = sorted(
        set(employee_hours) | set(employee_issue_counts)
    )

    employee_data = []

    for employee in employees:

        total_hours = round(employee_hours[employee], 2)
        issue_count = employee_issue_counts[employee]


        employee_data.append({
            "employee": employee,
            "total_tracked_hours": total_hours,
            "number_of_issues": issue_count,
            "status": (
                "Follow-up" if issue_count > 0 else "OK"
            )
        })

    issue_breakdown = defaultdict(int)

    for issue in issues:
        issue_breakdown[issue["issue_type"]] += 1

    report_data = {
        "employees": employee_data,
        "issue_breakdown": dict(issue_breakdown),
        "total_issue_flags": len(issues)
    }

    prompt = f"""
    You are an operations reporting assistant for Harbour View Hotel.

    Analyze the following verified reconcilation data:

    {json.dumps(report_data, indent=2)}

    Write a professional management summary without bold letters.

    Requirements:
    1. Maximum 180 words
    2. Identify employees who are on track
    3. Identify employees who need follow-up.
    4. Highlight recurring or notable issue patterns.
    5. Mention relevant issue counts.
    6. Be concise and actionable.
    7. Do not invent explanations or causes.
    8. Do not change any figures.
    9. Distinguish issue flags from employee counts.

    Return only the management summary (short, accurate, actionable)
"""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    summary = response.text.strip()

    if len(summary.split()) > 200:
        raise ValueError(
            "Gemini generated more than 200 words. "
            "Please regenerate a shorter summary."
        )

    return summary
    