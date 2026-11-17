"""Independently check annual, pairwise and R1 consistency in an R2 package."""

import csv
import gzip
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "web/public/data/r2"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def close(a, b, message):
    if not math.isclose(a, b, abs_tol=.01, rel_tol=0):
        raise ValueError(f"{message}: {a} != {b}")


def main():
    m = read(DATA / "manifest.json")
    years, codes = m["years"], m["class_order"]
    pairs = [f"{a}_{b}" for a, b in itertools.combinations(years, 2)]
    assert years == list(range(2010, 2025)) and pairs == m["pairs"] and len(pairs) == 105
    records = {r["region_id"]: read(DATA / r["stats"]) for r in m["region_index"]}
    assert len(records) == 62
    for rid, r in records.items():
        assert r["region_id"] == rid and set(r["pairs"]) == set(pairs)
        assert set(r["annual_area_ha"]) == {str(y) for y in years}
        for y in years:
            values = r["annual_area_ha"][str(y)]
            assert len(values) == len(codes) and all(math.isfinite(v) and v >= 0 for v in values)
            close(math.fsum(values), r["annual_valid_ha"][str(y)], f"Annual {rid} {y}")
        for a, b in itertools.combinations(years, 2):
            p = r["pairs"][f"{a}_{b}"]
            s, matrix = p["summary"], p["transition_area_ha"]
            assert len(matrix) == len(codes)
            assert all(len(row) == len(codes) for row in matrix)
            assert all(math.isfinite(v) and v >= 0 for row in matrix for v in row)
            common = math.fsum(v for row in matrix for v in row)
            stable = math.fsum(matrix[i][i] for i in range(len(codes)))
            close(common, s["valid_common_ha"], "Common")
            close(stable, s["stable_ha"], "Stable")
            close(common - stable, s["changed_ha"], "Changed")
            close(common + s["not_comparable_ha"], s["aoi_ha"], "AOI")
            for y in (a, b):
                close(s[f"valid_{y}_ha"], r["annual_valid_ha"][str(y)], "Annual coverage")
            for i in range(len(codes)):
                assert math.fsum(matrix[i]) <= r["annual_area_ha"][str(a)][i] + .01
                assert math.fsum(row[i] for row in matrix) <= r["annual_area_ha"][str(b)][i] + .01

    for name in ("luas_kelas", "transisi_kelas", "ringkasan_perubahan"):
        with (ROOT / f"outputs/tables/phase4/{name}.csv").open(encoding="utf-8-sig") as file:
            for row in csv.DictReader(file):
                r = records[row["region_id"]]
                if name == "luas_kelas":
                    close(r["annual_area_ha"][row["year"]][codes.index(int(row["class_code"]))], float(row["area_ha"]), "R1 annual")
                elif name == "transisi_kelas":
                    matrix = r["pairs"]["2010_2024"]["transition_area_ha"]
                    close(matrix[codes.index(int(row["class_from"]))][codes.index(int(row["class_to"]))], float(row["area_ha"]), "R1 matrix")
                else:
                    for key, value in r["pairs"]["2010_2024"]["summary"].items():
                        if row[key]:
                            close(value, float(row[key]), "R1 summary")
    size = math.prod(m["raster"]["dimensions"])
    for path in m["raster"]["year_paths"].values():
        raw = gzip.decompress((DATA / path).read_bytes())
        assert len(raw) == size and set(raw) <= {0, 255, *codes}
    report = {"checked_on": "2026-11-17", "status": "passed", "regions": len(records),
              "years": len(years), "pairs": len(pairs), "tolerance_ha": .01,
              "annual_cells": 62 * 15 * len(codes), "transition_cells": 62 * 105 * len(codes)**2,
              "r1_csv_regression": "passed", "raster_byte_lengths_and_codes": "passed"}
    (ROOT / "data/metadata/r2_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
