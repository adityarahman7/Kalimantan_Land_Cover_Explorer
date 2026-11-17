export function areaUnit(unit = "km2") {
  return unit === "ha" ? {label: "ha", divisor: 1} : {label: "km²", divisor: 100};
}

export function formatArea(value, unit = "km2") {
  const {label, divisor} = areaUnit(unit);
  return `${new Intl.NumberFormat("id-ID", {maximumFractionDigits: 2}).format(value / divisor)} ${label}`;
}
