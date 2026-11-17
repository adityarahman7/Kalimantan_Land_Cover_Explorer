export async function loadPairs(url, raster) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Raster tampilan tidak tersedia (HTTP ${response.status}).`);
  const stream = response.body.pipeThrough(new DecompressionStream("gzip"));
  const data = new DataView(await new Response(stream).arrayBuffer());
  const [width, height] = raster.dimensions;
  if (data.byteLength !== width * height * 2) throw new Error("Ukuran raster tampilan berbeda dari manifest.");
  return data;
}

export function createMap(canvas, raster, pairs, boundaries) {
  const context = canvas.getContext("2d");
  const [width, height] = raster.dimensions;
  const [west, spacing, xRotation, north, yRotation, ySpacing] = raster.geotransform_gdal;
  if (raster.crs !== "EPSG:4326" || xRotation || yRotation || spacing !== -ySpacing || spacing <= 0) {
    throw new Error("Grid raster tampilan tidak didukung.");
  }

  const image = document.createElement("canvas");
  image.width = width;
  image.height = height;
  const imageContext = image.getContext("2d");
  const pixels = imageContext.createImageData(width, height);
  const rgba = new Uint32Array(pixels.data.buffer);
  const palette = new Uint32Array(65536);
  const shapes = new Map();
  for (const {id, level, geometry} of boundaries) {
    const path = new Path2D();
    const polygons = geometry.type === "Polygon" ? [geometry.coordinates] : geometry.coordinates;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const polygon of polygons) {
      for (const ring of polygon) {
        ring.forEach(([longitude, latitude], index) => {
          const x = (longitude - west) / spacing;
          const y = (north - latitude) / spacing;
          if (index === 0) path.moveTo(x, y);
          else path.lineTo(x, y);
          minX = Math.min(minX, x);
          minY = Math.min(minY, y);
          maxX = Math.max(maxX, x);
          maxY = Math.max(maxY, y);
        });
        path.closePath();
      }
    }
    shapes.set(id, {path, level, minX, minY, maxX, maxY});
  }
  const provinces = [...shapes.values()].filter(shape => shape.level === "province");
  let selected;
  let scale = 1, fittedScale = 1, centerX = 0, centerY = 0;
  let drag;
  let land;

  function pathFor(geometry) {
    const path = new Path2D();
    const polygons = geometry.type === "Polygon" ? [geometry.coordinates] : geometry.coordinates;
    for (const polygon of polygons) for (const ring of polygon) {
      ring.forEach(([lon, lat], i) => {
        const x = (lon - west) / spacing, y = (north - lat) / spacing;
        if (i) path.lineTo(x, y); else path.moveTo(x, y);
      });
      path.closePath();
    }
    return path;
  }

  function draw() {
    if (!selected || !canvas.clientWidth) return;
    const indicator = canvas.parentElement.querySelector(".zoom-level");
    if (indicator) indicator.textContent = `${new Intl.NumberFormat("id-ID", {maximumFractionDigits: 1}).format(scale / fittedScale)}×`;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.round(canvas.clientWidth * ratio);
    const h = Math.round(canvas.clientHeight * ratio);
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    context.setTransform(1, 0, 0, 1, 0, 0);
    const ocean = context.createLinearGradient(0, 0, w, h);
    ocean.addColorStop(0, "#142833");
    ocean.addColorStop(1, "#0b1924");
    context.fillStyle = ocean;
    context.fillRect(0, 0, w, h);
    const factor = scale * ratio;
    context.setTransform(factor, 0, 0, factor, w / 2 - centerX * factor, h / 2 - centerY * factor);
    if (land) {
      context.fillStyle = "#293c3b";
      context.strokeStyle = "#607d78";
      context.lineWidth = .7 / scale;
      context.fill(land, "evenodd");
      context.stroke(land);
    }
    // Geographic grid follows the same EPSG:4326 coordinates as the raster.
    context.strokeStyle = "#a9c6d00c";
    context.lineWidth = .5 / scale;
    const step = scale / fittedScale > 4 ? .5 : 2;
    const westView = west + (centerX - canvas.clientWidth / scale / 2) * spacing;
    const eastView = west + (centerX + canvas.clientWidth / scale / 2) * spacing;
    const topView = north - (centerY - canvas.clientHeight / scale / 2) * spacing;
    const bottomView = north - (centerY + canvas.clientHeight / scale / 2) * spacing;
    context.beginPath();
    for (let lon = Math.ceil(westView / step) * step; lon <= eastView; lon += step) {
      const x = (lon - west) / spacing;
      context.moveTo(x, (north - topView) / spacing); context.lineTo(x, (north - bottomView) / spacing);
    }
    for (let lat = Math.ceil(bottomView / step) * step; lat <= topView; lat += step) {
      const y = (north - lat) / spacing;
      context.moveTo((westView - west) / spacing, y); context.lineTo((eastView - west) / spacing, y);
    }
    context.stroke();
    context.save();
    context.clip(selected.path, "evenodd");
    context.fillStyle = "#e7ece3";
    context.fillRect(selected.minX, selected.minY, selected.maxX - selected.minX, selected.maxY - selected.minY);
    context.imageSmoothingEnabled = false;
    context.drawImage(image, 0, 0);
    if (selected.level === "aoi") {
      context.strokeStyle = "#19372e88";
      context.lineWidth = .75 / scale;
      for (const province of provinces) context.stroke(province.path);
    }
    context.restore();
    context.strokeStyle = "#a2c5ac";
    context.lineWidth = 1 / scale;
    context.stroke(selected.path);
  }

  function fit() {
    if (!selected || !canvas.clientWidth) return;
    const {minX, minY, maxX, maxY} = selected;
    fittedScale = Math.min((canvas.clientWidth - 42) / (maxX - minX),
      (canvas.clientHeight - 42) / (maxY - minY));
    scale = fittedScale;
    centerX = (minX + maxX) / 2;
    centerY = (minY + maxY) / 2;
    draw();
  }

  function zoom(factor, x = 0, y = 0) {
    const nextScale = Math.max(fittedScale / 2, Math.min(fittedScale * 20, scale * factor));
    centerX += x / scale - x / nextScale;
    centerY += y / scale - y / nextScale;
    scale = nextScale;
    draw();
  }

  new ResizeObserver(fit).observe(canvas);
  canvas.addEventListener("pointerdown", event => {
    if (event.button !== 0 || drag) return;
    drag = {id: event.pointerId, x: event.clientX, y: event.clientY};
    canvas.setPointerCapture(event.pointerId);
  });
  canvas.addEventListener("pointermove", event => {
    if (drag?.id !== event.pointerId) return;
    centerX -= (event.clientX - drag.x) / scale;
    centerY -= (event.clientY - drag.y) / scale;
    drag.x = event.clientX;
    drag.y = event.clientY;
    draw();
  });
  canvas.addEventListener("lostpointercapture", () => { drag = null; });
  canvas.addEventListener("wheel", event => {
    event.preventDefault();
    const box = canvas.getBoundingClientRect();
    const delta = event.deltaY * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? canvas.clientHeight : 1);
    zoom(Math.exp(-Math.max(-200, Math.min(200, delta)) * .0025),
      event.clientX - box.left - box.width / 2, event.clientY - box.top - box.height / 2);
  }, {passive: false});

  return {
    setBasemap(collection) {
      land = new Path2D();
      for (const feature of collection.features) land.addPath(pathFor(feature.geometry));
      draw();
    },
    fit,
    zoom,
    setPairs(values) {
      if (values.byteLength !== width * height * 2) throw new Error("Ukuran pasangan raster salah.");
      pairs = values;
    },
    selectRegion(id) {
      selected = shapes.get(id);
      if (!selected) throw new Error("Batas wilayah tidak tersedia.");
      fit();
    },
    paint(colors) {
      palette.fill(0);
      const paletteBytes = new Uint8Array(palette.buffer);
      for (const [pair, hex] of colors) {
        const color = Number.parseInt(hex.slice(1), 16);
        paletteBytes.set([color >> 16, (color >> 8) & 255, color & 255, 255], pair * 4);
      }
      for (let i = 0; i < rgba.length; i++) rgba[i] = palette[pairs.getUint16(i * 2, true)];
      imageContext.putImageData(pixels, 0, 0);
      draw();
    },
  };
}
