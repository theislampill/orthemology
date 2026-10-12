# Ordinary total-computability argument for the actual cylinder table

This is a source-driven mathematical argument, not a Lean theorem that Codec.evaluateIndex or indexTable is Mathlib Computable. The exact measure/table equality and fixed-index Primrec statements are separately kernel-checked. The distinction matters because pointwise primitive recursiveness does not imply a uniformly primitive-recursive evaluator.

## Numeric decoding and syntax

CodecNumeric.toBytes repeatedly divides a positive natural number by 256, strictly decreasing it. decodeNumeric checks the nonzero leading-1 sentinel. CodecVarint.readAccum recurses on the finite byte list; uvRead checks its finite consumed slice against the canonical encoder. The canonical encoder repeatedly divides by 128. These are effective terminating algorithms. A separate numeric-component probe targets formal Primrec certificates for toBytes and decodeNumeric; any qualified additions are not required by the present prose argument.

CodecExpr.readExpr recurses on a natural fuel. CodecStmt.readStmt recurses on fuel and delegates a finite child count to readMany, which recurses on that count. It therefore returns a finite syntax tree or none for every finite input. decodeBytes supplies the remaining byte length as fuel, checks the fixed magic/version, parses natural arity/output fields, and rejects a nonempty remainder. The generated-code roundtrip theorem proves this fuel is sufficient for every serialized program.

## Uniform evaluation

For any decoded finite syntax tree, only finitely many registers occur in its input list, output field, reads, writes and loop indices. An ordinary implementation can store the touched natural register values in a finite map, with missing entries zero. There is no infinite tape or semantic oracle to query.

Expression evaluation recursively visits a finite expression tree. Addition, truncated subtraction, multiplication, total natural division/modulo and powers of two have uniform terminating algorithms. The specified division-by-zero and modulo-by-zero values match the retained natural-number semantics.

Statement evaluation is a nested recursion on finite syntax and natural loop counts. Sequence and branch evaluate smaller substatements. A loop first computes its bound once, then executes exactly that captured number of iterations; each iteration installs its current index before evaluating the strictly smaller body. Thus structural induction on a program proves termination on every input, without asserting a common primitive-recursive runtime bound for all program codes.

For malformed codes or decoded nonbinary arity, evaluateIndex explicitly returns zero. For valid binary codes it starts registers 0/1 at n/word, other registers at zero, executes the program and returns the designated output modulo two. Host storage/time/stack exhaustion is not one of these mathematical semantic cases and is not reclassified as zero.

## Finite rational matrix

FiniteOutputTable.finiteOutput runs each output position i<N on the sentinel encoding of the first i+1 bits of its supplied N-bit word. There are exactly 2^N source words and finitely many output words. preimageWords decides equality of two finite Boolean vectors and counts matching source words. tableProbability divides this natural count by 2^N in nonnegative rationals, a positive denominator even when N=0.

Consequently the real code gives a uniform terminating numerical algorithm for every index e, horizon N and output word w. The kernel theorem indexTable_exact identifies that rational with the actual fair-Cantor pushforward cylinder mass. A finite rational heavy-word sum and comparison are then uniformly decidable by exact arithmetic, including threshold equality. This supports the ordinary arithmetical normal-form membership argument, while a complete formal Mathlib Computable certificate for the decoder-plus-syntax-plus-evaluator remains an explicitly open mechanisation boundary.
