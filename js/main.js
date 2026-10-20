// Each chart lives in its own .vg.json file so the specs stay readable
// in the repository. Add one line here per chart.

const specs = {
  "#vis-trend": "js/01_trend.vg.json",
  "#vis-dumbbell": "js/03_focus_dumbbell.vg.json",
  "#vis-heatmap": "js/02_study_area_heatmap.vg.json",
  "#vis-slope": "js/04_level_slope.vg.json",
  "#vis-parallel": "js/05_parallel_profiles.vg.json",
  "#vis-symbols": "js/06_state_symbols.vg.json",
  "#vis-choropleth": "js/07_state_choropleth.vg.json",
  "#vis-spikes": "js/11_sa4_spikes.vg.json",
  "#vis-flows": "js/12_origin_flows.vg.json",
  "#vis-waffle": "js/08_cohort_waffle.vg.json",
  "#vis-attendance": "js/09_attendance_lollipop.vg.json",
  "#vis-spread": "js/10_spread_comparison.vg.json"
};

const options = {
  actions: false,   // hides the export / Vega Editor menu
  renderer: "svg"
};

// Browsers and the GitHub Pages CDN cache .json and .csv files aggressively,
// so an edited spec or dataset can keep serving its old copy after a reload.
// Adding a version to every request forces a fresh fetch.
// BUMP THIS after editing anything in js/ or data/.
const VERSION = "2026-10-21a";

const versioned = (url) =>
  url + (url.includes("?") ? "&" : "?") + "v=" + VERSION;

// The data files are referenced from inside each spec, so they need the
// version too; walk the spec and stamp every url it contains.
function versionDataUrls(node) {
  if (Array.isArray(node)) {
    node.forEach(versionDataUrls);
  } else if (node && typeof node === "object") {
    if (typeof node.url === "string") node.url = versioned(node.url);
    Object.values(node).forEach(versionDataUrls);
  }
  return node;
}

async function draw(selector, path) {
  const response = await fetch(versioned(path));
  if (!response.ok) throw new Error("HTTP " + response.status + " for " + path);
  const spec = versionDataUrls(await response.json());
  return vegaEmbed(selector, spec, options);
}

// A chart that fails used to leave an empty box with the reason buried in the
// console. Say so on the page instead, naming the file that failed.
function reportFailure(selector, path, error) {
  console.error(path, error);
  const host = document.querySelector(selector);
  if (!host) return;
  const note = document.createElement("p");
  note.className = "vis-error";
  note.textContent = "This chart could not load (" + path + "): " + error.message;
  host.appendChild(note);
}

for (const [selector, path] of Object.entries(specs)) {
  if (document.querySelector(selector)) {
    draw(selector, path).catch((error) => reportFailure(selector, path, error));
  }
}
