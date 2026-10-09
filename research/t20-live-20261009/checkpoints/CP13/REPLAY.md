# Bounded preservation checks

Use Python 3.12 or compatible standard-library Python. No packages or network are needed. Run from the extracted checkpoint root:

    python -B PACKING/check_manifest.py
    python -B PACKING/replay_python.py

The first command checks all packaged payload hashes, source copies, explicit native path/hash declarations, accepted author/reviewer relationships, correction snapshots and twelve prior identity records. Omitted dependencies are compared against the sealed registry, not silently fetched. Their actual retained bytes were checked during assembly; exact prior-member matches are distinguished from retained-file-only provenance.

The second command copies only each of the two inspected portable modal scripts to a separate temporary directory, executes it in isolated Python mode, and requires byte-identical recorded stdout (and the independent script's generated result). Author controls contain 626,901 assertions; separately authored reviewer controls contain 175,130. Finite tests do not substitute for general written proofs.

The native modal VERIFY.py is preserved but requires external predecessor files, so it is not claimed portable in this increment. The review's author_controls_snapshot.py is a byte-identical historical duplicate and is not executed again. No earlier Lean or Python science, source extraction, PDF read, or philosophical review is freshly replayed.

For a new extraction, invoke the trusted copy of safe_extract.py with ZIP path and a destination that does not yet exist:

    python -B PACKING/safe_extract.py CHECKPOINT.zip NEW_DIRECTORY

For disposable malformed-archive controls:

    python -B PACKING/integrity_controls.py CHECKPOINT.zip

Ten cases must reject: altered payload, missing/extra member, manifest alteration, traversal, absolute path, backslash path, duplicate member, symlink, and multiple roots. These are packaging tests, not research results. The external final receipt records fresh extraction/replay, binding-negative controls, source currentness and unchanged prior checkpoint files. It also binds the final ZIP; no self-referential ZIP hash is stored inside it.
