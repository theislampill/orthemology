# Pilot 0 scoring rubrics (deterministic)

Each probe scores 0/1 by the criteria below; no partial credit; no rater discretion beyond the written criteria (edge cases → ADJUDICATION-MANUAL.md; unresolvable by the manual → deviation ledger, item excluded from that endpoint).

**General rules.** Scoring is on content, not vocabulary: a response earns the point by expressing the criterion in ANY words (coined, sham, or ordinary). For endpoints where lexical scrubbing is declared, coined/sham labels are replaced by XXXX before rating. Token counts: `len(response.split())` on the raw response; primer amortization per the frozen v0 B.8 rule.

| Item | Probe | Score 1 iff the response… |
|---|---|---|
| P0-ID-1 | version mismatch | states the log/evidence describes an earlier or different state than the one being approved (any wording: "stale log", "different commit", "log predates the force-push") |
| P0-ID-1 | re-evidence | requires re-running/refreshing evidence or an explicit argument the refactor could not affect it — and does NOT simply reject the fix as wrong |
| P0-PL-1 | both defects | mentions BOTH the labeling defect and the seal defect as separate matters to handle |
| P0-PL-1 | composed routes | prescribes actions covering both (relabel all + quarantine/replace/inspect the three); shipping-after-relabel-alone scores 0 |
| P0-PW-1 | result/pathway split | states the pass is correct today AND the check itself is defective/unsound/unreliable |
| P0-PW-1 | neighbor prediction | predicts a failure case: a non-clean artifact would also pass (or removal of the string would fail a clean one) |
| P0-FC-1 | rejects Done | rejects or qualifies the 'Done' status citing at least the storage-team item |
| P0-FC-1 | names dispositions | distinguishes at least two non-resolved states (waiting-on-another-team; accepted-risk) instead of one undifferentiated "not done" |
| P0-RR-1 | rule revision | prescribes changing the freshness/timestamp rule itself (e.g., compare in UTC/monotonic time) as distinct from patching a fifth service |
| P0-RR-1 | impact recheck | flags reviewing/re-checking past decisions made under the defective rule (any scope wording) |
| P0-MB-1 | localizes binding | attributes the defect to the case-specific choices (datum plane and/or calibration) while explicitly NOT blaming the standard, the procedure, or the fitter |
| P0-MB-1 | luck vs pathway | states the pillar's actual perpendicularity does not validate the verification (right result, defective verification) |
| P0-MB-1 | both binding defects | names BOTH the wrong datum plane AND the expired calibration |
| P0-MA-1 | no contradiction | states the two reports are consistent (one fact indexed to two sides/objectives) |
| P0-MA-1 | categories apart | keeps at least three of {position, per-side objective, search policy, game rules, analysis standards} explicitly distinct |
| P0-NC-1/2 | simple fix | prescribes the one-step fix; introduces NO framework structure (no profiles/ledgers/verdicts) |
| P0-NC-1/2 | overhead guard | (measured, not scored) response token count; guard statistic = arm-mean minus Arm-A-mean |

**Comprehension checks (C and C′ primers only, scored before items):** five matching questions (term → definition, shuffled); accuracy recorded per rater/model; the C′-interpretability gate compares these accuracies.
