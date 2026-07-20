# R3 Review E — software/schema/PDF engineering (adversarial)

**Posture: assume the tests prove less than claimed and the builds lie.**

| Attack | Result | Disposition |
|---|---|---|
| Positive-only tests | 11 negative fixtures across both rejection layers + 208 deterministic mutants (drop-required / bad-enum / extra-field over every example part), **0 survivors**; omission-attack fixture for ReqPath | **FIXED** (was the R2 defect: 7/7 malformed classes accepted) |
| Schema permissiveness | `additionalProperties:false` everywhere except six declared typed map extension points; constitutive requirements (nonempty binding, governed component, scope; episode auditability set); schema-encoded factivity; minLength/uniqueItems | **FIXED** |
| Cross-record inconsistency | Dedicated semantic validator: analysis/anchor equality, id uniqueness, binder role, pathway recomputation, NA-reasons, zero-burden and route derivation matching, per-token resolution + V3c aggregate, handoff versioning, Definition-13 closure floor | **FIXED** |
| Nondeterminism | Double build in-process + CI clean-rebuild byte-equality on Linux against Windows-built artifacts — **cross-OS byte identity empirically green** (run at 9ff3a90); `SOURCE_DATE_EPOCH` from the source commit; `ignore_system_fonts` pins the font universe to Typst's embedded OFL set | **FIXED** (R2: all four hashes changed between builds seconds apart) |
| Silent failure | Strict converter raises on any unhandled Markdown construct; build fails on QA violations; the fpdf2 silent line-skip is gone | **FIXED** |
| Raw Markdown in output | Text-layer QA bans pipe rows, blockquote markers, link syntax, hr rules; visual pass over every page of all four PDFs | **FIXED** |
| Stale sidecar | `--check` fails on source-hash drift AND on byte-inequality of a rebuild | **FIXED** |
| Source/artifact revision ambiguity | Sidecars record the source revision + epoch and state the two-stage rule (artifact revision = the committing commit, discoverable via `git log -- artifacts/`) | **FIXED, with the note below** |
| Dependency drift | CI pins `typst==0.15.0`, `markdown-it-py==4.0.0`, `pypdf>=6,<7` | **FIXED this review** |
| Registry/prose drift | Generated enum + alias table with `--check` drift gate | **FIXED** |
| Manifest process | Manifest covers tracked files only — regeneration must follow `git add` (one CI failure was caused by ordering; process corrected) | **FIXED; process note recorded** |

**Residual findings (kept honestly):**
1. The sidecar's `artifact_commit` field is a descriptive rule, not a hash — a commit cannot contain its own hash. The two-stage model is documented; the final artifact commit is recorded in the sign-off report. **Risk-accepted (inherent).**
2. Property-based/metamorphic *generation* beyond the enumerated mutation operators was deliberately not added (CI determinism); the enumerated corpus is a floor. **Scoping decision, recorded.**
3. Internal `.md` links render as emphasized text (no in-PDF targets) — documented rendering rule in the visual QA report. **Risk-accepted (disclosed).**

**Verdict:** the engineering layer now enforces what R2 merely asserted; every prior "validator passed" claim has a negative-test counterpart that would have caught its failure.
