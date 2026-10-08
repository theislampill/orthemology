"""Generate and compare deterministic Python/Lean replay fixtures.

The CSV is trusted test data generated here, not an external protocol parser.
"""
from dataclasses import replace
from hashlib import sha256
from itertools import product
import argparse
import gzip
import json
from pathlib import Path

from criterion_model import Source, Grant, State, Command, execute

ROOT = Path(__file__).resolve().parent
SOURCE_BYTES = (ROOT / "sources/proper-function-and-candidate-e.md").read_bytes()
TARGET = ("theislampill/orthemology", "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
          "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")
SOURCE = Source(TARGET, SOURCE_BYTES, frozenset({"canonical-github-object"}))
FIELDS = ["owner", "revision", "epoch", "revoked", "now", "draft_tag",
          "grant_present", "grant_actor", "grant_expires", "request_actor",
          "expected_revision", "claimed_epoch", "operation_tag", "criterion_tag",
          "payload_tag", "observed_at", "lease_end"]


def fixtures():
    return product((0, 1), (0, 1), (0, 1), (0, 1), (0, 1, 2, 3), (0, 1, 2),
                   (0, 1), (0, 1), (2, 4), (0, 1), (0, 1), (0, 1), (0, 1),
                   (0, 1), (0, 1), (0, 2), (2, 4))


def decode(row):
    owner, rev, epoch, revoked, now, dtag, present, ga, expiry, ca, crev, ce, op, crit, ptag, obs, lease = row
    actor = lambda i: "A" if i == 0 else "B"
    destination = actor(owner) + "/draft"
    grant = Grant(actor(ga), destination, TARGET, epoch, 0, expiry, "replace-derived") if present else None
    drafts = (SOURCE_BYTES, SOURCE_BYTES + b"\n", b"wrong")
    state = State(SOURCE, destination, drafts[dtag], rev, epoch, grant,
                  bool(revoked), now, (b"retained-earlier-history",))
    command = Command(actor(ca), destination, TARGET,
                      "C1-exact" if crit == 0 else "C0-normalized", crev, ce,
                      drafts[ptag], "replace-derived" if op == 0 else "overwrite-source", obs, lease)
    return state, command


def expected_line(index, row):
    state, command = decode(row)
    result = execute(state, command)
    dtag = 0 if result.state.draft == SOURCE_BYTES else 1 if result.state.draft == SOURCE_BYTES + b"\n" else 2
    return ",".join(map(str, (index, int(result.applied), result.state.revision,
                               dtag, len(result.state.history), int(result.state.source == state.source))))


def generate(directory):
    directory.mkdir(parents=True, exist_ok=True)
    fixture_path, expected_path = directory / "shared_fixtures.csv", directory / "python_expected.csv"
    count = 0
    with fixture_path.open("w") as ff, expected_path.open("w") as ef:
        for index, row in enumerate(fixtures()):
            ff.write(",".join(map(str, row)) + "\n")
            ef.write(expected_line(index, row) + "\n")
            count += 1
    record = {
        "count": count, "fields": FIELDS,
        "output_fields": ["index", "applied", "revision", "draft_tag", "history_length", "source_preserved"],
        "fixture_sha256": sha256(fixture_path.read_bytes()).hexdigest(),
        "python_output_sha256": sha256(expected_path.read_bytes()).hexdigest(),
        "source_sha256": sha256(SOURCE_BYTES).hexdigest(),
        "scope": "Shared typed fixture domain; not an all-input refinement proof",
    }
    (directory / "SHARED_FIXTURE_MANIFEST.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


def compare(directory, label):
    expected, actual = directory / "python_expected.csv", directory / "lean_actual.csv"
    mismatch_count, first, count = 0, None, 0
    with expected.open() as ef, actual.open() as af:
        for index, eline in enumerate(ef):
            aline = af.readline()
            count += 1
            if eline != aline:
                mismatch_count += 1
                if first is None:
                    first = {"line": index + 1, "python": eline.strip(), "lean": aline.strip()}
        trailing = af.read()
        if trailing:
            mismatch_count += 1
            if first is None:
                first = {"unexpected_trailing_output": trailing[:200]}
    record = {"stage": label, "compared": count, "mismatches": mismatch_count,
              "first_mismatch": first,
              "python_sha256": sha256(expected.read_bytes()).hexdigest(),
              "lean_sha256": sha256(actual.read_bytes()).hexdigest(),
              "passed": mismatch_count == 0}
    (directory / ("CROSS_LANGUAGE_" + label.upper() + ".json")).write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
    return mismatch_count == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("generate", "compare"))
    parser.add_argument("--directory", type=Path, default=ROOT / "evidence")
    parser.add_argument("--label", default="green")
    args = parser.parse_args()
    if args.action == "generate":
        generate(args.directory)
    else:
        raise SystemExit(0 if compare(args.directory, args.label) else 1)
