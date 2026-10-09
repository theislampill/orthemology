# Independent review: interaction-absence approximation obstruction

8 October 2026 UTC. Mathematical verdict: **PASS within the stated oracle and
model contracts**. Final byte identities are recorded separately in
REVIEW_RECEIPT.json. This is a scoped independent review, with no release,
protected integration, owner acceptance, physical validation or T20 closure
authority. All review writes are confined to this new sibling.

## 1. Accepted conclusion

There is no always-terminating, universally correct finite adaptive procedure
that decides whether AB is absent or present from certified pointwise population
Cauchy queries in the stated unrestricted finite-count model. A query names a
rational command in the closed square and a strictly positive rational error
tolerance. A reply is a rational approximation center with that error guarantee.
Correctness is required for every valid fixed total oracle name. No common
query, precision, or computation bound is assumed or needed.

The same witness rules out an almost-surely terminating randomized procedure
whose error is uniformly at most delta for any fixed delta < 1/2, for every
allowed world and every valid name. Zero-error almost-sure termination is an
immediate special case. Internal randomization is independent of the unknown
world, and the customary measurability of protocol/output events is assumed.
This is not a result about uncertain Bernoulli data, actual calibration, or
philosophical existence and nonexistence.

The negative result already holds with two known roots, n_AB in {0,1}, no B-only
routes, known identity B calibration, computable response functions and
computable names, and a supplied common response Lipschitz constant 3. Individual
inventories are finite; their nuisance unary counts are not uniformly bounded.

## 2. Independent derivation of the hard family

In the base, n_A=1, n_B=n_AB=0 and both maps are identities. Thus Q_0(a,b)=1-a.
In alternative N>=1, n_A=N, n_AB=1, n_B=0, and the single shared A calibration is

    r_A,N(a) = 1-(1-a)^(1/N).

It is a static strictly increasing continuous endpoint-preserving map, used in
the unary routes and the AB route alike. B remains identity. The model's
independent-route law gives, with u=1-a,

    Q_N = (1-r_A,N)^N (1-r_A,N b)
        = u(1-b)+b u^(1+1/N).

No within-world count variation, mixture, support-specific calibration or
cross-talk is being introduced. A root is allowed to be unused, as in the
predecessor model; the known-root-set promise does not require every root to
occur in every inventory.

Put u=t^N. The nonnegative difference is b t^N(1-t). Maximization over b gives
b=1. The derivative in t is t^(N-1)[N-(N+1)t], positive to the left of
t=N/(N+1) and negative to the right. The endpoints give zero. Consequently

    max |Q_N-Q_0| = N^N/(N+1)^(N+1) < 1/(N+1).

The maximizing nominal point is rational: a=1-[N/(N+1)]^N, b=1. This is an exact
supremum, not a sampled or asymptotic estimate. It covers the entire closed
square. On b=0, a=0 and a=1 the two laws coincide exactly; the b=1 face contains
the maximum. Issued-root profile masks add no missing observation in this
unguarded model. Guards would require different semantics and are excluded.

The derivative bounds |partial_a Q_N|<=2 and |partial_b Q_N|<=1 extend by
one-sided limits to the boundary, proving the common sup-norm Lipschitz bound 3.
There is no corresponding common calibration modulus: the input pair
1-2^(-N), 1 has separation 2^(-N), while its r_A,N values have separation 1/2.
A known modulus for observable Q is therefore not a loophole; a restrictive
known common modulus for the hidden maps is a different promise.

## 3. Adaptive, fixed-name and termination attacks

**Finite base stopping.** The exact base name O_0(a,b,epsilon)=1-a is valid for
every rational query and has strict error slack at every positive tolerance.
A purported deterministic decider must return ABSENT on this name after
finitely many queries. There is no need for a uniform stopping or precision
bound across inputs. The finite transcript has a positive minimum tolerance.
For zero queries, the same unsupported output is already wrong on an alternative.

**One fixed extension.** Choose N so that 1/(N+1) is below the minimum base
tolerance. Define a total alternative oracle to return 1-a when
epsilon>1/(N+1), and otherwise return a fixed rational-bisection approximation
to Q_N within epsilon/2. The coarse branch is valid at all commands by the
uniform inequality; the fine branch is valid by construction. It is a single
computable query-response function. Repeated queries receive the same response;
off-transcript queries are defined; no post hoc change of world or history-
dependent replies is needed.

**Adaptive path.** The first reply agrees. Whenever previous replies agree,
the deterministic next query and finite computation agree. Induction reproduces
the entire halted base path, including its stopping decision and ABSENT answer,
under the one fixed alternative name. The answer is then wrong.

**Rational arithmetic on returned centers.** An algorithm may test its rational
reply centers for exact equality or for any other finite predicate, but those
same centers occur in both runs. Such tests do not certify equality of the
underlying population values. The strict positive tolerance is essential.

**Computability of the hard names.** For rational u, bisection on [0,1], comparing
rational N-th powers with u, encloses u^(1/N). Formula Q_N=u(1-b)+bu^(1/N)
transfers this enclosure to Q_N. Thus even restricting the worlds and oracle
names to computable examples does not repair the proposed decider.

These checks eliminate the principal quantifier hazards: the alternative is
chosen after a finite base transcript, but is then a single admissible world
with a fixed valid total name; every subsequent response on that path is valid.

## 4. Randomized strengthening

The author uses dyadic threshold levels P, without restricting the actual query
tolerances to be dyadic. Under O_0, let E_P mean that the protocol returns ABSENT,
halts, and every tolerance it requested is at least 2^(-P). The no-query path
satisfies the threshold condition. E_P increases with P, and its union is the
ABSENT-return event because each halted path has finitely many positive
tolerances. Its probability is at least 1-delta. Since 1-delta>delta, continuity
of probability from below gives one finite P with Pr(E_P)>delta.

Choose N with 1/(N+1)<2^(-P), and choose once and for all a Q_N name that copies
O_0 on every query of tolerance at least 2^(-P), using bisection on the rest.
That name is fixed independently of the random seed. Couple the two runs using
the same seed. Every seed in E_P has identical replies, queries, halt and output
under the alternative, so its error probability exceeds delta. This contradicts
the uniform guarantee. One need not select an individual seed or require an atom
of positive probability in the seed distribution.

This proof remains valid when halting time and requested precision have no
uniform bound. It does not interchange a stopping time with an infinite
transcript limit. The increasing finite-threshold events are the required
measure-theoretic step. A construction of a different alternative per seed
would have been insufficient; the author correctly avoids that mistake.

## 5. Compatible positive results and scope boundaries

For every fixed N and every interior a,b, the AB quotient is

    Q_N(a,b)/(Q_N(a,0)Q_N(0,b)) = 1-b+b(1-a)^(1/N) < 1,

while the base quotient is one. Thus the full laws are distinct. The result is
discontinuity of this binary target under the declared approximation evidence,
not an observational-equivalence counterexample to the earlier classification.

Positivity remains semidecidable, even at one fixed rational interior point.
For the general two-root model, use the multiplication-only contrast

    D=Q(a,0)Q(0,b)-Q(a,b).

Both marginal factors are strictly positive, and
D=Q(a,0)Q(0,b)[1-(1-r_A(a)r_B(b))^n_AB]. It is positive exactly when n_AB>0.
Certified shrinking intervals eventually certify D>0 in each positive world.
On a zero world they cannot certify positivity. This gives a division-free
check of the author's equivalent quotient semidecision and helps isolate the
asymmetry. The obstruction also excludes a universally sound absence
semidecider that halts on the displayed base name; divergence on positive inputs
would not prevent the copied base halt from being wrong.

The positive-support-promised half-integer procedure in the finite-panel
appendix is unaffected. Every present-support alternative here has n_AB=1;
the unknown question is whether the positive-support promise holds at all.
No finite panel identifies the whole hidden calibration function, and the
current result adds no such claim.

The following escapes are outside this proof rather than refutations of it:

- Exact rational population values explicitly certified as exact, symbolic
  response formulas, or an exact comparison/equality facility.
- Restricting to a specially selected oracle representation that furnishes
  discontinuous extra information through its selection or rounding rule.
- A common count ceiling or an additional restrictive prior on the hidden
  calibration maps that removes this unbounded sequence.
- Internal route observations, independent calibration observations, changed
  generative semantics, or a promise excluding absent support.
- Allowing failure to terminate or abstention on the absent case.

A vacuous calibration band does not remove the witness; excluding restrictive
bands does not assert that every band permits recovery. No theorem for a known
count ceiling is accepted or rejected here. The proof has no implication that
AB or any philosophical source does not exist, and it does not validate a
physical apparatus or intervention.

## 6. Controls and evidentiary weight

The separately written independent_controls.py uses integer and exact rational
arithmetic, including certified rational root brackets. Its 151,948 assertions
pass across 14 families. The families check model membership, the route-law
identity, supremum formula, derivative orientation, all masked boundary types,
uniform-gap controls, response derivative bounds, distinct full laws, fixed
total names, adaptive transcript copying (including zero-query runs), increasing
randomized precision events, positivity semidecision, and absence controls.

The adaptive probe takes later command points from earlier replies and includes
zero and unit endpoints; it is a finite diagnostic, not an arbitrary-protocol
proof. The randomized fixture has geometrically distributed stopping depth and
no uniform precision cap; its threshold-event masses are computed exactly.
The presence checks operate on approximation intervals rather than treating
the reply centers as exact values. Their observed refinement depths are only
fixture diagnostics.

The author's exact_controls.py was inspected in full and replayed from a
byte-identical review-local copy. All 65,208 author assertions pass, and the
reproduced JSON is byte-identical to the author output. Its exact finite-seed
example uses one alternative oracle across all absent-output seeds, preserving
an event of probability 7/8. The finite-seed example supports the control code;
the threshold-event proof establishes the full randomized claim.

Universal validity rests on the written arguments in this review and the
author result, not on the finite grid or assertion count. The receipt binds the
replayed author evidence separately from the independent controls. Original
author artifacts were not executed in place or modified.

## 7. Review disposition

No substantive mathematical blocker found. The author adopted the only
requested wording clarification: distinguishing an additional restrictive
calibration-error prior from a vacuous band. No change to the theorem or hard
construction was required.
SOURCE_AUDIT.md records the bounded local nonduplication/ancestry assessment.
The final receipt binds the actual inspected author payload and independent
evidence; later author changes require a new review binding.
