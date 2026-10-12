# Bounded source check: abstract diffusion with quadratic killing

10 October 2026 UTC. Separate follow-up to the completed moment-evolution source comparison. The earlier report is unchanged. This checks a specified implication in a small source chain; it is neither a novelty search nor an independent review of the active new proof.

## Result

No theorem in the inspected primary arguments supplies the proposed reverse implication

    L_t(1)=1,  L_t(q²)≥0 for all q,
    L_t'(p)=L_t(Δp−|x|²p)+L_t(|x|²)L_t(p)

from an abstract full coordinatewise-C¹ polynomial-functional path to a representing initial probability and its normalized harmonic-oscillator/Mehler evolution.

This is a bounded negative finding, not a claim that no such theorem exists elsewhere. Nothing inspected contradicts the proposed result either. In particular, the earlier pure-heat nonrepresentation obstruction is not a counterexample to the new hierarchy, since it does not satisfy its quadratic-killing term.

## 1. Retained primary arguments: what is reused and what is new

The earlier report already continuously inspected Curto–di Dio–Korda–Magron, arXiv:2211.04416v3, Section 2 and Section 4. Those readings are reused, not counted as new. Theorem 2.2 has supplied Schwartz initial data and smooth bounded spatial coefficients. Its multiplication coefficient would have to be h=−|x|² here, outside that stated class. Lemma 4.1 has no diffusion and supplied atomic initial data. The degree-four truncated backward-heat assertion in Corollary 3.25 is neither the full hierarchy nor quadratic killing; its universal-time premise remains quarantined by the earlier exact obstruction. [Primary PDF](https://arxiv.org/pdf/2211.04416v3)

Newly read: complete Section 4 of Curto–di Dio, arXiv:2108.03505v1, printed pp.18–19, from its opening combined PDE through the paragraph before References. Lemma 4.1 treats Δ plus diagonal linear transport with u_0 in Schwartz space. Its recursion lowers degree or stays at the same degree; no quadratic multiplication term appears. It supplies no representation theorem for abstract functionals. [Primary PDF](https://arxiv.org/pdf/2108.03505v1)

## 2. Following the actual cited existence theorem

The PDE/atoms paper invokes reference [41], Theorem 2.10, for Schwartz-valued existence. Its bibliography prints arXiv:1912.11075, which resolves to an unrelated black-hole paper. A title-and-author lookup identifies the matching primary work as Philipp J. di Dio, *Schwartz Function Valued Solutions of the Euler and the Navier–Stokes Equations*, arXiv:1912.11705. This bibliographic correction was verified against arXiv title, author, and version history. [Correct primary record](https://arxiv.org/abs/1912.11705)

The cited theorem number is present in v5, dated 11 January 2022. Theorem 2.10, printed pp.11–20, constructs a Schwartz-valued solution from f_0∈S(R^n)^m, with g_l,h_ij∈C^d_t(C_b^∞) and Schwartz forcing. Its complete proof approximates this supplied f_0, bounds Schwartz seminorms, takes a compactness subsequence, and identifies a PDE solution. Remark 2.12 adds diagonal linear drift; Remark 2.15 warns that extending the coefficient class is nontrivial. The current v6, dated 5 December 2022, restates the relevant existence result as Theorem 5.1, printed pp.11–16, again with supplied Schwartz data and bounded smooth g,h. These are not abstract moment representations, and −|x|² is not an admissible h in either statement. [V5](https://arxiv.org/pdf/1912.11705v5), [v6](https://arxiv.org/pdf/1912.11705v6)

No stronger conclusion is inferred from that paper's more general title or its nonlinear PDE applications. The earlier v1 was retrieved only to resolve theorem numbering; no reading credit or mathematical dependency is assigned to it.

## 3. Consequence for the active proof

The proposed radial/Riccati estimates and the resulting Carleman existence step remain a distinct proof obligation. A statement constructing a function from an already supplied f_0 cannot supply that step. Nor can a Mehler or Feynman–Kac formula by itself prove that a given square-positive functional is integration against a measure.

After representing measures have been obtained, a classical harmonic-oscillator kernel may identify their evolution, but the passage from polynomial equations to suitable compact/Fourier tests and recovery of the initial law still need justification. The inspected sources do not close those gaps for this abstract hierarchy.

One tempting transport must also be bounded carefully. The formal ground-state identity is

    (Δ−|x|²)(e^{−|x|²/2}f)
       =e^{−|x|²/2}(Δf−2x·∇f−d f).

This identifies a classical relation to Ornstein–Uhlenbeck evolution at function/measure level. Multiplication by e^{−|x|²/2}, however, is not a polynomial-algebra automorphism. An arbitrary abstract polynomial functional cannot be applied to that factor without an extension argument. Hence neither the affine-coordinate theorem nor the pure-heat counterexample can be transported through this identity without additional proof. This observation is our analysis, not a theorem attributed to the inspected papers.

## 4. Stop and claim boundary

The bounded citation chain has been checked: both retained moment/PDE sources plus their specifically invoked Schwartz existence theorem, including the earlier version matching the theorem number. There was no wide search and no external outreach. Other references to occupation-measure relaxations or Schwartz semigroup invariance were not followed: the retained texts did not identify them as a precise theorem furnishing the targeted square-positive reverse implication. No conclusion about all such literature is asserted.

The active mathematical investigator and parent were notified of the non-subsumption finding. This note does not assert the new harmonic-killing theorem is proved, novel, or ready for closure.
