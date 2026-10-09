# Finite interior calibration is governed by support-incidence rank

8 October 2026 UTC. New mathematical sibling, preserving interaction-calibration-anchor and the other frozen stages. This result concerns a fixed finite unguarded independent-route inventory and finitely sampled calibration values. It does not identify whole functions between samples, discover an unknown support pattern, provide a statistical sampling algorithm, certify physical architecture, or authorize integration or T20 closure.

## 1. Observation model and input contract

Use the predecessor's one-effect response law

Q(x)=product_(S in E) [1-product_(i in S) r_i(x_i)]^(n_S).

The positive-support set E is known and complete, and each n_S is a known positive integer. Unlisted supports are known absent in this theorem; absence is an input, not inferred from approximate values. Each r_i is one continuous strictly increasing endpoint-preserving homeomorphism of [0,1], shared across all occurrences and supports containing i. Distinct route occurrences are independent under the stated support-product success law. There are no guards, latent mixtures or cross-coordinate calibration effects.

Let V be the union of the supports in E. Unused root coordinates outside V have no endpoint information, not even sampled ratios, and are excluded from the rank count. Choose for every i in V finitely many interior commands

0<x_(i,1)<...<x_(i,m_i)<1, m_i>=2,

with the first as reference. Write z_(i,l)=r_i(x_(i,l)), u_i=z_(i,1). The finite interior observation alphabet is {0,x_(i,1),...,x_(i,m_i)} for each root. Zero masks are allowed; **unit commands are not part of this theorem's panel**. Boundary probes are treated separately in BOUNDARY_POINT_RECONSTRUCTION.md.

The primary datum is an exact population endpoint-probability panel on a finite set of such commands. A population Cauchy-oracle implementation is described below. Finite noisy frequencies are a different observation contract.

## 2. From raw endpoint values to products and sampled ratios

For S in E and chosen interior values on S, form the inherited multiplicative mask contrast

E_S(x_S)=product_(T subset S) Q(x_T)^((-1)^(|S|-|T|)),

where x_T agrees on T and is zero elsewhere, and Q(0)=1. Every raw Q here is positive because each nonzero command is interior and the inventory is finite. The same Boolean-lattice cancellation as in the predecessor gives

E_S=(1-product_(i in S) r_i(x_i))^(n_S).

Knowing n_S permits the nonlinear transformation

P_S(x_S)=1-E_S(x_S)^(1/n_S)=product_(i in S) r_i(x_i).

It is these positive products, not the raw log Q values, that become linear after taking logarithms.

Retain the base product p_S=P_S(x_(i,1):i in S) for every support. For each participating root i, choose any one incident support S_i and vary only coordinate i to each of its other selected levels, holding other coordinates in S_i at their reference values. Then

rho_(i,l)=P_(S_i)(i at level l, others at base)/p_(S_i)
          =z_(i,l)/u_i.

Thus all sampled within-root ratios are observed, with rho_(i,1)=1 and strictly increasing positive ratios thereafter. If a different incident support supplies the ratio, it must agree under the common-calibration promise. A known positive unary support works in the same construction: its base product directly supplies u_i.

These base and single-coordinate contrasts form a sufficient finite subpanel. It needs at most sum_(S in E)2^|S| base raw values plus sum_i (m_i-1)2^|S_i| varied raw values, before merging repeated commands and omitting known Q(0). Four-value positive-multiplicity panels from the predecessor may be added if interaction counts are not already supplied; that is an additional recovery step, not an assumption that raw logs reveal counts automatically.

Independent information fixing an actual sampled calibration value may also be included. The ratios convert such a value to a base value u_i; this adds a unit-row anchor below. It must be independently warranted or recovered by the separate unary-count theorem, not posited by the rank argument.

## 3. Exact observation-equivalence fibre

Let A have one row 1_S for each support S in E, on columns V. Include a unit row e_i for every additional actual-base anchor. Known positive unary supports already contribute those unit rows. Let y_i=log u_i, and let b contain log p_S and the corresponding logarithmic anchor values. Then

A y=b.

All other sampled values are rho_(i,l) exp(y_i). The compatible base-log domain is the open box

U={y: y_i < -log rho_(i,m_i) for all i}.

There is no lower finite bound because exp(y_i)>0 for every finite real y_i. Strict ordering of the ratios gives strictly ordered interior sampled values. The model promise ensures that the fibre F={y in U:Ay=b} is nonempty.

**Finite-panel equivalence theorem.** Fix one admissible world with sampled values z_(i,l). Every other admissible sampled-value array with the same sufficient subpanel and anchors has exactly the form

z'_(i,l)=exp(v_i) z_(i,l),
v in ker A,
exp(v_i) z_(i,m_i)<1 for every i.

Conversely every such v is realized by endpoint-preserving increasing calibration homeomorphisms with identical subpanel data.

For necessity, equality of the measured ratios forces z'_(i,l)/z_(i,l) to be one positive constant c_i for each root. Equality of every base product gives product_(i in S)c_i=1, and an actual anchor gives c_i=1. Taking v_i=log c_i gives A v=0 and the displayed interior constraint.

For sufficiency, positive scaling preserves the order of all sampled values. Interpolate linearly through

(0,0), (x_(i,1),exp(v_i)z_(i,1)), ...,
(x_(i,m_i),exp(v_i)z_(i,m_i)), (1,1).

Every consecutive slope is positive. The result is a continuous strictly increasing endpoint-preserving homeomorphism. Each support product at any selected combination of levels is unchanged because product_(i in S)exp(v_i)=1. The same holds when some coordinates are zero. Every factor of Q is therefore unchanged on the **entire finite interior/zero Cartesian grid**, not just on the compact subpanel. Anchors are also unchanged.

This proves equivalence between the compact record and full finite-grid endpoint observations within the known complete inventory class. With an incomplete list of possible supports, unlisted raw endpoint constraints might add information; the whole-grid converse must not be claimed from a partial interaction list.

## 4. Rank, partial identification and the remaining freedom

Every admissible reference array has positive slack below one at its finitely many sample points. Consequently every kernel vector admits sufficiently small positive and negative multiples satisfying the inequalities. The feasible base-log fibre is an open convex subset of y+ker A, and

span(F-F)=ker A,
dim F=|V|-rank A.

Therefore all sampled calibration values are identified exactly when A has full column rank. Rank deficiency gives an actual local continuum of admissible calibration arrays, not merely an algebraic null vector that cannot satisfy the model constraints.

A particular root i is identified exactly when every kernel vector has v_i=0, equivalently e_i belongs to the row space of A. More generally, a log-linear target h^T y, or its positive monomial exp(h^T y), is identified exactly when h belongs to that row space. This is an ordinary real linear-record criterion on the stated open domain.

The old probability-law linear-record proposition is not applied literally to y. Log calibration coordinates are negative real parameters, not probability masses. They do not sum to one or obey a mass-zero perturbation rule. The proof of span(F-F)=ker A above uses interior slack, not probability normalization. LINEAR_RECORD_SCOPE.md gives the source-bound inheritance and an exact counterexample to importing a mass constraint.

### Examples

- **One AB interaction:** A=(1,1). The gauge is (v_A,v_B)=(c,-c), recovering the predecessor's reciprocal scaling.
- **AB, AC, BC:** the unsigned incidence matrix has determinant -2 and full rank. No unary support is needed. In particular u_A=sqrt(p_AB p_AC/p_BC), with cyclic formulas for u_B,u_C. Positive branches are fixed by u_i>0.
- **AB and ABC:** u_C=p_ABC/p_AB is identified, while A and B retain reciprocal scaling. Thus some roots can be identified without full column rank.
- **AB, AC:** the connected star still has gauge (c,-c,-c). Connectedness alone does not identify the calibration values.
- **AB, BC, CD, DA:** the even cycle has gauge (c,-c,c,-c), while adding a suitable odd-cycle edge removes it.

For pair supports only, the equations are v_i+v_j=0. This is the **unsigned product-incidence** convention, not the difference-incidence equations v_i-v_j=0 of an offset problem. In a connected bipartite component, kernel vectors alternate c and -c on the two parts, giving one parameter. In a component with an odd cycle, alternating around it forces c=0 and connectivity forces every coordinate to zero. Thus the kernel dimension is the number of bipartite components of the participating pair graph. One actual/unary anchor anywhere in such a component removes its parameter. The graph records observation constraints, not metaphysical efficient dependence.

For hyperedges of larger size, use ordinary incidence rank; graph connectedness or pair-graph intuition is not a substitute. For example all four triples on four roots give the matrix J-I and full rank, despite having no unary row.

## 5. What the finite data do not identify

Even when A has full rank, they determine only the chosen sampled values. Between two consecutive commands, many strictly increasing continuous interpolants can share the same endpoint values. Their full response functions can differ at an unobserved command. No whole calibration map is identified by this finite grid.

When A is deficient, increasing precision or repeating the same finite-grid commands cannot remove the exact gauge. Adding more interior levels at the same participating roots determines more ratios but retains the same base-product kernel, if no new support constraint or actual anchor is added. Unit-boundary commands are a genuinely different instrument and can remove this residual, as the separate boundary procedure shows.

Common coordinatewise calibration, known support multiplicities and the fixed-inventory product law are essential. Support-specific maps, cross-talk, shared random gates or latent mixtures break the reduction to these products. Their existing predecessor countermodels remain in force.

## 6. Precise reconstruction/oracle contract

The rank of A and a full-rank square row basis are computed exactly from the known zero/one matrix by rational elimination. No unknown-real equality test is needed for this step.

If A has full column rank, choose a square nonsingular row matrix A_B. Its inverse has rational entries, so

u_i=product_j p_(B_j)^((A_B^(-1))_(ij)),
z_(i,l)=rho_(i,l)u_i,

where an anchor-row datum replaces p_(B_j) where appropriate. This is an exact population formula for real values, not a promise that an arbitrary real calibration has a finite rational encoding.

Under certified population Cauchy access to the finitely many raw probabilities, all contrast products and quotients are computable: refine each positive denominator until a positive rational lower bound is known. Integer roots recover E_S^(1/n_S), and further positive rational powers in the displayed inverse can be evaluated by certified root bisection and division. All required quantities are positive at the stated interior commands. Consequently any requested finite precision for the identified sampled values is obtained after finitely many refinements, with no uniform precision/runtime bound claimed.

This does not turn finite Bernoulli samples into exact population probabilities, decide arbitrary unknown-real consistency equalities, or certify absent supports. Feasibility and the observation model are promises. Exact-rational panel inputs are a different stronger contract and are used only for finite controls.
