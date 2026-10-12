# Constrained-learning independent review

Read REVIEW.md for the bounded verdict, proof checks, source scopes, and limits.

The exact author packet and eight bound inherited inputs are under replay/. Run the unchanged author controls safely against that copy:

    python3 replay/constrained-learning-possibility-20261010/verify.py

Run the four separately implemented reviewer controls:

    python3 independent_controls.py

REVIEWED_EXACTFILES.json binds the author/input snapshot; MANIFEST.json binds this completed review. Executing either verifier regenerates only its own result file. No author source is changed. There are no third-party Python dependencies. External primary-source documents were read through web tools; full remote PDF bytes are not included, and original Aumann–Maschler lemma text was not inspected.

This review does not authorize integration, release, protected changes, or T20/programme closure.
