"""One fixed 32-input structural control using unchanged public census code.

Python 3.10+, standard library only. No production/oracle edits or dependency
acquisition. The parent runner gives the sole campaign process 180 seconds.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
NAME = "four_state_two_nontrivial_children"
LIMIT_SECONDS = 180
LABELS = (
    "equal_row_anchor",
    "first_block_rival_even_removed",
    "second_block_rival_even_removed",
    "first_block_numerically_distinguished",
    "both_blocks_numerically_distinguished",
    "forward_bridge_removed_bad_first_block",
    "matched_exiting_internal_successor",
    "revealing_exiting_internal_successor",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_sources():
    bindings = json.loads((ROOT / "SOURCE_BINDINGS.json").read_text())
    require(len(bindings["files"]) == 12, "expected exactly 12 copied source files")
    actual = set()
    for entry in bindings["files"]:
        rel = Path(entry["path"])
        require(not rel.is_absolute() and ".." not in rel.parts, "unsafe source binding")
        data = (ROOT / rel).read_bytes()
        require(len(data) == entry["bytes"], "copied source byte count mismatch: " + str(rel))
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], "copied source hash mismatch: " + str(rel))
        actual.add(str(rel))
    require(actual == {str(p.relative_to(ROOT)) for p in (ROOT / "sources").rglob("*") if p.is_file()},
            "copied source inventory mismatch")
    return bindings


def load_census():
    verify_sources()
    folder = ROOT / "sources/tranche18/reviews/hidden-change-efficient"
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location("stress_control_unchanged_census", folder / "run_campaign.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def generated_inputs():
    """Fixed, labelled templates. No randomness, permutations, or hidden cases."""
    entries = []
    for label in LABELS:
        rows = []
        for theta in (0, 1):
            mode = []
            for state in range(4):
                block = state // 2
                internal = ["1/2" if target // 2 == block else "0" for target in range(4)]
                bridge_target = {0: 2, 1: 1, 2: 0, 3: 3}[state]
                bridge = [str(int(target == bridge_target)) for target in range(4)]
                mode.append([internal, bridge])
            rows.append(mode)
        priorities = [[[value, 1] for value in values] for values in ((2, 3, 4, 5), (3, 2, 5, 4))]
        if label in ("first_block_rival_even_removed", "first_block_numerically_distinguished",
                     "forward_bridge_removed_bad_first_block"):
            priorities[1][1][0] = 3
        if label == "second_block_rival_even_removed":
            priorities[1][3][0] = 5
        if label in ("first_block_numerically_distinguished", "both_blocks_numerically_distinguished"):
            rows[1][0][0] = ["1/3", "2/3", "0", "0"]
        if label == "both_blocks_numerically_distinguished":
            rows[1][2][0] = ["0", "0", "2/3", "1/3"]
        if label == "forward_bridge_removed_bad_first_block":
            for theta in (0, 1):
                rows[theta][0][1] = ["1", "0", "0", "0"]
        if label in ("matched_exiting_internal_successor", "revealing_exiting_internal_successor"):
            rows[1][0][0] = ["1/3", "1/3", "1/3", "0"]
        if label == "matched_exiting_internal_successor":
            rows[0][0][0] = list(rows[1][0][0])
        for initial in range(4):
            raw = dict(n_states=4, n_actions=2, initial=initial,
                       menus=[[0, 1] for _ in range(4)], rows=rows, priorities=priorities)
            # Serialization makes each input independently owned and exact.
            raw = json.loads(canonical(raw))
            entries.append(dict(template=label, initial=initial, input_sha256=digest(raw), raw=raw))
    return entries


def to_input(raw, census):
    from fractions import Fraction
    return census.prior.Input(
        raw["n_states"], raw["n_actions"], raw["initial"],
        tuple(tuple(menu) for menu in raw["menus"]),
        tuple(tuple(tuple(tuple(Fraction(p) for p in row) for row in state)
                    for state in mode) for mode in raw["rows"]),
        tuple(tuple(tuple(state) for state in mode) for mode in raw["priorities"]))


def assert_features(entries, census):
    require(len(entries) == 32, "must contain exactly eight templates times four initial states")
    require(len({entry["input_sha256"] for entry in entries}) == 32, "inputs must be distinct")
    require(tuple(dict.fromkeys(e["template"] for e in entries)) == LABELS, "template labels changed")
    for label in LABELS:
        require([e["initial"] for e in entries if e["template"] == label] == list(range(4)), "missing initial state")
    left = frozenset(((0, 0), (1, 0)))
    right = frozenset(((2, 0), (3, 0)))
    internal = left | right
    both = frozenset((left, right))
    features = {}
    for entry in entries:
        inp = to_input(entry["raw"], census)
        census.validate_model(entry["raw"])
        require(entry["input_sha256"] == digest(entry["raw"]), "input digest mismatch")
        require(inp.n == 4 and inp.a == 2 and len(census.full_pairs(inp)) == 8, "carrier/menu mismatch")
        if entry["template"] != "equal_row_anchor":
            continue
        model = census.validate_model(entry["raw"])
        for theta in (0, 1):
            ends = census.all_end_components(inp, theta)
            require(census.maximal_allowed(ends, census.full_pairs(inp)) == frozenset((census.full_pairs(inp),)),
                    "anchor must be a single unfiltered eight-pair MEC")
            allowed = frozenset(pair for pair in census.full_pairs(inp)
                                if inp.priorities[theta][pair[0]][pair[1]] >= 2)
            require(allowed == internal, "threshold must remove precisely the low-odd actions")
            require(census.maximal_allowed(ends, allowed) == both, "anchor must expose BOTH two-state MECs")
            require(frozenset(map(frozenset, census.maximal_components(model, theta, allowed))) == both,
                    "production must expose BOTH anchor two-state MECs")
            high = frozenset(pair for pair in census.full_pairs(inp)
                             if inp.priorities[theta][pair[0]][pair[1]] >= 4)
            require(high == right and census.maximal_allowed(ends, high) == frozenset((right,)),
                    "higher threshold must retain precisely the second nontrivial block")
            for block, minimum in ((left, 2), (right, 4)):
                own = {pair for pair in block if inp.priorities[theta][pair[0]][pair[1]] == minimum}
                rival = {pair for pair in block if inp.priorities[1-theta][pair[0]][pair[1]] == minimum}
                require(len(own) == len(rival) == 1 and own.isdisjoint(rival), "even witnesses must be separately attained")
                require(all(inp.rows[0][s][a] == inp.rows[1][s][a] for s, a in block), "anchor must exercise equal numerical rows")
                require(census.qualifying(inp, theta, block, True), "anchor block must qualify in both uncertain modes")
            representatives = census.uncertain_components(model, theta, internal)
            require(frozenset(map(frozenset, representatives)) == both, "anchor representatives must identify each block exactly")
            require(census.target_union(representatives) == frozenset(range(4)), "anchor target union must cover four states")
        require(frozenset(map(frozenset, census.known_components(model, internal))) == both, "known anchor representatives mismatch")
    # Feature checks are made from the exact input objects, independent of census counts.
    cases = {entry["template"]: to_input(entry["raw"], census) for entry in entries if entry["initial"] == 0}
    first_bad = cases[LABELS[1]]
    second_bad = cases[LABELS[2]]
    require(not census.qualifying(first_bad, 0, left, True) and census.qualifying(first_bad, 0, right, True), "first-block even loss missing")
    require(census.qualifying(second_bad, 0, left, True) and not census.qualifying(second_bad, 0, right, True), "second-block even loss missing")
    distinct = cases[LABELS[3]]
    require(tuple(p > 0 for p in distinct.rows[0][0][0]) == tuple(p > 0 for p in distinct.rows[1][0][0])
            and distinct.rows[0][0][0] != distinct.rows[1][0][0], "same-support numerical distinction missing")
    require(census.qualifying(distinct, 0, left, True) and not census.qualifying(distinct, 1, left, True), "Case A own/rival distinction missing")
    double = cases[LABELS[4]]
    require(double.rows[0][0][0] != double.rows[1][0][0] and double.rows[0][2][0] != double.rows[1][2][0], "two distinguishing blocks missing")
    removed = cases[LABELS[5]]
    require(all(removed.rows[t][0][1][2] == 0 for t in (0, 1)), "forward bridge was not removed")
    require(census.prior.regions(cases[LABELS[0]]) == (frozenset(range(4)), frozenset(range(4))),
            "positive anchor must win from all four initial states")
    require(census.prior.regions(removed) == (frozenset((2, 3)), frozenset((2, 3))),
            "isolated odd first block must lose while the second block wins")
    matched = cases[LABELS[6]]
    revealing = cases[LABELS[7]]
    require(matched.rows[0][0][0] == matched.rows[1][0][0] and matched.rows[1][0][0][2] > 0, "matched exit missing")
    require(revealing.rows[0][0][0][2] == 0 < revealing.rows[1][0][0][2], "revealing successor missing")
    require(not census.qualifying(revealing, 1, left, True), "revealing exit must reject a closed uncertain block")
    for label in (LABELS[6], LABELS[7]):
        inp = cases[label]
        require(census.maximal_allowed(census.all_end_components(inp, 1), internal) == frozenset((right,)),
                "exiting whole action must destroy the left closed block in mode one")
    features.update(anchor_initial_states_asserted=4, anchor_nontrivial_children_per_mode=2,
                    anchor_children=[[0, 1], [2, 3]], separately_attained_even_minima=[2, 4],
                    fixed_templates=8, distinct_inputs=32, state_action_relabellings=0,
                    random_inputs=0, allowed_pair_subsets_per_input=256,
                    k_w_region_combinations_per_input=256,
                    numerical_equality_and_same_support_inequality=True,
                    sparse_bridge_removal=True, matched_and_revealing_exits=True,
                    anchor_winning_initial_states=[0, 1, 2, 3],
                    isolated_odd_block_losing_initial_states=[0, 1])
    return features


def safe_value(value):
    if isinstance(value, (set, frozenset)):
        return [safe_value(x) for x in sorted(value)]
    if isinstance(value, (list, tuple)):
        return [safe_value(x) for x in value]
    if isinstance(value, dict):
        return {str(k): safe_value(v) for k, v in value.items()}
    if value is None or isinstance(value, (str, int, bool, float)):
        return value
    return type(value).__name__


def worker(output):
    require(sys.flags.optimize == 0 and __debug__, "optimized Python disables required census assertions")
    entries = generated_inputs()
    save(output / "INPUTS.json", entries)
    census = load_census()
    phase = "feature_assertions"
    try:
        features = assert_features(entries, census)
        save(output / "FEATURE_COVERAGE.json", features)
        expected_inputs = ROOT / "INPUTS.json"
        if expected_inputs.exists():
            require(json.loads(expected_inputs.read_text()) == entries, "generated inputs differ from distributed exact inputs")
        phase = "unchanged_census"
        result = census.census(NAME, lambda: (to_input(e["raw"], census) for e in entries), 32)
        require(result["models"] == result["signed_body_checks"] == 32, "incomplete signed-body coverage")
        require(result["known_operator_comparisons"] == 512, "incomplete known-region coverage")
        require(result["uncertain_operator_comparisons"] == 8192, "incomplete K/W-region coverage")
        require(result["mec_comparisons"] == 16384, "incomplete MEC coverage")
        require(result["target_union_comparisons"] == 24576, "incomplete target-union coverage")
        save(output / "RESULT.json", dict(schema=1, status="passed", scope="Small structured stress-control supplement; bounded implementation evidence only.",
             inputs_sha256=digest(entries), source_bindings_sha256=hashlib.sha256((ROOT / "SOURCE_BINDINGS.json").read_bytes()).hexdigest(),
             process_limit_seconds=LIMIT_SECONDS, campaign_invocations=1, features=features, census=result,
             excluded_claims=["new theorem", "arbitrary-finite proof by testing", "Python/Lean correspondence", "production change", "broad four-state census"]))
        return 0
    except BaseException as exc:
        failure = dict(schema=1, status="execution_or_coverage_failure", phase=phase,
                       exception=type(exc).__name__, message=str(exc),
                       mathematical_negative_evidence=False)
        for frame, line in traceback.walk_tb(exc.__traceback__):
            if frame.f_code.co_name == "census":
                values = frame.f_locals
                failure["census_line"] = line
                index = values.get("index")
                if type(index) is int and 0 <= index < len(entries):
                    failure["exact_input"] = entries[index]
                failure["comparison_context"] = {key: safe_value(values[key]) for key in
                    ("index", "theta", "uncertain", "allowed", "actual", "expected", "sets", "end", "k", "w", "expected_regions", "result") if key in values}
        save(output / "FAILURE.json", failure)
        print(json.dumps(failure, sort_keys=True), flush=True)
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--check", action="store_true", help="Check sources and structural assertions without running census")
    args = parser.parse_args()
    require(sys.flags.optimize == 0 and __debug__, "run without -O/-OO")
    sys.dont_write_bytecode = True
    if args.check:
        require(not args.output and not args.worker, "--check is a separate mode")
        print(json.dumps(assert_features(generated_inputs(), load_census()), sort_keys=True))
        return 0
    if args.worker:
        return worker(args.worker)
    require(args.output is not None, "provide --output pointing outside the source-only supplement")
    output = args.output.resolve()
    require(ROOT != output and ROOT not in output.parents, "output must be outside the distributed supplement")
    require(not output.exists(), "output must not already exist")
    verify_sources()
    output.mkdir(parents=True)
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    start = time.monotonic()
    with (output / "CAMPAIGN.stdout.txt").open("w") as stdout, (output / "CAMPAIGN.stderr.txt").open("w") as stderr:
        try:
            completed = subprocess.run([sys.executable, "-E", "-S", "-B", str(ROOT / "run_control.py"), "--worker", str(output)],
                                       env=env, stdout=stdout, stderr=stderr, timeout=LIMIT_SECONDS, check=False)
            status = "passed" if completed.returncode == 0 and (output / "RESULT.json").exists() else "failed"
            returncode = completed.returncode
        except subprocess.TimeoutExpired:
            status = "timeout"
            returncode = 124
    receipt = dict(schema=1, status=status, returncode=returncode, process_limit_seconds=LIMIT_SECONDS,
                   elapsed_seconds=round(time.monotonic() - start, 6), python=platform.python_version(),
                   system=platform.system(), machine=platform.machine(), campaign_processes_launched=1,
                   timeout_or_execution_failure_is_mathematical_negative=False)
    save(output / "EXECUTION.json", receipt)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if status == "passed" else (returncode or 1)


if __name__ == "__main__":
    sys.exit(main())
