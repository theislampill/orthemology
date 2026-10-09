# Choosing the second face after the first bit preserves the chi-squared supremum

8 October 2026 UTC. Separate successor to the frozen arbitrary-face-replay-design packet. The seventh checkpoint sealed before this successor was reviewed and frozen, so this addendum is excluded from that checkpoint. Earlier files remain unchanged.

## 1. Exact result

Use the same reference n-route product world and alternative Joe world with m=n+1,c=n/(n+1). The frozen predecessor proves, for every nonadaptive face pair (a,1),(1,b),

    d_chi(a,b):=chi²(P1^(a,b)||P0^(a,b)) <=32768/n^4.

Now permit the following attempted replay. Select a, draw a fresh threshold vector, probe (a,1), and observe its absence bit X. After observing X, a common randomized policy may choose b and probe (1,b), using the SAME realized thresholds, or abort the attempt. The first command, selected second command or abort decision, and all observed bits are part of the transcript. Choices may also depend on completed earlier attempts and common randomization. No hidden threshold access, gate-law change, mutation, or third probe is allowed. Distinct attempts redraw independent threshold vectors.

For a fixed a in (0,1), let A=(1-a)^n. Write mu_1 and mu_0 for the two conditional laws of the second choice after X=1 and X=0, each a probability law on [0,1] together with an abort symbol. Define d_chi(a,abort)=0. Then the exact one-attempt identity is

    chi²(adaptive transcript under 1 || under 0)
       =(1-A) integral d_chi(a,b) dmu_1(b)
          + A integral d_chi(a,b) dmu_0(b).                  (1)

In particular its chi-squared divergence, and hence its Joe-oriented KL divergence, is at most 32768/n^4. A common randomized first command averages these conditional divergences and obeys the same bound. Hiding action labels or common random seeds cannot increase either divergence.

Since a nonadaptive pair is included as mu_1=mu_0 concentrated at one b, equation (1) proves an exact equality for every n:

    sup_(all such adaptive attempts) chi²
        =sup_(a,b fixed before the pair) chi²(P1^(a,b)||P0^(a,b)).  (2)

Thus the predecessor's sharp chi-squared supremum asymptotic, 0.4193990202.../n^4, transfers to this enlarged two-face instrument. Its nonadaptive rate a=b=1-exp(-u*/n), u*=1.5936242600..., remains asymptotically optimal for chi-squared. Equation (2) alone does not characterize every adaptive optimizer or optimize adaptive KL; neither is needed here.

## 2. Derivation and literal boundaries

The reference face bits are independent. At the fixed second rate b their common absence margins are

    P0(X=1)=P1(X=1)=A,
    P0(Y=1)=P1(Y=1)=B=(1-b)^n.

Write Delta=P1(X=1,Y=1)-AB. The retained-threshold construction means that conditioning on X and then choosing b accesses the conditional law from this SAME fixed-(a,b) experiment. It does not invent a new coupling after X.

For interior a,b,

    P0(Y=1|X=1,b)=P0(Y=1|X=0,b)=B,
    P1(Y=1|X=1,b)=B+Delta/A,
    P1(Y=1|X=0,b)=B-Delta/(1-A).

The chi-squared divergence between Bernoulli(p) and Bernoulli(q) is (p-q)^2/[q(1-q)]. Therefore the first branch's common probability A times its conditional divergence is

    A [Delta²/(A² B(1-B))]
       =(1-A) d_chi(a,b),                                  (3)

using the predecessor identity d_chi=Delta²/[A(1-A)B(1-B)]. The other branch's weighted contribution is A d_chi(a,b). Summing at the two selected rates proves (1) for deterministic choices.

For randomized choices, conditional on the already observed X, the policy kernel mu_X is identical under both worlds and is independent of unobserved thresholds given the available history and X. Its likelihood factor cancels. The chi-squared integral over the recorded command is exactly the integral of the conditional chi-squared values. This proves (1), including discrete, continuous, or mixed command distributions. Abort gives the same deterministic continuation in both worlds and contributes zero. The first bit itself contributes no divergence because its marginal is identical.

If a is 0 or 1, X is deterministic in both worlds; the unobserved branch has probability zero. Every second-face marginal is still identical, so the entire adaptive attempt has zero divergence. If a is interior but b is 0 or 1, Y is deterministic in both worlds and that branch contributes zero. Common zero-mass cells are removed rather than divided by; the interior conditional formulas are not used where their denominator vanishes.

Without using the reference's independence, the generic branch-KL argument proposed by the parent would still bound each weighted conditional branch by the full nonadaptive KL at that branch's selected rate. Summing two branches gives the valid but weaker 2*32768/n^4 bound. Here the exact chi-squared coefficients in (3) sum to one, removing that factor two. This refinement relies on the stipulated product reference and equal two margins.

## 3. Cost, adaptive policies across attempts, and stopping

Charge one replay attempt as soon as its FIRST face probe is made. Aborted attempts and attempts screened out after their first bit are charged. If both probes are always completed, this is the ordinary pair count. The total number of endpoint probes is at least the attempted-replay count, and is twice that count when every attempt completes both probes. A cost convention making first probes free and charging only selected completions is not covered.

For a common policy across attempts, condition on the history before each charged first probe. Its chosen first rate has a common conditional kernel; the observation channel for the ensuing first bit, selected second rate or abort, and possible second bit satisfies the one-attempt bound above. A stop decision after X is included as an abort/terminal continuation. No extra information comes from a common policy decision conditional on the data already observed.

The frozen predecessor's finite-prefix KL argument therefore applies with attempts replacing atomic nonadaptive pairs. For any finite prefix,

    KL(Law_1(history)||Law_0(history))
       <= (32768/n^4) E1[number of started attempts].          (4)

Optional fresh single-endpoint observations still have equal conditional laws, provided their thresholds are independently redrawn and cannot later be repurposed as retained probes. For 0<alpha<1/2 impose unconditional terminal correctness:

    P0(stop finitely and accept reference)>=1-alpha,
    P1(stop finitely and reject reference)>=1-alpha.

Apply binary data processing to rejection by each finite prefix, then monotone convergence for the charged count and lower semicontinuity for binary KL, exactly as in the reviewed predecessor. The result is

    E1[N_attempt] >= (n^4/32768) kl(1-alpha,alpha).             (5)

It includes infinite stopping times only under that unconditional correctness promise; nontermination consumes failure probability. A fixed attempt budget obeys the same bound. The endpoint-probe cost also obeys (5), since it is at least N_attempt. The expectation is under the Joe alternative, not asserted for both worlds.

## 4. Why free first-bit screening would change the conclusion

There is an exact obstruction to silently charging only completed pairs. Set B=1/2 by choosing b=1-2^(-1/n), and repeatedly start fresh first-face probes until X=1. Observe the second face only on that success. The first-bit success probability A is the same under both worlds, so the geometric screening count alone carries no information. But the selected second bit has law Bernoulli(1/2) in the reference and Bernoulli(J1/A) in the Joe world.

For fixed n and y=1-b in (0,1), let x=1-a decrease to zero. Since c<1,

    S=x^c+y^c-[y+x(1-y)]^c =x^c-O(x),
    J1/A =S^(n+1)/x^n ->1.                                 (6)

Thus a can be chosen, separately for each n, so that J1/A>=3/4. If all unsuccessful first probes were free, each charged selected second bit would distinguish two Bernoulli parameters separated by at least 1/4, uniformly in n. At k independent selected completions, reject the reference when the mean absence bit is at least 5/8. The one-sided Hoeffding bounds for both errors are at most exp(-k/32), so k>=ceil[32 log(1/alpha)] suffices in this altered cost model. The expected number of first probes per completion is 1/A and is not free under (5).

This is not an improved design under the declared attempt cost. It shows concretely why the cost condition matters and why a lower bound on attempts cannot be relabeled a lower bound on selectively completed second probes. No empirical implementation or practical screening recommendation is claimed.

## 5. Scope and attribution

The parent proposed the general two-branch KL argument and required explicit first-probe charging. The author observed the exact chi-squared weighted-average identity, which removes the factor two, and supplied the free-screening countercontrol. These use the frozen predecessor's product-reference/equal-margin law and all-rate theorem. No frozen exclusion is silently edited: this separately reviewed successor discharges the second-command-adaptation exclusion for the exponent and chi-squared supremum under its stated cost, while preserving the earlier bytes and checkpoint cutoff.

The extension remains restricted to at most two coordinate-face observations on a retained vector. It does not address longer words, hidden gate access, calibration selection, gate-law changes, physical feasibility, full adaptive KL optimization, sharp sample constants, protected integration, or T20 closure.
