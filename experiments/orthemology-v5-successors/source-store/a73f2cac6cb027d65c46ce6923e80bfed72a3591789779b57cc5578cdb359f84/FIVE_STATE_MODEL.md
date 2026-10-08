# Five state evidence control

This is an ordinary written mathematical control, not a measured model of an organisation, an implementation or a Lean-certified theorem. The construction is supplied in the report. This supplement makes its full information structure and failure boundaries explicit.

## Fixed ingredients

The states are 0, 1, 2, 3 and 4, with probability masses 1/10, 2/10, 2/10, 2/10 and 3/10. State 0 is actual. Let A={0,1,2}, B={0,1,3}, C={0,2,3} and H={0,4}.

Member 1 observes the truth values of A and B. Member 2 observes A and C. Member 3 observes B and C. The complete observation partitions are therefore:

- Member 1: {0,1}, {2}, {3}, {4}
- Member 2: {0,2}, {1}, {3}, {4}
- Member 3: {0,3}, {1}, {2}, {4}

A proposition is known at a state if and only if it is true throughout the member's corresponding information cell. This is the ordinary idealised partition interpretation. At the actual assessment in state 0, relevant ease of access on the assessment timescale is an additional explicit premise: no further easy perceptual, testimonial, memory or inferential route supplies the missing indicator or equivalent information. Mere ignorance would not establish that premise. It is not a global or public announcement that every member lacks a missing indicator in every state; some nonactual cells are singletons.

The model and probability law are common background, but the actual state, the other members' observations and the actual group inventory are not publicly announced. The analyst's description of what holds at state 0 is not an announcement to the model's participants.

## Actual state check

At state 0, the three cells are {0,1}, {0,2} and {0,3}. Member 1 knows A and B, member 2 knows A and C, and member 3 knows B and C. Each indicator is thus known by two of the three equally relevant members. No member knows the missing indicator, H, or A-and-B-and-C.

The three components jointly entail H because their intersection is {0}, which is a proper subset of H. The proper-subset fact matters: H has not simply been defined as the conjunction. The extra H-state is state 4. Ordinary conditional probability gives P(H|A and B and C)=1.

Each actual private cell has total mass 3/10 and contains H-mass 1/10. Each member therefore has P(H|their cell)=1/3 and P(not H|their cell)=2/3. Any move from those probabilities to outright individual belief, and then from those beliefs to group belief, needs an additional belief policy. It is not part of the probability calculation.

Under a pointwise inventory rule accepting components known by a relevant majority, A, B and C enter the inventory. The set's joint entailment is evaluated over those entries; it does not require listing their conjunction as a fourth entry. This says nothing by itself about available integration or group knowledge.

## Baseline sensitivity

Unconditionally, P(H)=2/5, so each private cell lowers H to 1/3. Let the common background instead include D={0,1,2,3}, before assessing the same private observations. Then P(H|D)=1/7. Since each actual private cell is already contained in D, its posterior remains 1/3. Relative to D, that same observation raises H.

The posterior ranking, the private ignorance and joint entailment remain unchanged. Only the incremental comparison reverses. Therefore no background-invariant confirmation claim follows from this example.

## What would change the conclusion

1. Publicly announcing all three actual indicator values would eliminate the missing-information structure. Publicly announcing that all three components are in the stipulated majority-knowledge inventory likewise discloses their truth in this model. Neither announcement is present in the construction.
2. Giving an easy communication or testimony route can defeat the no-easy-route premise even before a member actually uses it. The relevant theory must specify its access standard.
3. Changing evidence membership to require an operative integration process changes the inventory/support theory being tested. The present conditional result cannot decide that theoretical choice.
4. Adding a belief threshold or majority-vote policy creates a further model. The calculation alone does not prescribe one.
5. Permitting noisy observations requires a different information and factivity treatment. The stated partition model assumes accurate observations.
6. Applying the model to a real organisation requires evidence for its bearers, observations, access routes, probabilities and support standard. The illustrative numbers supply none of those empirical bindings.

The intended result is therefore precise: component membership, set-level entailment, individual access, practical integration and group belief are different relations. This control tests one proposed inference between them without claiming a general new probability theorem or an actual collective-knowledge finding.
