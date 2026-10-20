"""Generate curved flow paths so the 15 origin->Australia routes separate
instead of overlapping in one bundle.

Every flow shares a single destination (147.5, -33.0), so straight rules
collapse onto each other near Australia. Each flow is redrawn as a quadratic
Bezier whose control point is pushed perpendicular to the chord by an amount
that varies with the origin's position, fanning the routes apart in the middle
while still converging on the one destination.
"""
import csv, math

SRC  = "data/flows_top_countries_2024.csv"
OUT  = "data/flow_arcs.csv"
STEPS = 40          # vertices per arc
BOW   = (0.030, 0.085)   # curvature as a fraction of chord length
CAP   = 5.5              # ...capped in degrees, so long routes do not swing
                         # wide and stretch the projection's fitted extent

rows = list(csv.DictReader(open(SRC)))
for r in rows:
    for k in ("lon","lat","dest_lon","dest_lat"): r[k] = float(r[k])
    r["students"] = int(r["students"])

# Order by bearing to the destination so neighbouring routes get neighbouring
# curvature and the arcs never cross one another.
def bearing(r):
    return math.atan2(r["dest_lat"] - r["lat"], r["dest_lon"] - r["lon"])
rows.sort(key=bearing)

n = len(rows)
out = []
for i, r in enumerate(rows):
    x0, y0, x1, y1 = r["lon"], r["lat"], r["dest_lon"], r["dest_lat"]
    dx, dy = x1 - x0, y1 - y0
    chord = math.hypot(dx, dy)
    # perpendicular unit vector
    px, py = -dy / chord, dx / chord
    frac = BOW[0] + (BOW[1] - BOW[0]) * (i / (n - 1))
    k = min(chord * frac, CAP)
    cx, cy = (x0 + x1) / 2 + px * k, (y0 + y1) / 2 + py * k
    for s in range(STEPS + 1):
        t = s / STEPS
        u = 1 - t
        out.append({
            "country": r["country"], "region": r["region"],
            "students": r["students"], "step": s,
            "lon": u*u*x0 + 2*u*t*cx + t*t*x1,
            "lat": u*u*y0 + 2*u*t*cy + t*t*y1,
        })

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["country","region","students","step","lon","lat"])
    w.writeheader(); w.writerows(out)

print(f"{n} flows -> {len(out)} vertices in {OUT}")
print("curvature fraction per flow (by bearing):")
for i, r in enumerate(rows):
    print(f"   {r['country']:26s} {BOW[0]+(BOW[1]-BOW[0])*(i/(n-1)):.3f}")
