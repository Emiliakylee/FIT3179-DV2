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

for (const [selector, path] of Object.entries(specs)) {
  if (document.querySelector(selector)) {
    vegaEmbed(selector, path, options).catch(console.error);
  }
}
