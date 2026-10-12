# HR-20261009-FINAL — independent delta review r2

**Verdict: accept the nine scoped corrections/evidence resolutions below; retain four insufficient prayer-proof bindings. No new change request within this delta.**

This is an addendum to, not a rewrite of, the original 22-node review. The nine original scoped PASS decisions are carried forward unchanged. Five documentation findings are now resolved; the three weather generated-consumer bindings and the INFO actual-consumer binding now meet their reviewed scopes. The four prayer documentation native-proof gaps remain insufficient.

| Disposition | Original record, preserved | Cumulative scoped position after this delta |
|---|---:|---:|
| PASS | 9 | **18** |
| REQUEST CHANGES | 5 | **0** |
| INSUFFICIENT EVIDENCE | 8 | **4** |
| Total original nodes | 22 | **22** |

These are **review dispositions**, not nine additional DAG completions, whole-issue closures, a release decision or approval of PR43. Root had already admitted the resolved work at the supplied cuts. No live GitHub status is asserted.

## 1. Reviewed identities and method

Input ZIP: `HR_20261009_FINAL_Delta_r2.zip`, 9,932,875 bytes; SHA-256:
`ea4c094e8372e308302720f8dfd548d20e396fd66eef6ec05591bc0b6cf446d4`.

The ZIP CRC/member check and all 495 listed payload hashes passed; there are 496 ZIP members including the outer manifest. The 350-file base and separately named 139-file appendix preserve their own manifests and chronological cuts. Exact references, byte counts and full SHA-256 values for every principal item below are in **SOURCE_REFERENCES.json**. `B/` abbreviates `base-20261009T144615Z/`; `A/` abbreviates `info-appendix-20261009T153108Z/` inside that ZIP.

| Identity | SHA-256 |
|---|---|
| Base manifest | `f934803be1390da0b6cb98411d53ffba361083d16a40b3598f8ec1b44753302f` |
| Appendix manifest | `898b9c5c68824aa0f35bbe60705acfc6bd7e64e3d0b8b95b115d117f97c05812` |
| Joined README | `b14791ffca9552d841066d6c8fff02c353f052b8952ef15d187fd340ebe317d1` |
| Joined DESIGN | `cfe7815f839b6f62d57b066f4562453cb370aa1ce783b66629460107cd283c0f` |
| Authored native entry | `ec59b3ff64e06713d652af5b30f04a18fcde404b92b4595bc1cee96818a6ec65` |
| Generated consumer entry | `14e1d92101dad56f1352a2b4a85a460067361ecdfca62093f9f9d1286b991fad` |
| Configuration | `91a37863cd85e232e9a63bba9db533b82699e63140086ba4b78fcf9c0581ec81` |
| Retained joined runtime inventory | `e718fe9e58f37535de4dc496a2da3bf2b05808153287e1fe328398ea59c0df53` |

The joined candidate is explicitly dirty relative to base `f0647b44e10c9ce4f80895b52861893c347512fd`. It is **not interchangeable** with delivered main, the separate PR43 runtime, or an arbitrary moving worktree.

Fresh work in this review comprised source/prose inspection, hash and inventory checks, in-memory patch reversal/reapplication, recorded assertion/counterexample analysis, inspection of raw actual-browser observations, and viewing twelve original card/settings images. The supplied custody verifier was read before its read-only execution. My separate verifier performed 1,000 byte/binding/observation checks with zero final failures. **Those are not 1,000 product tests.**

No retained producer, oracle, product test, builder, native browser or installer was executed. No input source was modified, no network or repository operation was performed and no public effect was authorised. Earlier full-campaign results remain historical evidence. Hash agreement establishes the supplied records' consistency, not an external attestation that every historical execution occurred exactly as recorded.

## 2. Five documentation findings — all resolved in scope

### HR-D01 / R000B-DOCS / issue #11 — PASS

**Evidence:** `B/joined-documents/root-snapshot/DESIGN.md:331–365`, README:305–310; `B/five-doc-findings/weather-review/{CLAUSE_BINDINGS,SOURCE_BINDINGS,SMALL_HUNK_BINDINGS}.json`; root admission `B/admissions/joined-admission-wave-02/nodes/R000B-DOCS.json` (`ccc095e2…`; full value in reference `HR-D01-ROOT`).

The clauses now identify raw model wall time/request zone/derived valid epoch, positive preceding interval and receipt, alongside separate radar frame/index/receipt clocks. They state inclusive 15-minute model and 20-minute radar source/receipt bounds, zero future tolerance and finite converted radar epochs before Image admission. The six-hour cache read rule is correctly strict: `0 <= now - receipt < 6 hours`; exactly six hours is a miss, not deletion or renewed current authority. Header/effect withdrawal, separate prayer cache and client wall-clock limitations are explicit. These agree with the bound source regions. **No further change to this reviewed prose finding is required.**

### HR-D02 / R000C-DOCS / issue #12 — PASS

**Evidence:** joined README:298–310 and DESIGN:367–386; the same clause/source maps; admission `B/admissions/joined-admission-wave-02/nodes/R000C-DOCS.json` (`223dc41d…`).

Blank unavailable temperature is distinguished from a genuine admitted `0°`, finite negative values and captured Celsius/Fahrenheit units. Conflicting supplied unit metadata and absent optional metadata are differentiated. A valid otherwise eligible condition may survive missing optional measurements. Null/reason values, the lack of wet-effect authority from missing/invalid amounts and the impossibility of retrospectively distinguishing old coerced zeros are stated. No validator, migration or runtime rewrite is implied. **The original omission is resolved.**

### HR-D03 / R000D-DOCS / issue #13 — PASS

**Evidence:** joined README:343–363; source/clock maps; admission `B/admissions/joined-admission-wave-02/nodes/R000D-DOCS.json` (`83ec55f0…`).

The documentation now explains a 10-second fetch-plus-body attempt and a separate 10-second Image attempt after manifest admission, giving only a nominal combined 20-second application budget under runnable JavaScript. It distinguishes the 60-second weather/10-minute radar eligibility, accepted-current-plus-track shortcut and approximately 30-second visible-loop opportunities from actual retry/recovery. Absolute deadline rejection of late settlement, suspended execution, non-monotonic wall-clock fallback and best-effort cancellation are qualified. **No promise of immediate retry or a hard suspended-JavaScript wall deadline remains in this clause.**

### HR-I01 / R0013-DOCS / issue #19 — PASS

**Evidence:** joined README:71–79 and retained-bundle lifecycle:148–166; `B/five-doc-findings/installer/HR-I01_INTERPRETATION.md`; pinned `originals/install.sh` (`9c3fd523…`); admission `B/admissions/joined-admission-wave-01/nodes/R0013-DOCS.json` (`198bcdbc…`).

No controlling terminal/initial target-selection EOF is correctly distinguished from EOF at later prompts, after staging or earlier requested actions may already have occurred. Successful empty input is not EOF. The prose preserves retained bundles and does not imply rollback of earlier clipboard/browser effects. The source's ordering supports this distinction. The interpretation note must remain linked to the original broad wording; **this scoped prose approval does not waive native signal, cleanup, platform or installer qualification requirements**.

### HR-S01 / R001B-DOCS / issue #27 — PASS

**Evidence:** joined README Credits:426–434 plus privacy/request sections; joined `tests/rlgwo-docs-contract.cjs`; `B/five-doc-findings/privacy/` guard, patch, logs and controls; admission `B/admissions/joined-admission-wave-01/nodes/R001B-DOCS.json` (`4cf0d130…`).

The contradictory blanket storage/no-tracking wording is absent from the joined README. The new R001B guard checks the entire README, not just the detailed privacy subsection. Retained raw logs show the old selection's false green, the new guard rejecting old prose, corrected prose passing, and outside-section/provider-certainty counterexamples rejected. The corrected scoped record is **5 PASS + 8 validated REUSED**, not thirteen freshly executed source tests.

Removing only the added guard recovers the exact stronger previous runner (`0163ebdb…`); the joined runner is `ef41fe13…`. The repair therefore does not regress the stronger reuse-validation fixture accepted in the prior review. **HR-S01 is resolved.**

### Composition limit that applies to all five

The seven-file joined patch reverses to its declared preimages and reapplies to exact postimages. Thirty declared documentation clauses and twenty-five bound source regions were checked. The broad composed documentation record still reports **55 PASS and 13 FAIL in 68 cases; all thirteen failures are assigned OTHER**. They remain separate unresolved outcomes, not erased, excused automatically or converted to PASS by these scoped approvals. There is **no whole-README or complete documentation-suite PASS**.

## 3. Three weather generated-consumer bindings — satisfied, source/VM scope only

| Node | Retained healthy result | Detected semantic mutations | Principal evidence |
|---|---:|---:|---|
| R000B-EVIDENCE / #11 | 30 PASS | 5 | `B/weather-generated/R000B/receipt.json` and raw GREEN/RED logs |
| R000C-EVIDENCE / #12 | 119 PASS, 4 TODO | 4 | `B/weather-generated/R000C/receipt.json` and raw GREEN/RED logs |
| R000D-EVIDENCE / #13 | 24 PASS | 3 | `B/weather-generated/R000D/receipt.json` and raw GREEN/RED logs |
| **Total** | **173 PASS, 4 TODO** | **12** | Generated entry `14e1d921…`, config `91a37863…` |

**Disposition for each: PASS — the formerly missing generated-source/VM binding is now supplied.** The earlier authored source approval is retained rather than reopened.

I verified the source kind, exact generated entry/configuration, test/log identities and raw TAP counts. Each mutation has its declared unique anchor; reconstructing it in memory produces the recorded mutant hash. Its retained failure reaches the intended assertion, not an unrelated syntax or missing-source failure; paired healthy controls remain green. The producer source explicitly selects the generated consumer instead of silently overriding it with the authored file.

The generated weather acquisition function includes an existing, exactly identified CP9 accepted-elevation hook. I accounted for that guarded hook rather than incorrectly asserting whole-function byte equality with authored source. The remaining twenty-four regions match directly. The two retained build inventories agree and recompute the declared runtime digest; available index/configuration bytes match them.

This closes the **reviewed binding gap**, not `R000B/C/D-NATIVE`, performance, visual, public-delivery or parent-issue requirements. The full runtime/scientific assets are intentionally absent, so this review does not freshly regenerate or qualify that whole product. The four TODOs remain TODOs and the 173 results are **retained executions verified here**, not tests rerun by this reviewer.

## 4. R0024-INFO / issue #36 — PASS in its retained actual-consumer scope

### The original failure is preserved, and the oracle correction is justified

The original positive actual-browser report, `A/native-evidence/positive/results.json`, remains **FAIL** with SHA-256:
`01ee6181a93a0b7b41080ad2151cb2790360fb1b6b405de44454b32c62c9243d`.

Its hourly case failed because the old oracle required `state.raw is None`. The bound source intentionally can retain an invalid-time raw/cache model record while refusing it as current. The recorded actual consumer shows precisely that separation: raw `currentTime` is invalid and its valid epoch is null, current eligibility is false, selected current is unknown, selected record/model codes are null, the header is an em dash, temperature is blank and all current rain/snow/lightning permissions and visible precipitation are off. A separately admitted hourly numerical forecast remains, without a qualified arrival or probability.

The corrected oracle does **not** simply delete the failing condition. It tests selected current/header/source fields and both decision/QA permissions explicitly, limits retained records to invalid-time current records, requires effects off and verifies the exact separate hourly interval/amount. This follows the actual source/selection contract rather than inventing a raw-record deletion requirement.

| Oracle evidence | Exact SHA-256 |
|---|---|
| `A/oracle-repair/before/tools/qa/info_contract.py` | `ad83baad53cce9806e32b498157b987d57d84ab43654d4738f91758da1e57bff` |
| `A/oracle-repair/proposed/tools/qa/info_contract.py` | `614d5de924f9d1ad6b12affa1e29e24263e87d10ad66c4804d65f909a2444d5d` |
| `A/oracle-repair/ORACLE.patch` | `2845e5f4c06aac8e46f0ce171d08660d08f2d7aa0a7cf2b9c91055f53c283416` |

The one guarded replacement reverses/reapplies exactly, leaving other cases' logic unchanged. Stored offline results retain the old single RED, show all thirty-six corrected checks true, reject twenty-eight mutated false-green candidates and retain three separate header counterexamples. I independently compared the recorded raw/current/header/effect/forecast invariants; I did not execute the supplied oracle or mutation producers.

**Accept this as an offline correction and evaluation of retained native observations—not a newly executed native PASS and not authority to overwrite the original FAIL.**

### Actual consumer, accessibility and settings coverage is bound

The complete retained actual-evidence set has thirty-eight files. Its seven positive cases cover qualified SIM approach, no trajectory, unqualified movement, current wet plus later approach, production current model weather, hourly forecast with unavailable current and local settings. A retained negative naming-control case catches the three intended concise-name/description failures. Individual per-case receipts agree with their aggregate records and original base copies.

Recorded raw CDP accessibility nodes match the selected backend node and the extracted name/description/role. DOM title and accessibility description convey the same admitted snapshot, retain existing described-by content without duplication, distinguish SIM from production estimates, and do not turn nearby/forecast information into present observed precipitation. The qualified absolute zone interval is an accepted representation within the retained scope; this is not a promise of a live arrival provider or a newly required relative countdown.

The actual local-settings workflow records click, Enter and Space activation; opening/closing focus; successful saving; rejected storage writes; and failed Reset preserving saved data and a meaningful warning/action name. I also viewed twelve original full-card/settings images: unknown-current blank temperature/no rain, appropriate wet-state presentation and the visible save/Reset warning outcomes agree with their records.

These were recorded in **Windows Chromium 148.0.7778.96 with controlled time/providers and suppressed fonts**. The hover target/title were inspected; a native tooltip bubble is not claimed as captured. The supplied prior independent review's image checks are retained separately from my twelve-image inspection. This is not whole-sky optical acceptance, real local weather verification, a fresh Firefox campaign, resource qualification or actual extension-parent coverage.

### Root admission and QA adoption are separate, correctly bound events

`A/admission/receipt.json` (`863f8311…`) records scoped INFO completion at **15:21:52 UTC**. `A/admission/QA_ADOPTION.json` (`5c61bbe2…`) separately binds the adopted QA oracle to `614d5de9…`; its preimage and patch match. The earlier sealed harness remains historical. The independent retained-consumer/image review (`A/independent-review/REPORT.json`, `bf2a1afd…`) supports the bounded exit without claiming fresh browser execution.

Thus the previously missing INFO binding is satisfied. Root has **already** accounted for that completion; this review contributes no additional node credit.

## 5. Four prayer documentation proof gaps — still INSUFFICIENT EVIDENCE

All four retain the accepted source-accurate proposal and available coalescence/regional-equivalence evidence. Full node approval still requires the following actual native bindings:

| Node | Remaining gap |
|---|---|
| R0002-DOC / #2 | Ingress/recovery, selected-cache corruption, malformed optional AH and specified suffix/equal-polar positives on the actual consumer. |
| R0004-DOC / #4 | Omitted-zone Tokyo current-day acquisition, selected legacy cache, finite correction and held day/generation ownership settlement. |
| R0006-DOC / #6 | Full-body deadline/backoff, operation-start 60-second fence, hidden/resume recovery, healthy third attempt and matching prefetch/promotion. |
| R0007-DOC / #7 | Spring/fall countdown/labels, missing/wrong/gap/fold days, same-epoch dirty recovery, actual formatter thresholds and selected-calendar boundaries. |

**Evidence:** `A/FOUR_REMAINING_PRAYER_PROOF_GAPS.json` and `B/eight-proof-bindings/prayer/{REPORT.md,PER_CRITERION_MAP.json,CLAUSE_NATIVE_MAP.json,SOURCE_EQUIVALENCE.json,NATIVE_RECEIPTS.json,MISSING_CASE_RECIPE.json}`.

The exact successor patch `618888ca50b8ee76e03cced1e2e27dd107cb869349f94ff3ed67fd9cfbdc0e7a` and its source equivalence are not native outcomes. Four healthy date/geometry examples provide limited context, not the hostile/recovery/DST proof above. Nine retained Chromium failures remain failures, and the referenced batch has no inferred Firefox execution.

The sixty-eight-case index is a recipe map, not a run-all request. Six explicitly absent recipes concern matching tomorrow before/after Maghrib, invalid optional AH and 58.4/59.6/3599.6-second remaining intervals. Prepared transformations and a driver that correctly refuses incompatible source do not satisfy their native exits. Use existing sufficient receipts where possible; otherwise admit the exact target and run only missing relevant cases under the current DAG. Preserve final coalesced hunk/root binding where required. Do not rewrite good prose, bypass source guards or repeat unrelated scientific campaigns.

## 6. Chronology and status accounting

The **14:46 base** is immutable history, even where its README described INFO as still pending. The later appendix supplies the relevant change rather than retrospectively rewriting that cut.

The **15:21:52 INFO admission** recorded 31 COMPLETE and two newly READY successors. The separate **15:31:08.084082 UTC checkpoint** instead records:

| COMPLETE | AWAITING_REVIEW | EXECUTING | READY | BLOCKED | NOT_STARTED |
|---:|---:|---:|---:|---:|---:|
| 31 | 37 | 12 | 0 | 31 | 102 |

The counts reconcile to 213. INFO is COMPLETE; RESOURCE is BLOCKED on its qualified comparison input; NATIVE is EXECUTING bounded preparation, not native qualification. No additional COMPLETE was added after the INFO admission. `GATED_NOT_COMPARABLE` may satisfy its own acquisition node but cannot qualify downstream resource measurements. These are supplied historical checkpoint states, not a fresh reading of the active thread.

The outer handoff receipt/seal still records root-readback-pending at packaging time. I verified the supplied archive independently; I neither infer an unrecorded external root readback nor treat that historical flag as a new product blocker.

## 7. Return disposition and next action

Retain the original nine PASS records byte-for-byte. Record this addendum's nine scoped resolutions; keep the four prayer bindings insufficient and the thirteen OTHER documentation failures separate. No new corrective finding is raised in this delta's scope. There is no need for another attachment to complete this review.

Continue the already-authorised DAG work. Check affected source/consumer drift before reusing these approvals in a newer integration; repeat only invalidated proof. Do not add duplicate completion credit, conflate INFO with RESOURCE/NATIVE, reopen accepted research or create a new review queue because this report exists. PR43 startup/lighting, deferred platform, visual, delivery, issue closure and exact-head owner merge/deployment gates are unchanged.

**No merge, deployment, public publication or issue closure is approved by this report.**
