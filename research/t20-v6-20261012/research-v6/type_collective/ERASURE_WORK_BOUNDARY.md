# Exact constructor erasure loses source work

New v6 corollary, source-level counterexample, 2026-10-11. Independently reviewable formal source: `ErasureWorkBoundary.lean`. Fresh pinned Lean 4.19 compilation succeeds with no axioms; receipt `fresh_lean/native_constructor/ERASURE_WORK_COMPILATION.json`. The initial failed `decide` attempt and its error output are preserved, with no proof credit. Its correction supplies literal reflexivity for Cert equality before finite decision.

Let p be the source proof `allI(i(var 0))`; let q be `reduce p [i]`, a valid singleton reduction trace. Both source checkers accept the same erased term I and the same polymorphic identity type. The actual Cert encoder returns literally the same certificate for p and q: a singleton trace emits zero Cert.step constructors.

Nevertheless sourceRun records structural checking charges 22 and 34. The separate exporter-construction counter is 2 versus 3 because the source reduce wrapper itself consumes one work unit even though it emits no target step. The formal theorem states all these equalities together. These quantities are exact declared structural charges, not host time, memory, gas, or total machine instruction count.

The same example was independently replayed through the unmodified archived reference.py and proof_export.py, instrumenting only the work-list observations around bound_tree. Both return equal term/type and equal certificate text; the measured logical charges are exactly 22/34 and 2/3. Receipt: `fresh_lean/native_python/FRESH_PYTHON_REPLAY.json`.

Thus no function of the erased Cert alone can recover either of these exact source work quantities on this input domain. Proof: if such a function existed, literal equality of the two Cert inputs would force equality of its outputs, contradicting 22 != 34 (or 2 != 3). A cost-preserving use of this source-to-target square therefore needs retained source work/provenance or a different explicitly justified cost objective. This does not deny the proved acceptance/term/type erasure square, nor prohibit computing target-only cost.

The stronger existing source obstruction remains separate: malformed singleton traces can erase to accepted targets despite source refusal, and a balanced source-accepted proof can fail the independent 512-unit exporter gate. Those are original results, not new v6 discoveries.
