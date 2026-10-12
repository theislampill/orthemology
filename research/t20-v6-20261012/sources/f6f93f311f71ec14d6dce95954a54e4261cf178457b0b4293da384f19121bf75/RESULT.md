# Actual HasE closed weakening

Three isolated modules prove the requested weakening with the unchanged actual 20-rule HasE grammar:

- `HasEStructuralBase.lean`: type-parameter renaming for CtxE, FormE, HasE; all piExt and allExt premises retained.
- `HasEStructuralRename.lean`: conversion substitution for the eight unchanged PolyConvPlus rules, dependent finite-scope term renaming for FormE and HasE, and ordinary one-step weakening.
- `HasEClosedWeakening.lean`: literal closed weakening into any well-formed HasE telescope and the exact Church specialization.

Namespace: `P01AC.ExtensionalRepair.Structural`.

Main signatures:

```
has_closed (h : HasE [] p A) (hΓ : CtxE Γ) : HasE Γ p A
closed_church_weaken (hn : HasE [] n EffectiveCompleteness.N) :
  HasE [ExactScalarFusion.End] n EffectiveCompleteness.N
```

The closed theorem uses the empty renaming and literal identity substitution; it preserves the original polynomial and type. It does not infer actual HasE weakening from old Has weakening and does not invoke semantic reflection, normalization, or completeness. The two structural ports are finite inductions over the actual mutual CtxE/FormE/HasE recursors. Every formation, typing, term-scope, and type-scope premise of piExt/allExt is transported explicitly.

Replay: `python3 replay.py`. It verifies the scalar package's INPUTS, manifest, acquisitions and fresh objects, all 92 reused objects, the Lean binary, and all source files in the pinned imported-compiler-transport manifest. It then compiles only the three new modules into a fresh directory with Lean 4.19.0 `--trust=0`. It rejects warnings, forbidden proof escapes, sorryAx, and theorem dependencies beyond propext and Quot.sound. No prerequisite baseline is rebuilt.

Scope: bounded isolated structural lemma result only; no protected repository mutation, integration, universal scalar-fusion claim, or programme closure.
