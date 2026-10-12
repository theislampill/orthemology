# Multivalued reset continuation: exact coordinate-value quotients

Status: project-relative generalisation of the inherited Boolean reset theorem. Ordinary proof independently reviewed; formal core and future-observation corollary separately qualified in the execution receipt. No claim of external mathematical novelty.

## Setting

Let I be finite and X=∏ᵢAᵢ, with nonempty coordinate alphabets. The action alphabet contains every single-coordinate reset r(i,a), acting by replacing xᵢ by a, and any family of total coupled maps X→X. Let h:X→O. Write x≈y iff every finite common action word gives the same final h-output. The empty word is included. All states and all resets are admissible.

For values a,b∈Aᵢ, define a≈ᵢb iff for every context z∈X, z[i:=a]≈z[i:=b]. This definition is stronger than equal present output in all contexts: it quantifies all future words through ≈.

## Theorem

1. Each ≈ᵢ is an equivalence relation.
2. x≈y iff xᵢ≈ᵢyᵢ for every i.
3. Consequently X/≈ is naturally in bijection with ∏ᵢ(Aᵢ/≈ᵢ). The coordinate-class tuple is the coarsest deterministic summary preserving h and commuting with all declared actions, up to isomorphism of reachable summary states.
4. If all alphabets are finite, the number of minimal reachable summary states is exactly the product of the numbers of ≈ᵢ-classes. This is a state-cardinality result, not an efficient algorithm for discovering the classes from arbitrary black-box maps.

### Proof

Continuation equivalence is reflexive, symmetric and transitive, and is preserved by any common action word: prepend that word to each continuation test. Therefore the universal contextual relation ≈ᵢ is itself an equivalence.

For necessity in (2), suppose x≈y. Fix i and an arbitrary common context z. Reset every coordinate except i to its z-value. Finiteness supplies a finite common word. The resulting states are exactly z[i:=xᵢ] and z[i:=yᵢ]. Action-congruence gives their continuation equivalence. Since z was arbitrary, xᵢ≈ᵢyᵢ.

For sufficiency, enumerate I. Starting at x, replace coordinates successively by their values in y. At each replacement the two adjacent states differ only at that coordinate. Its assumed contextual equivalence gives continuation equivalence of the adjacent pair. Transitivity along this finite chain gives x≈y.

The coordinate-class map therefore has precisely ≈ as its kernel. Every tuple of coordinate classes has a representative state (finite choice), giving the bijection. Each action descends because ≈ is an action congruence, and h descends because the empty word is tested. Conversely, equality of any deterministic summary with a correct output decoder and commuting update entails equality after every word and hence ≈. It cannot identify two distinct coordinate-class tuples. Counting finite products yields (4).

## Why the Boolean theorem is a special case

A Boolean coordinate has only two possible equivalence relations: identity or the universal relation. Thus it either retains its entire bit or retains nothing. The inherited essential-dependency closure theorem identifies exactly which alternative holds under its Boolean/full-reset conditions.

For three or more values a coordinate can be genuinely essential while some of its values remain equivalent. Essential/nonessential membership no longer determines its minimal state cost. Example: one ternary coordinate, only resets, h(0)=h(1)=0 and h(2)=1. The coordinate is essential, but the exact quotient has two states, not three. Adding a total coupled action that sends0 to0 and1 to2 can split the previously merged pair; all three values then become distinguishable. A quotient justified for one intervention alphabet need not survive an expanded alphabet.

## Boundaries and foundational relevance

Full resets are used for necessity, and the full Cartesian state space supplies every common context. Restricted interventions or coupled admissibility constraints require a different theorem. Infinite coordinate sets need not permit the finite isolation/telescoping words. The relation concerns declared observations and updates; it does not authenticate source provenance, establish the truth of h, or prove actual warranted cognition.

For a noetic model with more than two statuses per ground, the result identifies a precise representational question: which statuses remain distinguishable under every authorised future correction? It does not say that a named status is psychologically real or normatively warranted. Nor does it justify forgetting distinctions that a later source-revision action can expose. The faithful sidecar is relative to the specified correction language, extending the inherited binary continuation architecture without asserting that every coordinate must be stored literally.

## Independent-review refinements

From any designated initial state all full-product states are reachable by a finite reset word, so the reachable-quotient count is attained in this setting. The induced quotient update may remain coupled across coordinates. The count is not an optimal bit-encoding or computation-cost theorem.

The finite-coordinate hypothesis is essential. On Boolean sequences indexed by the natural numbers, let h record whether infinitely many entries are1, with only finite words of coordinate resets. Every contextual coordinate relation is universal, but the all-zero and all-one states have different h-values. Without resets, even finite Boolean parity gives a nonproduct continuation kernel. These are genuine missing-assumption controls, not counterexamples to the stated theorem.

Kernel scope: the Lean file proves coordinate-equivalence, abstract reset-congruent relation factorisation, and its direct corollary for all finite future action words with explicit reset-label semantics, for dependent coordinate alphabets. Quotient bijection, reachable-state cardinality, and the infinite-coordinate boundary remain ordinary written proofs with independent review; they are not silently given kernel credit.
