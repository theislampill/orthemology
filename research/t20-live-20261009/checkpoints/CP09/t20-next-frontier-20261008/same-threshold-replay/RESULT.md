# Same-threshold replay identifies count and within-route factorization

8 October 2026 UTC. New scratch sibling; the dependent-gate transport and its independent review remain unchanged. This result adds an explicit observation capability. It is not a physical-control claim or T20 closure.

## 1. Result and observation model

Fix an integer n>=1. The baseline has n independent AB route occurrences, each with independent uniform A and B thresholds, identity marginal calibrations, and one designated endpoint effect. Its fresh no-effect law is

    Q_0(a,b)=(1-ab)^n.

In addition to fresh single-command trials, suppose a replay group retains **the same threshold pair in every occurrence** while observing the two face commands (a,1) and (1,b). Each command has its own separately read endpoint response: the first output does not latch into the second, no command changes the thresholds or inventory, and the two readings are correctly paired. The baseline probability that neither probe produces an effect is

    J_0(a,b)=[(1-a)(1-b)]^n.

An alternative has m>=1 fixed independent route occurrences. There is one shared coordinate-calibration homeomorphism alpha:[0,1]->[0,1] for A and one beta for B, applied to every occurrence. They are continuous, strictly increasing and fix both endpoints. Occurrence j has its own arbitrary copula K_j, realized by a uniform-marginal threshold pair (U_j,V_j). All m pairs are mutually independent; their internal coordinates need not be independent. The gates at command (a,b) are

    1{U_j<=alpha(a)}, 1{V_j<=beta(b)}.

Write u=alpha(a), v=beta(b) and

    D_j(a,b)=K_j(u,v).

Then the two observable laws are

    Q(a,b)=product_j [1-D_j(a,b)],
    J(a,b)=product_j [1-u-v+D_j(a,b)].                  (1)

The second formula is a consequence of replaying the same threshold pair. At (a,1) a route succeeds exactly when its A gate is one; at (1,b) it succeeds exactly when its B gate is one. Both endpoint probes show no effect exactly when every route has U_j>u and V_j>v.

**Theorem.** If Q=Q_0 and J=J_0 on the entire closed command square, then

    m=n, alpha(a)=a, beta(b)=b, and K_j(u,v)=uv for every j.

Conversely these conditions give the two target laws. Thus this richer endpoint-only observation identifies the route count, the two calibration maps, and within-route threshold independence in the declared class. It does not infer mutual independence between different route pairs, which remains an assumption; identify hidden physical architecture; or recover occurrence names.

One can start with arbitrary baseline calibration homeomorphisms and change variables to baseline true rates a,b. The all-command equivalence proof is unchanged. This mathematical substitution does not imply that an experimenter can select a particular true rate without knowing that calibration.

## 2. Faces identify the only possible calibration gauge

On the b=1 face, every B gate succeeds almost surely and D_j(a,1)=alpha(a), even though the K_j may differ. Therefore

    (1-alpha(a))^m=(1-a)^n.

The nonnegative m-th root uniquely gives alpha(a)=H_c(a), where

    c=n/m>0, H_c(z)=1-(1-z)^c.

The other face gives beta=H_c. This uses the common marginal map across occurrences. With occurrence-specific maps, the face identifies only a product, and this step fails.

In the rest of the proof the unknown copulas are never differentiated. Only the now-explicit function H_c and ordinary scalar logarithms are expanded near zero.

## 3. The replay law forces c=1 without copula smoothness

Put a=b=t, and write d_j(t)=D_j(t,t), u(t)=H_c(t). The fresh law gives

    product_j(1-d_j(t))=(1-t^2)^n.

Every 0<=d_j<=1. Since the product is at most each factor,

    0<=d_j(t)<=1-(1-t^2)^n=O(t^2).

Here and below n and the alternative's finite m are fixed. The asymptotic constants need not be uniform across alternative counts; this all-command proof makes no uniform finite-panel claim.

Using log(1-z)=-z+O(z^2), the fresh-law identity yields

    -sum_j d_j(t)+O(t^4)
       =n log(1-t^2)=-nt^2+O(t^4),

so

    sum_j d_j(t)=nt^2+O(t^4).                          (2)

This remains valid for nonsmooth copulas: the argument uses only probability bounds, finitely many summands, and the scalar logarithm estimate.

Near zero the known marginal map has expansion

    u(t)=ct+c(1-c)t^2/2+O(t^3).

Each same-threshold both-gates-off factor is 1-2u+d_j, which is positive for all sufficiently small t because it tends to one. Its logarithm is

    log(1-2u+d_j)=-2u+d_j-2u^2+O(t^3).

The cross-term u*d_j is O(t^3), d_j^2 is O(t^4), and the scalar cubic remainder is O(t^3); none requires differentiating d_j. Sum over the fixed m occurrences and use (2), mc=n:

    log J(t,t)=-2m u+nt^2-2m u^2+O(t^3)
              =-2nt-nc t^2+O(t^3).                   (3)

But the target replay law has

    log J_0(t,t)=2n log(1-t)=-2nt-nt^2+O(t^3).

Subtract, divide by t^2 and let t decrease to zero. Equality of the two laws implies n(1-c)=0. Since n>0, c=1 and m=n. The forced maps are consequently alpha=beta=identity.

This argument is independently useful for the all-command characterization. A separate finite-panel count-certificate investigation is outside this packet. Nothing here asserts that count certification itself requires infinitely many commands.

## 4. Two product equalities force every copula to factorize

Fix any interior a,b, now with m=n and identity calibrations. Define

    R_j=1-K_j(a,b),
    S_j=1-a-b+K_j(a,b),
    R_0=1-ab,
    S_0=(1-a)(1-b).

All R_j and S_j are strictly positive because both prescribed products are positive. Equations (1) give

    product_j R_j=R_0^n, product_j S_j=S_0^n,
    R_j+S_j=2-a-b=R_0+S_0.

Arithmetic-geometric mean gives

    average_j R_j>=R_0, average_j S_j>=S_0.

The left sides sum to exactly R_0+S_0, so both inequalities are equalities. The equality condition of arithmetic-geometric mean forces every R_j=R_0 and every S_j=S_0. Hence K_j(a,b)=ab for each occurrence. For n=1 this conclusion is immediate from the product equalities and the same argument remains valid.

This holds at every interior pair. Copula boundary conditions give K_j(a,0)=K_j(0,b)=0, K_j(a,1)=a and K_j(1,b)=b, so the conclusion covers the whole square. Equivalently the threshold coordinates within every occurrence are independent under the stipulated threshold model.

No cancellation of zero factors or logarithms at unit boundaries is used. The small-t argument stays near zero, and the pointwise AM–GM step stays in the open square before handling boundaries separately.

## 5. The new capability really separates the frozen Joe alternatives

The preceding dependent-gate packet realizes every m>=n using c=n/m and the joint command-space CDF H_c(ab), while retaining fixed coordinate-only gate paths and route independence. Under same-threshold face replay its additional observable is

    J_Joe(a,b)=[(1-a)^c+(1-b)^c-(1-ab)^c]^m.           (4)

The bracket is the valid neither-gate cell proved in that packet. Formula (4) generally differs from J_0 even though the entire fresh Q agrees.

For n=1,m=2,a=b=1/2, the fresh Q is 3/4 in both worlds. Both face no-effect marginals are 1/2. Baseline paired no-effect is 1/4, whereas the Joe pair gives

    J_Joe=(sqrt(2)-sqrt(3)/2)^2=11/4-sqrt(6).

The excess over 1/4 is 5/2-sqrt(6)>0. The pair readout distinguishes them without exposing route labels or gates. The new information comes from the cross-command joint law under a fixed threshold realization.

The one scalar J plus the two face marginals A=Q(a,1), B=Q(1,b) determines the entire binary pair law, in order no/no, no/yes, yes/no, yes/yes:

    J, A-J, B-J, 1-A-B+J.

Separately collected face samples do not provide J. The pairing/persistence contract is essential.

## 6. Persistence levels and exact negative controls

These are different observation processes, not interchangeable meanings of "repeat."

1. **Fresh latent inventory:** a histogram can change between trials. The earlier mixture stages show that fresh averaging can erase information. No such mixture is used in the present theorem.
2. **Fixed inventory, fresh threshold realization at each probe:** even if m and every K_j persist, thresholds are redrawn independently. Two face no-effect readings then have joint probability Q(a,1)Q(1,b). The frozen Joe alternatives preserve every fresh Q, hence also every such independent-repeat transcript. Merely holding the inventory cannot supply (1)'s J.
3. **Fixed inventory and the same per-route threshold realization across two different commands:** this is the additional replay capability assumed here. Outcomes within the group are generally dependent, even though different route pairs are mutually independent. It is distinct from the conditionally independent repeated endpoints used to obtain grouped mixture moments.
4. **Same thresholds, same command repeated:** both endpoint bits are literally the same deterministic function of the retained thresholds. Their joint no-effect probability is Q(a,b), not Q(a,b)^2. Such same-command replay adds no separating information when the fresh Q functions already agree. The two different face commands do substantive work.

Replay requires a separately readable output for each command and no carryover, threshold change, route change, or irreversible-output contamination. The theorem supplies neither a reset operation nor evidence that these conditions are physically or psychologically available.

## 7. Finite panels cannot certify arbitrary global copula factorization

This negative result concerns a fixed, predeclared finite set of commands, even when its full same-threshold replay transcript law is retained. It does **not** say finite panels cannot identify the integer count under stronger or carefully chosen tests.

Let A and B be finite sets of all queried coordinate values, adding 0 and 1. Define nonzero polynomials

    f(x)=x(1-x) product_(a in A intersect (0,1)) (x-a),
    g(y)=y(1-y) product_(b in B intersect (0,1)) (y-b).

Let M,N be positive bounds on |f'| and |g'| on [0,1], and choose 0<epsilon<=1/(2MN). Then

    K_epsilon(x,y)=xy+epsilon f(x)g(y)

has continuous density 1+epsilon f'(x)g'(y)>=1/2. Integrating that density, using f(0)=g(0)=0, gives the displayed CDF. Endpoint zeros make its margins uniform, and total mass is one. Thus it is a genuine non-independent copula, not merely a probability-valued surface. It differs from xy wherever f(x)g(y) is nonzero.

At every queried grid vertex (a,b) it equals ab. Consequently all threshold rectangle-cell masses on the entire finite grid agree with the independent uniform pair. Every possible vector of threshold-comparison outcomes at the panel commands is determined by these cells. Taking n mutually independent route pairs with this common perturbed copula and identity calibrations therefore preserves the full endpoint replay transcript law over the panel, while within-route factorization fails elsewhere.

The same argument includes any predeclared finite collection of fresh probes, paired faces and longer fixed-threshold replay words. Their joint laws are all functions of the same finite-grid threshold cells. Matching only isolated CDF values would not suffice for arbitrary queried combinations; matching the whole queried coordinate grid is why this construction works.

For rational panels the proof can be made fully rational. If f(x)=sum f_k x^k, use M=sum k|f_k|; likewise N. On [0,1] these bound the derivatives, so epsilon=1/(2MN) supplies a certificate with density at least 1/2. The exact controls instantiate the grid {0,1/4,1/2,3/4,1}, verify all cell probabilities, and exhibit an off-grid difference.

This is a deterministic finite-panel indistinguishability result. No unrestricted adaptive/randomized protocol impossibility, approximate-data lower bound, finite-sample theorem, or full functional-reconstruction impossibility for an all-command oracle follows automatically.

## 8. A particular finite panel can also miss the count

Here is a separate negative control; it is not a universal finite-count impossibility theorem.

Compare n=1 with m=2 at a=b=t=3/4. Both alternative occurrences use alpha=beta=H_(1/2), so u=v=1/2 at the tested coordinates. Give the first route the comonotone copula K_1(u,v)=min(u,v). Give the second the convex-mixture copula

    K_2(u,v)=[max(u+v-1,0)+uv]/2.

Each is a valid copula: K_1 comes from equal uniform coordinates; max(u+v-1,0) comes from (U,1-U); uv comes from independent uniforms; averaging the latter two distributions preserves uniform margins. Draw the two route pairs independently.

At the tested point D_1=1/2, D_2=1/8. The four exact observed probabilities are

    Q(t,1)=Q(1,t)=1/4,
    Q(t,t)=(1-1/2)(1-1/8)=7/16,
    J(t,t)=(1/2)(1/8)=1/16.

These equal the n=1 independent baseline at t=3/4. Both full binary face-pair laws therefore agree. The independently noticed stronger control also holds: if all three commands (t,1), (1,t), (t,t) are replayed against the same thresholds, their effect-bit law is

    (0,0,0):1/16, (1,0,0):3/16,
    (0,1,0):3/16, (1,1,1):9/16,

in both models. In the alternative, the first route's two gates are always equal at these calibrated thresholds; if that route is off, all three endpoint bits come from the second route. Thus the interior effect bit equals the AND of the two face effect bits in both models. The reviewer identified this strengthening; it is independently enumerated in the author controls.

The model is valid across all commands; equality is claimed only for this panel. It does not refute a differently chosen low-command finite count certificate. It demonstrates why a finite-panel statement needs a proved design and constants rather than an inference from the existence of an all-command theorem.

## 9. Attribution and semantic boundary

The parent proposed the all-command replay conjecture, the small-command/AM–GM proof strategy, the distinction from held-inventory fresh gates, and the finite-grid perturbation strategy. This operation checks those arguments, supplies precise remainder bounds without copula differentiability, instantiates exact probability controls, and derives the high-command finite-panel alias. A separate worker investigates a stronger finite count certificate; that work is not claimed or reviewed here.

The Joe family and threshold/CDF mathematics are inherited. The prior gate-transport packet already isolates unknown within-route dependence; the earlier grouped-mixture work already distinguishes inventory persistence from conditional measurement independence. This continuation's added object is the joint endpoint law across distinct commands with the actual threshold realization retained.

Probabilistic independence is not whole-existence or original-source independence. The theorem does not establish that the replay instrument is admissible for the source's complete decisive willing, unchanged productive conditions or perfection premises. It neither supplies a model of harmonious plural Necessary Beings nor excludes one. No physical validation, psychological manipulability, original-source theorem, integration, owner acceptance or T20 closure is claimed.
