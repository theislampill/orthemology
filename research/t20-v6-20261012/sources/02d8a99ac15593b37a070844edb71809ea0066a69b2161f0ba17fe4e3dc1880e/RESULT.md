# Bounded contextual term-model assessment

10 October 2026. **No new model, theorem, or scalar separation was obtained. The literal source target remains OPEN.** This note records a rejected naive interpretation and the exact unfinished obligation of its more careful repair. Existing files are unchanged; there is no new Lean build.

## Candidate and inherited rejection

The candidate was an open contextual term model in which an assumption is represented by its free syntactic generator, equality at function types is typed beta/eta equality, and Raw retains the original conversion. A useful version would have to validate the actual HasE grammar, including dependent J, proofErase, piExt/allExt and impredicative instantiation. Substituting a System F term model would not meet that contract.

Independent free generators for identity assumptions are already excluded by inherited source controls. In AllInheritedPositiveControls.lean, the actually formed context jContext contains x:alpha, y:alpha and e:Id_alpha(x,y). The theorem literal_j_has derives the literal J term at

    Sigma r:Id_alpha(x,y). Id_Raw(e,I).

Its actual jMotive contains both the endpoint coordinate and a proof-sensitive Raw identity fibre. The fibre is legally formed using proofErase. The base is pair(I,I), and jPoly has the original two K-contractions. Thus simply interpreting the proof assumption e as an unconstrained fresh raw generator fails this existing dependent-J control. A well-typed valuation must respect e's identity type; the unconstrained assignment was never an admissible semantic environment.

This is an inherited test, not a new source theorem or a countermodel. ClosedProofCanonicalisation.proof_raw_conversion and canonical_identity give the complementary **closed-proof** statements; their closedness must not be dropped. The raw-motive boundary separately distinguishes the legally erasable proof coordinate from the endpoint coordinate, whose Raw typing is excluded in the actual original-pair theta context. That exclusion does not reject this proof-sensitive fibre.

## Why the contextual repair remains unvalidated

A context-indexed interpretation can avoid the preceding error by respecting identity assumptions and canonical proof representatives. That is a different candidate. It must specify precisely:

- its worlds, admissible substitutions, and type-indexed equality;
- how declared and derived identity evidence constrains endpoint equality and Raw proof observations;
- coherent substitution into both coordinates of every formed J motive;
- soundness of the actual Pi/All extensionality rules, proof erasure, and finite impredicative type substitution.

Merely checking that the two scalar expressions have different ordinary beta/eta normal forms would not prove their distinction in this repaired equality: the additional identity and proof-erasure equations have not been shown conservative. Conversely, defining contextual equality by existence of an original source identity would make the proposed soundness argument circular for the desired separation.

The missing substantive result is a normalization or conservativity/separation theorem for an **independently defined, all-rule-sound** contextual equality, strong enough to keep n f a apart from (originalQ n) f a in the actual scalar context. No such theorem, terminating reduction system, or concrete normalization route was found in this bounded assessment. No impossibility claim is made about all contextual models.

## Relation to completed work

The full-PER model already validates all twenty actual rules and the universal target. Every closed HasE Church input already has an exact source scalar instance. Neither fact supplies an open-variable source derivation, semantic completeness, or a separating contextual model. The strong graph invariant and its two homogeneous projection obligations are unchanged. Their untyped raw nonconversion witnesses cannot be used as typed environments here.

## Source fidelity

SOURCE_BINDINGS.json records the inspected files, SHA-256 digests, and checks against the inherited pinned-source replay receipt or acquisition record. The source commit is 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c. The actual ExtensionalRepairSyntax, AllSyntax, and AllInheritedPositiveControls files were inspected. No source conversion, typing rule, compiler endpoint, or predecessor evidence was edited. Source rehashing is not represented as a new kernel replay; this assessment deliberately stops before a new model campaign.
