# Probability coarse-graining and Bayes-compatible Bregman geometry

9 October 2026 UTC. Bounded T20 continuation; ordinary written proofs and exact symbolic/rational controls. No protected edits, integration, adoption, field-novelty claim, or programme closure.

## 1. Result and the preservation contract

The expanded repair family permits arbitrary coherent strictly convex potentials. Requiring a separately specified coarse-graining to contract its divergence is an additional, nontrivial condition. Ordinary Brier geometry, independently reset to unit coordinate weights after a lumping, fails it even on a statistically recoverable submodel. This does **not** contradict inherited preservation of distinctions: an injective representation can preserve its declared information while changing a numerical score.

A positive construction prevents an entropy-only conclusion. Transport a positive reference measure along with probability states. The reference-weighted quadratic Bregman geometry then contracts under every finite stochastic map. Three-object stochastic recovery of both laws and the reference guarantees equality. This is a conditional mathematical repair, not independent warrant for selecting that reference.

Two operations must remain separate throughout:

- **Fixed truth space, garbled evidence:** every convex coherent potential gives nonincreasing expected Bregman information under a fixed joint law. This holds for Brier.
- **Changed truth coordinates:** comparing the original potential with a newly selected potential on the lumped categories changes the scoring problem. Cross-space divergence/metric contraction requires an explicit transport contract and does not follow from Bayes-compatible normalization.

## 2. Exact contract and Hessian test

Let K be a nonnegative m-by-n column-stochastic matrix with no zero output row, so K sends positive probability vectors to positive probability vectors and preserves total mass. A deterministic lumping has exactly one unit entry in each column. Let f_n and f_m be differentiable strictly convex potentials on the respective open simplexes, and use the inherited orientation

    D_f(p,q)=f(p)−f(q)−df_q(p−q).

The proposed cross-space contraction condition is

    D_fm(Kp,Kq) ≤ D_fn(p,q)                         (C)

for all positive coherent p,q. This condition is additional structure, not a consequence of calling K a compression.

For C² potentials, (C) is equivalent to the **all-points tangent Hessian inequality**

    Hess f_m(Kq)[Kv,Kv] ≤ Hess f_n(q)[v,v]           (H)

for every interior q and every tangent v with Σv_i=0. Necessity follows by setting p=q+εv and dividing the divergence inequality by ε²/2 as ε tends to zero. Sufficiency follows from the exact segment integral

    D_f(p,q)=∫₀¹(1−t) Hess f(q+t(p−q))[p−q,p−q] dt.

Apply (H) along this segment and use linearity of K. A Hessian match at one point does not suffice. Equality of all divergences is similarly equivalent to equality of all these Hessian quadratic forms. For a genuine noninjective lumping and positive fine tangent metric, global isometry is impossible: a nonzero tangent v in ker K has zero coarse but positive fine norm. Equality is instead meaningful on a specified recoverable submodel or specified pair.

For the inherited ambient family F_n(sp)=s f_n(p)+a(s), use the **same radial potential a** on both spaces. The inherited identity gives

    D_Fm(K(sp),K(tq))=s D_fm(Kp,Kq)+D_a(s,t).

Thus full-cone contraction is equivalent to (C), by subtracting the shared radial term; the converse restriction follows already at s=t=1. No new radial restriction follows from this contract. Changing a between spaces would be a different contract.

All these families retain the elementary operation identity

    N(Kb)=K N(b),   N(b)=b/Σb_i.

It uses only mass preservation. It neither proves (C) nor asserts that arbitrary likelihood multiplication commutes through K. For a deterministic lumping, block-constant likelihoods do descend: K(L⊙p)=Lbar⊙Kp. General likelihoods require a separate coarse observation model.

## 3. Exact positive-channel Brier countermodel

Take a three-state truth variable X with prior

    q=(1/4,1/4,1/2).

For a binary observation Y use strictly positive conditional likelihoods

    L+=(3/4,3/4,1/4),   L−=(1/4,1/4,3/4).

They sum coordinatewise to one. Both observation probabilities are 1/2, and ordinary Bayes gives

    p+=(3/8,3/8,1/4),   p−=(1/8,1/8,3/4).

Let C lump states 1 and 2, represented by

    K=((1,1,0),(0,0,1)).

Then Kq=(1/2,1/2), Kp+=(3/4,1/4), and Kp−=(1/4,3/4). For the ordinary half-Brier potential f_d(p)=½Σp_i²,

    D_f3(p+,q)=D_f3(p−,q)=3/64,
    D_f2(Kp+,Kq)=D_f2(Kp−,Kq)=1/16.

Hence expected coherent Bregman information rises by a factor 4/3 when unit Euclidean weights are freshly chosen in both truth spaces. These are regrets/information gains, **not absolute Brier risks**. Standard unhalved Brier normalization doubles both numbers and leaves the failure unchanged.

This is stronger than merely selecting an information-destroying map. The stochastic reverse

    R=((1/2,0),(1/2,0),(0,1))

satisfies RKq=q and RKp±=p±, and recovers every distribution in the submodel {(a,a,1−2a):0<a<1/2}. The conditional distribution inside the merged block is always (1/2,1/2). Also Y is conditionally independent of X given C(X), since both fine states in the block have the same likelihoods. Thus the fine/coarse statistical experiments about Y are equivalent on this submodel.

Recovery here recovers probability laws and evidence-relevant distinctions. It does not reconstruct the particular fine atom of each realized sample. Even a noisy stochastic matrix can be injective on the space of full probability vectors while having no stochastic inverse; vector-level algebraic recovery, outcome recovery, statistical sufficiency, and isometry are distinct claims.

The local obstruction is exact too. With v=(1/8,1/8,−1/4), the fine Hessian norm is 3/32 and the reset coarse norm is 1/8. Thus (H) fails. No singular Hessian, boundary state, off-simplex implementation error, or inaccurate Bayes update is involved: the prior repair packet implements these posteriors exactly.

## 4. Warranted contrast with KL

For a deterministic partition into blocks B_j, write P_j=Σ_{i∈B_j}p_i and Q_j=Σ_{i∈B_j}q_i. Direct expansion of logarithms gives

    KL(p‖q)=KL(P‖Q)+Σ_j P_j KL(p(·|B_j)‖q(·|B_j)).

The last terms are nonnegative, establishing deterministic data processing. With positive laws, equality holds exactly when the within-block conditional laws agree. The countermodel above has this equality for each posterior and prior, so both expected KL information values equal

    (3/4) ln(3/2)+(1/4) ln(1/2).

For a general stochastic K, apply the log-sum inequality to each row with terms K_ji p_i and K_ji q_i, then sum; column stochasticity yields KL(Kp‖Kq)≤KL(p‖q). This is a distinct, cross-truth-space result. It does not follow merely from strict propriety or the posterior implementation.

These calculations show that KL satisfies this contract and reset Brier does not. They do **not** characterize every admissible generator or establish that KL alone can meet all appropriately structured transport contracts. The weighted quadratic construction below already shows why additional structure matters.

## 5. Fixed-truth observation garbling is always monotone

Fix one finite joint law of (X,Y,Z) with X→Y→Z Markov, and keep the same truth space and same differentiable convex f throughout. Assume all relevant posteriors are interior; the finite-boundary extension can be treated separately. Put q=P(X), p_Y=P(X|Y), p_Z=P(X|Z). Conditional expectation gives

    p_Z=E[p_Y|Z],   E[p_Y]=q.

Define the model-relative coherent information by

    I_f(X;Y)=E D_f(p_Y,q)=E f(p_Y)−f(q).

The linear Bregman term cancels because the posterior mean is q. Conditioning on Z and applying Jensen gives

    I_f(X;Z)≤I_f(X;Y).

More precisely, another conditional cancellation gives the exact gap

    I_f(X;Y)−I_f(X;Z)=E D_f(p_Y,p_Z)≥0.

For strictly convex f, equality holds exactly when p_Y=p_Z almost surely. When vertex first-argument scores are finite, this information is the decrease in Bayes risk for the proper loss D_f(e_X,forecast). Thus every member of the repair family, including Brier, has the stated evidence-garbling monotonicity.

This theorem retains a fixed justified joint law and score. Correcting a false likelihood model, retracting a discredited source, changing operative grounds, or revising an unjustified prior is not automatically garbling under that law. Nothing here says that removing contaminated evidence cannot improve actual warrant. The inherited provenance, selection, withdrawal, and basing qualifications remain intact.

## 6. Positive repair: carry a quadratic reference measure

Specify a positive vector μ alongside the coherent state, and transport it as ν=Kμ. It need not sum to one. Define the coherent potential and divergence

    f_μ(p)=½Σ_i p_i²/μ_i,
    D_μ(p,q)=½Σ_i (p_i−q_i)²/μ_i.

This strictly convex potential lies in the inherited Bayes-compatible perspective family, with any admissible strictly convex radial a. Let δ=p−q. For each output j, weighted Cauchy–Schwarz gives

    (Σ_i K_ji δ_i)² ≤ ν_j Σ_i K_ji δ_i²/μ_i.

Divide by ν_j and sum. Because every column of K sums to one,

    D_ν(Kp,Kq)≤D_μ(p,q).                           (Q)

For the exact loss and equality condition, set w_ji=K_ji μ_i/ν_j and d_i=δ_i/μ_i. Then

    2[D_μ−D_ν]=Σ_j ν_j Var_{w_j}(d)≥0.

Equality holds precisely when d_i is constant on the support of each output row. If a common stochastic reverse R recovers p,q,μ, contraction first through K and then R gives equality. This three-object recovery condition is sufficient; the displayed variance test is the exact pairwise equality condition.

For the countermodel use μ=(1,1,1) and ν=(2,1). The same R recovers μ. The transported coarse divergence and information are now 3/64, exactly the fine values. Resetting ν to (1,1) is what changed the geometry. Here μ denotes a fixed numerical reference vector, not a source identifier, true prior, or the repository's independently typed metaortheme.

The repair preserves these divergences and information gains, not every vertex-wise loss or absolute expected risk. In the positive-channel example, the fine prior Bayes risk is 5/16 and its expected posterior risk is 17/64. The transported coarse values are 3/16 and 9/64. Both gains are 3/64; an absolute risk difference of 1/8 remains because the truth atoms and their vertex scores changed.

### Guard A: recovering the two laws does not recover the reference

Keep p=p+, q, K, and R above, but take μ=(1,2,1), so ν=(3,1). Then

    D_μ(p,q)=11/256,   D_ν(Kp,Kq)=1/24,
    D_μ−D_ν=1/768>0.

The same reverse recovers p and q, but RKμ=(3/2,3/2,1)≠μ. Pair-only sufficiency must not be substituted for three-object recovery.

### Guard B: an arbitrary reference-weighted Bregman generator need not contract

For φ(t)=t⁴ define

    F_μ^φ(p)=Σ_i μ_i φ(p_i/μ_i).

Its Bregman divergence is Σ_i μ_i[φ(p_i/μ_i)−φ(q_i/μ_i)−φ′(q_i/μ_i)(p_i−q_i)/μ_i]. Use the same K, μ=(1,1,1), ν=(2,1), and positive coherent laws

    p=(19/100,1/100,4/5), q=(31/100,29/100,2/5).

Exact arithmetic yields

    D_Fνφ(Kp,Kq)−D_Fμφ(p,q)=921/1562500>0.

Transporting a reference alone therefore does not justify an unrestricted weighted-Bregman theorem. The quadratic scope of (Q) is intentional. A Csiszár f-divergence and a Bregman divergence generated by a similarly named scalar function are not the same construction.

## 7. Source-faithful transport boundary

The targeted repository pin is 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c. SOURCE_LEDGER.json binds the inspected local bytes, Git blobs, URLs, and reading scopes.

1. [H-formalisation, Proposition 4.1 and Theorem 4.2/Corollary 4.3](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-formalisation/orthing_formalisation_v1.md): faithful finite-record encoding preserves the declared view; target-preserving compression is a factorisation/fibre condition. These are not claims of numerical Bregman isometry. Our recoverable-submodel example preserves that information criterion and fails only an added score/metric contract. Typed interaction tensors are not assumed to be probability vectors or stochastic channels.
2. [H-ICS v5, information criterion, output determination, and observation congruence](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex): the manuscript explicitly supplies finite stochastic kernels and distinguishes determining an output law, preserving an observable, and factoring operations through an observation. Its channel mathematics gives a valid conditional setting for K; it does not supply a canonical Bregman score across every change of state type.
3. [Inherited local-Hessian repair note, S1 and S6](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/provenance/v5-research-continuations/notes/3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be.md): real Hessian geometry is already present. S6 already distinguishes common normal repair from different tangent normative comparisons. This report does not discover that distinction; it supplies the explicit coarse-graining test (H), sufficient-lumping countermodel, and conditional reference transport. The retained source verification banner is not upgraded.
4. [Sound-descent model comparison](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md): literal differentiable geometry requires a declared manifold, metric, objective, and operational semantics; provenance and warrant remain separate. The present finite probability model is a conditional candidate, not a claim that noetic or runtime tensors already carry it.

A transport proposal should therefore identify which preservation is intended: declared distinctions, fixed-target information, cross-space divergence, or an actual gradient field. This report settles the first three comparisons only. The sibling noetic-gradient-transport report separately tests tangent dynamics; divergence contraction alone is not a theorem about those dynamics.

## 8. Ancestry, verification, and stopping boundary

The elementary Jensen, log-sum, weighted Cauchy–Schwarz, Bregman segment integral, and conditional-expectation arguments above are proved explicitly. [Csiszár and Shields, Information Theory and Statistics: A Tutorial, §4, printed pp.447–448](https://www.renyi.hu/~csiszar/Publications/Information_Theory_and_Statistics:_A_Tutorial.pdf) defines the classical f-divergence family, includes χ², and establishes deterministic lumping monotonicity in Lemma 4.1. Only that targeted section and proof were checked; no full-paper reading or full characterization survey is claimed. The three-object reference inequality (Q) is proved directly, rather than attributed verbatim to their displayed two-law χ² formula.

The parent independently supplied the pairwise Brier witness, reference-quadratic construction, and ordinary transport distinctions. This worker independently supplied the genuine positive-channel realization, fixed-target garbling proof, the all-points Hessian iff, and this bounded source-faithful synthesis. The reviewer supplied the two guard counterexamples, independently replayed by the parent and by this packet. Attribution concerns this research workflow, not field priority.

verify.py checks the stated rational model, posterior implementation, sufficient recovery, Brier increase, exact KL equality, Hessian failure, weighted preservation, absolute-risk distinction, both guards, fixed-target positive/null garbling controls, and the inherited ambient split in a concrete quadratic instance. It also verifies the inherited source-byte bindings. verification.txt records the executed output. The reviewer's independently written 45-check script and frozen guard JSON are bound in SOURCE_LEDGER.json. These finite controls supplement the ordinary general proofs; no Lean certification or empirical validation is claimed.

No uniqueness campaign is needed to answer this bridge question. Bayes-compatible normalization is broad; meaningful cross-space geometry transport is extra structure; reset Brier fails one natural contract; transporting a quadratic reference gives a genuine nonentropy positive construction; fixed-truth evidence garbling remains monotone for all convex coherent potentials. Selecting and warranting the probability model, coarse-graining, reference, score, and its actual cognitive interpretation remains separate work. T20 remains active.
