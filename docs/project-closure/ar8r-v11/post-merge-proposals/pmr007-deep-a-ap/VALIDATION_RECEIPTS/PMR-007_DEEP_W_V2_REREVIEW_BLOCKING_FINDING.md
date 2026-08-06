# PMR-007 Deep W V2 fresh-rereview blocking finding

Disposition: `REPAIR_REQUIRED`.

The independent natural-join implementation reproduced the full-key pullback
and verified 168,505 compatible finite cones with zero universal-property
failure. Frozen hashes also matched.

However, the finite witness family did not independently exercise every field
that the V2 prose called load-bearing:

```text
target_id:
  no A/B pair differed only in target_id;

semantic_contract_digest:
  digest difference was coupled to version difference rather than isolated.
```

The theorem's standard universal property is unaffected, but the claimed
countermodel/evidence coverage is incomplete. Because the packet explicitly
advertises a target-identity and semantic-contract firewall, this is blocking
for admission.

Required repair:

1. add a valid profile object whose target differs from an otherwise identical
   warrant object;
2. add a valid warrant object whose semantic-contract digest differs from an
   otherwise identical profile object;
3. rerun the primary checker;
4. freeze V3;
5. rerun a distinct key-erasure and universal-property rereview.
