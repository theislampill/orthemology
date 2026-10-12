# Ordinary proof map: SCC elimination equals exhaustive maximal end components

The input is a finite retained pair set U, a source state for each pair, and a finite successor set for each pair. The observed-state type is finitely enumerated. Different pairs may have the same source. No transition probabilities or priorities are needed for this graph result.

A genuine end component E is nonempty; every used pair has nonempty successors; all successors are source states of E; and the graph enabled by E is strongly connected. These are the unchanged predecessor predicates.

## Preservation and stopping

The deletion test retains e only if its successor set is nonempty and every successor t remains a source of a retained pair and can reach source(e) in the current graph. The forward edge source(e)→t is supplied by e itself. Thus the test checks that all successors lie in its source SCC, with explicit source viability.

Suppose E is a genuine end component contained in current U. For e in E, its successors are nonempty. Every successor t is a source state of E, hence of U. Strong connectivity of E gives a path from t to source(e) using only E; monotonicity lifts that path to U. Therefore every pair of E passes the deletion test. This proves one-round preservation, and induction proves preservation through every iteration.

Every round filters its input. If it is not already fixed, its finite cardinality strictly decreases. Induction on the fuel shows that a number of rounds at least the initial pair count gives a fixed set K. Empty input gives empty output. The executable implementation uses exactly that conservative fuel; it does not rely on a convergence hypothesis or a numerically bounded priority range.

## Genuine components at stability

For any retained anchor pair a, let C_a be all pairs in K whose source is mutually reachable with source(a) in the K graph. The anchor belongs to C_a, so it is nonempty.

Stability means every pair in K passes the deletion test. For e in C_a and any successor t of e, there is a retained source pair f with source(f)=t. The paths source(a)→source(e)→t and t→source(e)→source(a) show that f lies in C_a. Thus C_a is successor-closed, and every used successor set is nonempty.

Strong connectivity must hold in the restricted C_a graph, not merely in K. Take a K-path between states s and t in the anchor SCC. Every intermediate state u is reachable from the anchor through s and can reach the anchor through the remainder of the path to t. Every used edge therefore has a source in the anchor SCC and is enabled by a pair of C_a. The entire path restricts to C_a. The Lean proof derives this by induction on reflexive-transitive reachability, retaining the endpoint return path as an explicit hypothesis. It does not postulate restricted strong connectivity.

## Maximality and completeness

Any end component F contained in K and containing the anchor pair has every used source mutually reachable with the anchor inside F and hence inside K. Consequently F is contained in C_a. This makes each C_a maximal among K-components.

Every original end component survives inside K and belongs to an anchor cluster. Conversely, a larger original end component extending a returned C_a would survive into K and contradict C_a's maximality there. Therefore the returned clusters are exactly the inclusion-maximal original end components. Finite image over the retained anchors returns all clusters and removes duplicates, without choosing an ordering or enumerating subsets.

This proves `mecs_eq_executable`, equality with the predecessor's independently defined exhaustive selector, for every finite input. In particular it handles source loss, SCC splitting after an escaping action disappears, multiple actions at one state, disconnected components and empty successor sets.

## Parity and normalized-row substitution

The new parity step computes the SCC-based component family once, then performs exactly the previous full-row matching and odd-minimum-layer deletion. Equality of the component selectors therefore gives equality of one step. Induction gives equality of every iterate, and the final output equality follows. All previously proved maximal-valid-component and target-state characterizations transfer through these equalities.

The normalized rational-kernel wrapper constructs exactly the same internal successors and zero-candidate-exit allowed-pair filter as its predecessor. Only the MEC implementation is replaced. The same full-row and supplied-licence boundaries remain. A live candidate is still required for the intended interpretation of internal support as candidate-positive support. No outer support recursion or stochastic policy theorem is added by this substitution.

The formal semantic equality and the ordinary polynomial operation count in `COST_ACCOUNT.md` are distinct claims. A fresh independent review is required before promoting this authored successor as independently accepted.
