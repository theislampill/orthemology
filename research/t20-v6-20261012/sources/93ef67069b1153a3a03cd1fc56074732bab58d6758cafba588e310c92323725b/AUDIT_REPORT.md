# Fast-path handoff audit — v2

8 October 2026. Scope: the supplied prior Codex transcript, delivered launch package, original frozen integration evidence and read-only live repository metadata. This is not a new mathematical review, full repository replay or billing audit.

## Verdict

**Keep the patch-first strategy; replace the private launcher and execution instructions.** All ten original inputs and the existing exact-base Git patch are retained without byte changes. The selected 7 October integration is already constructed. Codex does not need to reconstruct T07–T16, develop a new replay adapter, re-read the source corpus or reprove the research merely to publish a draft.

The task is mechanically bounded, but it is not a guaranteed-duration or guaranteed-green-CI operation. Live base drift, credentials, a concrete integrity defect or required CI failure can still block it. The supported claim is that the ready patch removes the substantial reconstruction work that dominated the earlier task.

## What the old transcript actually shows

The old task was broader than moving finished files to GitHub. Its initial work order demanded a new continuation registry, validator, source projection and replay interface (`Pasted text.txt:51–59`). The later T07–T15 task again demanded curated projections, source/review/claim mappings, isolated formal/reference replay interfaces, tests and supersession (`Pasted text.txt:1988–2054`). These are real implementation obligations, not a simple patch application.

The record then shows adapter development and checking: the replay core alone reached 33 tests (`Pasted text.txt:2728`), and a later Fifteenth run completed Lean compilation but stopped because the adapter could not match declaration readbacks (`Pasted text.txt:4271`). These details support the diagnosis that translation/replay infrastructure, not just importing existing files, consumed work. They do not establish that every test was unnecessary or that a particular skill caused the expense.

An earlier workflow also repeatedly copied the repository across Windows/WSL filesystems; the executor explicitly identified that bottleneck and prepared a Linux validation checkout (`Pasted text.txt:997–1016`). The new instructions therefore prefer native-Linux worktrees for recursive validation and forbid bespoke cross-platform shims merely for this task.

The owner's later cost directive is unambiguous: reuse valid evidence, do not repeat expensive builds/workflows/scans without a specific need, avoid speculative parallel workers and repeated polling, and stop if a blocker requires a substantial new campaign (`Pasted text.txt:8938–8951`). The final through-T16 handback retains valid evidence by identity and reports all 21 T16 fresh-science fields as NOT_RUN (`Pasted text.txt:10140–10164`). Reusing that finished history is the correct starting point.

No token ledger, complete timing telemetry or subordinate-agent transcripts were supplied. This audit does not calculate a dollar cost, exact wasted-compute percentage or causal attribution to a plugin. Coverage was targeted to the stated failure pattern and final integration boundary, not every line of the transcript.

## Why the current patch is materially different

The frozen parent archive supplies a complete 27,396,058-byte patch, an exact pre/postimage manifest, the original guarded apply helper, prior whole-diff review, final delta review and a successful clean-application receipt. Base: `fd0903d99d657c35e32fddcc8864d2a77930cf40`; candidate tree: `32e607c34ed32e9f90fed13bdde294fbc47ca7c2`. The delta has 990 added and 26 modified files, none deleted.

Its earlier clean-application receipt records an actual full application and checks of all 7,637 tracked worktree blobs, preserving 6,621 unchanged base files. The recorded check window was 7 October 19:02:09.689828–19:03:15.344709 UTC. This is historical evidence of the bounded workflow, not a forecast of Codex latency or a new execution by this audit. See the immutable `integration/final-patch/CLEAN_APPLY_VERIFICATION.json` inside the parent ZIP.

Live read-only GitHub inspection found PR30 still open/unmerged at the expected head, and main still at `19de267cd41d2a5eeeb3eaf0b91562f706e2a916`. The new execution must recheck those facts before applying. No remote changes were made by this review.

## Corrections in v2

**Launch guards.** Both earlier helper scripts used Python `assert` for security/integrity checks. Real subprocess probes demonstrated that the input verifier accepted a wrong hash under `-O`, and the unpacker wrote a `../` entry outside its destination under `-O`. Normal mode rejected the same fixtures. Explicit checks now retain these guards in both modes. Extraction additionally preflights all names and types before writing, refuses existing destinations, case/file-parent collisions and privileged modes, and preserves safe file execute bits. The original scientific apply helper is unchanged.

**Execution ambiguity.** The previous prompt delegated selection of “affected” tests and an optional in-repository checkpoint note to Codex. The latter could trigger new manifest/current-state/review work and change the already reviewed candidate tree. V2 supplies a fixed bounded checklist and keeps the active-T20/cutoff notice in the PR body. It forbids optional repository changes, whole-history campaigns and repeated live-CI polling. A pending-CI draft handback is explicitly distinguished from final acceptance.

**Coverage.** A private archive containing later checkpoints is not the same as publishing those checkpoints. V2 states that distinction at the start. The intermediate checkpoint explicitly excludes noise-aware calibration/review and warrant-standard-review from its own snapshot; a separate warrant appraisal is included. Later noisy, countable-input and grouped-observation work is not silently credited to this older Git patch.

## Verification performed here

All ten preserved input hashes and sizes passed, including ZIP CRC checks. The frozen package extracted all 842 entries and preserved its recorded executable permission. Its native archive/integration verifier passed all 75 specified receipt-field bindings. The repaired launch helpers passed 15 regression-test methods under normal and optimised execution; the pre-fix run produced 21 failing subcases. The unchanged original apply helper's seven author guard tests also passed in both modes; those tests use inert Git responses and are not a real full-patch application.

A direct Git clone failed before checkout because this container could not resolve GitHub. Consequently **a new full-repository patch application, new repository tests and new remote CI were not performed here**. No synthetic Git history was substituted. The original clean-application evidence is inherited and byte-bound. Codex must perform the new live application and existing required CI. The exact Docker/Poppler PDF rebuild remains a real gate, not something package hashing can discharge.

## Delivery and remaining boundary

The revised launch contains everything selected for this frozen integration apart from the existing Git base and normal external Git/CI prerequisites. It retains all later supplied inputs privately. It is **not** a final consolidation of all ongoing T20 research. That later source-bound integration remains separate, and T20 stays active without owner acceptance or invented timing compliance.

Use the v2 archive and v2 prompt together. Do not paste the old optional-work prompt. No merge, auto-merge, main write, PR30 change, release, licence decision or scientific completion is authorised.

Technical reference checked during this audit: Git's official `git-apply` documentation confirms that `--check --index` checks the index/worktree pair and `git apply` does not itself commit. Python guard behaviour was directly reproduced in the bundled test evidence.
