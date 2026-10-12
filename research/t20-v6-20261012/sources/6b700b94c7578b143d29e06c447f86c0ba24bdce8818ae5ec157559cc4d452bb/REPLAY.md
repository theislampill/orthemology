# Replay the author controls

Run from the workspace containing this packet and both bound predecessor packets:

    python cumulative-square-positivity-20261010/check_controls.py

The script reads predecessor files without changing them and writes CONTROL_RESULTS.json in its own directory. To retain console output as in the author run:

    python cumulative-square-positivity-20261010/check_controls.py > cumulative-square-positivity-20261010/check_controls.log

For an isolated copy of this packet, point to the original read-only source workspace explicitly:

    python /path/to/copied-packet/check_controls.py --source-root /path/to/source-workspace

Python and SymPy are required. The actual SymPy version and categorized executed checks are recorded in CONTROL_RESULTS.json. The checks are exact symbolic identities and digest verification, with no floating-point acceptance thresholds. They supplement, rather than establish, the universal written proof.
