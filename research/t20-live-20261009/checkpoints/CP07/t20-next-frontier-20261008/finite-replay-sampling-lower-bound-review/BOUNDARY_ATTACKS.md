# Adversarial boundary controls

## 1. Conditional-on-termination correctness is insufficient

Start with any finite-budget test of the hard pair having each error at most alpha. Such a finite test exists because Delta>0; elementary empirical testing of the replay joint cell suffices. Before taking any samples, toss an independent Bernoulli(epsilon) coin. On success run the test; on failure continue forever taking only fresh single endpoints, with no terminal decision.

Conditional on termination, both accuracy guarantees are still at least 1-alpha. The Joe-expected number of replays is epsilon times the original finite budget and can be made arbitrarily small. This violates any proposed positive expected-replay lower bound based only on conditional accuracy. Under the packet's actual unconditional contract it is inadmissible for small epsilon: terminal correctness is at most epsilon. No nonterminating path is silently assigned a label.

## 2. Fresh redraw is not retained-gate replay

If the two face outcomes are instead drawn from separate independent latent vectors, each face still has absence probability A in both worlds, but their pair law is exactly the product P0 in both worlds. Thus Delta=0 for that altered experiment. The packet's positive Delta specifically comes from retaining the actual gate realization, not merely the route count, calibration, or distribution.

## 3. Policy choices do not create new conditional information

After one actual replay, a common policy can choose its next action based on whether that replay was in the no/no cell. Because that cell has probability A^2 under reference and A^2+Delta under Joe, the next action has a different unconditional distribution across worlds. It still contributes zero conditional KL given the earlier observation. The finite-prefix proof correctly conditions on the complete common history instead of multiplying unconditional action distributions as though they were independent evidence.

## 4. Atomic actions and the cost convention

A paired replay is one action returning both fixed-command bits. The theorem is not a proof for a protocol that inspects a first face, conditionally completes the pair, and charges only selected completed pairs. Such a protocol changes the conditional observation law and the cost accounting. It can be covered by charging every initiated paired action and allowing discarded data, but that extra convention must be explicit. The reviewed packet uses atomic pairs and prohibits repurposing an earlier fresh endpoint as a replay.

## 5. Error range

At alpha=1/2, a no-data fair coin meets the two terminal-correctness bounds. At alpha>1/2 the same procedure is allowed, although kl(1-alpha,alpha)>0. Consequently alpha<1/2 is necessary for the monotonicity step in this stated bound. As alpha approaches 1/2 from below, kl(1-alpha,alpha) tends to zero while log(1/alpha) does not. The logarithmic comparison therefore needs the stated small-error restriction or fixed alpha strictly below 1/2.

## 6. KL orientation and cost orientation

The chi-square denominator is P0. The chain-rule orientation is KL(Law_1||Law_0), so the expected count is E1. The reviewed proof does not establish the identical constant for E0 by relabeling; that would need a separately bounded reverse divergence. The fixed maximum-budget consequence is valid because N_infinity<=N implies E1[N_infinity]<=N.

## 7. Summaries and larger instruments

A summary such as the joint-no-hit indicator is a deterministic function of the two observed bits. Data processing means it cannot defeat a lower bound already proved with access to the complete pair. Conversely, another retained-threshold rate, a longer retained-threshold word, route-level readout, or cross-action threshold persistence is not a function of the permitted data. No KL bound for those richer observations has been proved here.

## 8. What numerical evidence establishes

The independent controls certify exact root enclosures for the actual Joe construction at 36 selected integers and exact finite-tree likelihood/count bookkeeping. They are not an all-integer exhaustion, an arbitrary-stopping proof by simulation, formal kernel verification, or empirical evidence that the experiment can be implemented. The universal results depend on the written derivation.
