"""Finite shared fixtures for explicit criterion installation, not deployment."""
from itertools import product
from pathlib import Path
from hashlib import sha256
import argparse
import json

from criterion_model import Source, Grant
from rule_install_model import Rule, RuleState, InstallCommand, accepts, install

ROOT = Path(__file__).resolve().parent
DATA = (ROOT / "sources/proper-function-and-candidate-e.md").read_bytes()
TARGET = ("theislampill/orthemology", "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
          "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")
FIELDS = ["owner", "current_rule", "rule_version", "grant_operation", "revoked",
          "request_actor", "expected_rule", "expected_version", "new_rule",
          "command_operation", "epoch_mismatch", "lease_expired"]


def decode(row):
    owner, rule, version, grant_op, revoked, who, expected_rule, expected_version, new_rule, op, epoch_bad, lease_bad = row
    actor = lambda x: "A" if x == 0 else "B"
    criterion = lambda x: Rule.NORMALIZED_LF if x == 0 else Rule.EXACT
    operation = lambda x: "install-criterion" if x == 0 else "replace-derived"
    dest = actor(owner) + "/package"
    source = Source(TARGET, DATA, frozenset({"canonical-github-object"}))
    grant = Grant(actor(owner), dest, TARGET, 2, 0, 10, operation(grant_op))
    state = RuleState(source, dest, "exact-source-recovery", DATA + b"\n", 8,
                      criterion(rule), version, 2, grant, bool(revoked),
                      4 if lease_bad == 0 else 9, (Rule.NORMALIZED_LF,),
                      ("retain-original-source", "no-GitHub-mutation"))
    command = InstallCommand(actor(who), dest, TARGET, criterion(expected_rule),
                             expected_version, 2 if epoch_bad == 0 else 3,
                             criterion(new_rule), operation(op), 3, 9)
    return state, command


def project(index, state, result):
    after = result.state
    decisions = [int(accepts(after.rule, c, DATA)) for c in (DATA, DATA + b"\n", b"X" + DATA[1:])]
    return [index, int(result.applied), int(after.rule is Rule.EXACT), after.rule_version,
            int(after.draft == state.draft), int(after.source == state.source),
            len(after.rule_history), int(after.unrelated == state.unrelated), *decisions]


def generate():
    evidence = ROOT / "evidence"
    applied, rejected = 0, 0
    with (evidence / "rule_install_fixtures.csv").open("w") as ff, (evidence / "rule_install_python.csv").open("w") as ef:
        for index, row in enumerate(product((0, 1), repeat=12)):
            state, command = decode(row)
            result = install(state, command)
            owner, current, version, grant_op, revoked, actor, expected_rule, expected_version, new_rule, op, epoch_bad, lease_bad = row
            expected = (owner == actor and current == expected_rule and version == expected_version
                        and grant_op == op == revoked == epoch_bad == lease_bad == 0 and new_rule == 1)
            assert result.applied is expected
            assert result.state.source == state.source and result.state.draft == state.draft
            assert result.state.draft_revision == state.draft_revision
            assert result.state.unrelated == state.unrelated and result.state.grant == state.grant
            if expected:
                applied += 1
                assert result.state.rule is Rule.EXACT
                assert result.state.rule_history == state.rule_history + (state.rule,)
                assert [accepts(result.state.rule, x, DATA) for x in (DATA, DATA + b"\n", b"X" + DATA[1:])] == [True, False, False]
            else:
                rejected += 1
                assert result.state == state
            ff.write(",".join(map(str, row)) + "\n")
            ef.write(",".join(map(str, project(index, state, result))) + "\n")
    record = {"cases": applied + rejected, "applied": applied, "rejected": rejected,
              "fields": FIELDS,
              "output_fields": ["index", "applied", "new_rule", "rule_version", "draft_preserved",
                                "source_preserved", "rule_history_length", "unrelated_preserved",
                                "accept_exact_source", "accept_extra_LF", "accept_other_wrong"],
              "source_sha256": sha256(DATA).hexdigest(),
              "fixture_sha256": sha256((evidence / "rule_install_fixtures.csv").read_bytes()).hexdigest(),
              "python_output_sha256": sha256((evidence / "rule_install_python.csv").read_bytes()).hexdigest(),
              "scope": "4096 typed binary fixture combinations; no all-input implementation-refinement claim"}
    (evidence / "RULE_INSTALL_BOUNDED_AUDIT.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


def compare():
    evidence = ROOT / "evidence"
    a = (evidence / "rule_install_python.csv").read_text().splitlines()
    b = (evidence / "rule_install_lean.csv").read_text().splitlines()
    differences = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    result = {"python_rows": len(a), "lean_rows": len(b), "mismatches": len(differences),
              "same_length": len(a) == len(b), "first_mismatch": differences[0] if differences else None,
              "python_sha256": sha256((evidence / "rule_install_python.csv").read_bytes()).hexdigest(),
              "lean_sha256": sha256((evidence / "rule_install_lean.csv").read_bytes()).hexdigest(),
              "passed": len(a) == len(b) and not differences}
    (evidence / "RULE_INSTALL_CROSS_LANGUAGE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result["passed"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("generate", "compare"))
    action = parser.parse_args().action
    if action == "generate":
        generate()
    else:
        raise SystemExit(0 if compare() else 1)
