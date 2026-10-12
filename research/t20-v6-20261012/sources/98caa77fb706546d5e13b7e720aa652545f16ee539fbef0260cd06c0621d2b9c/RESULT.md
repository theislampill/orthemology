# Actual Joint dependent induction computes propositionally

## Checked result

For every actual `CtxJ Γ`, arbitrary `FormJ (N :: Γ) P`, newly typed seed `p : P(0)`, and newly typed curried step `s : dependentStepType P`, the literal retained `sectionPoly p s` now has actual source computation theorems:

- `induction_zero`: `HasJ Γ I (Id_(P(0)) ((sectionPoly p s) zero) p)`.
- `induction_successor`: for every actual `HasJ Γ n N`, some polynomial proves `Id_(P(succ n)) ((sectionPoly p s) (succ n)) (s n ((sectionPoly p s) n))`.

These conclusions use the frozen `JointCompletion.HasJ`, the existing source identity constructor, and the exact polynomial returned by its `natInduction` constructor. No old-E formation/typing requirement, semantic-reflection rule, or externally supplied rigidity witness occurs in either interface. Both families and data may be recursively newly formed through the two completion rules.

The zero computation also has the retained raw conversion certificate. The successor statement is genuinely propositional: the packet contains a checked counterexample to strengthening it to unrestricted Raw conversion.

## Why the successor theorem needs a source argument

The retained raw fold step computes at the folded total state's first projection, rather than directly at the supplied input n. The proof must identify those indices in the source and transport the dependent action; the constructor's output typing alone does not make this equation a raw computation law.

The first six modules explicitly port and credit the retained actual-E total-space construction from `hase-full-e-dependent-induction-20261010`. They reuse its unchanged definitions and raw equations, but their formation, context, and term premises are actual Joint judgments. Existing Joint term/mixed substitution, regularity, weakening, and impredicative instantiation supply the required structural lemmas. No old structural packet is reproved or modified.

The new source wrapper obtains the already established closed Joint Rigidity witness from `PositiveTransfer.joint_rigidity` and weakens it into the arbitrary Joint context. The ported dependent-action J argument then supplies the pointwise successor identity. Source identity transitivity joins it to the two retained section-application beta conversions, producing the theorem on literal `sectionPoly` applications. This is a syntactic derivation, not an inference from FullPER validity.

The broader ported helpers remain conditional on supplied Joint rigidity, as their names and signatures state. The public `induction_zero` and `induction_successor` discharge that condition using the existing induction-derived witness. No new source rule is added.

## A strict typed-versus-Raw successor control

Set P=N, p=zero, s=K in the well-formed context [N], with n the variable zero. Define the exact left and right endpoints by:

- left = `(sectionPoly zero K) (succ n)`
- right = `K n ((sectionPoly zero K) n)`

`RawBoundary.successor_typed_identity` proves `∃ e, HasJ [N] e (Id_N(left,right))`.

`RawBoundary.successor_not_raw` proves `¬ PolyConvPlus left right` for these same polynomials.

The second proof uses only retained conversion soundness into the concrete shared-application `CaseOperational` carrier. At the environment sending n to the retained ν, the pair seed is function-supported, so ν performs one total-space step. The left endpoint becomes Church successor-zero, while the right becomes ν. Applying both to `K a1` and `a0` yields the distinct inert atoms a1 and a0. Their separation is already checked in the retained operational calculus.

This valuation tests Raw conversion only. It is not asserted to inhabit the Joint context [N] in any sound Joint model. The typed identity and raw nonconversion therefore coexist without changing the source rules or reversing the older failed-model diagnoses.

## Genuinely newly formed dependent-family controls

Let E be the retained `JointCompletion.Controls.newMotive`, whose formation requires the completed Sigma witness and whose old-E formation is already excluded. The new family is:

`P(n) = Id_E(n I I, n I I)`.

The packet checks:

- actual `FormJ [N] P`, seed I, and curried step `abstract (abstract I)`;
- different literal zero and successor-zero instances, so the index occurs in the actual source type;
- `¬ FormE [N] P`;
- no old `HasE` inhabitant of the seed type, and no old `HasE` inhabitant of the step type;
- actual Joint zero and successor computation at this family.

The family is reflexive, and a direct section is separately constructed. Its purpose is strict input-scope discrimination. No necessity/minimality claim for induction is inferred from this easy instance, and literal index dependence is not described as semantic separation of the fibers.

## Precisely bounded comparison consequence

`comparisonFamily P u v` is the literal source family `Id_P(n)(u n,v n)` formed from any two actual Joint dependent sections u,v of P.

`induction_extensionality` proves actual function identity `I : Id_(Pi N P)(u,v)` from:

1. a supplied Joint seed for this comparison family at zero;
2. a supplied Joint curried induction step for this comparison family.

It uses actual `natInduction` to construct the pointwise identity section and actual `piExt`, with every formation and scope premise. The comparison-step premise is explicit. The packet does **not** claim that two arbitrary displayed algebra laws automatically supply it, nor a full categorical initiality theorem, proof-path uniqueness, or automatic uniqueness of arbitrary dependent recursors. This is an induction-to-extensional-identity interface with a declared remaining comparison-step obligation.

## Verification and integrity

Run `python3 hase-joint-induction-computation-20261010/verify.py` for fresh-output replay, or the adjacent `check.sh` for the narrow ten-module compile. The verifier pins the new sources/scripts/report and retained source/object inputs, compiles only these additive modules using the existing Lean 4.19.0 binary with `--trust=0`, and checks every pin again. It removes the candidate's existing validation directory from the replay search path, so no stale candidate object can satisfy an import. No baseline dependency rebuild occurs.

`JointInductionAudit` traverses kernel dependencies of the public results and controls. It rejects custom axioms and `sorryAx`, and rejects FullPER/Joint/Henkin semantic fundamental or completion-rule dependencies in the positive source constructions. Allowed dependencies are only the standard subset of `propext`, `Classical.choice`, and `Quot.sound`. Existing source infrastructure accounts for ordinary classical dependencies; no foundationally choice-free claim is made. The negative controls intentionally reuse their retained semantic/operational exclusions.

The freeze and fresh replay receipt are `validation/CANDIDATE_FREEZE.json` and `validation/AUTHOR_REPLAY.json`; retained inputs are in `validation/RETAINED_INPUTS.json`. Early failed local compilation logs are preserved only under `diagnostics/` and are outside the selected source/replay set. Independent review is separate.

## Frontier preserved

The original literal HasE identity is already excluded by the later retained homogeneous-Henkin whole-source countermodel; the earlier OPEN report is superseded. That negative result, the distinct positive faithful-Raw FullPER model, and the positive unadopted HasJ completion remain separate. This packet advances usable source computation in HasJ. It does not adopt its rules, alter HasE/HasC/HasJ, collapse typed identity to Raw equality, remove the explicit Raw no-confusion gap, establish global completeness or decidability, edit protected sources, integrate a branch, or close T20.
