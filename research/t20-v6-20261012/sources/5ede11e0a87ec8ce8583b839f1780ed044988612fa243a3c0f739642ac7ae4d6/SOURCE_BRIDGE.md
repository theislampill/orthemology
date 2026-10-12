# Source-to-kernel boundary

Target source is the unchanged `prcodec.py`, SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`, copied under `inputs/`. This document describes a structural transcription correspondence to the original generated AST. It is not a kernel formalization of the Python language or its host interpreter.

## Exact lowering used

The inherited `ObserverCore.Expr` has the source's constant, register, add, truncated sub, mul, div, mod, le, eq, and pow2 constructors. Natural division/modulo at zero and nonzero conditional guards agree with the source. The inherited `ObserverCore.exec` snapshots LOOP bounds and stores the iteration index separately from mutable registers. Its supported renaming/reset theorem already exists in `LoopRenaming` and is reused unchanged.

A Python variadic `Seq(s_1,...,s_k)` lowers to inherited `CodecStmt.sequenceList [T(s_1),...,T(s_k)]`; an empty sequence becomes skip. Other statements lower constructor-by-constructor. This is the existing decoder's Seq lowering. It preserves execution, but encoding the lowered binary AST again can introduce nested sequence tags. Accordingly this work does not claim numeric-code or byte-for-byte equality between Python's original variadic serialization and a reserialized binary core AST.

For an arity-two source program with body `s` and output `o`, `sourceRegisters (T s) o` is `{0,1,o}` union the source body's read/write/counter register support. The formal register list sorts this exact finite support in ascending order, and its fresh map is `r ↦ 12 + idxOf r registerList`. It does not replace compressed allocation with the different full-range translation used by `PRProgram.call`.

## Source correspondence by location

- Lines 297–298: registers 3 through 11 and expressions for `L=n+1`, current-bit modulo and `jlen=j+1` appear unchanged in `LiteralShiftSyntax`.
- Lines 300–305: `scanBody` and `scan` preserve the source's guard, assignment order, denominator and prefix extraction, below-first inclusive comparisons, and stored one-based stopping length.
- Lines 306–307: `replay` preserves truncated tail length, `2^tail_len + word % 2^tail_len`, base index `tail_len-1`, and final parity assignment.
- Lines 236–243: `literalInline` is the actual ordered zero-reset list, ordered argument list, renamed source body and answer capture, grouped by the exact Seq-list lowering. A new grouping lemma identifies its execution with the inherited `inlineCode` theorem; no replacement allocator is used.
- Lines 309–310: `compileShift` retains the three initial resets, scan, unconditional current-bit copy, and nested found/branch/`stop<=n` replay guards. `finish` and `initialise` are proof-time groupings; `compileShift_exec` proves their execution composition for the literal complete sequence.

These correspondences are checked by direct source inspection and the ordinary structural interpretation of the displayed functions. The kernel checks the resulting typed AST and its execution theorems. There is no new kernel theorem that parses `prcodec.py`, executes Python, or identifies every concrete original serialized byte string with that typed AST.

## Quantifiers and exclusions

The typed AST template is meaningful for every natural `a,b`, and some proofs intentionally cover this larger mathematical domain. The Python entry point validates natural inputs, requires arity two, `b>0`, and `a<=b`; only that accepted domain is claimed to correspond to Python construction. The source body must be a finite grammar-well-formed AST; the `Program` dataclass alone does not validate it.

Mathematical natural-number execution and successful host returns are distinct. Actual compilation can encounter recursion limits, and execution can encounter meter/storage/memory limits; no universal host-return guarantee follows. The formal store semantics does not contain an explicit Set-event trace, so the exact trace proof remains the separately reviewed ordinary result. The new kernel modules must be judged by their observed build and axiom records, rather than by this source correspondence alone.
