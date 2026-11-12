import os
from pathlib import Path

import gspread
from dotenv import load_dotenv

from google_sheets import write_issues, write_daily_report
from management_summary import generate_management_summary

from email_sender import send_management_email

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

HOURS_SHEET_ID = os.getenv("STAFF_HOURS_SHEET_ID")
EOD_SHEET_ID = os.getenv("STAFF_EOD_SHEET_ID")
OUTPUT_SHEET_ID = os.getenv("OUTPUT_SHEET_ID")

CREDENTIALS_FILE = (
    BASE_DIR / "credentials" / "service_account.json"
)

if not CREDENTIALS_FILE.exists():
    raise FileNotFoundError(
        f"Credentials not found: {CREDENTIALS_FILE}"
    )

gc = gspread.service_account(
    filename=str(CREDENTIALS_FILE),
    scopes= [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)

print("Successfully authenticated with Google!")


hours_spreadsheet = gc.open_by_key(HOURS_SHEET_ID)
hours_worksheet = hours_spreadsheet.sheet1

hours_records = hours_worksheet.get_all_records()

print("\nSTAFF HOURS")
print("Spreadsheet:", hours_spreadsheet.title)
print("Total records:", len(hours_records))
print("Columns:", list(hours_records[0].keys()))

eod_spreadsheet = gc.open_by_key(EOD_SHEET_ID)
eod_worksheet = eod_spreadsheet.sheet1

eod_records = eod_worksheet.get_all_records()

print("\nSTAFF EOD REPORTS")
print("Spreadsheet:", eod_spreadsheet.title)
print("Total records:", len(eod_records))
print("Columns:", list(eod_records[0].keys()))


print("\nGoogle Sheets API connection successful")


#######
from reconciliation import reconcile_data

issues = reconcile_data(hours_records, eod_records)
print("\nRECONCILIATION RESULTS")
print("Total issues:", len(issues))

for issue in issues:
    print(issue)

output_spreadsheet = gc.open_by_key(OUTPUT_SHEET_ID)

write_issues(output_spreadsheet, issues)
write_daily_report(output_spreadsheet, hours_records, issues)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing from .env")

summary = generate_management_summary(
    hours_records,
    issues,
    GEMINI_API_KEY
)

print("\nAI MANAGEMENT SUMMARY")
print("==================")
print(summary)
print("\nWord count:", len(summary.split()))

summary_file = BASE_DIR / "outputs" / "management_summary.txt"
summary_file.parent.mkdir(exist_ok=True)
summary_file.write_text(summary, encoding="utf-8")
print("\nManagement summary saved succesfully")

send_management_email(summary)