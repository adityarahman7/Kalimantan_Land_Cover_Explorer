import {areaUnit, formatArea} from "./area-units.mjs";

export function renderTrend(container, table, manifest, stats, code, selectedYear, onYear, unitKey = "km2") {
  container.replaceChildren();
  table.replaceChildren();
  if (!stats) return;
  const unit = areaUnit(unitKey);
  const headers = table.closest("table").querySelectorAll("th");
  headers[1].textContent = `Luas kelas (${unit.label})`;
  headers[2].textContent = `Area valid (${unit.label})`;
  const definition = manifest.classes.find(item => item.code === code);
  const index = manifest.class_order.indexOf(code);
  const number = new Intl.NumberFormat("id-ID", {maximumFractionDigits: 2});
  const coverage = new Intl.NumberFormat("id-ID", {maximumFractionDigits: 4});
  const series = manifest.years.map(year => ({
    year, area: stats.annual_area_ha[year][index] / unit.divisor, valid: stats.annual_valid_ha[year] / unit.divisor,
  }));
  const selectedYears = Array.isArray(selectedYear) ? selectedYear : [selectedYear];
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  const chartWidth = Math.max(container.clientWidth, 540);
  svg.setAttribute("viewBox", `0 0 ${chartWidth} 160`);
  svg.setAttribute("role", "group");
  svg.setAttribute("aria-label", `Grafik luas ${definition.label} di ${stats.region_name}, dalam ${unit.label}.`);
  const lineColor = `color-mix(in srgb, ${definition.color} 65%, #e6f2d5)`;
  function shape(tag, attributes, text) {
    const node = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
    if (text !== undefined) node.textContent = text;
    svg.append(node);
    return node;
  }
  const max = Math.max(...series.map(p => p.area), 1) * 1.08;
  const x = year => 62 + (year - manifest.years[0]) / (manifest.years.at(-1) - manifest.years[0]) * (chartWidth - 88);
  const y = area => 126 - area / max * 102;
  for (let i = 0; i <= 4; i++) {
    const value = max * i / 4;
    shape("line", {x1: 62, x2: chartWidth - 26, y1: y(value), y2: y(value), stroke: "#3c5141", "stroke-dasharray": "3 6"});
    shape("text", {x: 54, y: y(value) + 4, "text-anchor": "end", "font-size": 13, fill: "#b4c6a9"},
      new Intl.NumberFormat("id-ID", {notation: "compact", maximumFractionDigits: 1}).format(value));
  }
  shape("text", {x: 62, y: 12, "font-size": 12, fill: "#b4c6a9"}, `Luas (${unit.label})`);
  const defs = document.createElementNS(ns, "defs");
  const gradient = document.createElementNS(ns, "linearGradient");
  gradient.id = "trend-area-gradient";
  gradient.setAttribute("x1", "0"); gradient.setAttribute("x2", "0");
  gradient.setAttribute("y1", "0"); gradient.setAttribute("y2", "1");
  for (const [offset, opacity] of [["0%", ".35"], ["100%", ".015"]]) {
    const stop = document.createElementNS(ns, "stop");
    stop.setAttribute("offset", offset); stop.setAttribute("stop-color", lineColor); stop.setAttribute("stop-opacity", opacity);
    gradient.append(stop);
  }
  defs.append(gradient); svg.append(defs);
  shape("polygon", {points: `${x(series[0].year)},126 ${series.map(p => `${x(p.year)},${y(p.area)}`).join(" ")} ${x(series.at(-1).year)},126`, fill: "url(#trend-area-gradient)"});
  shape("polyline", {points: series.map(p => `${x(p.year)},${y(p.area)}`).join(" "),
    fill: "none", stroke: lineColor, "stroke-width": 3, "stroke-linejoin": "round"});
  const summary = document.createElement("div");
  summary.className = "trend-summary";
  const first = series[0], last = series.at(-1);
  const deltaHa = (last.area - first.area) * unit.divisor;
  for (const [label, value, className] of [
    [`${first.year}`, formatArea(first.area * unit.divisor, unitKey), ""],
    [`${last.year}`, formatArea(last.area * unit.divisor, unitKey), ""],
    [`Perubahan ${first.year}–${last.year}`, `${deltaHa > 0 ? "+" : deltaHa < 0 ? "−" : ""}${formatArea(Math.abs(deltaHa), unitKey)}`, "trend-delta"],
  ]) {
    const item = document.createElement("p"); item.className = className;
    const strong = document.createElement("strong"); strong.textContent = value;
    item.append(document.createTextNode(label), strong); summary.append(item);
  }
  for (const point of series) {
    if (selectedYears.includes(point.year)) {
      shape("line", {x1: x(point.year), x2: x(point.year), y1: 20, y2: 126,
        stroke: "#c4dc9f", "stroke-dasharray": "4 4"});
    }
    const dot = shape("circle", {cx: x(point.year), cy: y(point.area), r: selectedYears.includes(point.year) ? 6 : 4,
      fill: selectedYears.includes(point.year) ? "#e7f5cd" : lineColor, stroke: "#1a2721", "stroke-width": 2, tabindex: 0, role: "button",
      "aria-pressed": String(selectedYears.includes(point.year)),
      "aria-label": `${point.year}, ${number.format(point.area)} ${unit.label}. Pilih tahun ini.`});
    const title = document.createElementNS(ns, "title");
    title.textContent = `${point.year} · ${number.format(point.area)} ${unit.label}`;
    dot.append(title);
    dot.addEventListener("click", () => onYear(point.year));
    dot.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        onYear(point.year);
      }
    });
    if (point.year % 2 === 0 || point.year === manifest.years[0] || point.year === manifest.years.at(-1)) {
      shape("text", {x: x(point.year), y: 150, "text-anchor": "middle", "font-size": 13, fill: "#b4c6a9"}, point.year);
    }
    const row = document.createElement("tr");
    for (const value of [point.year, number.format(point.area), number.format(point.valid),
      point.valid > 0 ? number.format(point.area / point.valid * 100) + "%" : "—",
      stats.summary.aoi_ha > 0 ? coverage.format(point.valid * unit.divisor / stats.summary.aoi_ha * 100) + "%" : "—"]) {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.append(cell);
    }
    table.append(row);
  }
  container.append(summary, svg);
}
