# Independent review: compact initial law preservation

10 October 2026 UTC. Ordinary mathematical review and exact finite algebraic controls. No Lean, field-priority, protected integration, or research-closure claim. The reviewer did not edit the root proof.

## Verdict and binding

**Pass for the stated SOS/shifted-SOS theorem.** No unresolved mathematical defect was found in the corrected result:

- File: `compact-initial-law-preservation-20261010/RESULT.md`
- Reviewed SHA-256: `6943a1c274b177d107c8935e7d12d6a9e5094aa79df41546fb8e7d4d121914ce`

The originally assigned digest was `495e0dc0a6f5f10f4bceb7c563bc7cdd83540583f416f7487caea5a7fd682350`. That version contained an overbroad inherited-interface statement. The reviewer reported it, and the author corrected the two affected passages. This verdict applies to the corrected digest only.

The theorem concerns every **finite** dimension d. The notation R^d supplies that restriction; no infinite independent-coordinate statement is being approved. “Polynomial functional” is read throughout in its standard intended sense of a real **linear** functional.

## 1. Resolved scope defect

The inherited finite-channel programme uses arbitrary signed linear energies h_t(x)=u(t)·x. A nonconstant linear polynomial cannot be made globally nonnegative, and therefore cannot be made SOS, by adding any scalar. Already h(x)=x gives h(-c-1)+c=-1 for every shift c.

Thus the new theorem does not, by itself, force the whole original linear-control hierarchy from initial compact support and all-time square positivity. Its finite-support corollary is valid for its supplied SOS/shifted-SOS energies. The corrected result now states this restriction expressly in the introduction and Section 4. Nonnegativity only on the initial K has not been substituted for global SOS: doing so in the monotonicity step would presuppose the very support preservation being proved.

## 2. Static square-order domination lemma

The proof is valid, including the zero-mass case.

1. Polynomial Cauchy–Schwarz and 0<=A(1)<=1 imply |A(p)|²<=integral p² dmu. If p=0 in L²(mu), this gives A(p)=0. The functional therefore descends and extends boundedly to L²(mu).
2. Restricted polynomials are uniformly dense in C(K) by Stone–Weierstrass and consequently dense in L²(mu). The Hilbert representative a is real and in L²(mu), hence in L¹(mu), since mu has finite mass.
3. For nonnegative f in C(K), approximate sqrt(f) uniformly by real polynomials. The squared approximants converge uniformly to f, so both sides of the square-order inequality pass to the limit. Positivity of the finite signed measures a mu and (1-a)mu against every nonnegative continuous f gives 0<=a<=1 almost everywhere.
4. No representative outside K is accidentally omitted. For any positive representative nu on R^d, even coordinate moments give nu(|x_i|>=R+epsilon)<=(R/(R+epsilon))^(2n) for all n. Taking n to infinity and then a countable union in epsilon and the coordinates forces nu onto [-R,R]^d. Polynomial density on that box then identifies nu with a mu, including its support within K.

The argument genuinely uses compactness. The contrast construction supplies a nonmoment square-positive functional dominated in square order by an unbounded moment measure. Dividing that measure and functional by its finite mass converts the dominating measure to a probability if desired, so normalization does not remove the contrast.

## 3. Dynamic domination

On a compact time window, the degree bound gives finitely many coefficient functions. Their continuity and coordinate continuity of L make t->L_t(g_t) continuous. The integrating factor b is therefore positive and C¹, with A'_t(p)=-A_t(g_t p) for every fixed polynomial p.

For every fixed q, g_t q² is SOS at each time. No continuous choice or differentiation of SOS factors is required. Hence A_t(q²) decreases, and positivity yields 0<=A_t(q²)<=mu(q²). The static lemma supplies a unique nu_t<=mu at each t, rather than an arbitrary or unproved measurable selection of representatives.

There is no coercivity, damping-rank, or hidden-coordinate bound beyond finite ambient dimension at this step. Full square positivity at every time remains an essential premise; compact support at time zero does not independently prove that premise.

## 4. Weak extension and total-variation uniqueness

The time-extension argument is complete. If p_n converges uniformly to f on K, then uniformly for s in [0,H],

    |nu_s(p_n-f)| <= ||p_n-f||_infinity,
    |nu_s(g_s(p_n-f))| <= M ||p_n-f||_infinity.

The integrated equation therefore passes to f with an error bounded by (2+HM)||p_n-f||_infinity, and weak continuity follows by uniform approximation from continuous polynomial coordinates. In particular s->nu_s(g_s f) is continuous: split a time increment into the weakly continuous pairing with a fixed continuous function and the uniformly small change in g_s f.

The explicit measure nu*_t has the same equation by bounded differentiation on K. Both nu_t and nu*_t have mass at most one. The total variation D(t) of their difference is at most two. The unit ball of C(K) is separable in the uniform norm, so D is the supremum of countably many continuous absolute pairings and is Borel measurable. No total-variation continuity was assumed.

For each fixed continuous f with norm at most one, the difference equation gives |delta_t(f)|<=M integral_0^t D(s) ds. Taking the supremum yields the displayed integral inequality for D. Applying integral Gronwall to this bounded measurable function is legitimate and gives D=0 at every t. This establishes the precise tilt, including uniqueness among all positive representatives. Division by b=nu_t(1)>0 is safe.

The displayed converse is C¹ because K is compact and the supplied schedule is continuous and locally degree bounded. Continuation means continuation along a supplied schedule retaining the theorem's hypotheses, not an assertion about an unspecified future energy.

## 5. Finite vanishing ideal

For the finite support S, p in I(S) gives A_0(p²)=0. Positivity and monotonicity force A_t(p²)=0. Cauchy–Schwarz then gives A_t(pr)=0 for every polynomial r. Thus the full ideal remains null, not merely a finite tested list of its elements.

The evaluation map R[x]->R^S is surjective by finite interpolation and has kernel I(S). The functional therefore descends to R^S. For interpolating idempotents e_j, e_j²-e_j lies in the ideal, so A_t(e_j)=A_t(e_j²)>=0. Their sum is one modulo the ideal. These are exactly the atomic masses. Zero initial weights remain zero by domination. This supplies the claimed purely algebraic support argument without first assuming a representing measure.

## 6. Executed exact finite controls

`check_controls.py` passed and wrote `CONTROL_RESULTS.json` and `check_controls.log`. These are discriminating finite controls, not a proof of universal positivity by sampling.

Use the three support points

    (0,0,0), (1,2,-1), (2,-1,3)

with initial weights (1/2,1/3,1/6). Let x be the active coordinate and use h=x², leaving two independent ambient coordinates undamped. The full evaluation algebra is presented by

    P(x)=x(x-1)(x-2),
    y=(9x-5x²)/2,
    v=(5x²-7x)/2.

The script checks exact Lagrange idempotent products, partition of unity, square reduction for arbitrary atom values (q0,q1,q2), and multiplication by x². In particular the polynomial square is represented exactly by the three squared atom values, rather than tested only through a fixed moment degree.

Writing z=exp(-t), the unnormalized square form is

    [3q0²+2z q1²+z⁴ q2²]/6,

and its difference from the initial square form is

    [2(1-z)q1²+(1-z⁴)q2²]/6.

These exhibit square positivity and square-order domination for 0<z<=1. The normalized hierarchy is verified symbolically for arbitrary observable values q0,q1,q2. The time-varying SOS example h_t=(x+t)² is also checked, including its exact integrated energy j²t+jt²+t³/3 at atom j.

At t=log(2), the exact unnormalized weights are (1/2,1/6,1/96), the normalizer is 65/96, and the normalized weights are (48/65,16/65,1/65). The coordinate means are (18/65,31/65,-1/5). No floating point or numerical quadrature enters these controls.

## 7. Project-relative contribution and retained boundaries

The following retained results were read for scope rather than inferred from their filenames:

- `measure-moment-continuation-boundary-20261009/RESULT.md`, Section 3: compactly supported **actual laws** are determined by all their polynomial moments and therefore have a determined admitted tilt. That is static determinacy plus a declared law-level update. It does not show that every full-square-positive hierarchy path initially matching a compact law stays representable or stays on K.
- `tensor-moment-continuation-20261009/RESULT.md`: owns fixed finite-support interpolation, tensor closure, linear-control tilts, and the inherited continuation interface. The current ideal argument and forced lifting are additional initial-support preservation statements only within the new SOS energy class; finite interpolation itself is not a new contribution.
- `cumulative-square-positivity-20261010/RESULT.md`: obtains law existence without initial representability through cumulative radial SOS damping. The compact-initial theorem trades that damping condition for a strong initial-law condition. It is complementary, not an unqualified strengthening.
- `coercive-square-positivity-20261010/RESULT.md`: covers autonomous coercive polynomials without requiring SOS. The new result covers noncoercive supplied SOS schedules, but does not extend that theorem to all noncoercive or merely nonnegative energies.
- `partial-cumulative-law-persistence-20261010/RESULT.md`: starts from one positive-time joint representative and propagates it under partial cumulative damping. The new theorem creates positive-time representatives from the stronger compact initial datum; it requires neither that positive-time premise nor cumulative radial control.
- `valid-initial-partial-escape-20261010/RESULT.md`: demonstrates escape from an actual, unbounded, indeterminate initial law with all-time strict full-square positivity. Its square-order domination is compatible with failure of measure representation because the dominating law is not compactly supported. It is not a counterexample to this theorem.

The defensible new project-relative implication is therefore: compact initial law + this SOS hierarchy + all-time full square positivity forces the unique law-level tilt without imposing future support or full/partial coercivity. This does not settle unbounded determinate initial laws, effective recognition of compact support from finite observations, finite-cutoff validity, arbitrary signed linear energies, or an infinite-coordinate analogue.

## 8. Optional precision improvements

No further correction is needed for the mathematical verdict. For maximal standalone clarity, the opening statement could say “real linear polynomial functional” and “1<=d<infinity” explicitly. Those are clarifications of the intended standard conventions, not newly added substantive hypotheses.
