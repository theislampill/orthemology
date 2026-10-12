# Independent review: belief-state positive repair

PASS on the final separate author freeze, 2026-10-11 UTC. No required revision. This review is additive; the prior main review, its original bindings, and wording-only addendum are unchanged.

## Proof and boundaries

For finite state space, positive reference, and a>0, escort F and inverse H are continuous bijections of the full simplex, including faces. Strictly positive likelihoods make every branch defined. The original predictive masses g_o(q)=L_o·H(q) are positive, continuous, and sum to one. The displayed g_o(q)δ_(o,T_o(q)) therefore defines a genuine Borel Markov kernel on outcome × transformed-belief state. Intertwining T_o F=F B_(L_o) proves by induction that every finite trajectory has q_t=F(p_t); using original predictive masses preserves word probabilities and inverse target readouts simultaneously.

The explicit product-likelihood formula correctly assumes fresh conditionally independent uses of one passive channel given a fixed latent state. The report explicitly excludes rereading one stored observation as fresh evidence and requires the appropriate joint instrument for dependence or changing states. No additional stopping theorem is asserted.

This is a coordinate transformation of a full belief-state observation kernel. It does not provide fixed likelihood rows acting directly on q as probabilities of the original hidden state. In general g_o is nonlinear in q. The concrete mass discrepancy 3/8 versus 7/16 is exact. The added outcome-11 example is also exact: decoded first posterior (4/9,2/9,1/3), next mass 17/36, word mass 17/96, final transformed state (2/7,2/7,3/7), decoded posterior (4/17,4/17,9/17). Thus the repair does not contradict the main fixed-channel obstruction. Crucially, interpreting correction as actual changed beliefs and then decoding back to old beliefs changes that interpretation; the report says so explicitly. No evidence, authenticity, warrant, or new mechanism claim follows.

The inherited audit-continuation finite-instrument/readout contract, correction-audit-transport conjugation and normalizer recovery, and stochastic-inquiry predictive-versus-stopping boundaries were inspected. They support the attribution of this note as a bounded coordinate-change application rather than a new general Markov/filtering theorem.

## Controls and final identity

Separate belief_controls.py passed 43 exact symbolic checks, including actual radical-coordinate transitions, inverse readout, nonlinear predictive masses, and all eight binary words of length three. Isolated author verify_repair.py replay passed 4,621 assertion groups over 511 histories through length eight, including source hashes. The final narrative-only outcome-11 paragraph was independently checked and resnapshotted; the replayed code is byte-identical to the final frozen code. Every repair freeze hash was independently recomputed.

REPAIR.md SHA-256: 6b77cd702ae8ce8124a589b7c0603b05b90a536578f9cdfcf0df38d226acedfe. REPAIR_REVIEW_BINDINGS.json binds the adopted repair files and unchanged main report/freeze. This is ordinary independent review, not formal certification, release authorization, or programme closure. No original/protected edits were made.
