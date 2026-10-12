# Cost account for the SCC-based executable replacement

This is an **ordinary source-level operation-count argument**, separate from the kernel proof of semantic equality. No Lean theorem about machine time, allocation, compiler output or bit-cost semantics is claimed. The new computational definitions contain no powerset enumeration.

## 1. Input and cost model

Let n be the number of enumerated states, m the size of the initially supplied pair set U, and k the size of the live-model set B. The ordinary finite-table complexity claim requires concrete finite enumerations and computable equality, source, successor, row and priority accessors. Arbitrarily expensive caller-supplied Lean functions or decision instances have no uniform time guarantee just from their types.

First treat states and pairs as atomic identifiers, the source map and successor lists as explicit tables, and a row-equality/priority-operation cost as a parameter C. Scanning a list of length l takes O(l) steps. Membership, filter and image use their finite list representations. Duplicate removal and comparison of two sets of size at most l admit O(l^2) atomic equality bounds; no permutation enumeration is required.

The pinned library definitions used in this accounting are `Finset.biUnion` in Mathlib/Data/Finset/Union.lean, which binds the finite lists and then deduplicates, and the List.isPerm-based permutation decision in Lean Init/Data/List/Perm.lean. These are the same Lean 4.19.0 / Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b dependencies used by the proof replay. The bounds below intentionally allow quadratic deduplication of raw concatenated lists rather than relying on a faster set representation.

## 2. Verified finite reachability

`FiniteReachability.reachable` performs n forward-closure rounds. Each reached set has at most n states. One edge query scans at most m pairs and may scan a successor list of at most n states, hence costs O(m(n+1)).

One closure round performs at most n^2 such edge queries. Its union has at most n^2 raw entries before deduplication; allowing quadratic deduplication costs O(n^4). The other state-set union and membership costs are smaller. Thus one reachability computation is conservatively

    R(n,m) = O((n+1)^5 (m+1)).

The cardinal/finite-closure correctness theorem does not itself assert this cost bound. The bound comes from the explicit finite loops and the list-operation model just stated.

## 3. SCC deletion and final clusters

A deletion round scans at most m pairs. Each pair has at most n successors. For each successor, it checks source viability and one reverse reachability query. Even recomputing `usedStates` each time costs at most O(m^2) by the image/dedup bound. Hence one deletion round is at most

    O((m+1)^3 (n+1)^6).

There are exactly m fuel iterations in the current executable definition, even if stability occurs earlier. Each is bounded using the original m; the formal subset invariant ensures no later pair set is larger. The resulting deletion cost is O((m+1)^4 (n+1)^6).

The final algorithm forms at most m clusters. Each cluster filters at most m pairs, with two reachability computations per pair. Deduplicating the list of at most m resulting pair sets permits O(m^2) set comparisons, each of cost O(m^2). This fits the same bound. Therefore the complete SCC-based MEC selector has conservative graph-table operation count

    G(n,m) = O((m+1)^4 (n+1)^6).

This is not an optimized Tarjan implementation and no tight exponent is claimed. The point is that all loops and intermediate families are polynomially bounded. The formal `mecs_card_le` theorem additionally verifies that the returned family has at most m members.

## 4. Parity pruning using the new selector

`parityStep` binds the newly computed component family once and reuses it in the odd-layer test. There are at most m components, each of size at most m. Testing one pair against every component and every live model costs at most O(m^2(k+1)(C+1)), where C bounds a full-row equality and a scalar priority lookup/comparison/parity operation. Over all pairs this is O(m^3(k+1)(C+1)). Forming and deduplicating the component union costs at most O(m^4).

There are m outer parity iterations and one final MEC call. Thus a conservative complete parity-output bound is

    O((m+1)^5 (n+1)^6 + (m+1)^4 (k+1)(C+1)).

The implementation never loops through all integers below a priority. Only comparisons, the witnessed minimum test and reduction modulo two are used. Priority magnitudes affect scalar operation costs, not the number of deletion rounds.

## 5. Normalized rational-table wrapper

The normalized wrapper does not precompute/cache every internal successor list. A query to `internalSuccessors` scans at most n successor states and k live models. If a scalar table access, exact rational sign/equality test, identifier comparison and binary-priority operation costs at most a, this derived-successor query costs O((n+1)(k+1)a). A full-row equality costs O((n+1)a).

Multiplying the graph-call accounting by the derived-successor/query cost, and including the initial zero-exit filter, yields the deliberately loose bound

    O((m+1)^5 (n+1)^7 (k+1)(a+1)).

For explicitly stored finite rational tables and binary priorities, a is polynomial in their explicit representation size; arrays or finite lists both supply such a bound. Consequently this particular finite-table specialization is polynomial in the full explicit input size. This is not a uniform polynomial bound for arbitrary function-valued kernel presentations or arbitrary equality oracles.

## 6. Evidence boundary

The kernel proves exact equality of the SCC selector, the exhaustive selector, the parity outputs and the normalized target predicates. Native finite tests compare the implementation with exhaustive independent predicates. This note supplies the ordinary operation-count argument. None of those three evidence forms is relabelled as another. A formal cost semantics, sharper complexity bound, low-level performance qualification, outer support-recursion implementation and stochastic policy theorem remain separate work.
