# Posterior-equivalent continuation need not preserve almost-sure exact stopping

10 October 2026 UTC. Root candidate derivation, sent to the stochastic inquiry author for inheritance checking and separate review. Not yet independently reviewed; no new field-level novelty or human-warrant claim.

Use one fixed finite, static hidden-state instrument X={(0,R),(1,R),(0,N),(1,N)}. The requested initial label is the first coordinate. The universally permitted sole action emits wait with probability 1/2 and reveal-the-label with probability 1/2 in mode R; in mode N it always emits wait. It never changes hidden state. Stopping/reporting is permitted when the surviving labels are homogeneous.

Initial law p gives mass 1/2 to each R state and zero to N. Initial law q gives mass 1/4 to all four states. Both label priors are fair.

For every finite word:
- A word containing both reveal labels is impossible under both laws.
- A word containing a reveal of exactly one label has that label's posterior equal to one under both laws. Its q probability is half its p probability.
- The word wait^n has posterior (1/2,1/2) under both laws. Its p probability is 2^(-n), and its q probability is 1/2 + 2^(-n-1).

Thus p and q have exactly the same feasible-word language and all feasible finite-word target posteriors. They satisfy the previously established posterior-only continuation interface. This is stronger than equality of the current posterior or of a finite list of posteriors.

Under p, stop on the first reveal. Stopping is almost sure and always correct. Under q, probability 1/2 is placed on N states, which never reveal. No zero-error policy can stop at a wait-only history with positive probability: both labels have positive posterior there. Therefore no zero-error policy stops almost surely under q. The only inquiry action means that no policy can repair this limitation by choosing another action. Independent random stopping does not help, since it cannot distinguish the two labels at the same finite observed history.

This does NOT refute qualitative invariance with the same initial hidden-state support. Here the supports explicitly differ. In a fixed finite instrument, any two laws positive on the same support agree on whether a single policy succeeds almost surely from every supported state. The counterexample shows that the posterior-only interface can identify laws with different hidden support and thereby erase this distinction.

Full predictive equality gives a sufficient repair: if all finite observable histories have the same probability and the same label joint masses, with matching lawful menus and permitted verdicts, every common history-policy has the same finite stopped-verdict law. Increasing unions of finite stopping events then give the same almost-sure stopping/error law. This uses probability measure continuity, not a supposed Markov chain on posterior classes. Mathematical classical ancestry and any prior programme theorem must be checked before new-to-project credit.

## A weaker positive transport condition than predictive equality

For the same finite history interface and lawful common policy, suppose Q(h) <= C P(h) at every finite action/receipt word, for one finite C independent of the word. Action-choice and continuation factors for a shared history policy multiply both word masses by the same nonnegative scalar. Summing over nonstopped length-n histories therefore gives Q(tau>n) <= C P(tau>n). If P(tau<infinity)=1, continuity gives Q(tau<infinity)=1. Shared feasible-word target posteriors preserve the zero-error verdict condition. The argument also covers randomized stopping, whose shared probabilities multiply the relevant finite histories.

Thus mutual uniform prefix domination, together with the same permission/verdict interface and posterior contract, gives the almost-sure-stopping iff without exact equality of predictive laws. This is a classical measure domination argument, not a new general probability theorem. It is a sufficient criterion, not a claimed necessary one.

For the same finite instrument and initial distributions positive on the same support, choose C=max_x q(x)/p(x). Every finite history probability is a nonnegative linear functional of the initial distribution, so the bound follows for every history and every common policy. The reverse bound follows similarly. In the present counterexample Q(wait^n)/P(wait^n)=2^(n-1)+1/2, so no such uniform domination holds in the failing direction. Positivity of each individual finite prefix does not supply a uniform bound or absolute continuity on the infinite path sigma-algebra.
