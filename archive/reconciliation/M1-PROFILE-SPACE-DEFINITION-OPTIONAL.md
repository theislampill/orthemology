# M1 OPTIONAL PATCH — explicit definition of the profile space `Π_A`

**Status:** PROPOSED OPTIONAL patch, deliberately **separated from the D1 candidate package** by the D1 scope audit (2026-07-19, Fable 5). D1 required only the *index* normalization (`Π_T` as licensed shorthand for `Π_A`), which the candidates contain. The *content* definition below repairs the independent, pre-existing issue **M1** (theory review: `Π_T` used but never defined) and is gated separately.

**Target locus:** `orthemic-core-formalization.md` §2.2, the `Π_A` gloss paragraph (candidate line ~169); optionally mirrored as one sentence in the manuscript §2 or §5.

**Proposed insertion (replacing the parenthetical gloss with a definition):**

> `Π_A` — with `Π_T` its licensed shorthand under the standing convention — is the **profile space**: a complete profile is an assignment over the factorized axes of the manuscript's §5-family structure, selecting at most one *alternative*-marked value per axis and any set of *co-holding* values; equivalently, a subset of `O` consistent with the exclusivity markings, under the repertoire and merger family declared in `A`. (This supplies the definition the corpus previously used implicitly.)

**Why it is not in D1:** D1(d) fixes what ground truth is *indexed by*; it does not require saying what a complete profile *is*. Bundling the definition would have been silent scope expansion. Adopting this patch is an editorial decision (no owner fork depends on it), natural to batch with the H1 editorial repairs.

**Interaction note:** the definition is A-indexed (repertoire and merger family are components of `A`), so it presupposes D1 — apply it only on top of the D1 candidates, never to the pre-D1 text.
