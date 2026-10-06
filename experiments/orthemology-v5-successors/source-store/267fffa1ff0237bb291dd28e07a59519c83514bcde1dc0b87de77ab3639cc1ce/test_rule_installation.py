from dataclasses import replace
from pathlib import Path
import unittest

from criterion_model import Source, Grant, State, Command, execute
from rule_install_model import Rule, RuleState, InstallCommand, accepts, install

ROOT = Path(__file__).resolve().parents[1]
DATA = (ROOT / "sources/proper-function-and-candidate-e.md").read_bytes()
TARGET = ("theislampill/orthemology", "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
          "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")


def fixture():
    source = Source(TARGET, DATA, frozenset({"canonical-github-object"}))
    grant = Grant("A", "A/package", TARGET, 2, 0, 10, "install-criterion")
    state = RuleState(source, "A/package", "exact-source-recovery", DATA + b"\n", 8,
                      Rule.NORMALIZED_LF, 3, 2, grant, False, 4,
                      (Rule.NORMALIZED_LF,), ("retain-original-source", "no-GitHub-mutation"))
    command = InstallCommand("A", "A/package", TARGET, Rule.NORMALIZED_LF, 3, 2,
                             Rule.EXACT, "install-criterion", 3, 9)
    return state, command


class RuleInstallationTests(unittest.TestCase):
    def assertRejectedUnchanged(self, state, command):
        outcome = install(state, command)
        self.assertFalse(outcome.applied)
        self.assertEqual(outcome.state, state)

    def test_installs_exact_rule_and_changes_actual_decisions(self):
        state, command = fixture()
        candidates = (DATA, DATA + b"\n", b"X" + DATA[1:])
        self.assertEqual([accepts(state.rule, x, DATA) for x in candidates], [True, True, False])
        result = install(state, command)
        self.assertTrue(result.applied)
        self.assertEqual(result.state.rule, Rule.EXACT)
        self.assertEqual([accepts(result.state.rule, x, DATA) for x in candidates], [True, False, False])

    def test_source_draft_and_unrelated_state_are_preserved(self):
        state, command = fixture()
        result = install(state, command)
        self.assertTrue(result.applied)
        self.assertEqual(result.state.source, state.source)
        self.assertEqual(result.state.draft, state.draft)
        self.assertEqual(result.state.draft_revision, state.draft_revision)
        self.assertEqual(result.state.standard, state.standard)
        self.assertEqual(result.state.unrelated, state.unrelated)
        self.assertEqual(result.state.grant, state.grant)
        self.assertEqual(result.state.authorization_epoch, state.authorization_epoch)
        self.assertEqual(result.state.rule_version, state.rule_version + 1)
        self.assertEqual(result.state.rule_history, state.rule_history + (state.rule,))

    def test_rule_installation_does_not_claim_bad_draft_is_repaired(self):
        state, command = fixture()
        result = install(state, command)
        self.assertTrue(result.applied)
        self.assertNotEqual(result.state.draft, DATA)
        self.assertFalse(accepts(result.state.rule, result.state.draft, DATA))

    def test_data_repair_grant_does_not_authorize_rule_installation(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, grant=replace(state.grant, operation="replace-derived")), command)

    def test_installation_grant_does_not_authorize_data_repair(self):
        state, command = fixture()
        payload_state = State(state.source, state.destination, state.draft, state.draft_revision,
                              state.authorization_epoch, state.grant, False, state.now, ())
        payload_command = Command("A", state.destination, TARGET, "C1-exact", state.draft_revision,
                                  2, DATA, "replace-derived", 3, 9)
        result = execute(payload_state, payload_command)
        self.assertFalse(result.applied)
        self.assertEqual(result.state, payload_state)
        own_grant = replace(state.grant, operation="replace-derived")
        repaired = execute(replace(payload_state, grant=own_grant), payload_command)
        self.assertTrue(repaired.applied)
        self.assertEqual(repaired.state.draft, DATA)

    def test_copied_actor_does_not_inherit_install_grant(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, actor="B"))

    def test_fresh_b_grant_reuses_same_proof_without_new_source_root(self):
        state, command = fixture()
        state_b = replace(state, destination="B/package",
                          grant=replace(state.grant, actor="B", destination="B/package"))
        command_b = replace(command, actor="B", destination="B/package")
        result = install(state_b, command_b)
        self.assertTrue(result.applied)
        self.assertEqual(result.state.rule, Rule.EXACT)
        self.assertEqual(result.state.source.roots, state.source.roots)

    def test_stale_rule_version_rejects_even_if_rule_bytes_unchanged(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, rule_version=4), command)

    def test_wrong_expected_rule_is_rejected(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, expected_rule=Rule.EXACT))

    def test_wrong_new_rule_is_rejected(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, new_rule=Rule.NORMALIZED_LF))

    def test_wrong_rule_operation_is_rejected(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, operation="replace-derived"))

    def test_changed_retained_standard_is_not_silently_accepted(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, standard="normalized-content-recovery"), command)

    def test_source_target_is_bound(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, target=(TARGET[0], "other", TARGET[2])))

    def test_destination_is_bound(self):
        state, command = fixture()
        self.assertRejectedUnchanged(state, replace(command, destination="B/package"))

    def test_current_epoch_is_bound(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, authorization_epoch=3), command)

    def test_current_revocation_is_respected(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, revoked=True), command)

    def test_missing_grant_rejects(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, grant=None), command)

    def test_expired_lease_rejects(self):
        state, command = fixture()
        self.assertRejectedUnchanged(replace(state, now=9), command)

    def test_replay_cannot_reinstall_at_old_rule_version(self):
        state, command = fixture()
        first = install(state, command)
        self.assertTrue(first.applied)
        self.assertRejectedUnchanged(first.state, command)


if __name__ == "__main__":
    unittest.main()
