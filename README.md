# FIT3179 Data Visualisation 2

Student engagement in Australian higher education.
Author: [your name]. Last updated: [date].

Live page: https://[your-username].github.io/[repo-name]/

## Repository layout

```
index.html                  the single scrollable page
css/styles.css              layout and typography
js/main.js                  embeds each spec into its div
js/*.vg.json                one Vega-Lite spec per chart, pretty-printed
data/*.csv                  tidy data extracts (small)
data/*.topojson             simplified map geometry
img/                        sketch PDF, icons
```

One spec per file is what the assignment asks for: the JSON for every chart has
to be easy to find and easy to read in the repository.

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

| File | Source | Retrieved |
|---|---|---|
| `data/ses_overall_experience_2017_2025.csv` | 2025 Student Experience Survey National Report (QILT, Social Research Centre for the Australian Government Department of Education), Figures 1 and 2 | [date] |

Add a row here for every file. Re-check the transcribed trend figures against the
2025 SES National Report Tables before submitting.

Full source links:

- QILT Student Experience Survey: https://www.qilt.edu.au/surveys/student-experience-survey-(ses)
- Department of Education, Selected Higher Education Statistics 2024 student data: https://www.education.gov.au/higher-education-statistics/student-data/selected-higher-education-statistics-2024-student-data
- Department of Education, international student monthly data: https://www.education.gov.au/international-data/international-student-monthly-summary-and-data-tables
- ABS, ASGS Edition 3 digital boundary files: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files

## Notes

- Maps: convert shapefiles to TopoJSON at https://mapshaper.org, simplify to
  about 2-5%, and clip to Australia before exporting.
- Keep total downloaded data to a few megabytes.
- Acknowledge any use of AI tools on the page and in the Moodle submission.
