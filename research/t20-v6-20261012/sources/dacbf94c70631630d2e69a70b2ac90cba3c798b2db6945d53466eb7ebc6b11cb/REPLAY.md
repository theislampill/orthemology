# Replay and evidence scope

Run with Python 3 and SymPy:

    python check_exact.py --output-dir /absolute/fresh/output-directory

The output directory must not exist. The portable report has 25 checks: 19 small symbolic controls and six copied-input hash checks. To check the original six ancestor files as well, add:

    --original-root private-locator:8f24556a330b05a11a95

That run has 31 checks. Both author reports were executed with Python 3.12.14 and SymPy 1.14.0. The final checker was re-executed after clarity changes, and its report matched the historical author report byte for byte. No failing control run occurred.

The controls cover the action-tail derivative, comparison exponents, high-region algebra, the inherited double-well variance example, probability primitives and clock for the heavy-tail example, its two-interval variance constant and divergent length primitive. They do not compute a general analytic exponent, prove the uniformization by enumeration, sample trajectories, or establish formal-kernel verification. The proof is in RESULT.md.

INPUT_BINDINGS.json gives the exact copies and their original paths. No predecessor is written. The author's frozen manifest binds all payload files after verification. New replay or review outputs must be placed outside the frozen directory.

Primary source consulted on 10 October 2026 UTC: Absil, Mahony and Andrews (2005), Lemma 2.1, printed p.533, https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf . Only the finite-dimensional local analytic inequality is imported; the compact-level finite-cover argument is provided here. The inherited spherical-action source interface supplies the declared unit coefficients, without transferring a torus density theorem to arbitrary measures on R^d. No source paper is redistributed.

Independent review and preservation are separate. The initial-time countercontrol is outside the all-moment initial-hierarchy class, while every supplied all-moment initial law satisfies finite-energy sufficiency. No protected integration, philosophical identification or programme closure is claimed.
