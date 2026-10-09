# Addendum: the local transport needs less than S5

Date: 2026-10-09. This supplements, without replacing or editing, the independent modal assessment and its original control.

## Confirmed refinement

For the compressed reconstruction with globally true implications C -> S and S -> box C, symmetry of accessibility alone suffices for possibility of C -> C. Reflexivity, transitivity, and full S5 are unnecessary for this local inference.

Proof: suppose w accesses v and C holds at v. The two implications yield S at v and then box C at v. Symmetry means v accesses w. Therefore C holds at w. Equivalently, not-C at w implies box not-C at w.

The modal step is precisely the standard dual form of axiom B:

    diamond box p -> p.

The two explanatory implications give diamond C -> diamond box C; dual B then gives actual C. In standard notation, B is often written p -> box diamond p. Substituting not-p and taking the contrapositive gives the displayed dual form.

Global truth of the explanatory implications is stronger than the proof needs. At the evaluation world it is enough to have:

    box(C -> S) and box(S -> box C).

The proof uses those premises only at the accessible witness world. This addendum claims a clean sufficient condition, not an exact necessary frame condition for every model satisfying globally persistent C.

## Checked failure without symmetry

Use two worlds with accessibility {(w0,w0), (w0,w1), (w1,w1)}. This frame is reflexive and transitive, but not symmetric. Let C and S both be false at w0 and true at w1.

Both C -> S and S -> box C hold at every world: w1 accesses only itself, where C is true. Nevertheless, not-C holds at w0 and C is possible there. Thus even reflexivity plus transitivity does not validate the desired transport from these premises. No empty successor set or vacuously true terminal-world box is involved.

The small executable control `symmetry-premise-control.py` checks this example and all 16 C/S valuations on one symmetric, nonreflexive, nontransitive two-world frame. The latter has two assignments satisfying the explanatory premises, and neither is a counterexample. Results are recorded in `symmetry-premise-control-results.json`. This finite control illustrates the general proof; it is not a frame census or a claim of metaphysical possibility.

## Philosophical effect

The substantive assessment is unchanged. Cross-world explanatory adequacy and exhaustiveness remain premises; reducing the modal frame assumption cannot establish them. The source's S5 assumption is sufficient, but attributing the local burden-shift specifically to the full strength of S5 would overstate what this reconstruction uses.

This result concerns the transport after S -> box C has been admitted. It does not show that symmetry alone yields invariance of arbitrary modal-status predicates, or replace O'Connor's wider conception of absolute necessity in p. 42 n. 20. In particular, the original report's route through an invariant rich-profile predicate H may use stronger modal resources to establish that invariance. The present route bypasses that intermediate claim by admitting the already-compressed necessary-adequacy premise.

Recommended precise formulation: given the admitted explanatory and essential-coverage premises, symmetry already suffices for the local reversal from actual noncompleteness to necessary noncompleteness; S5 is a stronger sufficient framework. Neither the proof nor its weakening turns the thin coverage-switch model into a counterexample to the rich explanatory profile.
