# Independent review: fixed-calibration two-trial moment repair

11 October 2026 UTC. Separate additive review. The sealed credal-inquiry checkpoint and its reviewed files remain untouched.

## Verdict

**Pass within the stated two-trial contract. No correction required.** The feasible moment body, constructive realization, linear loss readout and third-trial counterexample are correct. This is elementary moment algebra applied to the already reviewed fixed-kernel/path-law distinction, with inherited continuation ownership and no cognitive-warrant consequence.

For a calibration distribution on [0,1], variance nonnegativity gives nu >= mu², and p² <= p gives nu <= mu. When mu=0 these force nu=0. Otherwise nu>0, the proposed support point nu/mu lies in (0,1], and the proposed weight mu²/nu lies in (0,1]. Their first and second moments are exactly mu and nu. Thus the conditions are sufficient as well as necessary, including the boundaries mu=0 and mu=1.

The reconstructed ordered law is (1-2mu+nu, mu-nu, mu-nu, nu). Its first cell is nonnegative because it is at least (1-mu)²; the other cells are nonnegative by the moment bounds, and all cells sum to one. For an arbitrary loss row (c00,c01,c10,c11), its expectation is

    c00 + (-2c00+c01+c10) mu + (c00-c01-c10+c11) nu.

This establishes the entire declared linear-loss contract, including signed losses, rather than only mismatch. At fixed mu, nu ranges from mu² to mu, so mismatch 2(mu-nu) has exactly the claimed range. The moving two-atom realization does not supply a single finite vertex catalogue for the curved body.

## Source-model meaning and continuation boundary

A genuinely single fixed calibration p lies on nu=mu². Interior points describe a supplied distribution over calibrations or a convex mixture of complete path laws. A convex-law relaxation may be computationally harmless for the extrema of a fixed linear path loss because a mixture’s value is an average of its constituent values. That equality of extrema does not authenticate a hyperprior, identify an unknown physical p, or make all mixed laws physically admissible.

The calibration is shared across the paired observations. Independently redrawing it each trial generally gives a different law. The body also does not contain every exchangeable two-trial law: the fair anticorrelated law (0,1/2,1/2,0) would have mu=1/2 and nu=0 and violates nu>=mu². The report correctly claims only the fixed-calibration mixture family.

The supplied distributions A and B both have first two moments (1/2,1/3). Their third moments are respectively 5/18 and 2/9. Two successes have probability 1/3 under both, and ordinary posterior reweighting of the calibration atoms gives next-success probabilities 5/6 and 2/3. Thus the claimed continuation collision is exact and uses a positive conditioning event. Two moments suffice for the specified two-trial observables, not unrestricted fresh-trial continuation or a closed filter for arbitrary future queries.

## Exact evidence and bindings

Reviewed RESULT.md SHA-256:
93bb189e12d85582871ce7eb30f11b28c50f957a5ea8657fc9acc834db5e0ebe

Reviewed check.py SHA-256:
1e4dbf2e997c77e1797ffe19dac15ebd0f441b319d019c6b1a3dab1f533607ff

The original checker passes 1,329 active checks in normal and optimized Python. The separate reviewer checker passes 1,725 active checks in each mode: it independently enumerates two-point calibration distributions, reconstructs their moment representatives, checks a signed loss readout, and computes the third prediction by both moment ratio and posterior atom reweighting. Its deliberate false guard rejects in both modes. The initial replay attempt detected the parent’s concurrent, announced scope clarification and stopped. The revised paragraph and added exchangeability control were inspected before updating the binding. Both final source hashes remain unchanged. REPLAY_RECEIPT.json records the runs and their outputs.

The written reasoning establishes the continuous statements; finite controls corroborate them. No general moment-theory priority, infinite-horizon sufficiency, numerical calibration, human-warrant result, protected edit, integration or closure is claimed.
