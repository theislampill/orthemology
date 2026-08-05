# AR8R-FABLE-R1 — specification defects in the T299 packet, exposed by formalization

Status: research finding. Non-adopted. No theorem is retracted and no historical
packet is edited. The exact historical payload hashes recorded in
`docs/project-closure/ar8r-v11/theorems/ar8r-t299-matched-intervention-burden-landing.md`
are unchanged and remain authoritative for custody.

The research prompt's step 6 asked for the *smallest* result whose formalization
would expose a real ambiguity, dependency cycle, or specification defect. T299
was selected. The formalization compiled with zero `sorry` (see
`AR8R-FABLE-R1-LEAN-RECEIPTS.yaml`), and in the course of compiling it, fifteen
places were found where the informal packet does not determine the formal
content.

**Reclassification after independent review.** Round 1 originally claimed five of
those were genuine defects rather than notation choices. That count is withdrawn.
The independently adjudicated classification is:

| Item | Classification |
|---|---|
| D1 (A4) | real ambiguity and scope-firewall defect — **not** a refutation of the abstract factorization theorem |
| D2 (A10) | genuine specification defect |
| D3 (A1) | notational/typing defect with an evident pair-indexed repair |
| D4 (A14) | **withdrawn** — not established as a packet defect; induced by a formalization choice |
| D5 (A11) | genuine cross-section specification defect |

## What was and was not machine-checked

This distinction was blurred in round 1 and is stated explicitly here:

- **Machine-checked:** a repaired, scoped interpretation of T299's
  quotient-factorization structure. The Lean development is a formalization of a
  reading of the packet, with the repairs recorded below.
- **Not machine-checked:** the original historical T299 packet, end to end. No
  kernel check can establish that a formalization faithfully renders an informal
  packet; the items below are precisely the places where faithfulness required a
  choice.

## D1 (A4) — "requires" is not a definition, and `B*` sufficiency is not established under the literal reading

The packet says: causal landing `L_b` **requires** all of clauses 1–6.

"Requires" states necessary conditions. Read literally the packet gives
`L_b → (c₁ ∧ … ∧ c₆)` and leaves `L_b` otherwise underdetermined.

**Correction (independent review).** Round 1 stated that under this reading "the
characterization theorem is **false**". That is wrong and is withdrawn. The
abstract characterization

```text
Certifiable P l  ↔  FibreConst P l
```

is proved in Lean for an *arbitrary* label `l`, with no constraint on how `l`
arises. It does not become false because the packet uses the word "requires".

The actual specification problem is narrower, and is real:

```text
if the six clauses are only necessary conditions for L_b, then their
conjunction — and the matched ingredient profile B* built from them —
does not, without an additional definition or equivalence, determine L_b;

therefore the packet's separate claim that B* is sufficient
"by construction" is not established under that reading.
```

So the casualty is the scope-firewall sufficiency remark, not the characterization.

**Witness status.** The Lean declaration `A4_requires_reading_is_insufficient`
proves the *generic* fact that necessary clauses need not determine an
independently selected label; it is instantiated at `Bool`/`Unit` and does not
mention `Model`, `matchedProfile`, or `L`. A T299-specific witness,
`A4_matchedProfile_insufficient_under_requires_reading`, was added in this
correction: it constructs an actual `Model` with two backgrounds sharing the same
`matchedProfile` and differing labels under the merely-necessary reading. Both are
recorded in the receipt with their roles distinguished.

**Consequence.** The packet should be read as stipulating a definition. Any future
use of T299 that treats the six clauses as merely necessary, and then relies on
`B*` sufficiency, is unsound.

## D2 (A10) — the twin's central claim is unstatable in the packet's own vocabulary

The declared setting supplies only `term(a,b)`: a terminal state as a function of
the operation value and background. There is no initial state anywhere.

The causal/spontaneous twin nevertheless asserts that "under `A=1`, the
before/after observations match across the models". That sentence requires an
initial state and an observation channel. The packet declares neither.

Formalizing forced the introduction of both (`init` and `obs`). The choice is not
free: **the twin claim is channel-relative.** Under the channel used here —
observing the target predicate and the burden disposition — the claim holds and
is machine-checked (`twin_before_agree`, `twin_after_agree`). Under a channel
that exposes the background coordinate, the models are distinguishable before
the operation and the claim fails. Under a poorer channel it is vacuous.

**Consequence.** "Before/after observations match" is not a property of the twin
alone. It is a property of the pair (twin, observation channel), and the channel
is undeclared. Any argument leaning on the twin must declare its channel.

## D3 (A1) — notational: the twin is not formally an instance of the theorem it illustrates

Classified as a **notational/typing defect with an evident repair**, not a
substantive specification defect: the packet's own `B*(M,u)` notation already takes
the model–unit pair as its argument, so the pair-indexed reading is available on the
face of the text.

The characterization quantifies over backgrounds `b` of one fixed model. The
twin's profile `B*(M,u)` ranges over model–unit pairs across two *different*
models. These are not the same index type.

As written, the twin does not instantiate the theorem. Two repairs are available:
either the theorem is about a fixed model and the twin illustrates something else,
or "background coordinate" must be read as absorbing the model identity. Only the
second makes the packet coherent, and the packet never says so.

## D4 (A14) — WITHDRAWN: not established as a packet defect

Round 1 claimed the declared model shape "cannot express its own twin": the setting
gives `Q : St → Bool` with no background index, while the twin requires `M_cause`
and `M_spont` to disagree on `Q(S_term^(0))`.

**This claim is withdrawn.** The alleged impossibility was introduced by a
formalization choice, not by the packet:

- The packet declares `term(a,b)` — a terminal state depending on **both** the
  operation value and the background coordinate.
- Under D3's own repair, in which the background coordinate absorbs model identity,
  `term(a, cause)` and `term(a, spont)` are simply *different states*. An unindexed
  `Q : St → Bool` then expresses the twin without difficulty, because the two
  models' terminal states are distinct objects rather than one shared object
  carrying two truth values.
- The Lean development instead defines `term := fun a _ => …`, discarding the
  background argument the packet supplies, and thereby collapses the two models'
  terminal states into one. Only after that collapse is a background-indexed `Q`
  forced.

The background index in the committed `Model` structure is therefore a convenience
of the chosen encoding. It is retained in the Lean sources — the development is
sound either way — but it no longer supports a claim about the packet, and the
in-source comment marking it as a forced repair overstates its status.

What remains is the already-recorded notational point in D3: the packet writes
`S_term^(a)` without a model index. That is D3, not a second independent defect.

## D5 (A11) — clause 4 has no argument, and the two readings contradict different parts of the packet

Clause 4 says "the declared whole-field reread passes" and supplies no state,
unlike clauses 1, 2, 3, 5. Two readings are available:

- **(i)** evaluate at the operation branch, `R_b(term(1,b))`;
- **(ii)** evaluate at both branches, which is what the words "whole-field" suggest.

The packet's own profile `B*` lists exactly `R_b(S_term^(1))`, i.e. reading (i).
But under reading (ii), `B*` would be an *incomplete* profile and the packet's own
claim that the matched profile is "sufficient by construction" would be **false**.

So two sections of the packet silently constrain each other, and only reading (i)
makes both true. Reading (i) was adopted; the lemma
`certifiable_matchedProfile` is what fixes it.

## Non-defects worth recording

- **(A7) "finite and deterministic" is not used by the theorem.** The
  characterization is true for arbitrary types; the Lean statement carries no
  `Fintype`, no `DecidableEq`, and no determinism hypothesis. Finiteness buys
  decidability of fibre-constancy and a *computable* certificate, nothing more.
  The packet conflates "the theorem needs finiteness" with "the certificate is
  effectively constructible".
- **(A13) the burden-disposition codomain is underspecified** but the
  characterization is genuinely insensitive to it. Recorded, not a defect.
- The twin's `M_spont` fails **two** clauses (2 and 5), not one. The packet does
  not say how many; the finite check establishes it.

## What this does not establish

- T299's mathematical content is not refuted. The abstract characterization is
  true for an arbitrary label, machine-checked, and exhaustively finite-checked;
  under the definitional reading of the six clauses, `B*` sufficiency holds too.
- The historical packet was **not** machine-checked end to end. What was checked is
  a repaired, scoped interpretation of its quotient-factorization structure.
- Four of the fifteen recorded places, not five, are defects beyond notation — and
  of those, D1's consequence is narrower than round 1 stated.
- No historical payload is altered, merged, or renumbered. The pre-repair and
  repaired payload hashes remain split exactly as recorded.
- No novelty is claimed. The underlying mathematics is the quotient
  factorization lemma.
- These are defects in a *specification*, not evidence of an error in the
  historical reasoning that produced it.
