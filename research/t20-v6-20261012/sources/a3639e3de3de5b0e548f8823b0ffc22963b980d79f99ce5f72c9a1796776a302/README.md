# Productive finite-prefix realisation of the tagged law

This is a separate successor to Tagged_Row_Measure_Bridge_20260930.zip. The original four-module seal is unchanged.

## New checked connection

PrefixBits proves exact arbitrary-bit extraction from ObserverCore's actual sentinel encoding. FiniteSelector selects the first zero using only the supplied n+1 bits. SelectorPrimrec proves that finite selector jointly primitive recursive.

PrefixObserver defines a concrete natural-number prefix evaluator. It echoes the current bit until and including the selector's first zero. Afterward it copies the current bit exactly when the selected row's least-candidate innovation flag is true; otherwise it emits zero. Its complete infinite ObserverCore.output is proved equal to the earlier tagged measurable observer, including the all-true input.

PrefixPrimrec proves this finite-input family jointly primitive recursive for one fixed jointly primitive-recursive matrix family. The actual fair-source output law therefore has defect zero exactly when forall rows i there exists a witness s satisfying every test t. The proof does not select a row by examining unseen future input.

Eight checked controls cover first/middle/last/no zero, a good row suppressing a bit, a bad row copying it, the zero-defect all-true matrix and a positive-defect split matrix.

## Exact ceiling

The result is about the mathematical unbounded-natural-number prefix semantics. It does not claim that a resource-limited host accepts every input size. It is not a uniformly primitive-recursive evaluator of arbitrary program syntax. It does not establish the numeric/byte codec or an effective index translator for every primitive-recursive derivation; the separate compiler lane owns those obligations. Consequently a Pi3-shaped semantic equivalence is not silently relabelled as a complete index-set reduction.

## Evidence

Fresh qualification rebuilt all 29 custom modules from copied source, reusing only pinned official Mathlib caches. All 59 designated theorem readbacks passed under propext, Classical.choice and Quot.sound. The 59 include the original 35; they must not be added to that predecessor count.

Lean4.19.0, compiler commit6caaee842e94; Mathlibc44e0c8ee63ca166450922a373c7409c5d26b00b. The archive contains the complete custom dependency closure, receipts and logs. Independent review is requested separately. No canonical source or campaign status changes are implied.
