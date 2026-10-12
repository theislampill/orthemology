# Actual P02 consumption and probability-carrying CV-O

## 1. Verified predecessor and exact evidence ceiling

The supplied file, despite the word “completed” in the continuation prompt, is the actual 4,192,393-byte checkpoint with SHA-256 `365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9`. Its receipt records **U05, U08, CV-R, CV-C and Q1c all PARTIAL**, no new kernel verification, eleven unexecuted theorem targets, and ordinary research supplied for review. P03 verified this ZIP, every member manifest binding, receipt outputs and schema, nested original archive, source Git/SHA identities and accepted evidence bindings. The outer detached P02 seal was not supplied; the new observed full-archive identity is recorded rather than pretending that an absent detached seal was checked.

The complete P02 ordinary statements and hypotheses are preserved verbatim in `inputs/P02_EXACT_RESULT_INTERFACES.json`, the five `inputs/p02-analysis/` files and the unchanged embedded ZIP. The statement-level map is `P02_P03_DEPENDENCY_MAP.json`. This document adds **P03 instantiations/proofs**, not a change to P02's statuses or a claim that its Lean candidates ran.

| P03 target | Exact P02 result | Actual reusable scope | Consequence |
|---|---|---|---|
| Declared model defect | U05 P02-M01 and P02-M04 | Positive singleton mass and finite/countable mixture affinity, under measurable-singleton hypotheses | Exact finite and tagged-interval calculations below; ordinary dependency discharged. |
| Rich-event tolerance | U05 P02-M02 | Full measurable event repertoire and measurable intersections, not arbitrary countable predicate lists | The Engine's explicit `events=full-measurable` field fixes the contract; it does not verify a real data source. |
| One-step refinement | U05 P02-M03 | Measurable coarsening, positive fibres and their normalised restricted laws | Returned positive-fibre weighted sum has its stated measure meaning; ordinary dependency discharged. |
| Finite revision debt | CV-R P02-R02 and P02-R07 | Exact finite telescope and budget slack | A lawful finite refinement path charges all increments; versions remain an additional guard. |
| Infinite-history extension | CV-R P02-R01/R03/R04/R06/R07 | Decreasing measurable cells, residual J and full-history hypotheses | Conditional inheritance; finite acceptance alone does not discharge J. |
| Probability-carrying outcomes | Q1c section 2, **not a fabricated theorem ID** | Finite nonnegative normalised tables, fibre-sum pushforwards and row-normalised kernels | Coupled finite histories admit the explicit sum proof below. Q1c's parity theorems are not needed. |
| Fixed points/convergence | U08 P02-F01–F04 | Restricted finite row-set proposal; no general iteration or computable-sampler guarantee | No fixed-point algorithm appears in the engine. These formal gaps are not CV-O prerequisites. |
| More general observer certification | CV-C P02-C04 | Finite Mealy machines under IID fair bits; exact deterministic-state hitting probability | Optional different model only, not the deployed binary-tape invariant checker. |
| General PR observer classification | CV-C P02-C-SYNTAX-01, C01–C03 | Numbering-specific ordinary hierarchy; concrete codec/compiler still absent | Unsupported extension, not a blocker for the existing finite grammar. |
| Guarded VCT | Q1c P02-QC01/QC02 | Separate parity/mixture examples | No Q1f prerequisite. P02's partial Q1c cannot be used to block or advance the guarded-version base. |

Each row is bound to its exact member SHA-256 in the JSON map. No required **ordinary finite-engine** dependency is left at `WAITING_ON_P02`. No new P02 kernel import is claimed.

## 2. Actual concrete measure grammar

A successful `observations.check` request has exactly the fields `space`, `law`, `weights`, `view`, `events`. The event field is literally `full-measurable`; the law field is a bounded nonempty identity string. There are 1–64 components. Each weight is an exact nonnegative [0,1] rational pair with numerator/denominator bounded by 128 bits, and the running exact sum must stay within the separate 256-bit arithmetic budget and finish at one. Those are computational constraints, not assumptions that arbitrary real measures have finite descriptions.

### Finite-program carrier

Let I={0,…,k−1} with mass w_i at i. A view assigns a finite label v_i∈{0,…,4096}. Its pushforward has mass

    ν({a}) = Σ_{i:v_i=a} w_i.

It has finite support, hence total positive singleton mass one and defect zero by M01. Calling these labels “programs” does not prove that an externally supplied label denotes a well-typed physical computation; that separate interpretation is not needed for the finite measure calculation.

### Tagged uniform intervals

Let X be the disjoint union of k tagged copies `{i}×[0,1)`, with probability w_i times Lebesgue measure on copy i. Tags remain part of the outcome, so coincident real coordinates in different components are not identified. For view v_i:

    v_i = -1: output (i,x), retaining the real coordinate;
    v_i = 0 or 1: output one tagged constant;
    v_i = m ≥ 2: output (i, floor(mx)), one of m equal-width bins.

Use the corresponding disjoint measurable output carrier with measurable singletons. A retained real coordinate is atomless; a finite-bin output has total atomic mass w_i. M01/M04 therefore give

    d(view) = Σ_{i:v_i=-1} w_i.

This is the exact expression calculated by the implementation. Views are restricted to −1…128 and the number of finite coarse bins to 256. Zero-weight components remain syntactic components even though they have no measure mass.

The fingerprint is the SHA-256 of canonical declared-specification bytes. It is a custody key, not an injective mathematical encoding of all measures or independent authentication of a source. For example view 0 and view 1 have the same semantics but different specification bytes; semantic equality does not cancel version/custody checks.

## 3. P03-A2-PROB-MODEL — one-step soundness and exact conditional fibres

Suppose the concrete refinement call succeeds. The carrier, law label and **normalised weight tuple** must match. In the finite case the implementation checks every pair of rows with equal fine label has equal coarse label, including zero-weight rows. Thus a function h is well-defined on the finite fine-label image by h(f_i)=c_i and can be extended arbitrarily off the image. Its pushforward is the coarse law. Every positive coarse atom has a finite conditional law and conditional defect zero.

In the interval case, success imposes per component:

* A fully revealed coordinate remains fully revealed.
* A coarse constant (0 or 1) permits any finer view.
* A coarse m-bin view, m>1, permits full revelation or a positive multiple n of m bins.

For finite bins n=qm, h(i,j)=(i,⌊j/q⌋); for full revelation h(i,x)=(i,⌊mx⌋). These measurable functions commute **pointwise** with the two views. When the coarse component was already atomless, its mass is already in d_coarse and it has no positive coarse singleton to sum. When coarse view is m bins (m=max(v_i,1)), each positive coarse atom has weight w_i/m. Its conditional fine law is atomless exactly when the fine view reveals x, and otherwise finite. Therefore M03 gives precisely

    d_fine = d_coarse + Σ_positive_coarse_fibres weight × conditional_defect.

The returned list contains exactly these positive atoms, not normalised zero-mass fibres. Its `increment`, both defects and equality flag follow by exact rational arithmetic. If an intermediate rational exceeds a bound, the call refuses instead of returning an approximate or false identity.

### Strong converse deliberately not asserted

**P03-A2-CE-AE-COMPLETENESS.** Weights [0,1], coarse [2,0], fine [3,0]. The only positive component is constant in both laws, so a coarse-factorisation exists almost surely. The source rejects because three bins do not pointwise refine two bins on the zero-weight component. Thus the grammar is a sufficient **pointwise** refinement contract, not a complete decision procedure modulo null sets. This does not refute M03, which remains true for its own hypotheses.

**P03-A2-CE-ARITHMETIC-COMPLETENESS.** Let p_1=2^89−1, p_2=2^89+1 and p_3=2^89+3. Use weights 1/(3p_i), followed by (p_i−1)/(3p_i), for i=1,2,3. Each input pair is within 128 bits and the total is one, but grouping the three small terms first creates a reduced running denominator above 256 bits. Interleaving each small term with its complement cancels to successive multiples of 1/3 and passes. Assign all finite views the same label: the two successful mathematical specifications describe the same point mass. A logical-work refusal is not a semantic nonexistence result, and reordering invariance of **acceptance** is false at these literal budgets.

These two countermodels finish the strongest-correct-result analysis rather than weakening either gate to force a converse.

## 4. P03-A2-PROB-BUDGET — finite debt and operational currentness

For successful comparisons along a fixed-law refinement chain v_0→…→v_n, section 3 and R02 yield

    d_n = d_0 + Σ_{j<n} Δ_j,     Δ_j ≥ 0.

Under the declared rich measurable-event contract M02/R07, a final tolerance ε is met iff d_n≤ε, equivalently the finite accumulated debt is at most ε−d_0. The implementation uses the closed threshold: equality passes. This is not the strict-threshold CV-C classifier and does not silently change its comparison sign.

At admission, `certify` computes that condition for each actual requirement, then records the requirement and model stamps. On a successful refinement **or coarsening**, a new stamp is installed. Any affected old record becomes stale regardless of whether the numerical tolerance remains true. Revalidation replays the immutable source under the new requirement/model; neither unchanged bytes nor an easier tolerance alone supply current authority.

The executed example uses weights 1/4,3/4, coarse views [0,2], fine views [−1,4], and ε=1/4. It reports d_0=0, Δ=d_1=1/4. The old licence becomes stale; a new revalidation succeeds at equality. Coarsening makes both older handles stale again, and a further new admission succeeds. This instantiates both the semantic and operational sides, not just a standalone arithmetic identity.

## 5. P03-A2-PROB-PUSH — probability-carrying history refinement

### Finite joint-law theorem

Let Θ be a finite set of fully declared environment transcripts: captured inputs, entropy draws, revision/scheduler choices and permitted failure choices. Assign nonnegative masses p(θ) summing to one. Let C(θ) be the concrete observed history and A(θ) its constructed abstract replay, and let α erase only the explicitly hidden implementation coordinates. Assume the pointwise operational theorem gives

    α(C(θ)) = A(θ)

for every θ with positive mass. Include refusals, pending and postcommit-indeterminate outcomes in the observation alphabet. Then for every observation y,

    Pr[α(C)=y] = Σ_{θ:α(C(θ))=y} p(θ)
              = Σ_{θ:A(θ)=y} p(θ) = Pr[A=y].

This uses Q1c's exact finite-table interface; equality of the index sets is the proof, not an assumption of equal output probabilities. A transition-kernel version follows by induction: if each coupled next-step kernel agrees on abstract images and the initial masses agree, summing over previous states and next outcomes preserves the joint prefix law. The proof needs either a common conditional environment kernel or an explicitly coupled scheduler. Arbitrary demonic trace inclusion is not enough.

**P03-A2-CE-TRACE-LAW.** Two processes both have possible outputs {0,1}; one gives masses (1/2,1/2), the other (3/4,1/4). Their support sets and possible one-step traces agree, but their output laws do not. Thus the concurrency theorem's existential abstract replay must be selected using the same input/environment transcript, not silently endowed with an unrelated probabilistic policy.

### Conditioning/refusal theorem

Let S be the measurable event of a successful observed result and p_S=Pr(S)>0. Equality of the full outcome laws yields equality of the conditional laws

    Pr[Y∈E | S] = Pr[Y∈E and S] / p_S.

At p_S=0 no normalised conditional-success probability is asserted. Dropping refused runs and renormalising without disclosing p_S changes the question. The actual executed example gives X masses 1/2,1/3,1/6 and an explicitly independent revocation flag of mass 1/4. Refusal mass is 1/4; success mass is 3/4; conditional successful outputs 1,2,3 retain masses 1/2,1/3,1/6. The unconditioned success masses are 3/8,1/4,1/8. These are exact finite observations from the proposed engine, not assertions that a real scheduler or source is independent.

### General measurable histories

Let (Θ,μ) be a specified probability space and C,A,α measurable maps into specified history spaces. If α∘C=A on a measurable full-measure set, the pushforward measures agree because inverse images of each measurable event differ only on that null set. This is a new P03 ordinary derivation; M01/M03 supply subsequent singleton-defect/coarsening consequences at their own measurable-singleton/fibre hypotheses. P02 did **not** supply a mechanised theorem about this particular engine or verify a physical entropy/scheduler law.

For countable output alphabets the finite-sum proof extends by nonnegative countable sums; for arbitrary path spaces measurability is an explicit condition. A constructed abstract replay can include committed pending calls; a trace abstraction that hides them inconsistently with later `project` observations does not meet α∘C=A.

## 6. Infinite history: what the actual P02 result permits

A finite prefix theorem does not imply zero full-history defect. A sequence of finite-valued observations can have an atomless infinite output law. When the exact decreasing-cell/full-history hypotheses of R01/R03/R04 hold, the inherited law is

    d_infinity = d_0 + Σ_n Δ_n + J.

R06's tagged mixture gives total finite debt 1/3, J=5/12 and full defect 3/4. It is preserved predecessor evidence, not rerun as a new P03 example. Infinite acceptance at ε requires the complete inequality including J; there is no permission to erase J because every finite stage passed.

The engine's 10,000-revision cap does not itself bound the number of dispatch observations or encode a theorem about all possible infinite histories. U08's fixed-point existence is not a replacement for such a theorem, and CV-C's finite-Mealy algorithm is not a generic classifier for binary-tape observers. The current finite engine makes none of those claims. A future infinite-law formal consumer must supply the stated measurable history model and, for a kernel claim, actual formal declarations. These are exact interfaces, not a broad unread-P02 dependency.

## 7. Evidence and remaining boundary

The new P03 experiment compares 6,480 tagged interval pairs, 729 finite-label pairs and 135 tolerance cases with independently structured mathematical oracles; all comparisons agree. It also executes the revision/conditioning examples and the null-component and rational-budget countermodels. Counts are finite evidence only. No P02 census is regenerated for credit.

All required ordinary finite-measure prerequisites have now been read, bound and instantiated. General measurable-history claims remain **conditional on their explicit measurable joint environment law**, as they must. No unproved P02 formal target is silently imported. External model identification, actual randomness, current authority and owner adoption remain outside a local mathematical certificate.
