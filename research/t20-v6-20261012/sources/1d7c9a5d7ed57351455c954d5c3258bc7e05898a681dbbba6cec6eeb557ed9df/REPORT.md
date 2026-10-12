# Early type interfaces and the Sixth residual agenda

11 October 2026. Additive reading and reconciliation of T1-P01, T1-DEPENDENT and S6F-26. Delivered v4 is unchanged. This is fresh source inspection and a written interface deduction; no Lean kernel was run in this audit.

## 1. What the early type inheritance actually supplies

The original P01 family is more specific than a general warning that type theory remains incomplete. `P01TypeAlgebra.lean` supplies a finite type-code grammar and capture-avoiding substitution laws. `P01DependentModel.lean` interprets its finite dependent successor grammar into a constructed, endpoint-aware PER model. Its raw-index relation is pointwise raw conversion; heterogeneous relations between type-parameter environments are a different object. The grammar includes parameters, bottom, universal quantification, raw terms, identity, arrows, dependent Pi and represented Sigma. It does not admit every semantic family as a syntactic type.

The read `P01PER.lean` definitions make the distinction concrete. A PER carries a symmetric and transitive binary relation compatible with raw conversion. Its carrier consists of self-related terms. Function-space membership additionally preserves the domain relation: for every related pair of inputs, the two outputs must be related in the codomain. A unary carrier predicate forgets this information.

`P01CanonicalCarrierProjection.lean` therefore proves carefully scoped positive squares, not a universal equivalence of representations:

- Raw-index Pi has the declared canonical dependent-Pi carrier.
- Represented Sigma has the declared canonical dependent-Sigma carrier under its stated coherence conditions. This is not the entire ambient Cartesian product.
- Raw identity has the canonical raw-equality carrier.
- The syntax-specific admission theorems preserve the very same evaluated source term. They do not replace it by another witness.
- For arbitrary PER arrows only one inclusion is supplied, from relational function membership to canonical unary-arrow membership.
- For arbitrary PER identity, canonical raw equality implies relational identity, but the converse can fail.

The paired counterexamples are inherited proved source statements. They are substantive reasons not to advertise a complete recursive canonical-carrier equivalence. They are not proof failures introduced by T20.

## 2. A missing T1-to-T20 connection: equal carriers are not a safe type-constructor quotient

Let U be `totalPER`, which relates every pair of raw terms, and R be `rawPER`, whose relation is raw conversion. Both have the same unary carrier: every raw term is self-related. Let I denote the raw identity combinator.

The source theorem `arbitrary_arrow_reverse_projection_fails` establishes that I belongs to the canonical arrow constructed from these two unary carriers, while I does not belong to the carrier of `ArrPER U R`. The reason is exact: the total input relation relates I to SKK; requiring their outputs to be raw-convertible contradicts the retained I/SKK raw-nonconversion theorem.

There is a useful explicit comparison implicit in the same definitions. I does belong to `ArrPER R R`: if x and y are raw-convertible, the reductions I x → x and I y → y, together with that conversion and symmetry/transitivity, give raw conversion between I x and I y. Thus:

1. The input types U and R have identical unary carriers.
2. Applying the same Arrow-with-codomain-R context yields different unary carriers, separated by I.

Consequently no operation depending only on those input carriers can reproduce both actual Arrow carriers. If such an operation existed, equal input carrier pairs would have equal outputs, contradicting the displayed separating term. This is an elementary written consequence of the inherited definitions and counterexample, not a newly kernel-checked theorem or a new general quotient theorem.

This supplies a concrete earlier witness for T20's continuation/fibre discipline: equality at the present observation interface need not remain equality after an admitted future operation. Here the observation is unary term admission; the future operation is a type constructor. A representation intended to support Arrow contexts must preserve enough of the input relation, or restrict its constructor menu to cases for which a square has actually been proved.

The positive raw-index Pi/Sigma/identity squares matter equally. The response is not to reject every projection. The exact class and coherence hypotheses determine which projections survive. A type-directed compiler or cache can use the proved restricted squares, while retaining relational semantics for the unsupported contexts.

### Boundaries of the connection

- This is a connection to the general future-operation preservation criterion, not a transfer of a P01DF theorem into HasE, HasJ, HasPlus or HasC.
- The exact judgement, context, source term and relation must remain attached to a type-directed certificate. The unary set alone is insufficient in the exhibited interface.
- It does not say that computing `carrierCode (ArrPER U R)` gives the same answer as constructing `Code.arrow (carrierCode U) (carrierCode R)`. Their disagreement is precisely the source result.
- No inference to psychological understanding, personal identity, metaphysical possibility or actual warrant follows from this formal separation.
- The old Option/PLift representation repair remains a real interface change. This selected reading does not requalify every original signature or every repaired declaration.

## 3. Identity has its own directional boundary

The same projection file proves `arbitrary_identity_forward_projection_fails`: its recursively interpreted identity type relates I and SKK, but canonical raw equality cannot identify them. This is not the same failure as an arrow's reverse inclusion. One concerns a relational extensionality obligation; the other concerns an equality relation stronger than raw conversion.

These inherited results help explain why T20 must keep proof identity, proposition identity, raw term identity and typed behavioural equivalence separate. They do not show that any particular later proof-irrelevant calculus has the same counterexample. The later calculus needs its own formation, context and conversion rules, which the v4 owner files already distinguish.

## 4. S6F-26: old open problems are dated obligations, not timeless status labels

The full pinned public projection of `SEVENTH_RESIDUAL_AGENDA.md` was read. It already gives a discriminating four-part research programme:

1. Establish the actual existential connection while retaining the separate P1/P2/N2/N3 burdens; do not substitute a conditional coverage theorem for their warrant.
2. Connect objective fittingness to truthful practical agency, separately tracking comprehension, motivation, attestation, actual address and recipient warrant.
3. Warrant an integrity commitment lasting from disclosure to actual intervention, with revocation and containment inside the same support budget.
4. Establish justified criterion revision across recipients and versions, preserving reference, permissions, actual repair capacity and an independent basis for diagnosing the rule's defect.

It explicitly regards the static disclosure frontier and the Unit-seed positive-exponential badCount endpoint as closed at their own scopes. It also says that badCount is not physical elapsed time; later controller terminology does not erase this limitation. These are earlier positive results and useful constraints on current cross-contributions.

The agenda's historical withholding on foundational bridges does not overrule later positive source-based appraisals. The correct join is chronological: retain what the Sixth proposed, identify the later premise/source argument that addressed it, and retain the exact unresolved generalisation. Conversely, later operational success does not retroactively supply philosophical premises it never consumes. This is consistent with the dated foundational reconciliation in v4 and the separate early-foundations audit.

The remaining agenda conditions are not permission to restart four research campaigns during this closure audit. They are source-owned safeguards for determining which later results actually answer which earlier questions.

## Evidence and disposition

`SOURCE_BINDINGS.json` records exact files, hashes and reading ranges. Full bodies were read for the type algebra, dependent model, canonical projection, status map and Sixth residual agenda. Only lines 1–180 of the recursive model, lines 1–115 of the PER file, and lines 1–65 of the dependent controls receive current reading credit. The latter supplies the explicit totalPER definition at lines 36–40. Original compile/review receipts mentioned by `STATUS_MAP.md` remain inherited evidence. Historical `UNCOMPILED` headers are not a fresh failure finding; later qualification must be resolved through the exact owner receipts.

The omission is a missing constructive interface explanation in the v4 reader, not loss of source custody. Add this explanation and the three explicit coverage rows to the closure supplement. No change to the original theorems, source files or v4's claims is required.
