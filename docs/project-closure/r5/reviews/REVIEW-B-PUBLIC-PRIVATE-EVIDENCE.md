# R5 Review B — public/private evidence attacks

Surfaced model: `claude-fable-5`. Publication-facing prose (manuscript/, theory/, companion/) scanned for casebook / Branch 11 / transcript-verified / real and recurrent / observational support / observational record / unpublished counts: zero occurrences; the only standing mentions of the private records are the boundary statements themselves (README/STATUS honesty notes; manuscript §17 non-evidential provenance).

Attacks: (1) casebook-evidence sentence appended to the manuscript — DEFEATED; (2) Branch-11 reference appended to a companion — DEFEATED; (3) the availability-section no-dataset statement stripped while the abstract copy remained — **SUCCEEDED on first run** (the presence check was file-global). Repaired: the check is now section-scoped (the availability section must itself carry the statement and the non-evidential clause); attack re-run — DEFEATED. No other blocking findings.
