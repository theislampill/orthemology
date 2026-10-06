# Independent review: monotone reference-clock v6

Verdict: **PASS within the stated scientific scope.** No scientific source correction is required. This acceptance applies to the frozen reference-clock extension, not to a deployed clock service, public replay wrapper, whole-program refinement, or progress result.

Candidate: `monotone-reference-clock-v6/MANIFEST.json`, SHA256 `58798e94a43d42595c58f61de8c0ec42be89275530d00b52e4f31024b4e7f611`.

Predecessor: `runtime-cancellation-v5/MANIFEST.json`, SHA256 `bc52d02249a41172488dc7caa34844802eeec4df811f644e4888ad2f412792d5`. Every file covered by the predecessor manifest is byte-identical in this successor; the copied predecessor manifest also matches exactly. Previous scoped acceptances remain separate.

## Source and proof evidence

The three additions are `ReferenceClock.lean`, `MonotoneReferenceTrace.lean`, and `ReferenceClockControls.lean`, in the declared `REFERENCE_CLOCK_SOURCE_ORDER.json` order. They add 23 actual theorem declarations, bringing the author-side total to 312 across 32 new modules, with nine exact accepted imports. Comments are excluded from counting. Ten independent reviewer theorems are additional review evidence, not added author theorem credit.

All three additions were independently compiled from source, sequentially with official Lean 4.19.0, commit `6caaee842e94`, executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, using `-j1 -s65536`. Compilation reused 38 unchanged, previously independently compiled v4/v5 objects. Their current identities were recorded and checked before and after this replay; they were consumed read-only. This is an incremental cold replay of the three additions, not a new cold rebuild of all 41 modules.

The 6,816 pinned Mathlib dependency source files were reverified against the accepted pin at commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The supplied dependency cache was used read-only, without an independent Mathlib cache rebuild. All 312 author theorem closures and all ten reviewer closures were checked; their only dependencies are subsets of `propext`, `Classical.choice`, and `Quot.sound`. The comment-aware proof-token audit found no new `sorry`, `axiom`, `native_decide`, or `unsafe` declarations in the 32 author modules. Compilation and the final challenge run produced no warnings or errors.

The eight original component bindings and the accepted native fixture binding were independently compared with the baseline. The embedded native source was decoded from `PinnedSource.lean` and matched the exact 3,013-byte accepted file, SHA256 `e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359`. The corrected v4 reporting lineage is retained; the old shortened prose/receipt digest is not used as the current source identity.

Replay evidence is in `reference-clock-v6-replay/RECEIPT.json`, SHA256 `f830103361e30e56abd0b6f55632d470482b172c0c2de44d1f31a932cd4c5219`. The separately bound review receipt enumerates the report, challenge source, successful logs, replay harness, and predecessor receipts.

## Accepted reference operation and trace correspondence

`setReferenceTime` is a **new reference-model operation**. It is a record update of `World.now`; the unchanged accepted compiled service contains no such clock operation. It preserves the entire plant, full effective policy, all root memories, completed certificates, fault predicate, and every threshold. It does not update an actor record or manufacture a refreshed observation.

`setReferenceTime_aligned` is deliberately unrestricted in its numerical argument. It preserves the full `Aligned` relation with the identical common state, even for a rollback or an expired lease. This is sound because structural alignment has no premise requiring stored grants to remain live at the present annotation. It does not equate alignment with current admission. The new lemma discharges each existing alignment field; it introduces no generic safety law or desired-conclusion axiom.

`MonotoneReferenceTrace` is a separately named finite trace class. It embeds the complete accepted cancellation runtime event class, and adds an `advance now` step with the explicit premise `w.now ≤ now`. Every ordinary event keeps its prior exact source semantics, shared bad-sign/bad-open flags, and failure/partial-effect behavior. There is no new cancellation fault flag. The old v4/v5 trace definitions and their constant-clock results are unchanged.

The step and finite-trace simulation theorems retain full final alignment and construct a valid common primitive history. An advance translates to an empty common history. A subsequent actual preparation or attempt uses the new value of the unchanged function argument `World.now`; its inherited primitive preparation/landing events carry exactly that value. The common history still has unrestricted numerical timestamp annotations. The theorem proves a forward simulation of this stated enlarged trace class, not a converse or a refinement of every possible service/physical trace.

Full-current-policy successful admission and durable exact-full-envelope cancellation transport through the enlarged class. Existing assumptions on source-bound owner certification, recorded certificate provenance, initial raw base, bounded full envelopes, lifetime fault union, and alignment remain in force. Numerical policy epoch equality does not replace full policy equality. The arbitrary-parameter reference theorem does not enlarge the demonstrated native configuration beyond n=4, B=1, q=r=3.

## Expiry and its limits

`localStep_before_lease_end` separately extracts the strict upper bound from the exact imported installation and repair grant-validity predicates. The source predicates require `observedAt ≤ now`, `now < leaseEnd`, and `leaseEnd ≤ grant.expires`, as well as the grant's own lower and upper time bounds and its other scope checks. The new proof does not assume expiry safety as an interface law.

Thus at or beyond a fixed command's lease end, the actual local step is `none`. At an aligned reachable runtime snapshot, successful full-envelope admission would contradict this fact. `expired_envelope_stays_rejected` combines the snapshot result with the proved numerical monotonicity of every finite reference trace. The conclusion holds for the fixed envelope, arbitrary later allowed events, requester, and shared bad-open flag.

The result permits fresh commands with different lease ends. It says nothing about physical elapsed time, authentic clocks, synchronisation, skew, a deadline service, or progress. Monotonicity is weak: equal-time events and arbitrarily large forward jumps are allowed. An expired command can still attract dishonest preparation evidence; intact live gates supply the veto. A stored actor observation remains independently checked by `propose` and is not repaired by moving the world annotation.

The rollback example is a genuine failure of durable expiry outside the monotone class: the same unlanded, uncancelled native installation envelope and cached commitments reject at 100, then admit again at 2. The author proves there is no monotone trace between those endpoints. The reviewer additionally proves both endpoints align with one and the same genuinely reachable common state, so the distinction is not based on a malformed or unreachable evidence record. The lower observation bound still matters: rolling back to 0 rejects, while 1 admits in this fixture.

Cancellation has a different persistence mechanism. The native control proves that advancing and rolling back the annotation does not erase its complete-envelope tombstone, including after another preparation with permissive dishonest flags. The general continuation theorem here is scoped to the named monotone class. Its premise remains a true cancellation return; the prior one-way Boolean/cumulative-certificate distinction is preserved.

## Non-vacuous source-bound controls and independent challenges

The eight-event timed fixture includes two new reference advances and the same six aggregate operations: prepare, install attempt, certify, deliver, prepare, repair attempt. Installation uses time 3 and raw epoch 2; repair uses time 4 and raw epoch 3. Both preparations and attempts succeed, the exact certificate is returned, and the entire final plant equals the existing `repaired` record. Thus the exact source, both audit histories, rule version 4, and draft revision 9 are retained through the full-record equality. There is a corresponding common history from the accepted initial state. The selected intact path `[1,2,3]` remains an existence witness, not a fault-discovery strategy.

Both installation and repair admit at 89 and reject at 90. This is the command lease boundary, before the grant's expiry at 100. Existing commitments survive the clock update. The actor controls distinguish cached observation 2, current world annotation 90, and non-admitting observation 0 without assigning the actor hidden access to the world clock.

`ReferenceClockV6Challenges.lean` independently checks:

1. Updating to the existing numerical time is full World identity.
2. Arbitrarily many equal-time advance events form a valid finite trace.
3. A single forward advance has no numerical size bound.
4. The rollback resurrection endpoints are aligned with the same reachable common state, including with shared bad-open set true.
5. An expired attempted operation preserves the entire World for any requester and shared bad-open flag under the stated alignment/reachability premises.
6. A distinct fresh envelope with lease end 95 can be prepared and landed at 90, while the old lease-90 envelope fails.
7. The exact observed-at lower bound rejects at 0 and admits at 1.
8. With selected path `[0,1,2]`, expired preparation can record faulty root 0's commitment, fail overall, and still fail the subsequent live attempt; intact root 1 does not commit.
9. Reference updates preserve n, budget, both quorums, and the exact fault predicate.
10. Every old cancellation trace embeds into the new class without additional premises on its ordinary events.

## Scope retained

No source correction or additional premise is needed for the stated v6 safety results. Physical clock warrant, actual authority and reservation, source interpretation, external authentication and cleanup rights, coherent root policy copies, and atomic same-plant/time live mediation remain external burdens. A fixed lifetime charged set is not an instantaneous mobile fault budget. Full runBatch refinement, progress or bounded service, alias-runtime transport, and N2/T0/R5 remain open.

This review does not accept the portable combined distribution wrapper. `replay_reference_clock_v6_incremental.py` is a source-neutral scientific provenance harness with explicit locations and required prior object inputs. A public source-only replay must establish its own package and executable entry-point evidence. Compiled objects, build directories, and private process notes are excluded from any public projection of this review.
