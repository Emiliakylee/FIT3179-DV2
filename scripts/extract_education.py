"""Extract enrolment data from the Department of Education 2024 tables.

Usage:
    python3 scripts/extract_education.py path/to/uploads

Expects 2024_Section2_All_Students.xlsx and 2024_Section7_Overseas_Students.xlsx
in that folder. Writes into data/.

Source: Australian Government Department of Education, Selected Higher
Education Statistics - 2024 Student Data, Tables 2.5, 2.12 and 7.4.
"""
import csv
import sys
from pathlib import Path

from openpyxl import load_workbook

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

ABBREV = {
    "New South Wales": "NSW", "Victoria": "VIC", "Queensland": "QLD",
    "Western Australia": "WA", "South Australia": "SA", "Tasmania": "TAS",
    "Australian Capital Territory": "ACT", "Northern Territory": "NT",
}


def num(cell):
    try:
        return float(str(cell).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


# ------------------------------------------- 2.5 enrolments by state (C6)
wb2 = load_workbook(SRC / "2024_Section2_All_Students.xlsx",
                    read_only=True, data_only=True)

states = {}
for row in wb2["2.5"].iter_rows(min_row=4, values_only=True):
    state, institution = row[0], row[1]
    if state not in ABBREV or institution is None:
        continue
    rec = states.setdefault(ABBREV[state], {
        "state": ABBREV[state], "state_name": state, "total": 0.0,
        "postgraduate_coursework": 0.0, "bachelor": 0.0,
        "universities": 0, "non_university": 0,
    })
    rec["total"] += num(row[8]) or 0
    rec["postgraduate_coursework"] += num(row[3]) or 0
    rec["bachelor"] += num(row[4]) or 0
    if str(institution).startswith("Non-University"):
        rec["non_university"] += 1
    else:
        rec["universities"] += 1

# ------------------------------------ 2.12 domestic vs overseas by state (C7)
for row in wb2["2.12"].iter_rows(min_row=5, values_only=True):
    state, institution = row[0], row[1]
    if state not in ABBREV or institution is None:
        continue
    rec = states[ABBREV[state]]
    domestic = sum(num(c) or 0 for c in row[2:5])     # citizen, NZ, PR
    overseas = sum(num(c) or 0 for c in row[5:8])     # humanitarian, temp, other
    rec["domestic"] = rec.get("domestic", 0) + domestic
    rec["overseas"] = rec.get("overseas", 0) + overseas

rows = []
for rec in states.values():
    head = rec["domestic"] + rec["overseas"]
    rows.append({
        "state": rec["state"],
        "state_name": rec["state_name"],
        "enrolments": int(rec["total"]),
        "postgraduate_coursework": int(rec["postgraduate_coursework"]),
        "bachelor": int(rec["bachelor"]),
        "overseas": int(rec["overseas"]),
        "overseas_share": round(100 * rec["overseas"] / head, 1) if head else "",
        "universities": rec["universities"],
    })
rows.sort(key=lambda r: -r["enrolments"])

with open(OUT / "enrolments_by_state_2024.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["state", "state_name", "enrolments",
                                      "postgraduate_coursework", "bachelor",
                                      "overseas", "overseas_share",
                                      "universities"])
    w.writeheader()
    w.writerows(rows)

# ---------------------------------------- 7.4 overseas students by country (C8)
wb7 = load_workbook(SRC / "2024_Section7_Overseas_Students.xlsx",
                    read_only=True, data_only=True)

countries = []
for row in wb7["7.4"].iter_rows(min_row=4, values_only=True):
    region, country, total = row[0], row[1], num(row[2])
    if not country or total is None or str(country).strip() == "Australia":
        continue
    if str(country).lower().startswith(("total", "not ", "unknown")):
        continue
    countries.append({"region": str(region).strip(),
                      "country": str(country).strip(),
                      "students": int(total)})
countries.sort(key=lambda r: -r["students"])

with open(OUT / "overseas_by_country_2024.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["region", "country", "students"])
    w.writeheader()
    w.writerows(countries)

grand = sum(c["students"] for c in countries)
top5 = sum(c["students"] for c in countries[:5])
print(f"states        : {len(rows)}")
print(f"countries     : {len(countries)}  total {grand:,}")
print(f"top 5 share   : {100 * top5 / grand:.1f}%")
for c in countries[:8]:
    print(f"   {c['country']:<22} {c['students']:>8,}")
