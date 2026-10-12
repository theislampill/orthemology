# Primary literature and API comparison — limited, not a priority audit

Research date: 22 September 2026. Public primary text was inspected through web/GitHub read tools. Raw web pages were not downloaded into the runtime; no raw-page SHA-256 is invented. The entries below identify inspected versions and locations, and contain research notes rather than reproductions of whole sources. No personal contact, purchase, submission or expert-review claim was made.

## L1. Christopher P. Porter, *Trivial measures are not so trivial*

arXiv:1503.06332v1 (2015), HTML: https://arxiv.org/html/1503.06332 . Inspected Definitions 2.1–2.4 and §3, especially Theorem 3.2.

Definition 2.4's triviality is exactly concentration on positive singleton atoms, corresponding to d=0 here; its word “atomic” alone means existence of a positive atom, not concentration. Definitions 2.2–2.3 concern total truth-table functionals and induced measures, not the PR one-bit-per-stage numbering stipulated in CV-C. Theorem 3.2 uses a tally functional from an approximation to a noncomputable Δ₂ sequence A; the additional randomness hypothesis on A governs its second conclusion. This is relevant prior machinery, not the exact rational-threshold index theorem. The inspected sections did not establish an equivalent PR-synchronous threshold classification. That limited observation establishes neither novelty nor absence elsewhere.

## L2. Benjamin Lucien Kaminski and Joost-Pieter Katoen

*Analyzing Expected Outcomes and Almost–Sure Termination of Probabilistic Programs is Hard*, arXiv:1410.7225, HTML: https://arxiv.org/html/1410.7225 . Inspected Theorems 3–4 and the geometric-input reduction around Theorem 4.

Theorem 3 classifies exact expected-outcome equality as Π₂-complete; Theorem 4 classifies almost-sure termination as Π₂-complete in that program model. These predicates are not concentration of an infinite output law on countably many singleton atoms. The geometric selector illustrates a related reduction technique but does not discharge CV-C's different syntax, soft-mass limits or Π₃ target. The comparison therefore supports separating predicates and models rather than importing its index bound by analogy.

## L3. Yitzchak Shmalo, *Combinatorial Proof of Kakutani's Fixed Point Theorem*

arXiv:1811.08454v1 (20 November 2018), HTML: https://arxiv.org/html/1811.08454 . Inspected Definition 2.4 and Theorem 2.5.

The theorem uses a finite-dimensional simplex and an upper-semicontinuous correspondence with nonempty compact convex values. Those are precisely the hypotheses discharged for the proposed U08 row-set correspondence. No algorithmic claim from the article's abstract is imported. The original Kakutani article has DOI 10.1215/S0012-7094-41-00838-4; its full text was not recovered through the attempted Project Euclid route. This checkpoint relies on the explicitly inspected primary restatement, not a claimed reading of that inaccessible original.

## L4. Exact-pin mathlib source inspection

Repository: leanprover-community/mathlib4; pin c44e0c8ee63ca166450922a373c7409c5d26b00b.

Read-only GitHub file retrieval inspected `Mathlib/MeasureTheory/Measure/Typeclasses/Finite.lean` and `.../SFinite.lean`. The latter's remotely reported Git blob is 3353fbdc70d9c6ac2f9b37bcf1ab843d7ab082ec. Its countability lemmas for disjoint positive-measure sets and positive level sets support the intended U05 implementation. Finite-measure and decreasing-intersection APIs were also inspected. This is text/API evidence only; no local full-file hash, compiled declaration type or axiom list is claimed.

Default-branch search for “kakutani” returned Riesz–Markov–Kakutani representation material. That is not the fixed-point theorem. No exact-pin fixed-point declaration was identified by this search, and absence is not proved. Discovery on a moving default branch was not used as pinned formal evidence.

## Search and acquisition boundary

The searches concerned computable atomic measures/tally functionals, probabilistic index-set complexity, Kakutani correspondence hypotheses and pinned measure APIs. They do not constitute exhaustive literature coverage. Runtime HTTP acquisition failed with DNS resolution errors, independently of the working text-oriented web/GitHub tools. Existing sources, elementary proofs and new application proposals carry no global-priority or peer-review credit.
