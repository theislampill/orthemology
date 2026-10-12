# Full actual-E Sigma elimination: bounded preservation checkpoint

For each admissible actual-E context, Sigma type and input, propositional Sigma eta is equivalent to weak dependent elimination over all actually formed motives and typed branches, and to strong elimination additionally supplying the retained raw erasure equation. The same equivalences hold uniformly. The original Form/Has premise restriction is removed; no additional source principle is introduced by this extension.

These are conditional metatheoretic schemas, not an internal source encoding of universal schemas or a proof that either schema is available. No universe, new constructor, universal witness selector or closed eta inhabitant is added. The fixed-input converse uses the actual formed eta motive and canonical pair branch. The forward construction retains the exact SigmaCompletion polynomials and reuses actual-E substitution and J transport.

Strong elimination's erased branch on projections is a raw PolyConv conclusion. It does not independently type that branch at P(z). The canonical-pair typed computation proves both endpoint typings separately before producing typed identity; arbitrary raw erasure does not license that identity and typed identity is not reflected into raw conversion. Raw computation is inherited and axiom-free. Central equivalences use propext and Quot.sound; inherited scope and model controls also use Classical.choice.

The R boundary directly reuses the existing all-rule tagged model. At the literal context [SigmaRaw,R] with Sigma input var 0 and R witness var 1, inherited eta exclusion and the new pointwise equivalence exclude weak and strong all-motives elimination. This is no new countermodel or soundness proof. The inherited two-sided R-to-Eta/source-negation nonderivability remains distinct from the external schemas.

Kernel-proved actual-E-only context, motive, branch and input exclusions substantiate scope expansion. The motive and branch exclusions occur in original well-formed contexts/telescopes. Canonical pair/constant motive examples do not prove necessity for those particular easy instances; all-motives necessity follows from the general converse.

## Evidence and reproduction

The frozen author sources, report and validation evidence and separately attributed independent review are retained verbatim. Fresh extraction compiles three author modules and IndependentPositive at Lean 4.19.0 --trust=0 and compares two intended negative diagnostics exactly after path remapping. This preservation is custody and bounded replay, not an additional independent mathematical review or human peer review.

REUSE_CONTRACT.json records exact retained toolchain, object inventories, source/provenance hashes and import order. The archive omits compiled objects and earlier ZIPs. Retained dependencies must exist under the recorded workspace-relative paths; this is portable source/evidence with a reusable dependency contract, not a standalone compiler distribution or a new baseline verification. Original scripts are historical recipes; the wrapper writes only to a new output directory.

Run from the extracted packet:

    python verify_replay.py --expected-manifest-sha256 <external-receipt-pin> --workspace <retained-workspace> --output <new-output-directory> --replay

The external receipt records actual replay counts, five custody guard tests, original-file preservation and fifteen preceding archive checks. No upload, protected changes, integration or programme closure is performed.
