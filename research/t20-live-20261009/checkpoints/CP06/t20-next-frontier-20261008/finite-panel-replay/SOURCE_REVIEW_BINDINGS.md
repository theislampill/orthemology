# Source, proof, review, and arithmetic bindings

Supplementary evidence only. The written proof supplies the all-count theorem; the independent review supplies a mathematical adversarial audit; the executable controls supply exact symbolic arithmetic checks. None is represented as kernel verification, a machine proof of the entire argument, or empirical validation.

## Bindings

dependent-gate-transport/RESULT.md

    b32125f6d4fc8a715e18b5f0761e3be88b8194d1f4db58f088cfc2df122ce997

finite-panel-replay/RESULT.md

    327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243

finite-panel-replay/SHARED_MARGINAL_BOUNDARY.md

    3d55f739d398ed1b4b28253cdb5db34ec9b32d46415e14750a612e35f43b4788

finite-panel-replay-review/REVIEW.md

    812eb02988e1e2e695e71fcdead1debbd20a9525570b5f3eb68c26b601af208e

finite-panel-replay/exact_controls.py

    04cffc5e5d694deb58f64e69f60479afd4a847234b75616c9f5c702d18e72a8b

finite-panel-replay/EXACT_CONTROLS_OUTPUT.txt

    ac4ccc9d9f475e5ed401f2682f9a938e5c75cf05d734d87e1a7b4f99414fc499

## What was inspected and checked

- The frozen dependent-gate-transport/RESULT.md was read as the predecessor model and scope source. No predecessor was edited.
- The finite-panel RESULT.md and SHARED_MARGINAL_BOUNDARY.md were independently reviewed. The review binds their exact hashes and reports PASS with explicit limitations.
- The supplementary exact_controls.py checks 33 symbolic identities, the n=1 specialization, local/copula panel identities, the route-specific-marginal products and homeomorphism joins, and the three frozen proof/review hashes. Its retained stdout is EXACT_CONTROLS_OUTPUT.txt.
- The script intentionally does not claim to verify Holder, all probability semantics, every analytic inequality, arbitrary m by enumeration, or the entire mathematical proof. Those claims remain in the written argument and independent mathematical review.
- The supplementary script and this binding record were added after the independent review. They do not retroactively enlarge the scope of that review.
- No external website was opened for this finite-panel proof or these controls. The standard inequalities used are written out and mathematically reviewed; this packet makes no literature-novelty assertion.

## Reproduce the arithmetic controls

Run from the base directory:

    python finite-panel-replay/exact_controls.py

The recorded run used Python 3.12.14 and SymPy 1.14.0, exited successfully, and printed 33 passing exact-identity checks plus three matching frozen hashes. There is no arbitrary finite numeric grid in this retained control script.

## Limits

The panel is calibrated/selectable in true reference-rate coordinates or only existential in latent coordinates. It uses exact probabilities and the same Bernoulli-pair law for fresh diagonal and retained-threshold replay observations. Shared marginals and mutual route independence remain substantive premises. No noisy-data guarantee, equality-decision algorithm, physical intervention validation, protected integration, or T20 closure is asserted.
