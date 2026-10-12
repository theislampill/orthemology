# P15 research brief — Normative gap disclosure and is–ought underdetermination

P15 is a **supplemental dependent research packet**. It does not add canonical open obligations. Its local `P15-IOxx` identifiers exist only to make the research handoff auditable.

The motivating thesis is not “Orthemology proves Hume.” It is more precise: Orthemology may be able to formalise **disclosure conditions** under which a normative conclusion depends on additional ordering, utility, objective, constraint, or admissibility structure that is absent from a fixed descriptive reduct.

Candidate core semantics:

`D |=_B phi` iff every admissible normative extension of `D` in the independently specified bridge class `B(D)` satisfies `phi`.

If there exist admissible extensions `N1,N2` over the same `D` with `N1 |= phi` and `N2 |= not phi`, then neither `phi` nor its negation is bridge-invariant over that class. This would be a **gap-disclosure certificate relative to the formalisation**, not a proof that every possible is–ought transition is invalid or unbridgeable.

Primary work units:

- **P15-IO01:** typed descriptive/normative signatures, bridge classes and admissible extension semantics.
- **P15-IO02:** bridge-dependent underdetermination / normative-gap disclosure theorem family.
- **P15-IO03:** scalarisation ranking-reversal and order-manufacturing witness family.
- **P15-IO04:** utility/order entry point in game and best-response semantics.
- **P15-IO05:** descriptive fixed points versus normative optima, with countermodels and sufficient bridge conditions.
- **P15-IO06:** reduct/fibre/section formalism and exact meanings of “canonical enrichment.”
- **P15-IO07:** machine-visible bridge provenance and gap-certificate/checker design.
- **P15-IO08:** general Orthemological gap-disclosure schema beyond is–ought.
- **P15-IO09:** Humean scope, standard logical/metaethical background and prior-art ceiling.
- **P15-IO10:** final applied-Orthemology specification and Codex implementation handoff.

P15 should distinguish at least two gaps:

1. descriptive/feasible structure does not yet specify a normative evaluation;
2. stability under a supplied evaluation does not thereby establish that the evaluation is correct.

The strongest useful outcome is a typed theorem/countermodel/certificate suite that exposes *where* an extra bridge entered and whether a target judgement is invariant under alternative admissible bridges. The weakest acceptable outcome is a precise negative result showing why this proposed Orthemology application fails.
