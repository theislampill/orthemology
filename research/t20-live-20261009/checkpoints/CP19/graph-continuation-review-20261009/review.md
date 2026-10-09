# Independent review: graph-restricted unary continuation masks

Date: 2026-10-09. This review does not alter any inherited source files.

## Verdict

The proposed minimum-step formula is correct for a nonempty target mask, undirected simple graph, both gate orientations, and a freely chosen starting singleton. The stated lower-bound argument works, including when the initial singleton lies outside the final mask. The pruning construction also works.

The main presentation corrections are to distinguish the raw continuation span from its constant augmentation, state the horizon convention, and avoid novelty claims about the Steiner/CNOT synthesis formula itself.

## Prior-art boundary

Vandaele, Martiel, and Goubault de Brugière, *Phase polynomials synthesis algorithms for NISQ architectures and beyond*, arXiv:2104.00934, Section 4.1, PDF page 10, explicitly gives the same cost `2|V_T|−|S|−1`, obtained by filling Steiner nodes and then eliminating along a tree. This is the same reversible parity-mask problem, with the direction reversed. The continuation-space and continuous-law compression interpretation may be the relevant application; the underlying formula and construction should be cited as known. The present lower bound supplies a self-contained global-optimality proof, not a basis for asserting new priority.

Source: https://arxiv.org/pdf/2104.00934#page=10

## Precise statement

Let `G=(V,E)` be finite, simple, and undirected. For each edge `{i,j}`, both ordered updates `F_ij`, with `(F_ij(x))_i=x_i x_j` and other coordinates unchanged, are available. Write `χ_S(x)=∏_{v∈S} x_v`.

Then

`χ_S ∘ F_ij = χ_(S Δ {j})` if `i∈S`, and `χ_S` otherwise.

For nonempty `S⊆V`, let `τ_G(S)` be the minimum cardinality of a vertex set `U⊇S` for which `G[U]` is connected, with infinity when no such set exists. Let `d_G(S)` be the minimum number of mask transitions needed from any singleton to `S`. Then

`d_G(S)=2τ_G(S)−|S|−1`,

with infinite cost when `τ_G(S)=∞`.

The minimum is over starting coordinates as well as gate sequences. If the initial singleton is fixed at `r`, the stronger statement is

`d_(G,r)(S)=2τ_G(S∪{r})−|S|−1`.

Neither statement applies to `S=∅`: no allowed sequence maps a nonzero mask to zero. Every gate is an invertible linear transvection on the binary mask vector.

## Complete proof of the freely chosen root formula

Consider a mask path `A_0={r}, A_1,…,A_L=S`. Let `U=⋃_t A_t`.

Every first appearance of a vertex `j≠r` results from toggling it using a currently active adjacent vertex. It therefore attaches to the previously visited set. Consequently `G[U]` is connected and `|U|≥τ_G(S)`.

If `r∈S`, each vertex in `S\{r}` must be toggled at least once; each vertex in `U\S` must be toggled at least twice. Thus

`L ≥ (|S|−1)+2(|U|−|S|)=2|U|−|S|−1`.

If `r∉S`, every vertex of `S` must be toggled at least once, the initial vertex `r` must be toggled at least once to remove it, and every vertex in `U\(S∪{r})` must be toggled at least twice. Thus

`L ≥ |S|+1+2(|U|−|S|−1)=2|U|−|S|−1`.

Steps whose source is absent do not change the mask and only increase `L`, so they do not weaken the lower bound.

For the upper bound, choose a minimum connected superset `U` and any spanning tree of `G[U]`, rooted at a vertex `r∈S`. Activate vertices in parent-before-child order. This takes `|U|−1` steps. Then remove precisely the vertices of `U\S`, deepest first, by toggling each from its tree parent. The parent remains active because it is shallower and has either not yet been removed or belongs to `S`. This takes `|U|−|S|` further steps, ending at `S`. The total matches the lower bound.

For a fixed root outside `S`, activate a spanning tree of a minimum connected set containing `S∪{r}` from `r`; then reroot that same fully active tree at any `s∈S` and remove all vertices outside `S` in decreasing depth. The same count proves the fixed-root formula.

Gate sequences used as pullbacks reverse the chronological ordering of physical state updates. Since every ordered gate remains available and the length is unchanged, this creates no obstruction.

## Continuation space and minimal continuous encoding dimension

For a nonnegative integer horizon `h`, define

`R_h={S⊆V : S≠∅ and d_G(S)≤h}`.

The raw real span of unary continuation pullbacks is

`W_h=span{χ_S : S∈R_h}`.

The constant belongs to none of these raw spans. The augmented space is

`V_h=span({1}∪{χ_S : S∈R_h})`.

Walsh characters are linearly independent, so `dim W_h=|R_h|` and `dim V_h=1+|R_h|`.

On the full probability simplex on `{−1,+1}^V`, the least number of real coordinates of a continuous exact sufficient encoder for all these expectations is `|R_h|`. This is `dim V_h−1`, or equivalently `dim W_h`; subtracting one from the raw span would be wrong.

A direct lower-bound proof avoids ambiguity about the inherited theorem. Let `q=|R_h|`, and for real vectors `a` with `Σ_S |a_S|<1` define

`p_a(x)=2^(−|V|)(1+Σ_(S∈R_h) a_S χ_S(x))`.

These are strictly positive probability laws, and Walsh orthogonality gives `E_(p_a)[χ_S]=a_S`. Any continuous sufficient encoder must be injective on this continuously parametrized open `q`-ball. It cannot map injectively and continuously into `R^d` for `d<q` (invariance of domain, after padding the target with zero coordinates). The `q` moments themselves achieve dimension `q`. No continuity of the decoders is needed for this argument. For `q=0`, the result is immediate.

This result concerns exact expectations of the specified scalar observables. If the task instead requests the joint law of all terminal coordinates, arbitrary nonlinear terminal observables, state-dependent hidden control, or a different law class, the conclusion needs reanalysis. In particular, a simultaneous full-state joint observation at horizon zero already identifies the entire law.

## Horizon and model boundaries

- “Up to `h` elementary updates” is the clean convention.
- If `E` is nonempty, the exactly-`h` family agrees with the up-to-`h` family: at the initial singleton `{r}`, choose any graph edge and orient it with source different from `r`. That source is inactive, so the corresponding mask transition is a self-loop. Repeat it to pad to any larger length. It need not be an identity map on the underlying state; it is an identity on the current pullback character.
- If `E` is empty and there is no explicit identity command, no positive-length word exists. Then the exactly-`h` family for positive `h` is empty. State an up-to convention or add an identity command if these cases should retain the unaries.
- Finite-horizon sufficiency is not automatically a fixed, time-homogeneous update-closed statistic: `F* W_(h−1)⊆W_h`, whereas `F* W_h⊆W_h` can fail. A remaining-horizon hierarchy is valid; if the intended theorem instead requires the same statistic to update exactly forever, use the invariant saturated space.
- Parallel gate layers have a different cost from sequential elementary gates.
- One-way directed gates, reset gates, duplicated slots, self-loops, state-dependent control, or noisy gates can invalidate the formula.
- Minimal connected superset means vertex cardinality. In the unweighted setting a spanning tree of that set has `τ−1` edges. Do not substitute an unrelated weighted Steiner objective.
- If there are no slots, the raw space is zero-dimensional, the augmented space consists of constants, and the law simplex is a point.

## Disconnected saturation

A mask started in one connected component remains within it. Conversely, every nonempty subset of a component has finite cost. Thus for components `C`,

`W_∞=span{χ_S : ∅≠S⊆C for some component C}`,

`dim V_∞=1+Σ_C(2^|C|−1)`,

and the minimal continuous encoding dimension is `Σ_C(2^|C|−1)`.

Equivalently, the saturated augmented observables are the functions `a_0+Σ_C f_C(x_C)`. Two laws are indistinguishable exactly when all their component marginal laws agree. The initial law need not factorize: cross-component dependence remains invisible to these observables. Every tuple of component marginals is attainable, for example via its product law.

## Sharp examples and additional corollaries

### Complete graph

`τ(S)=|S|`, so `d(S)=|S|−1` and

`dim V_h=Σ_(k=0)^min(n,h+1) binom(n,k)`.

### Path

Number the vertices consecutively. For nonempty `S`, its Steiner hull is the interval from `min S` to `max S`. If that interval has `L` vertices and `|S|=k`, then `d(S)=2L−k−1`.

For `n≥2`, the endpoint pair has cost `2n−3`, which is the saturation horizon. The full mask costs only `n−1`; larger cardinality need not mean greater synthesis cost.

A closed finite-horizon count is

`dim V_h = 1+n+Σ_(L=2)^n (n−L+1) Σ_(k=max(2,2L−h−1))^L binom(L−2,k−2)`,

where an inner sum with lower endpoint greater than its upper endpoint is zero.

For `P4`, augmented dimensions at `h=0,1,2,3,4,5` are `5,8,10,13,15,16`.

### Star

For a mask containing the center, cost is `|S|−1`. A singleton leaf has cost zero. A mask consisting of `k≥2` leaves costs `k+1`. For `K_(1,3)`, augmented dimensions at `h=0,1,2,3,4` are `5,8,11,15,16`.

### Any tree: exact saturation time

If a tree `T` has `n≥2` vertices and `ℓ(T)` leaves, its saturation horizon is

`h_sat(T)=2n−ℓ(T)−1`.

Proof: For a target with at least two vertices, let `H` be its hull. Every leaf of `H` lies in `S`, so its cost is at most `2|V(H)|−ℓ(H)−1`. Extend `H` one adjacent vertex at a time to `T`. Each extension increases this expression by either one or two, so it is at most `2n−ℓ(T)−1`. Taking `S` to be all leaves of `T` attains equality. Singleton masks have zero cost.

For every connected graph on `n≥2` vertices the simpler universal upper bound `h_sat≤2n−3` follows at once; paths attain it.

### Two disjoint edges

The saturated augmented dimension is `1+3+3=7`; continuous encoding needs six coordinates. Any cross-component pair mask is unreachable, even though either within-edge pair takes one step.

## Exhaustive verification

`verify_formula.py` independently computes gate-graph shortest paths by breadth-first search, and computes `τ` by direct induced-subgraph connectivity plus a minimum-over-supersets transform. It compares all nonempty masks on every labelled simple graph with one through six vertices.

Results:

- 33,867 labelled graphs checked.
- 2,097,151 nonempty graph–mask pairs checked.
- No discrepancy.
- Zero mask was never reachable.
- Fixed-root formula separately checked for all vertices, all masks, and every labelled graph through five vertices, with no discrepancy.
- Runtime in this environment was 3.254 seconds.
- The tree saturation corollary was additionally checked on all 1,441 labelled trees with two through six vertices, with the leaf mask attaining the largest distance in every case.

The raw results are in `test_results.json`. Concrete distance arrays and dimension profiles are in `sharp_examples.json`.

These checks support the proof and are not a substitute for it. The identity, dimensional claims, and tree saturation proof above are independently stated so that the deliverable does not depend on the test implementation.
