"""Extract the DV2 data files from the official SES 2025 tables workbook.

Usage:
    python3 scripts/extract_ses.py SES_2025_National_Report_Tables.xlsx

Writes into data/. Rerun any time; it overwrites.
Source: QILT, 2025 Student Experience Survey National Report Tables.
"""
import csv
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "SES_2025_National_Report_Tables.xlsx")
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

LEVELS = {"UG": "Undergraduate", "PGC": "Postgraduate"}

# Short labels for axes; the full name still goes in tooltips.
SHORT = {
    "Overall Educational Experience": "Overall experience",
    "Teaching Quality and Engagement": "Teaching quality",
    "Skills Development": "Skills development",
    "Learning Resources": "Learning resources",
    "Student Support and Services": "Student support",
    "Peer Engagement": "Peer engagement",
}

# Only the one name too long for the axis; tooltips keep the full name.
AREA_SHORT = {
    "Tourism, hospitality, personal services, sport and recreation":
        "Tourism and hospitality",
    "Humanities, culture and social sciences": "Humanities and culture",
    "Agriculture and environmental studies": "Agriculture and environment",
    "Architecture and built environment": "Architecture and building",
    "Computing and information systems": "Computing and IT",
    "Health services and support": "Health services",
    "Law and paralegal studies": "Law and paralegal",
}


def tidy_label(text):
    """Collapse non-breaking spaces and stray whitespace in a source label."""
    return " ".join(str(text).replace("\xa0", " ").split())


def clean_measure(text):
    """'Focus areas: Peer Engagement *' -> 'Peer Engagement'"""
    text = re.sub(r"^(Focus areas|Questionnaire item):\s*", "", str(text))
    return text.replace("*", "").strip()


def num(cell):
    try:
        return float(str(cell).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def grid(ws):
    """Header row is row 4; data starts row 5 and stops at the first blank label."""
    rows = list(ws.iter_rows(values_only=True))
    measures = [clean_measure(c) for c in rows[3][2:8]]
    out = []
    for row in rows[4:]:
        label = row[1]
        if label is None or str(label).strip() == "":
            break
        out.append((tidy_label(label), str(row[0] or "").strip(),
                    [num(c) for c in row[2:8]]))
    return measures, out


wb = load_workbook(SRC, read_only=True, data_only=True)

# ---------------------------------------------------------------- 1. trend
trend = []
for key, level in LEVELS.items():
    measures, rows = grid(wb[f"FOCUS_{key}_ALL_17-YY_YEAR"])
    for label, _group, values in rows:
        year = re.sub(r"\D", "", label)[:4]
        for measure, value in zip(measures, values):
            if value is not None:
                trend.append({"year": year, "level": level,
                              "measure": measure,
                              "measure_short": SHORT.get(measure, measure),
                              "value": value})

with open(OUT / "ses_trend_2017_2025.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["year", "level", "measure",
                                      "measure_short", "value"])
    w.writeheader()
    w.writerows(trend)

# ----------------------------------------------------------- 2. study area
area = []
for key, level in LEVELS.items():
    measures, rows = grid(wb[f"FOCUS_{key}_ALL_1Y_AREA"])
    national = {m: v for m, v in zip(measures, dict(
        (label, values) for label, _g, values in rows)["All study areas"])}
    for label, _group, values in rows:
        if label == "All study areas":
            continue
        by_measure = dict(zip(measures, values))
        overall = by_measure["Overall Educational Experience"]
        for measure, value in by_measure.items():
            if value is None:
                continue
            area.append({
                "study_area": label,
                "study_area_short": AREA_SHORT.get(label, label),
                "level": level,
                "measure": measure,
                "measure_short": SHORT.get(measure, measure),
                "value": value,
                "national": national[measure],
                "gap": round(value - national[measure], 1),
                "overall": overall,
            })

with open(OUT / "ses_study_area_2025.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["study_area", "study_area_short",
                                      "level", "measure", "measure_short",
                                      "value", "national", "gap", "overall"])
    w.writeheader()
    w.writerows(area)

# --------------------------------------------------- 3. class participation
part = []
for key, level in LEVELS.items():
    measures, rows = grid(wb[f"FOCUS_{key}_ALL_1Y_CLSPART"])
    for label, group, values in rows:
        if not group.startswith("Class participation"):
            continue
        for measure, value in zip(measures, values):
            if value is not None:
                part.append({"level": level, "participation": label,
                             "measure": measure, "value": value})

with open(OUT / "ses_class_participation_2025.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["level", "participation",
                                      "measure", "value"])
    w.writeheader()
    w.writerows(part)

# ---------------------------------------------------------------- 4. cohort
cohort = []
for key, level in LEVELS.items():
    rows = list(wb[f"CHARINT_{key}_ALL_1Y_AREA"].iter_rows(values_only=True))
    total = next(r for r in rows if r[1] == "All study areas")
    domestic = num(total[4])      # SES respondents: Domestic, n
    international = num(total[8])  # SES respondents: International, n
    for name, n in (("Domestic", domestic), ("International", international)):
        cohort.append({"level": level, "cohort": name, "respondents": int(n),
                       "share": round(100 * n / (domestic + international), 1)})

with open(OUT / "ses_cohort_2025.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["level", "cohort", "respondents", "share"])
    w.writeheader()
    w.writerows(cohort)

print(f"trend          {len(trend):4d} rows")
print(f"study area     {len(area):4d} rows")
print(f"participation  {len(part):4d} rows")
print(f"cohort         {len(cohort):4d} rows")
