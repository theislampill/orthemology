"""P03 attempt2 proposal: owned transport values, not an atomic caller snapshot.

No canonical source is replaced. Stable native trees are preserved modulo JSON
normalisation. Concurrent native mutation may produce a bounded read transcript
or a refusal; a single-instant snapshot requires caller cooperation. Resource or
host failures are not logical refutations and no exception is forged into proof.
"""
from __future__ import annotations
from typing import Any
import boundaries as b
import proof_export

def snapshot_native(value: Any) -> Any:
    """Copy exact builtins without invoking user-defined iteration/conversion.

    Dicts are fresh private dicts and sequence nodes become fresh tuples. Leaves
    are immutable exact builtins. Shared input subtrees are copied separately.
    MemoryError and asynchronous BaseException deliberately propagate.
    """
    active: set[int] = set()
    remaining = b.MAX_NODES
    def visit(x: Any, depth: int) -> Any:
        nonlocal remaining
        remaining -= 1
        if remaining < 0 or depth > b.MAX_DEPTH:
            raise b.Rejection('resource: owned snapshot structural budget')
        typ = type(x)
        if typ in (list, tuple, dict):
            if id(x) in active:
                raise b.Rejection('encoding: cyclic object')
            if len(x) > b.MAX_NODES:
                raise b.Rejection('resource: owned snapshot container length')
            active.add(id(x))
            try:
                if typ is dict:
                    out = {}
                    for key, item in dict.items(x):
                        if type(key) is not str:
                            raise b.Rejection('encoding: nontext key')
                        copied_key = visit(key, depth + 1)
                        out[copied_key] = visit(item, depth + 1)
                    return out
                # Fixed length bounds even a caller continually growing the list.
                length = len(x)
                get = list.__getitem__ if typ is list else tuple.__getitem__
                return tuple(visit(get(x, i), depth + 1) for i in range(length))
            finally:
                active.remove(id(x))
        if typ is int:
            if x.bit_length() > b.MAX_INT_BITS:
                raise b.Rejection('resource: integer bits')
            return x
        if typ is str:
            if len(x) > 4096:
                raise b.Rejection('resource: string size')
            if any(0xD800 <= ord(c) <= 0xDFFF for c in x):
                raise b.Rejection('encoding: unpaired surrogate')
            return x
        if typ in (bool, type(None)):
            return x
        raise b.Rejection('encoding: unsupported object')
    try:
        copied = visit(value, 0)
    except RecursionError as ex:
        raise b.Rejection('resource: owned snapshot host recursion') from ex
    except (IndexError, RuntimeError) as ex:
        # Exact builtin containers only: these are unstable traversal refusals.
        raise b.Rejection('encoding: native container changed during capture') from ex
    b.bound_tree(copied)
    return copied

def encode_owned(value: Any) -> bytes:
    """Successful return is in the existing strict decoder's domain."""
    copied = snapshot_native(value)
    raw = b.dump_json(copied)
    b.load_json(raw)  # Explicit postcondition; no limit or semantic guard is relaxed.
    return raw

def owned_json(value: Any) -> Any:
    return b.load_json(encode_owned(value))

def export_module_owned(examples: Any) -> str:
    """Bounded native adapter: exact list/tuple rows, immutable name/bytes leaves.

    The stricter row domain is a proposal. No legacy arbitrary-iterator contract
    is erased or claimed equivalent. Generated text is still not kernel proof.
    """
    if type(examples) not in (list, tuple):
        raise b.Rejection('export: example count')
    count = len(examples)
    if not 1 <= count <= 16:
        raise b.Rejection('export: example count')
    get_outer = list.__getitem__ if type(examples) is list else tuple.__getitem__
    rows = []
    try:
        for i in range(count):
            row = get_outer(examples, i)
            if type(row) not in (list, tuple) or len(row) != 2:
                raise b.Rejection('export: name/bytes pair required')
            get_row = list.__getitem__ if type(row) is list else tuple.__getitem__
            name, raw = get_row(row, 0), get_row(row, 1)
            if type(name) is not str or type(raw) is not bytes:
                raise b.Rejection('export: immutable name/bytes pair required')
            rows.append((name, raw))
    except IndexError as ex:
        raise b.Rejection('export: native row changed during capture') from ex
    return proof_export.module(rows)
