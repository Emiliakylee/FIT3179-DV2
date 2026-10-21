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
const VERSION = "2026-10-21m";

const versioned = (url) =>
  url + (url.includes("?") ? "&" : "?") + "v=" + VERSION;

const FORMAT_BY_EXTENSION = {
  csv: "csv", tsv: "tsv", dsv: "dsv", json: "json", topojson: "topojson"
};

// The data files are referenced from inside each spec, so they need the
// version too; walk the spec and stamp every url it contains.
//
// Vega works out a data file's format from its extension, and the version
// query hides that extension ("data/x.csv" becomes "data/x.csv?v=..."), which
// silently leaves the chart with no rows. So state the format explicitly,
// from the real extension, before adding the version.
function versionDataUrls(node) {
  if (Array.isArray(node)) {
    node.forEach(versionDataUrls);
  } else if (node && typeof node === "object") {
    if (typeof node.url === "string") {
      const extension = node.url.split("?")[0].split(".").pop().toLowerCase();
      const format = FORMAT_BY_EXTENSION[extension];
      if (format) {
        node.format = node.format || {};
        if (!node.format.type) node.format.type = format;
      }
      node.url = versioned(node.url);
    }
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

// ---------------------------------------------------------------------------
// Page behaviour: reveal-on-scroll and the jump bar's current-section marker.
// Both are enhancements. The CSS that hides a .reveal is scoped to .js, which
// an inline script in <head> sets, so if any of this fails the page still
// shows everything.
// ---------------------------------------------------------------------------

(function () {
  const reveals = document.querySelectorAll(".reveal");

  if (!("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  // Reveal a little before the element reaches the middle of the window, so
  // the sentence has finished moving by the time the reader is looking at it.
  const revealer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealer.unobserve(entry.target);   // reveal once, never re-hide
      }
    }
  }, { rootMargin: "0px 0px -18% 0px", threshold: 0.1 });

  reveals.forEach((el) => revealer.observe(el));

  // Mark the section the reader is currently in.
  const links = new Map();
  document.querySelectorAll(".jump a[href^='#']").forEach((a) => {
    const id = a.getAttribute("href").slice(1);
    if (document.getElementById(id)) links.set(id, a);
  });

  if (!links.size) return;

  const setCurrent = (id) => {
    links.forEach((a, key) => a.classList.toggle("is-current", key === id));
  };

  const spy = new IntersectionObserver((entries) => {
    // The topmost section currently crossing the band below the jump bar wins.
    const visible = entries
      .filter((e) => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible.length) setCurrent(visible[0].target.id);
  }, { rootMargin: "-62px 0px -55% 0px", threshold: 0 });

  links.forEach((a, id) => spy.observe(document.getElementById(id)));
})();
