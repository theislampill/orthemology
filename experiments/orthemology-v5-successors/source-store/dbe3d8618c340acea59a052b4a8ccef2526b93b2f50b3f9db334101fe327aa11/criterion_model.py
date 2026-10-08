"""A bounded, deterministic in-memory model of criterion transport.

Source identity/contents and the active grant store are supplied trusted model
inputs. This model proves nothing about the actual authentication of those
inputs or the integrity of the runtime. It performs no external operations.
"""
from dataclasses import dataclass, replace

Target = tuple[str, str, str]


@dataclass(frozen=True)
class Source:
    target: Target
    content: bytes
    roots: frozenset[str]


@dataclass(frozen=True)
class Grant:
    actor: str
    destination: str
    target: Target
    authorization_epoch: int
    not_before: int
    expires: int
    operation: str


@dataclass(frozen=True)
class State:
    source: Source
    destination: str
    draft: bytes
    revision: int
    authorization_epoch: int
    grant: Grant | None
    revoked: bool
    now: int
    history: tuple[bytes, ...]


@dataclass(frozen=True)
class Command:
    actor: str
    destination: str
    target: Target
    criterion: str
    expected_revision: int
    authorization_epoch: int
    payload: bytes
    operation: str
    observed_at: int
    lease_end: int


@dataclass(frozen=True)
class Outcome:
    applied: bool
    state: State
    reason: str


def weak_accept(candidate: bytes, source: bytes) -> bool:
    return candidate.rstrip(b"\n") == source.rstrip(b"\n")


def exact_accept(candidate: bytes, source: bytes) -> bool:
    return candidate == source


def execute(state: State, command: Command) -> Outcome:
    """One atomic guarded step, under the stated trusted-input assumptions.

    Rejection has no state effects. Mutation changes only the derived draft,
    its revision, and the append-only history. Exact source bytes remain fixed.
    """
    grant = state.grant
    checks = (
        (command.target == state.source.target, "target"),
        (command.destination == state.destination, "destination"),
        (command.criterion == "C1-exact", "criterion"),
        (command.expected_revision == state.revision, "revision"),
        (command.authorization_epoch == state.authorization_epoch, "epoch"),
        (command.operation == "replace-derived", "operation"),
        (exact_accept(command.payload, state.source.content), "payload"),
        (not state.revoked, "revoked"),
        (grant is not None, "missing-grant"),
    )
    for passed, reason in checks:
        if not passed:
            return Outcome(False, state, reason)
    assert grant is not None
    grant_checks = (
        (grant.actor == command.actor, "grant-actor"),
        (grant.destination == command.destination, "grant-destination"),
        (grant.target == command.target, "grant-target"),
        (grant.authorization_epoch == state.authorization_epoch, "grant-epoch"),
        (grant.operation == command.operation, "grant-operation"),
        (grant.not_before <= state.now < grant.expires, "grant-time"),
        (command.observed_at <= state.now < command.lease_end <= grant.expires,
         "lease-time"),
    )
    for passed, reason in grant_checks:
        if not passed:
            return Outcome(False, state, reason)
    return Outcome(True, replace(state, draft=command.payload,
                                 revision=state.revision + 1,
                                 history=state.history + (state.draft,)), "applied")
