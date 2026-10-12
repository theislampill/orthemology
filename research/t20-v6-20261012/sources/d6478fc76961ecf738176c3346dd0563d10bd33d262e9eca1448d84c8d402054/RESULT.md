# Literal `compile_shift`: universal generated-AST refinement

11 October 2026. Status: **ordinary mathematical proof, submitted for independent review**. No kernel verification, new finite audit, source repair, repository adoption, or T20 closure is claimed.

## 1. Result and exact scope

Let `P` be any well-formed finite P02-L1 program of arity two, with arbitrary designated output register. Let `a,b` be natural Python integers with `b>0` and `a<=b`. Let `S=compile_shift(P,a,b)` be the literal AST specified by `inputs/prcodec.py`, SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`, lines 293–310. No alternate selector or compiler is substituted.

The theorem below identifies its output and its entire explicit Set-event trace, for every natural numerical stage input `(n,w)`, not only genuine sentinel words. On genuine source prefixes it yields the pointwise stream identity, including the unique never-resolving input when `a/b` is non-dyadic. Consequently the already-stated P02 affine defect formula applies to this literal generated program.

The increment is a detailed, independently reviewable all-numerical-input and exact-Set-event refinement of the actual generated AST, with explicit scan and source-call invariants. **It is not the first ordinary universal correctness argument:** the inherited `CV_C_CODEC_AND_CORRESPONDENCE.md`, C2-03 and C2-06–07, already gives the renaming/snapshot argument and states the literal rational-shift correspondence on genuine prefixes. Its C2-02–04 also supplies an ordinary PR coding/construction argument. The rational-cell partition and affine measure calculation already appear in `CV_C_HIERARCHY.md`, C2-12. Those inherited results are not new discoveries here. The 97,456-case review did not itself establish this stronger universal exact-Set-trace/all-numerical-word statement, and its formal-verification exclusion does not erase the earlier ordinary proof.

A provenance correction was made during review after recovering the original codec-correspondence document: an initial draft overemphasized the bounded review's remaining gap without citing that earlier ordinary proof. The final supplement binds and includes the earlier document, distinguishes detailed refinement from first-proof novelty, and claims no closure of the remaining kernel-verification obligation.

**Execution convention.** `Run(P,n,w)` below is the mathematical natural-number operational semantics of the exact interpreter at lines 134–183, with both Meter limits disabled and no host memory/stack bound. It is not a promise that every Python call with its default limits returns. Each successful host execution has precisely this value and trace; a resource exception supplies no semantic value. Compiling/serializing very deep finite ASTs can also encounter host recursion limits: `registers` calls recursive `_regs_expr`, and the renaming functions recurse; `compile_shift` does not catch all resulting `RecursionError` exceptions. The serializer/parser wrap their recursion failures separately. Thus an unconditional universal successful-return claim about the finite-resource Python runtime would be false. This distinction is essential, not a qualification added after proving a different compiler.

A well-formed AST means exactly the finite expression and statement constructors accepted by the serializer, with natural constants/registers; `Program.__post_init__` alone is not a validity checker. Expressions use natural truncated subtraction, division by zero equal to zero, modulo zero equal to its dividend, and natural Boolean values, as at lines 149–155. The proof never assumes a uniformly primitive-recursive universal evaluator.

## 2. Specification on every natural numerical input

Fix `n,w` in the naturals and put

- `L=n+1`;
- `W=w mod 2^L`;
- `x_0,...,x_(L-1)` the unique length-`L` binary word of value `W`, allowing leading zeros;
- `U_k=floor(W/2^(L-k))` for `1<=k<=L`, and `U_0=0`;
- `q=a/b` as an exact rational.

A nonempty prefix of length `k` is **below** when

`b(U_k+1) <= a 2^k`,

and **above** when

`a 2^k <= b U_k`.

They mean respectively that the entire dyadic cell is at or below `q`, or at or above `q`. Since `b>0`, these two conditions cannot hold simultaneously. Define `tau` to be the least `k` in `{1,...,L}` satisfying either condition, if there is one; its branch is `c=0` below and `c=1` above. If no such `k` exists, write `tau=none`.

**Finite-stage refinement theorem.** The literal generated program satisfies

`Run(S,n,w) = w mod 2`

if `tau=none`, or `c=0`, or `tau=L`. In the remaining case, `c=1` and `tau<L`, put `t=L-tau>=1` and `v=2^t+(w mod 2^t)`. Then

`Run(S,n,w) = Run(P,t-1,v) mod 2`.

Thus every successful outer return is already a bit. The numerical input need not have a high sentinel; the compiler observes precisely its low `n+1` bits, and installs a fresh sentinel in the base argument.

For a genuine word `x` of length `L`, `word_code(x)=2^L+W`; hence the statement specializes directly to the source's actual word convention. Values `(n,w)` inconsistent with that convention are included in this finite-stage theorem but do not constitute arbitrary extra infinite-stream encodings.

The stronger trace statement is in Section 6. The proof follows the source execution, rather than using the claimed affine formula to infer program correctness.

## 3. Interpreter and hygienic inlining lemmas

### 3.1 Exact operational semantics and termination

A store is a natural-valued map with default zero. `eval_expr` implements the indicated expression evaluation by a postorder stack: a frame `(e,False)` first places the return frame and then children in reverse stack order; `(e,True)` pops child values in reverse order and supplies each operand in its original source position (for a binary operation, right operand `b` is popped before left operand `a`). Induction on expression structure proves that it returns the usual compositional value. Constants and variables are the base cases; every constructor combines already-evaluated natural child values by its displayed operation. This also proves termination for every finite expression under the unbounded convention.

For statements, `set` evaluates before updating its target; `seq` executes in written order because children are stacked in reverse; and `if` evaluates its guard once and chooses the positive branch exactly when its value is nonzero. `loop(r,e,B)` evaluates `e` **once in the entry store**, yielding a finite natural `c`, and places a repeat frame containing that saved `c`. For each `i=0,...,c-1`, it assigns `r=i` and executes `B`; mutations of `r` or of variables in `e` during `B` do not change the saved count. A zero-count loop leaves its counter unchanged; after a positive-count loop, the final body can leave the counter at any value, so no generic final-counter formula is assumed. Structural induction on statements, with an inner induction over this finite count, proves termination and equivalence to this big-step semantics. The final value is the designated output register, defaulting to zero.

With tracing enabled, only explicit `set` instructions append `(register,value)` events. The implicit LOOP-counter updates at line 169 are deliberately absent. Nothing here asserts equality of meter step counts between a base call and the entire compiled call.

### 3.2 Register support and renaming

For a well-formed program, `R=registers(P)` at lines 205–219 is finite and includes all argument registers, the output register, every variable read, every assignment target, and every loop counter. This follows by induction over the same finite AST. No expression or statement in `P` refers to a register outside `R`.

Let `m` be any injective map on `R`. Suppose stores `sigma` and `rho` satisfy

`rho(m(r))=sigma(r)` for every `r in R`.

Expression induction gives equality of original and renamed expression values. Statement induction gives the following simulation for `rename_stmt` at lines 226–231:

1. The final stores still agree under `m` on every register in `R`.
2. The renamed statement writes only registers in `m(R)`.
3. Its explicit Set-event sequence is exactly the original sequence with each register name `r` replaced by `m(r)`; values and order are unchanged.

For a loop, expression equality gives the same saved count in both runs. At iteration `i`, their implicit counter updates assign respectively `r=i` and `m(r)=i`, restoring the simulation relation before invoking the body induction. That induction permits the body to overwrite the counter, input registers, or any other supported register. The next iteration reassigns the counters and the stored count remains unchanged in both runs. This handles the potentially troublesome bound/counter/input aliases rather than assuming they are absent.

### 3.3 The actual `Builder.inline` call

The literal shift allocates registers as follows:

`0=n, 1=w, 2=outer output, 3=j, 4=found, 5=branch, 6=stop, 7=value, 8=den, 9=tail_len, 10=tail_word, 11=answer`.

Its only base inlining starts with `Builder.next=12`. If the members of `R` in increasing order are `r_0,...,r_(h-1)`, line 240 constructs precisely

`m(r_i)=12+i`.

This is injective and disjoint from all outer registers `0,...,11`. The helper emits a zero Set for **every** mapped source register, including never-written locals and a possibly never-written output register. It next assigns the two base arguments to `m(0)` and `m(1)`, executes the renamed body, and copies `m(P.output)` to register 11.

The argument expressions in this particular call read only registers 9 and 10. Therefore neither the resets nor either preceding argument assignment changes a later argument expression's value. After argument installation the mapped store agrees with a fresh direct call of `P` on those two arguments: source registers 0 and 1 contain the arguments and every other supported source register is zero. The renaming lemma consequently proves equality of base results and mapped Set traces. The final answer copy is correct even when the source output aliases an input or loop counter. During all of this registers `0,...,10` are untouched by the renamed base; the explicit answer copy only changes 11.

This is a proof for the actual call site's freshness conditions. It is not an unconditional theorem for every conceivable use of `Builder.inline` with argument expressions that might themselves mention newly allocated registers. Nor does the proof invent a history-leak defect: this shift executes its base at most once per fresh outer run.

## 4. Arithmetic extraction and the scan invariant

### 4.1 Exact prefix extraction

For `1<=k<=L`, Euclidean division writes `w=h 2^L+W`, with `0<=W<2^L`. Hence

`floor(w/2^(L-k)) = h 2^k + floor(W/2^(L-k))`.

The second summand belongs to `{0,...,2^k-1}`. Therefore

`floor(w/2^(L-k)) mod 2^k = U_k`.

This identity is valid for all natural `w`, not merely sentinel words. For genuine words the `h=1` term is exactly the high sentinel removed by the modulo operation. Also `w mod 2=x_(L-1)`.

### 4.2 Invariant after `s` scan iterations

The initial explicit Sets are `(4,0),(5,0),(6,0)`. The outer LOOP's entry bound is `L`; its counter is register 3. Registers 0 and 1 are never assigned during the scan, so their values remain `n,w`, but the proof still uses the interpreter's snapshotted-bound semantics.

For every `s` with `0<=s<=L`, after exactly `s` iterations:

- If no prefix among lengths `1,...,s` has resolved, then `found=0`, `branch=0`, `stop=0`. If `s>0`, additionally `den=2^s` and `value=U_s`; if `s=0`, registers 7 and 8 are still their default zero.
- Otherwise, let `k` be the earliest resolved prefix among those lengths, with branch `c`. Then `found=1`, `branch=c`, `stop=k`, `den=2^k`, `value=U_k`.
- Only registers 3 through 8 have been touched, apart from the three stated initial Sets. Registers 0,1 retain the arguments, register 2 is still zero, and registers 9 upward remain default zero.
- For `s>0`, register 3 has value `s-1`, whether or not resolution already occurred. A found selector suppresses the body, not the implicit remaining LOOP-counter updates.

The invariant at `s=0` is immediate. For the induction step, the implicit update sets `j=s`, so `jlen=s+1=k`. If `found=1`, the outer `if found==0` has no body effects; all stored selector values remain frozen and the invariant advances.

If `found=0`, `1<=k<=L`, so the source's truncated subtraction `L-k` is the ordinary nonnegative difference. Line 301 assigns `den=2^k` and then assigns `value=U_k` by the extraction identity. The first comparison is exactly the below condition. If true, lines 303 set found, branch and stop to `1,0,k`. Otherwise the nested comparison is exactly the above condition, and if true line 305 sets them to `1,1,k`. If neither holds they remain `0,0,0`. Earlier prefixes were unresolved by the induction hypothesis, so any new resolution is the earliest one. The two conditions are mutually exclusive because their conjunction would imply `b(U_k+1)<=b U_k`, contradicting `b>0`. This establishes the invariant for `s+1`.

At `s=L` the invariant identifies the actual final selector state with `tau` and its branch. In particular the scan does not inspect additional cells after finding `tau`, even though the LOOP continues its remaining counter/guard steps.

## 5. Post-scan refinement

Line 309 next executes `Set(2,w mod 2)` in every case. The three nested guards enter replay exactly when

`found=1`, `branch=1`, and `stop<=n`.

By the invariant, `1<=stop=tau<=L=n+1`, so the final inequality is equivalent to `tau<L`. Thus no base call occurs on the stopping observation itself, when `tau=L`; it copies the stopping bit.

On replay, `t=L-tau>=1`, so both truncated subtractions in the tail length and base index are ordinary subtraction. The assigned word is exactly

`v=2^t+(w mod 2^t)`.

Because `tau>=1`, the suffix is strictly shorter than `L`; its low `t` bits are `x_tau,...,x_(L-1)`. Their `word_code` is exactly `v`, including when they all vanish. The inlining lemma gives `answer=Run(P,t-1,v)`. Finally line 307 assigns its parity to register 2. This proves the finite-stage refinement theorem in every case.

The proof uses no numerical upper bound on `a,b,n,w`, no coprimality assumption, no bound on the number or names of source registers, and no restriction on source LOOP nesting beyond finiteness and well-formedness.

## 6. Universal explicit Set-event trace

Let `K=L` when there is no resolution and `K=tau` otherwise. The exact outer Set trace begins with

`(4,0),(5,0),(6,0)`.

For each `k=1,...,K`, in increasing order, append

`(8,2^k),(7,U_k)`.

If resolution occurs, append, immediately after the pair for `k=tau`,

`(4,1),(5,c),(6,tau)`.

After the entire scan, append `(2,w mod 2)`. No Set events arise from the suppressed scan body at later iterations; implicit updates to register 3 are not trace events.

If there is no above replay, this is the entire trace. Otherwise append:

1. `(9,t),(10,v)`;
2. `(m(r),0)` for all source registers `r` in increasing order;
3. `(m(0),t-1),(m(1),v)`;
4. the complete explicit Set trace of a fresh `Run(P,t-1,v)`, replacing each register `r` by `m(r)`;
5. `(11,Run(P,t-1,v)),(2,Run(P,t-1,v) mod 2)`.

Every event and its placement follow respectively from the scan induction and inlining simulation. This is the same observable that the old finite audit checked, now proved for arbitrary finite well-formed base ASTs and inputs. It does not silently enlarge “Set trace” into all writes or all instructions.

## 7. Arbitrary representations and endpoints

If valid pairs `(a,b)` and `(a',b')` represent the same rational, multiplication by the positive denominators proves that each below/above test has the same truth value. Thus all selector states, outer outputs and Set-event traces agree for every `P,n,w`. Their compiler ASTs and encoded indices may differ. No reduction to coprime terms is required.

This statement is about unbounded semantics, and successful executions when both return. With finite integer-storage caps, a very large unreduced constant can exhaust a cap when its reduced representative does not. In particular the theorem does not assert equivalence of resource-exception behavior.

At `q=0`, the below inequality is impossible because `b(U_k+1)>0`, while the above inequality holds already at `k=1`. Hence `tau=1,c=1` on every input. Stage `n=0` copies the first input bit; every later stage invokes the base on the suffix after that bit.

At `q=1`, `U_1+1<=2`, so the below inequality holds at `k=1`. Therefore `tau=1,c=0` and the literal shift copies every input bit. It is exactly the identity stream map, independently of the base.

In particular `q=0` preserves the base's defect but need not preserve its entire output law: the initial source bit is still copied. Claiming the literal zero shift equals the base stream map would be false.

## 8. Pointwise infinite-stream theorem, including the exceptional input

For a stream `x in {0,1}^N`, define its observer output by

`B_P(x)_n = Run(P,n,word_code(x_0,...,x_n)) mod 2`.

Every coordinate is defined by the finite operational semantics and depends only on the observed prefix. This is a synchronous Borel measurable map. Apply the cell tests to every nonempty prefix of `x`; let `T(x)` be the first resolved length, if one exists. Minimality makes this resolution independent of how much additional input is observed.

If `T(x)=k` and `u=x_0...x_(k-1)`, write `x=u z`, where `z` is the fresh tail.

- On a below stopping word, `B_S(u z)=u z`.
- On an above stopping word, `B_S(u z)=u B_P(z)`.
- If `T(x)` does not exist, `B_S(x)=x` at every coordinate.

Proof: for `n<k`, either no prefix has yet resolved or this is the stopping observation `n=k-1`; Section 5 copies `x_n`. For `n>=k`, the stored stopping length is `k`, `t=n+1-k`, and the base index is `t-1=n-k`. Its word is precisely `word_code(z_0,...,z_(n-k))`. The finite-stage theorem now proves the claimed concatenation coordinate by coordinate. In the never-resolving case it copies the current bit at every finite stage without trying to complete an infinite search.

For `0<q<1`, a prefix of length `k` remains unresolved exactly when

`U_k < 2^k q < U_k+1`.

If `q` is non-dyadic, none of `2^k q` is an integer. At each length there is exactly one unresolved prefix, with integer value `floor(2^k q)`. These prefixes are consistent, since

`floor(2^k q) - 2 floor(2^(k-1) q)` belongs to `{0,1}`.

They define exactly one infinite stream `x^q`, the usual non-dyadic binary expansion. This stream remains unresolved for every finite observation and the actual compiled observer copies it pointwise. Conversely any forever-unresolved stream has all these prefix values and therefore equals `x^q`.

If `q` is dyadic, choose `K>=1` such that `2^K q` is integral. Every length-`K` cell lies on one side or has `q` as an endpoint, so all streams resolve by length `K`. Both binary representations of an internal dyadic boundary are treated by the inclusive source comparisons; neither is an exceptional input. At `q=0` and `q=1`, the separate endpoint proof gives resolution at length one.

Thus this compiler is productive on the all-prefix exceptional input. Selector termination is almost sure, and is not universal at a non-dyadic threshold. No infinite source search occurs inside any one coordinate computation.

## 9. Connection to the inherited probability theorem

This section spells out the bridge to the old C2-12 law; it is not a new defect calculation.

Let `lambda` be fair product probability. Let `D` and `A` be respectively the below and above minimal stopping words. Their union is prefix-free: a proper extension of a stopping word cannot be a minimal stopping word. Consequently their input cylinders, and the corresponding output cylinders retained by Section 8, are pairwise disjoint.

At length `N>=1`, exactly `floor(2^N q)` binary words have their cell's upper endpoint at or below `q`. A path has resolved below by `N` iff its length-`N` cell satisfies that condition. Indeed a nested cell stays below after a below resolution, and if it is below now some first below resolution has occurred by now; a prior above resolution cannot coexist with a below descendant. Therefore

`lambda(resolved below by N)=floor(2^N q)/2^N -> q`.

Likewise there are `2^N-ceil(2^N q)` above cells, giving above mass tending to `1-q`. There is at most one unresolved cylinder at each depth, of mass at most `2^-N`. This proves

`sum_(u in D) 2^(-|u|)=q`,

`sum_(u in A) 2^(-|u|)=1-q`,

and the never-resolving set is null. Its output was already defined pointwise in Section 8 before this null-set argument.

Conditioned on an input cylinder `[u]`, the tail has law `lambda`, by the product-cylinder identity. The decision that `u` is a minimal stopping word depends only on `u`, so it imposes no condition on that tail. Let `i_u(z)=u z`, and `nu=(B_P)_*lambda`. The literal output law is therefore

`(B_S)_*lambda = sum_(u in D) 2^(-|u|) (i_u)_*lambda + sum_(u in A) 2^(-|u|) (i_u)_*nu`.

Prefixing is a measurable injection with tail as inverse on its cylinder. It preserves every singleton mass. Fair measure has no atoms since each singleton is contained in cylinders of mass `2^-N` for every `N`. The prefix-free output cylinders are disjoint, so the atomic mass of the right side is

`A_shift = sum_(u in A) 2^(-|u|) A_base = (1-q) A_base`.

For completeness, each positive singleton in an above row is exactly `u y` for an atom `y` of `nu`, of mass `2^(-|u|) nu({y})`; lower rows have none. Summing this countable family proves the displayed atomic-mass identity using the disjointness proved above. Defect `d=1-A` therefore satisfies

`d_shift=q+(1-q)d_base`.

At zero the full law is `1/2 (i_0)_*nu + 1/2 (i_1)_*nu`; at one it is `lambda`. These endpoint laws expose why equality of defects is weaker than equality of observers or laws. An explicit analytic negative control is a base that constantly outputs zero: the literal shift always copies its first input bit, so its first output bit equals one with probability `1/2`, whereas the unprefixed expression `q lambda+(1-q)nu` would give `q/2`. For every `q<1` these differ. The unprefixed law is therefore not the theorem, despite having the same affine defect value.

## 10. Codec and computability boundary

The well-formedness of `S` follows from its displayed finite constructors and the renaming lemma. For every well-formed finite AST `Q`, the mathematical serializers/parsers at lines 34–120 satisfy `decode(encode(Q))=Q`: canonical varint writing and reading are inverse on naturals; expression and statement structural induction then gives inverse syntax traversals; the magic/version bytes and outer high byte are restored exactly, with no trailing bytes. The parser's sequence child-count check cannot reject an encoded sequence because every encoded child consumes at least one byte. The high byte `0x01` survives integer-to-byte reconstruction.

Hence, whenever code construction and parsing return successfully, `evaluate_index(encode(S),n,w)` has exactly the finite-stage output above: its outer parity operation is redundant because `S` already returns a bit. The codec round-trip here is an ordinary proof over the same finite syntax; it is not a new Lean theorem or an executable replay result.

For each fixed resulting AST, its register functions on numerical inputs are primitive recursive by expression/statement induction, using bounded iteration for the snapshot LOOP; its stream remains a total synchronous PR observer in the mathematical semantics. This is a fixed-program claim. The constructor and numeric encoding give an effective code transformation on well-formed finite source ASTs. The inherited codec-correspondence document C2-02–04 already states an ordinary primitive-recursive coding/construction argument, with bounded syntax traversals and numerical size majorants. This refinement neither displaces it nor supplies a new independently formalized uniform numeric PR-transformer theorem. In particular no uniformly PR universal evaluator, proof-to-program extractor, or new numerical compiler index is claimed. If the remaining obligation demands a kernel-checked literal-compiler theorem or a stronger independently verified numeric PR-transformer bridge, this document does not close it; absence of a new bridge here is not evidence that the earlier ordinary construction claim is false.

## 11. Evidence and limits

- Source examined: complete 332-line `prcodec.py`, especially evaluator lines 134–188, register support/renaming/inlining 205–243, and literal shift 293–310.
- Prior scope examined: `inputs/BOUNDED_REVIEW.md`, which limits its assurance to bounded traces; `inputs/PRIOR_CODEC_CORRESPONDENCE.md`, which already gives ordinary universal source-correspondence and PR-construction arguments; and `inputs/PRIOR_HIERARCHY_PROOF.md`, which already owns the rational-cell/affine-law mathematics.
- No external software was downloaded or run. No compiler or repository file was modified. The source and three relevant inherited documents are copied byte-for-byte into this separate research directory for review.
- This is a mathematical induction argument, not another bounded enumeration dressed as a proof. No fresh numerical test counts are offered as evidence of universality.
- Remaining distinctions: independent mathematical review is required for acceptance; no kernel checking, host-resource completeness, new uniform PR numeric-transformer verification, integration, classification advance or T20 closure follows solely from this document. Most ordinary semantic/probability content is inherited; the exact Set-trace and arbitrary-numerical-word refinement is the narrower strengthened statement.
