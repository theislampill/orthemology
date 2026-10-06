# P1 source-to-model correspondence map

This map binds a reviewed algorithm translation. It does **not** certify a Python frontend, CPython or operating-system execution.

Source: the pinned `prcodec.py` in `P1_SCOPE.md` (also byte-identical in the independent review snapshot).

| Python source | Model declaration/rule | Exact observation and residual primitive |
|---|---|---|
| 123–129 `Meter`, `steps += 1`, strict `steps > limit` | `Meter`, `tick` | Exact built-in nonnegative-int starting steps and optional such limits; count increments even when tick raises. `Failure.steps` preserves the visible mutated count. Python exact-int addition/comparison are primitive assumptions. |
| 130–132 `check`, `x.bit_length() > max_bits` | `check`, `Nat.size` | Constant or binary result fails with integer-storage fault at current count. Bit length for natural Python ints is interpreted by `Nat.size`. This does not bound all dictionary values. |
| 134–137 initial stacks, `.pop()`, tick-before-tag | `Config`, `step`, `expression` | Head-top Lean lists correspond to end-top Python lists. A popped work item is metered before any tag check. Local work/value lists are not exposed on failure. |
| 138 constants | `.constant` rule | Check literal width then push; even an internal ready=true constant is handled as a leaf. |
| 139 `regs.get(r,0)` | `dictionaryRead`, `.reg` rule | Missing keys give zero, existing values are returned with no bit check. Exact built-in dict lookup is the source primitive. |
| 140–143 push-ready, reversed child pushes | compound ready=false rules | unary pushes child then ready; binary head-top order is left child, right child, ready. Each compound has two ticks. Finite immutable well-formed tuples exclude unknown tags/arity/cycles. |
| 144–147 `pow2`, pop, exponent guard, `1<<a` | compound ready=true power rule, `power`, `power_width` | Pop one; test a+1 BEFORE allocation. Exponent-storage fault is not integer-storage fault. No generic postcheck. Natural shift identity is the primitive interpretation. |
| 148 pop b, then a | binary ready=true rule | Top two values are bv then av; operation receives av,bv. Empty/short stacks correspond to Python IndexError; modeled distinctly as `valueStackUnderflow`. Such faults are unreachable from valid initial expression states. |
| 149–155 arithmetic | `Binary`, `binaryValue`, `binaryValue_correct` | exact natural +,*; max(0,a-b); divisor-zero division=0 and modulo=a; `int(comparison)` yields 0/1; operands must be exact nonnegative ints, not bool/user objects. |
| 156 unknown operation | excluded by `PyExpr` constructors | No theorem about arbitrary direct malformed tuples. The source may raise InvalidCode, IndexError, TypeError or ValueError on those inputs. |
| 157 result check | binary check rule | Arithmetic happens before `check`; host allocation may fail before a modeled width rejection. |
| 158–159 singleton result invariant | `expression` final check | On valid domain the universal local stack theorem leaves exactly one value. Stack underflow and final `InvalidCode` are distinct kinds in the model. |
| 163, 169, 174, 182 input dictionary, writes, final lookup | dictionary representation/read/write lemmas only | List representation erases old entries on overwrite; only extensional lookup is observed. P1 does not prove complete `run`, input initialization, loop execution, trace events or output lookup. |

## Intentionally excluded outcomes

- Direct `Program` bodies are not recursively validated by `__post_init__` (45–46), which validates arity/output only. Raw negative/Boolean constants or malformed tuples are outside this theorem.
- `run` checks argument arity then applies strict `nat` to argument values. It does not check initial argument widths. Loop-index writes, variable reads and final lookups do not check widths.
- `decode_bytes` requires a bytes object, checks magic, rejects invalid syntax/trailing bytes, and wraps RecursionError as ResourceLimit. `decode` strictly validates natural indices. P1 does not prove either parser.
- Parser/serializer ResourceLimit is different from syntax rejection. MemoryError, other host failures and OS interruption are not generally caught or represented as a semantic zero.
- `evaluate_index` returns zero for invalid syntax or wrong arity before n/word validation. Valid binary inputs propagate execution exceptions. Passing trace=True changes run's result shape and causes the wrapper's `%2` to fail. P1 proves neither wrapper.
- Negative or Boolean budgets, subclasses/custom numeric objects, mutated/custom dictionaries, callbacks and concurrent mutation are not part of the valid meter/input domain.

## Remaining trusted endpoints

The correspondence assumes the specified interpretation of exact built-in nonnegative integers, tuples, lists and dictionaries, plus faithful execution of the pinned Python control flow when no host failure occurs. The AST checker is an identity/control-flow drift detector only. It is not a verified translator and supplies no universal semantic proof by itself. Finite controls corroborate branch sensitivity and never replace the universal Lean theorem.
