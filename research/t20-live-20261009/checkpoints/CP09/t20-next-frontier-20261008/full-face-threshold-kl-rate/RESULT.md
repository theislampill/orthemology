# Full face-threshold readout retains the fourth-power KL rate

8 October 2026 UTC. New scratch-only successor to the frozen full-face-threshold-information packet. This is a conditional mathematical information-channel result, with no protected integration, empirical validation, physical-feasibility claim, or T20 closure.

## 1. Exact claim and observation contract

Fix an integer n>=1, m=n+1, c=n/(n+1). Use precisely the two worlds in the frozen predecessor:

- P0 has n independent product-uniform route-threshold pairs.
- P1 has m independent Joe route-threshold pairs with the common calibration H_c(t)=1-(1-t)^c and the stipulated within-route joint threshold CDF H_c(ab).

One ideal mathematical observation is the pair (T_A,T_B) of minimum coordinate thresholds of one unchanged route-threshold vector. It returns neither individual route thresholds nor route labels. Put X=1-T_A and Y=1-T_B. Their CDFs are

    F0(x,y)=x^n y^n,
    F1(x,y)=S(x,y)^m,
    S=x^c+y^c-(x+y-xy)^c.                                  (1)

Both margins are Beta(n,1). The predecessor proves absolute continuity with strictly positive interior densities, no singular or boundary remainder, infinite chi-square for every n, and finite forward KL. For this same full two-minimum channel, write D_n=KL(P1||P0), with natural logarithms. Then

    lim_(n->infinity) n^4 D_n = 1/2.                        (2)

Thus infinite chi-square at each n does not improve the forward-KL exponent of the exact face-minimum readout. Equation (2) is not a reverse-KL statement or an assertion that exact real-valued readout is physically available, free, or attainable with a finite number of probes.

Every finite adaptive FACE-ONLY word on one unchanged vector is a common randomized function of this pair. It therefore has forward KL at most D_n, regardless of its length or threshold precision. Under the fresh-independent-replicate and terminal-correctness conditions in section 6, this yields

    E1[N] >= kl(1-alpha,alpha)/D_n
           = (2+o(1)) n^4 kl(1-alpha,alpha),                (3)

where N counts independent retained vectors used and 0<alpha<1/2 is fixed. The bound concerns the stipulated hard pair. It is not an optimal broad wrong-count design or a sharp achievable sample/probe-cost constant.

## 2. One common transformation and the exact likelihood ratio

Transform BOTH worlds using the reference n:

    U=-n log X, V=-n log Y.

Their common margins are Exp(1), and the reference density on (0,infinity)^2 is f0(u,v)=exp(-u-v). The joint SURVIVAL function under P1 is

    G1(u,v)=P1(U>=u,V>=v)=exp(-u-v+H_n(u,v)),
    H_n=m log[S/(xy)^c], x=exp(-u/n), y=exp(-v/n).          (4)

Since the CDF in (1) has no singular remainder, the transformed density is the mixed derivative of (4). Consequently the exact likelihood ratio is

    R_n=f1/f0
       =exp(H_n)[1-H_u-H_v+H_u H_v+H_uv].                 (5)

All derivatives in (5) are with respect to u,v. The transformation is the same bijection in both worlds, so it preserves KL. Using n+1 to transform only the alternative would change its margins and would not justify (5).

## 3. A growing-box C2 expansion with a uniform remainder

Let t=1/n, A=exp(tu)-1, B=exp(tv)-1, q=c-2. The inherited positive double-integral identity, rescaled to the unit square, is

    h=S/(xy)^c-1=c(1-c) A B I,
    I=integral_[0,1]^2 (1+B s+A r)^q dr ds.                (6)

For L>=0 with tL<=1, set p=1+L and define ||f||_2 as the largest supremum on [0,L]^2 of any partial derivative of total order at most two. All constants K below are numerical, independent of n and L; their value may increase between displays. Leibniz's rule gives ||fg||_2<=4||f||_2||g||_2.

Put E(u)=(exp(tu)-1)/t and F(v)=(exp(tv)-1)/t. Taylor's theorem and exp(tu)<=e give

    ||E||_2, ||F||_2 <= e p,
    ||E-u||_2, ||F-v||_2 <= e t p^2.                     (7)

Here a univariate function is viewed as a function on the square, with the other derivatives zero. Since -3/2<=q<-1 and W=1+Bs+Ar>=1, direct differentiation under the finite integral gives

    |I-1| <= 2(A+B) <= 2e t(u+v),
    |I_u|,|I_v| <= 2e t,
    |I_uu|,|I_vv| <= (6e^2+2e)t^2,
    |I_uv| <= 6e^2 t^2.                                  (8)

For example I_u=q A' integral r W^(q-1), and I_uu is the sum of q(q-1)(A')^2 integral r^2 W^(q-2) and q A'' integral r W^(q-1). The mixed derivative contains q(q-1)A'B' integral rs W^(q-2). The bounds use |q|<=2, |q(q-1)|<=6, A',B'<=et, A'',B''<=et^2, and W raised to any displayed negative power at most one. Differentiation is legitimate on these compact squares because the denominator is at least one and the derivatives are continuous. Thus

    ||I||_2<=K,  ||I-1||_2<=K t p.                        (9)

The factor m(1-c)=1 is exact. Hence J=mh=c A B I=c t^2 E F I. Using |c-1|<=t and (7)-(9), expand cEFI-uv as

    (c-1)EFI + (E-u)FI + u(F-v)I + uv(I-1).

Leibniz's bound proves

    ||J-t^2 uv||_2 <= K t^3 p^3,
    ||J||_2 <= K t^2 p^2,
    ||h||_2=||J/m||_2 <= K t^3 p^2.                      (10)

To pass from J to H=m log(1+h), note h>=0. For phi(z)=log(1+z)-z and z>=0,

    |phi(z)|<=z^2/2, |phi'(z)|<=z, |phi''(z)|<=1.

The first and second derivative chain rules, and m<=2/t, therefore imply

    ||H-J||_2=||m phi(h)||_2 <= K t^5 p^4.

Combining this with (10), and t<=1,p>=1, gives the explicit polynomial remainder

    ||H-t^2 uv||_2 <= K t^3 p^4.                          (11)

Now fix ANY constant C>4 and choose L=L_n=C log n (for n>=2). Eventually tL<=1. Equation (10) and the preceding logarithm estimate show ||H||_2=O(t^2 p^2) on these boxes, since t^3p^2 tends to zero. In particular ||H||_2 tends to zero. Expand exp(H) in (5); every product of two or more H derivatives or H factors is O(t^4 p^4). By (11), uniformly on the entire growing square,

    R_n=1+t^2 k(u,v)+r_n(u,v),
    k(u,v)=(1-u)(1-v),
    sup |r_n| <= K t^3 p^4,
    sup |R_n-1| = O(t^2 p^2).                             (12)

The last estimate uses tp^2->0. Equations (7)-(11) supply the derivative control required to expand the density, rather than only expanding a CDF pointwise. No global L2 bound is asserted: it would contradict the predecessor's infinite chi-square result.

## 4. Entropy outside the growing square

The predecessor's global density estimate in x,y coordinates is

    f1_XY(x,y) <= C_n/(xy),
    C_n=n^2+n/(n+1).

The Jacobian of the common transformation is xy/n^2. Therefore

    f1(u,v)<=C_n/n^2<=3/2,
    log R_n <= a+u+v, a=log(3/2).                         (13)

Let B_L=[0,L]^2 and T_L its complement. The common exponential margins give P_i(T_L)<=2exp(-L), for both i=0,1. More importantly, arbitrary dependence does not spoil the required tail first moment. By the layer-cake identity,

    E1[U 1_{V>L}]
      =integral_0^infinity P1(U>s,V>L) ds
      <=integral_0^L exp(-L) ds + integral_L^infinity exp(-s) ds
      =(L+1)exp(-L).                                      (14)

The same bound holds with U,V exchanged, while E1[U 1_{U>L}]=(L+1)exp(-L). Splitting the union T_L gives

    E1[(U+V)1_{T_L}] <=4(L+1)exp(-L).                     (15)

Thus the positive entropy contribution on T_L is at most [2a+4(L+1)]exp(-L). Its negative contribution in absolute value is at most P0(T_L)/e, because -z log z<=1/e on 0<z<1. In particular the ordinary entropy tail is absolutely bounded by

    integral_(T_L) f1 |log R_n|
      <=[2a+4(L+1)+2/e]exp(-L).                          (16)

For an especially direct mass-corrected calculation, use psi(z)=z log z-z+1>=0. Since the densities both integrate to one and the entropy is finite,

    D_n=integral f0 psi(R_n).

Pointwise, f0 psi(R_n)<=f1(log R_n)_+ + f0. Consequently

    0<=integral_(T_L) f0 psi(R_n)
      <=[2a+4(L+1)+2]exp(-L).                            (17)

With L=C log n and C>4, n^4 times either tail bound tends to zero. This is a uniform entropy-tail argument and does not assume independence in P1. Equivalently, if one expands R log R directly, its first-order bulk term is P1(B_L)-P0(B_L), the negative of the tail mass discrepancy, whose absolute value is at most 4exp(-L). The centered function psi incorporates this cancellation exactly.

## 5. The limiting coefficient

On B_(L_n), put delta=R_n-1. By (12), sup|delta| tends to zero. Taylor's theorem, uniformly for |delta|<=1/2, gives

    psi(1+delta)=delta^2/2+O(|delta|^3).

Since sup|k|<=p^2 and sup|r_n|<=K t^3p^4, (12) gives

    sup |t^(-4)delta^2-k^2| <= K(tp^6+t^2p^8) ->0,
    t^(-4) integral_(B_(L_n)) f0 |delta|^3
       <= K t^2p^6 ->0.                                  (18)

The reference density integrates to at most one on each box. Also the boxes increase to the whole quadrant, and

    integral_0^infinity exp(-u)(1-u)^2 du = 1-2+2 = 1.

It follows that the scaled bulk entropy tends to

    (1/2) integral_[0,infinity)^2 exp(-u-v)k(u,v)^2 du dv
      =1/2.                                              (19)

Combining (17)-(19) proves (2). The far tail that destroys L2 integrability has negligible n^4-scaled entropy. There is no contradiction between the two divergence conclusions.

## 6. Transport to adaptive face-only words and stopping

For one retained vector, a coordinate-face probe at (a,1) returns the comparison T_A<=a, and a probe at (1,b) returns T_B<=b, up to null equality conventions. Given the pair of minima and the protocol's common random seed, one can simulate every next comparison, every command chosen from earlier bits, and the complete finite transcript. Thus every finite adaptive face-only word is a common Markov kernel of the exact pair. Data processing gives its conditional KL at most D_n. Word length and selected thresholds may depend on previous replicates and current face bits; no finite length or precision cap is needed for this upper bound.

Consider protocols that use a fresh independent vector for each replicate, retain it unchanged during its face-only word, and never count repeated access to that same vector as a fresh independent replicate. The policy, including all command and stopping randomization, is common in both worlds. Conditional on every finite action history, a newly drawn independent vector has the stated P0 or P1 law. Use finite ACTUAL-ACTION prefixes, not a sequence indexed only by completed words, as follows.

Augment the protocol by revealing the full pair of minima when the first face probe on a new retained vector is started. Charge that vector at this first action, even if its word never finishes. Continue to simulate the original policy from its original observed bits and randomization, ignoring any extra revealed information when making its decisions. The augmented history contains the revealed minima as well. A new reveal contributes exactly D_n conditional KL; later probes of that vector are deterministic functions of the already revealed pair and the selected commands, and contribute zero additional oracle KL. The policy choices themselves have the same kernel in both worlds. After termination pad with a common dummy symbol. For the augmented history through the first T actual actions, the chain rule gives

    KL(Law1(history_T)||Law0(history_T)) <= D_n E1[N_T].    (20)

Here N_T is the number of independent retained vectors STARTED by action T. Thus the history and its cost remain defined on a path that keeps probing one vector forever. Any separately allowed fresh endpoint-only observations must use distinct independent new vectors, discard them without later replay, and retain their stipulated identical conditional laws; they then add zero conditional information for this hard pair. Such zero-information additions do not alter (20). Reusing such a vector is outside this endpoint-only allowance; any vector observed more than once must remain entirely face-only and be charged from its first observation.

Require unconditional terminal correctness:

    P0(stop finitely and accept P0)>=1-alpha,
    P1(stop finitely and reject P0)>=1-alpha,
    0<alpha<1/2.                                         (21)

For E_T={stop within T actual actions and reject P0}, binary data processing bounds the left side of (20) below by kl(P1(E_T),P0(E_T)). Let T tend to infinity, using monotone convergence of E1[N_T] and lower semicontinuity of binary KL. The limiting rejection event has P1 probability at least 1-alpha and P0 probability at most alpha, giving D_n E1[N]>=kl(1-alpha,alpha), where N counts all independent retained vectors started. This proves (3), with infinite expected cost satisfying it trivially. Correctness only conditional on termination would not justify the claim. No almost-sure completion of individual words is needed for this actual-action argument; the data-processing statement for each finite word also remains valid on its own.

The cost in (3) is independent retained vectors, not an uncharged exact readout or a fixed number of face probes. The old two-face experiment is contained in this enlarged interface. The result excludes interior AB probes on retained vectors, gate-level bits, route labels, changing latent states, unknown-calibration effects, and other observation channels. It does not identify a physically optimal instrument, establish a minimax constant, or transfer an all-wrong-count certificate to a new design.

## 7. What is inherited and what this packet establishes

The Joe construction, positive integral, full law and density bound, infinite-chi-square obstruction, and two-face sharp KL constant 0.2096995101... are inherited from the bound predecessors. The common-transform/growing-box approach and candidate coefficient were supplied by the parent for attack. This packet proves the derivative remainder, entropy-tail control, limiting coefficient, and bounded face-only data-processing extension. Taylor expansion, entropy truncation, layer-cake integration, KL data processing, and the sequential change-of-measure argument are ordinary inherited mathematics; no field-wide novelty claim is made.

The full-readout coefficient 1/2 exceeds the old nonadaptive two-face maximum coefficient 0.2096995101..., while their exponents agree. This compares one-replicate information constants for the specified hard pair. It does not prove the corresponding ratio for any practical sample or probe cost.

CONTROL_RESULTS.json records bounded deterministic algebraic and numerical diagnostics, not empirical sampling and not a substitute for the proof. SOURCE_AUDIT.md records exact inspection scope. A separate fresh independent review must be bound to the final RESULT.md hash before this packet is marked accepted.
