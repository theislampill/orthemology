"""Executable semantics of the freshly declared versioned live-interlock family.

This is a small mathematical transition system, not a hardware implementation
or a cryptographic library.  Root labels are authenticated model identities.
All active gate/signing/revocation duties of a root share one taint budget.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from itertools import combinations
from typing import FrozenSet, Iterable, Literal

Table = tuple[int, int]
Receipt = Literal["APPLIED", "NO_EFFECT", "UNSAFE"]


@dataclass(frozen=True)
class Descriptor:
    epoch: int
    target_id: str
    target_version: int
    recipient: str
    scope: str
    table: Table
    allowed: bool = True


@dataclass(frozen=True)
class Certificate:
    """A completed, root-authenticated transition certificate in the model."""
    previous_epoch: int
    descriptor: Descriptor
    acknowledgers: FrozenSet[int]


@dataclass
class Actor:
    """The controller uses only its received descriptor, never world ground truth."""
    descriptor: Descriptor
    cursor: int = 0
    nonce: int = 0
    identity: str | None = None

    def __post_init__(self) -> None:
        if self.identity is None:
            self.identity = self.descriptor.recipient

    def receive(self, certificate: Certificate, n: int, r: int) -> None:
        assert len(certificate.acknowledgers) == r
        assert certificate.acknowledgers <= frozenset(range(n))
        assert certificate.descriptor.epoch == certificate.previous_epoch + 1
        # Authentication and the authoritative serial descriptor are model
        # premises.  A stale but valid certificate never rewinds local custody.
        if certificate.descriptor.epoch > self.descriptor.epoch:
            self.descriptor = certificate.descriptor
            self.cursor = 0

    def next_command(self, n: int, q: int) -> Command:
        paths = list(combinations(range(n), q))
        path = paths[self.cursor % len(paths)]
        self.cursor = (self.cursor + 1) % len(paths)
        self.nonce += 1
        command = Command.for_descriptor(self.descriptor, path, self.nonce)
        assert self.identity is not None
        return replace(command, recipient=self.identity)


@dataclass(frozen=True)
class Command:
    epoch: int
    target_id: str
    target_version: int
    recipient: str
    scope: str
    table: Table
    nonce: int
    path: FrozenSet[int]

    @classmethod
    def for_descriptor(cls, d: Descriptor, path: Iterable[int], nonce: int) -> Command:
        return cls(d.epoch, d.target_id, d.target_version, d.recipient,
                   d.scope, d.table, nonce, frozenset(path))

    def authorized_by(self, d: Descriptor) -> bool:
        return d.allowed and (
            self.epoch, self.target_id, self.target_version,
            self.recipient, self.scope, self.table
        ) == (
            d.epoch, d.target_id, d.target_version,
            d.recipient, d.scope, d.table
        )


@dataclass
class Root:
    local: Descriptor
    revoked: set[int] = field(default_factory=set)
    commitments: set[Command] = field(default_factory=set)
    cancelled: set[Command] = field(default_factory=set)

    def prepare(self, command: Command, requester: str) -> bool:
        if (requester == command.recipient and command.authorized_by(self.local)
                and command.epoch not in self.revoked
                and command not in self.cancelled):
            self.commitments.add(command)
            return True
        return False

    def acknowledge(self, old_epoch: int) -> None:
        # Closing is prior to acknowledgement, and does not install the next
        # descriptor before a complete transition certificate exists.
        self.revoked.add(old_epoch)

    def permits(self, command: Command, requester: str) -> bool:
        return (requester == command.recipient and command in self.commitments
                and command.authorized_by(self.local)
                and command.epoch not in self.revoked
                and command not in self.cancelled)

    def cancel(self, command: Command, requester: str) -> bool:
        # Tombstone creation is before the acknowledgement. It also prevents a
        # delayed preparation packet from reopening the same nonce afterwards.
        if requester != command.recipient:
            return False
        self.cancelled.add(command)
        return True


@dataclass
class World:
    n: int
    budget: int
    q: int
    r: int
    descriptor: Descriptor
    tainted: FrozenSet[int]
    table: Table = (1, 1)
    unsafe: bool = False
    roots: list[Root] = field(init=False)
    completed: list[Certificate] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert 0 <= self.budget < self.n
        assert 1 <= self.q <= self.n and 1 <= self.r <= self.n
        assert self.tainted <= frozenset(range(self.n))
        assert len(self.tainted) <= self.budget
        self.roots = [Root(self.descriptor) for _ in range(self.n)]

    def valid_path(self, path: FrozenSet[int]) -> bool:
        return len(path) == self.q and path <= frozenset(range(self.n))

    def prepare(self, command: Command, *, requester: str, bad_sign: bool = True) -> bool:
        assert self.valid_path(command.path)
        granted = []
        for i in sorted(command.path):
            if i in self.tainted:
                # A bad signer can mimic every truthful preparation.  Recording
                # this does not classify it as intact or untainted.
                if bad_sign:
                    self.roots[i].commitments.add(command)
                    granted.append(i)
            elif self.roots[i].prepare(command, requester):
                granted.append(i)
        self.history.append({"event": "prepare", "epoch": command.epoch,
                             "path": sorted(command.path), "grants": granted})
        return len(granted) == self.q

    def revoke(self, acknowledgers: Iterable[int], next_descriptor: Descriptor,
               *, deliver_to_all_good: bool = False) -> Certificate:
        acknowledgers = frozenset(acknowledgers)
        assert len(acknowledgers) == self.r
        assert acknowledgers <= frozenset(range(self.n))
        assert next_descriptor.epoch == self.descriptor.epoch + 1
        old_epoch = self.descriptor.epoch
        for i in acknowledgers:
            if i not in self.tainted:
                self.roots[i].acknowledge(old_epoch)
            # Byzantine acknowledgers can keep their gates open.
        self.descriptor = next_descriptor
        certificate = Certificate(old_epoch, next_descriptor, acknowledgers)
        self.completed.append(certificate)
        self.history.append({"event": "effective_revoke", "old_epoch": old_epoch,
                             "new_epoch": next_descriptor.epoch,
                             "acknowledgers": sorted(acknowledgers)})
        if deliver_to_all_good:
            self.deliver(certificate)
        return certificate

    def deliver(self, certificate: Certificate, actor: Actor | None = None) -> None:
        assert certificate in self.completed
        for i, root in enumerate(self.roots):
            if i not in self.tainted and certificate.descriptor.epoch > root.local.epoch:
                root.local = certificate.descriptor
        if actor is not None:
            actor.receive(certificate, self.n, self.r)
        self.history.append({"event": "deliver_certificate",
                             "epoch": certificate.descriptor.epoch,
                             "to_actor": actor is not None})

    def attempt(self, command: Command, *, requester: str, bad_open: bool = True,
                cached_votes: bool = False,
                checked_command: Command | None = None,
                omit_authorization_epoch: bool = False) -> Receipt:
        """Land via live gates, or one explicitly selected broken variant.

        cached_votes deletes continuing veto. checked_command != command deletes
        exact payload binding. omit_authorization_epoch deletes current permission.
        All three are counterexample controls, never the baseline algorithm.
        """
        # This assertion checks membership in the declared physical-path input
        # domain. It is not claimed as a deployed, independently trusted gate.
        assert self.valid_path(command.path)
        checked = command if checked_command is None else checked_command
        permits = []
        for i in sorted(command.path):
            root = self.roots[i]
            if i in self.tainted:
                permits.append(bad_open)
            elif cached_votes:
                permits.append(checked in root.commitments)
            elif omit_authorization_epoch:
                # Tempting but invalid: immutable target bytes/version are used
                # as if they were a current recipient grant.
                permits.append(checked in root.commitments
                               and checked.target_id == root.local.target_id
                               and checked.target_version == root.local.target_version
                               and checked.table == root.local.table)
            else:
                permits.append(root.permits(checked, requester))
        if not all(permits):
            result: Receipt = "NO_EFFECT"
        elif (self.unsafe or requester != command.recipient
              or not command.authorized_by(self.descriptor)):
            # Ground truth is used only to classify an already permitted bad
            # landing as unsafe. It does NOT veto it or inform the actor.
            self.unsafe = True
            result = "UNSAFE"
        else:
            self.table = command.table
            result = "APPLIED"
        self.history.append({"event": "attempt", "epoch": command.epoch,
                             "path": sorted(command.path), "receipt": result})
        return result

    def unmediated_write(self, root: int) -> None:
        """Counterexample only: add a common writer outside the q-gate mediation."""
        assert root in self.tainted
        self.unsafe = True
        self.history.append({"event": "common_bypass", "root": root,
                             "receipt": "UNSAFE"})

    def cancel_with_acknowledgers(self, command: Command,
                                 acknowledgers: Iterable[int],
                                 *, requester: str,
                                 threshold: int | None = None) -> bool:
        """Close a command using only its own live-gate roots.

        The optional threshold is a deletion-test parameter. The valid protocol
        uses B+1; smaller certificates may consist entirely of Byzantine roots.
        """
        c = self.budget + 1 if threshold is None else threshold
        requested = frozenset(acknowledgers)
        assert requested <= command.path
        acknowledged = set()
        for i in requested:
            if i in self.tainted or self.roots[i].cancel(command, requester):
                acknowledged.add(i)
        completed = len(acknowledged) >= c
        self.history.append({"event": "cancel_certificate", "nonce": command.nonce,
                             "path": sorted(command.path), "threshold": c,
                             "authenticated_requester": requester,
                             "acknowledgers": sorted(acknowledged),
                             "complete": completed})
        return completed

    def cancel(self, command: Command, *, requester: str, bad_ack: bool = False) -> None:
        # The actor requests every path root; the world determines which root
        # replies. It does not reveal taint labels to the actor. Good roots have
        # bounded independent service; Byzantine roots may withhold or falsely ack.
        responders = {i for i in command.path if i not in self.tainted or bad_ack}
        assert self.cancel_with_acknowledgers(command, responders, requester=requester)

    def common_selector_drop(self, root: int, command: Command) -> None:
        """Counterexample only: actual selection support has an omitted common root."""
        assert root in self.tainted
        self.history.append({"event": "common_selector_drop", "root": root,
                             "advertised_path": sorted(command.path),
                             "actual_required_support": sorted(command.path | {root}),
                             "receipt": "NO_EFFECT"})

    def run_batch(self, actor: Actor) -> int:
        """One full cyclic portfolio; no stopping on an untrusted receipt."""
        count = 0
        for count, _path in enumerate(combinations(range(self.n), self.q), start=1):
            command = actor.next_command(self.n, self.q)
            assert actor.identity is not None
            prepared = self.prepare(command, requester=actor.identity)
            if prepared:
                self.attempt(command, requester=actor.identity, bad_open=False)
            else:
                self.history.append({"event": "skip_unprepared_execution",
                                     "nonce": command.nonce, "path": sorted(command.path)})
            self.cancel(command, requester=actor.identity)
        return count


def threshold_contract(n: int, budget: int, q: int, r: int) -> bool:
    return (0 <= budget < n and 1 <= q <= n and 1 <= r <= n
            and q + r > n + budget
            and q <= n - budget and r <= n - budget)
