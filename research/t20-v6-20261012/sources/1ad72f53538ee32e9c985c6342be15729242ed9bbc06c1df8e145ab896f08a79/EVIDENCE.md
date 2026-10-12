# Review evidence and replay

This directory contains the independent finite Bayesian compatibility review and its exact executable controls. The reviewed source is frozen by SHA-256 in REVIEW.md. No universal theorem is claimed to have been proved by enumeration or by a formal proof kernel.

## Files

- REVIEW.md: findings, claim-by-claim proof assessment, hypotheses, ancestry and limitations
- reviewed_target/RESULT.md: exact source text to which this review applies
- reviewed_target/INPUT_BINDINGS.json and MANIFEST.json: original target bindings
- INPUT_CHECK.json: five packet-file and seven inherited-input hash/length checks, plus two recomputed Git blob IDs
- PRESERVATION_CHECK.json: all 13 original file hashes unchanged at review preservation check
- AUTHOR_RERUN_RECEIPT.json: author replay identity and local Python/SymPy versions
- author_rerun/verify.py: unchanged author control script, run here because it writes to its own directory
- author_rerun/CHECK_RESULTS.json and verification.txt: rerun outputs, byte-identical to original outputs
- independent_controls.py: independently implemented Fraction-based controls; no import from author code
- INDEPENDENT_CHECK_RESULTS.json and independent_verification.txt: complete successful independent control output
- PROJECTION_QUALIFICATION.json: exact nonconvex two-minimizer scope countercontrol
- INHERITED_SOURCE_SCAN.json: bounded keyword line index over four inherited result packets; not a novelty proof
- MANIFEST.json: SHA-256 inventory of review files excluding the manifest itself

## Replay

Use ordinary Python with assertions enabled, not python -O. The independent controls need only the Python standard library. The author replay additionally needs SymPy; its observed version is recorded in AUTHOR_RERUN_RECEIPT.json.

From this directory:

    python author_rerun/verify.py > author_rerun/verification.txt
    python independent_controls.py > independent_verification.txt

Both commands write only under this review directory. Compare author_rerun/CHECK_RESULTS.json with the original packet's CHECK_RESULTS.json, or use the stored byte-identity receipt. The independent JSON includes runtime data, so a replay under another Python/platform may change runtime metadata while leaving mathematical check details equal.

The reviewer control file initially had one unmatched parenthesis, corrected before any control completed. The retained final script then ran successfully without a failed assertion. This was a reviewer-script construction error, not a defect in the reviewed source.

## Source inspection scope

Local source inspection covered the complete target RESULT and verify.py, all input and manifest bindings, the relevant normalization and perspective hypotheses/decomposition, G1 status and feasibility boundary, Deep AX V2 Sections 1–5, and the audit-continuation inherited-observable boundary. The four-packet keyword index is navigation only.

External reading was limited to the Aitchison/Ng publisher abstract, metadata and keywords; the Krogdahl publisher-indexed abstract and bibliographic record, with direct page retrieval failing; and Grünwald/Halpern Sections 5.1–5.2 and adjacent introduction material. No full-text Aitchison/Ng, Krogdahl or Csiszár audit is claimed.

## Authority

The result is a bounded independent review within the existing research task. It is not an external endorsement, Lean compilation, formal-kernel validation, integration, release or T20 closure. No original packet, protected repository file or source doctrine was changed.
