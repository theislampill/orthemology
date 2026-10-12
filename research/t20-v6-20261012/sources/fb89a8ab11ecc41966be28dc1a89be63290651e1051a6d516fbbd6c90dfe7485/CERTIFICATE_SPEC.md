# Certificate contract: scoped two-criterion research prototype

## Data envelope

`gap-envelope.schema.json` describes an envelope with exactly four fields: `base`, `regime`, `target`, `certificate`. JSON Schema validates its closed structural types. The semantic verifier additionally checks exact rational limits, positivity, profile references, base identity, bounded target syntax, coverage and complete certificate readback. Schema success alone is insufficient.

The base uses `profile-base-v1`, a positive integer version, 1–256 named two-coordinate profiles, two declared coordinate kinds and up to 64 extraction-assumption records. A kind is DESCRIPTIVE, NORMATIVE, MIXED or LOGICAL. An evaluated/mixed coordinate requires disclosed extraction assumptions. This is a disclosure rule, not automatic semantic validation of the kinds. Both the coordinate names/meaning and calibration should be supplied in an owner's external source record; the prototype does not parse natural language meaning.

The regime uses `two-criterion-weight-interval-v1`, an ID (1–128 characters)/version, a hash binding it to the base, exact rational lower/upper endpoints, signed coordinate orientation, an explicit nonempty admissibility-assumption list and authority status `SUPPLIED_NOT_CERTIFIED`. Each endpoint must lie strictly inside (0,1). A reversed interval is permitted as an empty-class test and returns `NO_ADMISSIBLE_EXTENSION`. Equal endpoints represent a singleton. Assumptions may include normative/mixed assertions and retain their declared kinds.

Target AST: `gt` or `ge` compares named profiles; `const` contains a Boolean; `not` contains one child; `and`/`or` contain 1–16 children. Total nodes ≤256 and nesting depth ≤16. Integers or rational strings are exact inputs; Booleans and floats cannot masquerade as profile numbers. Rational syntax has a 128-character bound and numerator/denominator have 128-bit bounds. Unknown fields or operations are invalid. This is not an arbitrary expression evaluator.

## Verdict and evidence

- INVALID: no conclusion; malformed, stale or unsupported input. This is not a gap witness.
- NO_ADMISSIBLE_EXTENSION: no models under this interval regime, not a certificate of contradiction in the world or of both competing judgments.
- DISAGREEMENT: an exact rational α where the target is true and one where it is false, with full recomputed coverage.
- INVARIANT_TRUE / INVARIANT_FALSE: every admissible α has the designated value. These require a nonempty class.

The certificate includes schema version, base/regime/target hashes, verdict, checked-cell count, witnesses, proof rule `AFFINE_ATOM_SIGN_PARTITION_V1`, relative scope and declared-partition information. The input envelope carries the actual bridge ID/version, extraction and admissibility assumptions, and target. A certificate without its complete bound inputs cannot be verified.

Canonical content hashes are SHA-256 of Python-compatible JSON serialization with sorted keys and compact separators, default ASCII escaping and no added newline. This is an explicitly local encoding convention, not a claim of RFC 8785 compliance or cryptographic signature. The certificate checker compares complete typed JSON encodings after recomputation; it does not use Python's Boolean/integer-coercive dictionary equality. A test-first review caught and fixed that equality hazard.

## Trusted and untrusted components

Trusted for this prototype: Python's arithmetic/Fraction/JSON implementation, this checker implementation and its source identity, the ordinary sign-cell proof, and the supplied interpretation of its closed grammar. We did not compile a Lean proof or implement a separately verified arithmetic kernel. An independent exact linear-feasibility oracle provides test evidence but not a replacement for the proof.

Not certified: factual measurement accuracy, honest source provenance, complete extraction, descriptive/normative partition correctness, adequacy of linear aggregation, correctness or completeness of the admissibility class, substantive preference authority, philosophical possibility of an expansion, policy legitimacy, fairness, truth, adoption, or publication readiness.

## Transport and revision

Any content change to the base, regime or target requires rebuilding and rechecking. A changed base version invalidates the old regime binding. An equivalent presentation can be transported only with an explicit equivalence argument. Under positive coordinate rescaling e'_j=c_j e_j, equivalent weights are w'_j proportional to w_j/c_j; retaining the same numerical weights usually changes the evaluation. Arbitrary monotone coordinate transformations do not generally preserve linear expected-payoff structure. P14's exact transformation limits remain in force.

## Reproduction

Run in this directory:

`python -m unittest -v`

`python research_probes.py`

`python -c "import json,jsonschema; jsonschema.validate(json.load(open('example_certificate.json')),json.load(open('gap-envelope.schema.json')))"`

The example is not a normative recommendation. It discloses disagreement for crossing profiles under the supplied interval. The prototype is not exposed as a network service and has not undergone production security or performance qualification.
