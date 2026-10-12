"""Pure, fail-closed projection of explicitly reviewed JSON locator fields.

Public API: project_metadata(original: bytes, specification: bytes,
                            approved_fields: bytes) -> tuple[bytes, dict]
All inputs are strict UTF-8 JSON bytes. Raises ProjectionError (a ValueError)
on invalid input. Performs no filesystem, network, source execution or mutation.

The specification is a closed object:
  {"schema":"t20-metadata-projection-spec-v1", "source_sha256":HEX,
   "replacements":[{"pointer":"/source_path", "role":"source_locator",
     "old_value":ANY_JSON, "new_value":SAFE_REFERENCE_OR_IDENTITY_RECORD,
     "resolved_identity":{"sha256":HEX, "disposition":"included"}}]}
The separate approval is a closed object:
  {"schema":"t20-metadata-field-approval-v1", "source_sha256":HEX,
   "fields":[{"pointer":"/source_path", "role":"source_locator",
     "output_form":"relative_reference", "decision_reference":"review-id"}]}
Every field is required; unknown fields and unmatched pointer sets fail closed.
Roles are the finite LOCATOR_ROLES below. All pointers are exact RFC 6901 string
pointers; no root replacement, wildcards, URI fragments, or array-index aliases.

Relative references are either authored_objects/<first-two-hex>/<identity-hash>
or views/<namespace>/<path>. A view's identity binding must be reviewed outside
this helper; this function never resolves files. An identity_record is exactly
{"kind":"excluded"|"unresolved", "sha256":HEX, "replay_blocked":true}; its
kind/digest must match resolved_identity. Only an approval with output_form
identity_record allows this structured replacement. These are identity-only
blockers, not delivered dependencies. An unresolved identity still needs a
known SHA-256; sources with unknown byte identity cannot use this helper.

The caller must independently establish source eligibility, exact dependency
resolution, completeness of locator enumeration, field-role correctness, and
approval of the exact specification/approval bytes. Their names are not proof
of authorization. This is not a redaction/discovery tool and cannot certify that
unselected text is distributable. In particular, it leaves free prose alone.

Serialization is deterministic UTF-8, sorted keys, compact separators, and one
final newline. Numbers are parsed losslessly (int/Decimal). No arithmetic or
Unicode normalization is applied to source values. Unselected parsed values,
including types and Decimal tuples, are verified after output reparse. Byte
formatting/order may change. This must never be applied to consumed scientific
fixtures whose exact original bytes are required.

The public receipt binds SHA-256 of all three exact input byte strings and the
projected output; each row includes the pointer, role, original-value digest,
new value, resolved identity and permitted-field decision. Original-value
hashing uses the same canonical serialization WITHOUT a trailing newline.
Original values are absent from the receipt, but the specification is private
and must be retained by the caller for internal resolution. Pointers themselves
must be reviewed as public metadata; guards reject obvious private locators,
not every possible sensitive string. No publication or package assembly occurs.
"""
from __future__ import annotations

import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
import re
import unicodedata

SPEC_SCHEMA = 't20-metadata-projection-spec-v1'
APPROVAL_SCHEMA = 't20-metadata-field-approval-v1'
RECEIPT_SCHEMA = 't20-metadata-projection-receipt-v1'
LOCATOR_ROLES = frozenset({
    'source_locator', 'dependency_locator', 'packet_locator', 'report_locator',
    'correction_locator', 'scope_locator', 'navigation_locator',
})
_HASH = re.compile(r'[0-9a-f]{64}\Z')
_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}\Z')
_INDEX = re.compile(r'(?:0|[1-9][0-9]*)\Z')
_PRIVATE = re.compile(
    r'libfile_|Sentinel_|file_[0-9a-fA-F]{32}|/(?:workspace|mnt/data|home|Users)/'
    r'|[?&](?:sig|token|X-Amz-[^=]*)=|-----BEGIN .*PRIVATE KEY', re.I)
_RESERVED = {'con', 'prn', 'aux', 'nul',
             *('com' + str(i) for i in range(1, 10)),
             *('lpt' + str(i) for i in range(1, 10)),
             *('com' + i for i in '¹²³'), *('lpt' + i for i in '¹²³')}


class ProjectionError(ValueError):
    """A projection failed validation; no output has been returned."""


def _require(condition, message):
    if not condition:
        raise ProjectionError(message)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _hash(value):
    _require(type(value) is str and _HASH.fullmatch(value) is not None,
             'invalid SHA-256')
    return value


def _keys(value, expected):
    _require(type(value) is dict and set(value) == set(expected),
             'missing, unexpected, or malformed manifest fields')


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def _reject_constant(_value):
    raise ProjectionError('nonfinite JSON constant')


def _valid_strings(value):
    if type(value) is str:
        _require(not any(0xD800 <= ord(c) <= 0xDFFF for c in value),
                 'unpaired Unicode surrogate')
    elif type(value) is dict:
        for key, child in value.items():
            _valid_strings(key)
            _valid_strings(child)
    elif type(value) is list:
        for child in value:
            _valid_strings(child)
    elif type(value) is Decimal:
        _require(value.is_finite(), 'nonfinite JSON number')


def _parse(data):
    _require(type(data) is bytes, 'all inputs must be bytes')
    value = json.loads(data.decode('utf-8'), object_pairs_hook=_unique_pairs,
                       parse_float=Decimal, parse_constant=_reject_constant)
    _valid_strings(value)
    return value


def _canonical(value):
    """Exact typed-JSON canonicalization, without a final newline."""
    if value is None:
        return 'null'
    if type(value) is bool:
        return 'true' if value else 'false'
    if type(value) is int:
        return str(value)
    if type(value) is Decimal:
        _require(value.is_finite(), 'nonfinite JSON number')
        number = str(value)
        # Preserve Decimal type and its exponent for integral decimal tokens.
        return number if '.' in number or 'E' in number else number + 'e0'
    if type(value) is str:
        return json.dumps(value, ensure_ascii=False)
    if type(value) is list:
        return '[' + ','.join(_canonical(child) for child in value) + ']'
    if type(value) is dict:
        return '{' + ','.join(_canonical(key) + ':' + _canonical(value[key])
                              for key in sorted(value)) + '}'
    raise ProjectionError('unexpected parsed JSON type')


def _same(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(_same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    if type(left) is Decimal:
        return left.as_tuple() == right.as_tuple()
    return left == right


def _public_text(value):
    _require(type(value) is str and not _PRIVATE.search(value), 'private public-metadata token')
    _require(not any(unicodedata.category(c).startswith('C') for c in value),
             'control character in public metadata')
    return value


def _decision(value):
    _public_text(value)
    _require(_ID.fullmatch(value) is not None, 'unsafe decision reference')


def _pointer(value):
    _public_text(value)
    _require(value.startswith('/'), 'non-root JSON Pointer required')
    tokens = []
    for encoded in value[1:].split('/'):
        _require(re.search(r'~(?:[^01]|$)', encoded) is None, 'invalid JSON Pointer escape')
        decoded = encoded.replace('~1', '/').replace('~0', '~')
        _public_text(decoded)
        tokens.append(decoded)
    return tuple(tokens)


def _locate(document, tokens):
    current = document
    parent = None
    key = None
    for token in tokens:
        parent = current
        if type(current) is dict:
            _require(token in current, 'missing JSON Pointer')
            key = token
        elif type(current) is list:
            _require(_INDEX.fullmatch(token) is not None, 'explicit canonical array index required')
            key = int(token)
            _require(key < len(current), 'missing JSON Pointer')
        else:
            raise ProjectionError('JSON Pointer crosses a scalar')
        current = current[key]
    return parent, key, current


def _relative(value, identity):
    _public_text(value)
    _require(bool(value) and unicodedata.normalize('NFC', value) == value,
             'empty or noncanonical relative reference')
    _require(not any(c in value for c in '\\:%#<>|?*"'), 'unsafe reference character')
    components = value.split('/')
    _require(all(p not in ('', '.', '..') for p in components), 'unsafe reference component')
    for component in components:
        _require(not component.endswith((' ', '.')), 'ambiguous reference component')
        _require(component.split('.')[0].casefold() not in _RESERVED,
                 'reserved reference component')
    if components[0] == 'authored_objects':
        _require(components == ['authored_objects', identity[:2], identity],
                 'CAS reference does not match resolved identity')
    else:
        _require(components[0] == 'views' and len(components) >= 3,
                 'approved CAS or namespaced view reference required')


def _validate_replacement(row, field):
    _require(row['role'] == field['role'], 'unapproved locator role')
    identity = row['resolved_identity']
    _keys(identity, {'sha256', 'disposition'})
    digest = _hash(identity['sha256'])
    disposition = identity['disposition']
    _require(type(disposition) is str and disposition in {'included', 'excluded', 'unresolved'},
             'invalid identity disposition')
    new = row['new_value']
    if field['output_form'] == 'relative_reference':
        _require(disposition == 'included', 'reference requires included identity')
        _relative(new, digest)
    else:
        _require(disposition in {'excluded', 'unresolved'}, 'identity-only disposition required')
        _keys(new, {'kind', 'sha256', 'replay_blocked'})
        _require(new['kind'] == disposition and _hash(new['sha256']) == digest,
                 'identity record does not match resolved identity')
        _require(new['replay_blocked'] is True, 'identity-only dependency must remain blocked')


def _unchanged_outside(original, projected, selected, path=()):
    if path in selected:
        return
    _require(type(original) is type(projected), 'unselected JSON type changed')
    if type(original) is dict:
        _require(original.keys() == projected.keys(), 'unselected object fields changed')
        for key in original:
            _unchanged_outside(original[key], projected[key], selected, path + (key,))
    elif type(original) is list:
        _require(len(original) == len(projected), 'unselected array length changed')
        for index, (before, after) in enumerate(zip(original, projected)):
            _unchanged_outside(before, after, selected, path + (str(index),))
    else:
        _require(_same(original, projected), 'unselected JSON value changed')


def _project(original, specification, approved_fields):
    document = _parse(original)
    spec = _parse(specification)
    approval = _parse(approved_fields)
    _keys(spec, {'schema', 'source_sha256', 'replacements'})
    _keys(approval, {'schema', 'source_sha256', 'fields'})
    _require(spec['schema'] == SPEC_SCHEMA and approval['schema'] == APPROVAL_SCHEMA,
             'unknown projection or approval schema')
    source_digest = _sha(original)
    _require(_hash(spec['source_sha256']) == source_digest and
             _hash(approval['source_sha256']) == source_digest, 'source digest mismatch')
    _require(type(spec['replacements']) is list and bool(spec['replacements']),
             'explicit nonempty replacements required')
    _require(type(approval['fields']) is list and bool(approval['fields']),
             'explicit nonempty field approval required')
    permitted = {}
    for field in approval['fields']:
        _keys(field, {'pointer', 'role', 'output_form', 'decision_reference'})
        tokens = _pointer(field['pointer'])
        _require(tokens not in permitted, 'duplicate approved pointer')
        _require(type(field['role']) is str and field['role'] in LOCATOR_ROLES,
                 'unapproved locator role')
        _require(type(field['output_form']) is str and
                 field['output_form'] in {'relative_reference', 'identity_record'},
                 'unknown replacement form')
        _decision(field['decision_reference'])
        permitted[tokens] = field
    replacements = {}
    for row in spec['replacements']:
        _keys(row, {'pointer', 'role', 'old_value', 'new_value', 'resolved_identity'})
        tokens = _pointer(row['pointer'])
        _require(tokens not in replacements, 'duplicate replacement pointer')
        _require(tokens in permitted, 'unapproved locator field')
        for other in replacements:
            common = min(len(tokens), len(other))
            _require(tokens[:common] != other[:common], 'overlapping replacement pointers')
        _validate_replacement(row, permitted[tokens])
        _, _, old = _locate(document, tokens)
        _require(_same(old, row['old_value']), 'stale original JSON value')
        replacements[tokens] = row
    _require(replacements.keys() == permitted.keys(), 'approved pointer omitted from replacements')

    projected_document = copy.deepcopy(document)
    receipt_rows = []
    for tokens, row in sorted(replacements.items()):
        parent, key, old = _locate(projected_document, tokens)
        parent[key] = copy.deepcopy(row['new_value'])
        field = permitted[tokens]
        receipt_rows.append({
            'pointer': row['pointer'], 'role': row['role'],
            'original_value_sha256': _sha(_canonical(old).encode('utf-8')),
            'resolved_identity': copy.deepcopy(row['resolved_identity']),
            'new_value': copy.deepcopy(row['new_value']),
            'permitted_field_decision': {
                'decision_reference': field['decision_reference'],
                'output_form': field['output_form'],
            },
        })
    projected = (_canonical(projected_document) + '\n').encode('utf-8')
    reparsed = _parse(projected)
    _unchanged_outside(document, reparsed, replacements)
    for tokens, row in replacements.items():
        _require(_same(_locate(reparsed, tokens)[2], row['new_value']),
                 'replacement value changed during serialization')
    receipt = {
        'schema': RECEIPT_SCHEMA, 'source_sha256': source_digest,
        'projected_sha256': _sha(projected),
        'specification_sha256': _sha(specification),
        'approved_fields_sha256': _sha(approved_fields),
        'unselected_values_verified': True, 'replacements': receipt_rows,
    }
    return projected, receipt


def project_metadata(original: bytes, specification: bytes,
                     approved_fields: bytes) -> tuple[bytes, dict]:
    """Apply an exact reviewed projection, or raise ProjectionError atomically."""
    try:
        return _project(original, specification, approved_fields)
    except ProjectionError:
        raise
    except (ValueError, TypeError, UnicodeError, RecursionError, OverflowError,
            InvalidOperation) as error:
        # Do not echo parser messages or original values into public diagnostics.
        raise ProjectionError('malformed or unsupported JSON projection input') from None
