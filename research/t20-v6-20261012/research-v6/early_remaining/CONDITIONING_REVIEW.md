# Independent ordinary-proof challenge: joined conditioning budgets

Reviewed candidate SHA256: 602825b4b9fe359286bd619a9b7a86bcb9a54f237c97f2d4b51b8dbde6ba7b18, root_math/CONDITIONING_CROSS_CONTRIBUTION.md, full body. Also read original Pro1 source8aad39f6… lines244–268 and Pro2 sourcec2ca691c… lines199–255 and450–478. Source hashes are independently checked via the catalogue. This is ordinary mathematical review, not Lean verification or a novelty finding.

## Verdict

The sharper common-factor bound, joint origin/factor bound and bounded-observable transport consequence are valid under their displayed hypotheses. One boundary qualification in the sharpness fixture needs repair: `0<=delta<=alpha<=1` includes alpha0, where the two event masses vanish. State `0<alpha<=1` and `0<=delta<=alpha`. The main theorem already requires both masses positive, so this is a fixture-domain error, not a counterexample to the theorem.

## Direct argument check

Assume A>=B>0 and let S contain the positive coordinates of Lp/A−Lq/B. Then summing over S gives

TV=(1/A)sum_S L(p−(A/B)q) <=(1/A)sum_S L(p−q) <=(1/A)sum(p−q)_+ =delta/A.

No missing factor two appears: TV is the positive signed mass, equivalent to half the l1 norm for probability vectors. The A/B subtraction has the right sign because q and L are nonnegative. The last inequality uses L<=1, including zero likelihood entries. Swapping the laws handles B>A. The measure extension follows using p+q as dominating finite measure, a measurable positive-density set, and exactly the same signed-integral argument. Both normalizers must remain positive.

For a bound based only on A,B>=alpha, the four-state fixture attains delta/alpha throughout 0<=delta<=alpha with alpha>0. The claimed clipped sharpness at delta>=alpha can be made explicit, avoiding an existence assertion without a displayed model:

p=(1−delta,delta−alpha,0,alpha,0),
q=(1−delta,0,delta−alpha,0,alpha),
L=(0,0,0,1,1), 0<alpha<=delta<=1.

Both laws are probabilities, both accepted masses are alpha, priorTV=delta, and posteriorTV=1. This establishes the entire sharp uniform-alpha envelope. It does not assert pointwise sharpness for every prescribed unequal pair(A,B).

For the factor comparison, apply Pro2 D to nu=B_L q and r=M/L on L's positive support. The same zero support and strictly positive finite ratio bounds guarantee that the relevant normalization is finite and positive. M itself need not be bounded by one. The exact Pro2 proof uses the chord bound for |r−mean r|, then optimizes the mean at sqrt(ab). When a=b the normalized factor is constant and distance zero. Inserting the intermediate B_L q yields the stated triangle bound and clipping at one. The sum need not be jointly attained; that limit is correctly retained.

The transport consequence uses a common bounded observable whose range oscillation is R on the relevant union of endpoint ranges, and uniform displacement epsilon on the origins being integrated. One term changes posterior law under a fixed endpoint map, the other changes endpoint map under a fixed posterior. This proves R*posteriorTV+K*epsilon without implying small TV between nearby distinct point masses. Fixed common Markov postprocessing contracts TV. Policy-dependent/source-dependent kernels do not inherit that contraction argument without a separate common-kernel or replay condition.

## Independent exact controls

replays/check_conditioning_independent.py passed136 five-state delta>=alpha attainments,66 exact ratio-factor attainments using squared rational endpoints, and rare-event/zero-normalizer controls. Results: replays/CONDITIONING_INDEPENDENT.json. These are independently coded finite controls, complementary to the root's25,008 common-factor grid cases. Universal validity is established by the preceding proof audit rather than by enumeration.

## Relation to early-prior results

This is fully compatible with the reviewed early lifetime discontinuities. A bounded per-horizon count contributes N*posteriorTV; that coefficient grows with horizon. Infinite literal count is not a bounded observable with fixed R. The early nonconvexity and contamination constructions therefore do not refute the bound; they demonstrate why a uniform tail/integrability assumption is needed to pass the infinite-horizon limit. A source-faithful scalar posterior bound does not establish the correctness of the source likelihood or the latent criterion itself.

## Corrected candidate recheck

The complete revised candidate SHA2568390b2384bf91469c868d910eb257426e3488011d904e228f7f8f46d61dcb02e was reread. It now requires alpha>0 and adds the five-state clipped-bound sharpness fixture. The identified boundary qualification is resolved. The scoped ordinary-proof verdict is ACCEPTED; no Lean or joint-sharpness claim is added.
