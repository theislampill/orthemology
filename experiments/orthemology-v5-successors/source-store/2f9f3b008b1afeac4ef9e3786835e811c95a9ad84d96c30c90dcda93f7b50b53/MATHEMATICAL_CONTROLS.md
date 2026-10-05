# Independent mathematical and adversarial controls

3 October 2026 UTC. These are ordinary proofs and exact expected outcomes, independently constructed for review. They are not a new checker implementation or a report of executed acceptance tests. Source runtime behavior mentioned below was inspected directly. Author files are unchanged.

## 1. Direct construction of every coordinate and the enclosure

For any bit stream b, define

`y_i = Σ_(r≥0) b(i+r) / 2^(r+1)`.

The nonnegative series is bounded by 1. Splitting its first term proves `y_i=(b(i)+y_(i+1))/2`, so y is an actual compatible realization. For any other compatible z, unwinding n equations yields

`z_i = Σ_(r<n) b(i+r)/2^(r+1) + z_(i+n)/2^n`.

Both tail coordinates lie in [0,1], hence `|z_i−y_i|≤2^-n` for every n and z_i=y_i. This proves uniqueness at every coordinate, with no oracle choosing an infinite predecessor chain. The same unwinding gives the exact finite image interval and its uniform width `2^-n`.

For coordinate zero, define `V_n=Σ_(k<n) b(k)2^(n−1−k)`. This is an integer with `0≤V_n≤2^n−1`; the algebra gives `V_(n+1)=2V_n+b(n)`. Thus the displayed recurrence has the stated inverse-composition orientation. Directly applying `f_0(f_1(x))` to bits 0,1 gives `(1+x)/4`, not `(2+x)/4`.

## 2. Explicit admissible unary first-halting AST

Use the actual C2-01 syntax. Source data are a nonempty finite valid two-counter instruction table M. Each instruction is H, I(r,t), or D(r,t_zero,t_nonzero), with r∈{0,1} and in-range targets. Both counters and the initial program counter are zero. A stage t means the instruction at the configuration reached after t transitions; H at the initial configuration has stage 0.

Use the following fixed distinct registers:

- 0: unary input n, never written
- 1: output bit
- 2: pc
- 3: snapshotted pc
- 4,5: source counters
- 6: latched halt bit
- 7: bounded-loop index
- 8: old halt bit

Construct a finite P02-L1 program of arity 1 and output register 1. Its body initializes registers 1,2,4,5,6 to zero, then performs `loop(7, add(register(0),constant(1)), BODY)`. The finite BODY does the following, in order:

1. Set register 8 to register 6.
2. If register 6 equals zero, set register 3 to register 2 and execute one finite sequence containing a conditional case for each source index j. Each tests the unchanged register 3 against constant j.
3. In a matching H case set register 6 to 1. In an I case increment the selected counter and set pc to its target. In a D case test the selected counter: if zero, set pc to its zero target; otherwise perform truncated subtraction by 1 and set pc to its nonzero target.
4. Set output register 1 to `sub(register(6),register(8))`.

Every item expands into the listed `set`, `seq`, `if`, expression and bounded `loop` constructors. This description is a finite AST construction recipe, not a new expression tag or an external simulation oracle. Its register numbers are fixed and its source-dependent branches/numerals are finite. Source validity is decidable. The construction uses only bounded traversal of the finite source table, so the table-to-AST map is effective.

**Invariant.** Before the (t+1)-st loop iteration, either halt=0 and pc/counters are the source configuration after t transitions, or halt=1 and the source has already reached H. In the first case exactly one snapshotted-pc case runs. Changes to pc cannot make a second case run. In the second case no case runs. Halt remains a bit and can change only once, from 0 to 1. The output at the end of that iteration is 1 precisely for that change.

After n+1 iterations, output is therefore 1 iff the first H stage is n. An immediate H gives output 1 for input 0 and 0 thereafter. An initial increment to an H instruction gives output 0,1,0,... . A one-instruction increment jumping back to itself gives only zeros. These examples also catch an n versus n+1 indexing error.

This proves a uniform reduction into genuinely well-formed unary P02-L1 programs, using its actual bounded-loop semantics. No arbitrary-machine totality promise is being admitted: every finite evaluation terminates whether or not the simulated source ever halts.

For the resulting P_M,

`x_(P_M)=0` if M never halts; otherwise `x_(P_M)=2^−(t+1)` for its first H stage t.

The standard undecidability/non-c.e. premise for nonhalting of these finite two-counter tables is the inherited source-machine premise, not newly formalised here. Every target state is nevertheless uniformly computable to error at most `2^-n`, and every map is exactly 1/2-Lipschitz. The obstruction is the exact query.

## 3. Arbitrary global finite proofs do not defeat the uniform obstruction

Let C be any effectively enumerable set of finite certificates and let acceptance `A(P,c)` be c.e. Suppose acceptance is sound for `x_P=0` over all admitted P and complete for true zero instances among the P_M just constructed. Given M, enumerate/dovetail the acceptance runs for all c. Acceptance occurs iff M never halts. This would semidecide nonhalting, impossible under the inherited premise.

The verifier is allowed to accept source invariants, arithmetic derivations, induction proofs or finite machine arguments. None is excluded merely because it is not a prefix. The only requirements used are effective finite acceptance, soundness and uniform completeness.

Positive exception: for `P_zero=(arity 1, output 1, set(1,constant(0)))`, structural semantics proves every output zero and the sum is zero. Another exception is the self-looping increment machine above: pc=0 and “no H instruction exists” is a finite invariant. Either may have a genuine finite equality proof. These individual proofs do not make all nonhalting instances enumerable.

An arbitrary *asserted* law is not such a proof. A noncomputable acceptance oracle is outside this theorem. A checker with a finite list of true exceptional zero instances is allowed but remains incomplete across the whole reduction family.

## 4. Discriminatory exact controls

All named simple generators below are unary P02-L1 ASTs of the form `(1,1,set(1,e))`, where e is the given expression. Prefixes start at input 0. No implementation result is asserted.

### C01. Strict positive, with exact depth boundary

Generator `constant(0)`, τ=1/4. At n=2, V=0 and U=1/4: Below must fail. At n=3, V=0 and U=1/8: Below must pass. The equality of the upper bound at depth 2 is not equality of the scalar, which here is 0.

### C02. A genuine delayed nonzero completion

Generator `eq(register(0),constant(3))` emits 0001000... and has scalar 1/16. At n=3 it has exactly C01's interval [0,1/8] and the same below-1/4 conclusion. That interval alone cannot prove zero. The two ASTs differ; this is not a full-source indistinguishability claim.

### C03. Equality reached as a lower endpoint

Generator `eq(register(0),constant(1))` emits 01000... and has scalar 1/4. At n=2, V=1 and [L,U]=[1/4,1/2]. At every later depth L remains 1/4. Above at τ=1/4 must never pass. A mutated `L≥τ` would falsely pass at n=2.

### C04. Equality reached as an upper endpoint

Generator `le(constant(2),register(0))` emits 00111... and also has scalar 1/4. At n=2, V=0 and [L,U]=[0,1/4]. At every later depth U remains 1/4. Below at τ=1/4 must never pass. A mutated `U≤τ` would falsely pass at n=2. This control is essential; C03 alone need not detect that mutation.

### C05. Order-sensitive false acceptance

Use C03 but threshold τ=3/8 and n=2. Correct prefix 01 gives V=1 and interval [1/4,1/2], so neither side is certified at that depth. Reversing composition/order gives V=2 and the false interval [1/2,3/4], which would pass Above although the actual scalar is 1/4. At n=4 the correct interval is [1/4,5/16], which passes Below. All-zero fixtures cannot discriminate this error.

### C06. Valid unary generator versus wrong observer adapter

Generator `constant(1)` has scalar 1. Its depth-3 interval is [7/8,1]; Below at τ=1/4 must fail and Above must pass. Inspection of actual P02 `evaluate_index` shows it returns zero for this arity-one input. Using that wrapper would fabricate interval [0,1/8] and falsely pass Below. The correct general evaluator is `run(P,(i,))`, subject to its explicit resource-limit behavior.

### C07. Bit reduction and raw naturals

Generators `constant(2)` and `constant(3)` have bit streams zero and one respectively, because the design uses output mod 2. An implementation must not accept raw 2/3 as bit prefix entries, or use “nonzero” instead of mod 2. This tests a different issue from P02 conditionals, which correctly branch on nonzero.

### C08. Negative and out-of-range thresholds; depth zero

At n=0 the interval is [0,1] for every generator. Above passes for τ<0; Below passes for τ>1. At τ=0, Below is impossible. At τ=1, Above is impossible. For constant-one and τ=1, neither strict side ever passes; for constant-zero and τ=0, neither ever passes. Numerator p is an integer, not silently restricted to a natural number. Denominator d=0 is malformed, even if host division supplies a fallback.

### C09. Equivalent rationals versus literal binding

τ=1/4 and τ=2/8 give equivalent arithmetic tests. They need not be equal as raw expected records when unreduced rational syntax is permitted. A stale bound record must be rejected if literal equality is the declared rule. Alternatively canonicalise both through a separately declared normal form. Do not silently switch equality notions in one code path. No rule requires two freshly bound equivalent-rational requests to receive different semantic answers.

### C10. Source syntax and semantic equality are different

`set(1,constant(0))` and `seq(set(9,constant(7)),set(1,constant(0)))` have the same unary outputs but distinct ASTs. A certificate for the first is stale for an expected record naming the second. Fresh evaluation of the second can certify the same strict claim. This tests exact input binding without a false claim that the model's mathematical scalar changed.

### C11. Structural malformed inputs

Reject a prefix length differing from n, any non-bit entry, a claimed V unequal to replay, a malformed AST, an unsupported format, and any stale model/version/recipient/rule/comparison field. A depth-3 zero prefix with claimed V=1 is not justified merely because its resulting interval might still happen to lie below some threshold. The claim concerns the submitted verified calculation.

### C12. Refusal is not an answer

A syntactically legal unary program may spend more time or bits than a host budget permits. Its mathematical totality remains true. An explicit resource refusal provides no below/above/equality conclusion; it also does not make the input syntactically invalid. This preserves actual C2-02/C2-04/C2-07 source boundaries.

## 5. Controls for the general theorem, outside the one-dimensional checker

### C13. Nonunique state, robust answer

Let `X_i={0,1}×[0,1]`, `f_i(c,x)=(c,x/2)`. There are two realizations and `S_i={(0,0),(1,0)}`. With observable g(c,x)=x and threshold 1/4, depth 3 gives g-values in [0,1/8], certifying Below for every compatible realization. This is a control of the general robust-query theorem; it is not claimed to be an input to the proposed scalar-only certificate syntax.

### C14. Singleton first coordinate is insufficient for full uniqueness

Let X_0 be a singleton, let every X_i for i≥1 be {0,1}, let f_0 be constant and later maps be identities. S_0 is a singleton, but B has two elements. Do not use a coordinate-zero certificate as a proof that the whole infinite system is uniquely realized.

### C15. Continuity only on the survivor is insufficient

Take `K_n=[0,2^-n]`, S={0}, and q(x)=1 iff x=0. Its restriction to S is continuous. Every K_n also contains positive points, so no finite range makes q constant. A checked global theorem defining the whole family can still prove the survivor is zero; this control excludes only the purported ambient-open inference.

### C16. Compactness cannot be discarded

In ℝ take `K_n={0}∪[n+1,∞)` and U=(−1,1). The sets are nonempty nested and closed, and S={0}⊆U, but no K_n is contained in U. The obstruction is escaping noncompact mass/points, not ambiguity of the final survivor. This control has no effective-search claim.

### C17. Effective names cannot be discarded

Fix a noncomputable α∈[0,1] and let every map be the constant α. The system is compact, continuous and uniquely realized, and every finite positive-depth range is {α}. It does not supply a computable name for that map or point. Any proposed uniform effective solver using only those set-theoretic assertions would have to compute α. This example isolates a missing input contract; it is not the half-affine negative, whose data and state are uniformly computable.

### C18. Searchable slow shrinkage need not come with a preset rate

Let `(r_n)` be positive, nonincreasing computable rationals with limit zero, and `K_n=[0,r_n]`. The name permits exact calculation of each rational endpoint. To certify x<τ for τ>0, enumerate n until `r_n<τ`; the limit promise ensures termination. A numerical modulus need not be included as a separate input. The promise that the sequence tends to zero is not thereby decidable for arbitrary programs purporting to give r_n.

## 6. A stronger use of the example than constant-zero alone

For an arbitrary admitted first-halting generator, finite evaluation may establish bits 0,0,0 without determining whether the source ever halts. That prefix already certifies `x_P<1/4`. Later halting can change x_P from zero to a small positive value while preserving this strict conclusion. The pre-existing strict-release rule therefore has sufficient mathematical evidence now; a rule demanding exact zero requires a separate equality proof or continued withholding.

This is one unchanged query/rule per decision. It is not permission to replace the latter rule with the former. No empirical probability, harm interpretation or authority is derived from the scalar's construction.
