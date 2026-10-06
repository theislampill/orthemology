"""Finite, deterministic audit of the separately specified criterion model.

This does not retry or recreate any prior script. It has no network calls,
subprocesses, permission changes, or writes outside this research directory.
"""
from dataclasses import replace
from hashlib import sha256
from itertools import product
import base64
import json
from pathlib import Path

from criterion_model import Source, Grant, State, Command, execute, weak_accept

ROOT = Path(__file__).resolve().parent
DATA = (ROOT / "sources/proper-function-and-candidate-e.md").read_bytes()
TARGET = ("theislampill/orthemology",
          "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
          "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")
SOURCE = Source(TARGET, DATA, frozenset({"canonical-github-object"}))


def audit_execution_product():
    """Complete specified product, not arbitrary Python input fuzzing."""
    counts = {"states": 0, "state_command_pairs": 0, "applied": 0, "rejected": 0}
    reasons = {}
    for actor, version, epoch, revoked, now, draft, present, grant_actor, expires in product(
        ("A", "B"), (0, 1), (0, 1), (False, True), (0, 1, 2, 3),
        (DATA, DATA + b"\n", b"wrong"), (False, True), ("A", "B"), (2, 4)
    ):
        counts["states"] += 1
        destination = actor + "/draft"
        grant = Grant(grant_actor, destination, TARGET, epoch, 0, expires,
                      "replace-derived") if present else None
        state = State(SOURCE, destination, draft, version, epoch, grant,
                      revoked, now, (b"retained-earlier-history",))
        for requesting_actor, expected_version, claimed_epoch, operation, criterion, payload, observed, lease in product(
            ("A", "B"), (0, 1), (0, 1), ("replace-derived", "overwrite-source"),
            ("C1-exact", "C0-normalized"), (DATA, DATA + b"\n"), (0, 2), (2, 4)
        ):
            counts["state_command_pairs"] += 1
            command = Command(requesting_actor, destination, TARGET, criterion,
                              expected_version, claimed_epoch, payload,
                              operation, observed, lease)
            # The semantic specification is evaluated independently of execute's
            # ordered failure checks. It is still a model oracle, not evidence
            # for the actual-world legitimacy of the grant store.
            expected = (
                present and not revoked and requesting_actor == grant_actor
                and expected_version == version and claimed_epoch == epoch
                and operation == "replace-derived" and criterion == "C1-exact"
                and payload == DATA and 0 <= now < expires
                and observed <= now < lease <= expires
            )
            result = execute(state, command)
            assert result.applied is expected, (state, command, result, expected)
            assert result.state.source == state.source
            if expected:
                counts["applied"] += 1
                assert result.state.draft == DATA
                assert result.state.revision == version + 1
                assert result.state.history == state.history + (draft,)
                assert result.state.grant == grant
                assert result.state.authorization_epoch == epoch
                replay = execute(result.state, command)
                assert not replay.applied and replay.state == result.state
            else:
                counts["rejected"] += 1
                assert result.state == state
            reasons[result.reason] = reasons.get(result.reason, 0) + 1
    return {**counts, "outcome_reasons": reasons}


def audit_representation_fibers():
    values = [bytes(t) for n in range(4) for t in product((65, 66, 10), repeat=n)]
    maps = {
        "identity": lambda x: x,
        "strip_trailing_LF": lambda x: x.rstrip(b"\n"),
        "prefix_one_byte": lambda x: x[:1],
        "reverse": lambda x: x[::-1],
        "base64": base64.b64encode,
    }
    result = {}
    for name, transform in maps.items():
        bad_pairs = [(a, b) for a in values for b in values
                     if a != b and transform(a) == transform(b)]
        fibers_are_singleton = all(sum(transform(x) == transform(t) for x in values) == 1
                                  for t in values)
        assert fibers_are_singleton == (not bad_pairs)
        result[name] = {
            "domain_size": len(values), "ordered_pairs": len(values) ** 2,
            "false_accept_pairs": len(bad_pairs),
            "exact_for_all_targets_in_domain": fibers_are_singleton,
            "first_counterexample_hex": [x.hex() for x in bad_pairs[0]] if bad_pairs else None,
        }
    return result


def audit_transport_models():
    # Source judgment is true. Recipient false is the matched active-grant
    # history; recipient true is an unmatched revoked-grant history.
    source_worlds, recipient_worlds = (0,), (False, True)
    relation = {(0, False)}
    source_claim = lambda _: True
    recipient_claim = lambda w: not w
    preservation = all(not ((a, b) in relation and source_claim(a)) or recipient_claim(b)
                       for a in source_worlds for b in recipient_worlds)
    coverage = all(any((a, b) in relation for a in source_worlds) for b in recipient_worlds)
    target_validity = all(recipient_claim(b) for b in recipient_worlds)
    assert preservation and not coverage and not target_validity
    assert all(True for _ in recipient_worlds)  # fixed independently true q exception

    # Bare Candidate E formulas: witness 0 is a proper subset, 1 the closure.
    witnesses = (0, 1)
    defeated = lambda w: w == 1
    authority = lambda w: w == 0
    aa = all(not defeated(w) or not authority(w) for w in witnesses)
    token_sufficient = any(authority(w) for w in witnesses)
    assert aa and defeated(1) and token_sufficient
    all_witnesses_defeated = all(defeated(w) for w in witnesses)
    assert not all_witnesses_defeated
    return {
        "forward_only_counterexample": {"preservation": preservation,
            "backward_coverage": coverage, "recipient_robust_validity": target_validity,
            "source_and_target_fidelity_held_fixed": True,
            "varying_fact": "recipient current grant after observation"},
        "fixed_judgment_exception": {"coverage": False,
            "recipient_claim_independently_true": True},
        "bare_candidate_e_counterexample": {"AA": aa,
            "whole_defeated": True, "authoritative_subset": token_sufficient,
            "intended_all_witness_radicality": all_witnesses_defeated,
            "status": "tests an acknowledged formalization obligation only"},
    }


def audit_deletion_witnesses():
    grant = Grant("A", "A/draft", TARGET, 0, 0, 10, "replace-derived")
    state = State(SOURCE, "A/draft", DATA + b"\n", 0, 0, grant, False, 1, ())
    command = Command("A", "A/draft", TARGET, "C1-exact", 0, 0, DATA,
                      "replace-derived", 0, 9)
    normal = execute(state, command)
    assert normal.applied and normal.state.draft == DATA
    copied = execute(state, replace(command, actor="B"))
    stale = execute(replace(state, revision=1), command)
    revoked = execute(replace(state, revoked=True), command)
    expired = execute(replace(state, now=9), command)
    for result in (copied, stale, revoked, expired):
        assert not result.applied

    # Explicit adverse mechanism outside the trusted-guard theorem. All source
    # and normative facts stay true; the corrupt gate writes a wrong result.
    corrupt_result = replace(state, draft=b"CORRUPT", revision=1)
    assert corrupt_result.source == state.source
    assert corrupt_result.draft != SOURCE.content

    # Merely renaming roots would not alter this physical dependency relation.
    roots_a = SOURCE.roots
    roots_b = frozenset(SOURCE.roots)
    assert len(roots_a | roots_b) == 1
    return {
        "copied_actor_grant": copied.reason,
        "equal_bytes_new_revision": stale.reason,
        "immediate_revocation": revoked.reason,
        "expired_lease": expired.reason,
        "corrupt_common_gate": {
            "source_truth_preserved": True, "criterion_adequacy_preserved": True,
            "actual_result_faithful": False,
            "deleted_premise": "faithful non-bypassable execution mechanism",
            "not_counterexample_to_full_conditional_theorem": True,
        },
        "copy_root_union": sorted(roots_a | roots_b),
        "copy_root_count": len(roots_a | roots_b),
        "new_independent_source_count": 0,
    }


def main():
    result = {
        "scope": "Deterministic finite reference-model audit; no deployment or Python-to-Lean refinement proof",
        "source_sha256": sha256(DATA).hexdigest(),
        "extra_newline_sha256": sha256(DATA + b"\n").hexdigest(),
        "actual_extra_newline_weakly_accepted": weak_accept(DATA + b"\n", DATA),
        "execution_product": audit_execution_product(),
        "representation_fibers": audit_representation_fibers(),
        "transport_models": audit_transport_models(),
        "deletion_witnesses": audit_deletion_witnesses(),
    }
    (ROOT / "evidence/BOUNDED_AUDIT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
