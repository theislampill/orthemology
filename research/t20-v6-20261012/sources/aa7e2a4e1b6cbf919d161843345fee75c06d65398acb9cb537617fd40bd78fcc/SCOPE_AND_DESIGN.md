# SCC-based maximal end-component selector

Root approved this bounded isolated successor on 2026-10-01 at 16:25 UTC. All predecessor proof bytes and the independent review remain unchanged.

The computational graph selector repeatedly removes a pair if its successor set is empty, if a successor has no retained source pair, or if that successor cannot reach the pair's source in the current pair graph. Forward reachability is automatic from the pair's own edge, so this is exactly the source-SCC containment test with explicit source viability. Recompute after every round; finite cardinal descent gives a bound by the initial retained-pair count.

At stability, collect all retained pairs whose source belongs to the same SCC as a retained anchor pair. Prove these sets are nonempty closed strongly connected end components by deriving that a path between SCC states can be restricted to pairs in that SCC. Every original end component survives every deletion, and all its pairs belong to one final cluster. These facts yield exact equality with the independently defined maximal-component family and with the existing exhaustive executable selector.

Only after that equality is proved will the SCC selector replace the powerset selector in parity deletion. The parity target and normalized-row interfaces must retain the same full-row matching, live-candidate, zero-exit and supplied-allowed-pair boundaries.

The code must contain no powerset enumeration in the new computational definitions. A separate explicit finite-operation cost account will justify any polynomial claim; kernel equivalence, executable checks and bit-cost scope will remain separate. No stochastic iff or licensing recursion is inferred from this selector.

Tests will include empty successors, escaping actions, disconnected SCCs, source-loss cascades, retained higher odd priorities, rematching after deletion, all-odd fuel boundaries, and comparison with the exhaustive reference. Public type/axiom readbacks and a fresh source-only replay are required before freezing. The new author will not label its own successor independently reviewed.
