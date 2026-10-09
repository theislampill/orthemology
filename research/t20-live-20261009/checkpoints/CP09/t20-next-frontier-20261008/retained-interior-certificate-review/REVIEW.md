# Independent adversarial review: retained-interior route certificate

8 October 2026 UTC. Scratch-only sibling review. No prior file was edited; no integration, physical validation, or T20 closure is authorized or claimed.

## Verdict

The mathematical candidate passes independent review against the final artifact identities in FINAL_ARTIFACT_BINDINGS.json. No blocking mathematical or kernel issue was found. The retained-state staircase event forces at least m coordinate-separable AND routes. For exactly m independent identically distributed routes with law μ and null coordinate-axis mass, its probability is exactly m! ∏ᵢ μ(Bᵢ). The stipulated Joe command-space law gives strictly positive box masses. Consequently the finite panel has infinite forward KL from the m=n+1 alternative to the n-route baseline.

This is a one-sided pathwise count certificate and a distributional support separation. It is not certain one-vector identification, a broad sample-complexity theorem, a physical instrument, a certificate of route-to-route independence, or a certificate of arbitrary global copula factorization.

## 1. Source-specific pathwise proof

Let route r have retained gates G_A,r(a) and G_B,r(b), with success their conjunction. Suppose i<j and the same route witnesses both qᵢ=(aᵢ,bᵢ) and qⱼ=(aⱼ,bⱼ). Its A gate is therefore on at aᵢ. Its B gate is on at bⱼ≤bᵢ₊₁, so coordinatewise monotonicity of that gate makes it on at bᵢ₊₁. The route therefore hits the forbidden connector rᵢ=(aᵢ,bᵢ₊₁).

For E, every qᵢ has a witness, and distinct qᵢ must have distinct witnesses. Choosing one witness for each qᵢ gives an injection from m positives into the route inventory. This proof needs neither within-route nor between-route probabilistic independence. It needs retained route states, coordinate-separable conjunction, and the negative connector readings. The displayed orientation needs only B-gate monotonicity; A monotonicity and strict coordinate spacing enter the intended threshold model and the positive-volume construction, not this minimal combinatorial implication.

Mere coordinatewise monotonicity of an arbitrary two-input route response is insufficient. The one-route function

    (a≥1/3 and b≥2/3) or (a≥2/3 and b≥1/3)

is monotone, but returns (1,1,0) on the m=2 positives and connector. The source-specific AND premise is doing essential work.

## 2. Exact occupancy characterization and likelihood

A threshold route witnessing qᵢ must satisfy X≤aᵢ and Y≤bᵢ. For i>1, the preceding negative connector forces X>aᵢ₋₁. For i<m, the following negative connector forces Y>bᵢ₊₁. Thus, ignoring null axes, that route lies in

    Bᵢ=(aᵢ₋₁,aᵢ] × (bᵢ₊₁,bᵢ], a₀=bₘ₊₁=0.

Conversely a route in Bᵢ witnesses qᵢ, no other positive, and no connector. The Bᵢ are pairwise disjoint. With exactly m routes, the pathwise injection is a bijection: E holds precisely when the labelled routes occupy the m boxes once each. There are m! disjoint assignments, each having probability ∏ᵢ μ(Bᵢ) under iid route laws.

Null axis mass is a genuine premise of the open-axis box equality. An X=0 witness of q₁ need not lie in (0,a₁], although the pathwise certificate still holds. One can instead modify the first/last boundary conventions for laws with atoms; the candidate's stipulated continuous margins already make axes null.

For independent heterogeneous laws μⱼ, the exact expression is the permanent

    Σπ ∏ⱼ μⱼ(Bπ(j)),

not m! times one product. Independent full-support laws give positivity even without identical distribution. Full-support marginal route laws without between-route independence do not suffice: all route threshold pairs can be identical copies of one shared pair, leaving E impossible for m≥2.

For F_c(a,b)=1−(1−ab)^c, 0<c≤1, the interior mixed derivative is

    c(1−ab)^(c−2)(1−cab)>0.

Each Bᵢ contains a nondegenerate interior rectangle, so it has positive mass. This checks precisely the support needed here; F_c is a command-space CDF with margins H_c, not itself a uniform-margin copula when c≠1.

For the requested n=1,m=2 design, independent symbolic enumeration gives

    P₁(E)=2((2√2−√7)/3)²
         =10/3−8√14/9
         =0.0074156562009409905922233490519561762168712819744649… .

## 3. Forward KL and channel distinction

The transcript has 2m−1=2n+1 bits. The n-route baseline gives E probability zero by the pathwise proof; the stipulated m-route alternative gives E positive probability. Thus P₁ is not absolutely continuous with respect to P₀ on this finite transcript space, and KL(P₁∥P₀)=∞. No reverse-divergence or perfect single-vector classification conclusion follows from that argument.

Fresh redraws between queries destroy the certificate. For n=1 on the concrete three-query panel, independent redraws give E probability 32/729>0 in both endpoint-matched worlds. Holding only the inventory is insufficient. Separately readable nonlatched responses and retention of the entire actual threshold vector are essential.

The earlier full-face-minimum KL result explicitly restricts retained observations to coordinate faces. Interior queries are not a function of the pair of coordinate minima. For example, the two retained vectors

    {(1/6,1/2),(1/2,1/6)} and {(1/6,1/6),(1/2,1/2)}

have identical minima (1/6,1/6), but yield respectively (1,1,0) and (1,1,1) on this interior panel. Hence the finite face-only information bound is not contradicted.

The inherited t=3/4 heterogeneous-copula three-bit alias also remains intact. Its first route is comonotone and its second uses half countermonotonicity plus half independence. Independent enumeration reproduces the exact shared law

    000:1/16, 100:3/16, 010:3/16, 111:9/16.

In particular, that alternative assigns the certificate event 110 probability zero. Its singular/non-full-support route law is not the stipulated iid full-support Joe alternative. A particular heterogeneous finite-panel alias is not a counterexample to the pathwise implication or to the present positive-probability claim under its stated distribution.

## 4. Boundary inventory cases

- For arbitrary finite inventories of coordinate-separable conjunction routes, including unary and zero-gate supports, the certificate bounds total routes. In the four-support class ∅, A, B, AB, unary B can supply q₁, unary A can supply qₘ, and the middle positives require AB routes. Thus the certificate forces only max(m−2,0) AB routes without a pure-AB premise. The concrete m=2 panel can be satisfied by two unary routes and zero AB routes.
- A zero-gate route is always successful. For m≥2 it makes a negative connector impossible. For m=1 there are no connectors; one successful route, including a zero-gate route, satisfies the elementary lower bound.
- The m=1 pathwise and iid occupancy identities hold and were explicitly tested. The requested hard pair assumes n≥1 and m=n+1≥2. Substituting n=0,c=0 would not produce the stated continuous full-support Joe CDF and is excluded.
- Strict coordinate spacing and strictly interior positives ensure positive-volume boxes and exclude accidental connector-positive coincidences. They are sufficient conditions for this design, not a claim that every finite panel separates the counts.

## 5. Optional certificate-only waiting observation

For exactly m iid routes, disjointness gives Σᵢμ(Bᵢ)≤1, so AM–GM yields

    P₁(E)=m!∏ᵢμ(Bᵢ)≤m!/m^m.

Repeating one fixed panel on fresh independent retained vectors until E first appears gives a geometric waiting time with mean 1/P₁(E)≥m^m/m!. This observation concerns that certificate-only stopping rule under P₁. It gives no lower bound for a test using other transcript outcomes, other panels, heterogeneous route laws, or adaptive protocols. It is not an overall sample-rate conclusion from infinite KL.

## 6. Independent deterministic evidence

REVIEW_CONTROLS.py imports no author implementation and uses no Monte Carlo.

1. Exact OR-convolution over all threshold comparison cells for m=1,…,8 establishes zero E assignments for every route count k<m and exactly m! labelled assignments for k=m. Convolution groups identical signatures but counts the complete finite cell-vector space.
2. Unequally spaced rational panels for m=1,…,5 match the exact iid mass-product formula, avoiding equal-cell symmetry as a hidden assumption.
3. Independent symbolic enumeration of all 81 labelled cell assignments for n=1,m=2 verifies the requested radical exactly.
4. Ninety-decimal CDF-cell convolution for Joe alternatives n=1,…,6 matches the box formula, with absolute discrepancies below 10⁻⁸⁰ and positive cell masses.
5. Exact heterogeneous positive-cell controls verify the permanent and reject a naive iid diagonal expression.
6. The extended k>m occupancy inclusion–exclusion formula was independently checked by exact convolution for m=1,…,6 and every k=0,…,m+2. Its proof partitions the connector-avoiding routes into the disjoint positive boxes and the inactive region, then applies inclusion–exclusion to missing boxes.
7. Explicit controls cover nonseparable monotone logic, fully dependent identical routes, threshold redraws, unary/zero gates, axis atoms, identical face minima with differing interior bits, and the inherited heterogeneous alias.

The author controls were additionally copied into the review directory and rerun; their JSON result reproduced the author result byte-for-byte. These are separate from the independent reviewer controls. The bounded controls support and attack the proof; they do not replace its all-m argument.

## 7. Lean assurance and its limits

The source RetainedInterior.lean was read in full and independently replayed with Lean 4.19.0, warnings-as-errors, into this review directory. KERNEL_REPLAY.log records success. A second isolated replay through the inspected verify_kernel.sh used compiler trust level zero (`-t 0`) and also passed; kernel-isolated/TRUST_ZERO.log records its clean axiom report. Two deliberately mutated proofs were rejected: connector hits substituted for connector misses, and m+1 substituted for m in the cardinal conclusion. Their rejection is a compiler negative control, not a replacement for the semantic argument. The existing compiler and imported libraries remain identified dependencies; this does not claim a freshly bootstrapped verification of the entire toolchain.

The formal chain derives connector_forced from route-specific coordinate gates, derives witness_injection from positive and negative observations, obtains the finite cardinal inequality, and explicitly instantiates threshold AND. It does not merely postulate witness incompatibility. The axiom reports contain only the standard propext, Classical.choice, and Quot.sound dependencies; no sorry or custom semantic axiom appears.

The formalized scope is the pathwise cardinal certificate. Rectangle probability, density positivity, the exact radical, KL, and the optional waiting calculation are not formalized by this module and are reviewed by mathematical argument plus the separate deterministic controls.

## 8. Inspection, binding, and review time

The review read dependent-gate-transport/RESULT.md, same-threshold-replay/RESULT.md, and full-face-threshold-kl-rate/RESULT.md for the inherited observation and distribution contracts. It does not claim an independent bibliography audit of the named Joe family, or re-prove the predecessor's full-face asymptotic KL theorem.

The final source-audit, boundary-control, and reader-guide metadata were also inspected. Independent import-inventory replay reproduced all 1,798 imported module names. Every one of the 3,596 imported source and binary files and all 11 compiler/runtime/metadata bindings were individually rehashed and matched. The mathlib checkout commit matched the declared identity. The author's external Theis attribution was read as reported scope, not independently retrieved in this review.

FINAL_ARTIFACT_BINDINGS.json records the final author artifact hashes reviewed. REVIEW_MANIFEST.sha256 binds this review's own artifacts. RESEARCH_EVENTS.jsonl records prospective active proof-review intervals; report packaging and waits are excluded from active review time.

Active independent review time: 436.719 seconds across 3 prospective intervals. This excludes waits and report packaging.
