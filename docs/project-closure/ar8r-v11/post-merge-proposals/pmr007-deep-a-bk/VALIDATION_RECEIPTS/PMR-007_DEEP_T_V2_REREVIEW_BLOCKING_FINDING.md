# PMR-007 Deep T V2 rereview blocking finding

Disposition: `REPAIR_REQUIRED`.

The independent authority/profile rereview reproduced the mathematical and
ledger results but failed the frozen scope-guard check because the canonical V2
packet did not contain two required unambiguous formulations as exact clauses:

```text
The registered profile is not claimed to contain every current or possible
neutral discriminator.

Source compatibility is not neutral explanatory dominance.
```

The surrounding prose substantially implied both limitations, but the admission
contract requires these two authority firewalls to be explicit rather than
recoverable by interpretation. V2 remains preserved as a pre-repair candidate.
