# Independent adversarial review: homogeneous Henkin candidate

10 October 2026. This package records an independent attack and bounded machine checks, not a replacement whole-source model. No protected source was edited and no baseline was rebuilt.

## Result

No obstruction was found in the proposed homogeneous-support-or-universal PER universe after inspection of the actual source rules. The dangerous operational strictness obligation is valid, and the exact extended SKI calculus is consistent at its two atom tags. The cross-typing observer and the source-constructed graph invariant do not reject this support-sensitive candidate.

Two sharp restrictions are independently machine checked:

1. Within this universe, the actual Raw support obligations force Raw to be universal. Retaining the predecessor Raw=conversion interpretation would immediately fail universe eligibility.
2. One explicitly constructed proper, conversion-saturated mixed-support PER rejects ν. Omitting mixed PERs is a substantive restriction, not merely a different presentation of the full-PER model.

The original HasE noninhabitation conclusion is not supplied by this package alone. It additionally needs whole-source soundness for the new model and the exact originalQ/W application. Those are separate concurrent artifacts; this review does not substitute a assumed model contract for them.

## Actual source inspection

Read the requested retained FullPER.lean, CrossTypedObserver RESULT.md, and InternalGraph RESULT.md; also inspected the actual ExtensionalRepairSyntax.lean, P01Polynomials.lean, UArrowAndCompilerControls.lean, ScalarFusionCore.lean, and the new SourceTransport.lean.

The actual HasE constructors impose no rule identifying Raw with compatible conversion and no rule admitting every saturated PER. Thus Raw=universal and the restricted external All universe are possible semantic choices, provided actual formation closure and all-rule soundness are proved.

The FullPER mutual-induction design can be adapted because the relation interpretation is defined for arbitrary relation-valued type environments before admissibility is imposed. F_mixed therefore remains an unconditional structural equation. Formation must conclude membership in the new fixed universe; it cannot merely conclude ordinary PER laws. The candidate's written audit explicitly supplies this stronger conclusion.

The new SourceTransport has the required arbitrary-environment coverage. Its fold is parameterized by Nat→CaseOperational.T. The bracket-abstraction proof instantiates the old environment with var(n+1), the old argument with var0, and folds under cons a η. Consequently environments containing ν are covered; there is no restriction to old-carrier or source-definable values. All eight actual PolyConvPlus constructors are handled, including the atom/application bridge by compositional equality. The exact pairPoly expansion and its first/second projections agree with the source.

## Exact operational checks

The concrete calculus has I,K,S,ν,a0,a1 and binary application. Function WHNFs are I,K,K x,S,S x,S x y,ν,ν x. Its compatible reduction contains three SKI rules, two ν/atom rules and eight ν/function-WHNF rules.

Strictness.lean independently proves, with no axioms, that if t a reduces to an atom or function WHNF then t reduces to a function WHNF. The proof follows a finite reduction backwards: every root contraction has a function-WHNF left prefix, and without a root contraction the final partial application already has such a prefix. It requires no normalization, head-completeness, or standardization theorem. WHNF stability under reduction is also checked. Conversion strictness needs only a Church-Rosser join.

check_overlaps.py expands the thirteen first-order rules and checks left-linearity and every nonvariable-position unification overlap. All 702 overlap trials pass: the only thirteen overlaps are each rule with itself at its own root. This finite check is supplementary evidence, not a confluence oracle.

Confluence.lean independently checks the exact parallel complete-development triangle law. While this proof was being written, the canonical model worker completed its own confluence artifact. To avoid maintaining competing model carriers, canonical CaseOperational.lean was frozen and freshly recompiled in replay/CaseOperational.lean. Its confluence, conv_join, head_origin, atom_distinct, and atom_not_fun all check under Lean 4.19.0 --trust=0, with only propext, Classical.choice, and Quot.sound. Its ν function law has no axioms. The canonical operational source hash is 5575a1d8e69c8f857b0b15dc6f1358a4c3f44bd54a47bf528cf3295ae59c3708.

## Closure attack

Dependent Pi cannot be assumed to have function-only support without checking empty and universal cases. The candidate handles them correctly: if every supported fiber is universal, Pi is universal; otherwise choose one supported argument with a proper homogeneous fiber. Any supported function has a value-producing application there, so operational strictness forces function support.

Dependent Sigma requires a separate universal-first-carrier case. If its first carrier is proper, the first projection forces function support. If the first carrier is universal, extensionality forces all fibers to be literally the same relation. A universal fiber yields universal Sigma; any proper fiber makes the second projection force function support. Merely observing that introduced pairs are functions would not suffice, since the actual relation allows arbitrary realizers with valid projections.

Arbitrary intersections are universal when all factors are universal; otherwise one proper factor provides homogeneous support for the intersection. The empty PER is harmless. Identity proofs are I-conversion-class realizers and thus function-supported when inhabited. These arguments match the written model and do not presuppose that only source-introduced values inhabit types.

## Concrete mixed-PER rejection control

MixedPERControl.lean imports the freshly checked canonical operational carrier. Put j=K a0 and take the relation whose two classes are the conversion-closed sets {a0,I} and {j}. The file proves symmetry, transitivity, conversion saturation, nontriviality, and mixed support. Distinctness of I and j is tested by applying both to a1; distinctness of a0 and j follows from disjoint atom/function tags.

The constant function K j is an endomap of this relation. The related seeds a0 and I give

- ν (K j) a0 converts to a0
- ν (K j) I converts to j

Those outputs are unrelated. The checked theorem nu_rejected_by_mixed_PER therefore excludes ν from the Church interpretation as soon as this particular mixed PER is admitted. This is a sharp necessary restriction on the candidate universe. It does not refute the proposed homogeneous universe, which correctly omits that relation.

## Source-forced Raw top control

raw_support_forces_universal proves that a homogeneous-or-universal relation supporting both a0 and I is universal. Atom-only support contradicts that I has function tag; function-only support contradicts the atom tag of a0.

The actual rawAtom rule types both source zero and source I at Raw. Their chosen source embedding is a0 and I. Hence any Raw interpretation in this universe must be universal. conversion_not_admissible verifies that conversion itself cannot be an eligible relation, because it supports both values yet a0 and a1 remain nonconvertible.

This explains a genuine semantic scope change relative to retained FullPER. It is consistent with syntactic nonderivability arguments: a source rule system can have multiple sound models with different Raw relations. No claim is made that the new model preserves the predecessor's intended Raw semantics.

## Earlier observer and graph controls

The cross-typing test uses one literal pair seed with both Sigma and Church-pair typings. Its erased value is function-WHNF in both derivations. ν therefore takes one step on both sides, and derivation-independent interpretation gives the same observed value. This is not the earlier rejected split by outer type constructor.

The source graph seed is an encoded pair and hence function-valued; the counterexample scalar seed is a0. Under ν, the graph and state run take one step, whereas the external scalar run takes zero. The graph invariant compares its own internally advanced scalar/state projections and remains valid. The missing scalar projection bridge is precisely what fails at the separating valuation. Actual All elimination and J do not create that bridge without supplied identity evidence.

## Replay and boundaries

Run python homogeneous-per-adversarial-20261010/replay.py from any working directory. It verifies the retained review/input hashes, reruns the overlap check, and freshly compiles only the four added/frozen modules: Strictness, Confluence, CaseOperational, and MixedPERControl. It does not rebuild source baselines or claim a whole-model replay. The fresh result is validation/REPLAY.json.

No added axiom, sorry, unsafe definition, native_decide, or evaluator oracle occurs in these checks. The independent whole-source reviewer owns the fresh actual HasE-soundness replay; the exact W theorem remains a separate application obligation until its own certificate is present.
