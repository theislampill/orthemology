# Independent review: cached proof checking and adaptive inquiry

11 October 2026 UTC. Reviewer-owned additive work only. No inherited or author source edits, repository action, publication, or Lean replay.

## Verdict

**The core mathematical transport is sound under its stated contracts.** The actual inherited normalizer exhibits static cost 14→12 while remaining checking cost rises 2→12; the cache-relative optimum is 1. The cache-cut reduction proves attained optimum and the stated bound on new checks. The postponement result is a sufficient commutation/dominance theorem, not an unrestricted adaptive optimality theorem. The finite-memory CIRS obstruction is valid and consistent with the actual unbounded-memory CIRS and Sixteenth constructions.

I found no blocking mathematical or executable defect. One small implementation-scope qualification is recorded below. This is a selected-source/interface review, not a whole-programme priority audit.

## Independent execution

- Reran all 19 author tests with ordinary Python and optimized `-O` Python, with bytecode writes disabled. Both pass. The earliest review rerun covered the then-present 11 cache tests; later runs cover the seven added policy tests and the added all-live dependency-profile test too.
- Reviewer-owned direct proof-object oracle: **3,200** comparisons, spanning 80 seeded grammars, eight leaf-cache subsets, and five exact-support requests. The oracle directly enumerates ordered pairs of concrete proof leaves and admitted roots; it does not use state refinement or the inherited whole-DAG compiler to calculate its expected answer. Cases include zero prices, ordered/nonmonotone guards, repeated child judgments, and exact-support restrictions. Every computed optimum agrees.
- Independently reject a cached terminal whose rule is withdrawn, a cached terminal whose guard is changed under the same rule name, and a forbidden nullary root guard. These are actual adapter calls, not only algebraic examples.
- Independently checked a three-state controller that restores disjoint good-action targets when observations identify the model deterministically; making both observations possible under both models gives each model a reachable absorbing wrong-action state. This confirms why full support is load-bearing in Proposition 3.
- Recomputed `(9/20,11/20)` and the pasted `3/4` using exact fractions. Credential-gating and early-discount examples in the independent output are declared small countermodels illustrating omitted assumptions; the author's suite additionally executes the credential transition search and finite scheduling optimizations.

Exact commands, exit codes, source hashes, reviewed author artifact hashes, and control outcomes are in `VERIFICATION.json`; the reviewer code and logs accompany it. Mechanical matching of every author binding does not imply every bound source was read in full.

## Findings

### 1. The negative transport genuinely executes the old normalizer

The imported `guarded_dag.py` is byte-identical to its bound inherited source. Its earliest representative for `q,{e}` is `qa`; its literal ordered-reference rewrite changes `rq(qb)` into `rq(qa)`. Fixed rule prices validate the static retained-occurrence argument, while immutable structural identity makes the rewritten parent a new check. The cached parent cannot be reused merely because its conclusion and evidence support agree. This is additional accounting, not a counterexample to PT-07's theorem.

The chosen cache `{qb,rq(qb)}` is dependency-closed. Original and normalized root states agree. The true marginal optimum's cost 1 and static cost 13 are independently rerun in the author suite. No negative price, illicit root, mutable cached child, or changed support is doing the work.

### 2. Cache-cut attainment and adapter are correct for the declared syntax

Forward cutting stops at cached nodes. Dependency closure makes every removed descendant cached, so the static charge of the cut graph equals the original marginal charge. Exact macro support preserves every ordered guard, including the root guard. Reverse expansion preserves admitted applications and cannot introduce a cycle: immutable cached terms do not acquire new dependencies, and newly built terms follow their children. Coincident terms can only reduce charge. The two inequalities, together with an attained finite macro-graph minimum, establish equality and attainment.

Applying PT-07 before expansion bounds macro-graph nodes. Expansion adds cached terms only, so the stated `|J| 2^|E|` bound is on newly checked nodes, not total expanded size. The adapter's Boolean exact-state saturation is not a scalar cheapest-child solver; it calls the inherited whole-graph enumerator and rechecks expanded admission/guards with the guarded checker.

The exact-state availability compression at one snapshot is valid for *optimizing some terminal proof*. It need not preserve remaining cost of a *specified immutable proof*. Reconstruction still needs one recoverable cached witness per selected state. This distinction prevents an unjustified universal minimal-memory claim.

### 3. Source-validity ceiling and a narrow helper limitation

`valid_node` checks the supplied grammar and inventory. It cannot authenticate a rule, discover a changed external interpretation, infer an omitted version dependency, or determine whether a historical receipt remains substantively warranted. The report expressly keeps these as application obligations. Changed rule records, changed guards, and changed inventory are handled correctly when supplied.

The antichain theorem is valid for the stipulated conjunctive contract `d(v)⊆L`, and it is coarsest for exact-state macro-availability observations over all L. It is not necessarily the coarsest terminal-cost quotient; the report correctly says so. Reactivation over later L requires retention of the archival witnesses/dependency profiles, not destructive deletion of every presently invalid record.

**Low-severity implementation qualification:** `dependency_frontier` takes local dependencies by `n.rule.name` and unions child factors. This represents rule-local dependencies, not arbitrary occurrence-specific dependency data attached to different executions of the same rule. The general §5 theorem is broader than that helper's input format. This does not undermine the theorem or the tested rule-withdrawal example. The author added an explicit qualification in §5; this review verifies the amended final text. No silent general source-revalidation implementation should be inferred.

### 4. Postponement is a sound pathwise theorem with substantial premises

Virtual simulation is lawful only because checks are guaranteed successful, non-informative, do not unlock acquisition, and do not alter timing, prices, evidence, or transition laws. Terminal reproducibility excludes lost entitlements and expired-only check opportunities. On a fixed public history and private random realization, each terminal noncached node has already been paid at least once by the original policy; delayed topological checking pays for it once. Nonnegative fixed prices and equal query histories give pathwise dominance.

The theorem does not require a finite-memory original policy. Its computation/reconstruction costs remain outside the charged objective. It preserves the declared terminal result, not every possible intermediate external deliverable or original proof identity. If terminal certificate identity itself is valued, that must be added to the objective and the final minimization restricted accordingly.

Exogenous revision can fit the commutation contract, but does not restore PT-02's persistent full-transcript-union feasibility test. This distinction is correctly preserved. Under each fixed hidden model, pathwise dominance implies expected dominance. It supplies no licence for branchwise worst-model replacement. ET-17 already owns the policy-vector repair and numerical fixture.

### 5. Finite-memory obstruction is sound; source representability is not a new controller audit

For a stationary finite-memory behavioral controller, common full-support observations make the reachable memory support graph common to all standards. Every reachable bottom component has positive hitting probability under each. A positively enabled recurrent action occurs infinitely often almost surely there. Hence its action support must lie in every good-action set; a common-good action is necessary. It is also sufficient via a constant controller. Model-independent fresh behavioral randomization does not avoid this argument. An uncounted clock, archive, growing integer, or correlated hidden persistent state violates the finite-memory premise.

The actual CIRS owner explicitly permits arbitrary memory and constructs exact likelihoods with growing bit lengths. The inspected Sixteenth reader explicitly reconstructs history/counts, has one policy before quantifying the actual model, and explicitly denies a finite-state conclusion. Thus there is no contradiction or novelty in merely noticing that a finite certificate can describe an unbounded-memory controller.

Clearing a common rational denominator preserves all likelihood comparisons exactly. Actual source declarations provide PR multiplication, zero choice, truncated subtraction, finite lookup, `PR.compile_has`, and `PR.compile_obs`. A finite argmax and bounded candidate pointer updates are representable using these interfaces. This is a valid ordinary representability deduction. It is **not** an executed Lean construction of this CIRS controller, a runtime bound, an actual-law composition theorem for the new source program, or a proof that a supplied observation stream satisfies CIRS. The report correctly leaves those obligations open.

## Ownership and read scope

Directly inspected:

- PT-07 complete owner and actual `guarded_dag.py`; inherited whole-DAG compiler; adapter and all author tests.
- PT-01/02 owner §§1–4, including its explicit terminal-checking/reuse exclusion; PT-03 relevant §§1–5, particularly its already-existing terminal DAG catalogue/inquiry transport.
- PT-06 owner portions establishing aligned footprint costs and its express cache-invalidation exclusion.
- ET-17 owner §§1–3 and nearby policy contract distinctions; no new credit assigned to its fixture or fixed-model method.
- Full CIRS owner; Sixteenth direct-controller reader §§1,4–13, with specific attention to actual-policy quantifiers and unbounded histories.
- Actual PR compiler typing/observation theorem declarations and relevant bodies; arithmetic/comparison declarations and denotation proofs; full finite lookup source.

The selected prior work already owns static exact-state attainment, terminal DAG/inquiry transport, fixed-model vectors, CIRS restoration, and actual Sixteenth controller extraction. The bounded addition is the cache-relative macro reduction, actual normalizer counterexample, and explicit check-postponement bridge. The source-revision frontier, finite-chain obstruction, and denominator clearing are correctly presented as specializations or standard reasoning. No exhaustive originality or independent historical priority claim is supported.

## Evidence ceiling

Accept as ordinary mathematical research with exact finite diagnostics. No new Lean certification, real source authentication, calibrated costs or likelihoods, scalable synthesis algorithm, deployed cache, full literal source controller, physical timing theorem, repository adoption, or overall T20 closure follows. The verification manifest binds the reviewed final snapshot, including the amended §5 helper limitation and plain-language handoff. Both author receipts were checked against every bound file. Six deliberate false-claim subprocesses (three claims, ordinary and optimized Python) all failed with their intended semantic marker. Later author edits require a currentness check.

## Final currentness correction

At 14:07 UTC, the author added only an effective-enumeration qualification after Theorem 1: decidable guards and exact computable price addition/comparison are needed for executable enumeration; arbitrary nonnegative real prices still admit the mathematical attainment result. Removing precisely that added sentence and its preceding space recovers the previously reviewed RESULT.md hash `fcd7ad6f6a2a07034592574d372d2dd618da081669912c413c1644d8af3e2988`. Every previously bound Python file is byte-identical. This is a correct clarification already supported by PT-07, with no changed scientific verdict.

The accepted current RESULT.md hash is `77ea55a74bc79c9810cac1588693c7681c1403aa0606081c955d314d2222a890`. The reviewer reran all 19 tests in both modes and the six intended-failure subprocesses, and refreshed the bindings against both regenerated author receipts. Optional assembly navigation files do not extend this scientific acceptance.
