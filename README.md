# FIT3179 Data Visualisation 2

Student engagement in higher education.
Author: Emilia Kim Yoon Lee 34537910. Last updated: 21/10/2026

Live page: https://emiliakylee.github.io/FIT3179-DV2/

## Repository layout

```
index.html                  the single scrollable page
css/styles.css              layout and typography
js/main.js                  embeds each spec into its div
js/*.vg.json                one Vega-Lite spec per chart, pretty-printed
data/*.csv                  tidy data extracts
data/*.topojson             simplified map geometry
img/                        sketch PDF
```

## Local setup

1. Open the folder in VS Code.
2. Install the extensions **Live Server** (preview the page) and **Vega Viewer**
   (preview a `.vg.json` on its own with F1 → "Vega: Preview Vega Graph").
3. Right-click `index.html` → "Open with Live Server". Charts load by relative
   path, so opening the file directly with `file://` will fail.

## Publishing

1. Create a public GitHub repository and push this folder.
2. Settings → Pages → Source: deploy from branch `main`, folder `/root`.
3. Open the published URL in a private window to confirm everything is public.
   The assignment is marked 0 if the page or any embedded file isn't reachable.

## Data sources

Every file in `data/` is listed. The original downloads are kept in `data/raw/`,
so each extraction can be rerun and checked.

### Source data

| File | Source | Retrieved |
|---|---|---|
| `data/ses_trend_2017_2025.csv` | QILT, 2025 Student Experience Survey National Report Tables — overall experience by year and level | 14 Oct 2026 |
| `data/ses_study_area_2025.csv` | QILT, 2025 SES National Report Tables — each measure by study area and level | 14 Oct 2026 |
| `data/ses_class_participation_2025.csv` | QILT, 2025 SES National Report Tables — each measure by how classes were attended | 14 Oct 2026 |
| `data/ses_cohort_2025.csv` | QILT, 2025 SES National Report Tables — domestic and international respondents by level | 14 Oct 2026 |
| `data/ses_state_2025.csv` | QILT, 2025 SES National Report Tables, sheets `FOCUS_UG_UNI_1Y_INST_CI`, `FOCUS_PGC_UNI_1Y_INST_CI`, `RR_ALL_UNI_17-YY_INST` — institution results grouped to state and weighted by responses | 14 Oct 2026 |
| `data/ses_spread_2025.csv` | QILT, 2025 SES National Report Tables, same sheets — one value per group for each of the three lenses | 14 Oct 2026 |
| `data/enrolments_by_state_2024.csv` | Department of Education, Selected Higher Education Statistics 2024 Student Data, Tables 2.5 and 2.12 | 14 Oct 2026 |
| `data/overseas_by_country_2024.csv` | Department of Education, Selected Higher Education Statistics 2024 Student Data, Table 7.4 — overseas students by country of permanent home residence | 14 Oct 2026 |
| `data/international_by_sa4_2025.csv` | Department of Education, International Student Enrolments and Commencements by SA4 Location, year to date December 2025 (PRISMS), joined to SA4 label points | 14 Oct 2026 |
| `data/au_states.topojson` | ABS, ASGS Edition 3 state and territory boundaries (`STE_2021_AUST_GDA2020`), simplified to TopoJSON | 14 Oct 2026 |
| `data/au_sa4.topojson` | ABS, ASGS Edition 3 SA4 boundaries (`SA4_2021_AUST_GDA2020`), simplified to TopoJSON | 14 Oct 2026 |
| `data/world_countries.topojson` | Natural Earth 1:110m Admin 0 Countries, public domain | 14 Oct 2026 |

### Built from the files above

These are generated, not downloaded. Rerun any script to rebuild its output.

| File | Built by | From |
|---|---|---|
| `data/cohort_waffle.csv` | `scripts/build_derived.py` | `ses_cohort_2025.csv` — 100 squares per level |
| `data/spread_summary.csv` | `scripts/build_derived.py` | `ses_spread_2025.csv` — range and middle 80% per lens |
| `data/flows_top_countries_2024.csv` | `scripts/build_flows.py` | `overseas_by_country_2024.csv` + `world_countries.topojson` for origin points |
| `data/flow_arcs.csv` | `scripts/build_flow_arcs.py` | `flows_top_countries_2024.csv` — curved paths so routes separate |
| `data/sa4_triangles.csv` | `scripts/build_spike_triangles.py` | `international_by_sa4_2025.csv` — three vertices per region |
| `data/state_centroids.csv` | mapshaper, `-points inner` | `au_states.topojson` |
| `data/state_label_points.csv` | mapshaper, `-points inner`, nudged by hand where a label collided | `au_states.topojson` |

### Extraction scripts

| Script | Writes |
|---|---|
| `scripts/extract_ses.py` | `ses_trend_2017_2025.csv`, `ses_study_area_2025.csv`, `ses_class_participation_2025.csv`, `ses_cohort_2025.csv` |
| `scripts/extract_institutions.py` | `ses_state_2025.csv`, `ses_spread_2025.csv` |
| `scripts/extract_education.py` | `enrolments_by_state_2024.csv`, `overseas_by_country_2024.csv` |
| `scripts/extract_sa4.py` | `international_by_sa4_2025.csv` |
| `scripts/build_derived.py` | `cohort_waffle.csv`, `spread_summary.csv` |
| `scripts/build_flows.py` | `flows_top_countries_2024.csv` |
| `scripts/build_flow_arcs.py` | `flow_arcs.csv` |
| `scripts/build_spike_triangles.py` | `sa4_triangles.csv` |

`extract_institutions.py` reads institution names only to map each university to
a state and to weight the state averages. No institution name is written to any
output file, so nothing in this repository can be read as a university ranking.

### Full source links

- QILT Student Experience Survey: https://www.qilt.edu.au/surveys/student-experience-survey-(ses)
- Department of Education, Selected Higher Education Statistics 2024 student data: https://www.education.gov.au/higher-education-statistics/student-data/selected-higher-education-statistics-2024-student-data
- Department of Education, international student monthly data: https://www.education.gov.au/international-data/international-student-monthly-summary-and-data-tables
- ABS, ASGS Edition 3 digital boundary files: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files
- Natural Earth 1:110m Admin 0 Countries: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/

## Notes

- Maps: convert shapefiles to TopoJSON at https://mapshaper.org, simplify to
  about 2-5%, and clip to Australia before exporting.
- Keep total downloaded data to a few megabytes.
- Acknowledge any use of AI tools on the page and in the Moodle submission.
