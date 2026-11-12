*****Harbour View Hotel - Daily Operations Report Agent*****

***1. Project Overview***

This project automates the reconcilation of employee working hours agains their End-of-Day (EOD) reports for Harbour View Hotel.

The application is developed in Python and integrates Google Sheets API, Gemini API, and Gmail SMTP to identify discrepancies, generate management reports, and deliver summaries by email.

***2. Technology Stack***
- Python
- Google Sheets API
- Google Service Account Authentication
- gspread (Python library)
- Google Geminig API
- Gmail SMTP
- python-dotenv

***3. Workflow***
1. Authenticate with Google using a Service Account.
2. Retrieve Staff Hours and Staff EOD Reports from Google Sheets.
3. Match records using employee name and date.
4. Detect discrepancies using four predefined rules.
5. Write identified issues to the Issues worksheet.
6. Calculate employee-level statistics and write them to Daily_Report.
7. Send verification reconciliation results to Gemini for management summary generation.
8. Save the generated summary locally.
9. Delivery the management summary through Gmail SMTP.

***4. Issue Detection Rules***
Missing hours > Tracked hours are less than 7
Report with no hours > EOD exists but no tracked-hours record exists
Hours with no report > Tracked-hours record exists but no EOD report exists
Claim exceeds tracked > Claimed hours exceed tracked hours by more than 1 hour

***5. Output***
The application generates a Google Spreadsheet containing:
***Issues***
- employee
- date
- issue_type
- detail
***Daily_Report***
- employee
- total_tracked_hours
- number_of_issues
- status (OK/Follow-up)

It also generates a management summary of no more than 200 wrds and sends it to a configured test email address.

***6. Assumptions***
- Employee names are matched without regard to capitalization or surrounding whitespace
- Employee records are matched using employee name and date
- Duplicate employee/date records are treated as data errors
- A tracked-hours value below 7 hours trigger Missing hours
- A claim must exceed tracked hours by strictly more than 1 hour to trigger Claim exceeds tracked.
- Multiple issues can be flagged for the same employee on the same date.
- Missing tracked-hours records are not treated as zero when calculating total tracked hours.
- Employees with at least one issue flag received Follow-up status
- Gemini is responsible for writing the management summary, not determining whether an issue exits.
- Email delivery uses Gmail SMTP and an App Password.

***7. Configuration***
Create a .env file containing:

STAFF_HOURS_SHEET_ID=
STAFF_EOD_SHEET_ID=
OUTPUT_SHEET_ID=
GEMINI_API_KEY=
SENDER_EMAIL=
SENDER_APP_PASSWORD=
RECIPIENT_EMAIL=

Place the Google Service Account JSON file inside the credentials folder.

Never commit credentials, API keys, or .env to version control.

***8. Installation and Execution***
Install dependencies:
    pip install gspread google-auth google-genai python-dotenv

Run the application
    python main.py

***9. Validation***
The supplied dataset contains 8 employees across 5 workind days.

Expected reconciliation results:

- 39 tracked-hours records.
- 38 EOD records.
- 12 total issue flags.
- 8 employee summaries.

The four issue categories are validated independently, allowing multiple flags for a single employee-day.

***10. Security***
- Google Sheet access is authenticated through a Service Account.
- API keys and email credentials are stored in environment variables.
- Sensitive credentials are excluded from Git using .gitignore.
- The output spreadsheet is shared with authorized reviewers.