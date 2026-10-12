# Bounded occurrence/warrant crosswalk

Read `RESULT.md`, then `RESULT.json` and `READING_RECEIPT.json` for exact scope. Review status at freezing: author checked; independent review pending. Frozen sources are copied unchanged; no upstream source is edited.

Reproduce from this directory:

    python controls/contract_check.py
    python -O controls/contract_check.py
    python controls/verify_boundaries.py
    python -O controls/verify_boundaries.py
    python controls/inherited_t16/check.py
    cd controls && python -m unittest -v && python -O -m unittest -v

The inherited T16 script uses assertions and is only credited in normal mode. The own controls use explicit requirements. `RED.txt` records the expected initial failing test against the stub; it is not an unresolved result. Normal and optimized JSONs are exact matches. The direct-signature oracle is a separate own code path, not independent review.

The actual application is to the seven supplied manual source records and one absorbing excluded-view state. It does not model a whole document store or human cognition. Work exclusion is a declared view operation, not a source defeater or revocation of authority; no reinclusion operation is claimed. No new Arabic interpretation, historical authenticity, philosophical warrant, general theorem, protected edit, adoption, or T21 is established.
