# Finite retained-interior probes give a one-sided route-count certificate

8 October 2026 UTC. New scratch sibling. Frozen predecessors are preserved. This is a conditional mathematical observation-channel result, with no integration, physical-access validation, empirical experiment, or T20 closure.

## 1. Observation contract and result

Fix n>=1, m=n+1, c=n/m. The baseline P0 has n independent product-uniform threshold pairs. The Joe alternative P1 has m independent, identically distributed command-space threshold pairs with joint CDF

    F_c(a,b)=H_c(ab),  H_c(z)=1-(1-z)^c.

These are precisely the inherited fresh-endpoint hard-pair worlds. Their one-command no-effect probabilities agree at every command: (1-ab)^n. Each route succeeds at (a,b) exactly when X<=a AND Y<=b; the endpoint hits exactly when at least one route succeeds.

The new interface retains the SAME entire route-threshold vector through all commands. Each output is separately read and nonlatched. The commands do not redraw thresholds, mutate gates, change the inventory, or carry effects into later observations. No route identity or gate bit is read. True reference-rate coordinates are used here; this does not establish an ability to select them physically or under unknown calibration.

Choose any rational coordinates

    0<a_1<...<a_m<1,  1>b_1>...>b_m>0.

Query q_i=(a_i,b_i) for i=1,...,m and r_i=(a_i,b_(i+1)) for i=1,...,m-1. Record the ordered 2m-1 endpoint bits, for example all q bits followed by all r bits. Let E denote the single transcript in which all q bits are 1 and all r bits are 0.

**Theorem.** E requires at least m route occurrences under coordinate-separable monotone AND semantics. Thus P0(E)=0. For the Joe alternative,

    P1(E)=m! product_(i=1)^m mu_c(B_i)>0,                 (1)
    B_i=(a_(i-1),a_i] x (b_(i+1),b_i],
    a_0=0, b_(m+1)=0.

Consequently the forward divergence of this finite panel is

    KL(P1_panel || P0_panel)=infinity.                    (2)

The panel has 2n+1 probes and is fixed before the vector is drawn. No adaptive search, exact real-valued readout, or infinite command sequence is required for this support separation. It is a one-sided total-occurrence lower certificate, not a total count estimator or a claim that every larger-count law is exposed.

## 2. Direct source-specific witness injection

More generally let R be a finite set of fixed route occurrences. Route r has coordinate-only Boolean gates A_r(a), B_r(b), each nondecreasing in its own command, and success is A_r(a) AND B_r(b). The endpoint is their OR. The gates may have occurrence-specific calibrations, arbitrary joint dependence, deterministic values, or common shocks. None of those probabilistic choices affects this pathwise argument.

If route r covers q_i and q_j with i<j, it has A_r(a_i)=1 and B_r(b_j)=1. Since b_j<=b_(i+1), monotonicity gives B_r(b_(i+1))=1. Coordinate separability means its A gate is still A_r(a_i), so r covers r_i. This contradicts that endpoint's miss. Therefore no route covers two of the positive queries on E.

Choose one witnessing route for each q_i. Their identities are all distinct, giving an injection {1,...,m}->R and m<=|R|. Occurrence names need not be observable for this existential counting argument. In fact this direction uses only the antitone ordering of b and monotonicity of B; the increasing a sequence ensures a realizable positive-probability staircase with nondegenerate boxes. There is a symmetric proof using A and the connector r_(j-1).

Coordinatewise monotonicity of an arbitrary two-input success function is insufficient. The single Boolean function

    g(a,b)=OR_i [a>=a_i AND b>=b_i]

is nondecreasing in each input, hits every q_i, and misses every r_i. Treating that disjunction as one route defeats the certificate. The declared elementary AND-route semantics is substantive; counting the conjunction terms as distinct routes restores the bound.

## 3. Exact event geometry, not merely a positive-probability subevent

Work first with thresholds in [0,1]^2, allowing boundary atoms. A route covering q_i while avoiding every connector must lie in

    S_i = {x<=a_i, y<=b_i,
           x>a_(i-1) if i>1,
           y>b_(i+1) if i<m}.                             (3)

Indeed the previous connector r_(i-1) forces x>a_(i-1), because y<=b_i; the next connector r_i forces y>b_(i+1), because x<=a_i. The converses follow because every earlier connector has A coordinate <=a_(i-1), and every later connector has B coordinate <=b_(i+1). Thus (3) avoids them all. It also covers only q_i. The sets S_i are pairwise disjoint.

With exactly m occurrences, E implies that every occurrence witnesses exactly one q_i. There is no spare inactive route: m positive queries require m distinct witnesses. Therefore E is exactly the disjoint union, over all permutations of the m labeled occurrences, of the assignments putting one occurrence in each S_i.

For the Joe law the threshold margins H_c are continuous and put zero mass on either coordinate axis (and on every queried equality line). Hence mu_c(S_i)=mu_c(B_i): the open lower boundaries at a_0=b_(m+1)=0 in (1) discard only null sets. Equation (1) is an exact probability equality, whereas replacing S_i by B_i is an almost-sure event equality when the sample space includes the axes. With boundary atoms, use S_i directly; do not silently drop axis mass.

Writing F=F_c, each mass is the four-corner increment

    p_i=F(a_i,b_i)-F(a_(i-1),b_i)
         -F(a_i,b_(i+1))+F(a_(i-1),b_(i+1)).             (4)

The inherited density is f_c(x,y)=c(1-xy)^(c-2)(1-cxy)>0 throughout the open square. Every box contains an open rectangle of positive area, so every p_i>0. This is where the specified full-support law enters, in addition to route independence. Neither ingredient was needed for the logical lower bound.

The exact factor m! also uses identical distributions. For independent heterogeneous laws mu_j, the exact probability is the permanent

    sum_(permutations pi) product_(j=1)^m mu_j(S_(pi(j))). (5)

Independent full-support laws make (5) positive, though it need not reduce to (1). Independent full support is a sufficient positive-probability condition, not a necessary one; a dependent joint law can also assign positive mass to the assignment event. Full support of each route's marginal alone is insufficient: if all occurrences are identical copies of one common threshold pair, E is impossible for m>=2 despite those full-support marginals. With dependent routes, (1) and (5) generally fail, while the pathwise count bound remains valid.

For k>m iid occurrences, (1) is no longer the event probability. Let D be the connector-avoiding set that covers none of the q_i, p_D=mu(D), and p_i=mu(S_i). All routes must avoid connectors, and every S_i must be occupied. Inclusion-exclusion gives the exact general expression

    P_k(E)=sum_(J subset {1,...,m}) (-1)^|J|
              [p_D+sum_(i not in J) p_i]^k.             (6)

It is zero for k<m and reduces to m! product p_i for k=m. This also explains why a certificate event does not identify the exact count.

## 4. Low arity, endpoints, and the n=1 example

For m=1 there is one positive query and no connectors: a hit certifies at least one route, and with one threshold route its probability is F_c(a_1,b_1). The n versus Joe n+1 hard pair here has n>=1 and therefore m>=2. Setting n=0 would give c=0 and does not provide the inherited Joe construction. An empty inventory cannot produce any positive query under the stated endpoint OR.

The logical implication continues to hold for non-strict monotone coordinate sequences, but repeated adjacent a or b values can make E contradictory or collapse a box. Strict positive widths and heights are required for the positive-probability argument. The outer choices a_m=1 or b_1=1 are allowed if the successive widths and heights stay positive; some probes then lie on faces. At m=2 this can give the two-face-plus-interior panel. Setting a_1=0 or b_m=0 instead makes the relevant positive hit impossible under the continuous Joe law. Literal boundary probabilities use (3)-(4), not a density value at a singular corner.

Allowing unary A-only and B-only routes does not invalidate the total-route lower bound: represent the absent gate as identically true. But it changes what that bound counts. For m>=2 an A-only route can witness only q_m, and a B-only route only q_1. In an inventory whose allowed supports are exactly empty, A, B, AB, the internal positives therefore require at least max(m-2,0) AB occurrences; they do not force m AB occurrences. An always-on empty-support route violates every connector miss when m>=2; when m=1 it can supply the lone hit. In particular, for m=2, an A threshold 1/2 and a B threshold 1/2, as two unary routes, realize the example below with zero AB routes. The hard pair itself is pure AB, so its count conclusion is unambiguous within that class.

For n=1,m=2,c=1/2 take

    q_1=(1/3,2/3), q_2=(2/3,1/3), r_1=(1/3,1/3).

The two box masses are equal to

    F_(1/2)(1/3,2/3)-F_(1/2)(1/3,1/3)
      =(2 sqrt(2)-sqrt(7))/3.

Thus the transcript (1,1,0) has baseline probability zero and Joe probability

    2[(2 sqrt(2)-sqrt(7))/3]^2
      =(30-8 sqrt(14))/9
      =0.00741565620094099059... .                        (7)

The query coordinates are rational; the exact event probability need not be rational.

## 5. KL, sampling cost, and the precise new observation boundary

On the finite transcript alphabet, a P1-positive/P0-zero atom makes forward KL infinite by the usual extended-real definition. The implication does not require any limiting panel or asymptotic n argument. In particular the face-only finite-KL data-processing bound cannot extend to this channel. The inherited face-only theorem remains sound: it explicitly excludes retained interior AB queries. Interior endpoint bits are not, in general, functions of the two coordinate minima. For example, the vectors {(1/5,3/5),(3/5,1/5)} and {(1/5,1/5),(3/5,3/5)} have the same two minima, yet their endpoint bits at (2/5,2/5) differ. The nonseparable information comes from how the coordinate thresholds are paired within occurrences.

This is support separation, not a favorable expected-sample bound. Indeed the disjoint boxes imply sum p_i<=1, so arithmetic-geometric mean gives

    p=P1(E)=m! product p_i <=m!/m^m.                      (8)

For independent fresh retained vectors and a fixed panel, waiting for the first certificate has geometric mean 1/p>=m^m/m!. This lower bound grows exponentially in m, as is also seen without Stirling from m!/m^m<=2^(-floor(m/2)). Waiting until E occurs never terminates under P0, so that rule is not a two-sided terminally correct decision procedure. A fixed-budget rule that declares P1 iff E occurs at least once has zero P0 error and P1 error (1-p)^N; to reach error alpha it needs N>=ceil(log(alpha)/log(1-p)).

These statements concern that particular certificate-occurrence strategy, not every test using the full panel transcript or every interior-query design. Infinite forward KL makes the inherited forward-KL lower-bound method uninformative for this enlarged interface; it does not by itself prove a faster sample exponent, efficient exact count reconstruction, or an optimal intervention design. Each retained vector costs 2m-1 probes under this fixed design. Deterministic numerical controls illustrate very small regular-staircase event probabilities but are not used to infer an optimal rate.

Redrawing the threshold vector between the q and r probes invalidates the injection: the witnesses then live in different latent realizations. A single route can hit the q probes on favorable draws and miss the connector on another draw. Output latching, context-dependent gates, route mutation, noisy observations, and unmodeled effects likewise require a separate model. Common monotone calibrations are not required for the logical certificate, but command-space support and selectability must be justified anew before transporting (1) to a different law or interface.

## 6. The inherited three-bit alias is preserved

The same-threshold-replay predecessor gives an n=1,m=2 alias at t=3/4 for the three commands (t,1), (1,t), (t,t). Its two independent alternative routes have special heterogeneous copulas: one comonotone, one a half mixture of countermonotone and independent copulas, with shared H_(1/2) marginal calibrations. It is not the iid Joe hard pair considered here.

This old panel is itself the boundary staircase q_1=(t,1), q_2=(1,t), r_1=(t,t). The forbidden transcript (1,1,0) is absent in both worlds of that old construction. Because the first alternative route has equal command-space thresholds X=Y, it lies in neither off-diagonal box (0,t]x(t,1] or (t,1]x(0,t]; two distinct witnesses cannot be supplied. For the symmetric interior example in (7), its two off-diagonal boxes also exclude that diagonal route, so this particular heterogeneous larger-count model again assigns the certificate probability zero. Its other transcript probabilities are not asserted to alias on the new panel.

Accordingly (1)'s positivity is a result for the specified independent full-support routes. The logical lower certificate remains valid more generally, but it does not promise a positive chance of witnessing every larger count. This does not overturn the predecessor's alias, finite-grid factorization limitation, or all-command identification theorem.

## 7. Proof assurance, inherited ideas, and scope

RetainedInterior.lean is a compact Lean 4.19.0 proof checked with the existing mathlib and warnings treated as errors, including an isolated trust-zero (-t 0) replay. Its connector_forced theorem derives the forbidden hit from the actual coordinate gate predicates and B monotonicity. witness_injection chooses witnesses and proves injectivity. route_count_bound applies finite cardinality. threshold_route_count_bound explicitly instantiates coordinate-threshold AND gates. Pairwise witness incompatibility is not assumed. Standard logical axioms reported are propext, Classical.choice and Quot.sound; no sorry or new axioms occur in the accepted source. Exact compiler/runtime identities, mathlib commit and manifest, and all 1,798 imported module/source hashes are retained. Separate falsified controls replacing connector misses by hits or strengthening the conclusion to m+1 are rejected; they are not accepted proof artifacts.

This gives kernel assurance for the deterministic semantic obstruction and count inequality. The probability geometry, Joe support, exact product/permanent formulas, KL consequence, and sampling discussion are written mathematical proofs with deterministic executable controls and a separate adversarial review; they are not formalized in Lean. The kernel proof does not verify the semantic interpretation of physical routes or the observation contract. The general Lean theorem asks for an antitone b sequence on natural indices; a finite decreasing panel extends constantly after its last entry, so this does not strengthen the finite-panel premise.

The argument is an application of familiar rectangle-cover/fooling-set and pigeonhole reasoning. A route's success region is a Cartesian upper rectangle. The positive staircase points form a fooling-set-style obstruction, with adjacent forbidden points providing a compact monotonicity certificate for all pairwise incompatibilities. Dirk Oliver Theis's primary research note, [On some lower bounds on the number of bicliques needed to cover a bipartite graph](https://arxiv.org/pdf/0708.1174), introduction pp. 1-2, explicitly recalls the established bound from a set whose pairs cannot share a biclique. That source was inspected only for the relevant definition/bound and attribution; its other results are not being imported. No field-wide novelty is claimed.

The parent supplied the candidate panel, the Joe probability conjecture and n=1 value, the finite-KL boundary comparison, and the required semantic cautions. This packet verifies and sharpens those claims, provides the exact event characterization and dependency distinctions, adds the certificate-only rarity bound, and kernel-checks the source-specific injection. All frozen predecessors remain unchanged. The result says nothing about actual productive independence, psychological manipulability, original-source perfection premises, actual route architecture, or T20 closure.
