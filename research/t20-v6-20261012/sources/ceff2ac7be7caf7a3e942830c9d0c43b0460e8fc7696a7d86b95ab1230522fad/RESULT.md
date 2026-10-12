# Fixed calibration, finite exchangeability, and the value of continuing inquiry

11 October 2026 UTC. Additive, source-bound mathematical continuation. Written proofs and exact rational controls; no repository integration, metaphysical countermodel, empirical calibration, proof-assistant certification, or programme closure.

## Results and the missing joint

MOM-11 already gives the exact two-trial fixed-calibration body and an explicit failure at the third trial. ET-17 already gives fixed-model policy-loss vectors and rejects branchwise model reselection. H-Continuation already preserves bounded adaptive policy values once the required branch observables are retained. The source-bound companion D6 already separates finite exchangeability from iid mixtures. None of those facts alone determines the next inquiry policy.

This continuation supplies a joined, solved decision problem rather than another general polynomial expansion:

1. Starting with MOM-11's exact retained moments `(mu,nu)=(1/2,1/3)`, the **exact four-trial iid-mixture body** in `(t,s)=(E[p^3],E[p^4])` is

       2/9 <= t <= 5/18,
       12t^2 - 4t + 4/9 <= s <= -6t^2 + 5t - 2/3.

   Explicit two- and three-atom measures attain its lower and upper boundaries. Every interior point is attained. A closed formula below evaluates every affine policy-loss functional on this curved body.
2. The **exact four-exchangeable body with the same two-trial law** is the larger triangle with vertices `(1/6,0)`, `(1/4,1/4)`, `(1/3,1/3)`. Here `t` and `s` mean observable joint-success probabilities; this class is not assigned a latent calibration parameter.
3. After the same observed history `X1=X2=1`, reserve `Y=X4` as the target and permit one paid reading of `X3`. With ordinary 0–1 prediction loss and query price `0<c<1/2`, the iid-mixture optimum **skips and reports 1**, with value `1/3`. The finite-exchangeable optimum privately chooses **skip/report 1 with probability 4/5, or query/report 1-X3 with probability 1/5**, with value `2/5+c/5`. At `c=1/10` this is `21/50`; the best deterministic policy costs `1/2`. A silent iid-mixture assumption therefore changes the actual optimal continuation policy, despite identical pre-existing two-trial evidence.
4. A useful negative theorem prevents overgeneralisation: **before any observation**, with arbitrary fixed first two calibration moments and asymmetric 0–1 prediction loss, one observed sample is minimax-sufficient for every bounded adaptive horizon. The larger finite-exchangeable family has exactly the same minimax value for that contract. Explicit least-favourable measures prove it. Thus a missing higher moment need not change an optimal decision, although it changes full continuation laws.

These are new-to-the-inspected-interface calculations and proofs, using classical moment geometry and finite minimax decisions. No field-wide priority claim is made.

## 1. Source ownership and bounded comparison

`READ_LEDGER.json` binds the actual inherited bytes and the reading scope. `DEDUP_SCAN.json` records a machine search over 620 deduplicated textual result/report/theorem/continuation objects. Seventeen matched the declared moment/calibration/exchangeability terms; relevant actual owners were inspected. This is not a claim to have read 620 bodies or exhaustively searched the literature.

- **MOM-11 / fixed-calibration-moment-repair** owns `(1-2mu+nu,mu-nu,mu-nu,nu)`, `mu^2<=nu<=mu`, point-dependent atomic decomposition, the distinction between convex law representation and a physical calibration, and the third-trial collision `5/6` versus `2/3`. Our four-trial body continues its actual `(1/2,1/3)` slice.
- **ET-17 / coupled-credal-inquiry-transport and its independent review** own same-model aggregation across branches, private-coin timing, initial-law vertex reduction, set-valued finite policy recursion, the reused-kernel endpoint failure, and the distinct finite-dimensional/nonpolyhedral questions. Those claims are preserved, not rediscovered.
- **H-Continuation, Theorem 2, lines 217–292** owns operation-relative branch probabilities, terminal numerators, bounded adaptive values, finite-horizon maps into a shorter remaining-horizon space, and the distinction between horizon sufficiency and invariant closure. Our explicit moment maps instantiate this ancestry.
- **Audit-continuation and posterior-inquiry-value** own the distinctions among target posteriors, event frequencies, and target–audit joint numerators. Our conditional event has the same strictly positive mass `1/3` throughout both model families; the new separation is not missing frequency or null conditioning.
- **Companion diagnostics D5–D6**, actual coverage source S23, owns the source-local Bayes and finite-exchangeability warning. D5 expressly says Koons–Pruss choose a worst-case endpoint, rather than accidentally omit a likelihood. D6 does not turn a probabilistic representation into an efficient cause. Those qualifications survive here.
- The inspected grouped-count calibration owner already translates a conditional Bernoulli-mixture law into ordered laws and moments. It concerns latent integer counts and common powers of an unknown survival rate. We neither relabel that identifiability theorem nor add a sampling-rate optimisation.

The scan found no preceding owner of the displayed four-trial slice, its exact continuation game, or the horizon-uniform asymmetric-prediction minimax theorem. That is a bounded comparison, not an assertion of absence from all retained work.

## 2. A common target and an explicit uncertainty contract

All observable coordinates are binary. The target in the main continuation problem is the **reserved fourth observation `Y=X4`**. The only new observation allowed after history `11` is a reading of the distinct coordinate `X3`. Reading a coordinate again would return that same bit; it is not a newly drawn trial. Every policy uses public observations and independent private randomness, never an unobserved model label.

Two complete-law families are compared.

**Calibration-mixture family C4.** A probability measure `rho` on `[0,1]` is part of the complete model. One `p` is selected according to that measure and is held fixed for all four trials; conditionally on `p`, the trials are independent Bernoulli(p). The family restricts `E_rho[p]=1/2` and `E_rho[p^2]=1/3`. Nature selects one complete admissible model before the policy's private random realisation, and that model governs the whole experiment.

This is a declared family of mixtures of fixed-calibration laws. It is not a claim that calibration bounds alone imply a hyperprior. Nor is it the family of deterministic calibrations satisfying `p=1/2` and `p^2=1/3`, which would be empty. One may use the mixture as a stipulated generative model or as a convex complete-law uncertainty specification; the mathematical decision contract must say which is intended.

**Finite-exchangeable family E4.** This consists of all probability laws on four bits invariant under permutations, with

    E[Xi]=1/2,       E[Xi Xj]=1/3 for i != j.

No latent `p` is assumed in E4. Define its observable coordinates

    t=P(X1=X2=X3=1),       s=P(X1=X2=X3=X4=1).

Under C4 these equal the third and fourth calibration moments. Under E4 they remain ordinary observable joint-event probabilities. This operational identification permits comparison without treating a nonexistent calibration as E4's target.

Every model in either family has the same ordered two-trial law

    (P00,P01,P10,P11)=(1/3,1/6,1/6,1/3).

In particular the already observed history `11` has mass `1/3` in every model. Elementwise conditioning therefore retains a common denominator. No prior over model identities or branchwise reselection is introduced.

## 3. The exact four-trial fixed-calibration body

Write `m0=1,m1=1/2,m2=1/3,m3=t,m4=s`. For any square-integrable polynomial, its squared expectation is nonnegative. Consequently the moment matrix

    H = [[1, 1/2, 1/3], [1/2, 1/3, t], [1/3, t, s]]

is positive semidefinite. The upper-left two-by-two block is positive definite, with inverse `[[4,-6],[-6,12]]`. Its Schur complement gives

    s >= L(t) = 12t^2 - 4t + 4/9.

Likewise the expectation of `p(1-p)(a+bp)^2` is nonnegative, so

    G = [[1/6, 1/3-t], [1/3-t, t-s]]

is positive semidefinite. Its Schur complement gives

    s <= U(t) = t-6(1/3-t)^2 = -6t^2+5t-2/3.

The inequality `L(t)<=U(t)` is equivalent to

    18(t-2/9)(t-5/18) <= 0,

and hence the stated interval for `t`. This proves necessity. We now prove sufficiency constructively, without assuming a general truncated-moment theorem.

### Lower boundary: a two-atom measure

For any `t` in the interval, put

    alpha=12t-2,       beta=4/3-6t,
    f(x)=x^2-alpha*x-beta.

The two roots `u<v` lie in `[0,1]` and straddle `1/2`: `f(0)>=0`, `f(1)>=0`, the vertex lies between `1/3` and `2/3`, and `f(1/2)=-1/12<0`. In particular the roots are distinct. Give `u,v` weights

    (v-1/2)/(v-u),       (1/2-u)/(v-u).

These are nonnegative, sum to one, and give mean `1/2`. Since `p^2=alpha*p+beta` on the support, the second moment is `1/3`, the third is `t`, and the fourth is `L(t)`. The last identity also follows because the moment-matrix square represented by the Schur complement vanishes on the support.

At `t=2/9` this is the inherited measure with weights `1/4,3/4` at `0,2/3`. At `t=5/18` it is the inherited measure with weights `3/4,1/4` at `1/3,1`.

### Upper boundary: a three-atom measure

Put `z=2-6t`, so `1/3<=z<=2/3`, and place masses

    w_z=1/[6z(1-z)],
    w_1=1/2-1/[6(1-z)],
    w_0=1/2-1/(6z)

at `z,1,0`, respectively. The masses are nonnegative and sum to one. Their first two moments are `1/2,1/3`; their third is `t`. Moreover `t-s=E[p^3(1-p)]=z^2/6`, giving `s=U(t)`.

A common convex mixture of the lower- and upper-boundary measures at the same `t` attains every `s` between `L(t)` and `U(t)`, while preserving all earlier moments. This proves the exact body. The two boundaries coincide at the interval endpoints; no division by their zero gap is needed there.

### Exact support function: every affine policy loss can be evaluated

For coefficients `(a,b,d)`, maximize `a+b*t+d*s` over C4.

- If `d>0`, use `s=U(t)` and clamp `(b+5d)/(12d)` to `[2/9,5/18]`.
- If `d<0`, use `s=L(t)` and clamp `(4d-b)/(24d)` to that interval.
- If `d=0`, use the appropriate interval endpoint according to the sign of `b`; for `b=0` every point attains the same value.

Substitution gives the maximum. In the first two cases the resulting function of `t` is a concave quadratic, so its stationary point or a nearest endpoint is the global maximizer. This is an exact evaluation procedure, including for rational coefficients; it does not replace the curved body by a fixed list of vertices.

## 4. The exact finite-exchangeable comparison body

For a specified four-bit word containing `k` ones, exchangeability and inclusion–exclusion give probability

    k=0: 1-4t+s
    k=1: -1/2+3t-s
    k=2: 1/3-2t+s
    k=3: t-s
    k=4: s.

These are probabilities of individual ordered words, not count probabilities. The count probability is the displayed expression multiplied by `choose(4,k)`.

Nonnegativity is equivalent to the triangle with vertices

    A=(1/6,0),       B=(1/4,1/4),       C=(1/3,1/3).

One explicit verification uses barycentric coefficients

    lambda_A=6(t-s),
    lambda_B=4-24t+12s,
    lambda_C=18t-6s-3.

They sum to one; nonnegativity is exactly the three nonredundant inequalities. Conversely a convex combination of the vertices gives all five nonnegative word masses. The corresponding distributions of the head count J are:

- A: `P(J=0)=1/3, P(J=3)=2/3`;
- B: `P(J=0)=1/4, P(J=2)=1/2, P(J=4)=1/4`;
- C: `P(J=1)=2/3, P(J=4)=1/3`.

Within each head count, all corresponding ordered words have equal mass. These are explicit complete four-exchangeable laws with the stipulated first and second moments.

The fixed-calibration body is a proper subset. For example A is excluded by `t>=2/9`; after conditioning on `11`, A has perfect negative dependence between the two remaining bits. Even though the original pair covariance is positive (`1/3-1/4=1/12`), finite exchangeability need not admit a fixed-calibration representation. Thus the discriminating example is stronger than merely starting with the inherited negatively correlated two-bit pair.

## 5. Why these coordinates preserve every legal four-trial policy loss

A complete ordered path law on the four bits is determined by the five expressions above. For a fixed lawful deterministic policy, its total loss on each complete path is specified by its observed history, chosen actions and terminal report. Expected loss is the sum of those path losses times their probabilities, hence an affine function of `(t,s)`. A common private mixture of policies takes the same mixture of their affine coefficients. The unknown law cannot choose different coefficients or actions for different model coordinates.

This is the finite-path lifting of H-Continuation and ET-17: common coordinate-reading projectors act on the sixteen-point path space, and the model uncertainty is in its initial complete law. It is valid for every declared bounded path/history loss, including observation costs and optional stopping, so long as the same lawful information and action menu is used. It does not imply that costs or permissions absent from the path contract are automatically preserved.

Consequently:

- fixed-policy robust evaluation over C4 is exactly the support formula in section 3;
- fixed-policy evaluation over E4 is the maximum of its three vertex values;
- deterministic policy optimisation minimizes these values over the finite lawful tree set;
- private-randomised optimisation minimizes the same support function over the convex hull of the finite policy-coefficient set. For E4 this is an ordinary finite LP. C4's exact curved constraint is not silently called a vertex LP.

Conditional updates use unnormalised moments. Reading a fresh success maps `m_j` to `m_(j+1)`; reading a failure maps it to `m_j-m_(j+1)`. Normalize only by the positive branch mass, and reduce the remaining supported horizon. A four-trial statistic is not an invariant filter for arbitrary additional trials.

For the particular history `11`, division by `nu=1/3` gives the remaining pair `(X3,Y)`:

    P00=1-6t+3s,
    P01=P10=3(t-s),
    P11=3s.

These retain the mixed target–future-observation numerator as well as both marginals. A target-only interval is insufficient to evaluate the query in the next section.

## 6. A fully solved continuation decision that changes with the representation premise

The history `11` has already been observed. Its acquisition cost is sunk. The target is `Y=X4`. The remaining menu permits:

- skip and report either target label;
- pay `c>=0` to read `X3`, then report either label as a function of the observed bit.

Loss is wrong-report probability plus the incurred query cost. All six deterministic policies and all their independent private mixtures are admissible. Nature chooses one complete law before the realised private coin. No calibration target, branch-specific report restriction, artificial defer option, or additional verifier is introduced.

### 6.1 Calibration-mixture optimum

The skip/report-1 risk is

    1-P(Y=1|11)=1-3t <= 1/3,

with equality at `t=2/9`. Under the inherited endpoint measure `rho_B=(1/4)delta_0+(3/4)delta_(2/3)`, observing `11` rules out `p=0`, leaving `p=2/3` with certainty. Hence `X3` and `Y` are independent Bernoulli(2/3) under this conditional model.

Even an oracle revealing `p` would have 0–1 prediction risk `1/3`. No lawful randomised policy using `X3` can do better, and query cost is nonnegative. Therefore

    V_C4(c)=1/3 for all c>=0.

For `c>0`, any positive probability of querying increases risk under this least-favourable model; the optimal policy skips and reports 1. More fresh calibration trials could not improve its worst-case conditional prediction error either, provided the same target remains reserved and all such observations are conditionally independent of it given `p`.

### 6.2 Finite-exchangeable optimum, including private randomization

After `11`, the three vertex laws of `(X3,Y)` become:

    A: (P00,P01,P10,P11)=(0,1/2,1/2,0),
    B: (1/4,0,0,3/4),
    C: (0,0,0,1).

The six deterministic policy-loss vectors, in model order `(A,B,C)`, are

    skip 0:          (1/2, 3/4, 1)
    skip 1:          (1/2, 1/4, 0)
    query; always 0: c+(1/2, 3/4, 1)
    query; copy X3:  c+(1, 0, 0)
    query; invert:   c+(0, 1, 1)
    query; always 1: c+(1/2, 1/4, 0).

Thus every deterministic query is worse than, or at zero cost ties no better than, skip/report 1. The deterministic optimum is `1/2` for every `c>=0`.

For `0<=c<=1/2`, privately mix skip/report 1 with weight `4/5` and query/invert with weight `1/5`. Its vector is

    (2/5+c/5, 2/5+c/5, 1/5+c/5).

Its worst loss is `v=2/5+c/5`. For a matching lower certificate, put weights

    eta_A=(3+4c)/5,       eta_B=(2-4c)/5,       eta_C=0

on the three complete models. These are nonnegative and sum to one. The averaged loss of skip/report 1 and query/invert is exactly `v`. The other four policy averages are at least `v`: skip/report 0 averages `3/5-c/5>=v`, query/copy averages `3/5+9c/5>=v`, and the two constant query policies add nonnegative query cost to their corresponding skips.

Every private mixture therefore has worst-model loss at least its eta-averaged loss, at least `v`. This proves the exact optimum over the entire randomised policy class, not merely a finite grid.

For `c>=1/2`, model A alone lower-bounds every pure policy by `1/2`; skip/report 1 attains that robust value. Hence

    V_E4(c)=min(1/2, 2/5+c/5).

For `0<c<1/2`, the displayed mixture is the unique root mixture of complete deterministic plans attaining the optimum: under the lower certificate every other pure plan has strictly greater averaged loss, and balancing A and B forces the query/invert weight `1/5`.

At `c=1/10`, C4 optimally skips for `1/3`; E4 optimally queries with probability `1/5` and obtains `21/50`, improving on its own deterministic skip value `1/2`. The larger model class has higher minimax loss, as it must; its best policy is also different. This is a decision consequence of the representation premise.

If Nature sees the realised private plan before selecting its model, the mixture has value `(4/5)(1/2)+(1/5)(1+c)=3/5+c/5`, and randomisation cannot improve deterministic `1/2`. Private-coin timing is therefore load-bearing, exactly as ET-17 requires.

### 6.3 Scalar pruning and conditional reselection remain invalid repairs

The query/invert loss vector has a worse scalar maximum than skip/report 1, but is indispensable to the optimal private mixture. Pruning policies solely by their individual worst loss destroys the optimum. This is a concrete new continuation instance of ET-17's general warning, not a new general theorem about nonrectangularity.

Likewise one cannot independently choose A's adverse target conditional at one hypothetical branch and B's at another while claiming to retain one original four-trial model. A scalar branchwise enlargement requires its own explicitly declared uncertainty contract. No such enlargement is used to derive the exact values above.

### 6.4 The policy separation survives strictly positive complete laws

The zero cells at the E4 vertices are not essential. Let U be the four-trial law obtained from a uniform calibration on `[0,1]`. It has the same `(mu,nu)=(1/2,1/3)`, and every ordered word of count k has positive probability `1/[5 choose(4,k)]`. Replace each E4 vertex P by `(9/10)P+(1/10)U`, retaining their convex hull E4-positive. Every complete four-bit cell is now at least `1/300`, and the observed history still has probability `1/3`.

At query cost `c=1/10`, the same root mixture (4/5 skip/report 1; 1/5 query/invert) has exact worst loss `207/500`. A matching lower certificate assigns weights `164/225,61/225,0` to the three positive vertices. Direct evaluation of all six pure policies gives minimum averaged loss `207/500`, attained only by skip/report 1 and query/invert. Balancing the first two model losses again forces query probability `1/5`. The best deterministic policy is skip/report 1, with value `19/40`.

The C4 least-favourable measure used above already gives every four-bit word positive mass because its atom at `p=2/3` has positive weight. Restricting C4 to its positive complete laws therefore retains the value `1/3` and optimal skipping. The representation-premise policy separation thus survives strictly positive complete-law families on both sides. E4-positive is an explicitly narrower finite-exchangeable family, not silently substituted for the complete E4 triangle.

## 7. A sharp saturation theorem: why higher-moment differences sometimes do not change inquiry value

The previous continuation result must not be universalised to every prediction problem. Here is an exact countervailing theorem.

Fix `0<mu<1`, `mu^2<=nu<=mu`, and positive false-positive and false-negative losses `a,b`. Let

    tau=a/(a+b),
    q0=(mu-nu)/(1-mu),       q1=nu/mu.

One has `q0<=mu<=q1`. Before observing anything, reserve a future bit Y and allow any bounded adaptive sequence of readings of other distinct bits. Under C, conditionally on one held calibration p, all those observations and Y are iid Bernoulli(p), with the first two moments fixed at `(mu,nu)`. Under E, use all finite-exchangeable complete laws on that same horizon with those first and second moments. The target and policy information are the same in both families.

The best skip risk and best one-observation risk are

    R0=min(b*mu, a*(1-mu)),
    R1=min(b*(mu-nu), a*(1-2mu+nu))
       +min(b*nu, a*(mu-nu)).

**Theorem.** With zero observation costs and at least one permitted observation, both families have minimax value exactly `R1`, for every bounded adaptive horizon. If the first observation costs `c>=0` and all later observations have nonnegative costs, both values are exactly

    min(R0, c+R1).

The claim concerns expected asymmetric classification loss of a reserved future bit, not probability estimation, calibration recovery, log/Brier scoring, conditional continuation after arbitrary prior history, or all bounded path losses.

### Proof by an explicit least-favourable calibration law

The first-observation rule computed from `q0,q1` has risk `R1` under every complete law in either family, because its risk uses only the fixed two-bit marginal. This supplies an upper bound. We construct a member of C under which even revealing the actual calibration p cannot beat `R1`.

1. If `q1<=tau`, put mass `mu^2/nu` at `nu/mu` and the remaining mass at zero. The moments are `(mu,nu)`, its support lies in `[0,tau]`, and an oracle always reports zero. Its oracle risk is `b*mu=R1`.
2. If `q0>=tau`, use the two-atom measure supported at `q0` and 1, with mass `(1-mu)^2/(1-2mu+nu)` at `q0`. The support lies in `[tau,1]`; the oracle always reports one, and risk is `a*(1-mu)=R1`.
3. Otherwise `q0<tau<q1`. Put masses

       w_tau=(mu-nu)/[tau(1-tau)],
       w_1=(nu-mu*tau)/(1-tau),
       w_0=[nu-(1+tau)*mu+tau]/tau

   at `tau,1,0`. The inequalities defining this case give nonnegative weights; direct algebra gives sum one and moments `(mu,nu)`. At zero and one the oracle makes no error. At `tau`, either report has the same Bayes loss `a*b/(a+b)`. The oracle risk is therefore `(a+b)(mu-nu)=R1`.

The equality-boundary cases may be assigned to either adjacent construction. The limiting degenerate means zero and one have deterministic target and zero prediction risk, so skipping is optimal for nonnegative costs.

For any adaptive policy, conditionally on p its reserved Y remains Bernoulli(p) and independent of all observed non-target bits and private coins. No such policy can have error less than the oracle Bayes risk. Thus the constructed complete calibration model lower-bounds all adaptive prediction policies by `R1`, irrespective of horizon. It belongs to C and, at each finite horizon, to E. Since C is a subset of E and the common one-observation rule has loss `R1` throughout E, both values equal `R1`.

Before any observation, the event of taking the first observation depends only on private coins, not on p. Under this same least-favourable law, a skip plan has risk at least `R0`, and a plan that observes has risk plus cost at least `c+R1`. Nonnegative subsequent costs cannot reduce that bound. A private mixture is bounded below by the smaller of the two quantities. Skip or the one-observation rule attains it, proving the priced statement.

For `(mu,nu)=(1/2,1/3)` and `a=b=1`, the least-favourable calibration law is

    (1/6)delta_0 + (2/3)delta_(1/2) + (1/6)delta_1.

Here `R1=1/3`, `R0=1/2`, and the initial query threshold is `c=1/6`, uniformly in the allowed bounded horizon. The irreducible fair-calibration component explains why merely appending more samples cannot create a robust benefit in this ex ante contract.

This theorem also explains a failed candidate comparison: different third/fourth moments alone do not prove different optimal ex ante forecast values. Full predictive sufficiency and objective-specific minimax value sufficiency are genuinely different questions.

## 8. The horizon remains a substantive boundary

Four moments determine four-trial path laws, not arbitrary future continuation. For a fully positive finite control, take support `p=k/5`, `k=0,...,5`, and masses

    w_k^plus/minus = (5/192) choose(5,k)
                    +(1/12) 1[k in {0,5}]
                    +/- (1/192)(-1)^k choose(5,k).

Both measures have positive masses, sum one, and agree through degree four:

    (m0,m1,m2,m3,m4)=(1,1/2,1/3,1/4,61/300).

The alternating fifth finite difference annihilates every polynomial of degree at most four. Their fifth moments are `437/2500` and `219/1250`. After four successes, the fifth-success probabilities are `1311/1525` and `1314/1525`; the conditioning event has the same positive probability `61/300`.

Thus the exact C4 representation, support formula and all-four-trial policy preservation are not an arbitrary-horizon closed filter. This is a classical finite-difference specialization of inherited moment-continuation reasoning, not a new universal impossibility theorem.

## 9. Philosophical and evidential limits

The comparison shows exactly which mathematical decision changes when a finite symmetric observation law is replaced by an iid-mixture premise. It does not show that actual testimony is exchangeable, that actual uncaused events have this law, or that a latent p is an efficient cause. It does not refute the PSR or any complete Koons–Pruss argument. The source-bound companion's own likelihood, extendibility and interpretation distinctions remain indispensable.

The values are conditional on declared numerical losses, model classes, history, legal queries and private-coin timing. They are neither actual cognitive-warrant judgments nor recommendations about how ordinary knowers must store information. No human or empirical source reliability was estimated. No sampling-complexity programme is substituted for the original conceptual question.

`check_exact.py` is author evidence using exact fractions and explicit exceptions. `run_checks.py` executes normal and optimized positive runs and deliberate false-control rejections. Finite checks supplement the universal proofs above; they do not replace them. Independent review is a separate status and must bind the bytes actually inspected.
