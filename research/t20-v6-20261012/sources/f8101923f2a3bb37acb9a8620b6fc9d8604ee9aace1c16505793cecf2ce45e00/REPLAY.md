# Replay

From the workspace root:

    python partial-cumulative-one-hidden-lift-20261010/check_controls.py

The script uses Python and SymPy and writes CONTROL_RESULTS.json. Its existing successful run is also recorded in check_controls.log. It checks input integrity, SOS telescoping, both finite Volterra endpoint orderings through exact formal coefficients for varying energies, wrong-endpoint mutations, factorial cancellation, the active cumulative Gram certificate, genuinely noncommuting quadratic matrices, Gaussian hierarchy identities, inherited Stieltjes cancellation, the graph-law variance discriminator, the higher-degree scope boundary, and finite exact tensor-product positivity/reaction controls.

For a preserved original packet, copy the complete directory to a separate replay directory and set LIFT_SOURCE_ROOT to the original workspace root before running. The copied input code is executed locally; the accepted source directories are read only. The script does not execute any protected integration or closure operation.

The finite controls do not prove Hamburger or Putinar–Schmüdgen existence, uniqueness of Fourier transforms, the all-degree full-functional premise, or the universal lifting theorem. Those claims are established by the identified classical inputs and written proofs.

Proof map:
- RESULT.md: quadratic theorem, precise two-direction local proof, signed-field equivalence, continuation, conditional uniqueness, discriminators.
- GENERAL_SOS_BRIDGE.md: separate fixed-controlled-variable SOS extension through signed Fourier projections.
- SHARP_HIDDEN_BOUNDARY.md: separate tensor obstruction for at least two hidden variables, using the bound full-functional premise.
- SOURCE_CHECKS.md and INPUT_BINDINGS.json: reading scope, attribution, dependencies, and hash bindings.
- AUTHOR_RECEIPT.json and FROZEN_MANIFEST.json: executed evidence and frozen artifact inventory.
