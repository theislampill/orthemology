# Statement-to-semantics audit map

## Actual stream/sample space

`state M s x n` is the state after exactly n input bits. `output M s x n` emits using that state and x(n). `state_prefix` and `output_prefix` prove agreement with the predecessor literal list execution. `output_measurable` proves the map measurable; `law` is the pushforward of the actual infinite product.

## Cardinality-to-measure

`pref` is a literal finite-coordinate list. `cylinder` tests equality of that list. `cylinder_prefix` is exactly the finite coordinate Set.pi cylinder used by Q8Measure. `measure_cylinder` handles arbitrary finite words by an explicit false-tail extension. `blocks` parses x(kL+i); `flatten_blocks` identifies its flattened input with the first jL actual coordinates. `flattenBlocks_injective_of_length` excludes collisions, including the harmless L=0 edge case at a fixed block count. `measure_block_event` uses genuine disjointness, not just a union upper bound.

## Finite and infinite avoidance

`blocks_mem_surviving_finite` proves that finite matching plus a non-D endpoint gives an actually accepted block word in the existing state-dependent language. Earlier entry into D is impossible by transition closure. `finite_survivor_measure_bound` combines the exact event measure with the existing sharp cardinality bound. `avoidMatch_null` uses the true ENNReal geometric convergence theorem. It does not assume an infinite-limit/counting correspondence.

## Atomic mass

`hitting_prefix_determines_output` splits at the actual hit time and proves equal output from every stream sharing that prefix, using the universal-input D relation. `hits_output_positive` uses that prefix's positive cylinder measure. `positive_avoiding_null` takes a countable union over actual positive singleton atoms. `atomic_mass_eq_hitting_probability` is equality of genuine measures and P02A2's positive-singleton mass, not a newly defined proxy.

## Infinite-horizon rationality

`card_hittingBlocks_succ` uses the finite tuple head/tail equivalence, establishing the fair first-bit recurrence from actual input words. `hittingProbabilityQ_tendsto` uses monotone event continuity and ENNReal.toReal at a finite probability. `hittingReal_harmonic` follows by uniqueness of limits. Boundary1 on D and boundary0 on non-reaching states are derived from the actual hitting event.

`homogeneous_nonpos` takes a real or rational global maximum. If it is positive, it is neither in D nor in a non-reaching component. The strictly positive transition weights force both successors to preserve it; propagation along the state's literal finite word to D contradicts boundary0. Applying this to f and −f proves homogeneous uniqueness. `hittingSystem_injective` therefore derives, rather than assumes, invertibility. `exists_rational_solution` uses finite dimension over ℚ; `rational_hitting_probability` proves its real cast equals the actual law's solution. No computable inverse is claimed in the sealed first stage.

## Nonvacuity

`zero_atomic_mass_one` checks a one-state constant-output machine; `copy_atomic_mass_zero` checks a one-state input-copying machine; `split_atomic_mass_half` checks a three-state machine whose first fair input selects a deterministic-output sink or a fresh-bit-copying sink. These are kernel theorems about the actual output law, not finite cardinality examples alone.

All finite-state main theorems have explicit finite/nonempty premises and a supplied initial state. Their conclusions cannot be obtained from an empty state type. The generic product-cylinder lemmas correctly include empty prefixes.
