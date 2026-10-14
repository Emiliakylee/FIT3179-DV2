"""Derive two small files that Vega-Lite can't build itself.

  data/cohort_waffle.csv   100 squares per level for the waffle chart (C10)
  data/spread_summary.csv  range and middle 80% per lens (C12)

Usage: python3 scripts/build_derived.py
Inputs are the extracted CSVs in data/.
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# ------------------------------------------------------------ waffle (C10)
cohort = list(csv.DictReader(open(DATA / "ses_cohort_2025.csv")))
squares = []
for level in ["Undergraduate", "Postgraduate"]:
    rows = {r["cohort"]: float(r["share"]) for r in cohort if r["level"] == level}
    intl = round(rows["International"])
    for i in range(100):
        squares.append({
            "level": level,
            "index": i,
            "col": i % 10,
            "row": i // 10,
            "cohort": "International" if i < intl else "Domestic",
            "level_label": ("Postgraduate coursework" if level == "Postgraduate"
                            else "Undergraduate"),
        })

with open(DATA / "cohort_waffle.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["level", "level_label", "index", "col",
                                      "row", "cohort"])
    w.writeheader()
    w.writerows(squares)

# ------------------------------------------------------------ spread (C12)
def quantile(values, p):
    values = sorted(values)
    i = (len(values) - 1) * p
    lo = int(i)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (i - lo)


spread = list(csv.DictReader(open(DATA / "ses_spread_2025.csv")))
summary = []
for lens in ["States and territories", "Universities", "Study areas"]:
    for level in ["Undergraduate", "Postgraduate"]:
        v = [float(r["value"]) for r in spread
             if r["lens"] == lens and r["level"] == level]
        if not v:
            continue
        summary.append({
            "lens": lens,
            "level": level,
            "n": len(v),
            "min": round(min(v), 1),
            "max": round(max(v), 1),
            "p10": round(quantile(v, 0.10), 1),
            "p90": round(quantile(v, 0.90), 1),
            "median": round(quantile(v, 0.50), 1),
            "middle80": round(quantile(v, 0.90) - quantile(v, 0.10), 1),
            "label": f"{lens} (n={len(v)})",
        })

with open(DATA / "spread_summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["lens", "level", "n", "min", "max",
                                      "p10", "p90", "median", "middle80",
                                      "label"])
    w.writeheader()
    w.writerows(summary)

print(f"waffle squares : {len(squares)}")
for s in summary:
    print(f"  {s['level'][:4]} {s['lens']:<24} n={s['n']:>3} "
          f"range {s['min']}-{s['max']}  middle80 {s['middle80']}")
