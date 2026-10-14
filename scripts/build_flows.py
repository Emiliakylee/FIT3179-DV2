"""Build the flow map data (C12): top source countries into Australia.

Usage: python3 scripts/build_flows.py

Country positions come from the Natural Earth 1:110m countries file, via:
    mapshaper data/world_countries.topojson -target ne_110m_admin_0_countries \
        -points inner -o format=geojson /tmp/world_pts.json

Sources: Department of Education, Selected Higher Education Statistics 2024,
Table 7.4 (overseas students by country of permanent home residence);
Natural Earth 1:110m Admin 0 Countries (public domain).
"""
import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
POINTS = Path("/tmp/world_pts.json")
TOP_N = 15

# Department names that differ from Natural Earth's
ALIAS = {
    "China (excludes SARs and Taiwan)": "China",
    "Korea, Republic of (South)": "South Korea",
    "Taiwan": "Taiwan",
    "United States of America": "United States of America",
}

# City states too small to appear in the 1:110m boundary file
MANUAL = {
    "Singapore": (103.82, 1.35),
    "Hong Kong (SAR of China)": (114.17, 22.32),
    "Macau (SAR of China)": (113.55, 22.17),
}

SKIP = {"Overseas country not known", "Not elsewhere included"}

# Destination point: roughly the east-coast universities most students attend
DEST = (147.5, -33.0)

points = {}
for f in json.load(open(POINTS))["features"]:
    p = f["properties"]
    lon, lat = f["geometry"]["coordinates"]
    for key in ("NAME", "NAME_LONG", "ADMIN", "SOVEREIGNT"):
        if p.get(key):
            points.setdefault(p[key], (lon, lat))

rows, missing = [], []
for r in csv.DictReader(open(DATA / "overseas_by_country_2024.csv")):
    name = r["country"]
    if name in SKIP:
        continue
    coords = MANUAL.get(name) or points.get(ALIAS.get(name, name))
    if coords is None:
        missing.append(name)
        continue
    rows.append({
        "country": ALIAS.get(name, name),
        "region": r["region"],
        "students": int(r["students"]),
        "lon": round(coords[0], 3),
        "lat": round(coords[1], 3),
        "dest_lon": DEST[0],
        "dest_lat": DEST[1],
    })

rows.sort(key=lambda r: -r["students"])
rows = rows[:TOP_N]
total = sum(int(r["students"]) for r in csv.DictReader(
    open(DATA / "overseas_by_country_2024.csv")))
shown = sum(r["students"] for r in rows)

with open(DATA / "flows_top_countries_2024.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["country", "region", "students", "lon",
                                      "lat", "dest_lon", "dest_lat"])
    w.writeheader()
    w.writerows(rows)

print(f"flows written : {len(rows)}")
print(f"covering      : {shown:,} of {total:,} overseas students "
      f"({100 * shown / total:.1f}%)")
if missing[:10]:
    print(f"unmatched (not in top set if blank): {missing[:10]}")
for r in rows[:6]:
    print(f"   {r['country']:<22} {r['students']:>8,}")
