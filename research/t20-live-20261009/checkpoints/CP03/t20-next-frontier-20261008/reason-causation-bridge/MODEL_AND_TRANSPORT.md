# A form-sensitive causal implementation and its exact ceiling

## Question fixed before construction

Does having a sufficient local transition rule preclude implementing an inference that is sensitive to logical form and preserves truth? This is a weaker question than whether an entirely nonmental reality can originate thinkers who understand their reasons. The source's explicit computer objection makes that distinction indispensable.

The initial acceptance-only AND gate was rejected before construction as inadequate: it would respond to premise availability regardless of whether the premises instantiate a valid rule. The strengthened test uses fixed formula codes, a matching condition, compositional semantics and a deliberately unsound control. See PROSPECTIVE_TEST.md.

## Fixed apparatus

The two-bit codes 0,1,2,3 denote p, not-p, q, not-q. The codebook stays unchanged throughout. A nine-bit local input contains codes A, B and C, two premise-availability flags a,b, and one causally irrelevant noise bit z. The represented premises are A and B→C. A separate three-bit output consists of acceptance flag d′ and conclusion register D′.

The micro-transition uses only bit equality, conjunction and copying:

- d′ = a ∧ b ∧ (A=B)
- D′ = C

When d′ is zero, the formula in D′ is not accepted by this derivation. The mechanism does not assert its negation or declare it false. It does not decide every valid consequence. Matching formula codes is syntactic matching, not an independently established act of understanding.

A fixed abstraction map decodes the registers and drops z. The abstract transition applies the corresponding matching rule to the decoded formulas. For every input x, decoding the micro-output equals applying the abstract rule to the decoded input. This commuting property checks implementation fidelity, but is not the sole substantive test: an arbitrary chosen macro-description could make such a square uninformative.

The independent semantic condition uses all four valuations of p and q, with ordinary Boolean negation and material implication. “Input correct” means that every enabled premise is true. “Output correct” means that every accepted conclusion is true. These meanings remain fixed for original and faulty mechanisms.

## Soundness and the discriminating control

If the mechanism accepts, both premises are enabled and A=B. If enabled premises are true, A is true and B→C is true. Hence B is true and C is true. That is a mathematical conditional, not a thesis about what causes actual people to grasp implication.

The program checks all 512 packets, including both values of z, under all four valuations: 2,048 checks of conditional truth preservation pass. Many are vacuous because the input correctness condition fails or no conclusion is accepted; 32 cases have both true enabled premises and an accepted conclusion. It also checks 512 commuting-abstraction and 512 noise-invariance cases. These are finite exhaustive checks for this declared domain, not a proof about every possible cognitive system.

Dropping the A=B gate produces a decisive failure. Take A=p, B=q, C=not-p, with p true and q false. Both enabled premises p and q→not-p are true. The faulty mechanism accepts not-p, which is false; the correct mechanism withholds this derivation. Thus an output's dependence on two acceptance flags is insufficient, and the fixed interpretation makes the fault objectively testable within the model. A second mutant that ignores availability of the first premise also fails.

Changing only A, or only the implication's antecedent B, while holding both availability flags fixed alters the original mechanism's response. Changing C changes the output formula. These are interventions on encoded formula registers, not changes of the codebook and not interventions on disembodied meanings while physical facts stay fixed. They test form-sensitive implementation, not content causation as consciously understood.

## The external-premise control

For the unchanged local packet p, p→q, the machine accepts q. Under valuation p=true,q=true, the enabled premises and conclusion are true. Under p=true,q=false, the accepted implication and conclusion are false. Valid execution is preserved; input truth is not. No semantics is relabelled between cases.

This is initially a comparison of valuations with the same local packet, not an assertion that the same complete physical world can have different intrinsic meaning. The optional coupled version specifies upstream equations a=p and b=(not-p or q) or error. In the good case p=true,q=true,error=false; in the bad case p=true,q=false,error=true. Both cases obey the same equations and yield the same local packet. Their total external states differ. The second case explicitly includes source error; it does not silently retain a perfectly reliable sensor while violating its equation.

This shows precisely why a verified inference does not authenticate its input source. It does not show that a truth-connected, undefeated human inference lacks warrant, or that the correct device's output is never knowledge for its competent user.

## Four different kinds of dependence

1. Local operational closure: after a packet is fixed, the updater's next output is determined without a new outside input during that update.
2. Counterfactual input variation: different initially set registers define different runs. Such comparisons do not insert a new cause into a single closed run.
3. Historical design dependence: this specified program was constructed by reasoners. Its truth-preserving organization has not been shown to originate without them.
4. Interpretive dependence: a supplied codebook connects registers with propositions. This is separate from the causal history of the program. Neither dependence disappears merely because a run is operationally closed.

None equals metaphysical self-sufficiency of the whole natural world. A material process may also depend ontologically on a Creator without receiving a nonphysical intervention at each step. This construction takes no position on that further question.

## Exact transport result

A deterministic local causal mechanism can implement a form-sensitive, truth-preserving inference rule under fixed compositional semantics. Therefore local causal determination alone does not exclude formally appropriate transitions.

The qualification is essential. The model does not establish original intentionality, conscious grasp, warranted premise acceptance, human belief, evolutionary origin, or a reason's causal role *as understood*. It contains no measure over naturalistic worlds, so the enumeration supplies no probability of reliable cognition. Mathematical formula types and validity relations do not establish additional extramental necessary bearers or a separate causal action by abstract objects.

The result is a counterexample only to an unqualified implementation-incompatibility claim. It is not a counterexample satisfying the strongest chapter target's antecedent of an autonomously meaningful, wholly nonmental-origin total reality. Against that target it exposes the missing substantive bridge rather than settles it.
