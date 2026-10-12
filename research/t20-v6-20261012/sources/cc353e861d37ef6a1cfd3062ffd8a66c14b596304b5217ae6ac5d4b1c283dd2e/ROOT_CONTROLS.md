# Qualitative inquiry controls for the stochastic continuation investigation

10 October 2026 UTC. Root candidate controls; no universal controller theorem is claimed here. These finite models target an explicit source-transport issue: abstract support edges do not have fixed positive probabilities after Bayesian conditioning. They are not psychological models or claims about human warrant.

## A. Naive support-MDP false positive

Hidden initial label Θ is a or b, each with prior 1/2; it never changes. One repeatable experiment emits a revealing symbol r with probability 1/2 under a, never under b; otherwise it emits 0. A report r certifies a. After any finite string 0^n both initial labels remain possible.

The abstract support graph has an ambiguous node {a,b}, a self-edge 0 and a target edge r to {a}. Assigning any fixed positive chance to that target edge would incorrectly predict almost-sure termination. The actual chance of no reveal after n trials is

    1/2 + 2^(-n-1),

which tends to 1/2. Given 0^n, the next reveal probability is

    1 / [2(2^n+1)],

which has no positive uniform lower bound. The finite product of actual hidden state and retained support identifies the obstruction: (b,{a,b}) is a closed nonterminal class.

## B. Almost-sure finite stopping is weaker than uniform finite stopping

Modify the experiment so a emits its own revealing symbol a with probability 1/2, b emits b with probability 1/2, and each emits 0 otherwise. Every 0^n is possible and ambiguous, so no finite worst-case depth certifies the initial label. But nontermination probability after n trials is 2^(-n), tending to zero. Stop at the first revealing symbol. This is zero-error almost-surely finite identification, without a uniform finite bound.

## C. Consistent limiting learning is weaker than finite zero-error identification

For repeated fresh imperfect verifiers with likelihoods strictly positive under both labels, every finite observation word remains possible under each. Any finite terminal history claiming one label therefore has positive likelihood under the other. With both priors positive, a zero-error policy cannot stop there. Randomized stopping cannot remove the obstruction: every positive-probability finite stopping event selecting a label also has positive probability under the other label.

This does not prevent asymptotic learning or small-error decisions. In particular, distinct independent Bernoulli likelihoods permit almost-sure limiting identification under standard laws of large numbers, while not yielding a finite zero-error certificate. A proof of that asymptotic assertion is separate from the elementary finite-support argument above.

The actual retained source-audit model adds a provenance restriction: rereading a fixed verifier outcome is an idempotent revelation, not a fresh independent experiment. The perfect comparator control, when its exact correspondence is supplied, permits immediate identification. These cases must remain different instruments.
