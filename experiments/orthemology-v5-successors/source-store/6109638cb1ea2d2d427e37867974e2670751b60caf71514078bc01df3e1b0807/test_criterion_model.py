"""Test-first specification of a bounded in-memory repair model.

No test changes GitHub, the canonical source, permissions, or external state.
"""
from dataclasses import replace
from pathlib import Path
import unittest

from criterion_model import (
    Source, Grant, State, Command, Outcome, weak_accept, exact_accept, execute,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BYTES = (ROOT / "sources/proper-function-and-candidate-e.md").read_bytes()
TARGET = (
    "theislampill/orthemology",
    "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
    "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md",
)


def fixture():
    source = Source(TARGET, SOURCE_BYTES, frozenset({"canonical-github-object"}))
    grant = Grant("A", "A/draft", TARGET, 7, 10, 20, "replace-derived")
    state = State(source, "A/draft", SOURCE_BYTES + b"\n", 4, 7, grant, False, 12, ())
    command = Command("A", "A/draft", TARGET, "C1-exact", 4, 7,
                      SOURCE_BYTES, "replace-derived", 11, 19)
    return state, command


class CriterionTests(unittest.TestCase):
    def test_weak_criterion_accepts_actual_extra_newline_defect(self):
        self.assertTrue(weak_accept(SOURCE_BYTES + b"\n", SOURCE_BYTES))

    def test_exact_criterion_rejects_extra_newline(self):
        self.assertFalse(exact_accept(SOURCE_BYTES + b"\n", SOURCE_BYTES))

    def test_exact_criterion_accepts_identical_bytes(self):
        self.assertTrue(exact_accept(SOURCE_BYTES, SOURCE_BYTES))

    def test_exact_criterion_rejects_changed_byte(self):
        self.assertFalse(exact_accept(b"X" + SOURCE_BYTES[1:], SOURCE_BYTES))


class ExecutionTests(unittest.TestCase):
    def assertRejectedUnchanged(self, state, command):
        outcome = execute(state, command)
        self.assertFalse(outcome.applied)
        self.assertEqual(outcome.state, state)

    def test_valid_repair_preserves_source_and_retains_previous_draft(self):
        state, command = fixture()
        outcome = execute(state, command)
        self.assertTrue(outcome.applied)
        self.assertEqual(outcome.state.draft, SOURCE_BYTES)
        self.assertEqual(outcome.state.source, state.source)
        self.assertEqual(outcome.state.history, (state.draft,))
        self.assertEqual(outcome.state.revision, state.revision + 1)
        self.assertEqual(outcome.state.authorization_epoch, state.authorization_epoch)
        self.assertEqual(outcome.state.grant, state.grant)

    def test_copied_grant_does_not_authorize_different_actor(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, actor="B"))

    def test_copied_payload_does_not_authorize_different_destination(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, destination="B/draft"))

    def test_source_identity_must_match_even_if_payload_is_identical(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, target=(TARGET[0], "different-commit", TARGET[2])))

    def test_equal_bytes_do_not_erase_revision_identity(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, revision=state.revision + 1), command)

    def test_authorization_epoch_change_blocks_old_command(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, authorization_epoch=8), command)

    def test_current_revocation_blocks_old_command(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, revoked=True), command)

    def test_missing_grant_blocks_command(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, grant=None), command)

    def test_grant_target_is_not_just_a_display_label(self):
        state, command = fixture()
        grant = replace(state.grant, target=(TARGET[0], TARGET[1], "other.md"))
        self.assertRejectedUnchanged(replace(state, grant=grant), command)

    def test_grant_destination_is_checked(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, grant=replace(state.grant, destination="other")), command)

    def test_grant_epoch_is_checked(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, grant=replace(state.grant, authorization_epoch=8)), command)

    def test_grant_operation_is_checked(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, grant=replace(state.grant, operation="read")), command)

    def test_command_operation_is_checked(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, operation="overwrite-source"))

    def test_lease_end_is_exclusive(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, now=19), command)

    def test_command_cannot_extend_grant_lifetime(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, lease_end=21))

    def test_command_from_future_is_rejected(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, observed_at=13))

    def test_not_yet_valid_grant_is_rejected(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, now=9), replace(command, observed_at=8))

    def test_disputed_criterion_cannot_certify_its_own_replacement(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, criterion="C0-normalized"))

    def test_invalid_payload_is_rejected_despite_all_contextual_bindings(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, payload=SOURCE_BYTES + b"\n"))

    def test_replaying_success_is_safe_rejection_not_second_mutation(self):
        state, command = fixture()
        first = execute(state, command)
        self.assertTrue(first.applied)
        self.assertRejectedUnchanged(first.state, command)

    def test_recipient_b_can_reuse_criterion_with_its_own_fresh_grant(self):
        state, command = fixture()
        grant = replace(state.grant, actor="B", destination="B/draft")
        state_b = replace(state, destination="B/draft", grant=grant)
        command_b = replace(command, actor="B", destination="B/draft")
        outcome = execute(state_b, command_b)
        self.assertTrue(outcome.applied)
        self.assertEqual(outcome.state.draft, SOURCE_BYTES)
        self.assertEqual(outcome.state.source.roots, frozenset({"canonical-github-object"}))


if __name__ == "__main__":
    unittest.main()
