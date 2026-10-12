# Stochastic exact inquiry: cumulative evidence

10 October 2026. This is a compact, additive source-and-replay archive. The
mathematics is ordinary proof with exact finite executable controls, **not Lean
or other kernel verification**. It makes no empirical reliability, philosophical
warrant, field-level novelty, integration, or T20/HasE closure claim.

## Read in this order

1. stochastic-exact-inquiry-20261010/RESULT.md: the finite hidden-state stopping
   contract, fixed-point criterion, proof, counter-controls, and audit application.
2. stochastic-exact-inquiry-review-20261010/REVIEW.md: the separate independent
   assessment and the exact accepted report/solver hashes.
3. stochastic-inquiry-quotient-transport-20261010/ADDENDUM.md: why preserving every
   finite posterior and feasible receipt word can still lose almost-sure exact
   completion, and sufficient conditions that preserve it.
4. stochastic-inquiry-quotient-review-20261010/REVIEW.md: the separate addendum
   assessment, including its final source binding and independent controls.

The frozen author manifests retain their historical “independent review pending”
status. Their subsequent independent reviews are separate artifacts; no frozen
manifest or reviewed source was edited to update that historical wording.

## Main result: which exact stopping question is decided?

A finite labelled hidden-state model supplies fixed Markov kernels, exact positive
transition supports, finite actions/receipts, and state-dependent permission menus.
The label is the initial answer being sought and survives destructive state changes.
One common policy uses observation history, not the actual hidden state, and may
randomize independently. Inquiry must be permitted at every live possibility;
reporting a common label at a homogeneous support is assumed permitted.

The algorithm decides whether such a policy can stop almost surely in finite time
with zero error. It uses a greatest fixed point and a correctness graph on actual
state × current support. It does not put invented fixed probabilities on support
edges. Support memory with stationary randomized action selection suffices for this
particular objective. Sure finite stopping is a different, least-attractor question.

The exact controls include genuinely branching hidden successors under one receipt,
a shrinking-hazard trap, lawful-menu failures, destructive-label preservation,
partial and perfect reveal cases, and the stipulated 16-state source-audit model.
Repeated readings of the retained imperfect audit do not yield exact stopping;
fresh imperfect evidence and almost-sure limiting learning are not finite
zero-error certificates. This does not define ordinary human knowledge or warrant.

## Addendum: finite posterior preservation versus eventual completion

One fixed four-state instrument and two different initial supports can agree on
all feasible finite receipt words and every finite target posterior, yet disagree
on existence of any zero-error almost-surely terminating policy. Under the first
law, unresolved survival after n observations is 2^(-n); under the second it is
1/2 + 2^(-n-1). The all-word claim is proved, not inferred from finite enumeration.

With matching lawful action and terminal-report interfaces:

- Full finite predictive probabilities and target numerators preserve every shared
  policy's finite stopped-verdict laws, hence stopping/error probabilities by
  continuity from below.
- Uniform prefix domination is a weaker sufficient one-way stopping-transfer
  condition when the posterior verdict contract is preserved; mutual domination
  gives the corresponding two-way transfer.
- Same-support initial laws in one fixed finite instrument satisfy labelled
  two-sided domination and preserve qualitative stopping/error guarantees even
  when their numerical posteriors differ.
- The actual eight-mass audit quotient passes its support/receipt transport test.

Permission correspondence remains an independent requirement. These are scoped
transport statements, not new general probability theorems or a necessary-and-
sufficient classification of every possible quotient.

## Ancestry and source limits

The product-chain/allowed-action mechanism is classical qualitative POMDP reasoning.
The retained reports identify Chatterjee, Chmelík, Gupta and Kanodia,
*Optimal Cost Almost-sure Reachability in POMDPs*, §4.2, Lemmas 5–6:
https://arxiv.org/html/1411.3880v1#S4.SS2

The external paper was inspected during research/review but its bytes are not
bundled. This delivery performs no new live source authentication or literature
survey. No cost-optimization result or general hidden-parity theorem is imported.

The preserved internal inputs credit H-ICS initial-label and permission reasoning,
H-Continuation finite predictive laws, the broader posterior-deterministic control
scope, existing finite-history zero-error obstructions, and the actual audit and
inquiry-value constructions. Root/author collaboration is shared development;
separate reviews identify the genuinely independent evidence. The root notes retain
their historical status wording. Their presence is not another independent review.

## What is included, and why the archive stays small

Every frozen packet/review manifest payload and every explicitly bound dependency
is preserved byte for byte. Exact root derivations and controls are included.
PRESERVED_SOURCES.json inventories the canonical original files; ARCHIVE_CONTENTS.json
hashes every delivered file except itself. The external archive receipt binds the
ZIP, the index, all source preservation checks, and the fresh-extraction replay.

Repeated review snapshots are not stored again in the ZIP. Their original snapshot
binding ledgers are retained. The replay wrapper materializes the exact required
copies into a new throwaway workspace, verifies their hashes, and runs the actual
unchanged review/check scripts there. No broad project tree, dependency cache,
build output, environment, symlink, or unneeded parent directory is included.

## Verify and replay

Requirements: Python 3.9 or later, standard library only. No installation, network,
external package, or original workspace is needed for the listed replay.
From the extracted archive root:

    python verify_archive.py
    python replay_archive.py --out /path/to/a/new-directory

Choose an output directory outside the archive. The wrapper verifies the canonical
archive, materializes bound review snapshots, executes both actual review replay
scripts (which run their author checks as well), and executes the root probability
control. It records commands, exit codes, logs, regenerated review receipts, and
results, then rechecks every canonical archive hash.

Original scripts intentionally regenerate some logs, JSON outputs and receipts.
Only the throwaway replay workspace is modified. Unit-test timing in regenerated
logs may differ; accepted source bytes and deterministic control results are checked
separately. A passing replay corroborates the implementations and retained review
scope; finite tests do not establish the universal theorem by enumeration.
