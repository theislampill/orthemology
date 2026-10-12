# Input identity label clarification

An earlier local `verify_input.py` result used the ambiguous label `OBSERVED_ATTACHMENT_IDENTITY_MATCHED_TO_P01_RECEIPT`. The input preparation receipt binds its own source/evidence outputs; it does not provide a detached hash of its enclosing ZIP. The enclosing ZIP hash was observed from the actual uploaded bytes and then rechecked locally. The current script states that provenance explicitly as `OBSERVED_ATTACHMENT_IDENTITY_RECHECKED_AGAINST_INITIAL_LOCAL_DIGEST`.

The earlier raw output remains unchanged. Neither the measured input bytes/digest nor any verified source/evidence member identity changed. The final research receipt records the actual observed attachment identity; it is not represented as an externally supplied expected attachment hash. No input or canonical source record was edited.
