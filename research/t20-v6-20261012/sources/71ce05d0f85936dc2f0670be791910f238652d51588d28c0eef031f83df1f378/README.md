# Event-feasibility independent review

Read REVIEW.md for the mathematical verdict and exact scope. This directory contains a frozen original-author replay, separate independent controls, identity bindings, and unchanged-source receipts.

Portable replay from this directory:

    python3 author_replay/event-feasibility-descent-20261010/verify.py
    python3 independent_controls.py
    python3 verify_bindings.py --portable

The first program writes only its isolated copied CONTROL_RESULTS.json. The second writes only INDEPENDENT_CONTROL_RESULTS.json. The identity checker makes no writes. Removing --portable additionally checks the original workspace's source paths.

Expected author result: 29 groups, 304 support patterns, 252 exact support certificates, 52 explicit fibre ambiguities. Expected independent result: 29 groups, including 20 selected parity-support cases. These are bounded exact calculations accompanying a general proof review, not formal-kernel certification, field-novelty evidence, or closure authority.

MANIFEST.json binds every delivered review file except itself. Direct inherited result bytes are under author_replay; additional inspected reports are under inspected_sources. No original target file was edited.
