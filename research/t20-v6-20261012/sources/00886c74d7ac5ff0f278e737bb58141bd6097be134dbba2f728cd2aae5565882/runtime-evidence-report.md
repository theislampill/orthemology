# Runtime architecture and evidence review

## Bottom line

The repository contains a substantial diagnostic-control architecture and real executable consistency checks. It is more than a collection of prompts or decorative mathematical labels. Its strongest implemented property is **making selected classes of inconsistent routing, fabricated closure, detached owner records, and stale generated artifacts detectable**.

That does not establish that the initial diagnosis is true, that a chosen theological operation is warranted, that a model faithfully loaded the exact skill, or that a valid-looking answer changes an interlocutor's beliefs. The repository often states these limitations correctly. Several current surfaces still blur the boundaries, and one concrete schema/fixture inconsistency survives at the inspected commit.

The most important distinction is between three different operational products:

1. The canonical installed skill is a generated Markdown/reference package whose rules the model follows.
2. The older diagnose/route/validate/reconstruct scripts are an optional, bounded development harness.
3. The newer staged runner is an executable model-plus-normalization-plus-assembly-plus-verification workflow. Success here is composite workflow evidence, not a scriptless model-compliance result.

## Inspection boundary

- Repository: theislampill/daee-epistemics.
- Source commit: c86b3c6673147b8802fe222373a165a37d4d24a8.
- Tree: 6c359699739826aa839571abfa15256a6395ed26.
- Source reads: GitHub connector, pinned to that commit. Fifty fetched source files were saved and their local Git blob hashes checked against the connector/tree SHA. Two mixed-CRLF Python files were re-fetched in base64 to preserve exact bytes.
- Release metadata was independently read on 2026-10-07, approximately 22:14–22:15 UTC.
- No repository script, test suite, build, model smoke, package installation, or mutation was executed. No new CI PASS is claimed.
- This is a deep selective source review, not a full line-by-line audit of every implementation. The staged runner alone has 15,866 lines; its critical prompt, normalization, invocation, handoff and release-validation paths were inspected.
- Existing tests and historical PASS claims remain existing evidence. This review does not retrospectively turn them into a newly observed runtime event, and does not close T20 or grant owner research approval.

## 1. What actually runs

### A. Source-to-package compilation

atomics/skill is the canonical editable module corpus. The builder checks module IDs, catalogue/path agreement, source uniqueness and required inputs, then emits bundled Markdown with original module IDs, canonical paths and source hashes. The compiled map resolves an original module identity to its bundle. Bundle co-location is explicitly not activation.

This is a sound separation: physical packaging can reduce file calls without turning every adjacent module into an active authority. The compiler also adds a large authored control-plane instruction block ahead of the atomics SKILL body. Therefore, understanding current runtime behavior requires reading the compiler's generated_skill_text as well as atomics/skill/SKILL.md; the generated entry point is not a simple concatenation of atomics alone.

Sources: [tools/build_compiled_runtime.py L37-L105](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/build_compiled_runtime.py#L37-L105); [tools/build_compiled_runtime.py L108-L160](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/build_compiled_runtime.py#L108-L160); [tools/build_compiled_runtime.py L1842-L1970](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/build_compiled_runtime.py#L1842-L1970); [tools/compiled_runtime_lib.py L512-L522](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/compiled_runtime_lib.py#L512-L522).

The canonical archive excludes data, scripts and tests. Those remain optional repository/development material. Consequently, the presence of Python validators in the repository does not make them compulsory machine gates in every installed skill invocation. The packaged skill's runtime control is primarily model-followed governance.

Sources: [docs/compiled-runtime-tools.md L31-L50](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/compiled-runtime-tools.md#L31-L50); [docs/package-smoke-readiness.md L10-L56](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/package-smoke-readiness.md#L10-L56).

The apparent tracked-generated-file exception is deliberate, not an accidental source/runtime defect: the tree contains exactly skill/SKILL.md under skill/. The policy retains that generated entry point for exact-file smoke custody, while all other generated skill content is ignored. CI rebuilds then checks git diff --exit-code -- skill/SKILL.md. This closes the previous hole where rebuilding silently erased a stale committed entry point before freshness checking.

Sources: [docs/audits/v0.4.4.x-tracked-generated-skill-md-policy.md L7-L46](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/audits/v0.4.4.x-tracked-generated-skill-md-policy.md#L7-L46); [.github/workflows/ci.yml L20-L34](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/.github/workflows/ci.yml#L20-L34).

### B. The conceptual diagnostic machine

The intended pipeline is diagnostic reduction → typed IR → reconstruction → gates and precedence → one current burden → owner-specific operations → landing → mid-reread pressure → STOP/HOLD/RECURSE/PARTIAL.

There are useful ownership boundaries:
- Diagnostic IR owns the state carrier and dispatch gate.
- Recursive-state-transitions owns abstract state and carry/reset rules.
- Routing precedence owns ordering and suppression.
- Output release owns what and how much may be released.
- Render contracts own public presentation.
- P7 owns concrete stop instances.
- Operative contracts describe module capabilities; they do not independently authorize activation.

Sources: [atomics/skill/references/diagnostics/diagnostic-ir.md L266-L374](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/diagnostic-ir.md#L266-L374); [atomics/skill/references/diagnostics/recursive-state-transitions.md L42-L68](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/recursive-state-transitions.md#L42-L68); [atomics/skill/references/diagnostics/operative-contracts.md L15-L35](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/operative-contracts.md#L15-L35); [atomics/skill/references/diagnostics/framework-pipeline.md L42-L98](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/framework-pipeline.md#L42-L98).

The state model is stronger than a prewritten argument itinerary. HOLD means material remains but is blocked; PARTIAL preserves an unfinished burden when limits intervene; RECURSE requires a newly eligible same-input burden; STOP requires rereading the live and held sets. Matched modules, rendered content and next move reset after a pass, while diagnostic context and unresolved held material carry forward. These are concrete design protections against a model answering every detected topic or treating an initial plan as unconditional permission.

Source: [atomics/skill/references/diagnostics/recursive-state-transitions.md L386-L423](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/recursive-state-transitions.md#L386-L423); [atomics/skill/references/diagnostics/recursive-state-transitions.md L584-L642](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/recursive-state-transitions.md#L584-L642); [atomics/skill/references/diagnostics/recursive-state-transitions.md L1308-L1357](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/recursive-state-transitions.md#L1308-L1357).

These are normative semantics. The source itself says Level 1/2 refresh is performed by the model. The installed package does not by itself guarantee that the model really performed each transition.

### C. The older optional executable harness

diagnose.py extracts regex matches and attaches input spans. Its interpretive classes also use bounded heuristics with fixed confidence values; “llm_assisted_span_heuristic” is a label, not an LLM call. For example, grief keywords promote a grief register, while moral/authority terms promote an imported-criterion feature. That makes the extraction trace inspectable, but does not calibrate its confidence or establish semantic diagnosis across negation, quotation, paraphrase, context or languages.

route.py is genuinely deterministic given the feature set and rule tables: it evaluates rule requirements, sorts priority/precedence, records blocked/deferred owners, and builds a conditional continuation queue with state envelopes. This is useful reproducibility of a mapping. It is not truthfulness of the feature diagnosis.

Sources: [atomics/skill/scripts/diagnose.py L1-L8](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/diagnose.py#L1-L8); [atomics/skill/scripts/diagnose.py L167-L332](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/diagnose.py#L167-L332); [atomics/skill/scripts/route.py L159-L323](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/route.py#L159-L323).

validate.py checks hashes, licensed vocabulary, owner membership, internal span agreement and state-envelope shape. Its span check compares route spans with the supplied feature payload; it does not receive the original input text for independent substring verification. reconstruct.py explicitly discards input_text and loads the trigger matrix to recover a route from features. This is route/feature consistency, not the independent input-plus-IR reconstruction described by the canonical prose, whose reconstructor should not reload routing/catalogue owners.

That difference is a scope boundary in a historical optional harness, not evidence that the canonical package silently uses this weak reconstruction everywhere.

Sources: [atomics/skill/scripts/validate.py L131-L175](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/validate.py#L131-L175); [atomics/skill/scripts/validate.py L437-L580](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/validate.py#L437-L580); [atomics/skill/scripts/reconstruct.py L27-L125](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/reconstruct.py#L27-L125); [atomics/skill/references/diagnostics/diagnostic-ir.md L276-L284](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/diagnostic-ir.md#L276-L284).

check_execution.py adds meaningful local attachment checks: owner floor and Target/Operation/Result must occur within the correct burden window; held owners cannot be executed; closure cannot precede pending continuation. It also uses textual proxies for substantive quality, including required tokens, word/premise markers and operation-verb patterns. Those are useful false-pass guards, not entailment checking, source authentication or a general semantic evaluator. Simulated output deliberately bypasses its quality gate and is documented as simulated route/check evidence only.

Sources: [atomics/skill/scripts/check_execution.py L263-L317](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/check_execution.py#L263-L317); [atomics/skill/scripts/check_execution.py L428-L452](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/check_execution.py#L428-L452); [atomics/skill/scripts/check_execution.py L655-L680](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/check_execution.py#L655-L680); [atomics/skill/scripts/check_execution.py L793-L935](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/scripts/check_execution.py#L793-L935); [docs/compiled-runtime-tools.md L86-L105](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/compiled-runtime-tools.md#L86-L105).

### D. The newer staged workflow

The staged runner separates intake, diagnostic IR, routing, ACT execution records, MRP/terminal state, witness/NAR, public release output and verifier sidecars. It invokes model stages, stores responses, normalizes stage records, validates handoffs and only then proceeds. Its handoff checks bind route targets to diagnosed burden floors, executed targets to routed targets, witness body references to ACT references, and terminal-state burdens to witness coverage.

These are executable relational constraints, not just string-presence checks. The public ACT/MRP guard also rejects round-robin owner-slot coverage, repeated terminal Land gates covered by one final MRP, STOP before later burden work, and sidecar closure that contradicts visible traversal. The historical secularism failure is retained as a negative fixture.

Sources: [tools/run_staged_current_skill_smoke.py L69-L78](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L69-L78); [tools/run_staged_current_skill_smoke.py L5837-L5888](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L5837-L5888); [tools/check_staged_runtime_handshake.py L1768-L1934](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_staged_runtime_handshake.py#L1768-L1934); [tools/check_mrp_route_invariants.py L292-L448](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_mrp_route_invariants.py#L292-L448); [tests/mrp-route-invariants/invalid/secularism-round-robin-act-terminal-mrp-false-pass.md](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tests/mrp-route-invariants/invalid/secularism-round-robin-act-terminal-mrp-false-pass.md).

However, compiled-output mode is a composite producer. It can:
- Replace ACT rows with Stage04 rows.
- Rewrite an Operation line, append a stock state-change sentence and replace a Contribution-to-Land line after a regex body-backed check.
- Replace MRP and witness sections with deterministic stage-derived scaffolds.
- Rewrite an intermediate STOP/no_new_resultant into held-burden activation/RECURSE and add an edge when the Stage04 burden sequence already has a later burden.

These repairs may be intentional and valid for the composite workflow. They mean a compiled-output PASS is not evidence that the raw model independently emitted every checked state transition or sentence. The v0.4.5.0 release correctly states that Smoke C used compiled-output mode.

Sources: [tools/run_staged_current_skill_smoke.py L4813-L4845](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L4813-L4845); [tools/run_staged_current_skill_smoke.py L5025-L5166](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L5025-L5166); [tools/run_staged_current_skill_smoke.py L5523-L5659](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L5523-L5659); [tools/run_staged_current_skill_smoke.py L5694-L5805](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L5694-L5805); [docs/v0.4.5.0-release-notes.md L32-L51](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/v0.4.5.0-release-notes.md#L32-L51).

## 2. Concrete findings and unresolved evidence

### Finding 1: the formal schema and a designated valid fixture disagree

The JSON schema forbids routing_gate = open when reason_category is 3 or 4. The designated positive criterion-import fixture contains reason_category = 3 and routing_gate = open. The checker's own base sample has the same pairing.

The custom schema_errors function checks required fields, basic type/enum rules and selected hand-coded conditionals, but does not evaluate JSON Schema allOf. Its validation chain then calls integrity_errors, which adds catalogue/source-basis and post-render consistency checks, not the missing reason-category gate rule. This explains how the designated-valid corpus can diverge from the formal schema.

This is a confirmed source-level inconsistency. A fresh test execution was not performed, so this review does not report a newly observed runtime PASS or failure. The fixture also has alignment_state = tribunal-loosened and a post-render assertion that the imported tribunal has cleared. An intended post-repair opening may therefore be reasonable while reason_category preserves the input classification. The owner must resolve whether the schema needs a phase/resolution guard or the fixture needs a changed current-state category. Blindly changing the gate to HOLD or merely loosening the checker would not settle that semantic question.

Sources: [atomics/skill/references/diagnostics/diagnostic-ir.schema.json L1587-L1605](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/atomics/skill/references/diagnostics/diagnostic-ir.schema.json#L1587-L1605); [tests/ir-fixtures/valid/criterion-import-positive.json L1-L25](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tests/ir-fixtures/valid/criterion-import-positive.json#L1-L25); [tools/check_ir_instance_integrity.py L1602-L1727](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_ir_instance_integrity.py#L1602-L1727); [tools/check_ir_instance_integrity.py L2223-L2325](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_ir_instance_integrity.py#L2223-L2325); [tools/check_ir_instance_integrity.py L2347-L2358](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_ir_instance_integrity.py#L2347-L2358).

### Finding 2: exact-runtime loading is not established by a runtime hash

The inspected staged prompt supplies a runtime SHA, stage instructions, raw input and prior validated state, while telling the model not to read files. The Codex command uses the repository as cwd but has no explicit skill-content or instructions-file argument. The runner hashes skill/SKILL.md rather than reading its contents into these prompt builders.

AGENTS.md requires direct exact-file loading and describes a prompt-embedded fallback. Repository-level AGENTS auto-loading or another host mechanism might provide additional context, and historical invocation logs were not inspected here. Therefore the warranted conclusion is **a source-visible absence of an explicit delivery path in the inspected runner**, not “the model never loaded the skill.”

For a claim about this precise runtime, demonstrate instruction delivery separately from hash custody. The source hash proves which file was named and hashed; it does not prove those bytes reached the model.

Sources: [tools/run_staged_current_skill_smoke.py L6080-L6160](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L6080-L6160); [tools/run_staged_current_skill_smoke.py L6894-L6929](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L6894-L6929); [tools/run_staged_current_skill_smoke.py L15321-L15375](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/run_staged_current_skill_smoke.py#L15321-L15375); [AGENTS.md L144-L151](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/AGENTS.md#L144-L151); [AGENTS.md L198-L219](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/AGENTS.md#L198-L219).

### Finding 3: static routing parity does not exercise the diagnoser

The routing-parity checker explicitly calls itself static. It checks that expected module IDs resolve, bundles exist, governance phrases occur, and fixture-declared minimal pairs differ. Its minimal-pair comparison examines the fixtures' expected modules/governance sets. It does not feed their prompts to a model or diagnoser and compare observed diagnoses.

The grief-versus-moral-protest fixture is a good test design: it holds vocabulary roughly constant and asks for a different register/route. But its prose says the check verifies runtime/checker discrimination more strongly than the implementation warrants. The current implementation verifies that different expected reads are represented and supported in the corpus, not that an inference process actually produces them.

Sources: [tools/check_routing_parity.py L1-L10](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_routing_parity.py#L1-L10); [tools/check_routing_parity.py L534-L674](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_routing_parity.py#L534-L674); [tools/check_routing_parity.py L707-L756](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_routing_parity.py#L707-L756); [tests/routing-fixtures/12-grief-primary-hiddenness-vocabulary-minimal-pair.json L1-L5](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tests/routing-fixtures/12-grief-primary-hiddenness-vocabulary-minimal-pair.json#L1-L5).

### Finding 4: current evidence surfaces have historical residue

The behavioral-evaluation framework still describes a pre-public v0.4.2.0 candidate and its missing public-release proof. The file labelled current-canon package/smoke readiness still discusses a future live runner as unimplemented and says no smoke artifact suite is committed. The current tree contains a staged model runner and a retained sidecar-backed corpus manifest with 24 cases. Some older statements may intend a narrower package-bound replay claim; that scope is not consistently made explicit.

These statements should not be used to deny the newer implementation or to promote older release evidence into current proof. The v0.4.5.0 release documents provide a much clearer, bounded current release account.

Sources: [docs/behavioral-evaluation-framework.md L8-L31](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/behavioral-evaluation-framework.md#L8-L31); [docs/package-smoke-readiness.md L191-L210](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/package-smoke-readiness.md#L191-L210); [docs/package-smoke-readiness.md L306-L313](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/package-smoke-readiness.md#L306-L313); [tests/retained-proof-corpus/v0.4.3.0-schema-light/valid/sidecar-backed/manifest.json](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tests/retained-proof-corpus/v0.4.3.0-schema-light/valid/sidecar-backed/manifest.json).

The TODO explicitly keeps the manual Claude scriptless compact-DSL behavioral rerun open. Its rule is sound: specification and checker hardening do not prove recovery of live model behavior. This remains a declared open obligation unless a later retained artifact/matrix/audit explicitly closes it; this review did not find or verify such closure.

Source: [TODO.md L114-L140](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/TODO.md#L114-L140).

## 3. What the evidence supports

| Evidence layer | Inspected implementation/evidence | Warranted conclusion | Not established |
|---|---|---|---|
| Source/package identity | Builder, module map, source hashes, freshness gate | Generated section identity and drift can be checked; tracked SKILL exception is deliberate | Soundness of every owner, fresh build success in this review |
| Optional feature routing | Regex spans, rule predicates, priorities, hashes | Deterministic mapping for supplied features | Truthful/calibrated diagnosis or arbitrary NL-to-IR parsing |
| Diagnostic IR integrity | Custom schema-adjacent checks, catalogue membership, source-basis coverage, post-render consistency | Many malformed or contradictory records are rejectable | Full schema equivalence; the concrete positive-fixture mismatch disproves that assumption |
| Source basis | Module/claim/ref coverage and ghost-load guard | Claimed use is attached to a named source owner | The file was truly delivered/read, the source says what is claimed, or the claim is true |
| Routing fixtures | Static expected-owner mappings and minimal pairs | Expected distinctions remain represented in source/runtime | Model or parser actually diagnoses those distinctions |
| Public ACT/MRP traversal | Contiguity, local body refs, per-Land MRP, sidecar/visible parity | Real rejection of selected structural false-green classes is implemented | Semantic validity of every operation or completeness of every input burden |
| Staged model workflow | Model stages plus deterministic repairs, assembly and validators | A composite workflow can enforce stronger output consistency | Scriptless model compliance or unmodified raw-output quality |
| Retained corpus | 24 declared cases; sampled actual input/output/certificate; hashes and row-specific bindings | A substantial auditable regression corpus exists | Fresh rerun, latest-package applicability of every historical case, generalization |
| Release metadata | Fresh GitHub release/tag/asset metadata matches docs | Current published release identity and API-reported asset digests align | Independently downloaded/rehashed archive, reproduced Smoke C, current-main release equivalence |
| Philosophical/empirical validity | Explicit limits; no semantic truth oracle in inspected code | The framework can expose its own audit trail | Truth of theology, diagnosis, restored belief, practical usefulness or guaranteed uptake |

The sampled retained a9-science-source output illustrates the distinction well. It has actual local owner work, a visible Land → MRP sequence, explicit bounded closure and no-uptake language; it also explicitly leaves fuller revelation/Islam proofs for another pass. Its checker-owned collapse certificate is evidence about that bounded governed artifact, not a general proof of its philosophical conclusions.

Sources: [tests/retained-proof-corpus/v0.4.3.0-schema-light/valid/sidecar-backed/cases/a9-science-source/output.md L24-L111](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tests/retained-proof-corpus/v0.4.3.0-schema-light/valid/sidecar-backed/cases/a9-science-source/output.md#L24-L111); [tests/retained-proof-corpus/v0.4.3.0-schema-light/valid/sidecar-backed/cases/a9-science-source/collapse-certificate.json](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tests/retained-proof-corpus/v0.4.3.0-schema-light/valid/sidecar-backed/cases/a9-science-source/collapse-certificate.json); [tools/check_retained_proof_corpus.py L1-L7](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/tools/check_retained_proof_corpus.py#L1-L7).

## 4. Release verification

Fresh GitHub API readbacks confirm:

- Latest published, non-prerelease release: v0.4.5.0.
- Release ID: 339448208.
- Annotated tag object: 772f07d0cb8f476e4e9b06f55a97610337d232dd.
- Peeled source commit: 8c14e28fbcf440275f4d143a9b7cadc6148aa5a9.
- Two uploaded assets: the .skill package and provenance JSON.
- API-reported package size: 711841 bytes.
- API-reported package digest: SHA256 67FF081EF34B9CBE3BF03309F03DFAEF1C8D471640CED715D299A90344DFAB6F.
- API-reported provenance digest: SHA256 E0BE60F71D78184206846918AE9329B5CF28378F297338E74A6B181381324239.
- The release keeps its June 15 publication date, while replacement assets and the tag object are dated June 18. This is consistent with the documented replacement.
- The release source commit differs from the reviewed main commit. Release claims are not automatically current-main execution claims.
- Binary download/re-hash and raw Smoke C replay: NOT RUN.

The current release account explicitly limits its claim to bounded structural-integrity repair; it disclaims arbitrary-input correctness, cross-host/paraphrase proof and guaranteed interlocutor uptake. Raw Smoke C outputs and prompts are local custody evidence, not release assets. That is a genuine independent-verification limit, not evidence those runs did not happen.

Sources: [published release](https://github.com/theislampill/daee-epistemics/releases/tag/v0.4.5.0); [release API read surface](https://api.github.com/repos/theislampill/daee-epistemics/releases/latest); [annotated tag object](https://api.github.com/repos/theislampill/daee-epistemics/git/tags/772f07d0cb8f476e4e9b06f55a97610337d232dd); [docs/release-artifacts.md L36-L75](https://github.com/theislampill/daee-epistemics/blob/c86b3c6673147b8802fe222373a165a37d4d24a8/docs/release-artifacts.md#L36-L75).

## 5. Three bounded conclusions

1. **Use the architecture as a research discipline, with typed evidence levels.** It is particularly useful for forcing a bounded target, named source basis, alternatives, local state change, held remainder and explicit closure condition. Preserve the distinction between a contract, a checked representation and an observed external result.
2. **Before crediting a new behavioral claim, bind the actual causal path.** Establish which runtime bytes reached which model; separate raw stage response, deterministic normalization and final compiled artifact; then judge the claimed behavior on the appropriate surface. Prefer a new targeted case/minimal pair for a new claim rather than credit from packaging or a reused green envelope.
3. **Resolve the narrow contradictions before broadening claims.** The schema/positive-fixture disagreement, stale current-canon readiness wording and static minimal-pair overstatement are concrete places where apparent formal rigor outruns exact semantics. Their resolution is an owner decision or authorized future engineering task, not part of this read-only review.

## Reading coverage

Fetched and bound: 50 source files plus the recursive tree and three fresh release/tag API readbacks. The tree contains 1,569 blobs, including 1,157 files under tests; these counts are inventory only, not test execution or full reading credit.

Deeply inspected critical paths:
- diagnose.py, route.py, reconstruct.py, validate.py, check_execution.py.
- build_compiled_runtime.py generation/validation/package selection; compiled_runtime_lib.py normalization, bundling and cleanup guards; freshness checker and CI workflow.
- check_ir_instance_integrity.py required/type/conditional checks, source-basis/catalogue constraints and full validate_instance call chain.
- check_routing_parity.py fixture and minimal-pair logic.
- check_staged_runtime_handshake.py stage ordering, handoffs, burden coverage, ACT ownership and artifact bindings.
- check_mrp_route_invariants.py public traversal, per-Land, terminal MRP and sidecar-conflict paths.
- run_staged_current_skill_smoke.py stage prompts, model invocation, normalization, ACT/body rewrites, continuation rewriting, state handoffs, compiled assembly and release-validator invocation.
- Representative positive/negative IR and routing fixtures; historical secularism false-pass output structure; one retained input/output/certificate and the retained corpus manifest.

Selected substantive sections inspected:
- atomics SKILL control plane/execution spine/load and gate rules.
- Diagnostic IR gate/compiler/schema sections and schema conditionals.
- Recursive state ownership, state model, depth guard, carry/reset table and failure tests.
- Operative contracts' static/runtime boundary.
- Output-release and framework-pipeline owner/order/closure guidance.
- Current release artifacts/notes, readiness, behavioral framework, tracked-generated policy, hardcoding audit, staged harness history and active TODO.
- AGENTS exact-file loading and proof-corpus evidence rules, treated as objects of analysis.

Additional fetched files were searched or used to trace references rather than claimed as exhaustively read. No complete owner-corpus review, all-checker audit, browser Grapher QA, cross-host evaluation, empirical calibration study or full CI review was performed.

