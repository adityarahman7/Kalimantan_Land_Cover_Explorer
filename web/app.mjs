import {loadExplorer} from "./explorer-data.mjs";
import {renderTrend} from "./trend-chart.mjs?v=dark-4";
import {createMap} from "./raster-map.mjs?v=dark-4";
import {areaUnit, formatArea} from "./area-units.mjs";

const $ = id => document.getElementById(id);
const fmt = new Intl.NumberFormat("id-ID", {maximumFractionDigits: 2});
const ha = area => formatArea(area, $("area-unit").value);
const percent = (area, total) => total > 0 ? `${fmt.format(100 * area / total)}%` : "—";
const invalid = {label: "Data tahun ini tidak valid", color: "#747b86"};
const highlight = "#a22677";

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function addOptions(id, options) {
  $(id).replaceChildren(...options.map(([value, label]) => new Option(label, value)));
}

function showRetry(id, message, retry) {
  const button = element("button", "Coba lagi");
  button.addEventListener("click", retry);
  $(id).replaceChildren(document.createTextNode(message), button);
}

function swatch(color) {
  const mark = element("span", undefined, "swatch");
  mark.style.backgroundColor = color;
  mark.setAttribute("aria-hidden", "true");
  return mark;
}

async function initialize() {
  $("startup").textContent = "Menyiapkan peta dan statistik wilayah…";
  try {
    const data = await loadExplorer();
    const {manifest} = data;
    const levels = Object.keys(manifest.boundaries);
    const [pairs, ...collections] = await Promise.all([
      data.getRasterPair(2010, 2024),
      ...levels.map(level => data.getBoundaries(level)),
    ]);
    const boundaries = collections.flatMap(({features}, index) => {
      const level = levels[index];
      return features.map(({geometry, properties}) => ({
        level, geometry, id: properties[manifest.boundaries[level].id_field],
      }));
    });
    const map = createMap($("map"), manifest.raster, pairs, boundaries);
    fetch(new URL("./public/context/regional-land.geojson", import.meta.url))
      .then(response => { if (!response.ok) throw new Error("Basemap tidak tersedia"); return response.json(); })
      .then(context => { map.setBasemap(context); $("basemap-status").textContent = "Natural Earth · konteks regional"; })
      .catch(() => { $("basemap-status").textContent = "Basemap konteks tidak tersedia"; });
    connect(data, map);
    $("startup").hidden = true;
  } catch (error) {
    console.error(error);
    showRetry("startup", "Peta gagal dimuat. Periksa paket data lokal.", initialize);
  }
}

function connect(data, map) {
  const {manifest} = data;
  $("data-release").textContent = manifest.release === "R1" ? "Pilot R1 · 2010 & 2024" : "Data tahunan · 2010–2024";
  $("data-availability").hidden = manifest.release !== "R1";
  $("trend-scope").textContent = manifest.release === "R1" ? "Garis menghubungkan dua pengamatan; tahun di antaranya tidak tersedia." : "";
  const classes = manifest.class_order.map(code => manifest.classes.find(item => item.code === code));
  const classByCode = new Map(classes.map(item => [item.code, item]));
  const regionById = new Map(manifest.region_index.map(region => [region.region_id, region]));
  const provinces = manifest.region_index.filter(region => region.region_level === "province");
  const districts = manifest.region_index.filter(region => region.region_level === "district");
  const classOptions = [["", "Semua kelas"], ...classes.map(({code, label}) => [code, label])];
  const statsCache = new Map();
  let request = 0;
  let regionId;
  let mapRegionId;
  let activeStats;
  let paletteKey;
  let activeRegion;
  addOptions("province", [["", "Seluruh Kalimantan"], ...provinces.map(r => [r.region_id, r.region_name])]);
  addOptions("year", manifest.years.map(year => [year, year]));
  addOptions("from", classOptions);
  addOptions("to", classOptions);
  $("year").value = manifest.default_year;
  addOptions("year-from", manifest.years.slice(0, -1).map(year => [year, year]));
  $("year-from").value = "2010";
  function updateEndYears() {
    const previous = Number($("year-to").value) || 2024;
    const available = manifest.years.filter(year => year > Number($("year-from").value));
    addOptions("year-to", available.map(year => [year, year]));
    $("year-to").value = available.includes(previous) ? previous : available[0];
  }
  updateEndYears();
  addOptions("chart-class", classes.map(({code, label}) => [code, label]));
  $("chart-class").value = "35";
  $("metadata").hidden = false;
  $("filters").hidden = false;
  $("explorer").hidden = false;

  function refresh() {
    const annual = $("mode").value === "annual";
    const year = Number($("year").value);
    const from = Number($("from").value);
    const to = Number($("to").value);
    const filtered = !annual && Boolean(from || to);
    const matches = (before, after) => before && after && (!from || before === from) && (!to || after === to);
    const filterTitle = `${classByCode.get(from)?.label ?? "Semua kelas"} → ${classByCode.get(to)?.label ?? "Semua kelas"}`;
    const first = Number($("year-from").value), last = Number($("year-to").value);
    const modeLabel = annual ? `Tutupan lahan ${year}` : `Perubahan ${first} → ${last}`;
    const region = regionById.get(regionId);
    $("annual-controls").hidden = !annual;
    $("transition-controls").hidden = annual;
    $("mode-help").textContent = annual ? "Lihat jenis tutupan lahan pada satu tahun." : "Bandingkan dua tahun, lalu saring kelas bila diperlukan.";
    $("year-prev").disabled = year === manifest.years[0];
    $("year-next").disabled = year === manifest.years.at(-1);
    $("map-title").textContent = region.region_name;
    $("map-mode").textContent = modeLabel;
    $("stats-title").textContent = `${modeLabel} · ${region.region_name}`;
    $("selection-caption").textContent = region.region_name;
    $("map").setAttribute("aria-label", `${modeLabel}, ${region.region_name}${filtered ? `, ${filterTitle}` : ""}. Tersedia tombol zum dan pas wilayah.`);

    const change = manifest.change_legend;
    const filterLegend = [{label: filterTitle, color: highlight}, {label: "Transisi valid lainnya", color: "#b8c8bb"}, change[2]];
    const legend = annual ? [...classes, invalid] : filtered ? filterLegend : change;
    $("legend").replaceChildren(...legend.map(({label, color}) => {
      const item = element("li", label);
      item.prepend(swatch(color));
      return item;
    }));
    const key = annual ? String(year) : `${first}/${last}/${from}/${to}`;
    if (activeStats && key !== paletteKey) {
      const colors = [];
      const codes = [manifest.raster.invalid_class, ...manifest.class_order];
      for (const before of codes) {
        for (const after of codes) {
          let color;
          if (annual) color = (classByCode.get(before) ?? invalid).color;
          else if (!before || !after) color = change[2].color;
          else if (filtered) color = matches(before, after) ? highlight : filterLegend[1].color;
          else color = change[Number(before !== after)].color;
          colors.push([100 * before + after, color]);
        }
      }
      map.paint(colors);
      paletteKey = key;
    }

    $("cards").replaceChildren();
    $("insight").hidden = true;
    $("rows").replaceChildren();
    $("composition-bars").replaceChildren();
    $("chart-note").textContent = "";
    $("stats-table").hidden = true;
    if (!activeStats) return;
    const {summary, annual_area_ha: areas, transition_area_ha: matrix} = activeStats;
    const total = annual ? summary[`valid_${year}_ha`] : summary.valid_common_ha;
    const list = [];
    const cards = annual
      ? [["Luas wilayah", ha(summary.aoi_ha)], [`Area valid ${year}`, ha(total)],
        ["Cakupan valid", percent(total, summary.aoi_ha)]]
      : [["Area valid bersama", ha(total)], ["Tidak dapat dibandingkan", ha(summary.not_comparable_ha)]];
    if (annual) {
      classes.forEach(({code, label, color}, index) => list.push([`${label} (${code})`, areas[year][index], color]));
    } else if (filtered) {
      let area = 0;
      classes.forEach((a, row) => classes.forEach((b, col) => {
        if (matches(a.code, b.code)) area += matrix[row][col];
      }));
      cards.unshift(["Luas transisi terpilih", ha(area)], ["Proporsi transisi terpilih", percent(area, total)]);
      list.push([filterTitle, area, highlight]);
      if (total > 0 && area === 0) $("stats-status").textContent = "Tidak ada piksel valid untuk kombinasi kelas ini di wilayah terpilih.";
    } else {
      cards.unshift(["Luas berubah kelas", ha(summary.changed_ha)], ["Proporsi berubah kelas", percent(summary.changed_ha, total)]);
      list.push([change[0].label, summary.stable_ha, change[0].color], [change[1].label, summary.changed_ha, change[1].color],
        [change[2].label, summary.not_comparable_ha, change[2].color, true]);
    }
    if (!total) $("stats-status").textContent = "Area valid untuk pilihan ini tidak tersedia. Proporsi tidak dapat dihitung.";
    $("chart-note").textContent = annual ? `Proporsi dari area valid tahun ${year}.` : "Proporsi dari area valid pada kedua tahun.";
    $("composition-title").textContent = annual ? "Tutupan lahan dalam angka" : filtered ? "Transisi yang dipilih" : "Apa yang berubah?";
    const dominant = annual ? list.reduce((largest, item) => item[1] > largest[1] ? item : largest, list[0]) : null;
    $("insight").textContent = annual
      ? `${dominant[0].replace(/ \(\d+\)$/, "")} merupakan kelas terluas yang terpetakan: ${percent(dominant[1], total)} dari area valid tahun ${year}.`
      : filtered ? `Transisi ${filterTitle.toLowerCase()} mencakup ${percent(list[0][1], total)} dari area yang valid pada kedua tahun.`
      : `${percent(summary.changed_ha, total)} dari area valid bersama berubah kelas pada ${first}–${last}. Perubahan kelas tidak selalu berarti deforestasi.`;
    $("insight").hidden = false;
    $("table-label").textContent = annual ? "Kelas" : filtered ? "Transisi" : "Status perubahan";
    // Shares use one common denominator; excluded records have no percentage.
    list.sort((a, b) => Number(Boolean(a[3])) - Number(Boolean(b[3])) || b[1] - a[1]);
    const unit = areaUnit($("area-unit").value);
    $("area-column").textContent = `Luas (${unit.label})`;
    $("composition-bars").replaceChildren(...list.filter(([, area, , excluded]) => area > 0 && !excluded).map(([label, area, color]) => {
      const segment = element("span");
      segment.style.width = total > 0 ? `${100 * area / total}%` : "0%";
      segment.style.backgroundColor = color;
      segment.title = `${label}: ${percent(area, total)}`;
      segment.setAttribute("aria-label", segment.title);
      return segment;
    }));
    $("cards").replaceChildren(...cards.map(([label, value]) => {
      const card = element("div", undefined, "card");
      const strong = element("strong");
      const match = value.match(/^(.*) (km²|ha)$/);
      if (match) strong.append(document.createTextNode(match[1]), element("span", ` ${match[2]}`, "value-unit"));
      else strong.textContent = value;
      card.append(element("p", label), strong);
      return card;
    }));
    $("rows").replaceChildren(...list.map(([label, area, color, excluded]) => {
      const row = element("tr");
      row.dataset.areaHa = area;
      const name = element("td", label);
      name.prepend(swatch(color));
      if (!excluded && total > 0) {
        name.className = "area-cell";
        name.style.setProperty("--area-share", `${100 * area / total}%`);
        name.style.setProperty("--area-color", color);
      }
      const areaCell = element("td", fmt.format(area / unit.divisor));
      areaCell.dataset.unit = unit.label;
      row.append(name, areaCell, element("td", excluded ? "—" : percent(area, total)));
      return row;
    }));
    $("stats-table").hidden = false;
  }

  async function selectRegion() {
    const id = $("district").value || $("province").value || manifest.default_region_id;
    const annual = $("mode").value === "annual";
    const before = Number(annual ? $("year").value : $("year-from").value);
    const after = Number(annual ? $("year").value : $("year-to").value);
    const token = ++request;
    const changedRegion = mapRegionId !== id;
    regionId = id;
    activeStats = null;
    activeRegion = null;
    $("stats-status").textContent = "Memuat peta dan statistik…";
    $("map").style.visibility = "hidden";
    $("trend-chart").replaceChildren();
    $("trend-rows").replaceChildren();
    refresh();
    try {
      const [stats, pixels] = await Promise.all([
        statsCache.get(id) ?? data.getStats(id), data.getRasterPair(before, after),
      ]);
      if (token !== request) return;
      statsCache.set(id, stats);
      activeRegion = stats;
      const paired = annual ? null : stats.pairs[`${before}_${after}`];
      if (!annual && !paired) throw new Error("Statistik pasangan tahun tidak tersedia.");
      activeStats = {
        ...stats,
        summary: annual ? {...stats.summary, [`valid_${before}_ha`]: stats.annual_valid_ha[before]} : paired.summary,
        transition_area_ha: paired?.transition_area_ha,
      };
      map.setPairs(pixels);
      if (changedRegion) {
        map.selectRegion(id);
        mapRegionId = id;
      }
      paletteKey = null;
      $("stats-status").textContent = "";
      refresh();
      $("map").style.visibility = "visible";
      drawTrend();
    } catch (error) {
      if (token !== request) return;
      activeStats = null;
      activeRegion = null;
      $("map").style.visibility = "hidden";
      $("trend-chart").replaceChildren();
      $("trend-rows").replaceChildren();
      refresh();
      console.error(error);
      showRetry("stats-status", "Peta atau statistik pilihan ini gagal dimuat.", selectRegion);
    }
  }

  function drawTrend() {
    renderTrend($("trend-chart"), $("trend-rows"), manifest, activeRegion,
      Number($("chart-class").value), $("mode").value === "annual" ? Number($("year").value)
        : [Number($("year-from").value), Number($("year-to").value)], year => {
        $("year").value = year;
        $("mode").value = "annual";
        selectRegion();
      }, $("area-unit").value);
  }

  $("province").addEventListener("change", () => {
    const province = $("province").value;
    addOptions("district", [["", "Semua kabupaten/kota"],
      ...districts.filter(r => r.province_id === province).map(r => [r.region_id, r.region_name])]);
    $("district").disabled = !province;
    $("district-hint").textContent = province ? "Persempit wilayah atau lihat seluruh provinsi." : "Pilih provinsi untuk melihat kabupaten/kota.";
    selectRegion();
  });
  $("district").addEventListener("change", selectRegion);
  for (const id of ["mode", "year", "from", "to", "year-from", "year-to"]) {
    $(id).addEventListener("change", () => {
      if (id === "year-from") updateEndYears();
      selectRegion();
    });
  }
  $("chart-class").addEventListener("change", drawTrend);
  $("area-unit").addEventListener("change", () => { refresh(); drawTrend(); });
  let chartWidth = 0;
  new ResizeObserver(entries => {
    const nextWidth = Math.round(entries[0].contentRect.width);
    if (nextWidth !== chartWidth) {
      chartWidth = nextWidth;
      if (activeRegion) drawTrend();
    }
  }).observe($("trend-chart"));
  for (const [id, step] of [["year-prev", -1], ["year-next", 1]]) {
    $(id).addEventListener("click", () => {
      const next = manifest.years[manifest.years.indexOf(Number($("year").value)) + step];
      if (next === undefined) return;
      $("year").value = next;
      selectRegion();
    });
  }
  $("fit").addEventListener("click", map.fit);
  $("reset").addEventListener("click", () => {
    $("province").value = "";
    addOptions("district", [["", "Semua kabupaten/kota"]]);
    $("district").disabled = true;
    $("district-hint").textContent = "Pilih provinsi untuk melihat kabupaten/kota.";
    $("mode").value = "annual";
    $("year").value = manifest.default_year;
    $("year-from").value = manifest.years[0];
    updateEndYears();
    $("year-to").value = manifest.years.at(-1);
    $("from").value = "";
    $("to").value = "";
    $("chart-class").value = "35";
    selectRegion();
    map.fit();
  });
  $("zoom-in").addEventListener("click", () => map.zoom(1.3));
  $("zoom-out").addEventListener("click", () => map.zoom(1 / 1.3));
  selectRegion();
}

initialize();
$("about-link").addEventListener("click", () => { $("metadata").open = true; });
document.addEventListener("keydown", event => {
  if (event.key === "Escape") $("metadata").open = false;
});

