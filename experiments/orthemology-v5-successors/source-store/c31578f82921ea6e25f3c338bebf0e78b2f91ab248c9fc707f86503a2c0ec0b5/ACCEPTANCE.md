# Independent P1 acceptance: expression-stack algorithm correspondence

**Disposition: PASS, within the stated expression-only scope.**

Accepted source packet: `P1_v3`, manifest SHA-256 `d0177de1ebeb8de4ff71898dbccc729ca420c70a50c307f1bacccd6d2c38d43d`. The exact Python source is `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c` and matches the separate inherited literal snapshot. The 118 manifest-bound payloads were verified.

## Accepted mathematical result

Four source-shaped Lean modules establish the following for every admitted finite expression, finite natural dictionary, optional natural budgets and natural starting step count:

1. Default-zero dictionary read and overwrite agree extensionally with the semantic store.
2. The `(expression, ready)` work-stack machine executes an expression in its exact syntax-derived number of work pops. Under arbitrary pending work and preexisting natural values, it leaves one value above the unchanged prior value stack and the untouched pending tail, or returns exactly the recursive reference's modeled fault category and visible step count.
3. Successful complete evaluation equals `ObserverCore.evalExpr` and increases the meter by the expression cost: one tick for leaves; two plus child costs for compounds.
4. The admitted initial state cannot produce a value-pop underflow or final singleton-invariant fault. Only the three modeled resource-fault categories remain.
5. Explicit input-dependent finite step and checked-width bounds suffice in the ideal model. Register reads require no width allowance. Any two successful budget settings agree on the value; continued-success monotonicity under budget changes is not claimed.

These results concern a manually defined mathematical algorithm model. Rule-by-rule source review and exact AST-shape binding connect that model to the pinned implementation as reviewed correspondence, not as a verified Python frontend theorem.

## Independent verification

- Cold compilation of the copied `ObserverCore` dependency and all four scientific modules, using only independently produced custom objects and the restored pinned official dependency cache.
- Exact theorem census: 37 public theorems and one private dictionary lemma. All 37 public axiom readbacks use only standard Lean axioms; no admitted proof or custom axiom was found.
- Successful replay of 21 author Lean controls and four reviewer universal consumer theorems plus 28 reviewer concrete controls.
- Four deliberate machine mutations rejected at the intended universal stack proof: operand reversal, omitted ready ticks, checked variable reads and generic power postchecking.
- 266,760 independent recursive-oracle comparisons against the literal Python expression implementation, including exact modeled failure messages and meter counts; 1,593 separately instrumented pending-tail/value-stack cases; 18 detected behavioral source mutations.
- All 28 valid-domain executable source lines exercised; excluded malformed branches separately observed to establish the domain boundary. Author source-shape controls and all 26 bounded Python edge controls also replayed successfully.
- Fresh verification of all 5,065 compiler-distribution entries, 6,816 source records and 34,230 cache entries. The only allowed differences are the five documented cache-utility trace-path relocations. No proof object difference, extra cache entry or missing cache entry was accepted.

All Lean runs were sequential `-j1`, with default heartbeat settings and a 180-second per-module wall bound. No historical whole-program timeout probe was rerun, and no timeout was used as negative-control evidence.

The cold-compiled packet was v2. The v3 delta was checked exactly: one README paragraph plus three dependency-provenance documents; every Lean/Python/reference/control source byte is identical. The source-bound compilation evidence therefore applies unchanged to v3.

## Source-sensitive boundaries retained

- Every popped work item ticks before tag dispatch, including ready visits. Failure on a tick retains the incremented count.
- Constants and binary results receive generic width checks. Initial argument values, variable reads, loop-index writes and final output lookup are not globally bounded by `max_bits`.
- Binary children execute left then right; reduction pops right then left. Natural subtraction saturates; division by zero returns zero; modulo by zero returns its numerator.
- Power checks exponent+1 before shifting, produces the distinct exponent-storage fault and has no generic postcheck. Other arithmetic is computed before its result-width check.
- Well-formedness and exact built-in-natural input requirements are preconditions, not validation supplied by `Meter` or `eval_expr`. Booleans, int subclasses, negative values, custom dictionaries and malformed direct tuples remain outside the correspondence.

## Unclosed endpoints

Python tuple decoding/frontend extraction, Python built-in arithmetic/list/dictionary semantics, faithful CPython execution, allocation/time/OS failures, parser and serializer behavior, statements and repeat tasks, complete `run`, trace/wrapper behavior, arbitrary malformed direct ASTs and a fixed finite all-input budget remain outside this result. Finite controls and AST checks do not replace a universal frontend proof. P2/P3 are separate gated work; this acceptance neither authorizes nor claims them.

No mathematical gap was found inside the accepted scope. This is milestone acceptance evidence, not completion of the wider runtime gap or the research tranche.
