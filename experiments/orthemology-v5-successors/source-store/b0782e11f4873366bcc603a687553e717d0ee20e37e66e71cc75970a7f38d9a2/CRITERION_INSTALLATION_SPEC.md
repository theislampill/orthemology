# Explicit governing criterion installation

## Purpose and relation to the frozen V2 packet

The V2 payload model accurately verifies repair of a derived source copy under a fixed exact criterion. It does not change an installed criterion. This additive experiment directly models the C0-to-C1 rule installation that question 4 asks about. It uses the same canonical source and retained exact-recovery standard. V2 remains unchanged; this is a separately testable extension within the parent's approved research scope.

## Typed rule language

There are exactly two rule terms:

- `NORMALIZED_LF`: accept when trailing-LF normalization of candidate and source yields equal byte strings.
- `EXACT`: accept when candidate and source are byte-identical.

These constructors have an explicit local interpretation. They are not names for arbitrary uploaded code. The model does not accept plugins, executable strings, function pointers supplied by a sender, or an unverified implementation carrying the name C1. Rule identity is identity of a term in this two-constructor language, interpreted by the specified evaluator. The trusted interpreter remains part of the mechanism support.

## State and command

A state contains the immutable Source, destination, retained standard `exact-source-recovery`, derived draft and its revision, installed rule and its separate rule version, authorization epoch, active grant, revocation state, current time, prior rule history, and unrelated retained state.

An installation command binds actor, destination, source target, expected current rule, expected rule version, authorization epoch, new rule, operation, observation time and lease end. A valid install requires new rule EXACT and the retained exact-recovery standard. It also requires the current active grant to authorize this actor, destination, target and epoch specifically for `install-criterion` during the valid interval, with no current revocation.

On success, only the installed rule, rule version and rule history change. The prior rule is appended to history. Source, draft bytes, draft revision, retained standard, grant state and unrelated state remain unchanged. On rejection, the entire state remains unchanged.

## Permission separation

The operation `install-criterion` does not authorize `replace-derived`, and `replace-derived` does not authorize installation. A recipient can possess the copied rule term and the adequacy proof while lacking either grant. If subsequent draft repair is needed, it needs its own current scoped permission. Successful criterion repair may therefore expose an existing bad draft without yet changing it.

## Required evidence and tests

1. Before installation, the exact source is accepted, source-plus-LF is wrongly accepted under the retained exact standard, and a non-target mutation is rejected.
2. After installation, exact source remains accepted, source-plus-LF is rejected, and the other non-target mutation remains rejected. This demonstrates changed decision behavior, not only changed version metadata.
3. The exact criterion is adequate for every finite candidate sequence. Trailing-LF normalization accepts source-plus-LF for every finite source; the added LF makes a different sequence.
4. Stale rule version, wrong expected rule, copied recipient grant, missing/revoked/expired grant, wrong target, changed retained standard or wrong operation all reject without alteration.
5. A fresh B-specific installation grant permits B to reuse the same criterion proof without manufacturing a new source root.
6. The typed Lean installation model proves context-validity and preservation; bounded Python and Lean tests are verification of that declared model, not a deployment/authentication claim.

The full authority basis retains the target, exact-recovery standard, inferential resources, grants and custody obligations. This remains retained-standard repair and does not create a full-basis radicality instance.
