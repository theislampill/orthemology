# R7 Review E — FCSP leakage and unit audit

Surfaced model: `claude-opus-4-8`. Posture: treatment wins because the answer is stated, more tokens are provided, or repeats are pseudoreplicated.

- Answer-bearing phrase ("the evidence is stale and closure would be false") injected into a public item — **DEFEATED** (lexical/field-name leakage scan). Payload isolation is proven per run: no key/label/truth token in any exact `--dump-payloads` payload.
- Harness code path added to read `items/KEYS.json` — **DEFEATED** (methods gate: no harness code path may read the hidden keys).
- Units: the inferential unit is the item, paired; repeats are within-item replicates and temperature-0 reruns are never counted as independent; the pre-run sensitivity plan is item-level and there is no observed-power rescue. Ceiling/verbosity: the F9 negative controls + structure-overhead harm rule guard structure-for-structure's-sake. No blocking findings.
