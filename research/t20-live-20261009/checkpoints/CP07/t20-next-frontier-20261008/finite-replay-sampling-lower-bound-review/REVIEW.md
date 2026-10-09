# Independent adversarial review: fixed-pair replay sampling lower bound

8 October 2026 UTC. Separate prospective scratch review. All author and predecessor files were treated as read-only.

**Mathematical verdict: PASS within the stated instrument and model.** The all-n constants, fixed-budget consequence, adaptive allocation argument and potentially infinite stopping extension are valid. The exact frozen author manifest has SHA-256 3f7db7a3045f45135af93f82130791635cb56c808caf9aae89d137966095fa23; RESULT.md has SHA-256 56ad31e7d6495412585b13e10a400bc697746cbefa28f5080ae7864b0f21cd26. REVIEW_RECEIPT.json binds all nine author payloads and the manifest. This verdict does not extend to unbound changes.

## 1. Reviewed claim

For n>=1, m=n+1, c=n/m and t=1/[3(n+1)], the fixed paired-face replay instrument has pair laws

P0=(A^2,A(1-A),A(1-A),(1-A)^2),
P1=P0+(Delta,-Delta,-Delta,Delta),

where A=(1-t)^n and 0<Delta<=4/[25(n+1)^2]. The claimed sufficient entropy bound is

KL(P1||P0)<=3136/[625(n+1)^4].

A common policy with unconditional terminal correctness at least 1-alpha in each world, 0<alpha<1/2, therefore requires

E_Joe[number of paired replay actions]>=625/3136 (n+1)^4 kl(1-alpha,alpha).

This remains true when stopping can be infinite and arbitrarily many fresh single endpoints at adaptively selected commands are allowed. The count is under Joe. A fixed or almost-sure maximum replay budget inherits the same lower bound.

## 2. Independent proof audit

INDEPENDENT_DERIVATION.md supplies the independent derivation recorded before the author's result was read. The following key steps were separately checked:

- The Joe law is a valid command-independent joint threshold distribution; its shared H_c calibrations and m independent route pairs give exact equality of all fresh endpoint responses.
- S-B=p^c[2-(1+t)^c-(1-t)^c], with 0<B<S<1.
- The positive concavity gap is an integral against weight t-|x|, whose total is t^2. This gives the correct factor c(1-c), without a missing factor two.
- m c(1-c)=c, p>=5/6 and c<1 give the stated Delta constant, including n=1.
- The author floor 1/49 is safe. Independently, Bernoulli on p^-n yields the slightly stronger 2/3<A<=5/6, which is not needed for the advertised constant.
- The exact chi-square value is Delta^2/[A^2(1-A)^2]. Bounding its four terms by 49 Delta^2 each gives the author's 196 Delta^2 and entropy constant.
- Both laws have positive cells. In particular S<p^c implies S^m<A, so the subtractive off-diagonal perturbations remain positive; the loose Delta bound alone was not used as a validity argument.
- The KL direction, the expectation direction and the rejection event match throughout.

No large-n approximation or finite exhaustion is used in the all-n proof. Conservative constants are not arithmetic defects.

## 3. Adaptive allocation and stopping audit

The finite transcript includes the chosen actions, commands, observations, any randomization needed to make decisions measurable, and a common padding symbol after termination. At a common realized history, the policy has the same conditional kernel in both worlds. A fresh single endpoint then has exactly the same conditional Bernoulli law at the chosen command because its latent vector is independently redrawn. The entire fixed pair has conditional law P0 or P1.

Thus finite-prefix KL is exactly d E1[N_T]. Marginal action frequencies can differ across worlds because earlier replay histories differ; treating these frequencies as independent evidence would be wrong. The packet correctly uses conditional kernels.

The events E_T={tau<=T,reject} are measurable in the finite transcript and increase to actual terminal rejection. The assumptions give P1(E)>=1-alpha and P0(E)<=alpha without requiring almost-sure termination. Data processing at every finite T, monotone convergence for N_T, and lower semicontinuity of binary KL yield the result. No unbounded-time optional-stopping identity or terminal transcript likelihood is needed.

The proof permits infinite E1[N_infinity], where the inequality is immediate. Nontermination is included in the failure budget and is never counted as a correct decision. A concrete rare-entry countercontrol in BOUNDARY_ATTACKS.md shows why replacing these assumptions by conditional-on-stopping correctness would be invalid.

## 4. Independent executable controls

Run:

    python independent_controls.py

The script imports no author code and writes only this review sibling. Its retained report records 4,922 passed assertions, mostly exact pathwise likelihood checks. The substantive control families are:

1. Five exact symbolic/rational identities for the chi-square expression and constants.
2. Thirty-six actual Joe examples, n=1..32,64,100,256,1000. Integer root inequalities certify dyadic enclosures of the algebraic powers. Rational comparisons certify strict Delta positivity, the advertised upper bound, all replay cell positivity, the baseline interval/floor, and the entropy upper bound through chi-square.
3. Five prefixes of an independent rational four-cell adaptive-tree proxy. Exact rational products cancel common policy and fresh-probe factors; each replay-outcome log coefficient equals E1[N_T] times its P1 probability. Prefix masses normalize under both laws, and stopped branches retain their accumulated counts.

The frozen author controls were also replayed in the isolated author_snapshot directory: all 2,043 assertions in 27 families pass, and both result JSON and stdout are byte-identical to the frozen originals. The original author packet remains unchanged.

The finite adaptive tree is expressly a rational proxy for chain-rule bookkeeping, not an assertion that its artificial rational P1 is the exact Joe law. Approximate display columns are not used in assertions. These controls supplement the universal analytic arguments; they are not formal proof verification or empirical experiment results.

## 5. Boundaries and comparison to the upper test

The informative action is one atomic pair returning both fixed-command bits. Earlier fresh probes cannot be repurposed as held-threshold observations. The proof does not use an uncharged first-face screening convention or assert a bound for only selectively completed pairs.

Within the same fixed instrument and shared model, the separately reviewed upper reference test uses O(n^4 log(1/alpha)) paired replays and the same number of fresh diagonal trials. The hard Joe alternative is a member of its wrong-count class. Therefore the n^4 exponent matches at every fixed alpha in (0,1/2), and small-error logarithmic dependence matches as alpha decreases to zero. The explicit alpha<=1/4 qualification is valid: (1-2alpha)>=1/2 and (1-alpha)/alpha>=alpha^-1/2, hence kl>=one quarter log(1/alpha).

The comparison does not hold uniformly in the form kl comparable to log(1/alpha) as alpha approaches 1/2. The packet does not make that claim. Nor does it establish optimal constants, a globally optimal instrument, an unknown-calibration selection algorithm, a general count estimator, physical replay availability, productive occurrences or empirical validation.

## 6. Disposition

No mathematical correction was required in the inspected RESULT.md. The review retains the exact experiment, shared marginal/route-independence assumptions, fresh-replicate independence, stationary law, calibrated-command qualification, natural-log convention, alpha range and unconditional terminal contract. SOURCE_AUDIT.md separates inherited tools and targeted source reading from the application-specific derivation. BOUNDARY_ATTACKS.md records unsuccessful attacks within scope and genuine failures after changing the scope.

This verdict is a bounded mathematical review. It neither validates the model assumptions in an application nor confers checkpoint inclusion, protected integration, general research readiness or T20 closure.
