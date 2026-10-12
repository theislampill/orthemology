# Signed autonomous energy continuation

Read RESULT.md for the complete ordinary proof. The principal new implication is full-square-positive hierarchy forcing for autonomous signed polynomial energies from initial weighted-energy determinacy. Bounded energy gives a global path; compact joint support also gives unique laws and locally finite signed switching. An initial exponential energy moment covers unbounded data. A Gaussian negative-quadratic control shows an exact finite maximal horizon. Null ideals and every fixed finite polynomial Gram matrix's kernel and rank are invariant, even without an initial joint measure.

Artifacts:

- RESULT.md: theorem, full proof, corollaries, countercontrols and source attribution
- check_controls.py: exact symbolic/rational controls
- CONTROL_RESULTS.json and check_controls.log: executed author evidence
- INPUT_BINDINGS.json and inputs/: copied and hashed retained mathematical inputs
- FREEZE.json: exact reviewed-candidate file identities, once frozen

Author replay:

    python check_controls.py

Nonmutating review of this original directory:

    python check_controls.py --retained-root private-locator:8f24556a330b05a11a95 --output-dir /path/to/new/review-output

The same command works after copying this entire directory to a fresh location: keep the retained-root argument pointed at the unchanged original input directory. The script writes only its chosen output directory; it reads the four retained input files to verify their hashes. It requires Python and SymPy. No network, random sampling, numerical integration, or proof by finite cutoff is involved.

The participating proof-route check is separately stored in signed-energy-proof-check-20261010/REVIEW.md. It does not constitute independent final-artifact review. No protected sources were edited; no Lean or other formal-kernel proof, field-priority, canonical integration, or T20 closure is claimed.
