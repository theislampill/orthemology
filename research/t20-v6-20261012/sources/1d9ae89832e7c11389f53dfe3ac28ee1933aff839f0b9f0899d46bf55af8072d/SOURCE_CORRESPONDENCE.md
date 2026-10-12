# P2 source map (draft before proof acceptance)

Pinned `prcodec.py`, SHA-256 dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c. This reviewed translation consumes accepted P1; it is not a checked Python frontend.

| Source | Intended model | Distinction retained |
|---|---|---|
| 161–163 | public input wrapper plus initial Config | Correct arity checked before nat argument conversion; initial meter.steps=0. Built-in list/tuple of exact nonnegative ints and exact Program/well-formed body form the semantic domain; custom Sequence/attribute behavior is excluded. |
| 163 | dictionary initialization, one statement task, empty events | Arguments stored without width checks; output register may be absent. |
| 164–165 | task work-list and tick-before-dispatch | A task is popped and the shared meter ticks before recognizing repeat/statement or testing a loop counter. |
| 166–171 | Task.repeat(r,count,k,body) | Captured count remains unchanged. If k<count, index is written before body, body precedes the next repeat; the final repeat comparison still costs a tick. No width check or trace event for the index write. |
| 172–175 | Set statement plus accepted P1 expression engine | RHS expression completes before dictionary assignment; only then append a trace event if trace is true. Source `if trace: append` is represented by appending the conditional singleton/empty list, an extensional list normalization with no cost claim about host allocation. |
| 176–177 | variadic Commands list, schedule | Reverse Python pushes correspond to head-top natural source order. Empty and singleton Seq nodes still cost their outer task tick even when lowering erases them. |
| 178–179 | Loop entry | Evaluate the bound once using the current dictionary and shared meter, then create repeat(r,count,0,body). |
| 180 | If | Accepted P1 value selects false branch exactly at zero; every positive natural is true. Exactly one branch is scheduled. |
| 181 | malformed statement rejection | Excluded from typed well-formed syntax. No arbitrary direct body safety theorem. |
| 182–183 | final observation projection | Missing output=0; existing output returned without a bit check. trace=False exposes scalar value; trace=True exposes (value,steps,assignment events). |

Internal model errors retain the failure tick as proof data, but run's public ResourceLimit exposes only exception class/message. Model task-fuel exhaustion is pending; it is never assigned a source semantic value. Source host exceptions outside P1's modeled resource checks remain unproved endpoints.

## Reused facts, not new evaluator credit

P1 supplies expression-stack execution, exact expression ticks and checked-width bounds. CodecStmt supplies variadic-to-binary sequence lowering semantics. The ordinary forward-iteration/runLoop identity is already in the Eighth abstract statement machine; a local supporting proof, if needed to keep the import closure small, receives no new Python-refinement credit. The new target is their composition with source-shaped variadic tasks, shared metering and traces.
