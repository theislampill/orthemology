# SPA-R5 — epistemic closure radius as the common-knowledge correction term

**Status:** specialist-local standard finite epistemic-logic construction; no
novelty; durable ancestry locator remains for Deep Research 20.

## Frozen model

A finite Kripke model has two agents, equivalence accessibility relations, a
frozen proposition valuation, and common knowledge defined over the
reflexive-transitive closure of the union of the two relations.

## Result

For actual world `w`, let `d(w)` be the maximum shortest-path distance from `w`
to a world in its union-accessibility component. Then

```text
C phi at w  iff  E^d(w) phi at w.
```

Because the model is finite, `d(w) ≤ |W|-1`. This is a finite closure bound, not
a claim that one acknowledgement or one round of mutual knowledge is common
knowledge.

## Countermodel

Agent A has partition `{0,1}|{2}`; agent B has `{0}|{1,2}`; `phi` is true at 0
and 1 but false at 2. At world 0, both agents individually know `phi`, yet the
alternating A/B path reaches world 2, so common knowledge fails. The correction
term is the union-reachability radius.

## Executable evidence

The checker exhausts 15,034 model/valuation/world cases through four worlds.
The radius criterion and the universal `|W|-1` bound have zero mismatches. It
finds 588 distinct cases where first-order everyone-knows holds but common
knowledge fails.

Six mutants are killed: private acknowledgement, one-step mutual knowledge,
depth equal to agent count, omitted closure radius, prefilled counters, and
transfer to an asynchronous protocol.

## Conclusion ceiling

This does not establish delivered messages, acknowledgement reliability,
common clocks, execution, warrant, provenance independence, or source truth.
