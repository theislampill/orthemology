# Total-explainer uniqueness: the membership discriminator

## Result

**Yes, conditionally.** With reflexive and antisymmetric fact-parthood, exact source-side partial explanation, member projection, and No Extended Circles, two full explainers of a common target are identical **if both explainers belong to that target**. Consequently an all-actual-facts target has at most one full explanatory fact; unrestricted plural PSR plus a nonempty actual-fact domain supplies existence.

The uniqueness proof does **not** need either transitivity clause, global PSR, the previous proper-part-collapse lemma, or totality over the entire fact universe. The exact local membership premises are `F(q)` and `F(r)`. More generally, different targets suffice when each target contains the other target's explainer.

The same explanatory principles, even with unrestricted plural PSR, both transitivity clauses, and the full displayed distribution principle retained, **permit distinct full explainers of a narrower fixed target which excludes those explainers**. The kernel-checked four-fact control below verifies that distinction.

This is a source-relative conditional consequence and a transport discriminator. It is not a metaphysical realization, proof of a unique original bearer, or transfer of generic explanation into productive creation.

## Source and prior-work credit

The source is Robert C. Koons and Alexander R. Pruss, *Skepticism and the principle of sufficient reason* (2020), [publisher DOI](https://doi.org/10.1007/s11098-020-01482-3), [author-hosted paper](https://robkoons.net/uploads/1/3/5/2/135276253/koons-pruss2020_article_skepticismandtheprincipleofsuf.pdf).

The local continuous source capture is `epistemic-psr-warrant/sources/koons-pruss2020-web-continuous.txt`. Its retained source-line labels locate:

- L50–63: unrestricted plural PSR, all-actual-facts totality, and full/proper-part self-explanation.
- L88–97: source-side partial explanation, No Extended Circles, and both transitivity clauses.
- L98–119: the stated existence theorem for wholly self-explanatory facts.
- L122–139: restricted noncircular PSR and distribution to members and their parts.
- L64–67 and L162–175: the later application relies on a restricted natural-fact field; unrestricted all-facts comprehension is not to be silently substituted for that field.

The relevant source argument and the complete local text were checked for an explicit uniqueness result; none was found. The existing `DependencyAudit.lean` proves self-explanation under a weaker package, and `BridgeRepairs.lean` proves partlessness under a stronger package. Neither contains this explicit uniqueness statement. This bounded search is not a literature-priority claim: credit the source principles and the earlier audits, and describe the present result as an explicit checked corollary. The earlier audits' cautions about uniqueness under their weaker package remain valid.

Reflexivity and antisymmetry of fact-parthood are explicit additional background assumptions in the theorem. They should not be erased merely because they are standard for inclusive parthood.

## Unbounded theorem and proof

Write `P(x,{y})` for partial singleton explanation, and `x ≤ y` for fact-parthood. No Extended Circles says:

`P(x,S) ∧ y∈S ∧ y≠x ∧ ¬(y≤x) → ¬P(y,{x})`.

First prove the smaller lemma: **mutual partial singleton explanation implies equality**.

1. Assume `P(q,{r})` and `P(r,{q})`, but `q≠r`.
2. Apply No Extended Circles with source `r` and target member `q`. Since the return explanation exists, `q≤r` must hold.
3. Antisymmetry and `q≠r` then exclude `r≤q`.
4. Apply No Extended Circles with source `q` and target member `r`. The existing return explanation is forbidden, a contradiction.

This lemma does not need a source-side definition of `P`, reflexivity, projection, totality, or transitivity. It needs just the displayed circle restriction and antisymmetry of parthood.

For the source's `PE(x,S) := ∃z, x≤z ∧ E(z,S)`, reflexivity makes every full explanation a partial explanation. If `E(q,F)`, `E(r,F)`, `q∈F`, and `r∈F`, member projection supplies `E(q,{r})` and `E(r,{q})`; the lemma yields `q=r`.

The stronger cross-target version assumes `E(q,F)`, `E(r,G)`, `r∈F`, and `q∈G`. It does not require either source to belong to its own target. For the common-target corollary both displayed memberships are retained explicitly. No claim of globally weakest axioms or independence of every individual premise is made.

For existence and uniqueness over all actual facts, let `F(x)` be `True`. Nonemptiness and one instance of unrestricted plural PSR produce a full explainer. Every candidate is a member, so the uniqueness theorem applies. `Fact : Type u` is arbitrary: this proof has no finite-domain bound.

### Checked declarations

`Uniqueness.lean` contains:

- `mutual_partial_singletons_equal`
- `cross_target_explainers_equal`
- `member_inclusive_target_unique`
- `unrestricted_psr_unique_total`

The existence conclusion is written explicitly as `∃q, E(q,F) ∧ ∀r, E(r,F) → r=q`.

## Exact finite relational control

The fact domain is exactly `{q,a,b,e}`. Pluralities are **all predicates on this domain**, so all 15 nonempty subsets are admitted; the proof does not replace them with a selected family.

- `Part(x,y)` means `x=y`.
- `E(q,S)` holds for every nonempty `S`.
- `E(a,S)` and `E(b,S)` hold exactly when `S={e}`.
- `e` fully explains nothing.
- Empty pluralities have no full explanation.
- Partial explanation is defined by the exact existential source-side closure. Because parthood is equality, `PE(x,S) ↔ E(x,S)`.

`FiniteControl.lean` proves, over arbitrary predicate pluralities:

1. Reflexive, transitive, antisymmetric parthood.
2. Exact partial/full equivalence, full-to-partial inclusion, and partial source closure.
3. Unrestricted plural PSR for every nonempty plurality.
4. Both complete and partial transitivity clauses.
5. Distribution to every member and every part of a member, matching the displayed source principle.
6. No Extended Circles.
7. `q` is the unique explainer of all four facts.
8. `a≠b`, both fully explain `{e}`, and neither belongs to `{e}`.
9. Both are also external to the narrow target by parthood and explain every nonempty plurality restricted to the class `{e}`.
10. The full explainers of `{e}` are **exactly `q,a,b`**. Thus the control establishes at least two distinct local explainers, not exactly two in total.

Why the axioms hold: any chain beginning at `q` stays within `q`'s unrestricted explanatory range. The only target of `a` or `b` is `e`, which has no outgoing explanation, so those chains cannot create a missing transitive edge. Projection preserves the allowed singleton target. A reverse explanation into `q`, `a`, or `b` cannot complete a distinct two-way explanatory pair. No Extended Circles is also checked directly rather than inferred only from these remarks.

The control does not posit a fusion fact for every plurality. Equality parthood on four distinct facts does not have such fusions. The requested explanatory package did not include a fusion axiom; the control makes no claim about a stronger mereological or metaphysical package.

## What this discriminates, and what it does not

An all-facts explanation includes facts representing the proposed explainers themselves. A target described only as the complete created field can omit those candidates. The step from two explanations of that narrower field to reciprocal explanation therefore needs an additional bridge. The control isolates exactly this failure while retaining the explanatory principles.

Uniqueness here is identity of the **explanatory fact**. A unique fact may refer to multiple beings, or distinct bearers may be represented by one explanatory fact. No injective bearer-to-fact representation, bearer-identity theorem, or unique-agent conclusion has been supplied.

Nothing identifies the stipulated generic `E` with productive origination, entire creation, or an independently warranted causal relation. The relational control is evidence of non-entailment for the displayed formal package, not evidence that a multi-original metaphysical world is possible. Conversely, the conditional positive theorem does not establish that its all-facts target, projection, parthood, and circle principles are sound or available at the retained created-order interface.

## Verification

Both new Lean files were checked using the already installed Lean 4.19.0 toolchain. No installation, older-audit rerun, protected repository change, external integration, or closure action was performed. Prior source files are checksum-verified unchanged.

The complete new-file verification is `bash total-explainer-uniqueness/verify.sh`. It checks both files afresh, rejects unfinished proof placeholders, and checks the two prior-file hashes. The final logs are `uniqueness-check.log` and `control-check.log`. Axiom output contains only Lean's standard foundational axioms (`propext`, `Classical.choice`, `Quot.sound`) where applicable; there are no added theorem axioms or unfinished proof axioms. Initial statement-only failures are retained separately as red-test logs.
