"""Three vertices per region so the spike map can draw filled triangles.

Vega-Lite has no length-proportional triangle mark: `size` sets a symbol's
area, not its height. Drawing the triangle as a closed line through three
points gives a mark whose HEIGHT encodes the count, which is what the
proportional-symbol notes call a length-proportional symbol.

Two panels at different zooms need different base widths and heights in
degrees, so each gets its own set of columns.
"""
import csv

SRC = "data/international_by_sa4_2025.csv"
OUT = "data/sa4_triangles.csv"
TOP_N = 20

# (base half-width in degrees, height per student in degrees)
# Each panel carries its OWN symbol scale, because the zoom shows ~50 px per
# degree against the national map's ~17: matching the two would leave the
# zoomed triangles looking three times smaller than the land around them.
# The legend strip therefore shows a key for each panel.
NATIONAL = (0.52, 0.000075)
DETAIL   = (0.055, 0.000050)

rows = [r for r in csv.DictReader(open(SRC))]
for r in rows:
    r["enrolments"] = float(r["enrolments"]); r["lon"] = float(r["lon"]); r["lat"] = float(r["lat"])
rows.sort(key=lambda r: -r["enrolments"])
keep = rows[:TOP_N]

out = []
for r in keep:
    for (half, k), pre in ((NATIONAL, "nat"), (DETAIL, "det")):
        apex = r["lat"] + r["enrolments"] * k
        verts = [(r["lon"] - half, r["lat"]), (r["lon"], apex), (r["lon"] + half, r["lat"])]
        for i, (lon, lat) in enumerate(verts):
            out.append({"sa4_name": r["sa4_name"], "state": r["state"],
                        "enrolments": int(r["enrolments"]), "vertex": i,
                        "panel": pre, "lon": round(lon, 4), "lat": round(lat, 4),
                        "apex_lat": round(apex, 4),
                        # centre and base, for the invisible hover target
                        "cx": round(r["lon"], 4), "base_lat": round(r["lat"], 4)})

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)

print(f"{len(keep)} regions -> {len(out)} vertex rows -> {OUT}")
print(f"largest: {keep[0]['sa4_name']} {keep[0]['enrolments']:,.0f}")
print(f"smallest kept: {keep[-1]['sa4_name']} {keep[-1]['enrolments']:,.0f}")
print(f"share of all international students: "
      f"{sum(r['enrolments'] for r in keep)/sum(r['enrolments'] for r in rows)*100:.1f}%")
