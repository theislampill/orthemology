# Independent review of proper interaction moment likelihood closure

10 October 2026 UTC. Ordinary independent mathematical AI review of the specified frozen research packet. This is not a formal audit service, a formal-kernel certificate, an integration decision, a release authorization, or T20/programme closure.

## Result

No blocking mathematical defect was found in the categorical multiplier theorem, arbitrary-decoder normalized support-rank dichotomy, full-simplex versus full-support feasibility distinction, or the moment-image cone conclusion. The proofs work under their stated hypotheses. The channel-adapted repair works with the precise channel specified below. An explicit, source-faithful finite tensor realization is provided in this review; it does not identify interaction order with an undeclared semantic tensor degree.

Two small wording/scope clarifications should accompany reuse of the frozen text:

1. Corollary 3.2's “first-slot observables” means **first-order, or one-slot, observables across all slots**. Only observables of slot 1 would not separate product atoms.
2. The six-dimensional example in §7 means **nonconstant** L depending only on the first binary slot, with the multiplication operator D_L alone or the complete channel {L,1−L}. If L is constant the least enlargement has dimension four. Merely having one first-slot outcome in a larger, otherwise unspecified channel does not establish the six-dimensional answer.

Neither point changes a stated main theorem. They prevent incorrect readings of its explanation and its illustrative repair. The parent and author were notified; no frozen source was silently changed.

There is also a real reproducibility qualification. The original tensor packet binds an earlier cone report. That mutable cone path has since received two precision edits, so the original checker **fails its input gate against the current sibling path**. The unchanged checker passes all **13 author control groups**, reproducing the original output byte-for-byte, when run on the exact digest-bound cone bytes in the isolated replay tree. **12 independently constructed control groups** also pass. These are finite discriminating controls, not replacements for the general proofs and not an additive measure of proof strength.

## Frozen objects and dependency drift

The full RESULT reviewed is:

- Path: tensor-likelihood-closure-20261010/RESULT.md
- SHA-256: 4f5d51008ec623911221c23d685ce21e64c76d9cb6c1ef6c53877b802053fda9
- Size: 25,391 bytes

Every file listed in the author's manifest was hashed before and after replay. All six manifest-listed files match, and all seven files in the original directory, including its manifest, remain byte-identical. Eight of the nine declared external local inputs match their frozen bindings at the original paths. The sole drift is:

- Original bound cone RESULT: 28,789 bytes; SHA-256 e9f9a5465aa9f6f03f789f852e87a9847f4aa8b5641866b8c293ad2c9a1bb086
- Current cone RESULT: SHA-256 5c74c7086c038dce1be0e9098b42fce9cc4c7aee8670fe0ba682b50d780af5c0

The cone author reconstructed the older bytes by exactly reversing two recorded edits. The reconstruction matches both the original byte count and its pre-existing SHA-256 binding. This is a digest-verified reconstruction, **not a claim that an independently retained historical snapshot existed**.

I inspected and independently generated the complete text diff. It contains exactly:

- In the cone packet's compact-convex generation proof, supporting approximants are explicitly chosen in aff(Q)\Q, and the argument that the supporting face is proper is supplied.
- The Barnum–Wilce PDF link is pinned to arXiv version v1, matching the version already named in the text.

The tensor packet's moment cone is finitely generated directly by its specified columns, and its indecomposability proof is self-contained. It does not need the predecessor's compact-base extreme-generation argument. The two changes therefore do not alter the tensor conclusions. They do change the dependency identity and must not be hidden by a successful replay against substituted current bytes.

AUTHOR_REPLAY_RESULTS.json records both the observed current-path failure and the successful digest-bound replay. INPUT_BINDINGS.json records all reviewed file identities. DEPENDENCY_DIFF.patch records the independently regenerated two-edit delta. The author_replay tree contains the exact bound inputs and the unchanged author program. No original author or protected repository file was modified.

## Independent reconstruction of the central arguments

### The linear descent mechanism and its domain

Let M have full row rank with the all-ones mass row, and put A=MD_L. For d in ker M, mass(d)=0. Every full-support law p admits small positive and negative perturbations p+td that remain laws and have the same summary. If Ap is determined by Mp, then A(p+td)=Ap, hence Ad=0. Thus A vanishes on ker M and factors as A=TM. Conversely that intertwining supplies the decoder.

The row space statement is precisely LV⊆V. Including the mass row makes the first coordinate of Ap the branch probability. On an impossible branch, nonnegative L and p force D_Lp=0. Hence probability plus retained positive-branch posterior, together with the impossible-branch status, is equivalent to unnormalized descent.

This argument allows an arbitrary decoder from the start. It does not infer linearity merely from the decoder's notation. It proves that any successful arbitrary decoder of these linear outputs forces an underlying linear factorization on the whole ambient linear span. Full-support priors already suffice for this implication.

The mass row is load-bearing. For example, M=(1,2) without the mass row is injective on the two-state law simplex. For L=(1,2), a posterior decoder exists there, but MD_L=(1,4) is not a scalar multiple of M and the two supported columns differ. An ambient-kernel argument without mass control would wrongly test directions that do not preserve the simplex. The independent controls include this boundary.

### Proper binary and categorical multiplier algebras

For the binary case, 1∈V_k first forces L∈V_k. Given a nonzero nonconstant coefficient a_S, choose a disjoint T of size k−|S|+1. Multiplication by χ_T bijectively permutes Walsh coefficients by symmetric difference. Therefore the degree-(k+1) coefficient indexed by S∪T is exactly a_S and cannot be canceled. This proves that the stabilizing algebra is the constants.

For the full categorical case, it is important not to reuse the binary multiplication rule. Write the orthogonal decomposition into H_U, where H_U has zero-mean factors precisely on U. Choose a nonzero L_S with maximal interaction order d. Select disjoint T with |T|=k−d+1 and a nonzero pure product h_T of zero-mean factors. A term L_Uh_T can project onto H_(S∪T) only when U\T=S, because all factors outside T are unchanged. Thus U contains S. Maximality |U|≤d then forces U=S. The projected term is L_S⊗h_T and is nonzero.

This proof remains valid when dim H_i>1 and L_S is not a pure tensor. It uses tensoring with a nonzero vector, not a mistaken factorization of L_S itself. The condition |X_i|≥2 guarantees every needed H_i is nonzero. The cutoff is 1≤k<m; with singleton alphabets, nominal k<m may already include the full effective law space.

The independent categorical systems use mutually orthogonal integer contrasts h_j=(1,…,1,−j,0,…,0), different from the author's local contrast basis. Exact multiplier nullity is one for all tested proper orders on 3×3, 3×3×3, 2×3×4 and 2×2×3×3.

A more discriminating exact witness has three ternary slots, a=(1,−1,0), b=(1,1,−2), and R=a₁a₂+b₁b₂. Put

    L=1/2+R/16,
    p±=(1±Ra₃/8)/27.

The H_{1,2} component R has tensor rank two. All order-at-most-two marginals of the two positive priors coincide. L is strictly positive, both branch probabilities are 1/2, but their posterior expectations of a₃ are respectively 5/108 and −5/108. Local products genuinely differ from Walsh multiplication: a²=(2/3)1+(1/3)b, ab=a, and b²=2·1−b. The general projection proof and the exact witness both survive this distinction.

### Arbitrary nonlinear normalized descent

For a kernel direction d, set a=MD_Ld, b=Lᵀd, and q(p)=MD_Lp/(Lᵀp). If q is constant on each retained-record fibre, the equality for p and p+td cross-multiplies to

    a=b q(p)

for every full-support p. If some kernel direction has b≠0, this makes q(p) one constant vector over the entire full-support simplex. For each i with L_i>0, let p approach e_i through full-support laws. The explicit rational expression q(p), whose denominator tends to L_i>0, converges to c_i=Me_i. Consequently all supported columns must equal the same vector.

If those columns are not all equal, every b must vanish. Then every a vanishes too, which gives unnormalized linear descent. This establishes both directions of the support-rank dichotomy. No continuity, differentiability, measurability, or linearity of the decoder F was used. The only continuity invoked belongs to the explicitly given rational Bayesian map at an atom where the likelihood is positive.

Because the mass coordinate of every c_i is 1, equal supported columns are equivalent to rank(M|supp L)=1. Without the mass row, rank one and equality of columns are different conditions. A multi-state support exception really can occur for a general M: with rows (1,1,1,1) and (0,0,1,2), L=(1/4,3/4,0,0) always gives retained posterior (1,0), while equal-summary positive priors can have branch probabilities 1/4 and 3/16.

For proper product-marginal records, all one-slot observables together distinguish every pair of atoms. Thus the rank-one support case reduces to a singleton. Combined with the constant stabilizer calculation, this gives exactly positive constant or singleton-supported nonzero L. The all-zero likelihood is unnormalized zero descent and a vacuous posterior-only case, never a defined normalized posterior.

The independent script checks the full polynomial coefficient condition

    (MD_Ld)_j L_i = (Lᵀd)(MD_L)_{ji}

for a basis of ker M and every i,j, rather than sampling a few priors. It compares this exact condition against linear descent or support-rank one on six distinct summary spaces and 1,026 likelihood-grid cases. These include mass-only, repeated-column, nonpartition, partition, full-law, and 2×3 categorical-unary summaries. This is a finite check of the stated dichotomy's discriminators, not an exhaustive proof for arbitrary M.

### Feasibility and the prior domain

A singleton-supported branch always reveals its supported atom when possible. On the full simplex, feasibility is not determined by a proper marginal record: embed the binary even/odd parity pair on two selected values of each categorical slot, including the singleton atom. The proper marginals agree, while one prior gives that atom positive probability and the other gives zero. This confirms the packet's categorical boundary argument as well as the binary one.

On the full-support domain every nonzero nonnegative likelihood has positive branch probability. Feasibility then carries no extra information. The singleton exception remains a valid posterior-only decoder, even though its branch probability is still unrecoverable.

An independent 3×3×3 exact control uses h(x)=∏_i(1_{x_i=0}−1/3). Uniform laws perturbed by ±h/16 are both strictly positive and agree on all proper marginals. At the singleton (0,0,0), their probabilities are 1/18 and 1/54. The boundary parity pair instead gives probabilities 1/4 and zero. These are different output contracts, not competing answers to one contract.

For a complete channel whose every posterior row descends, each nonzero row is constant or singleton-supported. Pointwise channel normalization forces the total singleton mass to be the same at each latent atom, after subtracting all constant-row probabilities. The erasure-or-revelation description is therefore correct. It is a posterior-only classification; it does not make singleton outcome probabilities available from proper moments.

### Moment cone rigidity and the needed ambient lift

The moment-image cone K=M R_+^X is finitely generated, closed, pointed, and spanning. Its mass coordinate is strictly positive on nonzero elements: any nonnegative representing vector with zero mass is zero. For k≥1, the sum of unary mismatch indicators against a chosen atom x is a cone-nonnegative linear functional that vanishes on exactly c_x. Hence each specified latent column spans an exposed extreme ray.

If both T and I−T are K-positive, decompose c_x=Tc_x+(I−T)c_x. Extremality forces Tc_x=L_xc_x with 0≤L_x≤1. This is the required passive ambient lift TM=MD_L. The constant-stabilizer theorem then gives L_x=c and T=cI, since the columns span the whole reduced space.

A nontrivial cone direct sum would supply a nontrivial idempotent projection P with P and I−P positive. A scalar idempotent is only zero or identity, yielding the indecomposability contradiction. No unproved converse theorem from the cone predecessor is needed for this direction. For k=m the evaluation matrix is invertible; K is an orthant image and each atom ray is a separate component. Direct exact lift-equation systems confirm dimensions one at proper order and |X| at full order in categorical examples.

The exposed-column premise cannot be dropped when moving between an intrinsic feasible cone and a specified original hidden-state model. In the three-state segment with rays v=(1/2,1/2,0) and w=(1/2,0,1/2), the intrinsic projection onto v is positive with positive complement. Its actions on v and w would require the same original coordinate's likelihood L₁ to be both one and zero. It has no passive diagonal lift. Independently, diagonal maps preserving the cone satisfy L₁=L₂=L₃. This supports the packet's distinction between the moment-image cone with its given generators and an arbitrary restricted-prior cone.

For instruments, the conclusion requires Σ_yT_y=I as linear maps. Mere mass preservation or an arbitrary state-changing reset is insufficient. This is an exact order-theoretic property of the declared numerical state cone, not a statement about physically available measurements or ontological composition.

### Channel-adapted enlargement

For a single nonconstant binary-slot likelihood L=a+bχ_{1}, b≠0, multiplication by L generates the same invariant space as multiplication by χ_{1}. Starting from span(1,χ₁,χ₂,χ₃), the least invariant closure is

    span(1,χ₁,χ₂,χ₃,χ₁χ₂,χ₁χ₃).

Necessity of the two extra coordinates follows by subtracting the a multiple from Lχ₂ and Lχ₃ and dividing by b. Multiplying these six basis elements by χ₁ permutes them, proving sufficiency. Multiplication by 1−L preserves the same span, so this is also the least invariant closure for the complete two-outcome channel {L,1−L}. Neither χ₂χ₃ nor χ₁χ₂χ₃ is required by that channel and initial output contract.

The independent script discovers the span by exact row-space iteration, obtains the dimension path 4→6, explicitly derives both reduced branch matrices, and checks their intertwining for all 31 words of length at most four. This establishes the example's actual channel mapping, beyond merely listing six Walsh masks.

The repair is inherited finite-instrument closure applied to this passive channel. It does not prove closure for extra channel rows or a broader future observation repertoire. A constant L gives no enlargement. These qualifications are why the short wording clarification in the result section matters.

## Actual mapping to the inherited tensor formalism

The categorical evaluation construction in the frozen report is mathematically legitimate, but it should not be conflated with an automatic map from arbitrary semantic episodes. The following explicit finite construction supplies the precise crosswalk.

For each declared slot i, let E_i be the free real vector space on X_i, with basis e_a. A probability law is the coefficient tensor

    P(p)=Σ_x p(x) e_{x₁}⊗⋯⊗e_{x_m} ∈ ⊗_i E_i.

The augmentation ε_i(e_a)=1 contracts an omitted slot. Contracting all slots outside S gives the ordinary marginal coefficient tensor on S. An observable product ∏_if_i(x_i) is the dual tensor ⊗_if_i∈⊗_iE_i*, and its pairing with P(p) is its expectation. This is precisely the coefficient-tensor/contraction mechanism in inherited H-formalisation §5, with its declared basis and augmentation, not a structure-free deletion operation.

Let H_i⊂E_i* be the zero-uniform-mean function subspace. For S={i₁<⋯<i_d}, define

    z_S(p)∈⊗_{i∈S} H_i*

by z_S(p)(f_{i₁}⊗⋯⊗f_{i_d})=E_p[∏_{i∈S}f_i]. Finite-dimensional duality gives this identification; z_empty is mass. The tuple of z_S with |S|≤k has exactly the coordinates M_kp in chosen local bases.

To realize it in the inherited typed tensor algebra, declare a distinct numerical slot type with vector space Q_i=H_i*. Put Q=⊕_iQ_i. Embed each z_S into the typed-word summand Q_{i₁}⊗⋯⊗Q_{i_d} of T(Q), using the increasing slot order as an explicit declaration. Then

    ρ_k(p)=Σ_{|S|≤k} j_(i₁,…,i_d) z_S(p)

is a finite element of the algebraic direct sum, with grades at most k. This is a representation of the specified numerical moment record. It is not an assertion that differently ordered semantic words are identical. It requires no infinite completion and no symmetry assumption between distinct slot types.

Two cautions are decisive:

- The complete probability tensor P(p) always has m coefficient factors; its tensor order is not the cutoff k of its retained contractions. The parity difference can have tensor rank one while having order m and being invisible to all proper marginals.
- Pointwise multiplication of observables does not equal concatenation in the free tensor algebra. Repeated factors from one categorical slot can produce both constant and centered terms. Even in the binary case, χ_i²=1 in the function algebra, whereas a concatenated word (i,i) has free tensor degree two. Consequently the stabilizer theorem is about the represented observable algebra, not a free-tensor-algebra multiplication theorem.

When descent holds, the unnormalized map is represented by the declared linear T on the retained coordinates; its normalized version is generally rational on the admissible moment image. When descent fails, no update of that same record can reproduce the specified retained output for all priors. The fibre criterion, not the tensor notation, decides adequacy. The six-dimensional enlargement gives a concrete successful replacement for its one declared channel.

The independent controls check every marginal contraction and its moment pairing on a 2×3×2 coefficient tensor, verify the finite typed-word set through order two, and reproduce the rank-one order-three parity difference annihilated by all proper moment rows. This verifies an actual numerical mapping. It supplies no map from unspecified real episodes, no empirical adequacy claim, and no claim that the original full semantic record channel can be deleted.

## Inheritance and source scope

The retained H-formalisation passages inspected include the typed algebraic direct sum, the warning about semantic word order and workflow multiplication, Theorem 4.2's fibre criterion, the parity coefficient tensor, and augmentation contraction. The retained H-ICS observation-congruence passage supplies the deterministic invariant-fibre and kernel mechanism. The retained H-Continuation action–observation section supplies the increasing observable span, least invariant closure, exact intertwining, and normalization only on positive branches. These inherited results were not recast as novel claims of this packet.

The earlier tensor-moment report uses symmetric powers of one numerical vector type and controlled exponential tilts. Its first-order affine-independence theorem concerns all directions of that different update family. The present proper product-slot interaction cutoff and one-likelihood classification are distinct declared hypotheses. The audit-continuation report already supplies the moment-image cone and distinguishes posterior-only outputs from probability-plus-posterior outputs with a separate feasibility guard. Its paired-law tensor criterion does not itself provide a one-law closed filtering statistic.

I read those relevant retained passages and the original result in full, and inspected the bounded prior tensor review. This is not a complete priority search through all project files or a remote recertification of the repository commit tree. File hashes bind the concrete local inputs actually available. Source roles are retained: elementary factorization and invariant closure are inherited mechanisms; the present proper-interaction stabilizer calculation, support-rank specialization, and concrete cone transition are deductions within this packet's declared model.

Targeted primary-source checks support the external attribution. O'Donnell's §1.3, Theorem 1.5 and Fact 1.6 supply the Walsh orthogonal basis and symmetric-difference multiplication used by the binary proof. This is standard ancestry, not evidence of a new general Fourier theorem. [Analysis of Boolean Functions](https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf).

Randriambololona's arbitrary-field convention, Definition 2.6 and Proposition 2.11 directly treat the componentwise stabilizing algebra and its disjoint-support decomposition. Taking the field to be R is consistent with those sections. The paper is ancestry for the algebraic object, not a claimed source for this exact Bayesian normalized-support lemma or a substitute for the positive-cone bridge proved here. [On products and powers of linear codes under componentwise multiplication](https://arxiv.org/pdf/1312.0022).

No field-wide first-discovery claim was assessed or conferred. No external publication is bundled or given a local-byte hash by this review.

## Reproduction and use

From this review directory:

    python3 independent_controls.py
    python3 replay_author.py --portable

The first writes CONTROL_RESULTS.json with 12 independent groups. The second validates the bundled author's manifest, runs the unchanged author checker against its bundled digest-bound dependencies, and rechecks its manifest. It should report 13 author groups. It deliberately makes no claim about current outside paths.

In the original workspace, python3 replay_author.py without --portable also records the specific current-path dependency drift and regenerates the isolated snapshot replay. That mode is a workspace-specific diagnostic and expects the separately identified current cone and reconstruction paths. It is not the portable archive command.

MANIFEST.json binds this review's top-level artifacts and the full portable author_replay tree. File-hash checks detect byte changes; they do not themselves establish theorem validity. The written reasoning supplies the general argument, while exact controls test the important discriminators.

Keep the full prior domain, mass-row convention, nonnegative likelihood assumption, support behavior, output contract, and operation class attached to every use. No statement here establishes finite-precision efficiency, sample complexity, psychological architecture, physical realizability, actual observation, source truth, epistemic warrant, permission to act, or programme closure. No protected source edits or integration were performed.
