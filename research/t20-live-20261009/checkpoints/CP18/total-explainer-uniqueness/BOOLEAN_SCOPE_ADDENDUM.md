# Addendum: local nonuniqueness with supplemented fusion mereology

## Strengthened result

The local-nonuniqueness control does not depend on omitting fusions or making parthood equality. `BooleanControl.lean` verifies the same separation with all nonempty fusions, strong supplementation, and proper fact-parts.

The domain is the nonzero powerset mereology on four atoms: a fact is any nonempty predicate on `Fin 4`, with fact identity given extensionally. Thus the domain consists of the 15 nonempty subsets of four atoms. The formalization works directly with those predicates; it does not enumerate all 32,768 pluralities. The elementary cardinality description is not a separate cardinality theorem in the file.

Parthood is subset inclusion. Overlap means sharing a nonempty part. The fusion of any nonempty plurality is the union of its members. The kernel checks:

- Reflexivity, transitivity, and antisymmetry of parthood.
- Overlap exactly when the two facts share an atom.
- Strong supplementation: if `x` is not part of `y`, some part of `x` does not overlap `y`.
- For every nonempty predicate plurality, a fusion containing every member and overlapping precisely what overlaps some member.
- The same union fusion is a least upper bound.
- A witnessed proper part: atomic `q` is a proper part of the two-atom fact `{0,1}`.

## Explanatory relation retained

Name the four atomic facts `q,a,b,e`. Set:

- `q` fully explains every nonempty plurality of facts, including composite facts.
- `a` and `b` fully explain exactly the singleton plurality `{e}`.
- No other fact fully explains any plurality.
- No fact fully explains an empty plurality.

Partial explanation retains the exact source-side definition `PE(x,S) := ∃z, Part(x,z) ∧ E(z,S)`. Every full explainer is atomic, and every nonempty part of an atom equals that atom. Consequently `PE(x,S) ↔ E(x,S)` still holds; it is derived from the source-side definition, not imposed independently.

The kernel checks unrestricted plural PSR, both complete and partial transitivity, distribution to members and their parts, partial source closure, and No Extended Circles. It also checks that:

1. `q` is the unique full explainer of the all-facts target, now including all 15 facts.
2. Distinct `a` and `b` fully explain the narrower target `{e}` while both are outside it and are not parts of its member.
3. The full explainers of `{e}` are exactly `q,a,b`.
4. Composite facts do not fully explain anything under the stipulated relation.

The earlier four-fact model's missing-fusion caveat remains an accurate description of that earlier model. This strengthened model removes that particular limitation; it does not alter the unbounded positive theorem or its candidate-membership requirement.

## Strict semantic limits

The atoms and sets are mereological bookkeeping. Union is a **mereological fusion**, not a demonstrated interpretation of logical conjunction. No logical-negation operation is supplied. Any set complement discussed informally would be relative mereological complement among the four atoms, not the truth-negation of a fact: the complement of `q` is not `¬q`.

Every nonempty subset is treated as a fact in one fixed domain. No truth algebra, semantic entailment theory, modal realization, productive-creation relation, unique-bearer bridge, or actual metaphysical world is thereby established. The strengthened control shows only that adding these standard mereological conditions to the stipulated explanatory package still does not force uniqueness for a narrower target excluding its candidate explainers. There is no new source-priority claim.

## Verification and preservation

Fresh Lean 4.19.0 verification passes using the existing toolchain. The checked declarations use only standard Lean foundational axioms where applicable; no unfinished-proof axioms or new theorem axioms occur.

Run `bash total-explainer-uniqueness/verify-boolean.sh` for this new file only and preservation checks. Its proof output is `boolean-check.log`. The original `Uniqueness.lean`, `FiniteControl.lean`, `RESULT.md`, and `verify.sh` retain their recorded checksums. The earlier source-audit Lean files are also checksum-verified unchanged. `ROOT_VERIFICATION.json` is untouched. No old proof suite is rerun by the new verification script.
