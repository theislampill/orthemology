# Exact verification and coverage boundary

## What this handoff freshly establishes

At creation time, the local container held **61 top-level original files**, totaling **160,704,337 bytes**, including **48 top-level ZIPs**. The script that produced `07_SOURCE_INDEX/` calculated SHA-256 for every original, verified `ZipFile.testzip()` on all 48 originals, recursively inspected **168 distinct ZIP byte identities**, tracked **62 repeated nested aliases**, and recorded **23,200 ZIP central-directory member occurrences**. It identified no unreadable nested archives and **no font files to redistribute**. These are source-byte/inventory results, not source interpretation or mathematics verification.

The exact original bytes are placed under `ORIGINAL_UPLOADS/` in the Full edition. The separate Starter edition is a textual orientation and selected-source convenience package; it does not claim to include every original byte.

Fresh current read-only GitHub metadata established repo main commit pins and the merged state of PR30, PR31 and PR33, recorded in `01_PROJECT/REPOSITORIES_AND_PUBLICATION.md`. It is **not a fresh whole-repo source audit or CI replay**.

Selected key Markdown source documents in `08_SELECTED_ORIGINAL_REPORTS/` are extracted *byte-identically* from their original ZIP members; their `selected_document_origins.json` binds source ZIP, exact member path, byte length and SHA-256. No changes to original mathematical text are made by those convenience copies.

## Evidence ladder

1. **Filename or conversation report** — evidence that a result was reported, not necessarily that its source exists locally.
2. **Mounted source bytes / ZIP CRC / SHA manifest** — integrity and identity, not truth.
3. **Code tests / exact finite controls** — reproducibility for the represented finite cases, not automatic universal theorem proof.
4. **Written mathematics with inspected assumptions** — conditional general proof if the argument is correct; attribution/novelty still need checking.
5. **Lean proof checked against pinned calculus and admitted axioms** — formal theorem within the declared system, not mathematical meaning or metaphysical application for free.
6. **Source-critical Arabic/other text reading** — defensible contextual interpretation and bibliographic grounding at the particular scope; not proof of every associated theological inference.
7. **Independent human specialist replication / empirical testing** — a separate tier; none is asserted globally by this packet.
8. **Owner acceptance, release, PR merge** — governance and publication status, not mathematical/foundational truth status.

Each claim in these docs should be interpreted at its exact level. Status of different sections of one cumulative ZIP may differ.

## Known caveats to preserve

- Previously reported CI PASS for a **pinned** PR or code tree is stale after its code changes. In this handoff PR states were freshly checked, but CI wasn't newly rerun.
- First synthesis `Orthemology_T20_Whole_Corpus_Synthesis_20261010(1).zip` had 26/26 test replay reported. Later unobserved iterator and hybrid jump-timing limitations were identified. Old PASS must not be expanded to missing tests.
- Second synthesis recovered ~1MB actual mathematical authored work with a prior 52-test replay, but claims of complete original semantic source reading and all theorem novelty remain unearned.
- Many Lean formal packages rely on externally pinned Lean 4.19.0 + mathlib objects not in their portable ZIP. An included reviewer receipt is inherited validation until independently repeated.
- An internal AI reviewer may meaningfully catch errors but not provide the independence of an unexposed human specialist. The status `independently reviewed` within Dot frequently means **another AI/replay worker**, not a journal referee.
- Large nested archive indexes may contain draft claims later corrected by the same research. Prefer a final `RESULT.md`/`REVIEW.md` at a checkpoint's freeze; preserve historical red/green and failed-control evidence without confusing it with accepted success.
- Attribution: many methods have classical mathematical ancestors. In particular, a correct theorem can be classical but an exact conditional application or coupling can still be worthwhile. Novelty must be independently established.
- A repository or model can be technically correct while a modelled real-world assertion is ungrounded. The creator and cognition branches remain particularly sensitive to this category error.

## Source confidentiality and security

The original ZIPs are supplied by the project owner and may contain private working notes or material that should not be publicly disclosed. This packet is **not** a publication source projection. Avoid embedding secret information in future emails or GitHub issues; only send frozen, separately reviewed public materials. Do not publish source-file hashes as substitutes for licence review.

No passwords or secrets were sought or accessed to produce this handoff. Source archive files are included as given; do not execute unknown code or auto-extract untrusted paths indiscriminately. The included verifier reads ZIP members safely and does not execute inherited research scripts by default.
