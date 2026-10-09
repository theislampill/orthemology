#!/usr/bin/env python3
"""Check printed t/F-to-p arithmetic only. No participant data are read.

This is NOT a computational reanalysis, replication, or independent experiment.
Run: python recompute_reported_statistics.py
Requires scipy; writes arithmetic_results.json beside this script.
"""
from pathlib import Path
import json
import platform
import scipy
from scipy.stats import f, t

HERE = Path(__file__).resolve().parent

def evaluate(row):
    value = row["statistic"]
    df = row["df_denominator"]
    if row["distribution"] == "F":
        tail = lambda x: float(f.sf(x, row["df_numerator"], df))
        label = "F upper tail (equivalent to two-sided t when numerator df is 1)"
    else:
        tail = lambda x: float(2 * t.sf(abs(x), df))
        label = "two-sided t"
    result = dict(row)
    result["ordinary_p_convention"] = label
    result["ordinary_p_from_printed_value"] = tail(value)
    result["directional_t_equivalent_p_if_direction_prejustified"] = tail(value) / 2
    result["rounding_assumption"] = "nearest 0.01; statistic within printed value +/- 0.005"
    result["ordinary_p_rounding_range"] = [tail(value + .005), tail(value - .005)]
    result["directional_p_rounding_range"] = [p / 2 for p in result["ordinary_p_rounding_range"]]
    return result

def main():
    rows = json.loads((HERE / "reported_statistics.json").read_text())
    results = [evaluate(row) for row in rows]
    by_id = {row["id"]: row for row in results}
    assert by_id["S4_THEORY_SAGAN_INTERACTION"]["directional_p_rounding_range"][0] > .05
    assert by_id["S5_THEORY_ET_SIMPLE"]["directional_p_rounding_range"][0] > .05
    for key in ["S4_THEORY_THREE_WAY", "S4_THEORY_IDT_SIMPLE", "S5_THEORY_INTERACTION", "S5_THEORY_IDT_SIMPLE"]:
        assert by_id[key]["ordinary_p_rounding_range"][1] < .05
    assert by_id["S5_SIX_ET_SIMPLE"]["directional_p_rounding_range"][1] < .05
    output = {
        "classification": "reported-statistic arithmetic consistency check only",
        "participant_level_data_used": False,
        "empirical_reanalysis_completed": False,
        "python_version": platform.python_version(),
        "scipy_version": scipy.__version__,
        "results": results,
    }
    (HERE / "arithmetic_results.json").write_text(json.dumps(output, indent=2) + "\n")
    for row in results:
        print(f"{row['id']}: ordinary p={row['ordinary_p_from_printed_value']:.9f}; directional equivalent={row['directional_t_equivalent_p_if_direction_prejustified']:.9f}")
    print("PASS: internal checks. These assertions do not verify any participant-level result.")

if __name__ == "__main__":
    main()
