# Shared proof cost and retained overlap information

9 October 2026. Bounded additive T20 research. Existing inputs remain unchanged. No integration, solver, performance claim, or T20 closure.

## Result first

For a fixed compatible bundle of valid proof DAG branches, once-per-node checking cost is exactly a weighted union of their paid-node footprints. The inherited basis-declared tensor interface represents every intersection cost by a diagonal multilinear contraction. Inclusion–exclusion then recovers the union cost exactly.

The useful discriminator is sharper than “overlap matters.” Three valid branches can have the same individual costs and every pairwise overlap cost, yet their combined checking costs are 3 and 4. Both bundles occur in one explicitly admitted acyclic rule grammar. The inherited parity example extends this to every fixed maximum order of retained intersection scalars.

This is an application of inherited fibre sufficiency, parity cancellation, and classical finite set identities. It does not discover a new tensor or information theorem. Full node-incidence vectors already retain enough information to compute union directly. Tensor notation supplies a precise alignment and summary-loss analysis; it supplies no faster evaluation or escape from the predecessor's synthesis hardness.

## 1. Inherited inputs and exact reuse

The actual local sources read were:

1. `t20-next-frontier-20261008/qualitative-tensor-transport/INHERITED_GRADED_INTERFACE.md`: the declared real typed tensor spaces and finite record channel in §§2–4; Theorem 4.2 and Corollary 4.3; all of §5; the contraction and basis qualifications in §6. Theorem 4.2 already proves that an observable factors through a summary exactly when it is constant on summary fibres. Theorem 5.1 already proves that even/odd parity laws have equal proper marginals. Neither theorem is new here.
2. `t20-next-frontier-20261008/qualitative-tensor-transport/RESULT.md`, especially §§1–2 and 5–6: already requires explicit alignment of domain identities across roles and distinguishes numerical contraction from Boolean truth. This report keeps real arithmetic and Boolean-valued inputs; it does not identify real addition with OR.
3. `t20-next-frontier-20261008/productive-identifiability/THEOREMS.md`, Theorem 2: already performs Boolean-lattice inversion of an incidence histogram and warns that an omitted summary coordinate remains recomputable if raw joint data are retained. The upper-set inversion below is the same standard mechanism with a different declared observable, not a new inversion theorem or a transport of that report's causal assumptions.
4. `certificate-compilation-boundary-20261009/RESULT.md`, §§2–4, and its actual `compiler.py`: define admitted finite rules, node-level charging, root-reachable acyclic witnesses, and the already proved failure of intermediate standalone-cost pruning.
5. `shared-proof-cost-boundary-20261009/RESULT.md`, complete report: already separates fixed-witness validation from cheapest shared-proof synthesis, with the exact Set Cover transport. This report does not repeat that reduction.

The specifically inspected packets do not already state this fixed-bundle intersection-summary discriminator. A bounded local text search for paid-node, union-cost, intersection-summary, and inclusion–exclusion references found no additional exact proof-cost application. This is not a programme-wide priority claim. The source hash bindings are in `INPUT_BINDINGS.json`; the general graded interface matches its predecessor's recorded SHA-256.

## 2. The proof bundle and its identity contract

Let D1,...,Db be supplied finite valid proof branches with globally aligned node identities. If the same identity occurs in two branches, it denotes the same rule application, local price, ordered premise references, and scope. Their union is required to be a compatible acyclic graph. Branches of one supplied valid parent DAG satisfy this requirement. Two arbitrary separately numbered witnesses do not satisfy it merely because their integer indices, judgement labels, or rule names happen to match.

Let N be a finite declared universe of possible paid-node identities, with weights w(v)>0. It may include available identities unused by the chosen bundle. Let Fi⊆N be exactly the positive-price nodes reachable from branch i. All zero-price nodes remain in the proof but need not appear in this cost view. Then

    C(F1,...,Fb) = Σ[v in union_i Fi] w(v).

If a parent root has its own positive price, add that price separately; alternatively include its footprint as another component. A parent root cannot already occur below itself in an acyclic proof. Shared zero-price structure changes neither expression. Empty footprints and an empty bundle have cost zero.

The extraction discards rule structure and evidence support because only this fixed-bundle cost is the target. It does not certify validity or preserve every provenance question. Validity must already have been checked against the admitted grammar. Shared evidence-token identity is also not the paid-node identity: repeated uses may share evidence while still occupy different charged nodes.

## 3. Exact contraction transport

For each branch role i use a copy Vi of the free real vector space on N, with declared basis e(i,v). Define

    xi = Σ[v in Fi] e(i,v).

The map from labelled footprint tuples to the tuple (x1,...,xb) is a bijection onto Boolean coefficient tuples: read the coefficient-one support in each role for its inverse. This is faithfulness at the footprint level, not at the full proof-graph level. It is already expressible in degree one of the inherited typed direct sum.

For a nonempty branch-index subset J define the covariant diagonal tensor

    Δ(J,w) = Σ[v in N] w(v) tensor_product[i in J] e*(i,v),
    m(J) = Δ(J,w)(tensor_product[i in J] xi)
         = Σ[v in N] w(v) product[i in J] 1[v in Fi]
         = weight(intersection[i in J] Fi).                 (1)

Take the branch factors in increasing index order. Distinct roles remain typed; the common v is supplied by the declared identity alignment. All off-diagonal choices vanish. This establishes both directions of the asserted numerical interpretation: the contraction computes the weighted intersection, and every intersection member contributes precisely its weight once to the contraction. Inherited multilinearity and contraction make (1) legitimate. The application-specific diagonal and the cost interpretation are declared here.

The weights occur once in Δ, not in every input vector. Using weighted xi in every factor would produce powers of w(v) and generally give the wrong intersection price. Arbitrary changes of basis require transforming the vectors and covariant tensors together; independently reusing the old diagonal after a basis change or node relabelling is invalid. Simultaneous node permutations with transported weights preserve the calculation.

For every Boolean tuple of incidences a1,...,ab,

    1[at least one ai=1] = 1 - product_i(1-ai)
                        = Σ[nonempty J] (-1)^(|J|+1) product[i in J] ai.

Multiplying by w(v) and summing over N proves

    C = Σ[nonempty J subset [b]] (-1)^(|J|+1) m(J).          (2)

This is weighted inclusion–exclusion. It gives an exact decoder of the full scalar intersection summary. The decoder is linear in the retained m-coordinates; union is not linear in the original incidence vectors.

### What the complete scalar record reconstructs

For each nonempty K⊆[b], let h(K) be the total weight of nodes belonging to exactly the branches in K. Then

    m(J) = Σ[K superset J] h(K),
    h(K) = Σ[J superset K] (-1)^(|J|-|K|) m(J).            (3)

Substitution proves the second identity: the coefficient on h(L) is the alternating sum over K⊆J⊆L, equal to 1 for L=K and 0 otherwise. Thus the maps are inverse at the level of nonempty weighted incidence histograms. Conversely, applying the forward map to the inverse gives the original m by the same cancellation. On realizable records the reconstructed h is nonnegative.

The full scalar record does not reconstruct individual node identities or proof edges in general. Identity recovery can hold with additional separating metadata: on a known inventory with weights 1,2,4,..., even each singleton cost uniquely determines its footprint by binary expansion. The reconstruction guarantee in (3) is at the weighted incidence-histogram level; stronger recovery depends on the declared inventory and weights.

Because N and w are known in the present interface, m(empty)=Σ_N w is available and h(empty)=m(empty)−C is recoverable too. If only the nonempty scalar record is retained and the total available weight is not known, that record alone leaves h(empty) undetermined. Neither the total nor h(empty) is needed for C=Σ[nonempty K] h(K). Arbitrary formal real m arrays need not be realizable with a prescribed node inventory and weights; invertibility is an algebraic statement and an exact statement on the realizable image.

This identifies exactly the claimed observable level in both directions. A single already-computed C is an even smaller sufficient summary for this one target; no minimality of the full intersection record is claimed.

## 4. Three branches with identical lower-order summaries

Use four available unit-price identities N={0,1,2,3}. Form two incidence tables whose rows are these node identities:

    identity     even table     odd table
       0            000           001
       1            011           010
       2            101           100
       3            110           111

Columns are the three branch footprints. Explicitly,

    even: F1={2,3}, F2={1,3}, F3={1,2};
    odd:  F1={2,3}, F2={1,3}, F3={0,3}.

Every individual cost is 2. Every pairwise intersection has cost 1. The available-node count and total available weight both equal 4. But the even triple intersection is empty while the odd triple intersection is {3}; therefore their union costs are respectively 3 and 4. Equation (2) reads 6−3+0=3 and 6−3+1=4.

The full first-order incidence vectors differ, as does the full third branch footprint. Retaining those vectors permits direct computation of both union costs. The failed representation is explicitly only the six scalars m({i}), m({i,j}), even if augmented by the known total available weight. It is not the collection of uncontracted vectors or full lower-order tensors.

### Actual realization in one admitted acyclic proof grammar

Introduce four scoped leaf judgements p0,...,p3, three branch judgements q1,q2,q3, and root t. Admit:

- For every v, the nullary rule concluding pv, with price 1.
- For q1, the zero-price rule with premises (p2,p3); for q2, the zero-price rule with premises (p1,p3).
- For q3, two zero-price rules, with premises (p1,p2) and (p0,p3), respectively.
- The single rule q1,q2,q3 ⇒ t, of price 0.

Every evidence support is empty. Dependency ranks are t above the qi above the pv. For either table, select its three branch rules, use one leaf node pv per used v, and point all branch references for that v at that same node. Add the root. The result is an admitted, correctly labelled, premise-first acyclic proof DAG with every stored node root-reachable. In the even certificate p0 is absent; it is an available grammar leaf, not an unreachable stored certificate node. The common grammar still has all four available leaf identities.

The complete certificates cost 3 and 4 under the unchanged predecessor `dag_value`. Each branch extracted as its own reachable sub-DAG is also valid and costs 2. Their global identity footprints are exactly the displayed Fi. There is no philosophical or hidden proof-admission premise beyond this explicit synthetic ground-rule contract.

The construction works for every finite tuple of footprint sets, with any assigned positive natural leaf weights under the written predecessor contract. Its actual executable price interface additionally accepts exact positive rational weights, which the weighted controls use. Any finite collection of such tuples on the same universe can be represented as alternative branch rules in one grammar. This is a realization into the admitted class; it does not say every tuple can be realized inside an independently fixed arbitrary grammar, or that arbitrary symbolic proofs may be merged by head label.

## 5. Exact transport of inherited parity

For b≥2 index N by the 2^(b−1) binary words a of length b−1, each with unit price. The first b−1 branch memberships are exactly the bits of a in both tables. The last membership is parity(a) for the even table, and 1−parity(a) for the odd table. Thus the first b−1 branch rules remain identical; only the final branch has two alternatives. These are bijections to the even and odd binary words of length b, respectively. Selecting a uniformly random available identity returns precisely the two probability tensors P+ and P− of inherited Theorem 5.1.

For every proper nonempty J⊊[b], either table has

    m(J) = 2^(b−|J|−1).                                   (4)

Indeed fix all coordinates in J to one; one parity condition on the remaining b−|J| coordinates leaves 2^(b−|J|−1) completions. More generally every proper joint incidence marginal agrees, exactly as the inherited augmentation-contraction proof states. Multiplying the probabilities by the common inventory size converts those inherited probability marginals into counts; reading the all-ones cell yields (4). Conversely, the full incidence-pattern count table divided by that size recovers the original parity law. Only the proper scalar intersection entries are retained in the failed summary, not the full law.

The zero word is in the even table only. Thus

    C_even = 2^(b−1)−1,       C_odd = 2^(b−1).

These tables are realized by the same two-alternative layered grammar construction in §4. Hence inherited Theorem 4.2 applies to actual valid proof bundles: the reduced intersection summary has one fibre containing two different costs. No decoder of all proper-order intersection scalars can always recover shared cost in this class. For any fixed cutoff r choose b>max(r,1), establishing the analogous failure for order at most r. This is an information-sufficiency statement, not a size or computational lower bound; the explicit parity inventories grow exponentially with b.

The target here is OR/union cost, not parity expectation. That change is justified by its different zero-word mass and the displayed cost calculation. It would be incorrect simply to quote the inherited parity-expectation result as if it already proved every other target differs.

## 6. Verification and stopping point

`check_overlap.py` imports the unchanged predecessor compiler with bytecode writes disabled. It checks admitted-rule membership separately because `dag_value` alone performs structural and price checks without checking an external rule list. It constructs and validates the two certificates and every branch sub-DAG for parity sizes 2 through 6; compares extracted global paid footprints with the declared tables; verifies all proper intersection summaries, union costs, and histogram round trips; and checks weighted, repeated, empty, and identity-misalignment controls. `CHECK_RESULTS.json` records the exact executed checks. These finite checks supplement the proofs; they do not establish unrestricted claims by enumeration.

The useful addition is the concrete cost-observable application and valid-proof realization of a lost higher-order overlap distinction. The general fibre, parity, contraction, and inversion mathematics is inherited. Directly traversing the paid-node union computes the fixed-bundle value without constructing 2^b intersection terms, and the retained degree-one incidence vectors suffice. The tensor description is useful only as an explicit account of what the proposed scalar compression forgets and which aligned contraction recovers it.

No optimal bundle is selected here. The predecessor's NP-completeness boundary for exact shared-proof synthesis remains unchanged; neither complete overlap tensors nor inclusion–exclusion removes that selection problem. The result does not extend reuse across incompatible contexts, authenticate evidence, model cache invalidation or actual processor runtime, transport causal or psychological warrants, or settle the source-warrant questions keeping T20 open. There is no further tensor or performance campaign warranted by this result.
