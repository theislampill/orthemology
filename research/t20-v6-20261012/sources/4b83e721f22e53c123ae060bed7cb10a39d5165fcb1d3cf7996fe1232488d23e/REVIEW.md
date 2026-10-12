# Independent review of event-feasibility descent

10 October 2026 UTC. Ordinary independent mathematical AI review of the frozen `event-feasibility-descent-20261010` packet. The reviewer did not edit or execute the original author directory. This report is not a formal-kernel certificate, historical novelty assessment, empirical validation, integration decision, or T20/programme closure.

## Verdict and exact objects

No blocking mathematical defect was found. On the entire finite probability simplex, the support-face classification is correct under mass retention and nonnegative likelihood. The proof handles duplicate and nonvertex supplied columns, the empty/full support endpoints, and arbitrary decoders. The distinction among feasibility, probability, and retained normalized posterior is preserved. The global-facet and unrealizable-correlation countercontrols are correct, and they do not contradict the inherited exponential-leaf theorem.

The reviewed author objects are:

- RESULT.md: 20,422 bytes; SHA-256 `cb94649fa0e055d2ad405795470e280f5e0092291d0973ea334abb0613628852`
- verify.py: SHA-256 `d1a7dabfce68c13f270eedfe74c5801326c71e2628d64310d670ef19dc5d858a`
- MANIFEST.json: SHA-256 `e59653011c126a8d0ad0c8d2875adbd0b6b510c722af304d9076f963f8fa55c5`

All author-manifest entries and all three direct input bindings were checked. The unchanged author program ran in an isolated copied tree and passed all 29 assertion groups: 304 support patterns, with 252 exact support certificates and 52 explicit opposite-feasibility fibre witnesses. Its regenerated JSON and complete stdout are byte-identical to the author's recorded files. The separate reviewer program passed 29 independently constructed exact control groups, including 20 selected parity supports. These counts describe bounded test coverage, not an additive measure of theorem strength.

## 1. Reconstructed equivalence and saturation

Write P=conv{m_x}, Z={x:L_x=0}, S=X\Z, and F=conv{m_z:z∈Z}. Because L≥0, a prior has zero likelihood expectation exactly when it is supported in Z. Feasibility descends if and only if every representing probability law over a point of F is supported in Z: one Z-supported representation exists, and equality of the coarse record must preserve its zero status. Conversely, if one member of a fibre is impossible, this property makes every member impossible.

This preimage property implies that F is a face. If t a+(1−t)b∈F with a,b∈P and 0<t<1, choose laws representing a,b. Their mixture represents a point in F and is therefore supported in Z. Nonnegativity and strictly positive mixture weights make both constituent laws Z-supported. Hence a,b∈F. It also implies saturation: the point mass at any supplied column lying in F must be Z-supported.

The reverse implication is equally necessary to check. A convex representation of a point of a face can assign positive weight only to columns in that face, by isolating each positive coefficient in the face definition. Saturation then forces all such indices into Z. Thus having a face as the convex hull of the zero columns is not enough unless all supplied columns on that face are also zero-likelihood.

This correctly retains duplicate and nonvertex columns. Opposite zero/nonzero statuses at duplicate columns violate descent by their point masses. A nonvertex supplied column in a face is as compulsory as a vertex. For example, a midpoint with positive likelihood and two zero-likelihood endpoints gives a same-record feasible point mass and impossible endpoint mixture. The independent controls additionally use a triangle with edge-interior and strict interior columns, rather than only the author's collinear example.

## 2. The finite exposing-functional proof

The direct proof does not smuggle in strict separation of sets that may touch. Let W be the linear span of the zero columns, Q the orthogonal projection to W⊥, and K=conv{Qm_s:s∈S}. If 0∈K, a probability-weighted sum of S-columns equals a real linear combination Σ_z b_z m_z. Applying the mass covector gives Σ_z b_z=1. Splitting b into its positive and negative parts then produces two nonnegative combinations with the same positive total mass A=1+Σ_z b_z⁻. After division by A, one is Z-supported while the other gives S positive mass. That contradicts the already established preimage property.

Since K is a finite convex hull and excludes zero, its closest point a to zero exists, is nonzero, and lies in W⊥. Differentiating squared distance along each segment from a to k∈K gives a·k≥||a||²>0. Hence a·m_z=0 on Z and a·m_s>0 on S. The vector v=Mᵀa is nonnegative, belongs to the retained row space, and has exactly support S. Conversely any such v determines feasibility by 1_{a·Mp>0}, since two nonnegative functions with the same support have the same zero-expectation laws.

This verifies both strict positivity on all supported columns and exact vanishing on all zero columns. No regularity assumption on the proposed decoder is required. A witness determines the indicator, not the magnitude of L or its expectation.

The two endpoints need separate conventions and are correctly supplied: L=0 uses v=0 and F=P; a strictly positive L uses v=1 and the empty zero face. The empty face is not falsely described as a nonempty minimizing set. Full row rank removes redundant coordinates but is not mathematically essential. Independent controls scramble the displayed record coordinates so that no row is literally all ones, then append a redundant row; the certificate survives both operations.

Mass retention is essential to the stated linear row-space criterion. With M=(0,1), the normalized prior is affinely recoverable from p₂, so positivity of p₁ is known, although no multiple of M has support {1}. Nonnegativity of L is essential to the support argument: a signed likelihood can cancel to zero on a strictly positive law. On strictly positive priors alone every nonzero nonnegative L is feasible, so the all-simplex theorem must not be read as a nontrivial interior-only classification.

The finiteness restriction is respected. In particular, compact convex sets may have nonexposed faces, and projection of an arbitrary infinite set need not give the compact finite hull used here. This review approves no arbitrary-compact, cone, or measure extension of the iff.

## 3. Information contracts

Probability descent is the different condition L∈row(M). For any kernel vector d, mass retention gives Σd=0, so small perturbations of a positive law in direction d remain laws. Fibre constancy of Lᵀp forces Lᵀd=0; row/kernel duality gives the condition. This is stronger than existence of some same-support retained v.

The inherited probability-plus-posterior condition is M diag(L)=T M. It is stronger again. The normalized-only inherited dichotomy permits either that factorization or equality of every supported supplied column. Combining it with the new feasibility condition is logically valid. It does not manufacture probability information from support information.

Duplicate endpoint columns make this distinction substantive: the record can identify membership of the endpoint face, and every positive posterior can have the same endpoint record, while different positive likelihood weights on duplicate atoms give different branch probabilities. Duplicate columns at an interior point provide the converse adversarial distinction: the supported posterior record is still constant, but an endpoint mixture with that record may be impossible. Our independent controls check both cases.

## 4. Pairwise event and parity controls

For three binary coordinates, q=(1+xy+xz+yz)/4 is exactly the indicator of the two all-equal atoms. Its nonnegative retained formula certifies feasibility for every likelihood positive precisely on those atoms. Starting directly with the probability-valued likelihood L̃=3q(1+x/3)/4 gives values 1 at +++ and 1/2 at ---. Its cubic Walsh coefficient is 1/16, so its probability is unretained.

The full-support parity perturbations p±=(1±xyz/2)/8 share the entire pairwise record. Their event probabilities are 7/32 and 5/32; their posterior unary means are respectively 5/7 and −1/5; all posterior pair products equal one. Thus retained feasibility coexists with failures of both probability and retained-posterior descent. The author's unscaled likelihood has probabilities 7/24 and 5/24 and is correctly described as a likelihood weight until rescaled.

With q itself the two event probabilities both equal 1/4, while posterior unary means are ±1/2. With the singleton event +++, positive-branch posterior is constant, while the boundary parity laws disagree on whether the event is possible. These controls distinguish three genuinely different contracts.

For the seven-row pairwise matrix, the only kernel direction is parity h=xyz. A nonnegative row-space vector supported on nonempty S exists exactly when S meets both parity signs. A direct witness assigns to each supported positive-parity atom the number of supported negative-parity atoms and conversely; its parity inner product is zero. If S is confined to one sign, the two boundary parity laws explicitly disagree in feasibility. The resulting count is 256−2(2⁴−1)=226 feasible supports. The independent program checks a bounded selection with explicit certificates or explicit colliding laws, without importing the author's search or inferring impossibility from an unsuccessful search.

## 5. Global facet and local-potential obstruction

The pairwise matrix has rank seven, while its six q-zero columns have rank six. As mass is fixed, the global polytope has dimension six and this exposed face has dimension five. It is therefore a facet, rather than only some unspecified boundary subset.

Every assignment on every scope of size at most two occurs among the six q-zero atoms. If q were a sum of nonnegative functions on those scopes, each summand would have to vanish at every zero atom. Full projection of the zero set to each scope would then force every summand to vanish identically, contradicting q(+++) = 1. This argument also excludes any nonzero nonnegative-local sum having exactly the same support. Signed local terms are allowed in q's displayed formula; the obstruction is to individually nonnegative summands.

The uniform law on the six zero atoms has zero unary means and pair correlations −1/3. Every pair table nevertheless has same-sign cells 1/6 and opposite-sign cells 1/3. These locally strictly positive marginals represent a globally compatible boundary point. The facet equation forces any joint representation onto those six atoms, and the rank-six submatrix then makes the representation unique.

For any full-support reference and finite exponential parameter, every atom has positive probability, so the expectation of q is strictly positive. This excludes the displayed boundary record. For the uniform reference, the tilt exp(−t(xy+xz+yz)) tends to the uniform six-zero law only as t→∞. In the independent rational reparametrization a=exp(−4t)>0, E[q]=a/(3+a)>0 and tends to zero only as a→0. Finite-precision underflow is not mistaken for exact boundary membership.

## 6. Locally valid but globally unrealizable control

At three proposed correlations −2/5 and zero unary means, each pair table has same-sign cells 3/20 and opposite-sign cells 7/20, agreeing on uniform unary marginals. The proposed 3×3 correlation matrix is positive definite. Independently of the author's eigenvalue calculation, its leading principal minors are 1, 21/25, and 49/125, all positive.

However the proposed record evaluates the retained nonnegative q at −1/20. Therefore no joint binary law realizes it. This is stronger than the compatible-boundary example, but it is a classical marginal-polytope obstruction. The proposed matrix must not be called the covariance of an actually existing law with these moments, nor identified with the six-statistic exponential-family Hessian.

The leaf theorem already requires the actual global moment-polytope interior. These examples refute a possible substitution of local table positivity or proposed covariance positivity for that premise. They do not identify an error in that theorem, establish a failure of an actual DAEE implementation, or provide a field-novel discovery.

## 7. Inheritance and reproducibility boundaries

The following original passages and their review reports were inspected directly:

- The hierarchical-marginal result §6 already gives normalized support-cylinder descent and the whole-versus-partial cylinder feasibility distinctions. It explicitly does not provide a broader feasibility classification. The general saturated-face classifier is not a duplicate of its common-core theorem.
- The tensor-likelihood result §§3 and 5 already gives unnormalized quotient descent and the normalized support-rank dichotomy. Its proper-product parity example excludes singleton-event feasibility. Those input theorems and parity mechanism do not earn new-result credit here.
- The leafwise result §3 identifies the positive image with the actual relative interior, and §6 proves the global finite-parameter mean theorem on that interior. The new local-positivity control is a crosswalk protecting the existing premise, not a correction.
- The openings of the finite and measure-valued Bayes-feasibility reports concern invariance of separately restricted classes of priors under likelihood updates. That use of “feasibility” is different from the present one-bit event-positive-probability output.

The tensor review records historical drift in an older cone dependency and a successful replay on digest-reconstructed old bytes. This event review checks the directly bound tensor RESULT and does not rerun or silently recertify that transitive dependency gate. Likewise, successful direct-input verification does not transfer all prior review status to this packet. No exhaustive repository or literature priority scan was performed.

The independent verifier uses exact rational arithmetic, matrix identities, symbolic rational limits, direct support certificates, and explicit colliding laws. It imports no author checker and uses no linear-programming answer or numerical optimizer. Tests support the calculations; the written argument establishes the general theorem.

ORIGINAL_PACKET_BEFORE.json and ORIGINAL_PACKET_AFTER.json bind all seven originally present target files and verify that they remained unchanged. The isolated replay contains the exact author files and all three required direct inputs. The review also preserves the additional inspected reports at their bound identities. `python3 verify_bindings.py --portable` checks the self-contained copies and review manifest; without that flag it additionally checks the original workspace paths. No source correction is requested. Any broader prior domain, output contract, or application claim needs its own review.
