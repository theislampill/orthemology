# Primary-source check: fibrewise exact W→FR correction
Date checked: 2026-10-11 UTC. Scope: attribution and bounded comparison, not an exhaustive novelty review.

## Bottom line
The proposed one-fibre map R_h composed with D_h is already the exact probability-normalized W-FR Lie–Trotter splitting in Crucinio–Pathiraja. Gaussian preservation and SHK Gaussian geometry are also established. The present work should attribute those ingredients and separately prove its fixed-marginal/fibrewise, singular-entrance, measurability, and entropy statements. “Not located in the passages checked” is the strongest justified absence claim.

## 1. Exact-semigroup duplicate
Francesca Romana Crucinio and Sahani Pathiraja, *An operator splitting analysis of Wasserstein–Fisher–Rao gradient flows*, arXiv:2511.18060; first submitted 2025-11-22, latest checked v3 dated 2026-09-16.
Primary: https://arxiv.org/html/2511.18060v3
Stable PDF: https://arxiv.org/pdf/2511.18060v3

Locators: §2, printed pp. 3–5: (2.1)–(2.5), display (W-FR), Assumption 1, Propositions 2.2–2.3; §3, pp. 5–6, (3.3)–(3.4); Appendix B.1, pp. 22–23.
The paper explicitly uses exact component solution operators and the centred reaction. Equation (2.5) is the normalized power map. Display (W-FR) composes W first and FR second. Its Gaussian formulas directly overlap the proposed Gaussian step.
Assumption 1 requires smooth Gibbs initial density with bounded Hessian, an LSI, and absolute continuity relative to the target; it additionally assumes FR/WFR well-posedness. Appendix B.1 requires nondegenerate covariances. Consequently these stated results do not supply arbitrary/singular P2 entrance. No fibrewise fixed-marginal theorem was found in these passages. The p. 3 display begins its index at 2 despite an initial value at 0; avoid inheriting that indexing.
Version distinction: v1 labels the two schemes (2.6) and (2.7); v3 uses (W-FR)/(FR-W). Do not mix equation numbering.

## 2. Gaussian SHK geometry
Matthias Liero, Alexander Mielke, Oliver Tse, Jia-Jie Zhu, *Evolution of Gaussians in the Hellinger-Kantorovich-Boltzmann gradient flow*.
Primary HTML: https://arxiv.org/html/2504.20400v1
Existing primary PDF reused: https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf

Locators in WIAS Preprint 3198: §3.4, printed pp. 13–14, Onsager operator before (3.7), Lemma 3.10, Theorem 3.11, (3.8a–b); §6.1, pp. 28–29, (6.1)–(6.2) and updates.
The normalized SHK operator centres reaction, and Theorem 3.11 supplies Gaussian mean/covariance dynamics with separate transport and reaction contributions. Thus Gaussian invariance and the reduced SHK structure require attribution.
Section 6.1 interleaves discretized Fisher–Rao, Bures–Wasserstein, and mass updates; it is not the exact-semigroup scheme above. Its Gaussian manifold uses positive-definite covariance.
Caution: the expanded drift in (3.7) prints a plus before rho grad log pi, inconsistent with the preceding Onsager operator, (1.3), (3.8), and target stationarity. Use the operator/(3.8), rather than importing that sign. This narrow apparent typo was already documented in the existing workspace comparison and was independently rechecked here.

## 3. Variational splitting, unnormalized setting
Thomas O. Gallouët and Léonard Monsaingeon, *A JKO Splitting Scheme for Kantorovich–Fisher–Rao Gradient Flows*, SIAM J. Math. Anal. 49(2), 1100–1130 (2017), DOI 10.1137/16M106666X.
Author PDF: https://gallouet.github.io/JKOKFR.pdf
Record: https://arxiv.org/abs/1602.04457

Locators: §4, author-PDF printed pp. 13–15, (4.4)–(4.5), Lemma 4.1 and following monotonicity display.
These are successive Wasserstein and Fisher–Rao minimizing-movement problems for the same energy. The first preserves the preceding mass; the second varies it. The manuscript explicitly explains the operator-splitting interpretation and telescoping energy decrease, under finite initial energy.
This establishes substantial ancestry for transport/reaction splitting and discrete energy dissipation. It does not identify those variational resolvents with exact semigroups, impose centred probability reaction, or provide the present singular-initial-law entrance claim.

## 4. Earlier exact normalized reaction
Carles Domingo-Enrich and Aram-Alexandre Pooladian, *An Explicit Expansion of the Kullback-Leibler Divergence along its Fisher-Rao Gradient Flow* (2023).
Primary PDF: https://arxiv.org/pdf/2302.12229v1
Published paper: https://openreview.net/pdf?id=9pWjgQ3y85

Locators in downloaded arXiv v1: §2.2.2, (12); §2.3, printed pp. 5–6, (14), Proposition 1 and (20).
The normalized geometric interpolation is defined using its partition function. Proposition 1 identifies the FR time with interpolation parameter 1−exp(−t), yielding exactly R_t(q) proportional to q^(exp(−t)) pi^(1−exp(−t)). The exact power-map reaction is therefore independently established prior art.

## 5. Earlier implemented W→FR approximation
Crucinio–Pathiraja, *Sequential Monte Carlo approximations of Wasserstein–Fisher–Rao gradient flows*, arXiv:2506.05905v1 (2025).
Primary: https://arxiv.org/html/2506.05905v1
Locators: §3, (3.1)–(3.6), Algorithm 1.
It alternates a ULA-type transport approximation with normalized geometric reweighting, using delta=1−exp(−gamma). Distinguish the ULA kernel from exact OU. Equation (3.3) temporarily suppresses normalization; (3.5) uses proportionality and Algorithm 1 normalizes weights. This is further ancestry, not a substitute for the exact-splitting paper.

## 6. Normalization terminology
Stanislav Kondratyev and Dmitry Vorotnikov, *Spherical Hellinger-Kantorovich gradient flows*, arXiv:1809.03430v2 (2019).
Primary: https://arxiv.org/pdf/1809.03430v2
Locators: introduction, printed pp. 1–2, (1.8)–(1.11), Remark 1.1.
These distinguish conic HK on varying-mass measures from spherical HK on probabilities and explicitly centre the reaction. Their domain setting there is a bounded smooth domain or flat torus. Cite for terminology, not as an automatic whole-space/singular-entrance theorem.

## Independent application-level deductions for the current construction
These are derivations for the current task, not claims of historical novelty or assertions that the papers prove the present fibrewise theorem.

Fix y, let pi_y=N(g(y),T), T positive definite, and use unit transport/reaction coefficients. Put
A_h=exp(−h T^{-1}), Q_h=T−A_h T A_h.
Then the transport component solves the standard OU equation:
D_h r = integral N(g(y)+A_h(z−g(y)),Q_h) r(dz).
For Gaussian r=N(m,C), its moments are m_D=g+A_h(m−g) and C_D=A_h C A_h+Q_h. With a=exp(−h), reaction gives
C_new=[a C_D^{-1}+(1−a)T^{-1}]^{-1},
m_new=C_new[a C_D^{-1}m_D+(1−a)T^{-1}g].
These expressions avoid inverses of C−T. In contrast, the source's compact (3.3)–(3.4) presentation contains (C0−Cpi)^{-1}; “C0≠Cpi” alone does not ensure this inverse exists in dimensions greater than one. Do not inherit that restriction/ambiguity.

For every h>0, Q_h is positive definite. Thus D_h maps any initial probability to a smooth positive density. For initial r with finite residual second moment, mixture convexity of KL gives the explicit entrance bound:
KL(D_h r || pi_y) ≤ 1/2 [tr(T^{-1}Q_h) − d + log(det T/det Q_h)
+ integral (z−g(y))^T A_h T^{-1}A_h(z−g(y)) r(dz)].
This directly permits singular initial laws and does not require their initial entropy to be finite.

For positive q with finite KL, define psi(a)=log integral (q/pi_y)^a d pi_y. The normalized reaction has entropy a psi'(a)−psi(a); its derivative in a is a psi''(a)≥0. Since a decreases from 1 to exp(−h), reaction does not increase KL. Endpoint justification can use truncation/convexity rather than assuming finite log-variance at a=1.

Applying these maps to a measurable conditional probability kernel, normalizing separately on each fibre, leaves the y marginal fixed. Integrating the entrance bound is legitimate when the joint residual second moment is integrable. Integrating the component entropy decreases gives discrete conditional-entropy decrease. For finite starting conditional entropy, standard Gaussian OU entropy contraction additionally gives the transport factor exp(−2h/lambda_max(T)); the reaction cannot weaken that bound. Starting from singular data, state the finite bound after the first step before making finite-entropy contraction claims.

Recommended framing: “We apply the established exact W–FR splitting fibrewise, and verify its well-definedness, fixed-marginal preservation, singular entrance, and entropy descent under our hypotheses.” The fixed-marginal/disintegration and entrance packaging is not in the checked source passages, but follows directly from standard kernel and entropy facts; this search does not establish field novelty.

## Scope limits
No general convergence-to-the-coupled-PDE theorem for arbitrary singular fibres was checked or established here. Exact component flows do not make their composition the exact coupled flow. No continuous-time rate, SHK metric convexity result, acceleration claim, or source well-posedness theorem should be transferred without its assumptions. The PDF/text hashes and precise reading boundaries are recorded in SOURCE_READING.json.
