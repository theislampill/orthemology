# Fresh hidden switching: an exact conditional-error threshold

**Scope:** a brief corollary of the adapted conditional Borel–Cantelli interface in `correlated_restoration.md`, requested for this consolidation. It is an ordinary proof, not an additional implemented general controller solver. Standards, their target assignments and action permissions remain stipulated model inputs.

## Model and filtration

A binary standard h_t changes according to `h_t=h_(t−1) XOR B_t`. Before choosing response a_t, the controller observes h_(t−1) exactly but does not see the new innovation B_t. Target at step t means `a_t=h_t`. Initially h_(-1) is known. Both responses are provisionally stipulated safe and licensed under both standards.

Let F_t contain the entire past, the selected current action a_t and all randomness already used to select it, but not the current innovation. Assume

`P(B_t=1 | F_t)=p_t`,

where p_t is a declared deterministic sequence with 0≤p_t≤1/2. The next filtration includes h_t, B_t and the next selected action, so mistake event E_t={a_t≠h_t} belongs to F_(t+1). This is a fresh *conditional* innovation premise, not merely a statement about unconditional one-time marginals.

## SW1. Exact almost-sure threshold

There exists a nonanticipating policy with only finitely many mistakes almost surely if and only if `Σ_t p_t<∞`.

**Proof.** After conditioning on F_t the chosen action is known. If a_t=h_(t−1), its mistake probability is p_t. If it is the opposite response, its mistake probability is 1−p_t≥p_t. Thus every policy, including arbitrary randomized history-dependent policies, satisfies

`P(E_t | F_t) ≥ p_t`.

When the sum diverges, conditional Borel–Cantelli implies infinitely many mistakes almost surely. Unbounded memory cannot remove a fresh unobserved innovation.

When the sum converges, choose `a_t=h_(t−1)`. Then E_t is exactly {B_t=1}, so its probabilities sum to a finite value. The first Borel–Cantelli lemma gives only finitely many mistakes almost surely. This implementation needs only the most recently observed standard; it does not need the time-dependent p_t to choose its action. The environment's inhomogeneous hazard schedule is nevertheless an explicit model premise. ∎

If p_t is instead policy/endogenously dependent, the lower-bound argument still holds on paths with divergent conditional risk. The exogenous iff theorem does not imply that a greedy local predictor optimizes a future endogenous risk sequence.

## Guards

1. **Support and finite core entry differ.** If 0<p_t≤1/2 forever, both next standards remain possible after every finite history. No selected response guarantees the next target state against both possibilities, so there is no nonempty support-invariant target core for this response model. A summable positive schedule nevertheless gives almost-sure eventual target persistence. A support adversary can force infinitely many mistakes; the almost-sure result is not sure winning.

2. **Observation timing is decisive.** If the current h_t is revealed before a_t, issuing a_t=h_t makes every response correct. This is a different information contract, not an improved inference algorithm for the delayed model.

3. **A copied root destroys the claimed innovation lower bound.** Let a single Bernoulli(ε) variable Z be copied so that B_t=Z at every time. Each one-time marginal still has flip probability ε. After observing the result of the first transition, however, the controller learns Z and predicts all later transitions exactly. At most the first response is wrong. Conditional future risks are then zero; summing the unconditional marginal ε would give a false impossibility claim. Root-level dependence must remain in the filtration/model.

4. **Statistical correctness does not grant eligibility.** If response a is eligible only when a=h_t, both h_t alternatives remain in finite-time support whenever 0<p_t<1. Neither response is universally eligible at that decision point. If abstention is the only common licensed action and is not a target response, the statistical predictor is not an authorized restoration policy. SW1 applies only under its independent common-permission premise.

5. **No real-world standard identification follows.** The model prescribes how hidden standards affect observations and which responses count as target. The theorem neither establishes those prescriptions nor selects a norm from the observed switching frequencies.
