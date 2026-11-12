from datetime import datetime

def normalize_date(value):
    """Convert spreadsheet dates into a consistent format."""

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    return str(value).strip()[:10]


def build_lookup(records):
    """Create employee-date lookup dictionaries."""

    lookup = {}

    for record in records:
        employee = record["employee"].strip()
        date = normalize_date(record["date"])

        key = (employee.lower(), date)

        if key in lookup:
            raise ValueError(f"Duplicate record found: {key}")


        lookup[key] = record

    return lookup


def reconcile_data(hours_records, eod_records):

    hours_lookup = build_lookup(hours_records)
    eod_lookup = build_lookup(eod_records)

    all_keys = set(hours_lookup) | set(eod_lookup)

    issues = []

    for employee_key, date in sorted(all_keys):

        hours_record = hours_lookup.get((employee_key, date))
        eod_record = eod_lookup.get((employee_key, date))

        employee = (
            hours_record["employee"] if hours_record
            else eod_record["employee"]
        )

        tracked = (
            float(hours_record["tracked_hours"])
            if hours_record else None
        )

        claimed = (
            float(eod_record["claimed_hours"])
            if eod_record else None
        )

        if tracked is not None and tracked < 7:
            issues.append({
                "employee": employee,
                "date": date,
                "issue_type": "Missing hours",
                "detail": (
                    f"Only {tracked} tracked hours; "
                    "below the 7-hour minimum"
                )
            })

        if eod_record and not hours_record:
            issues.append({
                "employee": employee,
                "date": date,
                "issue_type": "Report with no hours",
                "detail": "EOD submitted but no tracked time recorded"
            })

        if hours_record and not eod_record:
            issues.append({
                "employee": employee,
                "date": date,
                "issue_type": "Hours with no report",
                "detail": "Tracked time exists but no EOD report submitted."
            })

        if (
            claimed is not None
            and tracked is not None
            and claimed - tracked > 1
        ):
            issues.append({
                "employee": employee,
                "date": date,
                "issue_type": "Claim exceeds tracked",
                "detail": (
                    f"Claimed {claimed} hours but"
                    f"only {tracked} hours tracked."
                )
            })

    return issues