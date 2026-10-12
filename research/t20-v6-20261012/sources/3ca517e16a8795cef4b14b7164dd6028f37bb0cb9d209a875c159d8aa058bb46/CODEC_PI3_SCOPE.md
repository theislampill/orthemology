# Exact numeric observer codes and a primitive-recursive Pi3 lower-bound bridge

## Qualified result

The eleven new modules CodecVarint, CodecNumeric, CodecExpr, CodecStmt, CodecProgram, CodecWitnesses, CodecParameter, CodecPrimrec, CodecIndexPrimrec, Pi3Program and Pi3IndexReduction were freshly compiled at Lean 4.19.0 / pinned Mathlib. All 82 named declarations were read back with their full types and axiom footprints. Only propext, Classical.choice and Quot.sound occur. Three false-proposition controls fail and the baseline passes. The receipt is receipts/codec-pi3-20260930T161529Z/CODEC_PI3_RESULT.json (SHA-256 9852843e0347603d65d60074e869df5c55333b60bb4e1472cda63d1a47d32bcf).

## Exact effective statement

For each fixed decidable four-variable matrix R(a,i,s,t) whose joint relation is Mathlib PrimrecRel, there exists a function f : Nat -> Nat such that:

- f is Mathlib Primrec;
- the actual fair-Cantor law of ObserverCore.output (evaluateIndex (f a)) has positive-singleton defect zero exactly when forall i, exists s, forall t, R(a,i,s,t);
- a companion theorem gives strictly positive defect exactly when exists i, forall s, exists t, not R(a,i,s,t).

The first theorem is P02A2.Pi3IndexReduction.exists_primrec_zero_defect_reduction. Its target set zeroDefectIndices is defined from the actual fairCantor.map of the actual numeric evaluator's ObserverCore output. The exact function is parameterIndex p, where p is one fixed ternary LOOP program for the jointly PR finite-prefix family. It inserts a as an actual constant, leaving inputs n and sentinel-coded word in registers 0 and 1, then serializes the resulting binary observer program with the recovered wire tags and numeric envelope. CodecIndexPrimrec.parameterIndex_primrec proves that map primitive recursive.

Pi3Program.numeric_observer_eq proves equality of the entire resulting output function with the sealed tagged observer, not merely finite sampling or equality of defect. The law therefore inherits the tagged mixture's exact quantifiers. A failing row yields positive defect, not necessarily atomlessness or defect one; the latter endpoints belong to individual Sigma2 rows.

The fixed-program existence uses the separately sealed extensional PR coverage theorem. Once that one program is fixed, literal specialization and encoding are explicit primitive-recursive functions. No extractor from erased Prop proofs or uniformly primitive-recursive universal program evaluator is used.

## Codec details and source binding

Exact recovered counterpart: codec-source/prcodec.py, identical to private-locator:d8dc20b3e088111e6617.
SHA-256: dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c.
Original uploaded ZIP SHA-256: f90e399269ccd33c1df42b13c085f09d4e85ea6e2ecfd6f6ee9501de6671d0e2.

CodecVarint translates the actual bitwise unsigned LEB128 emitter and the reader's shift/OR accumulator plus canonical re-encoding check. It proves both stream roundtrip and an exact acceptance characterization. CodecNumeric translates big-endian accumulation and minimal-byte expansion with a leading 0x01 sentinel, proving the exact range characterization on genuine bytes. Both emitters are formally Primrec.

Expression tags 1 through 10, statement tags 16 through 19, and magic bytes P02L followed by version 1 are preserved. Binary seq serializes as a Python-valid variadic sequence of length two; skip is length zero. The parser accepts arbitrary child counts and lowers them through sequenceList, whose execution equals the ordered list fold. This normalizes syntax and does not claim byte identity with the recovered compiler's flattened sequence output.

Expression and statement parsers have an explicit depth fuel. Generated encodings are proved to need at most their byte length, so the public decoder supplies enough fuel. decodeBytes_encodeBytes and decodeIndex_programIndex give exact generated-code roundtrips, and evaluateIndex_programIndex binds their interpreted value to the unchanged LOOP semantics, with the expected arity-two check and output modulo two.

A differential serialization check covers seven actual Lean-generated programs, including all expression operators, skip/set/seq/loop/branch, two PR-derived programs and the actual Sigma2 AST compiler. Every byte sequence is accepted by the recovered Python decoder, re-encodes exactly, and produces the same numeric sentinel encoding. The separate execution probe was interrupted because evaluating larger functional-store examples was too costly; it is not counted as a successful interpreter equivalence test. The independent auditor is running separate bounded source comparisons.

## Controls

Kernel-checked positive vectors cover varints 0,127,128,16384,624485, canonical rejection of overlong encodings, truncation and non-byte values, wrong magic version, trailing bytes, and arity-one observer rejection. Negative files assert the wrong varint byte order, reversed base-256 byte order, or ignored observer arity; each is rejected as a false proposition.

## Boundaries

This is a formal effective lower-bound reduction for the stated primitive-recursive normal forms. Calling those normal forms the full arithmetical Pi3 class relies on a separately stated standard normal-form convention/theorem. No index-set membership upper bound is proved here, so the complete index-set classification is not claimed.

The parser roundtrip is about generated valid codes. These theorems do not establish equivalence with every malformed Python input, Python type/exception behavior, early impossible-child-count rejection, or host recursion/storage/time limits. Resource exhaustion never becomes a proved semantic zero. The numerical evaluator is a mathematical total definition using the retained grammar; full implementation-level Python interpreter refinement is separate.

All earlier seals and original checkpoint sources are preserved. There is no canonical adoption, external mutation, or novelty claim.
