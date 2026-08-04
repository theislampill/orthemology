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
content. Five of those are genuine defects rather than notation choices. They
are recorded here because they change what the packet may be read as claiming.

## D1 (A4) — "requires" is not a definition, and under the literal reading the characterization is false

The packet says: causal landing `L_b` **requires** all of clauses 1–6.

"Requires" states necessary conditions. Read literally the packet gives
`L_b → (c₁ ∧ … ∧ c₆)` and leaves `L_b` otherwise underdetermined. Under that
reading the characterization theorem is **false**: an underdetermined label can
differ on a fibre for reasons the six clauses never see.

This is machine-checked. The Lean development contains a proved existence
statement, `A4_requires_reading_is_insufficient`, exhibiting a profile map and a
pair (clauses, label) such that the label implies the clauses, the clauses are
fibre-constant, and the label is not. It depends on no axioms.

**Consequence.** The characterization holds only if `L_b` is *defined as* the
conjunction. The packet should be read as stipulating a definition. Any future
use of T299 that treats the six clauses as merely necessary is unsound.

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

## D3 (A1) — the twin is not formally an instance of the theorem it illustrates

The characterization quantifies over backgrounds `b` of one fixed model. The
twin's profile `B*(M,u)` ranges over model–unit pairs across two *different*
models. These are not the same index type.

As written, the twin does not instantiate the theorem. Two repairs are available:
either the theorem is about a fixed model and the twin illustrates something else,
or "background coordinate" must be read as absorbing the model identity. Only the
second makes the packet coherent, and the packet never says so.

## D4 (A14) — the declared model shape cannot express its own twin

The declared setting gives `Q : St → Bool`, with no background index. But the twin
requires `M_cause` and `M_spont` to disagree on `Q(S_term^(0))` — the same state,
different truth value. That is impossible for an unindexed `Q`.

Formalizing forced `Q : Bg → St → Bool`. This is a structural defect: the packet's
§0 and its final section describe incompatible signatures.

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

- T299's mathematical content is not refuted. Under the definitional reading,
  the characterization is true, machine-checked, and exhaustively finite-checked.
- No historical payload is altered, merged, or renumbered. The pre-repair and
  repaired payload hashes remain split exactly as recorded.
- No novelty is claimed. The underlying mathematics is the quotient
  factorization lemma.
- These are defects in a *specification*, not evidence of an error in the
  historical reasoning that produced it.
