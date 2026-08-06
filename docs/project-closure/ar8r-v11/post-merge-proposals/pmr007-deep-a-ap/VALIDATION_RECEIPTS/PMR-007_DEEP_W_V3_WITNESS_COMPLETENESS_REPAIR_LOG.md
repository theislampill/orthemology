# PMR-007 Deep W V3 witness-completeness repair log

Repairs the blocking V2 fresh-rereview finding.

The V2 universal property passed, but its finite model lacked independent
key-erasure witnesses for:

```text
target_id;
target_version;
semantic_contract_digest.
```

V3 adds three valid warrant objects, each differing from `A_OK` in exactly one
of those coordinates. No theorem statement is strengthened. The change repairs
only the advertised countermodel coverage.
