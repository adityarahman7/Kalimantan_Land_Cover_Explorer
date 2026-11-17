// Run with node tests/r2_browser.cjs <Playwright module path> <Python executable>.
const assert = require("node:assert/strict");
const {spawn} = require("node:child_process");
const {mkdirSync} = require("node:fs");
const {chromium} = require(process.argv[2] || "playwright");
const base = "http://127.0.0.1:8767/";
const format = new Intl.NumberFormat("id-ID", {maximumFractionDigits: 2});
const binaries = [
  ["Edge", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"],
  ["Chrome", "C:/Program Files/Google/Chrome/Application/chrome.exe"],
];

async function check(name, executablePath) {
  const browser = await chromium.launch({executablePath, headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1366, height: 1000}});
    const errors = [];
    page.on("pageerror", error => errors.push(error.message));
    const table = page.locator("#stats-table");
    const ready = () => table.waitFor({state: "visible"});
    const select = (id, value) => page.selectOption("#" + id, String(value));
    const text = id => page.locator("#" + id).innerText();
    const signature = () => page.locator("#map").evaluate(canvas => canvas.toDataURL());
    const started = Date.now();
    await page.goto(base);
    await ready();
    const initialReadyMs = Date.now() - started;
    assert.equal(await page.inputValue("#area-unit"), "km2");
    assert.match(await text("cards"), /534\.354,34 km²/);
    await select("area-unit", "ha");
    const m = await (await page.request.get(base + "public/data/r2/manifest.json")).json();
    const statsUrl = id => base + "public/data/r2/" + m.region_index.find(r => r.region_id === id).stats;
    const aoi = await (await page.request.get(statsUrl("KALIMANTAN_ID"))).json();
    assert.equal(await page.locator("#year option").count(), 15);
    assert.equal(await page.inputValue("#year"), "2024");
    const initial = await signature();
    for (const year of m.years) {
      await select("year", year);
      await ready();
      assert.equal(await text("map-mode"), `Tutupan lahan ${year}`);
      const rows = await page.locator("#rows tr").allTextContents();
      assert.equal(rows.length, 13);
      m.class_order.forEach((code, i) => {
        const matched = rows.find(row => row.includes(`(${code})`));
        assert.ok(matched?.includes(format.format(aoi.annual_area_ha[year][i])));
      });
      const areas = await page.locator("#rows tr").evaluateAll(nodes => nodes.map(n => Number(n.dataset.areaHa)));
      assert.ok(areas.every((value, i) => !i || value <= areas[i - 1]), "descending shares");
      assert.equal(await page.locator("#trend-chart circle").count(), 15);
    }
    await select("year", 2010);
    await ready();
    assert.notEqual(await signature(), initial);
    await select("chart-class", 3);
    const chartValues = await page.locator("#trend-rows tr").allTextContents();
    m.years.forEach((year, i) => assert.ok(chartValues[i].includes(format.format(aoi.annual_area_ha[year][0]))));
    await page.locator('#trend-chart circle[aria-label^="2016,"]').click();
    await ready();
    assert.equal(await page.inputValue("#year"), "2016");
    assert.equal(await text("map-mode"), "Tutupan lahan 2016");
    await select("mode", "change");
    await ready();
    assert.match(await text("cards"), /10\.474\.804,21 ha/);
    for (const [a, b] of [[2010, 2011], [2014, 2021], [2023, 2024]]) {
      await select("year-from", a);
      await select("year-to", b);
      await ready();
      assert.equal(await text("map-mode"), `Perubahan ${a} → ${b}`);
      assert.ok((await text("cards")).includes(format.format(aoi.pairs[`${a}_${b}`].summary.changed_ha)));
      const endings = await page.locator("#year-to option").evaluateAll(nodes => nodes.map(n => Number(n.value)));
      assert.ok(endings.every(year => year > a));
    }
    await select("year-from", 2010);
    await select("year-to", 2024);
    await select("from", 3);
    await select("to", 35);
    await ready();
    assert.match(await text("cards"), /649\.739,68 ha/);
    assert.match(await text("legend"), /Formasi hutan → Sawit/);
    await select("from", "");
    await select("to", "");
    await ready();
    assert.equal(await page.locator("#rows tr").count(), 3);
    let release;
    const gate = new Promise(resolve => release = resolve);
    await page.route("**/stats/61.json", async route => {await gate; await route.continue();});
    await select("province", "61");
    assert.equal(await table.isHidden(), true);
    assert.equal(await page.locator("#map").evaluate(c => c.style.visibility), "hidden");
    assert.equal(await page.locator("#district option").count(), 15);
    await select("district", "61.01");
    await ready();
    const oldResponse = page.waitForResponse("**/stats/61.json");
    release();
    await (await oldResponse).finished();
    assert.equal(await text("map-title"), "Sambas");
    const district = await (await page.request.get(statsUrl("61.01"))).json();
    const matrix = district.pairs["2010_2024"].transition_area_ha;
    const row = matrix.findIndex(values => values.includes(0));
    const col = matrix[row].indexOf(0);
    await select("from", m.class_order[row]);
    await select("to", m.class_order[col]);
    await ready();
    assert.match(await text("stats-status"), /Tidak ada piksel valid/);
    await page.route("**/stats/62.json", route => route.fulfill({status: 404, body: "missing"}));
    await select("province", "62");
    await page.getByRole("button", {name: "Coba lagi"}).waitFor();
    assert.equal(await table.isHidden(), true);
    await page.unroute("**/stats/62.json");
    await page.getByRole("button", {name: "Coba lagi"}).click();
    await ready();
    await select("province", "");
    await ready();
    assert.equal(await text("map-title"), "Kalimantan Indonesia");
    await select("mode", "annual");
    await ready();
    await page.route("**/class_2013.u8.gz", route => route.fulfill({status: 404, body: "missing"}));
    await select("year", 2013);
    await page.getByRole("button", {name: "Coba lagi"}).waitFor();
    assert.equal(await table.isHidden(), true);
    await page.unroute("**/class_2013.u8.gz");
    await page.getByRole("button", {name: "Coba lagi"}).click();
    await ready();
    for (const width of [320, 390, 768, 1366]) {
      await page.setViewportSize({width, height: 1000});
      await page.waitForFunction(w => innerWidth === w && document.querySelector("canvas").width === document.querySelector("canvas").clientWidth, width);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${name} overflow ${width}`);
    }
    if (name === "Edge") {
      mkdirSync("data/interim/r2/qa", {recursive: true});
      await page.screenshot({path: "data/interim/r2/qa/desktop.png", fullPage: true});
      await page.setViewportSize({width: 390, height: 844});
      await page.screenshot({path: "data/interim/r2/qa/mobile.png", fullPage: true});
    }
    await page.click("#year-next");
    await ready();
    assert.equal(await page.inputValue("#year"), "2014");
    await page.route("**/r2/manifest.json", route => route.fulfill({status: 404, body: "missing"}));
    await page.reload();
    await ready();
    assert.equal(await page.locator("#year option").count(), 2);
    assert.equal(await page.locator("#trend-chart circle").count(), 2);
    assert.equal(await page.locator("#data-availability").isVisible(), true);
    await page.unroute("**/r2/manifest.json");
    await page.route("**/r2/manifest.json", route => route.fulfill({status: 200, contentType: "application/json",
      body: JSON.stringify({schema_version: 1, release: "R2", years: [2010]})}));
    await page.reload();
    await page.getByRole("button", {name: "Coba lagi"}).waitFor();
    assert.equal(await page.locator("#explorer").isHidden(), true);
    await page.unroute("**/r2/manifest.json");
    await page.getByRole("button", {name: "Coba lagi"}).click();
    await ready();
    assert.equal(await page.locator("#year option").count(), 15);
    assert.deepEqual(errors, []);
    console.log(`${name} ${browser.version()} passed annual, trend, pairs, filters, stale responses, retry and 4 viewports.`);
    return {browser: name, version: browser.version(), status: "passed", initial_ready_local_ms: initialReadyMs};
  } finally {
    await browser.close();
  }
}

(async () => {
  const server = spawn(process.argv[3] || "python", ["-m", "http.server", "8767", "--bind", "127.0.0.1", "--directory", "web"], {stdio: "ignore"});
  try {
    for (let i = 0; ; i++) {
      try {if ((await fetch(base)).ok) break;} catch {}
      assert.ok(i < 50, "server did not start");
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    const results = [];
    for (const [name, path] of binaries) results.push(await check(name, path));
    require("node:fs").writeFileSync("data/metadata/r2_browser_qa.json", JSON.stringify({
      checked_on: "2026-11-17", results, years_tested: 15,
      representative_pairs: ["2010_2024", "2010_2011", "2014_2021", "2023_2024"],
      viewport_widths: [320, 390, 768, 1366],
      r1_fallback_and_malformed_r2_manifest: "passed",
      year_navigation_buttons: "passed",
      limitation: "Local headless Chromium browsers. Not physical devices or hosting performance.",
    }, null, 2) + "\n");
  } finally {
    server.kill();
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
