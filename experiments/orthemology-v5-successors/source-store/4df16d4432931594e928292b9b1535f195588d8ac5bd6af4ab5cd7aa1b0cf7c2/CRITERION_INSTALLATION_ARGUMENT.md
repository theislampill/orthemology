# Installing the corrected governing criterion

## Additive result beyond the reviewed V2 packet

The original V2 guard repairs a derived document under a fixed exact-byte criterion. It does not install a new governing criterion. This extension supplies that distinct transition: a recipient's installed normalized-LF rule is replaced by the exact-byte rule under an install-specific grant, while the source, draft and unrelated state remain intact.

This completes a fully specified **retained-standard criterion repair** in the model. It remains a conditional research result, not a deployment in a real recipient's application, a general arbitrary-code updater, or an instance of full-basis radical correction.

## 1 The criterion has defined semantics

Rule identity is a constructor in a deliberately small language with two terms. NORMALIZED_LF compares candidate and source after stripping trailing LF bytes. EXACT compares their full byte sequences. The Python and Lean evaluators define these meanings directly. The command cannot supply arbitrary code merely labelled C1. The trusted evaluator and the representation of its terms are part of the operational premise.

For every finite source S, NORMALIZED_LF accepts S followed by one extra LF. That candidate differs from S, so the rule is defective under the retained exact-recovery standard. EXACT accepts precisely S. The Lean file `CriterionInstallation.lean` proves the generic appended-LF counterexample and the universal adequacy of EXACT.

Thus the replacement is identified by its whole acceptance condition, not selected because it happens to pass three samples. The samples separately show that the installed receiver actually changes its decisions under the intended interpreter. The proof and the interpreter must both retain their connection to the same source and exact-recovery task.

## 2 State and authority are separated by kind

The recipient state carries an installed rule, a rule version and a rule history. These are separate from the derived draft, its draft revision and the immutable Source. The state also carries the retained exact-recovery standard, current authorization epoch, active grant, revocation status, clock value and unrelated retained obligations.

The grant must authorize the named actor to perform `install-criterion` on the specified destination and source target during the current epoch and time interval. The command binds the expected current rule and rule version as well as the replacement term. A `replace-derived` grant does not authorize installing a rule. An install grant does not authorize editing draft bytes. The old V2 payload updater and the new installer enforce those distinct scopes.

These grant records are explicit model inputs. Their legitimate authority and accurate actor binding must be warranted outside the records themselves. A recipient's receipt of the new rule, or agreement that it is adequate, does not constitute a grant.

## 3 Exact transition and preservation theorem

Let I(s,c) be the conjunction of the retained-standard, target, recipient, expected-rule, expected-rule-version, epoch, new-rule, operation, current grant, revocation and time conditions described above. The installer is:

- If I(s,c), set the installed rule to EXACT, increase only the rule version by one, and append the prior rule to rule history.
- Otherwise return the entire state unchanged.

**Soundness.** The typed Lean guard accepts if and only if I(s,c). Every accepted operation therefore has a current install-specific model grant and installs a rule adequate for every candidate sequence relative to the retained target.

**Frame preservation.** On either branch, source, draft bytes, draft revision, retained standard, destination, authorization epoch, grant, revocation status, current time and unrelated state are unchanged. Success changes only the installed rule, rule version and rule history. This is proved by the record update, not inferred from equal output samples.

**Behavioral consequence.** If the old installed rule was NORMALIZED_LF and installation succeeds, it previously accepted S+LF; afterward it rejects S+LF and accepts S. For the actual canonical source, the separate wrong candidate obtained by changing its first byte to X remains rejected. These are measured decisions by the installed interpreter, not just a reported criterion ID.

**Separate restoration objective.** If the existing draft is S+LF, installation leaves that draft unchanged but now correctly rejects it. Criterion repair has succeeded; document repair has not yet occurred. A later draft repair requires its own current `replace-derived` grant. The test suite explicitly prevents the install grant from silently authorizing that second operation.

## 4 Recipients versions and copying

In the concrete fixture, A begins with the normalized rule at rule version 3, authorization epoch 2, a bad draft at draft revision 8, and a current A-specific install grant. Installation produces the exact rule at rule version 4 while the draft remains at revision 8. The source and old rule evidence are retained.

B can reuse the same rule definition and the same source-grounded adequacy proof, but it needs a B-specific install grant for its destination. Simply changing the actor field in A's command fails. A successful installation followed by replay of the old command also fails because the expected rule/version no longer matches. Byte-for-byte identity of the copied rule does not erase these recipient and version conditions.

The adequacy judgment and the permission judgment therefore transport differently. Under fixed source and standard, the same EXACT semantics can remain adequate for both recipients. Present authorization can fail after revocation or a version change while that semantic result remains true. The earlier cover-and-preserve theorem applies to the exact judgment being transported; it must not merge these two judgments.

## 5 Verification and its boundary

The original 25 tests remain unchanged. Nineteen new installation tests exercise actual before/after decisions, frame preservation, old-rule history, rule/draft permission separation, copied grants, fresh B grants, stale rule version, wrong expected rule, wrong replacement, wrong operation, changed retained standard, target/destination/epoch mismatch, current revocation, missing grant, expiry and replay. All 44 tests pass after the deliberate noninstalling baseline failed the five positive installation tests.

The typed Lean development proves the generic defect, exact criterion adequacy, contextual acceptance equivalence, frame preservation, actual changed decision behavior and the separation of data-repair from rule-install permission. No custom axioms or sorry placeholders are used. Some list-library proofs use Lean's standard logical axioms; the logs report these exactly rather than claiming that every new theorem is axiom-free.

A new shared 4,096-case binary fixture domain covers recipient, current rule, rule version, grant operation, revocation, requesting actor, expected rule, expected version, replacement rule, command operation, epoch mismatch and lease expiry. Its cross-language replay checks installation outcome, rule/version, preservation indicators, history length and the three actual decision results. The terminal comparison is recorded separately; finite agreement is not a universal Python-to-Lean refinement proof.

Actual source identity, present consent, trustworthy time, caller authentication, parser safety, concurrency, compiler correctness and non-bypassable execution remain outside this pure typed transition. The external dynamic-lane support and institutional-permission conditions remain necessary if its mechanism is imported. No new oracle or delayed-consent assumption is added here.

## 6 Foundational classification

The replacement is warranted by the retained exact-recovery standard, the fixed source and ordinary sequence reasoning. Current grants authorize installation; they do not make the criterion semantically adequate. The interpreter executes the rule; its success does not constitute the authority of the standard. Each role remains visible.

One precision to the retained primary-source comparison: Abadi et al. explicitly leave timestamp/lifetime freshness outside their formal logic. This report imports no theorem that their access-control calculus itself establishes those live checks.

The new transition therefore strengthens the operational realization of question 4 without strengthening its foundational conclusion. Necessary-source N2, productive completion P1, particular bearer P2, essential truthful attestation T0, Wisdom and metaphysical unity are still unused. The five Candidate E replies remain distinct as assessed in the V2 cold review. The full basis was not defeated, and no R5 defeat or canonical Candidate E adoption follows.
