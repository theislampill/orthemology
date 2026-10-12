# CV-C — concrete P02-L1 syntax, compilation and universal correspondence

P02-L1 is a **new scoped definition proposal**, not the recovered historical numbering. It is implemented in `code/prcodec.py`. This document proves its mathematical properties and the algorithms' source-level correspondence by ordinary structural arguments. It does not assert that Lean checked either the interpreter or the byte codec.

## C2-01. Concrete programs and canonical numeric codes

A program is `(arity k, output register o, statement s)`. Registers are natural-number indexed and store natural numbers. On arguments `(x_0,…,x_(k-1))`, registers j<k contain x_j and all other registers contain zero. The mathematical store has only finitely many relevant coordinates for each fixed program. Expressions are

`constant(n), register(r), add(e,f), sub(e,f), mul(e,f), div(e,f), mod(e,f), le(e,f), eq(e,f), pow2(e)`.

Subtraction is truncated at zero; div(a,0)=0; mod(a,0)=a; comparisons return 0 or 1. These are total primitive-recursive natural functions. Statements are `set(r,e)`, `seq(s_1,…,s_l)`, `loop(r,e,s)`, and `if(e,s,t)`. A loop evaluates its bound e **once**, obtaining N; for j=0,…,N-1 it sets r=j and executes s. Changing r or the bound's input registers in s does not change N or the next forced index. Conditionals branch on nonzero, not only on the value 1.

The bytes are completely specified, not “some Gödel numbering”:

- magic/version prefix: hexadecimal `50 30 32 4c 01`;
- then canonical unsigned LEB128 k, canonical unsigned LEB128 o, then one statement;
- expression tags: constant=1, register=2, add=3, sub=4, mul=5, div=6, mod=7, le=8, eq=9, pow2=10;
- constants/registers are followed by one LEB128 natural; pow2 by one expression; binary expressions by two expressions in left-to-right order;
- statement tags: set=16 followed by register and expression; seq=17 followed by its child count and that many statements; loop=18 followed by index register, bound expression and body; if=19 followed by condition, then branch, else branch.

Unsigned LEB128 emits successive low seven-bit digits, setting the continuation bit except on the final byte. Zero is the single byte 00; unnecessary leading high zero digits are rejected. A whole program permits no trailing bytes. Its natural-number index is the big-endian value of **01 followed by the complete program bytes**. A natural code without that leading sentinel, a bad magic, unknown tag, overlong varint, missing child, or trailing bytes is invalid. A syntactically valid program of arity other than two is also assigned the zero **observer** (though it remains usable as a matrix or closure program at its declared arity).

The well-formedness predicate is `decode(index) returns a program`; observer-well-formedness adds arity=2. Invalid observer indices have the total semantics `P_e(n,w)=0`. They are not discarded from the natural-number index universe. Resource exhaustion is not invalid syntax and never receives the zero semantics.

## C2-02. Codec correctness and primitive-recursive construction operations

Every syntactic node has a unique tag and declared number of children. Canonical varints have a unique digit decomposition. Induction on expressions and statements therefore proves `decode_bytes(encode_bytes(P))=P`. Conversely, each successfully parsed byte string has canonical components and consumes the whole input, so re-encoding returns exactly those bytes. The high numeric sentinel makes the byte/natural conversion injective. This is injectivity of **syntax encoding**, not injectivity of denotation.

The mathematical decoder is a bounded-stack scan. On an input natural e its byte length is at most e+1. Each parser action either consumes a byte or pops one finite pending-child record produced from a consumed tag. Parsed child counts exceeding remaining byte capacity are immediately rejected. Thus the number of scan/pending-record operations is bounded by a primitive-recursive function of e (a very loose `(e+2)^3` bound suffices). Arithmetic digit extraction, canonicality tests, stack pairing/unpairing and bounded traversal are primitive recursive. An explicit stack may be encoded by nested pairing with a length counter; each scan has a fixed numerical bound, so no unbounded minimisation is used. This establishes PR coding/decoding on natural indices without claiming the universal evaluator is PR.

The Python parser/serializer uses equivalent recursive tree traversal and can encounter a host recursion limit. That is raised as `ResourceLimit`, not returned as invalid-code None. Thus the mathematical decoder is total, while the supplied resource-limited implementation has the exact contract: on successful return it matches the mathematical decoder; on explicit resource failure it makes no semantic classification. No host crash or resource bound is used to decide a mathematical index predicate.

The compiler's register collection, ordered renaming, constant insertion, traversal and serialization are bounded syntactic operations, hence PR in the input numeric code and parameters. A decoded fixed-arity matrix has finitely many referenced registers. Parameter substitution inserts a numeral; it does not run the matrix. Invalid matrix/compiler input is an explicit compilation refusal, not a purported reduction of an undefined source instance.

## C2-03. Totality and exact PR expressive class

For each fixed well-formed P, its denotation is primitive recursive in its arguments. Prove this by syntax induction. An expression is a composition of the listed PR arithmetic primitives. An assignment updates one coordinate of a finite store, a PR operation. Sequential composition composes state transformers; if combines them using a PR zero-test. For a loop, use primitive recursion on the snapshotted natural N to iterate the body's PR store transformer, forcing the current index before each iteration. N itself is a PR function of the initial store. Therefore the loop transformer is PR. This proves totality independently of a physical resource bound.

Conversely every n-ary PR function has a program in this syntax. The implementation supplies `pr_zero(k)`, `pr_succ()` and `pr_proj(k,i)`. `compose(f,gs,k)` evaluates every g_i in a private freshly reset register block, then f on those values. `prim_rec(g,h)` initializes an accumulator to g(x), snapshots the recursion argument, and iterates h(x,j,acc) for j=0,…,n-1. Induction on n proves the standard equations `f(x,0)=g(x)` and `f(x,n+1)=h(x,n,f(x,n))`. Induction on a textbook PR derivation then compiles it into P02-L1. Source matrices with finite arity therefore have exactly the claimed PR expressive power; no external function oracle is an expression tag.

### Register-renaming invariant

`Builder.inline` chooses a fresh injection from **all** registers read or written by the subprogram, including inputs/output, into a disjoint caller block. It zeroes every register in that block on every invocation, writes the arguments, runs the renamed body, and copies the designated output. For expressions, renaming preserves value when corresponding registers agree. For statements, induction (and nested induction over a loop's fixed count) preserves the corresponding store. Disjointness ensures caller registers outside the block are unchanged except for the explicit output copy. Therefore every inlined invocation equals a fresh standalone invocation.

Resetting only inputs is insufficient: a subprogram can read a scratch register before assigning it, so a second invocation could otherwise depend on the first. A regression fixture deliberately uses such a register and confirms fresh-call semantics. The general proof depends on the reset invariant, not that fixture alone.

## C2-04. Time/size bounds and the non-PR universal evaluator

No polynomial-time or uniform PR execution bound is claimed. For a fixed syntax tree one can construct explicit PR majorants by induction. Let B bound all relevant input register values and constants. For each expression build a monotone majorant H_e(B) by replacing sub/div/mod/boolean tests by a sufficiently large monotone bound (e.g. `a+b+1`), and using ordinary addition, multiplication and exponentiation for the remaining nodes. The number of evaluator-stack actions for that fixed expression is bounded by twice its node count plus one; its arithmetic bit-cost is a separate cost model.

For a fixed statement s build monotone store/time majorants `(G_s,T_s)` with G_s(B)≥B. Assignments use `max(B,H_e(B))`; sequences compose G and sum time bounds at intermediate majorants; conditionals take the maximum branch bounds plus expression cost. For `loop(r,e,s)`, put N=H_e(B), start B_0=max(B,N), and recursively set `B_(j+1)=max(B_j,N,G_s(B_j))` and accumulate `T_s(B_j)+2` for N steps. This is primitive recursion in N for the fixed body. It bounds all stores and statement-stack steps. The mathematical finiteness proof does not assume the loop body preserves its index register.

There is no single PR universal evaluator for all these codes. If a uniformly PR U(e,x) enumerated all unary PR denotations, then `g(x)=U(x,x)+1` would be PR. Let e_g be its code; evaluating at e_g yields `g(e_g)=g(e_g)+1`, contradiction. A total **computable** universal evaluator exists by traversing the finite syntax and executing each bounded loop. The distinction is essential to the hierarchy proof: its rational cylinder predicate needs computability uniformly in e, not PR evaluation uniformly in e.

For the concrete reductions the syntactic output is two copies of the fixed input matrix plus bounded fixed control syntax (Σ2/Π3), one copy of the base observer plus fixed control syntax (shift), or one case block per finite machine instruction (Q8). Fresh renaming compresses used register labels. Size is bounded by a computable, indeed PR, function of input code/parameters. One deliberately loose numeric majorant is obtained by the bounded construction itself: traverse at most e+1 source bytes, permit every copied numeral/register up to a PR bound in e and the numeric parameters, and reserve `(e+parameters+2)^4` bytes times a fixed implementation constant. This is a numerical-input bound, not a claim of polynomial bit complexity. Runtime of the candidate test at stage u invokes the fixed matrix at most `(u+1)^2` times per candidate search; Π3 adds a scan of at most n+1 input positions. Rational selection uses at most n+1 dyadic comparisons and one base invocation.

## C2-05. Observer semantics and cylinder correspondence

For a finite bit word u, define its sentinel `code(u)=2^|u|+binary_value(u)` (bits read most-significant first). For every code e, define

`q_e(x)_n=P_e(n,code(x↾(n+1))) mod 2`.

The fallback zero convention makes this total for all natural indices. Each output reads only n+1 input bits, so q_e is synchronous, productive, 1-Lipschitz in the prefix metric and Borel measurable. The implementation `word_code` uses `w←2w+b`, and `output_prefix` calls the program at successive prefix lengths. Induction on input length proves equality with the displayed semantics for every returned trace. `evaluate_index` agrees for decoded binary-arity programs and returns the specified zero for invalid/wrong-arity codes.

Under fair Cantor input λ, every input word u of length n has probability 2^-n. Output prefix σ of length n occurs on the disjoint union of exactly those length-n input cylinders whose computed output is σ. Hence

`ν_e[σ]=2^-n #{u∈{0,1}^n:q_e(u)↾n=σ}`.

This formula is uniformly computable by decoding and evaluating finitely many total programs. The default finite resource limits may refuse some computations; the theorem concerns the mathematical unbounded evaluator. A refusal is not an answer to a hierarchy predicate.

## C2-06. Explicit reduction compilers and their universal simulation relations

### Σ2 matrix compiler

Input: a P02-L1 program R of arity 3 and a natural parameter e. Regard nonzero output as true. Define

`r(u)=min{s≤u:∀t≤u,R(e,s,t)≠0}`, with default u+1,
`r(-1)=0` by convention at the first output only.

`_candidate` initializes its output to u+1, scans s=0,…,u, computes every bounded test t=0,…,u in a fresh matrix block, and stores the first passing s. The `found` bit prevents later overwrites. Two loop invariants prove it returns exactly r(u): before candidate s, no earlier candidate passed if found=0; within its t-loop, good=1 iff all tested values were nonzero. `compile_sigma2` computes r(n), the previous r(n-1) when n>0, and emits the fresh current input bit exactly when they differ. Thus its output is **identically the least-candidate change observer** on every finite/infinite input, not merely on tested words.

### Π3 row compiler

Input: R of arity 4 and e. `compile_pi3` scans the first n+1 input bits for the first zero. If none exists, it copies the current input bit; if the first zero is at n, it copies that stopping zero. If the first zero was at i<n, it computes the row candidate with parameters (e,i) at tail time `u=n-i-1`, compares the previous candidate (with the same time-zero convention), and reveals exactly the current fresh bit on changes. Thus selector word 1^i0 is copied verbatim and followed by the row Σ2 observer on independent tail bits. The all-ones input remains productive and is a single null path. The bit extractor divides the sentinel word by `2^(length-1-position)` and reduces mod 2; at the scanned valid positions the high sentinel cannot alter the extracted bit.

### Rational shift compiler

Input: binary-arity observer P and integers `0≤a≤b`, b>0. At prefix length j it computes the interval `[v/2^j,(v+1)/2^j]`. It stops at the first j for which `(v+1)b≤a2^j` (below) or `a2^j≤vb` (above). All bits through the stopping prefix are copied. Below, fresh bits continue to be copied forever. Above, it strips that prefix, reconstructs the tail sentinel as `2^tail_length+(word mod 2^tail_length)`, and invokes P at the tail output index. The first completed stopping prefix is not accidentally passed to P as a tail bit. At q=0 the above branch is taken after the first bit; at q=1 the below branch is; both yield the correct defect formula even though they use a harmless copied prefix. Every comparison is integer arithmetic.

### Q8 machine compiler

The source is a finite list of two-counter instructions H, increment/register/jump, or zero-test/decrement/two-jump. Registers must be 0 or 1 and every jump must target a valid instruction; malformed or empty instruction tables are refused. The source state is `(pc,c0,c1,halt)`. Each target loop snapshots pc, then tests every instruction index against that snapshot. Exactly one case can run. A zero-test leaves a zero register unchanged and otherwise subtracts one. H sets the halt bit; subsequent iterations do nothing. Induction on simulated steps proves correspondence with the original transition relation. Testing n+1 current instructions detects halting after at most n transitions, including immediate H. The output uses the fresh bit exactly when halt was detected. This is the source-level proof behind M2-06.

## C2-07. Which implementation correspondences are true — and false

1. **Syntax roundtrip:** encode/decode are mutually inverse on well-formed canonical syntax, proved in C2-02. Not a semantic injectivity theorem.
2. **Execution soundness:** whenever the resource-limited interpreter/decoder returns normally, its result matches the mathematical semantics. The expression stack evaluates children left-to-right before applying a tag; the statement stack simulates sequential execution and fixed-count loop recursion. Induction on these stack invariants gives the result for every program/input. Resource failure is an explicit non-answer.
3. **Unbounded semantic completeness:** the mathematical evaluator terminates for every well-formed program/input by C2-03, and emits all its prescribed finite traces. This does not guarantee completion within the configured host limits.
4. **Expressive completeness:** every n-ary PR function has a P02-L1 code, via the closure compiler. Every PR synchronous prefix observer of the declared form therefore has a code. No unknown historical index is asserted to be that code.
5. **Denotational noninjectivity:** two different programs, one setting output zero and one additionally setting an unused register to 7, have distinct encodings and exactly the same output behavior. No injectivity or syntax-level full abstraction is claimed.
6. **Not every computable synchronous observer is represented:** enumerate q_e and define a computable stream `z_n=1-q_n(0∞)_n`; it is computable because the universal evaluator is total computable. The observer constantly outputting z ignores its input and is synchronous, but cannot equal any q_e (evaluate at n=e on input 0∞). Thus the PR class is genuinely smaller than all computable observers. Arbitrary measurable observers are even further outside the countable coded class.
7. **No semantic-decision correspondence:** the hierarchy results do not produce an executable recognizer for zero defect. Σ2/Π3 formulas are classifications with quantifiers, not runtime decision algorithms. The finite Mealy solver is a separate decidable representation.

The exact code-to-measure and compiler equalities are ordinary proofs and explicitly recorded as such. The test suite corroborates concrete finite instances and catches implementation mistakes; it is not promoted into a universal kernel-checked simulation.
