"""P03 attempt2 proposal: private copy-on-write Engine transactions.

This is a separate adapter over the exact attempt1 Engine; not adoption, crash
persistence, distributed serialisability, or verification of CPython. The host
contract requires an all-or-none reference store and no private-state mutation.
Precommit exceptions cannot expose partial writes. Cancellation/response loss
AFTER publication is an indeterminate committed/pending call, not rollback.
"""
from __future__ import annotations
from threading import RLock
from typing import Any
import operational as op
from safe_frontend import encode_owned, owned_json, snapshot_native

class AtomicEngine:
    def __init__(self, *, standard: bool = False) -> None:
        self._guard = RLock()
        self._active = False
        self._engine = op.Engine.standard() if standard else op.Engine()
        self._engine._lock = self._guard

    @classmethod
    def standard(cls) -> AtomicEngine:
        return cls(standard=True)

    def _fork(self) -> op.Engine:
        original = self._engine
        private = object.__new__(op.Engine)
        private._lock = self._guard
        private._issuer = original._issuer
        # Every reachable value below these maps is immutable in the bound
        # Engine implementation. The maps, and only the maps, are mutable.
        private._rules = original._rules.copy()
        private._observations = original._observations.copy()
        private._issued = original._issued.copy()
        private._prob_observations = original._prob_observations.copy()
        private._prob_requirements = original._prob_requirements.copy()
        private._epoch = original._epoch
        return private

    def _call(self, method: str, *args: Any, **kwargs: Any) -> Any:
        with self._guard:
            # Nested *base* calls use the same RLock and private Engine. A new
            # public transaction must not fork the still-committed old state
            # from a signal/finalizer/reentrant host callback.
            if self._active:
                raise op.Rejection('transaction: public reentrancy refused')
            try:
                self._active = True
                private = self._fork()
                result = getattr(private, method)(*args, **kwargs)
                # COMMIT: the only publication of provisional registry state.
                self._engine = private
                return result
            finally:
                self._active = False

    def revise_rule(self, key: Any, allowed: Any) -> None:
        return self._call('revise_rule', key, allowed)

    def set_observation(self, name: Any, values: Any) -> None:
        # No borrowed container remains when the state transaction starts.
        return self._call('set_observation', name, snapshot_native(values))

    def remove_observation(self, name: Any) -> None:
        return self._call('remove_observation', name)

    def set_probability_observation(self, name: Any, spec: Any) -> None:
        return self._call('set_probability_observation', name, owned_json(spec))

    def refine_probability_observation(self, name: Any, spec: Any) -> dict:
        return self._call('refine_probability_observation', name, owned_json(spec))

    def coarsen_probability_observation(self, name: Any, spec: Any) -> dict:
        return self._call('coarsen_probability_observation', name, owned_json(spec))

    def require_probability(self, rule: Any, observation: Any, epsilon: Any) -> None:
        return self._call('require_probability', rule, observation, snapshot_native(epsilon))

    def remove_probability_requirement(self, rule: Any) -> None:
        return self._call('remove_probability_requirement', rule)

    def admit(self, candidate: Any) -> op.Licence:
        return self._call('admit_json', encode_owned(candidate))

    def admit_json(self, raw: bytes) -> op.Licence:
        return self._call('admit_json', raw)

    def revalidate(self, licence: op.Licence) -> op.Licence:
        return self._call('revalidate', licence)

    def describe(self, licence: op.Licence) -> dict:
        return self._call('describe', licence)

    def dispatch(self, licence: op.Licence, value: Any) -> Any:
        return self._call('dispatch', licence, owned_json(value))

    def project(self, *, limit: int = 128, offset: int = 0) -> list:
        return self._call('project', limit=limit, offset=offset)
