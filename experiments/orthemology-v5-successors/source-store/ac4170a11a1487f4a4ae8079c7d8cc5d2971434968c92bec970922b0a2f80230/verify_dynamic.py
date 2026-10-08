#!/usr/bin/env python3
"""Fresh bounded mathematical checks; no inherited Seventh check is invoked.

Every control is finite and reports its scope. Ordinary and Lean proofs provide
the stated generality. Uses only the Python standard library and local inputs.
"""

from __future__ import annotations

from dataclasses import replace
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import hashlib
import json

from dynamic_interlock import Actor, Command, Descriptor, World, threshold_contract

OUT = Path(__file__).resolve().parent
COUNTS: dict[str, int] = {}
TRACES: dict[str, dict] = {}


def subsets(n: int, k: int):
    return [frozenset(x) for x in combinations(range(n), k)]


def check_thresholds() -> None:
    pairs = 0
    parameter_cases = 0
    # Compute the actual worst cross-intersection for each pair of thresholds,
    # rather than assuming its formula in the checker.
    for n in range(1, 10):
        by_size = {k: subsets(n, k) for k in range(1, n + 1)}
        minima = {}
        for q in range(1, n + 1):
            for r in range(1, n + 1):
                observed = n
                for left in by_size[q]:
                    for right in by_size[r]:
                        pairs += 1
                        observed = min(observed, len(left & right))
                minima[q, r] = observed
                assert observed == max(0, q + r - n)
        for b in range(n):
            feasible = []
            for q in range(1, n + 1):
                for r in range(1, n + 1):
                    parameter_cases += 1
                    actual = minima[q, r] > b and q <= n - b and r <= n - b
                    assert actual == threshold_contract(n, b, q, r)
                    if actual:
                        feasible.append((q, r))
                        assert q > b and r > b
            assert bool(feasible) == (n >= 3 * b + 1)
            if n == 3 * b + 1:
                assert feasible == [(2 * b + 1, 2 * b + 1)]
    COUNTS["cross_quorum_pairs_n_le_9"] = pairs
    COUNTS["threshold_parameter_cases_n_le_9"] = parameter_cases


def initial() -> Descriptor:
    return Descriptor(0, "two-input-rule", 10, "actor-A", "replace-rule", (0, 1))


def check_stale_gate_traces() -> None:
    cases = 0
    for b in range(3):
        n, q, r = 3 * b + 1, 2 * b + 1, 2 * b + 1
        for c_size in range(b + 1):
            for tainted in subsets(n, c_size):
                for left in subsets(n, q):
                    for right in subsets(n, r):
                        world = World(n, b, q, r, initial(), tainted)
                        command = Command.for_descriptor(world.descriptor, left, 0)
                        assert world.prepare(command, requester="actor-A")
                        # Deliberately hide the new descriptor from every root
                        # outside the revocation set and from the actor.
                        next_d = replace(initial(), epoch=1, target_version=11,
                                         table=(1, 0))
                        world.revoke(right, next_d)
                        assert world.attempt(command, requester="actor-A", bad_open=True) == "NO_EFFECT"
                        assert not world.unsafe and world.table == (1, 1)
                        cases += 1
    COUNTS["executable_stale_landing_cases_B_le_2"] = cases


def check_repair_and_persistence() -> None:
    cases = 0
    batch_slots = 0
    for b in range(4):
        n, q, r = 3 * b + 1, 2 * b + 1, 2 * b + 1
        for c_size in range(b + 1):
            for tainted in subsets(n, c_size):
                world = World(n, b, q, r, initial(), tainted)
                actor = Actor(initial())
                # A genuine prior version change precedes the final stable epoch.
                next_d = replace(initial(), epoch=1, target_version=11, table=(1, 0))
                revokers = frozenset(range(r))
                certificate = world.revoke(revokers, next_d)
                world.deliver(certificate, actor)
                slots = world.run_batch(actor)
                assert slots == comb(n, q)
                assert world.table == next_d.table and not world.unsafe
                # Repeating every operation retains the full repaired table.
                assert world.run_batch(actor) == slots
                assert world.table == next_d.table and not world.unsafe
                cases += 1
                batch_slots += slots * 2
    COUNTS["quiescent_repair_fault_sets_B_le_3"] = cases
    COUNTS["quiescent_and_persistence_attempt_slots"] = batch_slots


def check_actor_custody() -> None:
    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    actor = Actor(initial())
    final = replace(initial(), epoch=1, target_version=11, table=(1, 0))
    certificate = world.revoke({1, 2, 3}, final)
    world.deliver(certificate)  # To good roots only, not secretly to the actor.
    assert actor.descriptor.epoch == 0
    assert world.run_batch(actor) == 4
    assert world.table == (1, 1) and not world.unsafe
    assert all(x["receipt"] == "NO_EFFECT" for x in world.history if x["event"] == "attempt")
    world.deliver(certificate, actor)
    assert actor.descriptor.epoch == 1
    assert world.run_batch(actor) == 4
    assert world.table == final.table and not world.unsafe
    save_trace("actor_requires_received_certificate", world, expected="SAFE_THEN_REPAIRED_AFTER_DELIVERY",
               note="The actor's batch uses its custody, not the global descriptor oracle.")
    COUNTS["actor_local_descriptor_matched_cases"] = 2
    rotation_cases = 0
    for bad_root in range(4):
        for cursor in range(4):
            final_world = World(4, 1, 3, 3, final, frozenset({bad_root}))
            cycling_actor = Actor(final, cursor=cursor)
            final_world.run_batch(cycling_actor)
            assert final_world.table == final.table and not final_world.unsafe
            rotation_cases += 1
    COUNTS["stable_suffix_cycle_alignment_cases"] = rotation_cases


def check_minimal_search_bound() -> None:
    uniqueness_cases = 0
    for b in range(5):
        n, q = 3 * b + 1, 2 * b + 1
        roots = frozenset(range(n))
        all_paths = subsets(n, q)
        assert len(all_paths) == comb(n, b)
        for tainted in subsets(n, b):
            good = [p for p in all_paths if not (p & tainted)]
            assert good == [roots - tainted]
            uniqueness_cases += 1
    # Every possible B=1 path order, every prefix, and an actual fixed hidden
    # taint witness to failure of any cap below N.
    n, b, q = 4, 1, 3
    roots = frozenset(range(n))
    prefix_cases = 0
    for order in permutations(subsets(n, q)):
        for k in range(len(order)):
            unseen = order[k]
            tainted = roots - unseen
            assert all(p & tainted for p in order[:k])
            assert not (unseen & tainted)
            prefix_cases += 1
    COUNTS["unique_good_path_cases_B_le_4"] = uniqueness_cases
    COUNTS["all_B1_search_order_prefixes"] = prefix_cases


def check_complete_command_binding() -> None:
    mutations = {
        "target_id": "other-rule", "target_version": 12, "epoch": 1,
        "recipient": "actor-B", "scope": "unapproved-write", "table": (1, 0),
        "nonce": 7, "path": frozenset({0, 1, 3}),
    }
    for field, value in mutations.items():
        world = World(4, 1, 3, 3, initial(), frozenset({0}))
        approved = Command.for_descriptor(initial(), {0, 1, 2}, 0)
        assert world.prepare(approved, requester="actor-A")
        substituted = replace(approved, **{field: value})
        assert world.attempt(substituted, requester="actor-A") == "NO_EFFECT"
        assert not world.unsafe and world.table == (1, 1)
        # A rejected mutation preserves future ability to execute the original.
        assert world.attempt(approved, requester="actor-A") == "APPLIED"
        assert world.table == initial().table and not world.unsafe
    COUNTS["complete_command_binding_and_future_route_controls"] = len(mutations)


def check_charged_cancellation() -> None:
    cases = 0
    for b in range(3):
        n, q = 3*b+1, 2*b+1
        for faults in subsets(n, b):
            for path in subsets(n, q):
                for acknowledgers in combinations(sorted(path), b+1):
                    world = World(n, b, q, q, initial(), faults)
                    command = Command.for_descriptor(initial(), path, 1)
                    assert world.prepare(command, requester="actor-A")
                    assert world.cancel_with_acknowledgers(command, acknowledgers, requester="actor-A")
                    # A late gate opening, including all bad roots cooperating,
                    # cannot revive the command after its cancellation certificate.
                    assert world.attempt(command, requester="actor-A", bad_open=True) == "NO_EFFECT"
                    assert world.table == (1, 1) and not world.unsafe
                    cases += 1
    COUNTS["charged_cancellation_late_landing_cases_B_le_2"] = cases
    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    command = Command.for_descriptor(initial(), {0, 1, 2}, 1)
    assert world.prepare(command, requester="actor-A")
    assert world.cancel_with_acknowledgers(command, {0}, requester="actor-A", threshold=1)
    assert world.attempt(command, requester="actor-A", bad_open=True) == "APPLIED"
    save_trace("too_small_cancellation_certificate", world,
               expected="LATE_WRITE_AFTER_FALSE_CANCELLATION",
               note="One bad root can falsely acknowledge; B+1 root acknowledgements are required.")
    # Landing can lawfully win the race. Authenticated cancellation then closes
    # only that nonce, preserving the already repaired state and all fresh work.
    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    command = Command.for_descriptor(initial(), {0, 1, 2}, 2)
    assert world.prepare(command, requester="actor-A")
    assert not world.cancel_with_acknowledgers(command, command.path, requester="actor-B")
    assert world.attempt(command, requester="actor-B") == "NO_EFFECT"
    assert world.attempt(command, requester="actor-A") == "APPLIED"
    world.cancel(command, requester="actor-A", bad_ack=True)
    assert world.attempt(command, requester="actor-A", bad_open=True) == "NO_EFFECT"
    assert world.table == initial().table and not world.unsafe
    assert not world.prepare(command, requester="actor-A")
    fresh = replace(command, nonce=3)
    assert world.prepare(fresh, requester="actor-A")
    assert world.attempt(fresh, requester="actor-A") == "APPLIED"
    save_trace("authenticated_cancellation_race_and_nonce", world,
               expected="REPAIR_PRESERVED_AND_FRESH_ROUTE_OPEN",
               note="Foreign actor cannot cancel or execute; old nonce stays closed; new nonce remains available.")

    # A delivered grant for another recipient must not rename the actor.
    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    actor = Actor(initial())
    other = replace(initial(), epoch=1, recipient="actor-B")
    certificate = world.revoke({1, 2, 3}, other)
    world.deliver(certificate, actor)
    assert actor.identity == "actor-A" and actor.descriptor.recipient == "actor-B"
    world.run_batch(actor)
    assert not world.unsafe and world.table == (1, 1)
    save_trace("new_recipient_does_not_rename_actor", world,
               expected="SAFE_WITHOUT_UNAUTHORIZED_REPAIR",
               note="A copied current descriptor cannot turn actor A into recipient B.")
    COUNTS["cancellation_race_identity_and_nonce_controls"] = 2


def save_trace(name: str, base: World, *, expected: str, note: str) -> None:
    TRACES[name] = {"parameters": {"n": base.n, "B": base.budget,
                                   "q": base.q, "r": base.r,
                                   "tainted": sorted(base.tainted)},
                    "expected": expected, "note": note,
                    "unsafe": base.unsafe, "history": base.history}


def check_deletions() -> None:
    # Live commitments vs old cached votes, with the exact same root budget.
    for cached in (False, True):
        world = World(4, 1, 3, 3, initial(), frozenset({0}))
        command = Command.for_descriptor(initial(), {0, 1, 2}, 0)
        world.prepare(command, requester="actor-A")
        world.revoke({1, 2, 3}, replace(initial(), epoch=1, allowed=False))
        result = world.attempt(command, requester="actor-A", cached_votes=cached)
        assert result == ("UNSAFE" if cached else "NO_EFFECT")
        save_trace("cached_votes" if cached else "live_commitment_control", world,
                   expected=result, note="Revocation closes actual shared good gates; cached votes ignore closure.")

    # One corrupted dispatcher switches the payload after preparation.
    for exact_binding in (True, False):
        world = World(4, 1, 3, 3, initial(), frozenset({0}))
        approved = Command.for_descriptor(initial(), {0, 1, 2}, 0)
        world.prepare(approved, requester="actor-A")
        substituted = replace(approved, table=(1, 1))
        result = world.attempt(substituted, requester="actor-A", checked_command=None if exact_binding else approved)
        assert result == ("NO_EFFECT" if exact_binding else "UNSAFE")
        save_trace("exact_payload_control" if exact_binding else "mutable_payload", world,
                   expected=result, note="Correct target proof does not bind a substituted physical write.")

    # Same target/version/payload, only recipient authorization epoch changes.
    for check_epoch in (True, False):
        world = World(4, 1, 3, 3, initial(), frozenset({0}))
        command = Command.for_descriptor(initial(), {0, 1, 2}, 0)
        world.prepare(command, requester="actor-A")
        world.revoke({1, 2, 3}, replace(initial(), epoch=1, allowed=False))
        result = world.attempt(command, requester="actor-A", omit_authorization_epoch=not check_epoch)
        assert result == ("NO_EFFECT" if check_epoch else "UNSAFE")
        save_trace("current_authorization_control" if check_epoch else "current_authorization_deleted", world,
                   expected=result, note="Byte-correct repair can be an unauthorized act.")

    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    command = Command.for_descriptor(initial(), {1, 2, 3}, 0)
    assert world.prepare(command, requester="actor-A")
    assert world.attempt(command, requester="actor-A") == "APPLIED"
    world.unmediated_write(0)
    assert world.unsafe
    save_trace("common_downstream_writer", world, expected="UNSAFE",
               note="Shared writer root 0 is charged, not declared trusted after failure.")

    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    for nonce, path in enumerate(subsets(4, 3)):
        command = Command.for_descriptor(initial(), path, nonce)
        world.prepare(command, requester="actor-A")
        world.common_selector_drop(0, command)
    assert world.table != world.descriptor.table and not world.unsafe
    save_trace("common_selector_omitted", world, expected="SAFE_BUT_NEVER_RESTORED",
               note="Every actual liveness support contains root 0, including advertised path {1,2,3}.")

    # Too-small cross-quorum overlap despite static availability/containment.
    world = World(3, 1, 2, 2, initial(), frozenset({1}))
    command = Command.for_descriptor(initial(), {0, 1}, 0)
    assert world.prepare(command, requester="actor-A")
    world.revoke({1, 2}, replace(initial(), epoch=1, allowed=False))
    assert world.attempt(command, requester="actor-A") == "UNSAFE"
    save_trace("two_B_plus_one_failed_candidate", world, expected="UNSAFE",
               note="Repair and revocation share only the one tainted root.")

    # Independent external permission ceases before any gate has learned it.
    world = World(4, 1, 3, 3, initial(), frozenset())
    command = Command.for_descriptor(initial(), {0, 1, 2}, 0)
    assert world.prepare(command, requester="actor-A")
    world.descriptor = replace(initial(), allowed=False)
    world.history.append({"event": "immediate_external_consent_end_without_gate_notice"})
    assert world.attempt(command, requester="actor-A") == "UNSAFE"
    save_trace("immediate_external_revocation", world, expected="UNSAFE",
               note="Deletes the reservation institution; not a valid base-model transition.")

    # A genuinely mobile historical-ack attack. This explicitly violates the
    # union bound and is not passed to World as if it were a valid taint set.
    mobility = []
    for root in (1, 2, 3):
        mobility.append({"currently_faulty": [root], "false_ack": root,
                         "old_gate_retained": True})
        mobility.append({"currently_faulty": [], "restored_appearance": root,
                         "revocation_state_not_recovered": True})
    assert all(len(event["currently_faulty"]) <= 1 for event in mobility)
    ever = {event["false_ack"] for event in mobility if "false_ack" in event}
    assert len(ever) == 3 > 1
    TRACES["instantaneous_budget_failed_candidate"] = {
        "history": mobility,
        "instantaneous_bound": 1,
        "lifetime_tainted": sorted(ever),
        "expected": "FAILS_LIFETIME_PREMISE",
        "note": "Apparent recovery does not erase false historical acknowledgements or tainted state."}

    # A valid perpetual-change trace defeats unqualified eventual persistence.
    world = World(4, 1, 3, 3, initial(), frozenset({0}))
    actor = Actor(initial())
    for epoch in range(1, 5):
        if world.completed:
            world.deliver(world.completed[-1], actor)
        world.run_batch(actor)
        assert world.table == world.descriptor.table and not world.unsafe
        next_table = (1, 0) if world.table == (0, 1) else (0, 1)
        world.revoke({1, 2, 3}, replace(world.descriptor, epoch=epoch,
                                     target_version=10 + epoch, table=next_table))
        assert world.table != world.descriptor.table and not world.unsafe
    save_trace("perpetual_version_change_prefix", world, expected="SAFE_NONPERSISTENT_PREFIX",
               note="Four-step regression prefix of the ordinary infinite alternating-target counterexample.")
    COUNTS["deletion_and_matched_control_traces"] = len(TRACES)


def main() -> None:
    check_thresholds()
    check_stale_gate_traces()
    check_repair_and_persistence()
    check_actor_custody()
    check_minimal_search_bound()
    check_complete_command_binding()
    check_charged_cancellation()
    check_deletions()
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (OUT / "dynamic_interlock.py", OUT / "verify_dynamic.py")}
    result = {"status": "PASS_FINITE_DECLARED_CONTROLS", "counts": COUNTS,
              "scope": "Finite enumerations and executable traces, not a general proof or a deployment test.",
              "source_sha256": sources,
              "minimal_parameters": [{"B": b, "n": 3*b+1, "q": 2*b+1,
                                      "r": 2*b+1, "N": comb(3*b+1, b)} for b in range(7)]}
    (OUT / "FINITE_CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    (OUT / "DELETION_TRACES.json").write_text(json.dumps(TRACES, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
