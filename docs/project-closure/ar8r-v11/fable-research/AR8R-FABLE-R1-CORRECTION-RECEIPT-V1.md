# AR8R-FABLE-R1 — correction receipt V1

Public-safe record of the repairs applied after independent review of Fable
research round 1. This receipt governs where it disagrees with any round-1
artifact.

```text
reviewed commit:         f0e386ad9fe0b110977fd51797913f5bcb8a1391
review verdict:          BLOCK
second-pass verdict:     BLOCK CONFIRMED
correction base:         7b05340e6fdb03a5f2700d05e385268acbc2fdfa (origin/main, verified)
correction branch:       fable/ar8r-r1-blocking-repairs
meniscus:                MENISCUS_NOT_REACHED
natural closure:         NOT_REACHED
integrated champion:     NONE
theorem-origin authority: V5
historical payloads modified: false
Round 20 statement modified:  false
decision record added:        none required (see below)
```

## Withdrawn claims

1. **N1's target attribution.** Round 1 said its transversal/packing and
   exchange-axiom results refuted the Round-20 restorative-cutset result and
   milestone candidate MEN-2. Both Round-20 V1 (rejected) and V2 (proposed)
   define `τ(H)` and `κ_root = min_p τ(H_p)` and prove `f`-root-robust ⟺
   `κ_root > f`; neither uses maximum packing as the criterion, asserts a Menger
   equality, or assumes a matroid. MEN-2 is `NOT_ADOPTED`, proposes *defining* a
   rank, and carries the nonclaim `NOT_A_THEOREM`. Nothing was refuted.
2. **The sharp threshold.** "Both properties hold iff every item requires at most
   one root" and "both fail as soon as one item requires two" are false.
3. **"The characterization is false" under the literal "requires" reading.**
   `Certifiable P l ↔ FibreConst P l` is proved for an arbitrary label. The
   casualty is the packet's separate `B*`-sufficiency remark.
4. **D4 (A14) as a packet defect.** The alleged inexpressibility was induced by
   the formalization's own `term := fun a _ => …`, which discards the background
   argument the packet supplies.
5. **"Five genuine defects."** Four of fifteen recorded places are defects beyond
   notation, and D1's consequence is narrower than stated.
6. **"Four of five negative results refute premises the program was relying on."**
   No adopted premise was refuted.
7. **The double-derivation claim.** "Derived twice independently by two lines of
   work that did not share intermediate results" is a process claim no committed
   artifact can confirm.
8. **The unqualified no-global-section claim.** A finite surjection onto its
   attained image has a set-theoretic section; the supported limitation is the
   absence of a canonical, transition-compatible section and latent-state
   nonidentifiability.
9. **Unreproduced sampling counts** are no longer presented as evidence.

## Preserved valid results

The Lean work survived review intact and is unchanged in substance:

- clean build from committed sources, exit 0, `Build completed successfully (636 jobs).`;
- 0 `sorry`; no `axiom` declaration, `@[implemented_by]`, `native_decide`,
  `unsafe`, `partial`, or checking-weakening `set_option`;
- axiom split after adding the new witness pair: **7 declarations with no axioms,
  7 with only `propext`, `Classical.choice`, `Quot.sound`** (the pre-correction
  split was 6 and 6, not the 5 the original commit message stated);
- historical T299 and T300 payload bytes unchanged; recorded pre-repair and
  repaired hashes untouched;
- the triangle (`τ=2`, `ν=1`) and path exchange-failure countermodels are
  arithmetically correct, now re-verified by a committed checker;
- quorum arithmetic correct within `2 ≤ n ≤ 7`;
- N4's split-number nonmonotonicity counterexample correct;
- privacy clean;
- frozen status block unchanged: duration `09:41:25.405101139`, segment `357`,
  authority `V5`, champion `NONE`, meniscus and natural closure `NOT_REACHED`.

First-review bookkeeping errors, corrected here: the axiom split is **6/6** (not
5), and round 1 added **15** `SHA256SUMS` entries (not 16).

## Corrected T299 interpretation

What was machine-checked is a **repaired, scoped interpretation** of T299's
quotient-factorization structure. The historical packet was **not** machine-checked
end to end. Defect reclassification: D1 real ambiguity and scope-firewall defect;
D2 genuine; D3 notational with an evident pair-indexed repair; **D4 withdrawn**;
D5 genuine cross-section defect.

A T299-specific A4 witness was added and kernel-checked, since the original
`A4_requires_reading_is_insufficient` proves only the generic truism at
`Bool`/`Unit`:

```text
A4_matchedProfile_insufficient_under_requires_reading   (no axioms)
A4_matchedProfile_not_certifiable_under_requires_reading (standard axioms)
```

Both construct an actual `Model` whose two backgrounds share one `matchedProfile`
while a label satisfying the merely-necessary reading differs across them.

## Corrected N1 interpretation

`τ ≠ ν` is retained as an **interpretation firewall** (a minimum transversal
cannot in general be replaced by a maximum packing) and the exchange-axiom failure
as a **constraint on any future MEN-2 definition** (it must name whether the
proposed quantity is a transversal quantity, packing quantity, matroid rank,
polymatroid quantity, or another invariant). `FABLE-R1-B01` and `FABLE-R1-B02`
were rewritten accordingly; neither now asserts that existing text is unsound.

## Sharp-threshold counterexamples preserved

| Structure | Exchange | `τ` | `ν` |
|---|---|---|---|
| one item `{r₁,r₂}` | holds | 1 | 1 |
| two disjoint two-root items | holds | 2 | 2 |
| `{r₁,r₂}`, `{r₁,r₃}` | holds | 1 | 1 |

Surviving one-directional statement: the single-root regime is **sufficient** for
partition-matroid structure and `τ = ν`; it is **not necessary**. No replacement
`iff` is offered.

## Experiment-status correction

Round 1's only experiment statement — "No designed public experiment packet has
ever been run" — was checked against `experiments/experiment-status.yaml` and
found **already correctly qualified**: the historical internal pilot is recorded
outside `packets` with `public_experiment_packet: false`. No unqualified "no
experiment ran" wording existed in any round-1 artifact. The burden text was
nevertheless expanded to name the pilot explicitly, so the boundary cannot be
misread in either direction. This is the one instructed repair whose premise did
not hold; it is recorded rather than fabricated.

## Reproducibility changes

Two checkers are now committed under `checks/`, each recording Python version,
input domain, enumeration bounds, case-count derivation, deterministic ordering,
output schema, exit status, and result digest:

```text
checks/t299_finite_check.py           361164 cases, 0 mismatches, exit 0
checks/n1_transversal_packing_check.py  7 checks, all pass, exit 0
```

Randomized (4000) and rejection-sampled (2000 kept / 72753 rejected) counts are
marked `UNREPRODUCED_FROM_COMMITTED_ARTIFACTS` and carry no evidential weight.
The "13/13 twin assertions" claim is superseded by the direct kernel check.
Properties labelled "proved" in the typed-core and separation-index packets, with
no derivation or check attached, are downgraded to `DERIVED_BUT_UNVERIFIED`.

## Sourcing changes

`AR8R-FABLE-R1-SOURCING.md` adds a row per load-bearing attribution with source,
identifier, claim supported, exact relationship, and verification status. All rows
are `UNVERIFIED` — no literature search was performed in round 1 or in this
correction, and none is invented. Myhill–Nerode is narrowed from `identical` to
`adjacent`.

## Lean-status reconciliation

`AR8R-V11-LEAN-FORMALIZATION-QUEUE.yaml` now scopes its `NOT_PERFORMED` axes to
the historical external corpus and records the round-1 development separately
under `scoped_developments`, explicitly **not** identified with any lost or
intended historical Lean declaration. Q0 is marked performed; Q1a–Q1i are
unblocked but not performed.

## Decision-record policy

No numbered decision record is added. Nothing adopted changed: MEN-2 remains
`NOT_ADOPTED` and untouched, the Round-20 statement is unaltered, no registry,
notation, or verdict semantics moved, and the corrections are to a non-adopted
research finding. Restating MEN-2 itself would require a decision record; this
correction does not do that.

## Remaining unresolved burdens

`FABLE-R1-B01` (definitional constraint on future MEN-2 drafting),
`FABLE-R1-B02` (optional standalone formalization of the firewall),
`FABLE-R1-B03` (T299 superseding note), `FABLE-R1-CI-01` (Lean in CI),
`FABLE-R1-B05` (Candidate 1 prior art), `FABLE-R1-B06` (rival cores), plus all
pre-existing owner and specialist burdens. Source-level readings of the external
source remain `SOURCE_LEVEL_UNVERIFIED`; the paper was outside the review
boundary and is outside this correction's boundary.

Round 1's method note claimed nothing was accepted merely because it was
plausible. Independent review found three places where that failed. The corrected
record is that external review, not round 1's own discipline, caught them.
