# Approximate migration: finite departures need an actual return mechanism

**Status:** a separate successor to `stochastic_refinement.md`, at the same pinned repository identity. Ordinary proofs and exact synthetic probes; no canonical admission, actual-world validation, or kernel-verification claim. The exact-coupling theorem SR1 has received a separate mathematical readback from the root researcher; this successor has not inherited that review automatically.

## 1. A sharp two-state obstruction

Take an always-good one-state source. The destination begins at good S. At time t, while in S, it moves to absorbing bad F with probability

`δ_t = 1/(t+2)²`,

and otherwise stays S. Let the matching relation be R={(source_good,S)}. After reaching F it never returns. There is at most one departure from R on **every** path. The conditional departure probabilities are bounded by the summable deterministic sequence δ_t.

Nevertheless, after n transitions the probability of no departure is

`∏_{k=2}^{n+1} (1−1/k²) = (n+2)/(2(n+1))`,

because the factors telescope. Its limit is 1/2. Therefore destination restoration succeeds with probability exactly 1/2; with probability 1/2 the single departure produces infinitely many bad visits.

This is not a failure of Borel–Cantelli. Departure events occur finitely often, as promised. Occupancy outside R can persist forever. A theorem bounding per-step departure hazards only while the process remains related has no authority to constrain the path after an exit.

With a fixed δ>0 instead, no-departure probability is (1−δ)^n→0, so even an arbitrarily small constant local approximation error can destroy almost-sure persistence completely. Approximate finite-horizon satisfaction bounds are not exact infinite-horizon restoration guarantees. This agrees with the explicit finite-horizon probability loss in the established approximate-refinement theorem. [Haesaert–Soudjani–Abate, Theorem 3](https://arxiv.org/pdf/1605.09557).

## 2. A direct repair when information stays valid globally

There are two different relations to consider:

- S: the interface remains informationally and probabilistically valid, with independently licensed destination actions;
- R⊆S: destination badness reflects to source badness.

Suppose the exact full-kernel and information clauses of SR1 hold on invariant S for all time. Define the *occupancy mismatch* E_t={(X_t,Y_t,Z_t)∉R}. These events need not be publicly observed, but must be adapted to the full joint proof filtration F_t. Suppose

`Σ_t P(E_{t+1} | F_t) < ∞` almost surely.

**Theorem AR1.** If the source restores almost surely, so does the destination.

**Proof.** Exact gluing on S supplies the correct source and destination path marginals. Conditional Borel–Cantelli gives only finitely many occupancy mismatches almost surely. For every time t,

`Bad_B(Y_t) ⇒ Bad_A(X_t) or E_t`.

Both sets of exceptional times are finite almost surely. Hence the destination is eventually always good. ∎

No controller-side detection of E_t is needed here because the information interface, authority and full law remain valid on all of S, including mismatches. Conversely, summable hazards of *leaving* R cannot replace the displayed summability of *being outside* R. The obstruction in §1 has finitely many departure events but infinitely many occupancy mismatches on its failed paths.

The conditional Borel–Cantelli statement and filtration hypotheses are established in `correlated_restoration.md`, CR2. In particular, conditioning only on a coarser public history is not enough when the mismatch is hidden.

## 3. A regenerative repair when the interface can genuinely break

If leaving R also destroys observation reconstruction or invalidates the migrated controller's memory, AR1 is unavailable. The implementation needs an actual recovery/reentry interface. The following contract makes that obligation explicit.

Let the destination have publicly distinguishable running and recovery modes, possibly with history-dependent internal memory. Time is discrete. A *fault flag* D_t is generated after transition t and is observable to the controller by time t+1. A flag starts a recovery episode. Flags may conservatively report more events than actual relation failures.

Require:

**A1, a conditional finite-fault budget.** For a full nonanticipating joint filtration F_t, D_t∈F_{t+1}, and there are predictable δ_t≥0 with

`P(D_t | F_t) ≤ δ_t` and `Σ_t δ_t < ∞` almost surely.

During recovery one may set D_t=false; the recovery contract must then itself cover any disturbances there. Alternatively all relevant flags must be counted. No ignored adversarial reset is allowed.

**A2, public sound detection while running.** Before a flag, running uses an observation-compatible translated source controller as in SR1. Every step has a **full** source/destination coupling. A successor with no flag remains in R, preserving the information interface, public mode and badness reflection. A flagged successor may be outside R. The flag cannot be computed by reading a hidden proof-state pair unless that information is actually available. A merely existential hidden coupling is not a public fault detector.

**A3, almost-sure finite recovery.** From every reachable recovery entry and allowed conditional law, a specified executable recovery policy reaches a public reentry point in finite time with conditional probability one. It may visit bad states during recovery. Source or destination authority and sure safety, when required, are checked independently on all recovery actions and all possible recovery outcomes.

**A4, legitimate reentry law and memory.** At every reached public/controller-information history h of reentry, the actual conditional destination law has a full initial coupling with a source initial law μ_A^h in a declared winning family. A publicly chosen restart policy σ^h restores almost surely for that family against the same strong adversary class as SR1. Reconstructed history, controller memory, public modes and authority are reset or transferred according to a specified lawful interface. If several hidden/environment-conditioned laws are compatible with h, the claim must hold for every induced law. A hand-picked favourable initial pair is insufficient.

A2 does not say that the source process conditioned on *never being flagged* retains its original law. That is generally false. The proof below avoids needing it.

### AR2. Regenerative almost-sure restoration

**Theorem.** Under A1–A4, and with a valid initial running entry or an almost-surely completing initial recovery, the destination restores almost surely. No bound on expected recovery duration or deterministic cutoff time is implied.

**Proof, step 1: finitely many recovery entries.** By A1 and conditional Borel–Cantelli, only finitely many flags occur almost surely. A3 has conditional failure probability zero at each recovery entry. There are only countably many discrete entry indices and finite histories; taking their countable union shows that every recovery episode that occurs completes almost surely. Thus, outside a null set, a final running episode starts at a finite time and is never flagged again.

**Proof, step 2: validate each candidate final episode without postselection.** Fix an episode index j and a positive-probability reentry history h. A4 starts a full joint coupling with an almost-surely winning source law. During the running episode use A2's full step couplings, until its first flag. Construct a *proof-only source continuation*: if a flag ever occurs, continue the virtual source autonomously from its then-current state and memory with its original policy and any legal source disturbance. Before a flag its source marginal is correct by the same summation argument as SR1; after a flag it remains a legal source law by construction. A destination-dependent disturbance becomes an allowed randomized full-source-history adversary when marginalized, just as in SR1.

Consequently the unconditioned source continuation has probability zero of infinitely many bad visits. On the event that episode j never receives a flag, the extension is never used: R and badness reflection hold for the whole episode. Therefore

`P(episode j never flagged AND destination bad infinitely often | h) = 0`.

This is an event inclusion inside a correctly marginalized law. It is not a claim about the law obtained by renormalizing on no future flag. Summing over the countably many entry histories and episode indices preserves zero probability.

**Proof, step 3: the final episode.** Step 1 guarantees that almost every path has some finite last recovery and hence some candidate final running episode. If such a path were bad infinitely often, it would belong to one of the zero-probability events in step 2. The preceding finite number of finite-length episodes adds only finitely many bad visits. Thus destination badness occurs finitely often almost surely. ∎

The last fault time is generally **not** a stopping time. The countable-episode argument is precisely what prevents an illicit strong-Markov or conditional-law argument at that last time. Public recovery entry and reentry times are stopping times; no claim of independence between episodes is needed.

## 4. Positive controls and limits

### 4.1 Geometric recovery under the same square hazards

Replace absorbing F in §1 by a recovery state R. While at good S, use the same fault probability δ_t. From R, return to S with probability ρ=1/2 each step, otherwise remain in R. The mode is observed, and every recovery step is licensed and safe in the synthetic model.

A1 holds because the conditional fault probability is `1_{state=S}δ_t≤δ_t`. A3 holds because every recovery duration is geometric. Reentry restarts the always-good source. AR2 therefore gives restoration probability one.

There is also a direct expected-occupation bound. If r_t=P(state_t=R), r_0=0, then

`r_{t+1}=(1−r_t)δ_t+(1−ρ)r_t ≤ δ_t+(1−ρ)r_t`.

Summing or unrolling gives `Σ_t r_t ≤ (1/ρ)Σ_t δ_t < ∞`. Hence the expected total number of bad visits is finite in this particular model. Neither its infinite time horizon nor the hazard schedule is produced by a time-homogeneous finite-state controller without a source of the unbounded time index.

### 4.2 Almost-sure recovery need not have finite mean

A recovery policy with elapsed-recovery counter k returns on its next step with probability `1/(k+2)` and otherwise increments k. Then

`P(T>n)=∏_{k=0}^{n−1}(1−1/(k+2))=1/(n+1)→0`.

Thus recovery is finite almost surely, while `E[T]=Σ_{n≥0}P(T>n)=∞`. A single such recovery followed by an always-good running mode satisfies the persistence conclusion of AR2 but has infinite expected bad occupation. This counter policy requires unbounded elapsed-time memory; it is not a finite homogeneous Markov-chain example.

### 4.3 Constant faults defeat the finite-fault sufficient condition

With constant fault probability δ>0 from S and return probability ρ>0 from R, the two-state chain is irreducible. Its stationary bad mass is `δ/(δ+ρ)>0`, and R is visited infinitely often almost surely. Recovery works each time, but it is repeatedly needed forever. Thus almost-sure finite recovery alone does not prove eventual persistence.

A1 is a sufficient fault-budget condition, not a necessary condition for all possible architectures: infinitely many flags might be harmless if they trigger no badness and preserve a winning interface. The theorem does not relabel every flag as an actual physical target violation.

## 5. Verification and remaining interface work

`probe_regenerative_refinement.py` checks, with exact fractions:

- 80 telescoping no-departure probabilities for the sharp probability-1/2 obstruction;
- 80 geometric-recovery marginal recurrences and finite-prefix occupation bounds;
- 80 heavy-tail recovery probabilities;
- 40 constant-hazard stationary equations and positive bad masses.

All checks pass. `regenerative_refinement_results.json` records the claims and distinguishes analytic infinite-horizon conclusions from finite verification. Run `python probe_regenerative_refinement.py` in this directory.

AR2 is a usable proof contract, not an implemented general recovery synthesizer. A concrete migration still owes public fault detectability, an actual lawful recovery controller, and a complete conditional reentry-law/memory certificate. This is the substantive boundary exposed by replacing exact migration with approximation; summability by itself cannot supply any of those three obligations.
