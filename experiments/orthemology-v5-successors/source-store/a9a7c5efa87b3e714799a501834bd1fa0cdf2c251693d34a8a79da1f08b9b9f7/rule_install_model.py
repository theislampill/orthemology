"""Typed in-memory criterion installation under an explicit retained standard.

The two rule constructors carry defined local semantics, not arbitrary code.
Source, grant, actor and clock records are trusted model inputs.
"""
from dataclasses import dataclass, replace
from enum import Enum

from criterion_model import Source, Grant, Target


class Rule(Enum):
    NORMALIZED_LF = "trailing-LF-normalized-equality"
    EXACT = "exact-byte-equality"


def accepts(rule: Rule, candidate: bytes, source: bytes) -> bool:
    if rule is Rule.NORMALIZED_LF:
        return candidate.rstrip(b"\n") == source.rstrip(b"\n")
    if rule is Rule.EXACT:
        return candidate == source
    raise ValueError("Not a term in the typed two-rule language")


@dataclass(frozen=True)
class RuleState:
    source: Source
    destination: str
    standard: str
    draft: bytes
    draft_revision: int
    rule: Rule
    rule_version: int
    authorization_epoch: int
    grant: Grant | None
    revoked: bool
    now: int
    rule_history: tuple[Rule, ...]
    unrelated: tuple[str, ...]


@dataclass(frozen=True)
class InstallCommand:
    actor: str
    destination: str
    target: Target
    expected_rule: Rule
    expected_version: int
    authorization_epoch: int
    new_rule: Rule
    operation: str
    observed_at: int
    lease_end: int


@dataclass(frozen=True)
class InstallOutcome:
    applied: bool
    state: RuleState
    reason: str


def install(state: RuleState, command: InstallCommand) -> InstallOutcome:
    checks = (
        (state.standard == "exact-source-recovery", "retained-standard"),
        (command.target == state.source.target, "target"),
        (command.destination == state.destination, "destination"),
        (command.expected_rule is state.rule, "expected-rule"),
        (command.expected_version == state.rule_version, "rule-version"),
        (command.authorization_epoch == state.authorization_epoch, "epoch"),
        (command.new_rule is Rule.EXACT, "replacement-semantics"),
        (command.operation == "install-criterion", "operation"),
        (not state.revoked, "revoked"),
        (state.grant is not None, "missing-grant"),
    )
    for passed, reason in checks:
        if not passed:
            return InstallOutcome(False, state, reason)
    grant = state.grant
    assert grant is not None
    grant_checks = (
        (grant.actor == command.actor, "grant-actor"),
        (grant.destination == command.destination, "grant-destination"),
        (grant.target == command.target, "grant-target"),
        (grant.authorization_epoch == state.authorization_epoch, "grant-epoch"),
        (grant.operation == "install-criterion", "grant-operation"),
        (grant.not_before <= state.now < grant.expires, "grant-time"),
        (command.observed_at <= state.now < command.lease_end <= grant.expires,
         "lease-time"),
    )
    for passed, reason in grant_checks:
        if not passed:
            return InstallOutcome(False, state, reason)
    return InstallOutcome(True, replace(state, rule=command.new_rule,
                                        rule_version=state.rule_version + 1,
                                        rule_history=state.rule_history + (state.rule,)), "installed")
