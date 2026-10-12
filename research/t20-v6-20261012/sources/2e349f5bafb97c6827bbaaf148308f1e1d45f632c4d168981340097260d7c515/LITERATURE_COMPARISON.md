# Primary-literature comparison and source-status proposals

No priority, foundational novelty, peer review or exhaustive literature coverage is claimed. All statements below concern the named versions and locations. The research's own proofs are in the obligation files. Downloaded publication bytes are **not** asserted to be present in this checkpoint: literature was read through the web tool. The retrieval record retains exact URLs, versions and locations rather than inventing byte hashes.

## L1 — Pistone, exact 5.21 / 7.1 comparison

Paolo Pistone, *On completeness and parametricity in the realizability semantics of System F*, arXiv:1802.05143v5; LMCS 15(4), 2019. Primary source: https://arxiv.org/pdf/1802.05143v5 . Locations: printed 6:34, 6:36–37 and 6:45; PDF indices 33, 35–36, 44.

**Primary statements (paraphrased).** 5.21: adequate F-closure C over L⊆Λ, satisfying SU/SA/SS; any type σ, closed M; C-realizability implies C-invariance. No positive-type restriction belongs to this theorem. 7.1(i): additionally C≤βη-closure, M closed βη-normal, σ∈∀+; realizability, βη-invariance and βη-dinaturality are equivalent to existence of a typed M₀ with M₀→η* M. 7.1(ii): C≤β-closure, M closed β-normal, σ∈∀+_P; the corresponding β conditions are equivalent to typing M itself. Section 5.3 distinguishes full Reynolds semantics; Proposition 5.23 refutes identity extension even for βη-stable semantics.

**Exact P01 comparison.** Our finite theorem assumes a derivation. The fixed-environment K countermodel does not address universal unary interpretability. Our Ω result uses a rigid empty primitive and a divergent realiser. Neither example contradicts the cited implications. No C-closure/model-transport verification is supplied. Separately, our own I/SKK calculation proves that the SKI macro map does not reflect canonical conversion; target beta equality cannot silently replace it. A PER replacement would change the model and needs review, not automatic “novel theorem” credit.

The current read successfully included theorem text and page screenshots; historical failed screenshot attempts in the input remain historical failures. This proposes only a **new scoped literature-read record**. It does not rewrite `PRIOR_ART_COMPARISON.md`, retrospectively recover historical visual credit, or establish a new theorem about its source.

## L2 — Girard, Lafont and Taylor: System F normalisation

*Proofs and Types*, primary author-hosted PDF: https://www.paultaylor.eu/stable/prot.pdf . Chapter 14, §14.3, printed p.118 (PDF index 125), gives reducibility and strong normalisation for System F. The page was read and visually inspected in this run.

The target in the present historical transfer is Curry-style typing. A formal import of the explicit System F proof needs a proved annotation/erasure bridge or a matching Curry metatheorem, plus the rigid-atom extension and subject reduction. P01-U09-03 exposes these assumptions. No new normalisation theorem is claimed, and the local compiler's absence is not conflated with the truth or falsity of this ordinary theorem.

## L3 — Clairambault and Dybjer: contextual equality requirements

Pierre Clairambault and Peter Dybjer, *The Biequivalence of Locally Cartesian Closed Categories and Martin-Löf Type Theories*, primary manuscript https://arxiv.org/pdf/1112.3456 . Definitions 3–5, PDF indices 4–5, explicitly include substitution stability for identity/Sigma/Pi operations; the Pi structure includes beta and eta, and its identity types are extensional.

That is a comparator, not a theorem automatically applicable to this packet. Our raw-SKI core does not supply the required abstraction on equivalence classes; we directly refute the proposed bracket-congruence bridge. We also do not postulate the comparator's equality reflection or unrestricted ambient sections. No biequivalence or full categorical-model claim is made for Orthemology.

## L4 — Speight and van der Weide: a scoped advance beyond the supplied abstract lead

Sam L. Speight and Niels van der Weide, *Impredicativity in Linear Dependent Type Theory*, arXiv:2602.08846v1, primary text https://arxiv.org/html/2602.08846v1 . The inspected portions include §3 Proposition 4 (combinatory abstraction), §4 Definition 21/Theorem 22 (modest sets/PERs), and Example 23 (PER-based universe with Cartesian and linear decoders and the stated product closure).

These named portions support a more specific comparison than the input's abstract-only lead. Their use of relational/modest decoding is not the raw-program Code decoding retained here. Proposition 4 gives an applicative abstraction equation; it does not grant our two compilers congruence under raw SKI conversion. No complete reading of the manuscript or independent execution of its Rocq formalisation is claimed. The associated source-status proposal is **PARTIAL_FULL_TEXT_TARGETED_READ**, not “fully verified comparator”, and no canonical literature-status edit is authorised.

## Provenance and limits

The retrieval record is `LITERATURE_READS.json`. Formal pin information comes from the input evidence, not from a moving release page. Technical conclusions about the proposed P01 models follow from the explicit calculations in U09–U11. Independent terminology overlap and standard constructions are not proof of novelty; absence of a matching phrase is not proof of priority. No inaccessible owner/licensing evidence has been filled in with a literature inference.
