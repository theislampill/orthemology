# Exact cost and early failure

The original acceptance document remains unchanged as a provenance artifact. Its phrase “executes an expression in its exact syntax-derived number of work pops ... or returns ... fault” must be read with the following explicit success/failure distinction.

- On success, the machine performs the exact syntax-derived work-pop/tick cost and leaves one value above the unchanged prior values and pending tail.
- On failure, exception propagation stops immediately. The theorem preserves that earlier fault category and the actual visible step count. It does not execute remaining pops.

This is a wording clarification of the already accepted `expression_stack_exact` and `expression_success_ticks` statements. No theorem, source definition, accepted source byte, or failure behavior changes. The syntax-derived transition count supplied to `runSteps` is available fuel; an error short-circuits that recursive computation.
