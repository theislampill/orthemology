# Tensor moments and corrective dynamics

## Abstract

A tensor of expectations can describe a state without determining how that state will respond to a later intervention. This chapter develops the exact boundary between those two tasks for Fisher gradient flows and polynomial reweighting of probability laws. On a known finite numerical support, interpolation gives an exact finite closure of the tensor hierarchy. On compact supports, all moments determine the law; on unbounded supports, even the complete moment record and every derivative at the initial time can leave the future undetermined.

The central existence results start from polynomial functionals rather than presumed probability laws. For autonomous coercive polynomial energies, the full hierarchy and positivity on every polynomial square force an actual normalized exponential tilt. Signed energies require a different hypothesis on the initial weighted energy distributions. Time-dependent sums of squares admit a cumulative coercivity theorem, including rates that are rank one at every instant. With a fixed controlled subspace, zero hidden coordinates give automatic existence and identification, one hidden coordinate gives existence with possible ambiguity, and two or more permit strictly square-positive paths that cease to represent any law immediately after a genuinely valid initial state. Complete proofs, counterexamples, effective recovery under explicit promises, and finite diagnostic limits are developed together.

This is a public mathematical exposition. It preserves the accepted editions of the established Orthemology papers and makes no adoption or priority claim. In particular, a moment hierarchy on a fixed numerical state space does not complete the unfinished programme of an original n-person noetic field. The constructive results here supply conditional mathematical components; their application to cognition, normativity, or a field of persons requires separate scientific arguments.

## 1. States, records, and actual operations

Let $`\mathcal P_\infty(\mathbb R^d)`$ denote the Borel probability measures having every absolute polynomial moment, with $`1\le d<\infty`$. A law $`\mu`$ defines the real linear functional

```math
L_\mu(p)=\int_{\mathbb R^d}p(x)\,d\mu(x),
\qquad p\in\mathbb R[x_1,\ldots,x_d].
```

Its full moment record consists of all numbers $`L_\mu(x^\alpha)`$, equivalently all symmetric tensors $`M_r=\int x^{\otimes r}\,d\mu`$. The coordinate dimension is finite; the set of tensor grades is infinite. The record belongs to a product of finite-dimensional tensor spaces. It is generally not an element of their algebraic direct sum, whose elements have only finitely many nonzero grades.

A real polynomial functional $`L`$ is normalized when $`L(1)=1`$. Independently of normalization, it is **square-positive** when $`L(q^2)\ge0`$ for every real polynomial $`q`$. Equivalently, every finite polynomial Gram matrix $`(L(p_i p_j))_{i,j}`$ is positive semidefinite. Positive scalar multiples preserve square positivity. All hierarchy records in this chapter are normalized; their unnormalized intermediate functionals retain square positivity without being required to have mass one.

Square positivity and nonnegativity of individual monomial coordinates are different conditions on a real polynomial algebra; neither implies the other in general. On $`\mathbb R[x]`$, evaluation at $`-1`$ is square-positive because $`L(q^2)=q(-1)^2\ge0`$, although $`L(x)=-1`$. Conversely, the normalized functional specified by $`m_0=m_1=1`$ and $`m_r=0`$ for $`r\ge2`$ has no negative monomial coordinate, but $`L((1-x)^2)=1-2+0=-1`$. Square positivity imposes cross-moment consistency that individual sign checks miss, while allowing negative odd moments on a real state space. It is necessary for a positive representing measure, but in several variables it is not sufficient, as the explicit construction in §9.1 will show.

A polynomial is a **sum of squares**, abbreviated SOS, if it is a finite sum of real polynomial squares. Square positivity allows evaluation of an SOS as nonnegative; it does not allow that inference for every pointwise nonnegative polynomial.

Failure of coordinate positivity to ensure a law persists at every fixed square-test depth. Fix an integer d≥1 and let μ be uniform on {1,…,d}. On polynomials of degree at most 2d define a normalized truncated functional L by retaining the moments of μ below degree 2d and replacing its moment of degree 2d by ∫x^(2d)dμ−1/2. Every displayed monomial moment remains strictly positive, since each original moment is at least one. For every polynomial q of degree less than d, q² has degree below 2d, hence L(q²)=∫q²dμ≥0. But P(x)=∏_(j=1)^d(x−j) is monic, P² has leading coefficient one, and ∫P²dμ=0. Therefore L(P²)=−1/2. No positive measure can represent these truncated moments. This is a static finite-moment construction: it does not describe an ODE from admissible initial data, and no finite list of executed tests is claimed. [AFTER2134-F25-017](../research/t20-v6-20261012/sources/852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0/contracts.py#L260-L282)

The retained scalar certificates and moment table give a separate finite three-variable obstruction. Define L on polynomials of total degree at most four by L(1)=1, L(x²)=L(y²)=L(z²)=4, L(xyz)=3/2, L(x⁴)=L(y⁴)=L(z⁴)=50 and L(x²y²)=L(x²z²)=L(y²z²)=1, with every other listed moment zero. In the quadratic basis 1,x²,y²,z²,x,yz,y,xz,z,xy, L(q²) splits into one even block and three odd blocks. The even block has the certificate (c+4(a+b+d))²+4(a²+b²+d²)+15((a−b)²+(a−d)²+(b−d)²), and each odd block is (2u+3v/4)²+7v²/16. Thus L(q²)>0 for every nonzero q of degree at most two. Nevertheless P=1−4xyz+x²y²+x²z²+y²z² is nonnegative everywhere and L(P)=−2. For xy≥0 its positivity follows from (xy−1)²+z²(x−y)²+2xy(z−1)²; for xy≤0 use (xy+1)²+z²(x+y)²−2xy(z+1)². No positive measure realizes these finite moments. This reconstruction from the displayed table is not the full-polynomial functional of §9.1, an all-degree extension, or a newly checked implementation of the imported Certificate module. [SUB250-R17-052](../research/t20-v6-20261012/sources/579f6262345d253651b7c21f65fb7b1aa65fe6a4aacb569730efe3b4f1c2dbcb/ScalarPositivity.lean#L17-L166) [SUB250-R17-096](../research/t20-v6-20261012/sources/5f8fed504c938f3c57a67c38efbc106ba8292c607230315bf347f1da38904091/MomentValues.lean#L5-L108)

The specified zero-coefficient continuation of that truncated table fails even non-strict square positivity outside the certified domain: for the cubic q=x³−x it gives L(q²)=−96. This does not contradict strict positivity on nonzero quadratics. Their squares have degree at most four, and linearity makes every finite sum of such squares strictly positive when at least one summand is nonzero. The failure concerns this chosen continuation, not an assertion that no other extension could preserve square positivity; the imported quadratic certificate and the displayed all-degree construction remain different interfaces. [A750-F50-013](../research/t20-v6-20261012/sources/aff81e2824f374975a1207bd589f99081580e1d67409930785a87c61bab5d0e1/Controls.lean#L7-L35)

Three questions must therefore be separated:

1. **Existence:** does a proposed record have a probability representative?
2. **Identification:** is that representative unique within the declared state space?
3. **Continuation:** do all representatives produce the same declared later observations under the admitted operations?

For a real energy $`h`$, the actual reweighting operation, whenever all required integrals exist, is

```math
\mathcal T_t^h\mu(dx)
  =\frac{e^{-t h(x)}}{Z_\mu(t)}\,\mu(dx),
\qquad
Z_\mu(t)=\int e^{-t h}\,d\mu>0.
```

For a supplied time-dependent energy $`h_t`$, replace $`t h`$ by $`H_t=\int_0^t h_s\,ds`$. Adding a scalar depending only on time does not change the normalized law. A likelihood that depends on an unobserved coordinate is a different operation from one that acts only on the observed coordinates.

A **coordinatewise $`C^1`$ hierarchy** means that every polynomial coordinate is continuous on $`[0,T)`$, continuously differentiable in the interior, and has its continuous right derivative at zero. It does not assume a norm on the infinite sequence, a uniform bound in the degree, or a Banach-space uniqueness theorem. For autonomous polynomial energy the hierarchy is

```math
\frac{d}{dt}L_t(p)
 =-L_t(hp)+L_t(h)L_t(p),
\qquad p\in\mathbb R[x_1,\ldots,x_d].
\quad\text{(1)}\quad
```

The finite sum defining $`hp`$ makes every equation meaningful. Whether a solution of these equations is an actual law-level evolution is a theorem to prove, not a definition to smuggle in.

A separate transport-and-killing control warns against splitting a scalar residual into stronger statements than it supplies. For a first-order operator D=c₀+b·∇, D(pχ(H))=χ(H)D(p)+χ′(H)p b·∇H; the second term cannot be dropped when localizing by energy. After scalar pushforward a vanishing residual can have the form ∫χ dα+∫χ′ dβ=0 with a nonzero signed measure α and a nonzero positive measure β: α=δ₀−δ₁ and β equal to Lebesgue measure on [0,1] cancel by the fundamental theorem of calculus. This does not imply α=β=0. Passing such an order-one residual from polynomials to smooth tests requires derivative control as well as uniform control: for n≥1, Tₙ(x)/n has sup norm 1/n on [−1,1] but derivative n at 1. The supremum follows from the standard identity Tₙ(cos θ)=cos(nθ); the source's finite control checks only the endpoint value and derivative for n=2,…,9, not the supremum over the interval. These elementary examples explain the interface requirement; the finite symbolic controls, factorial checks and cubic-valley identities are not a universal measure-existence or localization proof, and their transport operator is distinct from the pure reweighting hierarchy (1). [AFTER1384-08](../research/t20-v6-20261012/sources/240737b4766b9869591daa5ccba2d3a97b978d94a74c4f430c994538cb35df8c/check_independent.py#L14-L78)

A separate complete-flow control gives a concrete nonlinear contrast to an exploding characteristic. For b(x,y)=(−(x²+y²)y,(x²+y²)x), the radius squared is conserved, so each trajectory is rotation at its fixed angular speed and exists for every finite positive or negative time. The selected atoms (0,0),(1,0),(0,2) follow (0,0),(cos t,sin t),(−2 sin 4t,2 cos 4t). With signed rate k_t(x,y)=t(x²+y²)+x, their integrated rates are respectively 0, t²/2+sin t and 2t²+(cos 4t−1)/2. Positive initial masses multiplied by exp(−K_j(t)) remain positive and can be normalized; the source requests the raw generator and normalized quotient identities. By contrast x′=x² with x(0)=1 has the characteristic 1/(1−t) on its maximal interval t<1, while x′=−x³ has forward map a/√(1+2a²t) whose inverse is only defined on its image for t>0. Thus nonlinear polynomial drift alone supplies neither two-sided completeness nor global surjectivity. These explicit characteristics do not prove a general measure-representation or hierarchy-uniqueness theorem, and the symbolic controls and predecessor bindings were not executed. [AFTER2384-THIRD25-62](../research/t20-v6-20261012/sources/acf390f50b5cf3f2fa4e068a7ba0c3d88b75944e8b47638358333f27cd0fd4c8/check_exact.py#L18-L85) [AFTER2384-THIRD25-62](../research/t20-v6-20261012/sources/acf390f50b5cf3f2fa4e068a7ba0c3d88b75944e8b47638358333f27cd0fd4c8/check_exact.py#L90-L109)

Continuous time coefficients do not force a twice-differentiable moment path once transport is included. On 0≤t≤1 take a(t)=|t−1/2|, drift b_t(x)=a(t)x and killing K(x)=1+x². With H=1+x², b_tH′=2a(t)x²≤H and K=H, so this example retains uniform elementary growth and killing bounds. A characteristic starting at z is X(t)=z exp(g(t)), where g(t)=t/2−t²/2 for t≤1/2 and g(t)=t²/2−t/2+1/4 for t≥1/2. The two formulas and their first derivatives agree at the join. Their second derivatives give X″(1/2+)-X″(1/2−)=2z exp(1/8), nonzero when z≠0. A positive killed Dirac mass normalizes to δ_X(t), whose first spatial moment is exactly X(t); it is therefore C¹ but not C². This direct characteristic calculation shows why differentiating time-dependent coefficients requires an additional regularity premise. It does not contradict the autonomous pure-killing hierarchy or supply a general transport representation, uniqueness or global norm estimate. The source’s symbolic checks, including its separate moving-quadratic example, were read rather than run. [AFTER2634-FOURTH25-082](../research/t20-v6-20261012/sources/d2719d5f4f7ef6da483352302d01502f4d7600a1fff11f8a7047e5d8275d74a6/check_independent.py#L76-L90)

The background measure results used below are classical: one-dimensional Hamburger and Stieltjes existence, Carleman determinacy, the multivariate Carleman existence theorem, the compact algebraic-set moment theorem, and Haviland's representation theorem. Their precise roles are cited at the point of use. Most of the chapter consists of direct arguments linking those results to the specified dynamics.

### 1.1 Finite typed words and their declared meaning

The full moment record above belongs to a product of grades. A different construction represents a finite structured record in an algebraic tensor algebra. Keeping these constructions distinct prevents a false inference from the finite support of an episode description to the finite support of its entire moment sequence. The formalisation source develops the following optional encoding of a declared view; it does not identify an episode, a person or a worldly process with a tensor. [FORM, §§2–4][FORM]

Fix an analysis and representation declaration. Let $`D`$ be the selected set of episode tokens and $`\xi:D\to\mathscr D`$ a supplied finite record view. A finite reference to an equation, a person or an infinite candidate family need not enumerate its referent. The view records the distinctions required by its contract: occurrence and version, analysis and task, evidence and its order, actor and authority, claims and unresolved obligations, and relevant handoff or successor relations. Empty, absent, inapplicable, unknown and unsupported entries remain distinct whenever the contract distinguishes them. A missing finite view calls for a restricted domain or a partial encoder; it is not made finite by silently discarding unavailable material. No addition operation on the set $`D`$ is presumed.

Let $`\mathcal T`$ be a set of role types and $`V_\tau`$ a real vector space for each type. Put

```math
V=\bigoplus_{\tau\in\mathcal T}V_\tau,
\qquad
T(V)=\bigoplus_{n\geq0}V^{\otimes n},
\qquad V^{\otimes0}=\mathbb R.
```

For a finite ordered word $`w=(\tau_1,\ldots,\tau_n)`$, write $`V_w=V_{\tau_1}\otimes\cdots\otimes V_{\tau_n}`$. The empty word contributes $`\mathbb R`$. Distribution over algebraic direct sums gives

```math
T(V)\cong\bigoplus_{w\in\mathcal T^*}V_w.
```

Multiplication concatenates ordered factors. For a linear map $`f:V\to\mathcal B`$ into an associative unital real algebra, define its extension on a pure word by

```math
\widetilde f(v_1\otimes\cdots\otimes v_n)
 =f(v_1)\cdots f(v_n),
\qquad \widetilde f(1)=1_{\mathcal B}.
```

Multilinearity makes this well-defined on each tensor power, and linear extension over finite sums gives an algebra map. Every algebra extension must have these values on the spanning pure words, proving uniqueness. This universal property extends a supplied linear map; it does not provide an episode-composition operation on the set $`D`$.

A declaration can restrict admissible words to $`\mathcal W`$ and use $`H=\bigoplus_{w\in\mathcal W}V_w`$. Without closure of $`\mathcal W`$ under concatenation, this is a graded subspace and need not be a subalgebra. The admitted encodings within $`H`$ need not form a vector subspace either.

A multi-degree counts how often each type occurs. Its component is the **direct sum of all words with those counts**, rather than one silently sorted tensor product. For example, actor–evidence–claim and evidence–actor–claim have the same counts and occupy different word summands. Permuting factors gives a linear isomorphism between the corresponding spaces. Treating the roles as interchangeable requires an additional semantic argument.

For any supplied map $`\rho:D\to H`$, let $`P_w`$ be the word projection and define

```math
S(e)=\{w:P_w\rho(e)\ne0\},
\qquad
N(e)=\max\bigl(\{0\}\cup\{|w|:w\in S(e)\}\bigr).
```

**Finite word decomposition.** Each $`\rho(e)`$ has the unique expression

```math
\rho(e)=\sum_{w\in S(e)}j_wP_w\rho(e),
\qquad |S(e)|\lt{}\infty,
\quad N(e)\lt{}\infty,
```

where $`j_w`$ is inclusion into the direct sum.

**Proof.** An algebraic direct-sum element has finitely many nonzero coordinates. Its independent summands make those coordinates unique. The finite set of their finite word lengths has a maximum, with the stated zero convention when the support is empty. ∎

This is a consequence of the chosen codomain, not an empirical discovery about episodes. A nonzero scalar has degree zero; the zero element has empty support and $`N=0`$ by convention. Selected interaction occurrences and nonzero algebraic support also differ: zero coefficients or cancellation can remove a component. An ambient language admitting all finite lengths does not prove that the actual range of $`\rho`$ has unbounded degree. Coefficient count, tensor rank, stored-record size, number of players and derivative order are separate quantities. [FORM, Proposition 3.2][FORM]

### 1.2 A faithful finite record channel

Choose an injective finite atomisation $`\mathrm{At}:\mathscr D\to\mathcal P_{\mathrm{fin}}(X_{\mathrm{rec}})`$. An atom records its typed field path and value, including container markers, ordered-sequence indices, and the identities and versions of references. Distinct occurrences have distinct paths or occurrence identifiers, so equal list entries do not disappear through set deduplication. Fixing or normalising map-key order belongs to the declaration.

In the free vector space on these atoms, put

```math
V_{\mathrm{rec}}=\mathbb R^{(X_{\mathrm{rec}})},
\qquad
\eta(d)=\sum_{a\in\mathrm{At}(d)}[a]_{\mathrm{rec}}.
```

Every retained atom has coefficient one. This record channel has tensor degree one even when it contains many fields.

A separate interaction extractor supplies finitely many occurrences $`r`$. Each has a relation signature $`\lambda(r)`$, a finite arity $`n_r`$, ordered argument values $`v_{r,j}`$, an occurrence identifier and a real coefficient $`a_r`$. Give each argument its own tagged role type $`(\lambda(r),j,\tau_{r,j})`$ and use free basis vectors carrying both the occurrence identifier and its value. Define

```math
\iota(e)=\sum_r a_r
 \bigotimes_{j=1}^{n_r}
 [r,v_{r,j}]_{(\lambda(r),j,\tau_{r,j})},
\qquad
\rho(e)=\eta(\xi(e))+\iota(e).
```

The record type is disjoint from every interaction-role type. The occurrence identifier preserves incidence across the factors; it is metadata for the chosen occurrence, not another semantic argument. Its omission needs justification if multiplicity or identity matters. The extractor must supply the relations; co-occurrence alone does not create a support or authority relation.

**Faithfulness to the declared view.** Under the finite-view and injective-atomisation hypotheses, $`\rho(e)`$ is well-defined with finite word support and determines $`\xi(e)`$ exactly. If $`\xi`$ is injective on $`D`$, then so is $`\rho`$.

**Proof.** Both displayed sums contain finitely many finite tensors. Projection onto the distinguished record summand removes the interaction channel and leaves $`\eta(\xi(e))`$. Independence of the record basis recovers precisely its retained atom set. Injective atomisation then reconstructs $`\xi(e)`$. An injective view consequently separates the original selected tokens. ∎

The disjoint positive record channel matters: even signed interaction coefficients cannot cancel its atoms. For example, take a nonempty record and unit-coefficient interactions: two evidence-to-claim occurrences add two coefficients in one degree-two word component; an actor–evidence–claim occurrence adds degree three, and a configuration–evidence–claim–route occurrence adds degree four. Along with the record channel these have degree profile $`\{1,2,3,4\}`$. An unresolved obligation can remain a tagged record atom throughout; no degree change is needed merely to change its status. [FORM, Proposition 4.1 and worked finite view][FORM]

This construction establishes preservation of the declared record, with no claim of compression or efficient storage. The ambient basis can be very large or infinite across episodes. Equality of reference identifiers does not authenticate their referents. A record containing a false conclusion is just as encodable as a record containing a true one. Mapping that record injectively into a disjoint set of higher-level appraisal objects preserves its identity and leaves the conclusion false. Thus injective encoding or reification supplies no truth upgrade. A new appraisal needs its own grounds. Nor does informal conversational activity automatically satisfy the separate domain conditions for a canonical episode record, an ecology registration or a game declaration. These boundaries concern the proposed representation, not a universal reflective requirement on ordinary knowers. [FORM, §§4 and 12][FORM]

### 1.3 Degree shifts, contractions and a higher-order distinction

Let $`H=\bigoplus_{n\geq0}H_n`$ be any algebraic graded real vector space, with negative-index spaces interpreted as zero. For a **linear** map $`D:H\to H`$, define

```math
D^{[k]}v=\sum_{n\geq0}P_{n+k}D(P_nv),
\qquad k\in\mathbb Z.
```

Then $`D^{[k]}`$ shifts degree by $`k`$ and

```math
Dv=\sum_{k\in\mathbb Z}D^{[k]}v
```

is pointwise locally finite. To prove this, fix $`v`$. It has finite input-degree support; each of the finitely many vectors $`D(P_nv)`$ has finite output-degree support. Only the finite set of differences between these input and output degrees contributes. Summing their projections recovers $`Dv`$. No uniform bound on the shifts for every possible $`v`$ is required. Conversely, an arbitrary proposed family of degree-shifting maps does not define this algebraic sum without pointwise local finiteness, unless a separate completion and convergence rule is supplied. A state-dependent or guarded revision may be nonlinear or partial, so this linear decomposition cannot simply be assigned to it. [FORM, Proposition 6.1][FORM]

A contraction of an ordered tensor slot requires a specified covector:

```math
C_{j,\varphi}(v_1\otimes\cdots\otimes v_n)
 =\varphi(v_j)
   v_1\otimes\cdots\widehat{v_j}\cdots\otimes v_n.
```

Its output word must also be admitted if the operation is to remain inside a restricted representation space. The covector cannot be chosen as a nonzero real linear functional invariant under **every** invertible basis change. If $`\ell\circ g=\ell`$ for all $`g\in\mathrm{GL}(W)`$, taking $`g=2\mathrm{id}_W`$ gives $`2\ell=\ell`$, hence $`\ell=0`$. A declared free basis does supply the useful augmentation $`[x]\mapsto1`$; that added structure is precisely what probability marginalisation uses. The basis-copy discussion in [Received Actuality, §10.7](../foundations/received-actuality-and-intrinsic-necessity.md#107-an-invariant-average-need-not-identify-any-individual) likewise keeps basis-relative operations and their transported interpretation together. [FORM, Proposition 6.2][FORM]

An algebraically valid contraction need not preserve a required target. Take a nonzero $`v`$ and distinct basis vectors $`d_0,d_1`$ with $`\varphi(d_0)=\varphi(d_1)=1`$. Both $`v\otimes d_0`$ and $`v\otimes d_1`$ contract to $`v`$. Any target distinguishing the two originals therefore fails the fibre criterion already proved in [Physical Realisation, §9.3](physical-realisation-and-continuation.md#93-lossless-abstraction-is-target-relative). Calling the operation a discharge does not alter the collision. [FORM, Counterexample 6.3][FORM]

Parity gives a useful positive calculation of exactly which tensor component is lost. For $`n\geq2`$ and $`x\in\{0,1\}^n`$, let

```math
P_\pm(x)=2^{-n}\bigl(1\pm(-1)^{x_1+\cdots+x_n}\bigr).
```

These are probability laws uniform on the two parity classes. Summing over any missing coordinate cancels the alternating term, so every proper-subset marginal is the corresponding uniform law. Their parity expectations are nevertheless $`+1`$ and $`-1`$. If $`v_0,v_1`$ is the basis of $`\mathbb R^2`$ and laws are represented by their coefficient tensors, expansion gives

```math
P_+-P_-=2^{1-n}(v_0-v_1)^{\otimes n}.
```

This nonzero tensor has rank one and order $`n`$. Augmentation $`\varepsilon(v_0)=\varepsilon(v_1)=1`$ annihilates one factor of the difference, and therefore every proper marginal annihilates it. The sign covector $`\psi(v_0)=1,\ \psi(v_1)=-1`$ instead detects the difference through $`\psi^{\otimes n}`$. For any fixed marginal order $`r`$, choose $`n>\max\{r,1\}`$: the retained marginals agree while parity differs, excluding an exact decoder for both laws. A single target-specific parity statistic still suffices. Thus the result constrains the permitted representation family; it does not require unbounded actual episode degree or large tensor rank. [FORM, Theorem 5.1 and Corollary 5.2][FORM]

The stronger continuation question is already developed in [Information and Inquiry, §2.4](information-and-inquiry.md#24-how-a-constrained-action-graph-changes-the-necessary-information): permitted pairwise operations and their graph determine when a hidden character becomes observable. The parity calculation here isolates the contraction mechanism without asserting a comparative advantage over relations, hypergraphs or another adequate representation.

### 1.4 Representation changes and future-relevant reductions

For type-preserving linear isomorphisms $`g_\tau:V_\tau\to V'_\tau`$, the induced tensor map satisfies

```math
T(g)|_{V_w}=g_{\tau_1}\otimes\cdots\otimes g_{\tau_n}.
```

It preserves word types and degrees. A passive representation change has the stronger, checkable condition $`\rho'=T(g)\rho`$ on the admitted domain. Free-basis relabelling satisfies it when the encoder and its interpretation are transported together. An arbitrary change in the analysis, target or authority is not made passive by the existence of a linear isomorphism. Similarly, representing a workflow composition by tensor multiplication would require $`\rho(e\circ f)=\rho(e)\rho(f)`$ wherever composition is defined, or another explicit intertwining law. Shared evidence, aliases and duplicate obligations can defeat that equation. The free-record construction establishes no such blanket homomorphism. [FORM, §4][FORM]

The existing attained-image fibre criterion applies to the entire intended continuation contract. Let $`r:D\to Y`$ be a reduction, $`F:D\to D`$ a deterministic update, $`q:D\to Z`$ a required target and $`\ell:D\to\mathcal P(\mathscr J)`$ the declared set of feasible future inquiries. Applying that criterion to $`r\circ F`$, $`q`$ and $`\ell`$ gives reduced maps on $`r(D)`$ exactly when all three are constant on every fibre of $`r`$:

```math
\bar F\circ r=r\circ F,
\qquad
\bar q\circ r=q,
\qquad
\bar\ell\circ r=\ell.
```

The same finite induction as the exact-continuation proof in [Physical Realisation, §7.1](physical-realisation-and-continuation.md#71-the-exact-induction) then gives

```math
r(F^m(d))=\bar F^{\,m}(r(d)),
\qquad
q(F^m(d))=\bar q(\bar F^{\,m}(r(d))),
\qquad
\ell(F^m(d))=\bar\ell(\bar F^{\,m}(r(d)))
```

for every finite $`m`$. The first equation follows by iterating the commuting update equation; substitution gives the other two. This is an application of those factorisation and induction arguments, without a finiteness assumption on $`D`$ and without an effective algorithm being inferred. Probabilistic and nondeterministic updates need their own compatible contracts. The finite instrument construction in [Information and Inquiry, §§2.1–2.4](information-and-inquiry.md#2-finite-instruments-and-exact-predictive-states) supplies substantially stronger computational and memory results under its stated premises. [FORM, Theorem 11.2][FORM]

A present target can be constant on a collapsed pair while a later target separates the pair. The export counterexample in [Physical Realisation, §6.2](physical-realisation-and-continuation.md#62-a-one-bit-export-can-lose-a-two-step-state) supplies an operational instance. Future adequacy therefore declares a target family and horizon; it does not demand preservation of every possible distinction forever. Active degree reduction and the truth of a recorded disposition are also different from retaining the relevant history, as [Information and Inquiry, §9.4](information-and-inquiry.md#94-selecting-a-valid-certificate-rather-than-recovering-a-state) makes explicit.

An orbit reduction is a useful special case. If a group acts on $`D`$ and $`F(gd)=gF(d)`$, then $`[d]\mapsto[F(d)]`$ is well-defined: representatives $`d'=gd`$ have outputs in the same orbit. A target descends exactly when it is constant on each orbit. A differentiable gauge or slice still needs its own regularity conditions, and a change of analysis need not be such a symmetry. [FORM, Proposition 10.7][FORM]

Finally, finite support at every stage does not supply a state after infinitely many structural changes. The source gives events at times $`t_m=1-2^{-m}`$ with increasing tensor degree. To make the retained-history issue explicit, take a nonzero generator $`v`$ and retain each new grade as

```math
s_m=\sum_{j=1}^{m}v^{\otimes j}.
```

Every $`s_m`$ lies in the algebraic direct sum. Its prospective coordinatewise limit has a nonzero component in every positive grade and lies outside that direct sum. Thus a finite-stage encoding and a finite-transition preservation proof do not provide an admissible state at the accumulation time. One must exclude such unhandled accumulation or supply a different state space and a justified continuation. This explicit history sum spells out the source's finite-support boundary; it neither declares a topology for all episode encodings nor equates formal degree growth with a physical singularity. [FORM, §10, “Hybrid safety and the infinite-event boundary”][FORM]

The source's conditional synthesis now has a concrete reading across the chapters. Under one compatible set of declarations, the encoder gives finite typed support, the retained-history theorem keeps the obligation lineage, and the inquiry-menu definition supplies the prospective feasible set. Wherever the additional finite-game premises hold, [Collective Inquiry, §3.2](collective-inquiry-and-strategic-coordination.md#32-existence-is-conditional-stability) supplies a mixed equilibrium; an adequate quotient gives the finite continuation identities above. These conclusions follow from their respective hypotheses, without identifying their different objects. They do not imply that an equilibrium is played, a recorded conclusion is true, the menu improves or infinite-time execution exists. Probability marginalisation here and mixed-payoff contraction in [Collective Inquiry, §3.1](collective-inquiry-and-strategic-coordination.md#31-a-game-is-additional-structure) are actual uses of multilinear structure. A comparative advantage still needs a target-preserving calculation or measured benefit at a declared cost; mere encodability, including the degree-one record construction, establishes none. [FORM, Theorem 11.3 and “What would make tensor structure substantively useful?”][FORM]

The 7 October modelling examination distinguishes a declared tensor representation from a further geometric realization. Semantic factor spaces need not be tangent spaces, and payoff tensors need not be metric tensors. A selected smooth state space Q, smooth positive-definite Riemannian metric g, encoding map and smooth objective J support literal conditional geometry through g(grad_g J,v)=dJ(v); they do not identify an unencoded episode with a manifold. Required identities, authority records and history may remain attached outside lossy smooth coordinates, with their recovery governed by the preservation contracts above and in [Information and Inquiry](information-and-inquiry.md). The coordinate-transport identity, metric sensitivity and a descent-without-feasibility counterexample are already developed in [Common Repair, §5.5](common-repair-and-geometric-obstructions.md#55-faithful-changes-of-representation). Objective decrease alone supplies neither global continuation, convergence nor truth-directed warrant. The examination’s foundationalist and proper-functionalist orientation is a stated philosophical modelling commitment, not a scalar objective’s mathematical consequence or a universal metric specification. [AFTER3634-SEVENTH25-155](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/21276da9c57ce7cb7b321e33f46c4ecd21c544a86187fb07377352de2422ae54/Orthemology_Tensor_Riemannian_Examination_and_Dot_Prompt_20261007.md#L21-L60) [AFTER3634-SEVENTH25-155](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/21276da9c57ce7cb7b321e33f46c4ecd21c544a86187fb07377352de2422ae54/Orthemology_Tensor_Riemannian_Examination_and_Dot_Prompt_20261007.md#L198-L267)

### 1.5 Finite relations as Boolean tensors

The declared record representation of §§1.1–1.4 and an extensional interpretation of predicates answer different questions. A record can preserve which occurrence was supplied, while a predicate interpretation assigns tuples of model elements to a relation. Moving between them requires an interpreted extraction: argument roles must be aligned with the same domain, relation symbols must remain distinguished, and occurrence information must be retained separately whenever the task still observes it. A repeated record of one tuple is not another model element; two elements with the same descriptive label remain two elements. The finite transport below begins after these choices have been supplied. [R18-G273, §§1–2][R18-G273]

Fix a finite **nonempty** domain $`D`$ and the Boolean semiring $`\mathbb B=(\{0,1\},\lor,\land,0,1)`$. At arity $`n\geq0`$ put

```math
T_n(D;\mathbb B)=\{P:D^n\longrightarrow\mathbb B\},
\qquad D^0=\{()\}.
```

These finite arrays are the tensor powers of the free Boolean semimodule with distinguished basis indexed by $`D`$. A relation $`A\subseteq D^n`$ corresponds to its characteristic array $`\chi_A`$; taking the support is the inverse. This is a bijection of **extensions at a fixed grade**. Distinct formulas or property intensions can have the same extension. An arity-tagged family, or a graded direct sum, keeps the grades separate; an individual finite expression uses finitely many of them. Complement is taken inside its particular finite cube $`D^n`$, not simultaneously across an infinite graded space or a countably infinite predicate vocabulary. [R18-G273, §2][R18-G273]

For an $`n`$-ary $`P`$ and an $`m`$-ary $`Q`$, let $`k=\max(n,m)`$. The predicate-functor operations have the following exact array interpretation:

| Operation | Array value and arity |
|---|---|
| Negation | $`(\neg P)(a_1,\ldots,a_n)=1-P(a_1,\ldots,a_n)`$, arity $`n`$. |
| Conjunction | $`(P\mathbin{\&}Q)(a_1,\ldots,a_k)=P(a_1,\ldots,a_n)\land Q(a_1,\ldots,a_m)`$, arity $`k`$. |
| Cyclic permutation | $`(\sigma P)(a_1,\ldots,a_n)=P(a_n,a_1,\ldots,a_{n-1})`$ for $`n\geq2`$. |
| First-pair permutation | $`(\iota P)(a_1,\ldots,a_n)=P(a_2,a_1,a_3,\ldots,a_n)`$ for $`n\geq2`$. |
| Existential contraction | $`(cP)(a_2,\ldots,a_n)=\bigvee_{a_1\in D}P(a_1,\ldots,a_n)`$ for $`n\geq1`$; $`c`$ is the identity at arity zero. |
| Leading padding | $`(pP)(a_1,\ldots,a_{n+1})=P(a_2,\ldots,a_{n+1})`$. |
| Equality | $`I(a,b)=1`$ exactly when $`a=b`$. |

Declare $`\sigma`$ and $`\iota`$ to be identities below arity two. This low-arity completion is an explicit hypothesis, not a conclusion about every literal clause in the historical presentation. Conjunction aligns the **initial** coordinates and implicitly pads shorter inputs at the end; $`p`$ adds an ignored coordinate at the **beginning**. Neither conjunction's arity nor its operation is ordinary outer product. [R18-G273, §§2, 4][R18-G273]

**Finite extensional transport.** For every term in this completed typed language, tensor evaluation at each assignment equals satisfaction of the term under the same finite nonempty interpretation. In particular, arity-zero evaluation gives the truth of the corresponding obtaining sentence.

**Proof.** Induct on the term. Atomic predicates agree by the characteristic-array definition, and $`I`$ agrees with equality. Complement reverses membership. Conjunction evaluates both subterms under the same prefix-aligned assignment, including the ignored trailing coordinates of the shorter term. The two permutation clauses pull back the assignment along exactly the displayed coordinate permutations; at low arity both sides use the declared identity. The contraction is one precisely when some first-coordinate witness makes its subterm true, which is the existential clause. Padding ignores precisely its newly added first coordinate. At arity zero there is one empty assignment, and the stated $`c`$ convention preserves its scalar. These cases exhaust the constructors. Reading coefficient support recovers the extension at each grade, proving that the translation and support are inverse homomorphisms of these finite relation algebras. ∎

This theorem preserves truth at each assignment. It therefore preserves both existential closure and the source's universal, all-assignment notion of truth of an **open predicate on a model**, provided the two are not confused. If $`D=\{0,1\}`$ and $`F=\{0\}`$, then $`cF=1`$ although $`F`$ is not true at every assignment. Repeated contraction gives existential closure, not universal model-truth. The resulting consequence comparison is restricted to finite nonempty models. No unrestricted first-order consequence, finite-model property, or completeness of finite testing follows. [R18-G273, §2][R18-G273]

The low-arity hypothesis has a concrete reason. Applied literally to an infinite assignment sequence, the historical unary $`\iota`$ clause can read its second coordinate. A unary predicate true just of $`0`$ then gives different values on sequences beginning $`(0,0,\ldots)`$ and $`(0,1,\ldots)`$, although both have the same declared unary argument. Under those uncompleted clauses, the syntactically scalar $`c(\iota F)`$ can still depend on the incoming first coordinate: contraction prepends its witness and the swap moves the old coordinate into the predicate's argument. The zero-arity cyclic clause also lacks its indexed final coordinate. The stated completion, or a restriction to well-typed permutation terms, removes this ambiguity before the induction is applied. This is the source report's bounded finding about that presentation, not a claim about an unread original system or a refutation of the binary examples. [R18-G273, §4][R18-G273]

### 1.6 Shared witnesses and equality wiring

With $`\varepsilon(e_a)=1`$ on the distinguished domain basis, positive-arity $`c`$ is first-slot contraction by $`\varepsilon`$ **over the Boolean semiring**. Its sum is existential OR. Padding is $`pP=u\otimes P`$ for the all-one vector $`u=\sum_{a\in D}e_a`$. The composite $`pc`$ is an arity-preserving operation that forgets dependence on the first slot; the source's $`c`$ itself lowers arity. Conjunction is pointwise product after the declared lifts. A tensor product can implement it only when the common variables are subsequently joined by equality wires. [R18-G273, §3][R18-G273]

Here is a general and directly checkable binding rule. For a slot map $`\alpha:\{1,\ldots,n\}\to\{1,\ldots,k\}`$, define

```math
(\alpha^*P)(a_1,\ldots,a_k)
   =P(a_{\alpha(1)},\ldots,a_{\alpha(n)}).
```

Using the Kronecker equality coefficients $`\delta`$, the same operation is

```math
(\alpha^*P)(a)
 =\sum_{b\in D^n}P(b)\prod_{j=1}^{n}\delta(b_j,a_{\alpha(j)}).
```

For fixed $`a`$, exactly one tuple $`b`$ satisfies all the equalities; its multiplier is one and every other multiplier is zero. The sum is therefore the displayed coefficient of $`P`$. This proves the formula over any unital semiring, including $`\mathbb B`$ and $`\mathbb N`$. Repeated values of $`\alpha`$ bind occurrences to the **same index**. They do not identify different domain elements with matching names or labels. The formula includes permutation, padding and repeated variables, without asserting that those operations have the same semantic role. [R18-G273, §3][R18-G273]

In particular, the diagonal pullback $`P(x,x)`$ retains the free $`x`$ wire. A trace $`\sum_xP(x,x)`$ removes it. Within the predicate-functor signature, $`c(P\mathbin{\&}I)(y)=P(y,y)`$: equality forces the existential first argument to be the remaining second one. Multiplying two independently contracted predicates usually does something else because their successful witnesses need not agree.

The distinction is visible even in a two-element domain. Let $`D=\{a,b\}`$, $`F=\{a\}`$ and $`G=\{b\}`$. Compare $`R_+=\{(a,b)\}`$ with $`R_-=\{(b,a)\}`$. Both interpretations have the same three separated truth values

```math
\exists x\,F(x),\qquad
\exists y\,G(y),\qquad
\exists x\exists y\,R(x,y),
```

all true. Their corresponding simple counts are also all one. Adding the exact domain cardinality two, or a scalar asserting two distinct elements, leaves the interpretations indistinguishable. Yet

```math
\exists x\exists y\,
  [F(x)\land G(y)\land R(x,y)\land x\ne y]
```

is true only for $`R_+`$. Its exact tensor expression is

```math
c\,c\,(F\mathbin{\&}pG\mathbin{\&}R\mathbin{\&}\neg I).
```

Trailing padding places $`F`$ on the first coordinate, leading padding places $`G`$ on the second, and the oriented relation and inequality are evaluated on those same coordinates until the final contraction. This calculation supplies both a failure and a repair: separate existence/count summaries, or symmetrizing $`R`$, lose the target; retaining the predicates on aligned oriented axes recovers it. The impossibility of decoding the separated summaries is the already established fibre criterion applied to this pair, not a second origin for that theorem. The example rejects this compression, rather than every structured decomposition, and settles no direction of metaphysical grounding. [R18-G273, §6][R18-G273]

### 1.7 Counting coefficients, support and negation

Boolean truth and natural-number counting use the same finite wiring but different addition. On $`\mathbb N`$ or $`\mathbb R_{\geq0}`$ define $`s(0)=0`$ and $`s(x)=1`$ for $`x>0`$. Then

```math
s(x+y)=s(x)\lor s(y),\qquad
s(xy)=s(x)\land s(y),\qquad s(0)=0,
\quad s(1)=1.
```

The first equality holds because a sum of nonnegative terms is positive exactly when a term is positive; the second holds because a product is positive exactly when both factors are positive. Induction over a finite network now shows that coefficientwise support commutes with products, contractions, permutations, equality wiring and padding. This is the standard positive-semiring mechanism behind the transport, with the provenance-semantics ancestry retained by the source. It intentionally forgets multiplicities and weights. [R18-G273, §§1, 5][R18-G273]

For flat products of characteristic atomic factors, natural-number contraction counts satisfying assignments to the contracted variables. Nested bag-style expressions can instead count combinations of witnesses or derivations. Repetition can add multiplicity, and a self-join can square a weight. Thus arithmetic operations need not preserve logical idempotence before support is taken. In a two-element domain, $`c_{\mathbb N}(1,1)=2`$ while $`c_{\mathbb B}(1,1)=1`$. More generally,

```math
c_{\mathbb N}p_{\mathbb N}P=|D|P,
\qquad
c_{\mathbb B}p_{\mathbb B}P=P
```

under the nonemptiness assumption. The direct inclusion of Boolean coefficients as $`0,1`$ is consequently not a homomorphism for these contractions. The exact positive comparison applies the support quotient **after** numerical arithmetic.

Negation requires another declared operation. Applying $`1-x`$ to a count of two gives $`-1`$, neither a natural number nor the intended false value. The correct numerical operation for this support interpretation is

```math
z(x)=\begin{cases}1,&x=0,\\0,&x>0.\end{cases}
\qquad s(z(x))=\neg s(x).
```

Adding this zero-test at every negation extends the structural induction to nested negative terms; alternatively one can Booleanize the relevant array before complementing it. The zero-test is nonlinear and is not supplied by positive semiring arithmetic. A network built from fixed nonnegative Boolean coefficients, finite sums and products is monotone in each input coefficient, by induction on its construction. Coefficient complement reverses $`0<1`$, so such a network cannot implement it on that one-coefficient representation. [R18-G273, §5][R18-G273]

A different representation can carry the missing information. Encode truth $`b`$ by the one-hot vector $`v_b(a)=1`$ iff $`a=b`$, with $`a\in\{0,1\}`$. For any finite truth function $`f`$, use the gate tensor

```math
G_f(a_1,\ldots,a_r,c)=1
   \quad\Longleftrightarrow\quad c=f(a_1,\ldots,a_r).
```

Contracting its input legs with $`v_{b_1},\ldots,v_{b_r}`$ leaves $`v_{f(b_1,\ldots,b_r)}`$, since precisely one input tuple survives. NOT is a two-leg swap, AND and OR use their truth tables, and a finite existential can be built from OR gates. Copy wires preserve shared intermediate truth values. This is a standard full Boolean-circuit construction. Its initial lift $`b\mapsto(1-b,b)`$ already includes both truth rails and is not monotone or semiring-linear in the original coefficient. It therefore does not refute the preceding obstruction, or make negation an undeclared real linear contraction. [R18-G273, §5][R18-G273]

### 1.8 Signed arrays and transported structure

The positive-support result does not extend to arbitrary signed coefficients. Nonzero support fails to preserve addition because $`1+(-1)=0`$ although each summand is nonzero. The positive-part predicate fails to preserve multiplication because two negative numbers have positive product. More generally, no unital semiring homomorphism from a nonzero ring to $`\mathbb B`$ exists: it would give

```math
0=s(0)=s(1+(-1))=1\lor s(-1),
```

a contradiction. Cancellation of the **difference** of two probability tensors can still prove equality of their marginals, as in §1.3. That signed difference is not thereby a positive relation or a truth predicate. [R18-G273, §5][R18-G273]

The distinguished domain basis also matters. With

```math
g=\begin{pmatrix}1&0\\-1&1\end{pmatrix},
\qquad P=\binom10,
\qquad\varepsilon=(1,1),
```

the changed coordinate vector is $`gP=(1,-1)^{\mathsf T}`$. Applying the unchanged covector gives zero. Transporting the covector as well gives $`\varepsilon g^{-1}=(2,1)`$ and restores the value one. This is ordinary passive numerical transport. The signed entries in the changed basis do not acquire the original entrywise membership interpretation. Domain permutations, by contrast, preserve the distinguished basis, equality tensor and augmentation and commute with the declared truth operations. No arbitrary-general-linear invariant truth interpretation is supplied.

There is an even simpler obstruction to a real linear existential evaluator on characteristic vectors when $`|D|\geq2`$. It would require $`L(e_a)=L(e_b)=1`$ for distinct $`a,b`$, and also $`L(e_a+e_b)=1`$ because the union is nonempty. Linearity gives two instead. Boolean contraction, a nonnegative calculation followed by support, and truth-wire encoding are different legitimate responses; ordinary real linear contraction alone is insufficient. [R18-G273, §5][R18-G273]

### 1.9 Plurality, inhabitation and the limits of the interpretation

The qualitative language need not erase numerical plurality. If $`F=D`$, the term

```math
c\,c\,(F\mathbin{\&}pF\mathbin{\&}\neg I)
```

is true exactly when $`|D|\geq2`$; with natural-number coefficients its value is $`|D|(|D|-1)`$. All objects can share the same unary $`F`$ label while inequality still distinguishes two from one. Quotienting the domain to one element per unary label would change the sentence's truth and is therefore invalid for this target. The model's indices retain its numerical elements, but indexing is not an independent metaphysical explanation of their individuation. Renaming the indices by a bijection changes no closed truth value. [R18-G273, §7][R18-G273]

Nonemptiness is another real premise. At $`D=\varnothing`$, the set $`D^0`$ still contains its empty tuple, so the scalar $`1_0`$ exists. Padding it gives an empty unary array; existentially summing that array gives zero. Thus

```math
c(p(1_0))=0\ne1_0
```

outside the nonempty-domain class. The separate convention that $`c`$ itself fixes scalars remains valid. An inhabited genus or capacity carrier does not imply an inhabited extension of its actual tokens; a many-sorted application must state inhabitation separately for every sort on which it uses dummy-variable elimination. Neither the empty tuple nor the tensor unit establishes an actual event, concrete resource or bearer. The productive and modal questions require the additional interpretations discussed in [Received Actuality, §§3–4](../foundations/received-actuality-and-intrinsic-necessity.md#3-from-an-original-resource-to-its-actual-bearer). [R18-G273, §7][R18-G273]

The transport is finite and extensional. The source report attributes the predicate-functor presentation to Dasgupta's 2009 text and distinguishes its inspected clauses from bibliographic references whose full texts were unavailable. Its reported 553,359 finite controls compare direct-set and array evaluations; they are historical checks, not executions performed for this exposition or a proof over unrestricted models. It also retains a development failure in a helper that captured a changing loop-domain instead of the fixed tensor domain; the reported repair concerns the helper, not a failed mathematical assertion. The proofs above, the explicit low-arity qualification and the counterexamples carry the scientific result without treating that finite count as a replacement for them. The earlier representation, fibre and parity results keep their own ancestry. No ontological priority, physical advantage or completed empirical test follows merely from this tensor encoding. [R18-G273, §§1, 8][R18-G273]


## 2. Finite channels: exact tensor closure and its limits

### 2.1 Fisher gradient descent produces a moment hierarchy

Let $`K`$ be an $`m\times n`$ column-stochastic matrix, with nonnegative entries and columns $`k_i\in\Delta_m`$. Zero rows are permitted. Let $`p`$ lie in the interior of the fine probability simplex, put $`q=Kp`$, and use the Fisher metric

```math
\langle a,b\rangle_p=\sum_{i=1}^n\frac{a_i b_i}{p_i},
\qquad
\sum_i a_i=\sum_i b_i=0.
```

For a fixed covector $`g\in\mathbb R^m`$, consider $`J_g(p)=g\cdot Kp`$. Its negative gradient is

```math
\dot p_i=-p_i\bigl(g\cdot k_i-g\cdot q\bigr).
\quad\text{(2)}\quad
```

Indeed, the displayed vector has zero sum and its Fisher pairing with every tangent vector $`a`$ is $`-\sum_i(g\cdot k_i)a_i=-dJ_g(a)`$. This verifies the constrained gradient directly. The Fisher–Shahshahani interpretation of replicator dynamics is classical; see [Harper](#references). The present concern is what a coarse record retains about that dynamics.

Collect identical columns into the distinct numerical support points $`\kappa_1,\ldots,\kappa_N`$, and let $`w_j`$ be the total fine mass of the corresponding class. Equation (2) preserves ratios inside each class and induces

```math
\dot w_j=-w_j(g\cdot\kappa_j-g\cdot q),
\qquad
q=\sum_jw_j\kappa_j.
```

Every strictly positive aggregate vector is realized by a strictly positive fine law. This aggregation concerns the specified numerical channel and controls. It does not identify source tokens, provenance, or fine labels for a later operation that distinguishes them.

Define $`M_0=1`$ and $`M_r=\sum_jw_j\kappa_j^{\otimes r}`$. Let $`\iota_g`$ contract exactly one tensor slot with $`g`$. Differentiating gives

```math
\dot M_r=-\iota_gM_{r+1}+(g\cdot M_1)M_r,
\qquad
\dot q=-(M_2-qq^{\mathsf T})g.
\quad\text{(3)}\quad
```

There is no factor $`r+1`$ in this contraction convention. Symmetry here reflects repeated numerical coordinates in a product; it does not symmetrize distinct semantic roles. Since contracting every slot with the all-ones vector gives one, all tensor grades are nonzero even for this finite support.

When both masses and atom positions vary, a labelled finite-law chart has a different gradient from a fixed-support weight simplex. Let w_i>0, Σ_iw_i=1, let the atom positions x_i be distinct, and give mass tangents Σ_iu_i=0 and position tangents v_i the squared norm Σ_i u_i²/w_i+Σ_i w_i|v_i|². For E=Σ_iw_iF(x_i), pairing against every tangent gives the gradient coordinates w_i(F(x_i)−E) and ∇F(x_i). Thus its negative gradient obeys ẇ_i=−w_i(F(x_i)−E), ẋ_i=−∇F(x_i), and Ė=−Σ_iw_i|∇F(x_i)|²−Var_w(F). For observables L_p=Σ_iw_ip(x_i), the same pairing gives the cometric Σ_iw_i[∇p(x_i)·∇q(x_i)+p(x_i)q(x_i)]−L_pL_q. These identities follow by differentiating E and L_p and using the zero-sum mass constraint. The source writes a three-atom planar matrix control of them; the finite-sum argument, not an unexecuted symbolic PASS, explains the formulas. Strict positivity of every mass, including the eliminated mass 1−w_0−w_1, is needed for the stated metric, and this distinct-atom chart does not by itself define a metric through collisions or a global law-space flow. [AFTER2634-FIRST25-002](../research/t20-v6-20261012/sources/c6b0d93461e6e825ddc7d3fe1069b519d6ff8f729a8e71f8ed569bf3fc93294f/check_exact.py#L37-L78)

The same finite-law calculation has a factored-mobility extension. Let M(x)=B(x)ᵀB(x) for a polynomial matrix B, put b=−M∇F and H=F+C. Then −b·∇H=|B∇F|² is explicitly a sum of squares, supplying the drift certificate used in the transport hierarchy when its other energy and path hypotheses hold. If M is pointwise positive definite, replace the positional part of the labelled metric by Σ_i w_i v_iᵀM(x_i)⁻¹v_i while retaining the Fisher mass term Σ_i u_i²/w_i. Pairing with every tangent gives ẋ_i=−M(x_i)∇F(x_i), the unchanged centered weight equation, and observable cometric L(∇pᵀM∇q)+Cov_L(p,q). This is a metric on the same positive-mass, distinct-atom chart, not an automatic metric through collisions. Singular factored mobility still supplies the displayed SOS energy certificate but is not called Riemannian; pointwise matrix positivity alone is not silently replaced by a supplied polynomial factorization. Nor does an arbitrary energy-controlled drift thereby become a gradient or convergent flow. The received author summary reports this extension at ordinary-proof scope, without a new kernel or finite-data claim. [AFTER3884-SIXTH25-140](../research/t20-v6-20261012/sources/3304c1da07dd5e2a28a58f2e576c64bc8dd1e81d600ee97cc94b2e1e7c1d24b4/REPORT.md#L3-L11)

The characteristic-law report adds a conditional tail estimate beyond this finite-atom identity. For a coercive polynomial F, let Φ̇=−∇F and μ_t=Φ_t#(exp(−∫₀ᵗF(Φ_s)ds)μ/Z_t). Retain the report's inherited limit data: μ_t→μ_∞ in each polynomial observable, F≥c* on its occupied support, h(t)=μ_t(F)−c*↓0, −h′=D=μ_t(|∇F|²)+Var_{μ_t}(F), and uniformly bounded fixed polynomial moments on every [t₀,∞), t₀>0. A finite cover of the compact level F=c* by local analytic gradient inequalities gives κ>0, ε∈(0,1] and θ∈[1/2,1) with |∇F|≥κ(F−c*)^θ throughout 0≤F−c*≤ε. If h≤ε/2, the complementary region has |F−μ_t(F)|≥(F−c*)/2. Thus, with C=min(κ²,ε^(2−2θ)/4), integration and Jensen give D≥Ch^(2θ). Consequently ∫ₜ^∞√D ds≤h(t)^(1−θ)/[√C(1−θ)]. The variance term is essential: a mixture of the zero-gradient points 1 and 0 for F=(x²−1)²/4 has positive mean gap and variance but zero gradient contribution. The displayed support and limiting properties are inputs inherited by this source, not consequences of a small mean gap or newly established here. This is a classical finite-dimensional analytic inequality transported to the stated law, not an infinite-dimensional Łojasiewicz theorem. [AFTER3384-THIRD25-051](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/07f993085f5e0066db587c0ef4fd9efd06c302179845007b886d3dcd8cafc352/RESULT.md#L7-L69) [AFTER3384-THIRD25-051](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/07f993085f5e0066db587c0ef4fd9efd06c302179845007b886d3dcd8cafc352/RESULT.md#L71-L110)

For that same law, B_t(p,q)=μ_t(∇p·∇q)+Cov_{μ_t}(p,q) gives μ′_t(p)=−B_t(p,F) and |μ′_t(p)|≤√B_t(p,p)√D(t). A finite bound M_p≥sup_{s≥t₀}[μ_s(|∇p|²)+μ_s(p²)] therefore yields |μ_t(p)−μ_∞(p)|≤√M_p h(t)^(1−θ)/[√C(1−θ)] in the tail. This concerns each fixed observable, not a uniform stable reconstruction over all degrees. The displayed velocity/reaction fields v=−∇F and α=μ_t(F)−F have finite action length on [t₀,∞) for every t₀>0. Finite initial μ(F) also bounds the initial segment by √(T[μ(F)−μ_T(F)]), but is only sufficient. An explicit contrary boundary uses F=x²/2, x=√(2Y), and initial density 1/[y(log y)²] for y≥e. With s=(1−e^(−2t))/2, exponentially tilted Y has variance at least c/[s²log²(2/s)] near zero; since ds=e^(−2t)dt, the action length dominates √c∫₀ ds/[s log(2/s)]=∞. Positive-time moments and finite tails still hold. Infinite length of this prescribed path is not infinite endpoint distance after optimizing over other paths; the report's predecessor identities and finite checks have not been rerun. [AFTER3384-THIRD25-051](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/07f993085f5e0066db587c0ef4fd9efd06c302179845007b886d3dcd8cafc352/RESULT.md#L92-L161)

The labelled metric cannot simply be carried unchanged through coincident atoms. At the single location 7, retain two labels of weights 1/3 and 2/3. Redistributing mass with tangent (1,−1) leaves every law observable unchanged to first order, yet its Fisher squared cost is 3+3/2=9/2. Keeping the masses fixed and using velocities (2,−1) likewise gives derivative [2/3−2/3]p′(7)=0 for every smooth test p, while its weighted squared cost is 2. These positive-cost invisible directions are a concrete failure of direct metric descent from the labelled presentation at collision. Merging labels or minimizing over their lifts is a further construction; neither a matrix inverse in the positive labelled chart nor finitely many moment identities supplies it automatically. The source requests these exact controls and nonnegative merger-remainder identities, but no symbolic run, complete quotient metric or extension across changing rank is asserted here. [AFTER2634-FIRST25-002](../research/t20-v6-20261012/sources/c6b0d93461e6e825ddc7d3fe1069b519d6ff8f729a8e71f8ed569bf3fc93294f/check_exact.py#L149-L160)

### 2.2 Exact finite closure on known support

**Theorem 1 (known-support closure).** For fixed distinct support points $`\kappa_1,\ldots,\kappa_N`$, moments through degree $`N-1`$ determine the aggregate law. Every higher moment is a fixed linear function of those moments, so (3) has an exact finite closure on its admissible moment image.

**Proof.** Choose $`v\in\mathbb R^m`$ outside the finitely many hyperplanes $`v\cdot(\kappa_i-\kappa_j)=0`$. Then $`a_j=v\cdot\kappa_j`$ are distinct. The contractions $`s_r=\langle v^{\otimes r},M_r\rangle=\sum_jw_j a_j^r`$ are available for $`0\le r<N`$. Write the Lagrange polynomials as

```math
\ell_j(z)=\prod_{\ell\ne j}\frac{z-a_\ell}{a_j-a_\ell}
        =\sum_{r=0}^{N-1}c_{jr}z^r.
```

Their values on the support are Kronecker deltas, hence $`w_j=\sum_r c_{jr}s_r`$. Therefore, for every degree $`k`$,

```math
M_k=\sum_{r=0}^{N-1}
       \left(\sum_{j=1}^N c_{jr}\kappa_j^{\otimes k}\right)s_r.
\quad\text{(4)}\quad
```

In particular, this replaces the top missing grade in (3). The resulting system is conjugate to the aggregate equation on the image of the positive simplex. Arbitrary tensor tuples outside that image are not admitted states. For $`N=1`$, the known support and degree-zero mass already determine the stationary law. ∎

For rational support points, a separating vector can be found by a finite exact search. Use $`v(t)=(1,t,\ldots,t^{m-1})`$. Each pair contributes a nonzero polynomial with at most $`m-1`$ roots. Some integer among $`0,\ldots,(m-1)N(N-1)/2`$ therefore separates all points. Arbitrary real support descriptions do not automatically give an effective equality test. Nor does exact interpolation imply stability: nearby projected support values can make its coefficients poorly conditioned.

The finite scalar recovery source isolates an algebraic result over any field K: for a supplied injective support a:Fin N→K, the record of degrees 0 through N−1 is a linear equivalence on arbitrary field-valued weights, including N=0. Its written proof derives a nonzero Vandermonde determinant from distinctness and uses the matrix inverse for both reconstruction identities. Every scalar observable, and every observable in a K-module, is then a fixed linear combination of the retained record. This does not assume positivity or normalization, but it also does not construct a separating projection for arbitrary multivariate support, certify admissible probability states, or establish tensor evolution or analytic continuation. It is a source-relative algebraic proof interface, not a newly executed verification. [NEXT-FL8-175](https://github.com/theislampill/orthemology/blob/ffca0abdf25079ef7639fe19776a21db60272fc4/research/t20-v6-20261012/sources/3cb16a5ba7f9daa392f407ae5496c0d8dfce9f59f4f2020b2c9a986d6413f96e/MomentRecovery.lean#L21-L137)

<a id="baseline141-projection-field-boundary"></a>

The separate finite-moment boundary source states recovery for empty and singleton supports, including dimension zero; an injectively enumerated zero-dimensional support necessarily has at most one point. Its general separating-projection interface assumes an infinite field. Over a finite field K, enumerating all of K² gives distinct support points but no injective scalar projection, since that would require |K|²≤|K|. This limits an extension of the projection argument to other fields, not the real-valued theorem above. The source depends on the imported projection/recovery theorem; no new compiled verification is asserted. [Exact source](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/085afba3f65a33d1ae7ea555dcfefefe93ad148f376e25259c953f58851ade31/Checks.lean#L11-L54)

The infinite-field separator can be constructed for any finite injective family x:Fin N -> (Fin d -> K). Associate to x_i the polynomial sum_j x_i(j) X^j. Each difference for distinct points is nonzero, so their finite product is nonzero; over infinite K there is a parameter t outside its roots. The direction v_j=t^j then separates all the points, equivalently yielding an injective scalar linear functional on this support, without assuming N or d positive. Feeding those distinct projected values to the imported recovery formula reconstructs arbitrary weights from moments of degrees0 through N-1 and consequently every observable sum with values in an additive group that is a K-module. The direction depends on the support. Infinity belongs to its existence proof, while recovery after separation uses the field interface; this is neither a universal direction nor a finite-moment theorem for arbitrary distributions. [L34-108](../research/t20-v6-20261012/sources/f9dd1ffaf94b2d4b6519a59f892c1700c57a59a7df0d3d8d860307a7dec8c3e5/SeparatingProjection.lean#L10-L41) [L34-108](../research/t20-v6-20261012/sources/f9dd1ffaf94b2d4b6519a59f892c1700c57a59a7df0d3d8d860307a7dec8c3e5/SeparatingProjection.lean#L45-L88) [L34-108](../research/t20-v6-20261012/sources/f9dd1ffaf94b2d4b6519a59f892c1700c57a59a7df0d3d8d860307a7dec8c3e5/SeparatingProjection.lean#L92-L122)

The cutoff is sharp in the worst case within this family of moment records. Place $`N`$ distinct points on the line $`\kappa_j=(x_j,1-x_j)`$. The equations $`\sum_jh_jx_j^r=0`$ for $`0\le r\le N-2`$ have a nonzero solution $`h`$. The full Vandermonde matrix implies $`\sum_jh_jx_j^{N-1}\ne0`$. Small positive and negative perturbations of uniform weights in direction $`h`$ are positive laws with equal lower moments and different next moments. This is not a lower bound on every conceivable state encoding. The original weights themselves are already a finite encoding.

The independent finite-atom controls distinguish known-support interpolation from identifying moving or unknown support. At three specified planar nodes, a separating scalar projection gives Lagrange factors eⱼ; the polynomials (xᵢ−xⱼᵢ)eⱼ² have zero values at every node and the prescribed first derivative at the selected node, with degree at most five. The known-support N−1 rule cannot be reused as an unknown-support identification rule. A positive Hankel matrix for each inspected Gaussian truncation has increasing rank, rather than a bound on the full moment rank. Likewise the control f(t)=t² satisfies (f′)²=4f while leaving zero; that inequality alone cannot justify persistence of a null direction. It is not a counterexample to the full hierarchy. The finite signed-energy examples instead differentiate explicit positive atomic weights proportional to exp(−∫h_t), including a genuinely changing polynomial h_t, so they corroborate those specified normalized paths without proving a general noncompact signed, time-dependent exhaustion theorem. All these controls were read, not executed, and the separate written universal proofs remain separate dependencies. [A1634-F25-234](../research/t20-v6-20261012/sources/61a80b65a3910f3551bcc2f868e932294fcd1a9d9f41804a32cf7b761bb12ead/check_independent.py#L60-L86) [A1634-F25-236](../research/t20-v6-20261012/sources/61f916c42e97d212f7632326394f44b6efdacdad00b87af54e8abb7328630a28/verify.py#L5-L56) [A1634-F25-237](../research/t20-v6-20261012/sources/620f3149b1bf5e0aa961569f8ea5273d50121e46841440275014ff07c0ec9ba4/check_review.py#L3-L48)

### 2.3 Exact continuation and a single discriminating experiment

For a locally finite piecewise-constant control $`g(t)`$, put $`U(t)=\int_0^t g(s)\,ds`$. Integration of the logarithmic weight ratios gives

```math
w_j(t)=
\frac{w_j(0)e^{-U(t)\cdot\kappa_j}}
     {\sum_\ell w_\ell(0)e^{-U(t)\cdot\kappa_\ell}},
\qquad
\mathcal T_a\mathcal T_b=\mathcal T_{a+b}.
\quad\text{(5)}\quad
```

Finite cumulative controls preserve strictly positive weights. The endpoint depends on the cumulative covector, although the intervening observation history can depend on the schedule. A scalar component parallel to the all-ones vector is a normalization gauge.

An exact three-label grouping control keeps the normalization visible. With equal prior weights and positive factors (1,1,z²), let the second group contain the last two labels. Its updated mass is (1+z²)/(2+z²), obtained from group prior masses (1/3,2/3) and the within-group mean factors (1,(1+z²)/2). Replacing that second mean factor by z would instead give 2z/(1+2z), and the difference is (1−z)²/[(2+z²)(1+2z)], positive except at z=1. The correct coarse factor therefore retains the same partition function A=(2+z²)/3. If Iᵢ=−log fᵢ and Pᵢ=wᵢfᵢ/A, direct substitution gives D(P∥w)+E_P I=−log A. Averaging multiplicative likelihood factors before taking their negative logarithm is thus different from substituting an averaged cost. This finite algebra identifies a specific grouping error; it neither establishes a general measure-theoretic entropy theorem nor supplies the unreceived predecessor's domain hypotheses. The symbolic body and its predecessor hash check were read without execution. [A1634-F25-249](../research/t20-v6-20261012/sources/6344132a4bfee6b40ffd70d0d0010c1643515f9fe13790ea499c04ca95c90436/check_exact.py#L8-L30)

Equal terminal energy need not restore equal labelled mass. The limit-control source uses w_i(t)=a_i exp(−K_i(t))/Σ_j a_j exp(−K_j(t)), with K_i′=F_i, so differentiating gives the replicator equation and −(log Z)′=Σ_i w_iF_i. Its double-well fixture F(x)=(x²−1)²/4 has, for z>0, x(t)=z/[z²+(1−z²)e^(−2t)]^(1/2) and integrated excess I(z)=(z²−1−log(z²))/8. Thus the labels starting at 1 and 2 both approach the spatial point 1, but equal initial weights approach the ratio 1:exp(−(3−log 4)/8). Spatial coalescence does not recover their separate histories. The source also specifies v_ε(t)=ε/[ε+(1−ε)e^(−δt)] for 0<ε<1 and δ>0: its fixed-time limit as ε tends to zero is zero, whereas its long-time limit for each positive ε is one. These explicit controls distinguish integrated-energy bias and absent-basin sensitivity; they do not establish the source's full analytic limit classification or an all-law convergence theorem. [G23-023](../research/t20-v6-20261012/sources/038608c92a952d8cf54b1641101a40fdbec6515c9925031789319cbe9e3a1c55/check_exact.py#L89-L134) [G23-023](../research/t20-v6-20261012/sources/038608c92a952d8cf54b1641101a40fdbec6515c9925031789319cbe9e3a1c55/check_exact.py#L156-L170)

**Theorem 2 (finite continuation equivalence).** For two aggregate laws on the same known finite support, the following are equivalent: equality of the weights; equality of all coarse histories under all admitted controls; equality under all constant controls; equality of the scalar response $`v\cdot q(t)`$ under one separating constant control $`g=v`$ on an initial interval of positive length; and equality of the moment record through degree $`N-1`$.

**Proof.** All implications from equal weights, and the moment implication, follow from (4)–(5). For the single-control implication let $`z_w(t)=\sum_jw_je^{-ta_j}`$. Then $`v\cdot q(t)=-(\log z_w)'(t)`$. Equal responses and $`z_w(0)=1`$ give equal normalizers on the interval. Their derivatives at zero through order $`N-1`$ give equal projected moments, and the Vandermonde matrix gives equal weights. ∎

The interval in the single-control implication need not begin at zero. Keep the same known finite support and the same separating constant control applied from the initial time, and suppose the two exact scalar response functions agree on any interval of positive duration. Their partition functions then satisfy Z_a=CZ_b there for a positive constant C. At an interior time t₀, derivatives of orders 0 through N−1 give Σ_j(a_j−Cb_j)e^(−t₀λ_j)(−λ_j)^r=0, where λ_j are the distinct projected support values and a_j,b_j are the initial weights. The Vandermonde matrix and its nonzero exponential diagonal are invertible, so a_j=Cb_j for all j; normalization gives C=1. This proves identification without analytic continuation from zero. It still requires an exact continuous response, fixed known support and the declared control; it supplies no finite-sample or noisy reconstruction bound. [S39:L52–62](../research/t20-v6-20261012/sources/2a8a3fbcbd12072e3785f3c5424f1390c0953db4a0b4f344b46cc88bf40bd67c/REVIEW.md#L52-L62)

The observation in this theorem is an exact function on an interval. It is not a finite sampled experiment or a noise-robust reconstruction procedure. With a nonlinear objective $`J(q)`$, one may substitute $`g=\nabla J(q)`$ when the usual finite-dimensional uniqueness hypotheses hold; a single fixed objective need not distinguish states. A constant objective distinguishes none.

Restricting the correction family can require strictly less information than the full known-support law. On the six columns κ=(x,y,1−x−y) with x∈{0,1/2} and y∈{0,1/4,1/2}, write q=Eκ and retain the additional scalar r=E[y·1{x=0}]. The two x-group masses are 1−2q_x and 2q_x. Under any positive likelihood taking values a,b on these groups, the normalizer is Z=a(1−2q_x)+2bq_x, the updated first coordinate is bq_x/Z, and the updated second coordinate is [ar+b(q_y−r)]/Z; the updated side coordinate is ar/Z. Hence (q,r) closes every finite sequence of these corrections, including the x-only exponential family. It does not recover all six weights: in lexicographic (x,y) order, adding or subtracting h=(1,−2,1,0,0,0)/24 from the uniform law preserves both q and r. Conversely q alone fails. Adding or subtracting k=(1,0,−1,−1,0,1)/24 gives strictly positive laws with q_x=q_y=1/4 but r=5/48 and 7/48. The correction a=1,b=1/2 makes their second output coordinates differ by −1/36. Finally, the expectation rows 1,x,y,y·1{x=0} are linearly independent: restricting a putative relation to the x=1/2 group first kills the y coefficient, and restricting to x=0 then kills the remaining group-y coefficient and constant. Thus one additional scalar expectation is sufficient and necessary within this linear-record contract. The source’s symbolic rank and evolution checks were not run; these finite formulas establish only the specified restricted-family result, not a lower bound on arbitrary encodings or a full-control quotient. [AFTER2634-SIXTH25-130](../research/t20-v6-20261012/sources/d9430c2638404329fbc1709d872043804b3b6f6a36fc9e8a1eb9d8e86ca85574/verify.py#L16-L60) [AFTER2634-SIXTH25-130](../research/t20-v6-20261012/sources/d9430c2638404329fbc1709d872043804b3b6f6a36fc9e8a1eb9d8e86ca85574/verify.py#L67-L73)

Complete output profiles for separate correction directions need not determine their compositions. On the nine support columns κ_ij=(i/4,j/4,1−(i+j)/4), 0≤i,j≤2, put v=(1,−2,1) and weights w_ij^±=1/9±v_i v_j/100. They are strictly positive and normalized. For every fixed i, Σ_jv_j=Σ_jjv_j=0 makes the κ-weighted perturbation sum vanish, and the corresponding statement holds for every fixed j. Consequently every positive reweighting depending only on i gives identical full output vectors under the two laws, as does every positive reweighting depending only on j. This includes their entire isolated constant-control profiles. But compose the admitted factors 2^(−i) and 2^(−j). Since Σ_i v_i2^(−i)=1/4 and Σ_i(i/4)v_i2^(−i)=−1/8, the two normalizers become 49/144±1/1600 and the first-coordinate numerators become 7/144∓1/3200. Their ratios differ. Each one-direction profile is therefore complete for its own update family while their stacked record loses the mixed correction. This is an ordinary finite-sum counterexample, not a failure of composition on the full weight law or a new execution of the source’s symbolic controls. [AFTER2634-SIXTH25-130](../research/t20-v6-20261012/sources/d9430c2638404329fbc1709d872043804b3b6f6a36fc9e8a1eb9d8e86ca85574/verify.py#L74-L99)

Restricted audit covariance can coexist with genuine coupling of moving atoms. For normalized positive weights w=(mr,m(1−r),1−m), 0<m,r<1, consider E=w1w2(x1−x2)²/(w1+w2) and the joint field wdot_i=−αw_i(∂E/∂w_i−Σ_jw_j∂E/∂w_j), xdot_i=−(∂E/∂x_i)/w_i, with α>0. Writing d=x2−x1 gives xdot=(2(1−r)d,−2rd,0), rdot=−αr(1−r)(1−2r)d² and mdot=−αm(1−m)r(1−r)d². A positive audit with factors(a,a,b) leaves r and x fixed and sends m to am/[am+b(1−m)]; differentiating this map verifies covariance of this displayed field. It does not commute with every singleton audit: at equal thirds and positions(0,1,2), the position velocities are(1,−1,0), whereas factors(2,1,1) give(2/3,−4/3,0). The example is neither uncoupled motion nor a theorem for arbitrary energies or audit groups. It is a direct finite-dimensional calculation from the specified energy; the source’s symbolic checks and external theorem bindings were not executed. [AFTER2884-FIRST25-009](../research/t20-v6-20261012/sources/e8a1ada4474cd5af57e12a77a6ce38702871b2fa5e007f4368a8432d4c12251a/check_exact.py#L54-L76) [AFTER2884-FIRST25-009](../research/t20-v6-20261012/sources/e8a1ada4474cd5af57e12a77a6ce38702871b2fa5e007f4368a8432d4c12251a/check_exact.py#L88-L126)

Known support is also essential to interpreting a single scalar response. The finite control takes support columns e1,e2 in one three-dimensional probability model and e1,(e1+e3)/2 in another. The direction v=(0,1,2) assigns projected values 0,1 in both models. For weights (1,r)/(1+r), r>0, both scalar responses equal r/(1+r), while the vector responses are respectively (1,r,0)/(1+r) and (1+r/2,0,r/2)/(1+r). In particular r=e^(−t) gives the same scalar response throughout a constant-control trajectory from equal weights, although the full vectors differ. This follows directly from the displayed columns and normalized weights; it does not contradict the theorem for one fixed known support, identify unknown support from that response, or turn the source’s symbolic assertions into an executed test. [AFTER2384-SECOND25-36](../research/t20-v6-20261012/sources/a8ecc7637d8db74354e9ce2d22d60fcec5fefd8f9d2b3ab481d4d776645af373/verify_independent.py#L107-L114)

An implicit energy-decreasing step has a separate root-selection obligation. The numerical-review source gives the exact one-dimensional counterexample φ(x)=−x²/2, u=0 and h=2. With discrete gradient D(u,v)=−(u+v)/2, the equation v−u+hD(u,v)=0 admits v=1 even though φ′(u)=0; its energy change is −1/2. Thus residual zero and descent alone do not force a stationary input to stay fixed. This does not say that the review's Picard iteration initialized at zero chooses that nonlocal root, or refute a locally selected consistent branch. The same file's nonquadratic convergence-rate, audit-covariance and random-chord controls are floating-point comparisons, including a numerical ODE reference, rather than a proof of universal second order or interval-certified error. [G23-066](../research/t20-v6-20261012/sources/09d04d744ddd57cf75c113adb5bcaa42334334b51286eb6319ac57c1d33e703a/independent_checks.py#L18-L65)

A different finite-law control separates raw moment Euler updates from moving actual atoms. For a Dirac mass at x with drift b, the raw first-order updates m₁=x+τb and m₂=xxᵀ+τ(xbᵀ+bxᵀ) have covariance −τ²bbᵀ; for τ>0 and b≠0 this destroys even quadratic positivity. Positive covariance is not sufficient for a multi-atom record: the two-atom control at −1 and 2, weights 1/3 and 2/3, F=x⁴/4 and τ=1/100 constructs a cubic Hermite test q whose squared value under the raw update is negative while its covariance is positive. The construction sets q to zero with zero derivative at the other atom and fixes q=1 and an adverse derivative at the selected atom; the resulting square probes information beyond covariance. Zero drift with nonnegative updated weights can still work, so this is not a blanket prohibition on Euler methods. These are explicit algebraic controls, not a newly executed symbolic check. [AFTER1384-01](../research/t20-v6-20261012/sources/2377d26e078cb8bd1c2c9b60c9ebd22e0303abed37dbcd7b5f5027116c8471a2/check_independent.py#L45-L95)

The reported finite-support obstruction has an elementary scalar extension beyond the two-atom control. Let a law have r distinct scalar atoms x_i with positive weights w_i, and apply the raw full-hierarchy Euler rule L⁺(p)=Σ_iw_i[p(x_i)+τ(b_i p′(x_i)+α_i p(x_i))], where τ>0 and all b_i,α_i are finite. If b_j≠0 at one occupied atom, Hermite interpolation supplies a polynomial q of degree at most 2r−1 with q(x_j)=1, q′(x_j)=d and q(x_i)=q′(x_i)=0 for i≠j. Then L⁺(q²)=w_j[1+τ(2b_jd+α_j)], which is negative for a suitable d. The square has degree at most 4r−2, so the updated full record is not square-positive for any positive step. For the normalized transport-and-selection generator, α_i is the centered reaction coefficient; it does not remove the obstruction. This written argument sharpens the reported degree bound without executing its controls. It does not prohibit Euler motion in a finite reconstruction chart followed by rebuilding the moments of an actual positive law. [AFTER3384-FIFTH25-115](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/research-v6/early_remaining/geometry_review_completion/REPORT.md#L35-L41)

The same obstruction extends to finitely many distinct atoms in any finite Euclidean dimension. Choose a linear form separating the support, use its Lagrange polynomial ℓj, and put q(x)=ℓj(x)²[1+v·(x−xj)]. Then q(xj)=1, while q and its gradient vanish at every other atom. Choosing v fixes the selected gradient to −C bj, so a nonzero drift bj makes the raw Euler value on q² negative for sufficiently large C. The degree remains at most4r−2. If every drift vanishes, square positivity instead holds exactly when every updated scalar mass wi(1+ταi) is nonnegative, as Lagrange isolation proves. Thus the result concerns Euler of all hierarchy coordinates, not motion in a finite reconstruction chart followed by rebuilding an actual law. [AFTER3634-THIRD25-73](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1b11866c5999c464e3fdbec244832995e6ee4bf34870e88a636bb48f77846f5c/gradient-discretization-independent-review-20261010__REVIEW.md#L9-L19)

For the law-valued move yi=xi−τ∇F(xi), a Hessian upper bound Li on the entire actual step segment yields F(yi)≤F(xi)−τ(1−τLi/2)||∇F(xi)||². Strict transport descent needs nonzero gradient and τLi<2; equality at2 gives only nonincrease. If Hess F≤LI on a common convex domain and τL<1, integrating along each chord gives ⟨T(x)−T(y),x−y⟩≥(1−τL)||x−y||² and hence injectivity and a separation lower bound. An absolute Hessian norm bound is unnecessary. Positive normalized reciprocal reweighting then preserves the actual law and support rank; with the common guard, zero total energy loss requires zero occupied gradients and equal occupied energies, not a minimum. For each fixed initial finite law and fixed polynomial test, the minimum used to center the rational factors is Lipschitz through ties, which suffices for offset cancellation and one-step O(τ²) consistency. None of these facts gives a uniform-in-degree error estimate, global convergence or recovery when the step/rule/domain is omitted. [AFTER3634-THIRD25-73](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1b11866c5999c464e3fdbec244832995e6ee4bf34870e88a636bb48f77846f5c/gradient-discretization-independent-review-20261010__REVIEW.md#L21-L45)

For a positive normalized finite law on [−M,M], the same source instead moves each atom by y=x−τx³ and reweights it proportionally to w/[1+τ(F(y)−c)], with F=x⁴/4, c=min F(y) and 0<τ≤1/(6M²) when M>0. The atom map has derivative at least 1/2 on that interval, preserves the interval and decreases F; the positive reweighting factor decreases with F, so its covariance with F is nonpositive and the reweighting also cannot increase mean energy. Thus the rebuilt law remains positive and normalized, distinct starting atoms do not collide, and duplicate atoms may be aggregated without changing the law. First-order expansion cancels the common offset and gives the selection term −w(F−E F), alongside the atom drift. These conclusions concern a fixed recorded step and normalization. The source separately gives two guarded input/step pairs with the same output, a collision caused by changing the quartic energy scaling while retaining the old guard, and, for the different nonconvex objective G(u,v)=(u²−1)²+(v²−1)², stationary nonminimum points (0,±1). Its finite rational examples and symbolic derivatives establish no global convergence, numerical stability or reversible recovery when the step is omitted. [AFTER1384-01](../research/t20-v6-20261012/sources/2377d26e078cb8bd1c2c9b60c9ebd22e0303abed37dbcd7b5f5027116c8471a2/check_independent.py#L25-L43) [AFTER1384-01](../research/t20-v6-20261012/sources/2377d26e078cb8bd1c2c9b60c9ebd22e0303abed37dbcd7b5f5027116c8471a2/check_independent.py#L97-L185)

For the normalized reciprocal reweighting just described, the energy drop has an exact finite sum-of-squares formula. Freeze the atom energies fᵢ, take positive weights wᵢ summing to one, and put dᵢ=1+η(fᵢ−minⱼ fⱼ), Z=Σᵢwᵢ/dᵢ and vᵢ=wᵢ/(Zdᵢ), with η≥0. Then Σᵢwᵢfᵢ−Σᵢvᵢfᵢ=(η/Z)Σᵢ<ⱼ wᵢwⱼ(fᵢ−fⱼ)²/(dᵢdⱼ). All denominators are positive. For η>0 the decrease is strict exactly when the occupied energies are not all equal; equality does not require zero energy. At η=0 the mathematical reweighting is the identity for every energy list, although the displayed helper rejects nonpositive steps. Given the fixed energies and step, the original weights are recovered by normalizing vᵢdᵢ. These statements concern normalized probabilities, not unnormalized killing masses, and do not remove the separate quartic atom-motion guard 0<τ≤1/(6M²) for M>0. Pairing the two ordered summands for each i,j proves the identity directly; the source's symbolic and rational controls were not executed. No global convergence or recovery with an omitted step is inferred. [AFTER2384-TENTH25-243](../research/t20-v6-20261012/sources/c4a8dea9ca3b786f7973682b30d9eccce77210587d1c942048b669679923c179/check_exact.py#L41-L76) [AFTER2384-TENTH25-243](../research/t20-v6-20261012/sources/c4a8dea9ca3b786f7973682b30d9eccce77210587d1c942048b669679923c179/check_exact.py#L201-L214) [AFTER2384-TENTH25-243](../research/t20-v6-20261012/sources/c4a8dea9ca3b786f7973682b30d9eccce77210587d1c942048b669679923c179/check_exact.py#L244-L275)

The moving-atom control also identifies the metric behind the simultaneous weight and position update. For a two-atom law with parameters (u,a,b), 0<u<1 and a≠b, it uses G=diag(1/u+1/(1−u),u,1−u) and E=uF(a)+(1−u)F(b). The negative gradient has weight component −u(F(a)−E) and position components −F′(a),−F′(b), giving dissipation −Eμ[(F′)²]−Varμ(F). Pushing this inverse metric through polynomial moments yields B(p,q)=Eμ[p′q′]+Eμ[pq]−Eμ[p]Eμ[q], not a diagonal collection of independent moment costs. For the first three scalar moments this gives Bᵢⱼ=ij mᵢ₊ⱼ₋₂+mᵢ₊ⱼ−mᵢmⱼ for 1≤i,j≤3, with determinant u²(1−u)²(a−b)⁸; the moment-coordinate Jacobian has determinant u(1−u)(a−b)⁴. At u=1/3,a=0,b=2 the mixed first/second-moment cometric entry is 40/9. [AFTER1634-N9-212](../research/t20-v6-20261012/sources/5eb8e384d14be96545cfe01fd81f9a4150475d032bcb6e86690f3c6b178bf0b8/check_exact.py#L9-L34) The full polynomial cotangent radical need not consist only of constants: z²(z−2)² and its derivative vanish on the support {0,2}. These finite symbolic controls supply an explicit chart and a support-dependent degeneracy, not a global nonsingular moment chart, complete-metric assertion or executed convergence proof. For positive weights and a nonnegative step, the rational frozen-potential update remains positive; it commutes with positive weight audits when the potential values and step selection are held fixed across the audit. [A1634-F25-234](../research/t20-v6-20261012/sources/61a80b65a3910f3551bcc2f868e932294fcd1a9d9f41804a32cf7b761bb12ead/check_independent.py#L27-L58) [A1634-F25-234](../research/t20-v6-20261012/sources/61a80b65a3910f3551bcc2f868e932294fcd1a9d9f41804a32cf7b761bb12ead/check_independent.py#L88-L107) [A1634-F25-229](../research/t20-v6-20261012/sources/6123760c05b86bc572aed9fd7fbd2e9b2bd4e7845de86e4d20f7cd09cd3670bd/contracts.py#L219-L232)

The reaction term is necessary even when every occupied atom is spatially stationary. In the independent control, take F(x)=(x²−1)²/4 and μ=(7/8)δ₁+(1/8)δ₀. Both support points have F′=0, so μ((F′)²)=0, while μ(F)=1/32 and Varμ(F)=7/1024. The full transport-plus-reaction action is therefore positive although its transport-only part vanishes. This is a direct finite calculation, not a contradiction of stationarity for the separate atom positions: the unequal energy levels still drive the weights. The same source requests a finite-atomic metric-speed/cometric comparison and annihilation of a constant polynomial. Those symbolic checks were not executed and establish no general metric completion, tail-length or convergence theorem merely by appearing in the review driver. [AFTER2384-FIFTH25-122](../research/t20-v6-20261012/sources/b4de183993ae08845d7ef46afb81d71030c8c1f3157aec88fb4b14fcd5223d64/check_review.py#L124-L148)

A separate finite-law scheme uses Pₘ(z)=Σⱼ₌₀ᵐzʲ/j! and damping a(v)=1/Pₘ(hv), with integer m≥1, h≥0 and nonnegative energy values. Reweighting positive masses by a and renormalizing keeps them positive; since a decreases with energy, the covariance identity gives nonincreasing mean energy. For a fixed factor a, any nonnegative audit likelihood with positive normalizer commutes with the damping, and n repeated identical steps multiply by aⁿ. Neither statement permits the energy baseline to be recomputed after the audit. With equal masses on energies (0,1,2), m=2 and h=1, damping gives factors (1,2/5,1/5); deleting the zero-energy atom then gives conditional masses (2/3,1/3). Deleting first and recentering the remaining energies to (0,1) instead gives (5/7,2/7). Thus fixed multiplicative commutation and support-dependent rebaselining are different contracts. The source’s exact finite loops also check local series coefficients and weighted maxima, while its telescoping comparisons use 80-digit numerical arithmetic with an explicit tolerance. These controls were read rather than run; they supply no general unbounded-support integrability, global convergence or formal-verification result. [AFTER1384-S5-074](../research/t20-v6-20261012/sources/2cb6e4b9d7d44aa9e43e8fcb3d8c6ee1a7ea0febe26395514e119e8452489cc4/check_independent.py#L12-L40) [AFTER1384-S5-074](../research/t20-v6-20261012/sources/2cb6e4b9d7d44aa9e43e8fcb3d8c6ee1a7ea0febe26395514e119e8452489cc4/check_independent.py#L41-L53)

Positivity of a discrete law does not itself preserve the audit symmetry of a chosen update. Write A_r(w)_i=w_i r_i/Σ_j w_j r_j and E_h(w)_i=w_i+h w_i(c_i−Σ_j w_j c_j). With w=(1/2,1/2), c=(0,1), r=(1,2) and h=1/2, direct substitution gives A_r(E_h(w))=(3/13,10/13), whereas E_h(A_r(w))=(2/9,7/9). Both are strictly positive normalized laws, but each coordinate differs in absolute value by 1/117. This is an order-of-operations defect, distinct from the raw-moment positivity failure above. The same control instead uses reciprocal factors 1/[1+h(F_i−min_j F_j)] with h≥0 on a fixed finite support. Those positive factors are nonincreasing in F and, when held fixed, commute with every strictly positive multiplicative audit by cancellation of the common normalizers. Strictly positive audits retain that support; this statement does not license deleting an atom and then recomputing the baseline. The rational spot checks neither test an existing integrator nor establish universal numerical convergence, and no run is asserted here. [AFTER1384-S8-118](../research/t20-v6-20261012/sources/31cce82c4cb5394a0b5807d63c34fc1b5b9c1b63db918aa3b1890aaa2a0d7011/independent_exact_controls.py#L16-L29) [AFTER1384-S8-118](../research/t20-v6-20261012/sources/31cce82c4cb5394a0b5807d63c34fc1b5b9c1b63db918aa3b1890aaa2a0d7011/independent_exact_controls.py#L36-L63)

Holding the step fixed is substantive even on two atoms. Let R_h(w) be the normalization of (w₀/(1+h),w₁), corresponding to the fixed potential values (1,0), and let the positive audit T normalize (w₀,2w₁). Select h(w)=w₀ and write A(w)=R_{h(w)}(w). At w=(1/2,1/2), the first coordinate of T(A(w)) is 1/4, while that of A(T(w)) is 3/11. Both updates remain positive; recomputing the step after the audit has changed the factor that was required to stay fixed. A separate nonlinear-score control sets F₀(w)=−2w₀²w₁ and F₁(w)=−F₀(w). At the same w, the first coordinate of DT(w)F(w) is −2/9, whereas F₀(T(w))=−4/27. Thus this nonlinear fixed-objective field is not covariant under the audit. These are direct finite calculations from the stated formulas, not a run of the imported inherited integrator or its symbolic controls, and they imply no general failure of target-only quotient descent. [AFTER2134-S7-170](../research/t20-v6-20261012/sources/9a327d05462b37dce8d73eb02bba461e9b9a52d1230493e9029a73a407a17505/independent_controls.py#L24-L41)

The joint finite-law control separates whole-energy descent from local accuracy. Write Vᵢ and Vᵢ′ for the before/after atom energies, cᵢ=(Vᵢ+Vᵢ′)/2, and E=ΣᵢwᵢVᵢ. The exact product identity gives E′−E=Σᵢ(wᵢ′−wᵢ)cᵢ+Σᵢ(wᵢ′+wᵢ)(Vᵢ′−Vᵢ)/2. If each internal step decreases its energy and wᵢ′ is proportional to wᵢ/P₂(h(cᵢ−b)), where P₂(z)=1+z+z²/2, h≥0 and b=minᵢcᵢ over the retained catalogue, both terms are nonpositive: the second by hypothesis and the first by the nonpositive covariance of c with its decreasing positive multiplier. This is a direct finite-law argument. In the quadratic fixture with initial positions (1,0) and weights (1/2,1/2), put γ=(1−h/2)/(1+h/2). Endpoint averaging gives first weight 1/[1+P₂(h(1+γ²)/4)], while the exact flow gives 1/[1+exp((1−exp(−2h))/4)]. Their difference is −7h³/192+O(h⁴). Using only the new energy instead gives 1/[1+P₂(hγ²/2)], whose error is h²/8+O(h³). Thus even an energy-decreasing endpoint-only choice can lose one order of local accuracy. These Taylor expansions concern this explicit fixture; the source's grouped numerical rates, implicit-solver controls and symbolic requests were not executed and do not establish universal global second order. [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L27-L63) [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L144-L170)

Coordinate convergence does not determine convergence of the represented laws in every metric. For the quadratic trajectory starting at one, n midpoint steps of size 1/n place a Dirac mass at γ(1/n)ⁿ rather than at exp(−1). Since log γ(h)=−2 artanh(h/2)<−h for 0<h<2, these atoms differ for every finite n, so their total variation distance is one, although their positions differ by O(n⁻²). A separate fixed-support example on {0,1} has one weight wₙ=1/[1+P₂(1/n)ⁿ] and exact weight w*=1/(1+e). The expansion n log P₂(1/n)=1−1/(6n²)+O(n⁻³) gives wₙ−w*=e/[6(1+e)²n²]+O(n⁻³). Here total variation is |wₙ−w*|, but the squared 2-Wasserstein distance is also |wₙ−w*| because the excess mass must cross unit distance. The Wasserstein distance consequently has order n⁻¹, not n⁻². These explicit formulas justify the two metric distinctions independently of the source's unexecuted rate diagnostics. The same midpoint map sends both −1 and 1 to zero at h=2, so positive normalized reconstruction and energy descent do not by themselves preserve distinct atoms or moment rank. No all-law error theorem or numerical replay is inferred. [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L155-L165) [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L223-L225) [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L267-L274)

The scalar quartic has a constructive contrast to the preceding root-selection warning. For V(x)=x⁴/4, rational x≠0 and rational h>0, set u=|x|>0 and f(z)=z−1+(hu²/4)(z³+z²+z+1). Then f(−1)=−2 and f(1)=2hu²>0, while f′(z)=1+(hu²/4)[3(z+1/3)²+2/3]>0, so there is exactly one real root z* in (−1,1). Put y*=sign(x)u z* and D=(y*³+y*²x+y*x²+x³)/4. The root equation gives y*−x+hD=0, and the quartic chain identity gives V(y*)−V(x)=(y*−x)D=−hD²≤0. Exact rational bisection starts from [−1,1], retains the sign bracket and halves its width unless it finds an exact midpoint root. After k halvings the width is 2^(1−k); hence for every such input it reaches u(hi−lo)≤h³/100 in finitely many steps. The returned rational midpoint position y consequently satisfies |y−y*|≤h³/200. Because the entire bracket stays inside [−1,1], it also satisfies |y|≤|x| and V(y)≤V(x), even before the requested accuracy is reached. The h=0 or x=0 branches instead return x exactly. These are direct existence, uniqueness, descent and finite-error arguments for this specified scalar quartic algorithm under exact rational arithmetic. They are not an all-potential or multidimensional solver theorem, a global-flow or convergence-order result, a machine-resource guarantee, or a newly observed execution. [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L35-L53) [AFTER1384-S13-239](../research/t20-v6-20261012/sources/424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff/check_joint.py#L171-L172)

### 2.4 When does the first moment suffice?

**Theorem 3 (coarse closure).** The vector field for $`q`$ in (3) depends only on $`q`$, for every covector $`g`$, exactly when the distinct support points are affinely independent.

**Proof.** Affine independence makes $`w\mapsto q`$ injective, so sufficiency is immediate. Conversely, form the matrix with columns $`(1,\kappa_j)`$, and let $`V`$ be its row space, viewed as functions on the support. A kernel vector $`h`$ can be used for small positive perturbations of any interior law. Equal first moments and equal coarse vector fields for all $`g`$ imply $`\sum_jh_j\kappa_j\kappa_j^{\mathsf T}=0`$. Thus every product of two coordinate functions lies in $`V`$, the annihilator of that kernel. Since $`V`$ is spanned by one and the coordinate functions, it is closed under products. A separating linear function belongs to $`V`$; its Lagrange polynomials give every point indicator. Therefore $`V=\mathbb R^N`$, and the matrix has column rank $`N`$. ∎

This is a criterion for descent of the specified vector field. It does not assert equality of an induced coarse metric with a chosen canonical Fisher metric.

Two examples show why the distinction matters. With columns $`(1,0),(0,1),(1/2,1/2)`$, weights $`(1/4,1/4,1/2)`$ and $`(3/8,3/8,1/4)`$ share $`q=(1/2,1/2)`$, but their second tensors are

```math
\begin{pmatrix}3/8&1/8\\1/8&3/8\end{pmatrix},
\qquad
\begin{pmatrix}7/16&1/16\\1/16&7/16\end{pmatrix}.
```

For $`g=(1,0)`$, their velocities are $`(-1/8,1/8)`$ and $`(-3/16,3/16)`$. On the same three-point support, writing $`Q=E[X]`$, $`S=E[X^2]`$, and $`\lambda=g_1-g_2`$ gives the exact closure

```math
\dot Q=-\lambda(S-Q^2),\qquad
\dot S=-\lambda\bigl((3/2-Q)S-Q/2\bigr).
```

The admissible weights at $`1,1/2,0`$ are respectively $`2S-Q`$, $`4(Q-S)`$, and $`1-3Q+2S`$, all positive. On four points $`0,1/3,2/3,1`$, the weights $`(5,9,3,7)/24`$ and $`(7,3,9,5)/24`$ instead share both first and second moments. Their third moments differ by $`1/54`$, and under unit linear damping their second mean derivatives differ by that amount, since $`Q''=E[X^3]-3QS+2Q^3`$. Equality of an immediate velocity is weaker than equality of a future trajectory. These finite results incorporate [the finite-channel proof][finite-source].

A different scalar correction flow distinguishes its output clock from the information in its output jets. Put z=Σᵢbᵢ and bᵢ′=−(z−1)bᵢ(1−bᵢ), and write pₖ=Σᵢbᵢᵏ. Direct differentiation gives pₖ′=k(z−1)(pₖ₊₁−pₖ). The selected control builds the output-jet polynomials Q₀=p₁ through Q₄ by this recurrence and requests the triangular coefficient ∂Qⱼ/∂pⱼ₊₁=j!(p₁−1)ʲ for j=1,…,4. Its finite inverse divides by those coefficients, so it is restricted away from z=1; the subsequent Newton reconstruction recovers an unordered multiset, not its labels. More concretely, b=(1/10,1/2,3/5) and b̃=(1/5,3/10,7/10) have equal z=6/5 and Σbᵢ(1−bᵢ)=29/50, hence equal z′=−29/250, but their displayed z″ values are 853/12500 and 889/12500. Dividing z′ by Σbᵢ(1−bᵢ) where this denominator is nonzero gives only −(z−1), which loses this distinction. At z=1 the entire field is zero, and the two different triples (1/10,3/10,3/5) and (1/5,7/20,9/20) both have jet (1,0,0). These explicit polynomial and rational controls do not prove arbitrary-order reconstruction, analytic observability or a global dimension lower bound; the symbolic program was read rather than run. [AFTER1884-S25-025](../research/t20-v6-20261012/sources/6681e33adb37ca200a81864c49c6bb1fb34b825dff955d76e98cb0caffc36edd/check_controls.py#L10-L51) [AFTER1884-S25-025](../research/t20-v6-20261012/sources/6681e33adb37ca200a81864c49c6bb1fb34b825dff955d76e98cb0caffc36edd/check_controls.py#L53-L107) A separately retained two-triple control supplies complementary finite co-support: its equal-total triples have different immediate aggregate rates for its two nonlinear mobilities, unlike its constant and affine choices, yet their time-normalized aggregate is again −(z−1). This is a different example from the equal-immediate-mobility, different-second-jet pair above and does not classify general mobilities; that control also remains unexecuted. [AFTER1884-T25-066](../research/t20-v6-20261012/sources/6be1d0c8d88150e0d25b6fce2b81acefd66714d7917ce70f8139ff401810c3c2/scalar_closure_controls.py#L5-L36)

The full independent review extends those finite jet controls by induction: differentiating the highest term j!(z−1)^j p_(j+1) is the only way to create p_(j+2), so the leading coefficient persists at every order. Away from z=1, the first n output-jet entries recover p₁,…,pₙ; Newton identities then recover the initial multiset, and a fixed strictly ordered chamber recovers the vector itself. An exact continuous encoder for the whole original-clock output on any fixed positive interval is consequently injective on each open incoherent chamber. Invariance of domain rules out fewer than n real coordinates, even with an arbitrary decoder; the identity encoder attains n. This is not a lower bound for one future scalar value, for approximate/noisy observations, for discontinuous encodings, or for coherent inputs, whose output is constant. If the initial sum is free side information, n−1 additional continuous coordinates are needed on the corresponding fixed-sum open pieces. For the normalized field V/S, dτ/dt=S yields dz/dτ=1−z, so one coordinate suffices: changing the clock changes the target. Labels outside an ordered chamber and actual epistemic warrant are not recovered. [After3634 DISCOVERY 214](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/25740e5fc024188a058bd68b043cdde26e0bbf2795816ce324fa87db628151ec/REVIEW.md#L88-L119)

The two-bit control separates retention of observable coordinates from preservation of a particular exponential leaf. Let x,y range over {−1,1}, start from the uniform law, and retain the observable space span{1,x,y}. The positive likelihood L=1+(x+y)/4 lies in that space, yet its normalized update has probabilities (1/8,1/4,1/4,3/8) in the order (−,−),(−,+),(+,−),(+,+). Its odds ratio changes from one to (1/8)(3/8)/[(1/4)(1/4)]=3/4. Consequently this update leaves the product leaf: membership of L in the retained linear space does not imply that log L has no interaction term. Indeed the xy coefficient of log L is log(3/4)/4. Multiplying L by 2/3 makes it a valid event likelihood without changing the posterior or repairing that failure. By contrast, a product likelihood of separate positive x and y factors cancels from the odds ratio. This explicit finite calculation distinguishes the likelihood from its logarithm; it is not a classification of all observable stabilizers, a general leaf-geometry theorem or a newly executed symbolic check. [AFTER1634-S2-041](../research/t20-v6-20261012/sources/4949238b7193ea22e41951819702f17320a281b50610c26b44c6605273744a33/independent_controls.py#L96-L107) [AFTER1634-S2-041](../research/t20-v6-20261012/sources/4949238b7193ea22e41951819702f17320a281b50610c26b44c6605273744a33/independent_controls.py#L126-L154)

The same two-bit setting has a positive restricted-family geometry that must not be confused with closure on every law sharing the unary record. For |ρ|<1 take pρ(x,y)=(1+ρxy)/4. Every such law has zero unary means, but its covariance is [[1,ρ],[ρ,1]]. Under the Fisher field for the linear objective E[x], the initial unary velocity is therefore (−1,−ρ), giving opposite transverse velocities at ρ=1/2 and ρ=−1/2 despite identical observed means. The exponential family proportional to pρ(x,y)e^(θ₁x+θ₂y) preserves odds ratio [(1+ρ)/(1−ρ)]²; its log-partition Hessian is the unary covariance, and its statistic tangent is Fisher-orthogonal to the moment fibre. In particular the exact linear-objective orbit proportional to pρ(x,y)e^(−tx) has means (−tanh t,−ρ tanh t). Thus a declared reference leaf supplies a coherent positive continuation while different leaves still disagree on the same initial unary record. These identities follow from the displayed four-state probabilities and exponential differentiation; the selected symbolic checks were not run. They do not make the leaf label observable, classify arbitrary finite observable spaces by a bounded rank census, or extend an interior Fisher calculation to singular probability boundaries. [AFTER1884-F25-019](../research/t20-v6-20261012/sources/65f195f5573411844423cc67bbafe471cec8edaadd5781563ccbf9d199ca3249/verify.py#L110-L172) [AFTER1884-F25-019](../research/t20-v6-20261012/sources/65f195f5573411844423cc67bbafe471cec8edaadd5781563ccbf9d199ca3249/verify.py#L198-L230)

<a id="finite-descriptors-and-law-closure"></a>

### 2.5 A fixed descriptor and a restricted family answer different questions

The known-support theorem has a finite domain built into its hypotheses: the locations of the atoms are fixed before the weights vary. The polynomial-state-closure guides concern a different universal claim. They report that, for a nonconstant polynomial objective on $\mathbb R^d$, no fixed finite vector of polynomial expectations containing a nonconstant coordinate has the stated universal, arbitrarily nonlinear vector-field closure over **all finitely supported laws**. Allowing a nonlinear function of the retained vector does not, by itself, recover information that varies inside one of its fibres. The author and accepted-preservation guides describe the same result, with the latter also retaining the independent rank-boundary control; they do not describe two additional closure theorems. [GUIDE105-G038] [GUIDE105-G083]

The elementary obstruction underlying such claims is already visible in §§2.2–2.4. If a record map $R$ and an observable velocity $V$ have $R(\mu)=R(\nu)$ but $V(\mu)\ne V(\nu)$, then there is no function $v$ on the record image with $V=v\circ R$: applying $v$ to the one common input would have to give two values. Conversely, constancy of $V$ on every record fibre defines a set-theoretic descended function. That converse supplies neither continuity nor a conveniently computable formula. The existing explicit three- and four-point examples prove particular failures of first- and second-moment closure without requiring a general polynomial impossibility theorem.

This distinction preserves the positive exceptions. A known finite support can be reconstructed by the interpolation argument above. A chart with a genuine bound on atomic rank has an additional promise. A family invariant under one specified quadratic flow can have exact finite-dimensional equations. None is the universal all-law contract. The preservation guide specifically warns that agreement of the first three moments does not identify a promised-rank representation: its rank-two versus rank-three comparison concerns different admissible support classes. A claimed rank bound must therefore be an input assumption justified independently of the moment match. [GUIDE105-G083]

A supplied positive two-atom law has an explicit reconstruction that illustrates this rank-restricted exception. Write μ=wδₓ+(1−w)δᵧ with 0<w<1 and x≠y, let a=m₁, b=m₂, c=m₃ and D=b−a²>0. Then S=(c−ab)/D=x+y and P=(ac−b²)/D=xy; the roots of z²−Sz+P recover the unordered support, and the mean recovers its weights. The identity S²−4P=(c−3ab+2a³)²/D²+4D keeps those roots distinct, while a²−Sa+P=−D places the mean between them. Its higher moments follow the two-support recurrence mₙ₊₂=S mₙ₊₁−P mₙ. The promise and the third moment both matter: (δ₋₁+δ₁)/2 and δ₋₂/5+4δ₁⁄₂/5 share mean zero and second moment one but have third moments zero and −3/2. This is direct algebra on the specified nondegenerate family, not authentication of an unknown law’s rank, a global chart through atom collisions, or a newly executed symbolic or kernel result. [AFTER1634-N9-212](../research/t20-v6-20261012/sources/5eb8e384d14be96545cfe01fd81f9a4150475d032bcb6e86690f3c6b178bf0b8/check_exact.py#L9-L34)

The general polynomial theorem's full operator specification, positive-law witnesses and proof are in the guides' linked result and review, which are not supplied with these short guides. The universal statement is retained here as their source-reported result, not as a deduction from the finite examples in this chapter. The reported float-coercion defect and subsequent exact-arithmetic correction likewise concern the historical control implementation. Correcting that implementation does not replace the ordinary universal proof, and reading its guide is not a new execution. [GUIDE105-G038] [GUIDE105-G083]

The separate exact-control body supplies the operator B_F p=−∇F·∇p−Fp and a concrete positive-law witness for the reported closure boundary. For F(x)=x²/2 and p(x)=x³, put mass binom(5,j)/16 on the even j in {0,…,5} for μ and on the odd j for ν. Both laws have moments of degrees zero through four equal to (1,5/2,15/2,25,90), while their fifth moments are 340 and 695/2. Since B_Fp=−3x³−x⁵/2, the normalized velocities E[B_Fp]+E[F]E[p] are respectively −605/4 and −155, differing by 15/4. Giving each law half its former mass and half the uniform law on all six points makes every atom positive while retaining equality of their lower moments; the velocity gap becomes 15/8. Thus this specified finite descriptor cannot determine that instantaneous velocity even in the common simplex interior. The source separately requests checks of finite degree families, degree-preserving multivariate directions and constant-objective or constant-descriptor exceptions. Dropping the killing term changes the example: drift alone sends x^k to −k x^k for this F. These explicit algebraic calculations do not complete the universal all-law theorem, justify analytic continuation, or establish a passing symbolic or kernel run. [AFTER1384-S8-128](../research/t20-v6-20261012/sources/336e93760d27548474b49753404d71d41dbaf14afd87e90d081bd3195f2e596b/verify.py#L30-L48) [AFTER1384-S8-128](../research/t20-v6-20261012/sources/336e93760d27548474b49753404d71d41dbaf14afd87e90d081bd3195f2e596b/verify.py#L60-L90) [AFTER1384-S8-128](../research/t20-v6-20261012/sources/336e93760d27548474b49753404d71d41dbaf14afd87e90d081bd3195f2e596b/verify.py#L92-L144) [AFTER1384-S8-128](../research/t20-v6-20261012/sources/336e93760d27548474b49753404d71d41dbaf14afd87e90d081bd3195f2e596b/verify.py#L146-L198)

The separate verification record supplies a smaller positive-law witness for the descriptor (E[x],E[x²],E[x³]). For F=x²/2, take μ=(δ₁+δ₃)/2 and ν=(δ₀+6δ₂+δ₄)/8. Both have first three moments (2,5,14), hence the same E[F]=5/2, but their fifth moments are 122 and 152. Since B_F(x³)=−3x³−x⁵/2, their normalized derivatives E[B_F(x³)]+E[F]E[x³] are −68 and −83. Thus this descriptor again cannot determine its own vector field, now with five union-support points rather than the preceding six-node binomial construction. The report describes the unnormalized separating functional as having positive mass 1/15 and B_F(x³)-value one; the displayed probability laws directly explain the normalized gap 15. This particular calculation neither proves the general finite-evaluation lemma nor replaces the all-degree obstruction. Its historical exact-arithmetic repair and reported tests were not rerun here. [AFTER3384-TENTH25-232](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/151d0c597b41e8a6bcca1fa0dd5e58225fa58158a0d672e9623e6d541057dcc2/VERIFICATION_NOTES.md#L5-L11)

The general polynomial obstruction has a direct proof beyond the preceding quadratic example. Let F be a nonconstant real polynomial on R^d, d≥1, of degree D≥1, and let a fixed finite descriptor consist of polynomial expectations with at least one nonconstant coordinate. Choose a retained polynomial p of maximal degree K≥1 and put M=D+K. For B_Fp=−∇F·∇p−Fp, the derivative term has degree at most M−2, so its degree-M leading form is −F_Dp_K, where F_D and p_K are the leading homogeneous parts. Their product is nonzero; choose v with F_D(v)p_K(v)≠0. Put mass binom(M,j)/2^(M−1) at jv on even j for μ and on odd j for ν, for 0≤j≤M. Both are probability laws. The Mth finite-difference identity makes their expectations agree for every polynomial of degree less than M, hence for every retained coordinate and for F. Applied to B_Fp, the same identity instead gives E_μ[B_Fp]−E_ν[B_Fp]=(−1)^(M+1)M!F_D(v)p_K(v)/2^(M−1)≠0. The normalized velocity V_F,p(λ)=E_λ[B_Fp]+E_λ[F]E_λ[p] has this same gap because its second term agrees for the two laws. Thus a function of the common finite descriptor would have to assign two different velocities to one input: no universal closure over all finitely supported probability laws exists for this operator, even with an arbitrary nonlinear decoder. This is an all-degree algebraic argument, not extrapolation from finite test cases. It also witnesses actual local trajectories: the finitely many characteristic equations x′=−∇F have a common small existence interval, and positive weights proportional to w_j(0) exp(−∫F(x_j(t))dt) (where w_j(0) are each law’s constructed initial masses) give precisely the displayed normalized derivative. Constant F and all-constant descriptors are excluded; unrestricted polynomial drifts need not exist globally. Neither source execution nor a symbolic or kernel PASS is asserted. [AFTER1384-S12-233](../research/t20-v6-20261012/sources/419fd3082fd153eaa6fc90a06a4b19861e55af6dde6a1798efa408dc3566704d/independent_controls.py#L20-L52) [AFTER1384-S12-233](../research/t20-v6-20261012/sources/419fd3082fd153eaa6fc90a06a4b19861e55af6dde6a1798efa408dc3566704d/independent_controls.py#L67-L71) [AFTER1384-S12-233](../research/t20-v6-20261012/sources/419fd3082fd153eaa6fc90a06a4b19861e55af6dde6a1798efa408dc3566704d/independent_controls.py#L138-L160)

The same leading-degree calculation gives a separate unnormalized linear-subspace boundary. For nonconstant F of degree D≥1 and any nonzero polynomial p of degree k, B_Fp=−∇F·∇p−Fp has degree k+D: its derivative term has degree at most k+D−2, while the nonzero product of the leading forms cannot cancel. Thus B_Fⁿp has degree k+nD, and these iterates are linearly independent. No nonzero finite-dimensional real polynomial subspace is B_F-invariant, including a proposed finite observable space containing 1. This elementary written corollary concerns the unrestricted polynomial ring and unnormalized linear evolution. It neither strengthens the preceding nonlinear all-law obstruction by declaration nor excludes fixed finite supports, restricted atomic-law families or nonpolynomial observables. Constant F and omission of the killing term change the argument. The source labels this note not yet independently reviewed; no execution or historical priority is inferred here. [AFTER3384-NINTH25-220](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/142d247e5d0bc5b7e8d9cce2275aa7b21b3574441a1d80259840ee82a2ed6e12/polynomial-linear-closure-boundary-20261011__NOTE.md#L3-L15)


## 3. Complete records on compact and unbounded spaces

### 3.1 Compactness and the absence of a universal finite cutoff

**Proposition 4 (compact numerical states).** On a fixed compact subset $`K\subset\mathbb R^d`$, the full polynomial record determines the law. It consequently determines every normalized linear exponential tilt.

**Proof.** Coordinate polynomials contain constants and separate points. Their algebra is uniformly dense in $`C(K)`$ by Stone–Weierstrass. Equal polynomial integrals therefore give equal continuous integrals and equal finite Borel measures. The exponential of any linear functional is bounded above and below on $`K`$, so the tilt is well defined. Alternatively, expand the exponential uniformly: if $`|x|\le B`$, the absolute series is bounded by $`e^{|u|B}`$, with another factor $`B`$ for the mean numerator. ∎

This applies to the aggregate distribution of any measurable map into a fixed finite-output simplex, even if there are infinitely many underlying source states. It does not recover distinctions lost by that map.

There is no universal finite degree on arbitrary compact supports. For any proposed cutoff $`D`$, choose $`D+2`$ distinct collinear points and perturb positive weights along the kernel of the truncated Vandermonde matrix, as in Theorem 1. Full compact determination and finite known-support closure are different statements. A single generic projection also need not identify an arbitrary multivariate compact law.

### 3.2 Actual half-line evolution

For $`\mu\in\mathcal P_\infty([0,\infty))`$, set

```math
A_r(t)=\int x^r e^{-tx}\,d\mu(x),\quad
Z(t)=A_0(t),\quad
m_r(t)=\frac{A_r(t)}{Z(t)},\quad t\ge0.
\quad\text{(6)}\quad
```

Every integral is finite and $`Z(t)>0`$. Dominated differentiation, including the right boundary derivative, gives $`A_r^{(k)}=(-1)^kA_{r+k}`$ and

```math
m_r'=-m_{r+1}+m_1m_r,\qquad
m_1'=-\mathrm{Var}_{\mathcal T_t\mu}(X).
\quad\text{(7)}\quad
```

At zero, the bound $`|(e^{-ux}-1)/u|\le x`$ justifies the first derivative; higher moments give the rest. The actual laws obey the semigroup rule and have exactly the same null sets as their initial law at every finite time.

In score coordinates, the Fisher pairing is $`E_\mu[ab]`$ for mean-zero square-integrable scores. The mean functional has gradient score $`X-E_\mu X`$, so (7) is its negative gradient trajectory, with squared speed equal to the variance. This does not make all positive densities an open Hilbert manifold or make every $`L^2`$ direction a positive two-sided perturbation.

Within a law-level class of positive densities relative to $`\mu`$, with almost-everywhere absolutely continuous log density satisfying $`\partial_t\log f_t=-(x-q(t))`$ and locally integrable $`q`$, integration and normalization force (6). That uniqueness statement is about the specified densities. It does not by itself classify arbitrary infinite moment sequences solving (7).

### 3.3 A full-moment ambiguity with different continuations

Let $`f(x)=e^{-(\log x)^2/2}/(x\sqrt{2\pi})`$ on $`x>0`$, and define

```math
d\mu_\pm(x)=f(x)
 \left(1\pm\frac12\sin(2\pi\log x)\right)\,dx.
\quad\text{(8)}\quad
```

These are distinct positive probabilities. For every integer $`n\ge0`$,

```math
E[e^{nZ}\sin(2\pi Z)]
  =e^{n^2/2-2\pi^2}\sin(2\pi n)=0,
\qquad Z\sim N(0,1).
```

Thus both have moments $`e^{n^2/2}`$. This is a classical lognormal Stieltjes-class mechanism, not a new discovery; see [Schmüdgen's moment lectures](#references), §2.1. For a general lognormal $`\log X\sim N(a,\sigma^2)`$, the phase must be $`2\pi(\log X-a)/\sigma^2`$ for the same integer cancellation.

**Proposition 5 (equal records, distinct dynamics).** The laws (8) have the same full initial moment sequence and every finite initial derivative of (7), but different full moment records at every positive time. Their means differ somewhere in every open positive-time interval.

**Proof.** First, a finite measure on $`[0,\infty)`$ is determined by its Laplace transform. Push it forward by $`y=e^{-x}`$ onto $`(0,1]`$, assign zero mass to zero, and observe that Laplace values at positive integers give its polynomial moments. The total mass and polynomial approximation on $`[0,1]`$ identify the pushforward, hence the original law.

Laplace transforms are analytic on $`\mathrm{Re}\,t>0`$. If the means of two tilted laws coincide on an open interval, the logarithmic derivatives of their normalizers coincide there. Analytic continuation makes those normalizers proportional on the positive half-line; their limits one at zero remove the factor. Laplace uniqueness would identify the original laws, contradicting (8).

At positive time $`t`$, a tilted law has the exponential moment $`E_{\mathcal T_t\mu}e^{tX/2}=Z(t/2)/Z(t)<\infty`$. Such a law is moment-determinate: any competitor inherits the exponential moment from its nonnegative series, its convergent moment expansion identifies the Laplace transform near zero, and uniqueness finishes the argument. Equality of the full tilted records at one positive time would thus give equal tilted laws. Multiplying by $`e^{tx}`$ and normalizing recovers equal initial laws, again a contradiction.

Finally, repeatedly differentiating (7) expresses every finite coordinate derivative at zero in finitely many initial moments. Hence all those derivatives agree. The initial mean and its first two derivatives are $`e^{1/2}`$, $`e-e^2`$, and $`e^{9/2}-3e^{5/2}+2e^{3/2}`$. The difference of the mean curves is flat at zero while failing to vanish on any positive interval. ∎

The formal series for the normalizer has terms $`(-t)^n e^{n^2/2}/n!`$. Their absolute ratio is $`|t|e^{n+1/2}/(n+1)`$, so its radius of convergence is zero. Positive-time analyticity does not supply analyticity at the boundary. No ordinary Banach-space uniqueness theorem is contradicted: no suitable locally Lipschitz vector field on a specified sequence norm was assumed.

An exact repair is to retain the Laplace profile itself:

```math
Z_{\mathcal T_u\mu}(s)=\frac{Z_\mu(s+u)}{Z_\mu(u)},
\qquad
E_{\mathcal T_u\mu}X=-\frac{Z_\mu'(u)}{Z_\mu(u)}.
\quad\text{(9)}\quad
```

Even the countable values $`Z_\mu(n)`$ determine the law set-theoretically, since they are the moments of $`e^{-X}\in[0,1]`$. That does not provide an error modulus for the unbounded observable $`-\log y`$ near zero. A complete exact record, a computable inverse, and a stable finite-data procedure remain distinct. The proofs and limits in this section incorporate [the unbounded continuation analysis][moment-boundary-source].

The actual Laplace-tilted family also gives a precise mean-coordinate comparison. For a nondegenerate law in the preceding half-line setting and positive parameters s,t, put F(t)=log Z(t), q(t)=−F′(t) and V(t)=F″(t)=Var_{μ_t}(X)>0. Positive-time Laplace differentiation gives q′=−V and V′=−κ₃, where κ₃ is the third centered moment. Thus q is locally invertible. Define ψ(q(t))=−tq(t)−F(t); differentiation gives ψ′(q)=−t, ψ″(q)=1/V and d(1/V)/dq=−κ₃/V³. The same Fisher line element is V dt²=dq²/V. With the truth-first convention D_H(a,b)=H(a)−H(b)−H′(b)(a−b), direct integration of log(dμ_s/dμ_t) yields KL(μ_s∥μ_t)=F(t)−F(s)+(t−s)q(s)=D_F(t,s)=D_ψ(q(s),q(t)). The natural-parameter arguments are reversed, while the original-mean arguments retain their order. Replacing q by −q without changing these formulas would alter the convention. Translating the starting tilt gives G(u)=F(a+u)−F(a): the normalization constant cancels from the corresponding derivatives and divergences, but remains necessary in the normalizer itself. These are ordinary consequences of the actual-law and differentiability premises, supplemented by the source’s unexecuted symbolic and finite Bernoulli controls. They give neither an inverse chart where V=0, recovery from an uncalibrated metric jet, nor analyticity of the boundary Taylor series at t=0. [AFTER2134-S6-144](../research/t20-v6-20261012/sources/968e36228f46cbc5d34a73278d5b5302f51798493d283a26bdc203e40ebd23eb/verify.py#L23-L84) [AFTER2134-S6-144](../research/t20-v6-20261012/sources/968e36228f46cbc5d34a73278d5b5302f51798493d283a26bdc203e40ebd23eb/verify.py#L100-L112)

For the lognormal pair (8), the endpoint comparison is stronger than a singular-chart warning. Put Lσ(t)=∫e^(−tx)dμσ, Fσ=log Lσ, qσ=−Fσ′ and Vσ=Fσ″ for t≥0. Every moment is finite, so dominated differentiation of the square-root densities in their common L² space gives a one-sided C∞ Fisher immersion with metric Vσ(t)dt². On each [0,b], Vσ is positive, Vσ(0)=e²−e, and Vσ(t)≤e²/Lσ(b); hence the displayed curve has length at most b√(e²/Lσ(b)). This is not a minimizing-distance claim or an open natural-parameter neighborhood of the boundary: every positive exponential moment of the original lognormal laws diverges. The two endpoints remain distinct full statistical states, with square-root inner product ∫√(1−¼sin²(2πlog x))dρ<1 and finite strictly positive mutual KL divergences. Their identification is imposed only by the retained moment record. [AFTER3634-THIRD25-69](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1b051b438726e2a41bda222f08dfd6e3d9a70499454c9ccef0a62ee9ddac74f6/RESULT.md#L25-L108)

At their common endpoint mean q₀=e^(1/2), invert qσ on a common left neighborhood and calibrate ψσ(q)=−tσ(q)q−Fσ(tσ(q)), so ψσ(q₀)=ψσ′(q₀)=0. Equal moments give equal full one-sided jets of Fσ,qσ,Vσ,ψσ and ψσ″ and equal bivariate endpoint jets of their Bregman divergences. Inverse-jet formulas use the same nonzero Vσ(0), so each derivative is uniformly computable from finitely many moments; no function-reconstruction modulus follows. Their actual metric, potential and boundary-anchored divergence germs nevertheless differ. Equality of V on an interval, integrated with the common F and F′ endpoint values, would identify the Laplace transforms and hence the laws. Equality of ψ or ψ″ similarly recovers the same inverse tilt and F, the same contradiction. Thus finite nonsingular one-sided geometry and every endpoint derivative still do not determine the actual continuation germ. The two mean vector fields dq/dt=−1/ψσ″(q) differ; uniqueness for one fixed locally Lipschitz vector field is not violated. [AFTER3634-THIRD25-69](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1b051b438726e2a41bda222f08dfd6e3d9a70499454c9ccef0a62ee9ddac74f6/RESULT.md#L110-L189)

Every finite covariance block of (X,…,X^d) is positive definite for either endpoint: zero variance of a nonconstant polynomial is impossible under an everywhere positive density. This gives no bounded inverse for an infinite covariance operator. The zero-radius Laplace Taylor series also rules out real-analytic extension of F,q,V in the declared natural affine coordinate and of ψ,ψ″ in the declared mean affine coordinate, by integration and the analytic inverse Legendre map. This is coordinate-relative: arc length makes any one-dimensional positive metric constant. It asserts neither intrinsic nonisometry nor impossibility of an abstract smooth extension. The two reference laws are in different scalar exponential leaves, and retaining their reference class or original certified tilted law with its control history is a distinct repair. Normalizer translation constants remain history data even though calibrated derivatives and Bregman divergences cancel them. [AFTER3634-THIRD25-69](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1b051b438726e2a41bda222f08dfd6e3d9a70499454c9ccef0a62ee9ddac74f6/RESULT.md#L47-L58) [AFTER3634-THIRD25-69](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1b051b438726e2a41bda222f08dfd6e3d9a70499454c9ccef0a62ee9ddac74f6/RESULT.md#L175-L219)

Positive-time smoothing does not ensure finite Fisher–Rao length from the initial law. In the unit-rate metric g_q(u,u)=Σu_n²/q_n, take p₀=1/2, p_n=1/[2n(n+1)] and losses V₀=0, V_n=exp(n²), n≥1. The normalized tilt q_n(t)=p_n exp(−tV_n)/B(t) has 1/2≤B(t)≤1, is continuous in total variation at zero and smooth in total variation at every positive time. Its speed is √Var_q(V), as follows from the radius-two square-root embedding into ℓ². On the disjoint intervals I_n=[1/V_n,2/V_n], the two variance terms involving atoms0 and n give Var_q(V)≥q₀q_nV_n², hence ∫_(I_n)√Var_q(V)dt≥1/[2e√(n(n+1))]. The harmonic lower bound makes every initial segment have infinite arc length, despite finite length on each delayed compact interval. There is no finite initial total-variation derivative: the singleton-zero difference quotient diverges. This is a continuous nonrectifiable orbit, not infinite endpoint distance; the nonnegative great-circle path between its square-root endpoints has finite Fisher distance 2 arccos(Σ√(p_nq_n(t)))<π. [After3884-185](../research/t20-v6-20261012/sources/35efa98e6673b44566fb1c6a26dffc4c6a699ec7a59356f60bac70414cb3a6fb/REVIEW.md#L12-L64)

A finite initial mean supplies a sufficient repair without requiring initial finite variance. For any probability p and measurable finite nonnegative loss V, let q(t) be its normalized exponential tilt and M(t)=E_q(t)V. At positive time M′(t)=−Var_q(t)(V). For 0<T<∞, if M(0)<∞, convergence of the tilted means at zero and integration give ∫₀ᵀVar_q(t)(V)dt=M(0)−M(T); Cauchy–Schwarz then bounds the initial arc length by √(T[M(0)−M(T)]). Finite mean is not necessary: retaining V_n=exp(n²), V₀=0, but taking p_n=1/[2ζ(4)n⁴] and p₀=1/2 gives infinite mean and Σ_(n≥1)√p_n<∞. Writing r_n(t)=√p_n exp(−tV_n/2) and q(t)^(1/2)=r/‖r‖₂ yields length at most (2/√p₀)Σ_(n≥1)√p_n, by the normalization derivative bound and Tonelli. Thus infinite mean alone cannot establish nonrectifiability; the separated-scale lower bound in the preceding example is essential. These ordinary analytic results neither identify psychological correction nor follow from a finite numerical divergence test. [After3884-185](../research/t20-v6-20261012/sources/35efa98e6673b44566fb1c6a26dffc4c6a699ec7a59356f60bac70414cb3a6fb/REVIEW.md#L66-L99)



<a id="full-density-and-gaussian-geometry"></a>

### 3.4 Full-density tangents and an invariant Gaussian family

A finite family of laws can inherit geometry from an ambient law space without being a sufficient state for every ambient evolution. The Gaussian-geometry guides distinguish precisely these claims. Their metric is induced by a minimum over **all admissible square-integrable density tangents**, rather than by minimization over a chosen polynomial ansatz. They report a one-dimensional metric and curvature, a multivariate positive-definite-matrix cometric, and the quadratic gradient flows that genuinely leave the Gaussian family invariant. Noncommuting precision evolution belongs to the multivariate claim and cannot be inferred by treating the matrices as scalars. [GUIDE105-G011] [GUIDE105-G094]

There are two different operations here. Restricting an ambient tangent norm to a tangent of a parametrized family asks what the least ambient cost of that same tangent is. Evolving the ambient law asks whether its actual vector field stays tangent to the family at every point of the trajectory. The first question does not answer the second. Even a correct induced Riemannian metric consequently gives no finite polynomial closure for arbitrary laws. Nor does a distance intrinsic to the Gaussian submanifold equal the unrestricted endpoint distance merely because both are obtained from an action: the latter permits additional paths, and equality needs a separate minimizing-path argument. The inherited Hessian and Bregman results concern their own metrics and remain intact. [GUIDE105-G011] [GUIDE105-G094]

The full functional minimization and the multivariate formulas are not contained in the short guides received here. Their existence is a source report, with the analytic argument assigned to the original result and review. Exact algebraic controls can check formulas after those analytic premises are supplied; they do not show that an unexamined ansatz exhausts an infinite-dimensional admissible class. The distinction between the historical original-aware and portable control counts concerns omitted original-location integrity checks, not permission to omit mathematical hypotheses. [GUIDE105-G011]

The exact-control body supplies candidate formulas absent from the short guide. For a scalar Gaussian of variance v>0 and requested mean/variance velocity (M,V), it chooses the centered potential f(x)=a x+b(x²−v), with a=M/(1+v) and b=V/[2v(v+2)]. Its requested full-density identity and action calculation give the candidate quadratic form M²/(1+v)+V²/[2v(v+2)]. The multivariate specification uses mean operator I+Σ and covariance operator L_Σ(A)=2(AΣ+ΣA+ΣAΣ); its diagonal two-dimensional control retains the coefficient 2(λ_i+λ_j+λ_iλ_j), including the off-diagonal multiplicity in the quadratic form. The noncommuting matrix fixture is a separate control, not a scalar substitution. Null-field orthogonality and Pythagoras are requested only for scalar monomials of degrees 0–8 and one matrix polynomial family of degrees 0–4. Those finite requests expose the intended geometry but do not establish minimization over every admissible L² field, an arbitrary-dimensional theorem or an observed passing run. [G21-214](../research/t20-v6-20261012/sources/1f715fe8055e9f3ce79cb9135a73a7d68dadba37f42d8f691e7a46dd2bf67cde/verify.py#L49-L205)

The selected independent Gaussian control extends the displayed unit-weight formulas to separately weighted transport and reaction. For positive-definite Σ, symmetric A, α,β≥0 with α+β>0, and a centered potential aᵀx+xᵀAx−tr(AΣ), its proposed mean and covariance tangents are h=(αI+βΣ)a and LΣ(A)=2α(AΣ+ΣA)+2βΣAΣ. The corresponding quadratic action is aᵀh+tr(A LΣ(A)). In a diagonal covariance basis with eigenvalues λᵢ>0, solving LΣ(A)=B gives Aᵢⱼ=Bᵢⱼ/{2[α(λᵢ+λⱼ)+βλᵢλⱼ]}; the Frobenius pairing counts each symmetric off-diagonal entry twice. The source additionally requests inverse-mass scaling of the shape action when the potential coefficients are divided by a positive mass and the action is multiplied by that mass. Its inverse formulas require the nondegeneracy condition α+β>0: the source's nonnegative symbol declarations alone also admit α=β=0, where those denominators vanish. The full-density and action comparisons are two-dimensional symbolic controls, not a minimization over every admissible field, a general-dimensional analytic proof or an observed symbolic execution. [AFTER1884-T25-065](../research/t20-v6-20261012/sources/6bc0cb3dc073e46e55d04e7258766eea93afc94d3bccd6e4466e373479c9a25a/check_independent.py#L28-L72)

### 3.5 Equal initial variance rates need not give equal continuations

The quartic diagnostic gives a particularly sharp warning about a locally plausible restriction. For the objective $F(x)=x^4/4$ and a centered initial Gaussian of variance $v>0$, the guide reports equality of the initial variance rates in the actual-law and restricted-Gaussian models, but a positive gap between their right-hand second derivatives:

```math
3v^3(7v^2+32v+16)>0.
```

At $v=1$ the stated gap is $165$. Equality of one initial derivative therefore does not identify the actual continuation. The reported second-order discrepancy does not contradict the exact quadratic invariant-family result: the objective and the invariant-family premise have changed. [GUIDE105-G061]

The right-hand differentiability is substantive. The independent argument described in the guide uses domination along weighted characteristics to justify the actual-law right-$C^2$ assertion. Formal differentiation of finitely many moments, or agreement of symbolic expressions, would not establish that analytic premise. The full domination argument is an unreceived dependency of this particular diagnostic. The guide also preserves an initially failed structural-equality assertion whose printed mathematical values agreed; that failure is an implementation comparison issue, not a counterexample to equality of those values. Neither the failure nor its corrected finite controls is substituted for the analytic proof. [GUIDE105-G061]

For the displayed scalar quartic characteristic, the missing right-differentiability premise can be supplied directly under a centered Gaussian initial law. Let X have variance v>0, d=1+2tX², q=tX⁴/(4d), w=exp(−q), h=X²/d, Z=E[w] and N=E[hw], for t≥0. Since d≥1 and 0<w≤1, the absolute first and second time derivatives of w are bounded respectively by X⁴/4 and X⁶+X⁸/16. Those of hw are bounded by 2X⁴+X⁶/4 and 8X⁶+2X⁸+X¹⁰/16; h itself is bounded by X². All bounds are Gaussian-integrable and independent of t. Pointwise continuity of these derivatives and dominated convergence therefore make Z and N right-C² at zero, with Z>0, so the normalized second moment N/Z is right-C² as well. The characteristic X/√d is odd and w even, so its weighted mean is zero. Using Gaussian even moments gives variance derivative −6v²−3v³ and second derivative 120v³+186v⁴+48v⁵. Differentiating the restricted variance field f(v)=−6v²−3v³ instead gives f′(v)f(v)=72v³+90v⁴+27v⁵, leaving the positive gap 3v³(v+4)(7v+4), equal to 165 at v=1. This is an ordinary analytic argument for this explicit normalized characteristic family, not receipt of the referenced review, a new symbolic run, or a general PDE existence, uniqueness or arbitrary-initial-law theorem. [AFTER1884-Z25-230](../research/t20-v6-20261012/sources/814864a0ec9d94226db354c23f2bcee9c7b4e0dad3fdca306aa45f4eb29aab23/independent_check.py#L5-L13) [AFTER1884-Z25-230](../research/t20-v6-20261012/sources/814864a0ec9d94226db354c23f2bcee9c7b4e0dad3fdca306aa45f4eb29aab23/independent_check.py#L19-L40)

The quartic control also specifies the whole-density residual that the first two moments miss. At the centered Gaussian, it requests that the full score minus the Gaussian variance score equal −(1/v+1/4)(x⁴−6vx²+3v²), with variance velocity −3v²(v+2). The residual has zero integrals against 1, x and x²: odd centered Gaussian moments vanish, and the even-moment identities E[x²]=v, E[x⁴]=3v² and E[x⁶]=15v³ give the two remaining cancellations directly. Nevertheless its quartic coefficient is nonzero for v>0. Thus matching those instantaneous moments can conceal a nonzero density tangent. This elementary finite-polynomial comparison does not supply the actual-law right-differentiability or the continuation argument behind the second-derivative gap above; the program’s requested symbolic checks have not been executed here. [G21-214](../research/t20-v6-20261012/sources/1f715fe8055e9f3ce79cb9135a73a7d68dadba37f42d8f691e7a46dd2bf67cde/verify.py#L113-L120)

The independent radial control supplies an exact characteristic calculation for the fixed quartic objective without asserting the missing Gaussian analytic bridge. Write R=|x|² and F=R²/4. Under x′=−Rx, a starting squared radius r follows q_t(r)=r/(1+2tr), and the accumulated killing is K_t(r)=r[1−(1+2tr)^(−1)]/8, since K′_t=q_t²/4. Thus a finite atomic law moves each atom to x/√(1+2t|x|²), multiplies its mass by exp(−K_t(|x|²)), and then normalizes. For every radial polynomial power n, differentiation gives the unnormalized generator −2nq_t^(n+1)−q_t^(n+2)/4; normalization adds the mean-killing term. At t>0 every finite starting radius satisfies q_t<1/(2t), and the bound is sharp as r tends to infinity. On the whole radial image interval the inverse is r=y/(1−2ty); its pole at the excluded endpoint prevents a polynomial inverse on that interval, although a finite support can of course admit polynomial interpolation. These identities and the finite atomic construction distinguish transport-plus-killing from pure reweighting. They do not prove that every square-positive polynomial hierarchy has an actual law, justify differentiating arbitrary initial-law integrals, or certify the all-polynomial theorem referenced by the unexecuted control program. [AFTER1634-F25-087](../research/t20-v6-20261012/sources/4eb2cb9349b28ce8279815b98dbd47717136ec95b012324be3069e969450659b/check_independent.py#L7-L33) [AFTER1634-F25-087](../research/t20-v6-20261012/sources/4eb2cb9349b28ce8279815b98dbd47717136ec95b012324be3069e969450659b/check_independent.py#L49-L68)

The full radial-quartic argument supplies a specific reverse-realization theorem beyond the finite-law characteristic calculation. Fix d≥1 and a nontrivial horizon 0<T≤∞, put R=|x|² and F=R²/4, and suppose L_t is a real linear functional on every polynomial, with L_t(1)=1, L_t(q²)≥0 and every coordinate C¹ through zero (with a continuous right derivative there). Assume L′_t(p)=−L_t(R x·∇p)−L_t(R²p)/4+L_t(R²)L_t(p)/4 throughout. No rank, initial representing-law or initial tail-growth hypothesis is imposed. Set a(t)=exp(−∫₀ᵗL_u(R²)du/4), A_t=a(t)L_t and a_n=A_t(Rⁿ). Since each Rⁿ is a sum of squares, a_n≥0, and the hierarchy gives a_n′=−2n a_(n+1)−a_(n+2)/4. Iterating the integrated inequality a_j(s)≥2j∫ₛᵗa_(j+1)(u)du for j=1,…,n−1 cancels the simplex factorial against the product of the j factors. Hence a_n(t)≤L₀(R)(2t)^(1−n) for n≥1 and t>0. Marginal even moments inherit this geometric bound, so the multivariate Carleman existence-and-determinacy theorem yields a unique positive-time representing law. Markov bounds place it in the closed ball R≤1/(2t). This derives representation from full square positivity before making a nonpolynomial flow substitution; when L₀(R)=0 the same argument yields the point mass at zero. [After3884-184](../research/t20-v6-20261012/sources/35ecab255d407a8b8405471b60f52c8f37d35fae6cd5f2b9a4c16573926c4e26/RESULT.md#L7-L30) [After3884-184](../research/t20-v6-20261012/sources/35ecab255d407a8b8405471b60f52c8f37d35fae6cd5f2b9a4c16573926c4e26/RESULT.md#L48-L98)

The remaining steps identify one initial law rather than only separate compact representatives. On each interior time window the measures ν_t=a(t)ρ_t have common compact support and bounded mass. Polynomial approximation first gives weak continuity; exponential Taylor tests and Fourier inversion extend their polynomial equation to ∂tν=−div(−Rxν)−Fν. Applying its time-dependent test rule to the cutoff backward characteristic E_(t−s)f∘Φ_(t−s), with Φ_t(x)=x/√(1+2tR(x)) and E_t(x)=exp(−R(x)[1−(1+2tR(x))^(−1)]/8), gives ν_t=(Φ_(t−s))#(E_(t−s)ν_s). Uniform higher radial moments near zero give tightness and polynomial uniform integrability, so a subsequence recovers a probability μ representing L₀ and the same law satisfies ν_t=(Φ_t)#(E_tμ) at every positive time. The flow is a homeomorphism onto the open ball R<1/(2t), and E_t is strictly positive at each finite point. Inverse pushforward and division by this weight are injective on the actual range, so the initial μ is unique for the supplied path and no independent boundary inflow remains. The boundary sphere has zero mass, although it can belong to the topological support. This argument does not assert a stable inverse or surjectivity onto all laws in the closed ball. [After3884-184](../research/t20-v6-20261012/sources/35ecab255d407a8b8405471b60f52c8f37d35fae6cd5f2b9a4c16573926c4e26/RESULT.md#L100-L190) [After3884-184](../research/t20-v6-20261012/sources/35ecab255d407a8b8405471b60f52c8f37d35fae6cd5f2b9a4c16573926c4e26/RESULT.md#L240-L246)

Conversely, every initial probability with all absolute polynomial moments generates the displayed normalized quartic path: |Φ_t(x)|≤|x| and 0<E_t≤1 dominate the integrands and their derivatives by fixed polynomials on compact time windows, including right differentiation at zero. Thus paths with a fixed initial full moment functional are in bijection with its representing-law fibre, and distinct laws in that fibre have different full records at every positive time. A supplied path nevertheless determines its law and has a unique extension to all t≥0. Finite initial full Hankel rank forces a finite atomic law whose distinct atoms cannot collide and whose weights remain positive, so constant rank is a conclusion here rather than a full-path assumption. The represented dynamics satisfies dL_t(F)/dt=−L_t(R³)−Var(F); positive-time confinement gives L_t(F)≤1/(16t²) and weak convergence to δ₀. Finite-time injectivity therefore coexists with a common information-losing weak limit. These are results for this fixed radial quartic generator, not arbitrary nonlinear gradients, a new infinite-dimensional Riemannian theorem, or fresh kernel verification; primary theorem attributions remain those of the authored report. [After3884-184](../research/t20-v6-20261012/sources/35ecab255d407a8b8405471b60f52c8f37d35fae6cd5f2b9a4c16573926c4e26/RESULT.md#L192-L248)

<a id="full-law-marginal-contracts"></a>

### 3.6 Coarse action and a whole marginal constraint

The full-law coarse-graining guides describe a transport-and-reaction action contract supported by Hilbert-space projection, distributional arguments and cutoff or well-posedness hypotheses. Their universal claims are ordinary written mathematics. The finite controls concern exact algebra and identity checks. A contraction of action, an attained endpoint minimum, an evolution equation and uniqueness of that evolution are distinct assertions; none should be inferred merely from another's name. The historical initial failed checker remains evidence of its own failure, while the corrected result has its own scope. The reviewer-supplied strict-norm residual example is participating work, not independent corroboration of that same example by its originator. [GUIDE105-G005] [GUIDE105-G007]

The separate coarse-action control exposes three losses rather than treating contraction as an evolution theorem. For a finite weighted group, write uᵢ=Dᵢvᵢ and let ū and ā be its weighted conditional means. Expanding squares decomposes fine minus coarse action into Σwᵢ(‖vᵢ‖²−‖Dᵢvᵢ‖²), Σwᵢ‖uᵢ−ū‖² and Σwᵢ(αᵢ−ā)²; nonnegativity of the first term needs contraction of the Dᵢ. The source's three-atom fixture includes both discarded spatial directions and conditional variation. For a coisometric projection P, PPᵀ=I gives ‖Pᵀg‖=‖g‖ and P(I+Σ)Pᵀ=I+PΣPᵀ; its correlated Gaussian quadratic fixture requests the corresponding projected mean and covariance equations. These premises matter. The contraction x↦x/2 at the displayed Gaussian state instead gives projected mean/variance velocity (−5/4,−3/2), whereas the canonical coarse velocity is (−2,−3); their determinant is 3/4, so not even a scalar time change identifies them. Likewise T(x)=(2/3)sin x+(1/6)sin 2x has T(0)=T(π)=0 but derivative-square values 1 and 1/9, obstructing a Gram coefficient determined by the output alone. These are explicit algebraic distinctions in an unexecuted control body, not a proof of general-law projection or existence. [AFTER1384-S6-076](../research/t20-v6-20261012/sources/2d6240fb03e257f60669edefb2dfe367df1c62f2af5b46d1938c4d5482b8699f/verify.py#L14-L56)

A correlated Gaussian gives a concrete failure of unconstrained marginal evolution to follow the marginal objective. For Σ₀=[[1,c],[c,1]], 0<|c|<1, and identity target covariance, the source writes Σ̇=2I−Σ−Σ², so initially Σ̇₁₁=−c² and Σ̇₁₂=−3c. The first marginal is already N(0,1), whose own canonical KL flow is stationary, yet the projected joint flow leaves that marginal. The written solution has common diagonal a=1−3c²q(1−q)/(9−c²(1−q)²) and off-diagonal 9cq/(9−c²(1−q)²), where q=e^(−3t). At c=q=1/2 its marginal variance is 140/143. Meanwhile the initial derivative of marginal KL is zero and its quadratic Taylor coefficient is c⁴/4, so a zero first derivative does not show persistence at the target. The full joint initial KL dissipation is −c²(3−c²)/(1−c²), which is compatible with that marginal departure. The source requests exact differential, endpoint and rational-state checks for this candidate solution. Reading those requests supplies neither a completed symbolic run nor the general analytic chain-rule and well-posedness premises. [AFTER1384-S6-076](../research/t20-v6-20261012/sources/2d6240fb03e257f60669edefb2dfe367df1c62f2af5b46d1938c4d5482b8699f/verify.py#L57-L65) [AFTER1384-S6-076](../research/t20-v6-20261012/sources/2d6240fb03e257f60669edefb2dfe367df1c62f2af5b46d1938c4d5482b8699f/verify.py#L77-L108)

The preserved initial symbolic checker makes the historical failure more precise. It sets S=[[1,c],[c,1]] and D=2I−S−S², but asks that tr((I−S⁻¹)D)/2 equal −3c²/(1−c²). Direct multiplication instead gives −c²(3−c²)/(1−c²), the joint dissipation above. The residual in its requested equality is c⁴/(1−c²), strictly positive for 0<|c|<1 and equal to 1/12 at c=1/2. Thus this exact initial check cannot certify all seven displayed identities on that domain; the final assertion is not evidence for the incorrect formula. This diagnoses the written algebra, not an observed SymPy run or a failure of the corrected Gaussian marginal argument, and supplies no general PDE existence claim. [AFTER2884-FIRST25-018](../research/t20-v6-20261012/sources/ea0a6dbb674c4eb4c3e9dd0c086036293371ca008790440b753396a3d5bc2afa/check.initial.py#L1-L14)

Even after fixing the entire coarse density tangent, its displayed representation can waste action. Under the standard Gaussian density ρ on the line, a nonzero variance velocity V gives relative density derivative V(y²−1)/2. The pure-reaction representative u=0, α=V(y²−1)/2 has action V²/2. The source's alternative u=Vy/3, α=V(y²−1)/6 has the same derivative, since −u′+yu+α=V(y²−1)/2, and action V²/6 using E[y²]=1 and E[(y²−1)²]=2. Their cost gap is V²/3. Thus the first representative cannot minimize over an admissible class containing both, independently of whether the second is globally optimal. This is stronger than comparing a few marginal moments: the whole polynomial density derivative agrees. The source labels the second cost a full-tangent minimum, but its finite algebra alone does not establish minimization over every admissible field; that analytic claim remains subject to the full-domain premises in §3.4. The reviewer-contributed example also retains participating authorship, rather than becoming independent corroboration merely because it appears in the author checker. [AFTER1384-S6-076](../research/t20-v6-20261012/sources/2d6240fb03e257f60669edefb2dfe367df1c62f2af5b46d1938c4d5482b8699f/verify.py#L66-L76)

The distinction between a whole marginal and finitely many statistics can be stated without importing an unreceived formula. On a product space $X\times Y$, fixing the $Y$ marginal to $\nu$ means

```math
\int f(y)\,d\mu_t(x,y)=\int f\,d\nu
```

for a measure-determining class of tests $f$. Under a differentiable weak equation, the derivative of every such integral must vanish. Preserving a finite list of marginal moments asserts only the corresponding finite list of equalities. Unless that list determines the admitted marginal class, it does not impose the whole-marginal constraint. This is the same distinction between a record and a law that §§2–3 make explicit; it becomes a restriction on the admissible tangent space when deriving a constrained gradient.

The fixed-marginal correction guides report that the constrained construction accounts for the complete density tangent. The correlated-target extension keeps the inherited constrained metric and includes a target-dependent conditional spatial score in its multiplier. Its exact Gaussian coordinate flow converges globally, by compact Kullback–Leibler sublevels, toward an arbitrary centered correlated Gaussian target with the prescribed marginal $N(0,1)$. It claims no additional convergence rate. The reported example moves from identity covariance toward

```math
\begin{pmatrix}1&1\\1&2\end{pmatrix}
```

while retaining the designated marginal. The off-diagonal covariance is allowed to change: it is not an extra conserved coordinate. The guide does not specify which displayed coordinate is named $y$, so the matrix alone should not be used to reverse the declared marginal convention. [GUIDE105-G046] [GUIDE105-G016]

Feasibility must also be separated from optimality. A conditional recentering may obey the marginal constraint while having strictly greater tangent cost than the constrained minimizer. The fixed-marginal review explicitly retains an initially mislabeled passing recentering control and its correction to a feasibility-and-gap check. That is a change in what the example establishes, not a reason to infer that the feasible recentering is the optimal projection. The reviewer's supplied rate-six inequality has participating authorship; its originator's later review is not independent corroboration of that same contribution. [GUIDE105-G053] [GUIDE105-G101]

For general laws, the reported projection and evolution statements keep their solution-domain, chain-rule and regularity assumptions. The directly global Gaussian construction is a narrower positive result, not a general-law partial-differential-equation existence or uniqueness theorem. The full constrained operator and its proofs are unreceived here; the guides support the distinctions and reported scope above, not a new derivation of that operator from marginal preservation alone. [GUIDE105-G053] [GUIDE105-G101]

The separate scalar Gaussian control fixes the coordinate convention explicitly: x=(y,z), Σ=[[1,b],[b,b²+s]] and Γ=[[1,β],[β,β²+τ]], with s,τ>0 and the y marginal fixed to N(0,1). Put δ=b−β. Its log-density ratio is q=½log(τ/s)+(z−βy)²/(2τ)−(z−by)²/(2s). Differentiating in y while holding z fixed gives E[∂ᵧq∣y]=−βδy/τ. Differentiating the conditional expectation instead gives δ²y/τ and generally changes the result. Combining this spatial score with the centered conditional divergence gives γ=δ(δ−2β)/τ and multiplier φ=γ(y²−1)/6. With A=Γ⁻¹−Σ⁻¹ and C=A−γ diag(1,0)/3, the written covariance field V=−(CΣ+ΣC)−ΣCΣ has Vᵧᵧ=0 and is checked against the complete Gaussian density tangent. Replacing γ by the conditional-divergence-only coefficient δ²/τ instead gives Vᵧᵧ=2βδ/τ. At (b,s,β,τ)=(0,1,1,1), that incorrect drift is −2, while the corrected control has velocity (z,y), reaction yz, relative density derivative 3yz and ḃ=3 with the y law unchanged. This explicit diagnostic explains the missing term; the unexecuted algebraic checks do not prove a general-law evolution, global convergence, or an endpoint minimizer. [AFTER1384-S4-047](../research/t20-v6-20261012/sources/2900bebcb82b6bab7b3ddf7eb7902f3e289a47e7583f4aac5f205eb930259636/verify.py#L15-L99)

The distinct correlated-target control also writes the coordinate mobility explicitly. For δ=b−β and s,τ>0, its energy is E=(s+δ²)/(2τ)−1/2+(1/2)log(τ/s), and its matrix is M=[[1+2s+b²/3,−2bs],[−2bs,2s(s+2+2b²)]]. Direct multiplication of −M∇E gives ḃ=[−(1+2s+b²/3)δ+b(s−τ)]/τ and ṡ=[2bsδ−(s+2+2b²)(s−τ)]/τ. The first diagonal entry and determinant (2s/3)(b²+2s+1)(2b²+3s+6) are positive, so this specified coordinate flow has Ė=−∇EᵀM∇E≤0. In particular, b=β alone is not invariant: there ḃ=β(s−τ)/τ. The program separately requests equality with the complete density tangent and with the squared velocity/reaction action, and checks the missing-score variance leak at (b,β,s,τ)=(1/2,1/3,3/4,5/4) as 4/45. Its claim of independence is an algebraic implementation that imports no author/root code; it is not newly observed external review. Reading these formulas and controls establishes neither their general-law projection premises nor analytic existence, global convergence or a rate. [AFTER1634-S7-154](../research/t20-v6-20261012/sources/57bdce1b135b08cbff4c6432ab213934ba5c4a788bebe964c67d7b9ced52e137/check_independent.py#L18-L94)

The identity-target scalar Gaussian control quantifies three different dissipation expressions under the same whole-marginal convention. For b∈R and s>0 let Σ=[[1,b],[b,b²+s]], A=(I−Σ⁻¹)/2, P=diag(b²/6,0) and KΣ(X)=2(XΣ+ΣX+ΣXΣ). Its candidate constrained covariance velocity is −KΣ(A−P), with first diagonal entry zero, ḃ=−b(s+2+b²/3) and ṡ=(1−s)(s+2)+2b². Write Dfull=tr(AKΣ(A)), Dcon=tr((A−P)KΣ(A−P)) and Dfib=b²(1+s)+(s−1)²(1/s+1/2). The requested identities are Dfull−Dcon=b⁴/6 and Dcon−Dfib=b²/s+b⁴/3; thus these two gaps have different formulas and both vanish at b=0. For the conditional Gaussian divergence J=(s+b²−1−log s)/2, direct substitution of the displayed velocities gives J̇=−Dcon. This sharpens the distinction between the constrained tangent and the source’s fibrewise comparison without identifying them. The eight symbolic checks were not run here; the finite formulas supply neither general-law projection or well-posedness nor a global rate or endpoint-minimizing theorem. [AFTER1634-F5-101](../research/t20-v6-20261012/sources/50bcd7f4a8c68c598eabe6b03ad69a0f10cd3d10d041d8f0eb6da97fccb61acf/check.py#L2-L19)

The longer identity-target control supplies a rate calculation within that same Gaussian coordinate field. With J=(b²+s−1−log s)/2 and s>0, set R(s)=(s−1)²(1/s+1/2)−3(s−1−log s). Its displayed identities are R(1)=0, R′(s)=(s−1)³/s² and Dcon−6J=R(s)+b²(s−1)²/s+b⁴/3. The derivative is negative below one and positive above it, so R≥0. Along a differentiable solution remaining in this domain and satisfying the stated J̇=−Dcon, integration gives J(t)≤e^(−6t)J(0). The coefficient six is sharp for this Gaussian inequality: at b=0, letting s approach one gives Dcon/J→6. This argument supplies neither existence on all future times nor the general-law projection and chain-rule premises.

A different control at b=1/2, s=3/4 holds the entire fibrewise Gaussian density tangent fixed, with covariance velocity [[0,−7/8],[−7/8,−3/16]]. It proposes the symmetric potential matrix [[−235/924,17/42],[17/42,−43/231]], whose covariance equation −(BΣ+ΣB)−ΣBΣ equals that velocity and whose stated action is 2489/7392, below the fibrewise representative's 53/96 by 199/924. This is a specified same-tangent competitor, not merely agreement of one marginal moment. Even if its exact algebra is verified, strict improvement only disproves minimality of the more costly representative; the program's label “ambient minimum” additionally requires the full admissible-class argument. The SymPy checks, input bindings and referenced ordinary proof were not run or received here. [AFTER2134-S25-045](../research/t20-v6-20261012/sources/88f32b9450f85e4c10ff8e7b28446cbaedca3c10604af49187993fd3b932b86a/verify.py#L22-L118)

The selected block-covariance control makes one boundary diagnostic explicit. It writes Σ=[[I,Bᵀ],[B,BBᵀ+S]], computes a polynomial covariance tangent F, and defines Ḃ=F_zy and Ṡ=F_zz−ḂBᵀ−BḂᵀ. For a nullspace basis K of S it requests KᵀṠK=2Kᵀ(I+BBᵀ)K and positive definiteness of that compressed derivative. The supplied observed and hidden dimensions are 2 and 3, with fixed B and target and four selected residual covariances of ranks 1, 0, 2 and 3. The singular cases additionally request the determinant’s first nonzero coefficient; their chosen null/range bases are coordinate orthonormal. The positive residual case separately checks the full-density coefficients, exact KL-dissipation identity and noncommutation of S with the target residual covariance. These are distinct finite algebraic obligations, not a general-dimensional proof, an existence result or a received successful execution. [G21-020](../research/t20-v6-20261012/sources/034ed66aa79cbcac738633fb34a20decd40d4ba1aa25dd9938b065c7d2c896ad/verify.py#L11-L54)

The matrix correction has a direct block-algebra explanation. For conformable real matrices B and B̃, positive-definite residual covariances S and T, and W=T⁻¹, put δ=B−B̃, N=δᵀWδ, M=−B̃ᵀWδ and P=(N+M+Mᵀ)/3. Let Σ=[[I,Bᵀ],[B,BBᵀ+S]], Q=[[I+B̃ᵀWB̃,−B̃ᵀW],[−WB̃,W]], and P̄=diag(P,0). Define the unit-entropy base covariance generator G₁(Q,Σ)=2I+Σ−QΣ−ΣQ−ΣQΣ. In the corrected polynomial field F=G₁(Q,Σ)+P̄Σ+ΣP̄+ΣP̄Σ, the observed block is exactly 3P−N−M−Mᵀ, hence zero. Replacing P by N/3 instead leaves −(M+Mᵀ), which need not vanish; M itself need not be symmetric. This follows by multiplying the displayed blocks and does not require a commutation assumption on the residual covariances. The selected independent program supplements this identity with a symbolic observed/hidden dimension 2/2 control and one positive rational dimension 3/2 fixture, using Wick integration for the full density, centered reaction, action and KL-dissipation comparisons. These are specified finite checks, not an observed symbolic run or a derivation of the general-law constrained evolution, analytic existence or global convergence. [AFTER1884-F25-004](../research/t20-v6-20261012/sources/63ba3473b8564bd960c852383b77e345c71790e68db1ddf99eaf9edeb9a72427/independent_controls.py#L17-L48) [AFTER1884-F25-004](../research/t20-v6-20261012/sources/63ba3473b8564bd960c852383b77e345c71790e68db1ddf99eaf9edeb9a72427/independent_controls.py#L64-L103)

### 3.7 Conditional entropy transfer retains the reaction and flux terms

An entropy calculation must use the actual constrained tangent. The conditional-entropy guide reports a coercivity transfer through the same fixed-whole-marginal projection, under explicit domain and energy-chain-rule premises. Its non-Gaussian quartic example includes the full observed-flux correction and retains reaction. Dropping either term because a simpler unconstrained or Gaussian calculation omits it would change the evolution being assessed. [GUIDE105-G002]

Three comparisons need separate quantifiers. Decay of total entropy is not automatically decay of conditional entropy. An inequality after integration over the observed variable is not a uniform inequality on every conditional fibre. A constant proved for centered Gaussian laws is not thereby valid on all laws. A non-Gaussian example can diagnose the difference, but one example does not prove a universal coercivity constant. The guide's full inequalities and domains remain in its unreceived result; no new constant is supplied here. [GUIDE105-G002]

Separate conditional normalization can also leave the integrated moment domain while every conditional law remains finite-moment. Take observed masses ν_n=2^(−n), ε_n=2^(−n), x_n=2^(n/2), and r_n=(1−ε_n)δ_0+ε_nδ_(x_n), n≥1. Initially Σ_nν_nε_nx_n²=1. Use the bounded strictly positive pointwise Borel likelihood L(n,x_n)=1 and L(n,x)=ε_n² elsewhere. Normalizing each fibre while preserving ν gives Z_n=ε_n+ε_n²−ε_n³ and high-atom mass p_n=1/(1+ε_n−ε_n²)≥4/5. Its integrated second moment is therefore Σ_np_n=∞, with the first N terms at least 4N/5. One global joint normalization instead has Z=43/105, changes the observed masses to ν_nZ_n/Z, and yields second moment 105/43. It is a different marginal contract. A uniform positive lower likelihood bound is sufficient protection for the conditional route, without being asserted necessary. Thus the fixed-ν finite-moment entrance hypothesis must be rechecked after the audit; the example does not make the law-level OU–reaction step undefined or establish anything about its later integrated entropy or convergence. The divergence follows from the analytic lower bound, not the source's reported finite checks, which were not rerun here. [AFTER3884-FOURTH25-077](../research/t20-v6-20261012/sources/2d1a4c7372f007e0693cb8b0812665507e5991c5b7cf38723dc4ac888a45697e/DOMAIN_ADDENDUM.md#L3-L32)

The independent algebra control makes two of these distinctions quantitative. In its correlated quartic model, Y is standard normal, e=z−by has the quartic innovation law, and differentiation in y at fixed z is ∂ᵧ−b∂ₑ, not differentiation at fixed innovation. With q=V(e+(b−a)y)−V(e), V(u)=u²/2+u⁴/4, it constructs a centered Hermite-polynomial multiplier and requests zero conditional marginal drift; removing the target-dependent score term leaves a nonzero drift whose y⁴ coefficient is −1 at a=1 and b−a=1. Separately changing the target’s observed marginal from N(0,1) to N(L,1) adds ℓ(y)=−Ly+L²/2 to q and ℓ−Eℓ to the multiplier. The projected difference therefore changes only by the constant Eℓ, while total relative entropy retains the residual L²/2. Another specified derivative control, at β=1 and variance 11/10, is d(y)=169/2200−(103/30)y²: it is positive near zero but has negative N(0,1) average. The latter is a separate inherited-flow diagnostic, not the quartic formula. These exact algebraic consequences expose the difference between a constrained field, total entropy and fibrewise monotonicity; the unexecuted controls do not establish a general logarithmic Sobolev inequality, chain rule, or existence and uniqueness of the underlying evolution. [AFTER1384-S5-061](../research/t20-v6-20261012/sources/2b2558caef082184ddeb341cda15efc318cc25f96f7b68242a13cb036885fd90/check.py#L1-L111) [AFTER1384-S5-061](../research/t20-v6-20261012/sources/2b2558caef082184ddeb341cda15efc318cc25f96f7b68242a13cb036885fd90/check.py#L113-L150) [AFTER1384-S5-061](../research/t20-v6-20261012/sources/2b2558caef082184ddeb341cda15efc318cc25f96f7b68242a13cb036885fd90/check.py#L152-L175)

The quartic author control makes that multiplier and its dissipation remainder explicit at a=1/2 and b=1. Let Y be standard normal and let the independent innovation e have density proportional to exp(−e²/2−e⁴/4); write c=E[e²], A=1+3c and q=V(e+Y/2)−V(e), where V(u)=u²/2+u⁴/4. At fixed z=e+Y, the observed derivative is ∂y−∂e. Conditional expectation gives h(y)=E[q|Y=y]=Ay²/8+y⁴/64 and m(y)=E[(∂y−∂e)q|Y=y]=−Ay/4−y³/16. With H₂=y²−1 and H₄=y⁴−6y²+3, the centered polynomial φ=−(4A+3)H₂/96−3H₄/320 solves (−∂yy+y∂y+1)φ=ym−m′+h−E[h], because H₂ and H₄ have eigenvalues three and five. Put f=q−φ and D=E[((∂y−∂e)f)²+(∂e f)²]+Var(f). The conditional-variance identity then gives D=E[(∂e q)²]+E[Var(q|Y)]+E[((∂y−∂e)q−φ′)²]+Var(h−φ). The last two terms form a nonnegative remainder, and the conditional reaction variance is retained. These finite polynomial and expectation identities explain the specified control without treating its quadrature or symbolic assertions as executed, or deriving a general projection theorem, chain rule or PDE well-posedness result. [AFTER2634-TENTH25-238](../research/t20-v6-20261012/sources/e62ab6630606d10c4e8bbe77e6d855e6a5db776aa65be88280c16649bebc8681/verify.py#L32-L94)

The Gaussian entropy-transfer author and review guides retain an all-dimensional analytic result within a fixed Gaussian contract, with classical transport geometry credited separately from the local derivation. Their evidence combines distinct types of controls: the portable author branch includes numerical ordinary-differential-equation corroboration, whereas the independent suite is symbolic and rational. Neither turns the fixed-family comparison into a global unrestricted endpoint identification. Source-inspection records, PDF hashes and reported page checks remain historical evidence; a portable run that lacks the raw source cannot renew that inspection. [GUIDE105-G019] [GUIDE105-G029]

The scalar Gaussian control places a necessary upper limit on a universal entropy-dissipation coefficient without proving such an inequality. For target variance T>0 and Gaussian mean m and variance v>0, its expressions are E=[(v+m²)/T−1+log(T/v)]/2 and D=m²/T²+(v−T)²/(vT²)+m²v/T²+(v−T)²/(2T²). Along m=n, v=1/n as n tends to infinity, E/n² tends to 1/(2T) and D/n² tends to 1/T², hence D/E tends to 2/T. Any inequality D≥cE valid on this whole scalar family must therefore have c≤2/T. At T=1 and v=1 with m≠0, the ratio is instead exactly four; in the centered limit m=0, v→1 it is six. Those restricted comparisons cannot justify their larger constants on all scalar Gaussians. The limiting argument concerns the displayed formulas at positive variance and supplies no lower-bound proof, chain rule, global evolution or unrestricted law-space result; the source's symbolic assertions were not run. [AFTER2634-EIGHTH25-199](../research/t20-v6-20261012/sources/e1f274dc0c171db2fed7a202a7d862a2ba72e603d2067a039d45420ae6850166/check.py#L3-L16)

The independent entropy-control body makes the Gaussian candidate generator explicit. Let Q be positive definite, e=m−g, ε≥0 and Σ positive definite at the point being evaluated, and put Sε=(Q−εΣ⁻¹)/2. For Eε=½eᵀQe+½tr(QΣ)−(ε/2)log det Σ, the displayed field is ṁ=−(I+Σ)Qe and Σ̇=G₁(Q,Σ)+(ε−1)(2I+Σ), using the unit-entropy base covariance generator defined in the preceding block-algebra discussion. With LΣ(A)=2(AΣ+ΣA+ΣAΣ), it has Σ̇=−LΣ(Sε) and Ėε=−eᵀQ(I+Σ)Qe−tr(Sε LΣ(Sε)). At positive ε the covariance equilibrium is εQ⁻¹; at ε=0 the precision P=Σ⁻¹ instead satisfies Ṗ=PQ+QP+Q. The order of the noncommuting products is essential: the supplied positive-definite rational fixture makes the shortcut −2ΣQ−ΣQΣ nonsymmetric. A separate two-dimensional OU/reaction step control requests the ε=1 infinitesimal generator for one noncommuting rational fixture. These are finite algebraic identities and check designs, not an observed run, convergence of a splitting scheme, global existence, uniform zero-temperature convergence or an unrestricted endpoint-distance theorem. [AFTER1884-T25-053](../research/t20-v6-20261012/sources/6a39707df172f7b7508c10e61cc3ec93327489ff990de1500a5c03a9058b1c27/check.py#L3-L21) [AFTER1884-T25-065](../research/t20-v6-20261012/sources/6bc0cb3dc073e46e55d04e7258766eea93afc94d3bccd6e4466e373479c9a25a/check_independent.py#L74-L115) [AFTER1884-T25-065](../research/t20-v6-20261012/sources/6bc0cb3dc073e46e55d04e7258766eea93afc94d3bccd6e4466e373479c9a25a/check_independent.py#L117-L137)

A scalar stationarity control isolates a drift-sign obligation separate from the covariance algebra. Let ρ(x)=(2π)^(−1/2)exp(−x²/2) and, for smooth u, define D₋u=(u′−u(logρ)′)′ and D₊u=(u′+u(logρ)′)′. Since ρ′=−xρ, D₋ρ=0 whereas D₊ρ=2(x²−1)ρ, which is not identically zero. Thus changing this sign changes stationarity at the operator’s own Gaussian target; this is an elementary density calculation, not a numerical trajectory comparison. [AFTER2884-SIXTH25-143](../research/t20-v6-20261012/sources/fad4e3508cb26be867b7d9eaf8de53e7cf3c98fcbef03563f4f9feb14dfd9ba7/verify.py#L70-L76) The unexecuted source treats raw-manuscript custody as a separate optional gate, so this calculation supplies no renewed primary-source inspection or attribution of an error to the unseen manuscript, and no PDE well-posedness or convergence theorem. [AFTER2884-SIXTH25-143](../research/t20-v6-20261012/sources/fad4e3508cb26be867b7d9eaf8de53e7cf3c98fcbef03563f4f9feb14dfd9ba7/verify.py#L78-L90) [AFTER2884-SIXTH25-143](../research/t20-v6-20261012/sources/fad4e3508cb26be867b7d9eaf8de53e7cf3c98fcbef03563f4f9feb14dfd9ba7/verify.py#L130-L135)

A finite OU-first reaction step admits an exact Gaussian formula without commuting its covariance matrices. Let the target be N(g,T) with T positive definite, choose h>0, and set A=exp(−hT⁻¹), Q=T−ATA and α=exp(−h). From an initial Gaussian with mean m and positive-semidefinite covariance Σ, the OU step has residual d_D=A(m−g) and covariance Σ_D=AΣA+Q. Since Q is positive definite, Σ_D is invertible even when Σ is singular. Raising this Gaussian density to power α and the target density to power 1−α, then normalizing, gives Σ_R=[αΣ_D⁻¹+(1−α)T⁻¹]⁻¹ and m_R=g+Σ_R αΣ_D⁻¹d_D. Completing the quadratic exponent proves the entire-density identity; the order of the matrix factors cannot be reversed. For the supplied fixture T=diag(1,2), Σ=[[2,1],[1,3]], m=(−1,2), g=(3,−1) and h=log4, the output is Σ_R=[[74,2],[2,150]]/73 and m_R=(1603,−371)/584. This regularize-before-invert construction is a finite step, not the continuous singular-entrance theorem. Nor may density powers be distributed over mixture components. The source’s exact symbolic and numerical controls were read rather than executed, and no convergence of the splitting scheme or general PDE result is inferred. [AFTER2634-SEVENTH25-163](../research/t20-v6-20261012/sources/dda057694b1deab9f08d815e58cb04259dd89180e34317a032438b997ee0dd95/verify.py#L43-L75) [AFTER2634-SEVENTH25-163](../research/t20-v6-20261012/sources/dda057694b1deab9f08d815e58cb04259dd89180e34317a032438b997ee0dd95/verify.py#L94-L130) [AFTER2634-SEVENTH25-163](../research/t20-v6-20261012/sources/dda057694b1deab9f08d815e58cb04259dd89180e34317a032438b997ee0dd95/verify.py#L148-L153)

### 3.8 Endpoint minima, singular entrance and feasible paths

The endpoint-action guide reports finite-action feasibility, attained constrained transport-and-reaction minima, a finite geodesic metric and convergence of nested finite marginal-test minima on compact product tori. Singular laws and zero-density endpoint conventions are included in its stated result. These are specific additional assertions, whose compactness and limiting proofs are not supplied by the guide. A theorem for finitely many constraints cannot simply be applied to the infinitely many tests defining an entire marginal; a passage to that limit must be proved. [GUIDE105-G012]

The same guide names a conditional sphere path and a convex-mixture path as feasible competitors. Their role is to establish an admissible connection or an upper bound on the infimum. They are not claimed to minimize the action. In general, if $\mathcal A$ is the admissible path class and $\gamma\in\mathcal A$, then $\inf_{\eta\in\mathcal A}I(\eta)\le I(\gamma)$; reversing that inequality requires an optimality argument. No explicit endpoint metric formula or finite-to-infinite-constraint proof is reconstructed from the short description. [GUIDE105-G012]

The conditional-sphere control exhibits why global normalization is insufficient for the whole-marginal constraint. Give one observed fibre mass 1/3, with its initial and final conditional atoms disjoint, and a second, unchanged fibre mass 2/3. In the changing fibre set p₀(t)=cos²(πt/2) and p₁(t)=sin²(πt/2). Its mass stays one and its reaction action density is ṗ₀²/p₀+ṗ₁²/p₁=π² for interior times, hence the weighted competitor has action π²/3 while retaining both observed masses. The globally normalized square-root sphere midpoint instead assigns mass 4/5 to the shared fibre and 1/5 to the changing fibre, a marginal error of 2/15. The source also writes the mixture identity 4(a′²f₀+b′²f₁)(a²f₀+b²f₁)−[2(aa′f₀+bb′f₁)]²=4f₀f₁(ab′−ba′)²; for nonnegative densities its right side is nonnegative and supports a separate feasible-action bound. These formulas concern explicit competitors and the interior action, with endpoint quotients interpreted through their limits. They neither identify the minimizing path nor establish the unreceived compactness, conditional-measure or endpoint-attainment arguments, and their symbolic checks were not run. [AFTER1384-S5-068](../research/t20-v6-20261012/sources/2bcb080d79509746b02c643ae32401cf86541214dd938aa699854b80ba04cb44/verify.py#L14-L47) [AFTER1384-S5-068](../research/t20-v6-20261012/sources/2bcb080d79509746b02c643ae32401cf86541214dd938aa699854b80ba04cb44/verify.py#L48-L68)

A smooth finite-test example makes the whole-marginal boundary explicit. On the unit circle, fix an integer N≥1 and 0<ε<1 and put ρ_t(y)=1+ε sin(πt)cos(2π(N+1)y), 0≤t≤1. It is positive, has total mass one, has uniform endpoints, and agrees with the uniform law on every sine and cosine moment of frequencies one through N. Orthogonality of the Fourier modes nevertheless gives its next cosine moment as ε sin(πt)/2, which is nonzero at interior times. Thus even a smooth positive path can satisfy these finitely many marginal tests while violating the entire uniform-marginal constraint. This is the analytic leakage example supplied beside the reviewer’s numerical finite-fibre controls, not a numerical extrapolation. It gives neither an endpoint optimizer nor an obstruction to a separately proved limit over all marginal tests, and no numerical control was run here. [AFTER2634-FIRST25-021](../research/t20-v6-20261012/sources/c977d94c97f3c2588d6aa5510c6e7843cc6b62ced7b2be1b7f33c0e03a47f4e3/independent_controls.py#L71-L95)

Participating pre-review notes supply a conditional-measure construction for the compact product-torus endpoint contract, with unhalved action ∫(|v|²+α²)dμ_t dt. Disintegrate μ_i(dy,dz)=ν(dy)q_i(y,dz), put λ_y=q_0(y)+q_1(y), and obtain compatible fibre densities f_i from one globally Borel Radon–Nikodym derivative with respect to μ_0+μ_1, after a common null-set adjustment. Then u_i=√f_i have fibre L² norm1, c_y=∫u_0u_1dλ_y is measurable, and θ_y=arccos(c_y) lies in[0,π/2]. The spherical interpolation u_t=[sin((1−t)θ_y)u_0+sin(tθ_y)u_1]/sinθ_y, with its continuous value at θ_y=0, keeps each fibre norm1 and has squared derivative norm θ_y². Taking q_t=u_t²λ_y and zero transport gives reaction action4∫θ_y²dν≤π². The reaction rate2∂_t u_t/u_t is defined at interior times; endpoint zero-density divergences are harmless for the time integral. The estimate ∫|u_t²−u_s²|dλ_y≤2θ_y|t−s| gives total-variation continuity and the endpoint traces. This is a feasible competitor and sharper upper bound, not an optimal metric formula or a final review acceptance. [AFTER3634-SECOND25-049](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1a59ebbb6b37a031bb47cf851b2c7f6df2bf483f495cd0b2f40e5bd64478ed33/PRE_REVIEW_ANALYTIC_CHECKS.md#L3-L15)

At that compact probability-measure scope, the notes also give the missing direct-method mechanism. A bounded action and exact unit mass bound the spacetime measure and, by Cauchy–Schwarz, the total variations of transport flux and reaction. Weak-* subsequences exist, and the quadratic perspective is lower semicontinuous through its dual formula sup_{b,c}[2∫b·dj+2∫c dr−∫(|b|²+c²)dρ]. Finite action forces j and r to be absolutely continuous with respect to ρ. The fixed pushforward to time and observed coordinates remains dt⊗ν. The continuity-equation estimate |∫φ d(μ_t−μ_s)|≤√((t−s)E_[s,t]) sup√(|∇φ|²+φ²), first for smooth φ, supplies narrow equicontinuity, a continuous representative and the prescribed endpoint traces; continuous marginal tests then hold at every time. This gives attainment in the declared compact setting, not compactness in the constrained metric topology. Reversal gives symmetry, the same test estimate separates endpoints, and concatenating paths over durations λ and1−λ gives energy E_01/λ+E_12/(1−λ), yielding the triangle inequality after optimization. For an attained minimum d², every time partition satisfies d≤Σd_i≤Σ√(ℓ_i E_i)≤d; equality forces d_i=ℓ_i d and hence constant-speed geodesicity. These are written analytical arguments, not solver or formal-kernel results. [AFTER3634-SECOND25-049](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1a59ebbb6b37a031bb47cf851b2c7f6df2bf483f495cd0b2f40e5bd64478ed33/PRE_REVIEW_ANALYTIC_CHECKS.md#L17-L37)

The limit from finite tests retains exact mass1 at every stage and imposes the first N members of a countable continuous family with uniformly dense linear span on the observed compact space, at every path time. Its feasible sets decrease, and the preceding full-marginal competitor bounds the increasing minima E_N by E_∞≤π². Compactness gives a subsequential limiting minimizing path; each fixed test eventually holds, and density together with narrow continuity supplies the entire marginal. Lower semicontinuity then yields E_∞≤E_limit≤lim E_N≤E_∞, proving convergence of the optimal energies and optimality of every cluster path. This does not make any finite test stage exact, contradict the preceding Fourier leakage example, provide a rate, or prove full-sequence or strong control-field convergence without further hypotheses. The cosine-squared mixture μ_t=cos²(πt/2)μ_0+sin²(πt/2)μ_1 gives a separate action≤π² competitor in any weakly closed, time-independent convex subset of the same probability-measure space; it does not identify the optimizer. The notes are pre-freeze participating review work, and their reported primary-source comparisons do not become new external readings or field-wide priority claims here. [AFTER3634-SECOND25-049](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1a59ebbb6b37a031bb47cf851b2c7f6df2bf483f495cd0b2f40e5bd64478ed33/PRE_REVIEW_ANALYTIC_CHECKS.md#L39-L65)

The singular-Gaussian-entrance guides identify a further ordinary analytic result and a separate scoped review. Their symbolic and input-binding controls are supplemental. They do not prove analytic existence, the asserted endpoint trace or uniqueness merely by evaluating formulas. Nor does a result for nondegenerate Gaussian geometry automatically cover a singular initial law: the boundary and its admitted entrance need their own argument. This preserves the positive source-reported entrance result together with the unreceived analytic dependency and the precise limit of its historical checks. [GUIDE105-G010] [GUIDE105-G035]

The scalar entrance control distinguishes a dissipation singularity from the cost of a reparameterized approach. In Σ=[[1,b],[b,b²+s]] with target parameters (β,τ), τ>0, its polynomial covariance system has boundary derivative ṡ=2(1+b²). Its requested pole decomposition is D=(1+b²)/s+R, with R regular in s at zero for fixed τ. Along the formal first-order entrance b(t)=B+O(t), s(t)=2(1+B²)t+O(t²), the requested leading limit is tD→1/2. The displayed energy correspondingly has form −(log t)/2+C₀+o(1), where C₀=((B−β)²/τ−1+log(τ/[2(1+B²)]))/2. For the leading density D=1/(2t), changing time to t=u² gives action density 2, and the squared leading length on [0,ε] is 2ε. These finite symbolic and leading-order calculations separate original-time dissipation from reparameterized finite action; they do not construct an actual entrance solution, prove its trace or uniqueness, or identify an endpoint minimizer. No passing run is inferred from the checker’s output instructions. [G21-205](../research/t20-v6-20261012/sources/1e700d5359bbbae2dbd7741478b22f54c3f14815b4c2c71095452c9692eb54cd/verify.py#L15-L58)

The rotated block controls separate that scalar pole from a coordinate artifact. For a positive-semidefinite residual S₀, let U,V be orthonormal range and kernel bases, and put H=I+BBᵀ and A_K=2VᵀHV. The displayed residual tangent has VᵀṠV=A_K>0. In the basis [U,V], the range block of S₀+tṠ is invertible at zero, the kernel block is tA_K, and the off-diagonal blocks are O(t); its Schur complement is therefore tA_K+O(t²). If r is the nullity, this gives det(S₀+tṠ)=tʳ det(UᵀS₀U)det(A_K)+O(tʳ⁺¹) and limₜ↓₀ t(S₀+tṠ)⁻¹=VA_K⁻¹Vᵀ, with the empty range determinant interpreted as one. Consequently the inverse-covariance contribution has residue tr(HVA_K⁻¹Vᵀ)=r/2. The source requests these identities for hidden dimension 3 and ranks 0,1,2 after the rational Householder rotation I−2hhᵀ/(hᵀh), h=(1,2,3)ᵀ, so the nontrivial range/kernel cases are not aligned with coordinate axes. This is an argument about a first-order matrix jet and its finite controls. It does not construct an actual entrance solution, establish its endpoint trace or uniqueness, or turn that jet into an endpoint-minimizing path; the program was not executed. [AFTER1884-F25-004](../research/t20-v6-20261012/sources/63ba3473b8564bd960c852383b77e345c71790e68db1ddf99eaf9edeb9a72427/independent_controls.py#L106-L134)

A separate exact-control source supplies an explicit product trajectory rather than only a formal first-order entrance. At b=B=0 and target variance T=1, its covariance is diag(1,s(t)), where s(t)=2(e^(3t)−1)/(2e^(3t)+1), s(0)=0 and s′=(s+2)(1−s). Substitution in the displayed dissipation expression gives D=(s−1)²(s+2)/(2s), providing a concrete product instance of the singular leading behavior. The same source retains a noncentered extension with conditional mean c+by: its multiplier is (b−B)(b−3B)(y²−1)/(6T)+c(b−2B)y/(2T), and the requested mean equation is c′=−c(1+s+b²/2)/T while the observed mean stays zero. It requests the full noncentered Gaussian density identity, not merely agreement of a few moments. These explicit formulas add neither a general singular-entrance existence or uniqueness proof nor an endpoint-minimizing-path result; the symbolic assertions have not been executed here. [G23-194](../research/t20-v6-20261012/sources/1cdb4572d324dd22d6ee387ed7ddb61c9e17ac27cd346a489016e8a48eb56465/check_independent.py#L8-L57)

For that explicit product trajectory, the independent control refines the leading action estimate without claiming an optimal path. It uses s(t)=2(e^(3t)−1)/(2e^(3t)+1) and D(t)=(s(t)+2)(1−s(t))²/[2s(t)]. The product tD(t) has a removable analytic extension at zero with expansion 1/2−5t/4+3t²/8+O(t³). On the unit parameter interval 0≤r≤1, set t=εr² and rescale the displayed transport and reaction fields by dt/dr. Their action is the integral of 4ε²r²D(εr²), hence 2ε−5ε²/3+3ε³/10+O(ε⁴). The remainder follows from the local analytic expansion of the explicit expression, not from a finite list of moment checks. This concerns this chosen reparameterized field representation and its small-ε action; it is not the original-time dissipation integral, a squared-distance equality, an endpoint minimization theorem or a general singular-entrance uniqueness proof. The source’s symbolic checks were not executed. [AFTER2384-SECOND25-33](../research/t20-v6-20261012/sources/a8abc4f286941c6e1638be0479c51a167be5ce620e25ad9e456850ae1da5d70e/independent_controls.py#L19-L66)


## 4. Scalar hierarchies: realizability is an additional condition

### 4.1 Exhaustion of all realizable solutions

**Theorem 6 (scalar classification).** Suppose $`m_0=1`$ and every $`m_r:[0,T)\to\mathbb R`$ is coordinatewise $`C^1`$ and satisfies (7). If the sequence at every time has a Stieltjes probability representative on $`[0,\infty)`$, then there is a unique initial law $`\mu\in\mathcal P_\infty([0,\infty))`$ whose tilt gives the whole path. The same conclusion holds under the weaker assumptions $`m_r(t)\ge0`$ for every degree and time and existence of a representative at just one positive time.

For a fixed valid initial record $`c`$, its realizable hierarchy paths are therefore in bijection with its representing laws. Every such path extends uniquely to all nonnegative times.

**Proof.** Define
```math
a_0(t)=\exp\!\left(-\int_0^t m_1(u)\,du\right),
\qquad a_r(t)=a_0(t)m_r(t).
```
Then $`a_r'=-a_{r+1}`$ and all $`a_r`$ are nonnegative. Iterating the equations makes every coordinate smooth. Taylor's formula backwards from $`t`$ to $`t-b\ge0`$, with its integral remainder of positive sign, gives
```math
\sum_{k=0}^{N}\frac{b^k}{k!}a_{r+k}(t)\le a_r(t-b).
\quad\text{(10)}\quad
```
In particular $`a_n(t)\le n!/t^n`$. On a compact interior time interval, choose a common shorter backward distance. Applied to each fixed $`r`$, (10) bounds its derivatives by $`C_r n!b^{-n}`$, proving real analyticity there.

Choose the positive time $`s`$ in the hypothesis and a probability representative $`\rho_s`$. The finite measure $`\lambda_s=a_0(s)\rho_s`$ has moments $`a_r(s)`$. By the nonnegative exponential series and (10),
```math
\int x^r e^{bx}\,d\lambda_s(x)\le a_r(s-b),
\qquad 0\lt{}b\lt{}s.
\quad\text{(11)}\quad
```
Thus $`G(u)=\int e^{(s-u)x}\,d\lambda_s`$ is analytic for every $`u>0`$. At $`u=s`$ all its derivatives agree with those of $`a_0`$. The identity theorem gives $`G(u)=a_0(u)`$ throughout $`0<u<T`$, and differentiation gives all the other coordinates. As $`u\downarrow0`$, monotone convergence yields
```math
\mu(dx)=e^{sx}\lambda_s(dx),\qquad
\int x^r\,d\mu=\lim_{u\downarrow0}a_r(u)=m_r(0).
```
In particular, $`\mu`$ is a probability with every moment. Dividing the recovered $`a_r`$ by $`a_0`$ proves the assertion. Laplace uniqueness proves uniqueness of the initial law for the complete path.

Conversely, (6) supplies such a path for every initial representative. Distinct representatives give distinct records at every positive time by Proposition 5's determinacy and inverse-tilt argument. The explicit formula supplies the unique global extension. ∎

The uniqueness is attached to the **complete realizable path**, not merely to its initial moment sequence. If that initial sequence is indeterminate, several realizable paths begin there. The proof does not select a measurable family of representatives; one positive-time representative is enough.

The distinction cannot be removed by checking individual signs. Let $`b(t)=1-\varepsilon e^{-1/t}`$ for $`t>0`$, extend it smoothly by $`b(0)=1`$, and take $`0<\varepsilon<1`$. Put $`a_r=(-1)^r b^{(r)}`$ and $`m_r=a_r/b`$. These solve the hierarchy and start from the valid record of $`\delta_0`$, but
```math
a_2(t)=\varepsilon e^{-1/t}\frac{2t-1}{t^4}<0
\quad (0\lt{}t<1/2).
```
This is a formal solution outside the positive cone. Conversely, $`a_0=(T-t)/T`$, $`a_1=1/T`$, and $`a_r=0`$ for $`r\ge2`$ give nonnegative coordinates on $`[0,T)`$ but negative variance. Their initial sequence is already invalid, so this second example does not settle what can happen from a valid initial record. The next construction does. These classification and boundary arguments incorporate [the scalar realizability proof][scalar-source].

### 4.2 Loss of realizability from a determinate initial law despite positive coordinates

**Proposition 7 (strictly positive coordinates without a law).** There is a smooth scalar hierarchy whose initial sequence has a unique probability representative, while every coordinate remains strictly positive and no positive-time sequence has a Stieltjes representative.

**Proof.** Let $`\mu`$ be the standard lognormal law, with moments $`b_r=e^{r^2/2}`$. The classical Krein extremal measure $`\eta_K`$ for this indeterminate Stieltjes problem is a discrete representative with an atom $`w=\eta_K(\{0\})\in(0,1)`$. The full-atom-deletion theorem of Berg and Christensen states that deleting one whole atom of an extremal measure leaves a Hamburger-determinate measure. Consequently
```math
\rho=\frac{\eta_K-w\delta_0}{1-w},
\qquad
c_0=1,\quad c_r=\frac{e^{r^2/2}}{1-w}\ (r\ge1)
\quad\text{(12)}\quad
```
is a determinate probability sequence. Full deletion matters: the theorem used here is not an assertion about arbitrary partial subtraction.

Write $`B_r(t)=\int x^r e^{-tx}\,d\mu`$, and define
```math
a_0(t)=\frac{B_0(t)-w}{1-w},
\qquad
a_r(t)=\frac{B_r(t)}{1-w}\ (r\ge1),
\qquad m_r(t)=\frac{a_r(t)}{a_0(t)}.
\quad\text{(13)}\quad
```
Since $`B_0(t)\ge1-te^{1/2}`$, the denominator is positive for
$`0\le t<T_0=(1-w)/(2e^{1/2})`$. Every coordinate is positive, the equations $`a_r'=-a_{r+1}`$ hold, and the initial record is (12).

Suppose a probability $`\sigma`$ represented the record at some $`t>0`$. Then
$`(B_0(t)-w)\sigma+w\delta_0`$ would have all moments of $`e^{-tx}\mu`$. That latter finite measure has a positive exponential moment and is determinate. The two measures would be equal, although the first has mass at least $`w`$ at zero and the second has none. This is impossible. ∎

The construction uses established extremal-measure results, with the zero-atom premise supplied by [Jabłoński, Jung and Stochel](#references), §2.1, and the full deletion step by [Berg and Christensen](#references), Theorem 7. The logical lesson is precise: uniqueness of the initial representative plus positivity of every *individual moment* does not force later moment realizability.

Here the atom is itself computable. With $`q=e^{-1}`$, the finite Christoffel extremal values are
```math
w_N=
\frac{\det(b_{i+j})_{0\le i,j\le N}}
     {\det(b_{i+j})_{1\le i,j\le N}}
 =\prod_{j=1}^{N}(1-q^j),
\qquad
w=\prod_{j=1}^{\infty}(1-q^j),
\qquad
0\le w_N-w\le\frac{q^{N+1}}{1-q}.
\quad\text{(14)}\quad
```
For the determinant identity, factor the powers $`q^{-i^2/2}`$ and $`q^{-j^2/2}`$ from rows and columns, leaving a Vandermonde matrix in $`q^{-j}`$; the ratio cancels all but the displayed factors. Extremality makes the orthogonal polynomials complete in $`L^2(\eta_K)`$. Evaluation at the atom has squared norm $`1/w`$, so Parseval identifies the decreasing Christoffel limit with $`w`$. The final error bound follows from $`1-\prod(1-u_j)\le\sum u_j`$. This gives exact names for (12)–(13), not merely a nonconstructive counterexample.

The shifted Hankel matrices remain positive definite:
$`\sum v_i v_j B_{i+j+1}(t)=\int x(\sum v_i x^i)^2e^{-tx}\,d\mu>0`$.
Only the unshifted positivity can fail. For $`G_N(t)=(B_{i+j}(t))_{0\le i,j\le N}`$, the unnormalized unshifted matrix is
```math
G_N(t)-w e_0e_0^{\mathsf T}.
```
It is positive semidefinite exactly when
$`w\le(e_0^{\mathsf T}G_N(t)^{-1}e_0)^{-1}`$, by completing the square after applying $`G_N^{1/2}`$. At zero this threshold is $`w_N>w`$, so each fixed truncation passes on some initial interval. At every positive time some truncation must fail, by the Stieltjes existence theorem. The necessary detecting degree therefore tends to infinity towards zero.

One can locate a strict negative quadratic form effectively at any fixed rational positive time in the stated interval. Express
$`B_r(t)=E[\exp(rZ-te^Z)]`$. For $`M>r`$, the omitted two tails are bounded by
$`e^{r^2/2}\{Q(M-r)+Q(M+r)\}`$, and the usual Gaussian bound
$`Q(u)\le e^{-u^2/2}/(\sqrt{2\pi}u)`$ makes this computable. On the compact integration interval, the derivative is the integrand times $`r-te^z-z`$, giving a certified quadrature bound. Together with (14), this computes
$`\sum v_i v_j B_{i+j}(t)-wv_0^2`$. Enumerating rational vectors and dovetailing strict upper-bound tests eventually finds a negative one. There is no uniform degree or termination-time estimate near zero.

The predecessor calculation also gave an actual low-degree witness at $`t=1/10`$, namely $`1-17x/50`$, with a negative interval between $`-0.038075910`$ and $`-0.032572829`$ for the unnormalized quadratic form. That numerical certificate and its independent review are retained as historical evidence; the general proof above does not treat a fresh numerical or kernel execution as having occurred. This section incorporates [the determinate-initial construction][coordinate-counterexample-source], [its Hankel diagnosis][coordinate-diagnostic-source], and [its computational refinement][coordinate-computation-source].

### 4.3 A sufficient condition that really restores the scalar implication

**Theorem 8 (Stieltjes–Carleman recovery).** Suppose a coordinatewise nonnegative scalar hierarchy has a valid initial Stieltjes record $`c`$ satisfying
```math
\sum_{n=1}^{\infty}c_n^{-1/(2n)}=\infty.
\quad\text{(15)}\quad
```
Then the hierarchy is the actual tilt of its unique initial law.

**Proof.** If $`c_1=0`$, that law is $`\delta_0`$; since $`a_1'=-a_2\le0`$ and $`a_1(0)=0`$, all the required conclusions follow. Otherwise fix $`s>0`$ in the supplied interval. The backward Taylor argument in Theorem 6 gives an analytic generating function
```math
a_0(s(1-z))
 =\sum_{j=0}^{\infty}p_j z^j,\qquad
p_j=\frac{s^j a_j(s)}{j!}\ge0,\quad 0\le z<1.
```
Monotone convergence as $`z\uparrow1`$ gives $`\sum p_j=1`$. Thus these numbers define an integer-valued random variable $`N`$. Differentiating the generating function and taking the same boundary limit yields factorial moments
$`E(N)_r=s^r c_r`$.

Let $`X`$ have the initial representing law, and let $`Y`$, conditionally on $`X`$, be Poisson with mean $`sX`$. It has the same factorial moments, hence the same ordinary moments
```math
d_n=\sum_{k=0}^{n}S(n,k)s^k c_k,
```
where $`S(n,k)`$ are Stirling numbers of the second kind. The estimate
$`S(n,k)\le\binom nk n^{n-k}`$ follows by choosing one representative per block and assigning the other elements to at most $`n`$ possibilities. Hölder gives $`c_k\le c_n^{k/n}`$. Therefore
```math
d_n\le\bigl(s c_n^{1/n}+n\bigr)^n,
\qquad
d_n^{-1/(2n)}
 \ge\frac1{\sqrt2}
       \min\{s^{-1/2}c_n^{-1/(2n)},\,n^{-1/2}\}.
\quad\text{(16)}\quad
```
The sequence $`b_n=c_n^{-1/(2n)}`$ is nonincreasing. Cauchy condensation proves divergence of the right-hand series: at the dyadic indices its condensed terms are the minimum of the divergent terms $`s^{-1/2}2^k b_{2^k}`$ and $`2^{k/2}`$. If the latter bound is active infinitely often, the terms do not even tend to zero; if it is active only finitely often, divergence is inherited from the first series. The minimum is itself nonincreasing before condensation.

Thus $`d`$ satisfies the Stieltjes Carleman condition. Both $`N`$ and $`Y`$ are nonnegative laws, so they have the same distribution. Their probability generating functions give
$`a_0(s(1-z))=E[e^{-s(1-z)X}]`$ for $`0\le z<1`$. Differentiation and analytic continuation identify every $`a_r`$, hence the whole path. ∎

The relevant criterion is (15), not the stronger series $`\sum c_n^{-1/n}`$. For example, $`c_n=(2n)!`$ satisfies (15) but not that stronger condition. The mixed-Poisson argument is related to the determinacy transfer studied by [Kuba and Panholzer](#references), but their quoted Hamburger formulation is not silently substituted for the Stieltjes transfer proved here. Proposition 7 and Theorem 8 delimit different hypotheses: determinacy alone is weaker than the quantitative Carleman condition. The proof is part of [the same scalar correction][coordinate-counterexample-source].



## 5. Coercive polynomial energies: positivity forces actual laws

The scalar argument uses the order of the half-line. In several variables, nonnegative coordinates are no longer an adequate substitute for positivity on squares, and square positivity alone is not a general representation theorem. Dynamics supplies additional restrictions. This section proves that those restrictions are sufficient for **every coercive polynomial energy**, not only quadratic energies or energies with a convenient SOS certificate.

### 5.1 Unnormalization and exhaustion under actual representability

For any solution of (1), define
```math
a(t)=\exp\!\left(-\int_0^tL_u(h)\,du\right),
\qquad A_t(p)=a(t)L_t(p).
```
Then
```math
A_t'(p)=-A_t(hp),\qquad
A_t^{(n)}(p)=(-1)^nA_t(h^np).
\quad\text{(17)}\quad
```
The second identity follows by repeatedly applying the first to a polynomial. It requires no unbounded-operator calculus.

**Lemma 9 (lower-bounded exhaustion).** Let $`h`$ be a lower-bounded polynomial. A normalized coordinatewise $`C^1`$ solution of (1) that has an actual probability representative at every time is the moment path of $`\mathcal T_t^h\mu`$ for some initial $`\mu\in\mathcal P_\infty(\mathbb R^d)`$. More generally, after shifting $`h\ge0`$, it suffices to assume $`A_t(q^2h^n)\ge0`$ for every $`q,n,t`$ and a representative at one positive time.

**Proof.** A constant shift changes $`a`$ but not $`L`$. With $`h\ge0`$, the backward Taylor argument gives
```math
\sum_{n=0}^{N}\frac{b^n}{n!}A_t(q^2h^n)
 \le A_{t-b}(q^2),\qquad 0\lt{}b\le t.
\quad\text{(18)}\quad
```
It proves interior analyticity of $`A_t(q^2)`$, hence of every $`A_t(p)`$ by
$`p=((p+1)^2-(p-1)^2)/4`$. Choose the one representative $`\rho_s`$ and set $`\lambda_s=a(s)\rho_s`$. Monotone convergence in (18) gives
$`\int q^2e^{bh}\,d\lambda_s\le A_{s-b}(q^2)`$ for $`b<s`$.
The analytic function
$`u\mapsto\int q^2e^{(s-u)h}\,d\lambda_s`$ has the same derivatives at $`s`$ as $`A_u(q^2)`$, so the two agree throughout $`u>0`$ in the supplied interval. Monotone convergence as $`u\downarrow0`$ gives
$`\mu=e^{sh}\lambda_s`$, with $`\int q^2\,d\mu=A_0(q^2)`$. Its mass is one. The bound $`|p|\le(1+p^2)/2`$ gives every absolute polynomial moment. Polarization recovers all coordinates and normalization gives the claimed tilt. ∎

The supplied path determines its continued moment record even when it does not identify its initial law. For two initial laws under a fixed lower-bounded $`h`$, the exact equivalence is
```math
\mu\sim_h\nu
\quad\Longleftrightarrow\quad
h_*(p\mu)=h_*(p\nu)
\ \text{as finite signed measures for every polynomial }p.
\quad\text{(19)}\quad
```
Indeed, equality of the normalized path fixes the unnormalizer from $`L_t(h)`$ and hence fixes every integral $`\int p e^{-th}\,d\mu`$. Signed Laplace uniqueness gives (19); the reverse implication is immediate. Thus the set of paths from a fixed initial moment record is its representing fibre modulo (19). Inverse multiplication by the positive weight identifies the law-level lifts of any one complete path with the representing fibre at any positive time. A unique lift is equivalent to determinacy at one, and then at every, positive time. A determinate initial record guarantees a unique path, but the converse fails for a constant energy: every initial representative then gives the same constant record.

### 5.2 Even derivatives yield exponential energy control

**Lemma 10 (interior energy bounds).** For an arbitrary real polynomial $`h`$, a square-positive solution of (1) has analytic unnormalized coordinates at every positive interior time. At $`s`$ and any $`b>0`$ with $`[s-b,s+b]\subset[0,T)`$,
```math
A_s(q^2h^{2n})
 \le C_q\,\frac{(2n)!}{b^{2n}},
\qquad
C_q=\frac{A_{s-b}(q^2)+A_{s+b}(q^2)}2.
\quad\text{(20)}\quad
```

**Proof.** For $`f(t)=A_t(q^2)`$, (17) gives
$`f^{(2n)}(t)=A_t((qh^n)^2)\ge0`$.
Taylor expansion to order $`2N+1`$ at $`s`$ in the two directions has nonnegative even-order integral remainders. Adding the expansions cancels the odd terms:
```math
\sum_{n=0}^{N}\frac{b^{2n}}{(2n)!}A_s(q^2h^{2n})
 \le\frac{f(s-b)+f(s+b)}2.
```
This proves (20). The Cauchy–Schwarz inequality for a positive polynomial functional follows from the discriminant of $`A((u+\lambda v)^2)\ge0`$. Applied to $`u=qh^n`$, $`v=qh^{n+1}`$, it bounds the odd derivatives by
$`\sqrt2 C_q(2n+1)!b^{-(2n+1)}`$.
Taking a common smaller $`b`$ in a neighborhood of $`s`$ gives uniform derivative bounds. Taylor's remainder tends to zero there, proving analyticity for squares and then by polarization for every polynomial. ∎

This is an interior assertion. The flat examples at zero remain possible outside the required positivity classes. The radius $`b`$ in (20) is common to all polynomials; their constants $`C_q`$ may differ. That common radius matters in the next existence argument.

The pure-killing generator is essential to this even-derivative proof. Put R(x)=|x|² in dimension d≥1 and change the unnormalized generator to L=Δ−R. The chain rule gives ΔRⁿ=2n(2n+d−2)Rⁿ⁻¹ for n≥1, so radial moments now satisfy a_n′=2n(2n+d−2)a_(n−1)−a_(n+1), rather than a_n′=−a_(n+1). A concrete positive solution starting from a point mass at zero has, for t>0, density (2π sinh(2t))^(−d/2) exp(−coth(2t)R/2). Differentiating this Gaussian verifies ∂_tν=Δν−Rν; its mass tends to one and its variance tanh(2t) tends to zero. Gaussian integration gives mass M(t)=(cosh(2t))^(−d/2) and first radial moment a_1(t)=d tanh(2t)M(t). Thus a_1′(0)=2d while M″(0)=−2d, and continuity makes M″ negative at sufficiently small positive times too. Positivity of every square moment therefore does not supply the nonnegative even time derivatives used above after this generator change. This is a failure of transferring that proof to diffusion, not a counterexample to the theorem for its original pure-killing hierarchy. The density verification and Gaussian integration are ordinary calculations stated here; the archival control body supplies the radial identity and endpoint expressions but was not executed, and its named polynomial-failure variant is not credited as a passing analytic or symbolic verification. [AFTER1384-S12-230](../research/t20-v6-20261012/sources/418d4f201ad75908ee3864736def88169147f2d6868f8be261428dcf6cebc09a/independent_controls.poly_failure.py#L22-L29) [AFTER1384-S12-230](../research/t20-v6-20261012/sources/418d4f201ad75908ee3864736def88169147f2d6868f8be261428dcf6cebc09a/independent_controls.poly_failure.py#L50-L65) [AFTER1384-S12-230](../research/t20-v6-20261012/sources/418d4f201ad75908ee3864736def88169147f2d6868f8be261428dcf6cebc09a/independent_controls.poly_failure.py#L89-L102)

The separate Mehler control supplies a positive general-start calculation alongside that failed transplant. In one dimension put c=sech(2t), v=tanh(2t), and M(t,y)=(cosh(2t))^(−1/2) exp(−v y²/2). For t>0 the displayed kernel has Gaussian conditional mean cy and variance v, with total mass M. Its monomial integral is M Q_m, where Q_m=Σ_{j=0}^{⌊m/2⌋} m! (cy)^(m−2j)v^j/[(m−2j)!2^j j!], and Q_m=0 for negative m. Differentiating c′=−2cv, v′=2c² and M′/M=−v−c²y² gives (−v−c²y²)Q_m−2cv ∂_cQ_m+2c²∂_vQ_m=m(m−1)Q_(m−2)−Q_(m+2); at c=1,v=0 the initial polynomial is y^m. These are the Gaussian polynomial identities for Δ−x², with the factor M retained rather than silently normalizing away killing. The source requests exact symbolic checks through degree sixteen, a density-equation check modulo cosh²(2t)−sinh²(2t)=1, and a separate Fourier check modulo c²+v²=1. Its radial interpolation, Riccati and barrier checks are finite supporting obligations, not a proof that arbitrary square-positive functional paths admit this kernel representation. Neither the program nor its dependencies were executed; uniqueness, analytic interchange and a general functional-to-measure theorem remain separate. [AFTER1884-V25-101](../research/t20-v6-20261012/sources/715bc187849945eb704979c482519e0c987a8c6525435383f25ce4555114df3a/check_controls.py#L62-L94)

A separate two-atom calculation keeps transport and normalization visible. For a,b,x,z>0, set μ=aδ₀+bzδₓ, N=a+bz and m_j=a·1_{j=0}+bz x^j. On an interval where this positive configuration exists, ẋ=x² and ż=−x⁴z give, by product differentiation, ṁ_j=j m_{j+1}−m_{j+4}; quotient differentiation therefore gives q̇_j=j q_{j+1}−q_{j+4}+q₄q_j for q_j=m_j/N, including q₀=1. The normalized correction term cannot be deleted merely because the unnormalized weights satisfy a simpler equation. The raw second-order minor is Nm₂−m₁²=abzx²>0, so the two positive distinct atoms have positive variance after normalization. For the reversed field, x(t)=1/t and z(t)=exp(−1/(3t³)), t>0, satisfy ẋ=−x² and ż=x⁴z, and all signs in the displayed normalized evolution reverse. These identities are ordinary product and quotient calculations; the source's generalized-weight and degree-zero-through-nine symbolic requests were not executed. They do not establish endpoint continuation, a continuum-density boundary condition or a universal realization theorem, and they are not the pure-killing hierarchy used above. [AFTER1634-S7-161](../research/t20-v6-20261012/sources/581fd198b7c4c4409f32e05c7b21b7dced6ad2119d7a89fb7874bf68f72c247c/independent_checks.py#L4-L30)

### 5.3 From energy fibres to a joint representing measure

**Lemma 11 (compact algebraic fibres).** Let $`\Lambda`$ be a nonzero square-positive polynomial functional. Suppose each level set $`K_r=\{x:h(x)=r\}`$ is compact, and for one common $`b>0`$ and every polynomial $`q`$ there is $`C_q<\infty`$ such that
```math
\Lambda(q^2h^{2n})\le C_q(2n)!b^{-2n}
\quad(n\ge0).
\quad\text{(21)}\quad
```
Then $`\Lambda`$ has a positive joint representing measure.

**Proof.** For each $`q`$, the one-variable functional
$`r\mapsto\Lambda(q^2r(h))`$ is positive on squares, hence has a Hamburger representative $`\nu_{q^2}`$. By the nonnegative series for $`\cosh`$ and (21),
$`\int\cosh(cz)\,d\nu_{q^2}(z)<\infty`$ whenever $`0<c<b`$.
Since $`e^{c|z|}\le2\cosh(cz)`$, these measures have an exponential absolute moment and are unique. The zero-mass case is the zero measure. More generally, a finite signed measure with an exponential absolute moment is determined by its polynomial moments: its Laplace transform is analytic in a strip, and zero moments force a zero Fourier transform there and hence a zero measure.

Define, by polarization,
```math
\nu_p=\frac{\nu_{(p+1)^2}-\nu_{(p-1)^2}}4.
```
Its moments are $`\Lambda(ph^n)`$. Signed uniqueness proves linearity in $`p`$ and $`\nu_{hp}(dz)=z\,\nu_p(dz)`$. It also proves that this definition for a square agrees with its positive scalar representative. For every Borel set $`B`$, the map $`p\mapsto\nu_p(B)`$ is square-positive. Its Cauchy–Schwarz inequality gives
```math
|\nu_p(B)|^2\le\nu_{p^2}(B)\nu_1(B).
```
Consequently every $`\nu_p`$ is absolutely continuous with respect to $`\nu_1`$.

Take Radon–Nikodym derivatives $`f_\alpha`$ for the countable family of monomials. Outside one common null set, $`f_0=1`$; all rational-coefficient square inequalities hold; and the finitely supported coefficient relations for $`\nu_{hx^\alpha}=z\nu_{x^\alpha}`$ hold. Define
$`\ell_z(\sum p_\alpha x^\alpha)=\sum p_\alpha f_\alpha(z)`$.
Continuity in each finite coefficient space extends positivity from rational to real squares. Thus $`\ell_z`$ is normalized, positive on all squares, and annihilates every multiple of $`h-z`$.

The compact algebraic-set moment theorem now applies: a positive functional annihilating that ideal is represented on the compact real zero set $`K_z`$. This is precisely the algebraic existence statement in [Schmüdgen](#references), revised Chapter 12, Corollary 12.34(iv). Empty fibres cannot carry such a normalized functional.

For any polynomial $`P`$ nonnegative on all of $`\mathbb R^d`$, the fibre representation gives $`\ell_z(P)\ge0`$ almost everywhere. Integration gives $`\Lambda(P)\ge0`$. Haviland's theorem therefore supplies a joint measure on $`\mathbb R^d`$ representing $`\Lambda`$. No measurable selection of the individual fibre measures has been used: only their implication for the measurable quantities $`\ell_z(P)`$ is integrated. ∎

The first scalar Hamburger step is not already a joint representation. Nor is uniqueness of an existing joint measure a substitute for this existence step. The proof preserves both distinctions.

### 5.4 The arbitrary coercive theorem

**Theorem 12 (coercive square-positivity theorem).** Let $`h\in\mathbb R[x_1,\ldots,x_d]`$ be coercive, meaning $`h(x)\to+\infty`$ as $`|x|\to\infty`$. Every normalized coordinatewise $`C^1`$ square-positive solution of (1) is the full moment path of $`\mathcal T_t^h\mu`$ for a unique $`\mu\in\mathcal P_\infty(\mathbb R^d)`$. Its record is determinate at every positive time. For each valid initial record, its square-positive hierarchy paths are in bijection with its initial representing laws; every such path has a unique global continuation.

**Proof.** Coercivity gives compact level sets. At each interior positive time, Lemmas 10–11 give an actual representative. This part does not assume that a nonnegative polynomial is SOS or that the initial record already has a measure. Shift $`h`$ by its finite lower bound so that $`h\ge0`$. The positive-time representatives now imply $`A_t(q^2h^n)\ge0`$; continuity gives the same at zero. Lemma 9 produces an initial measure and the actual tilt.

It remains to establish determinacy. Let $`\lambda`$ be a positive-time unnormalized measure. The backward bound gives $`\int e^{bh}\,d\lambda<\infty`$ for some $`b>0`$. If $`\lambda'`$ has the same polynomial moments, the nonnegative exponential series in the polynomial $`h`$ gives the same finite bound for $`\lambda'`$. For each polynomial $`p`$, Cauchy–Schwarz shows that
$`\tau_p=h_*(p\lambda-p\lambda')`$ has a positive exponential absolute moment, at a smaller rate. All its moments vanish, so signed uniqueness gives $`\tau_p=0`$.

For each $`R`$, it follows that the restrictions of $`\lambda`$ and $`\lambda'`$ to the compact sublevel set $`\{h\le R\}`$ agree on all polynomials. Polynomial density on that compact set gives equality of the restrictions. Exhausting the space gives $`\lambda=\lambda'`$. Positive-time determinacy and inverse weighting identify the initial law for the whole path. Conversely, the lower bound on $`h`$ makes the tilt well defined for every nonnegative time and permits polynomial dominated differentiation. This proves the bijection and global extension. ∎

The compact-sublevel proof also works on a fixed closed support set whose energy sublevels are compact. A direct disintegration theorem with a **strictly determinate** base is not invoked under the weaker claim of ordinary determinacy; the compact-sublevel argument avoids that mismatched hypothesis. This corrects a potential shortcut identified in [the independent tensor review][tensor-review-source].

There is a useful independent proof in the quadratic case. For $`h=|x|^2`$, the difference $`h^n-x_i^{2n}`$ is SOS. Equations (18) therefore give
```math
L_t(x_i^{2n})\le\frac{n!}{a(t)t^n}.
```
Each marginal Carleman series diverges, since its terms are bounded below by a constant times $`n^{-1/2}`$. The multivariate Carleman theorem supplies existence from full square positivity and uniqueness from all marginal conditions. More generally, $`h-c|x|^2`$ SOS gives the same argument with $`ct`$. The relevant theorem, recalled by [Putinar and Schmüdgen](#references), Theorem 25, gives existence when all but at most one marginal satisfy Carleman, and determinacy when all do. This separate route will matter for hidden coordinates below.

A polynomial change of coordinates may make that quadratic route available without a radial bound in the original coordinates. If $`\Phi`$ is a polynomial automorphism with polynomial inverse and $`h=|\Phi(x)|^2+C`$, apply the quadratic argument in $`\Phi`$-coordinates. For example, $`\Phi(x,y)=(x,y-x^k)`$ gives
$`h=x^2+(y-x^k)^2`$. Along $`(r,r^k)`$, this is $`r^2`$, so for $`k\ge3`$ it need not dominate even the first power of the ambient norm at infinity. Coercivity, rather than a presumed quadratic growth rate, is the invariant condition in Theorem 12.

The cubic shear gives a quantitative distinction between compact energy sublevels and domination by squared energy. For all (x,y)∈ℝ², put u=x−y³, F=u²+y², H=1+F and R=x²+y². Then R=(u+y³)²+y²≤2u²+2y⁶+y²≤3H+2H³. In particular H≥1 and {H≤M} lies in the closed radius-squared bound R≤3M+2M³ for every M≥1, so these sublevels are compact. Nevertheless, along x=y³, (F+C)²−cR=(y²+C)²−c(y⁶+y²) has negative leading coefficient for every real C and every c>0. No constant energy shift therefore supplies that squared-energy domination. The positive cubic envelope and negative quadratic-envelope result are elementary all-state polynomial bounds, not extrapolations from the source’s finite symbolic checks. The inverse shear (u,y)↦(u+y³,y) is a static change of coordinates, not a proposed gradient flow; this comparison alone proves no analytic localization or measure-representation theorem. [AFTER2384-NINTH25-212](../research/t20-v6-20261012/sources/c0776992ab1ae215a00e9578fdc8164b214bd4141ec8c27e4749fdbf0841f0f2/check_exact.py#L73-L88)

A reviewed transport-and-killing extension requires stronger algebraic energy premises than the pure-reweighting theorem above. Let H be a coercive SOS polynomial and b a polynomial vector field with the actual SOS certificate S=−b·∇H. Suppose L_t is normalized and square-positive on the whole polynomial algebra at every supplied time, every coordinate is C¹ through zero with continuous right derivative, and L′_t(p)=L_t(b·∇p−Hp)+L_t(H)L_t(p) on a nontrivial interval. With A_t=a(t)L_t and a=exp(−∫L_t(H)dt), put b_n=A_t(H^n). Then b_n′=−nA_t(H^(n−1)S)−b_(n+1) and b_0′=−b_1. Products of SOS polynomials make the discarded terms nonnegative, so repeated integration from b_0(0)=1 gives b_n(t)≤n!t^(−n). Polynomial-functional Cauchy–Schwarz and the 4n-factorial bound yield the common weighted energy strip required by the compact-fibre representation lemma, with width t/2 and a constant allowed to depend on the polynomial. Positive-time representatives are determinate by signed energy-pushforward uniqueness and compact-sublevel polynomial density. This argument does not replace SOS by merely pointwise energy decrease before representation, assume initial representability, or require spatial Carleman bounds. The received review supplies this extension's ordinary proof account; its author controls, formal dependencies and primary-source checks were not rerun or reopened here. [AFTER3384-THIRD25-069](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/093d123354273d72f5a7461e64b9326f541e62c59113d55a777855d7d574ea1d/REVIEW.md#L7-L21) [AFTER3384-THIRD25-069](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/093d123354273d72f5a7461e64b9326f541e62c59113d55a777855d7d574ea1d/REVIEW.md#L86-L96)

Passing that transport hierarchy to a compact-test PDE requires a further argument, not determinacy alone. On an interior time interval its represented laws have uniform polynomial moments and a common exponential energy strip. The integrated residual D is an order-one distribution. The product rule for pP(H) retains both (b·∇p−Hp)P(H) and p(b·∇H)P′(H). Taylor approximation and analytic continuation in the scalar energy frequency give D(pe^(iξH))=0; scalar Fourier inversion gives D(pχ(H))=0. The signed scalar coefficients cancel as a distribution and need not vanish separately. For compactly supported χ, coercivity makes χ(H)D compactly supported with a C¹ seminorm bound. Coordinate exponential Taylor polynomials then converge together with first derivatives, forcing that localized distribution to vanish. Choosing χ=1 near H(supp φ) proves D(φ)=0 for every compact smooth spatial test. Energy decrease traps characteristics in compact sublevels, and weighted backward tests with a fixed spatial cutoff identify the law. Tightness and polynomial uniform integrability at zero recover one initial all-moment law for the whole path; positive weights and the inverse flow on its actual image give uniqueness without inferring initial determinacy from moments alone. Polynomial coercivity supplies a polynomial sublevel-radius bound for the converse. The review therefore supports unique continuation of each supplied path under these hypotheses, not convergence of arbitrary energy-controlled drift, all-space backward flow, stable inversion or a smooth manifold of all laws. [AFTER3384-THIRD25-069](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/093d123354273d72f5a7461e64b9326f541e62c59113d55a777855d7d574ea1d/REVIEW.md#L23-L84)

A more tightly confined gradient subclass has a quantitative radial proof that does not need a polynomial inverse flow. Fix κ>0 and λ,D,C≥0 with actual SOS certificates V=F+C and Q=x·∇F−κR²+λR+D, where R=|x|². For the normalized, fully square-positive gradient/killing hierarchy with polynomial coordinates C¹ through zero, set A_t=a(t)L_t, a=exp(−∫₀ᵗL_s(V)ds), and a_n=A_t(R^n) for n≥1. Then a_n′=2nD a_(n−1)+2λn a_n−2κn a_(n+1)−2nA_t(R^(n−1)Q)−A_t(VR^n). Every discarded term is nonnegative by square positivity and SOS products, before any measure is assumed. Polynomial Cauchy–Schwarz gives radial log-convexity, hence a_(n−1)≤a_0^(1/n)a_n^((n−1)/n) and a_(n+1)≥a_n^((n+1)/n)/a_0^(1/n), reading the first inequality at n=1 simply as a_0=a_0. Since 0<a_0≤1, u_n=a_n^(1/n) satisfies u_n′≤2D+2λu_n−2κu_n² wherever positive. Compare with a strictly positive finite-initial Riccati solution: any interval of excess lies in that differentiable positive set, and the local Lipschitz/Gronwall argument excludes it. No derivative at a zero root is required. Taking the supremum of finite-initial comparators yields a_n(t)≤Y(t)^n, where Y(t)=[λ+Δ coth(Δt)]/(2κ), Δ=√(λ²+4κD)>0, and Y(t)=1/(2κt) when Δ=0. This is a derived envelope, not an initial-value problem started at infinity. [After3884 source 163, lines 13–50](../research/t20-v6-20261012/sources/3475ad324dbb7f872fec00c7e9a1161581bafed80eefebb43de2604ade5c911d/REVIEW.md#L13-L50)

The geometric bound makes the represented positive-time laws compactly supported: R^n−x_i^(2n) is SOS, so L_t(x_i^(2n))≤a(t)^(−1)Y(t)^n satisfies every marginal Carleman condition; the stated multivariate representation theorem gives existence and determinacy. Markov's inequality applied to A_t(R^n) and n→∞ then gives no mass outside R≤Y(t). On positive-time compact intervals there is one common compact support, permitting the polynomial-to-Fourier compact-test passage without an assumed measurable choice of representatives. Radial comparison also gives |Φ_t(x)|²<Y(t) for every finite starting point, while dropping the negative quadratic term gives |Φ_t(x)|²≤e^(2λt)|x|²+2D∫₀ᵗe^(2λs)ds and forward completeness. Local reversed uniqueness makes Φ_t injective, and its positive Jacobian determinant makes it a diffeomorphism onto its open image O_t, not onto all of Euclidean space. Positive characteristic weights and that image-only inverse recover the one initial all-moment law from a supplied path, with polynomial uniform integrability at zero providing the boundary passage. Thus each positive-time law assigns no mass to the comparison sphere, although its topological support can meet it. If the initial full Hankel rank is finite r, its law has exactly r atoms; positive weights and injective characteristics preserve them. Neither stable inverse reconstruction nor global-minimizer convergence follows. [After3884 source 163, lines 52–94](../research/t20-v6-20261012/sources/3475ad324dbb7f872fec00c7e9a1161581bafed80eefebb43de2604ade5c911d/REVIEW.md#L52-L94) [After3884 source 163, lines 96–110](../research/t20-v6-20261012/sources/3475ad324dbb7f872fec00c7e9a1161581bafed80eefebb43de2604ade5c911d/REVIEW.md#L96-L110)

The additive radial constant is a substantive hypothesis relaxation, as the already displayed shifted-well fixture shows. For F(x)=(x−1)^4/4 one has xF′−x^4/4+x²+1/4=(3/4)(x²−2x)²+(x−1/2)², so κ=1/4, λ=1, D=1/4 and C=0 meet the certificate conditions. No D=0 certificate of this form exists in these coordinates: its nonnegative Q would vanish at zero and therefore have derivative zero there, whereas Q′(0)=F′(0)=−1. The characteristic starting at zero nevertheless moves immediately, as in the null-ideal example below, so its initially zero positive radial moments cannot be assumed strictly positive through the initial endpoint or frozen forever. The zero-safe comparison above covers this case. This reuses the existing translated-quartic example to distinguish certificate classes; it is not a new independent gradient model or evidence of generic optimization. [After3884 source 163, lines 96–106](../research/t20-v6-20261012/sources/3475ad324dbb7f872fec00c7e9a1161581bafed80eefebb43de2604ade5c911d/REVIEW.md#L96-L106)

The theorem also genuinely exceeds the SOS-dominance route. The Motzkin form
```math
M(x,y,z)=x^4y^2+x^2y^4+z^6-3x^2y^2z^2
```
is nonnegative by the arithmetic–geometric mean inequality. The energy $`h=M+x^2+y^2+z^2`$ is coercive, but no choice of scalar $`C`$ and $`c>0`$ makes $`h+C-c|x|^2`$ SOS. Otherwise its leading homogeneous part $`M`$ would be a sum of squares of cubics. The zero coefficients of $`x^6,y^6`$ eliminate the cubic monomials $`x^3,y^3`$ from every summand. The zero coefficients of $`x^4z^2,y^4z^2`$ then eliminate $`x^2z,y^2z`$, and those of $`x^2z^4,y^2z^4`$ eliminate $`xz^2,yz^2`$. The coefficient of $`x^2y^2z^2`$ would consequently be a sum of squares of the remaining $`xyz`$ coefficients, and so could not equal $`-3`$. Theorem 12 nevertheless applies.

These arguments reconcile [the vector realizability theorem][tensor-source] with [its stronger coercive-polynomial successor][coercive-source]. The earlier unresolved general-coercive question is closed by the latter proof; it is not retained here as an open problem.

### 5.5 What the hypotheses prevent

Full energy information alone need not be full state information. Take independent $`X`$ uniformly distributed on $`\{0,1\}`$ and $`Y`$ with either law in (8). Under $`h(x,y)=x^2`$, only the first coordinate tilts. All mixed moment paths coincide, although the joint laws remain distinct. This is the noncoercive equivalence in (19).

Even identical energy distributions can conceal different full responses under a coercive energy. On the two half-lines, put densities
$`\tfrac12 f(r)(1+\varepsilon\sin(2\pi\log r))`$ at $`+r`$ and
$`\tfrac12 f(r)(1-\varepsilon\sin(2\pi\log r))`$ at $`-r`$, and reverse the signs for a second law. Their odd moments vanish, their even moments equal $`e^{2n^2}`$, and their $`x^2`$ distributions agree. Nevertheless the full records under $`h=x^2`$ differ at every positive time by Theorem 12. The first moments have opposite signs as functions and cannot agree on any positive interval, though a claim that the first moments differ at every individual time would be stronger than proved.

Lower bounds also control the time horizon. For mass $`2^{-n-1}`$ at $`x=-n`$ and energy $`h=x`$, the normalizer is
$`Z(t)=(2-e^t)^{-1}`$, finite only for $`t<\log2`$, and the tilted mean is $`-e^t/(2-e^t)`$. A real quadratic polynomial $`x^{\mathsf T}Bx+b\cdot x+c`$ is bounded below exactly when the symmetric matrix $`B`$ is positive semidefinite and $`b`$ lies in its range. A negative eigenvector gives quadratic descent to minus infinity; a linear component along the kernel gives linear descent; otherwise completing the square gives a lower bound. Signed energies require the different analysis that follows.



## 6. Signed energies, finite horizons, and exact null ideals

A scalar shift cannot make an arbitrary polynomial energy nonnegative. For signed energies, forward damping can become amplification on part of the support. The backward monotonicity used in Lemma 9 must then be replaced by the even-derivative argument and a hypothesis about the initial energy distributions.

### 6.1 Weighted energy determinacy

**Theorem 13 (signed-energy exhaustion).** Let $`h`$ be any real polynomial, and let a normalized square-positive coordinatewise $`C^1`$ solution of (1) have initial moment functional $`L_0=L_\mu`$ for $`\mu\in\mathcal P_\infty(\mathbb R^d)`$. Suppose that, for every polynomial $`q`$, the finite positive measure
$`h_*(q^2\mu)`$ on $`\mathbb R`$ is Hamburger-determinate. Then throughout the supplied interval,
```math
A_t(p)=\int p(x)e^{-th(x)}\,d\mu(x),\qquad
L_t(p)=\frac{\int p e^{-th}\,d\mu}{\int e^{-th}\,d\mu}.
\quad\text{(22)}\quad
```
In particular, the existence of the square-positive path forces all these weighted integrals to be finite. No positive-time joint representative is assumed.

**Proof.** For a fixed $`q`$ and positive interior $`t`$, the scalar functional
$`r\mapsto A_t(q^2r(h))`$ is positive on squares. Hamburger existence gives a measure $`\sigma_t^q`$ with moments $`A_t(q^2h^n)`$. Lemma 10 and the cosh series give a positive exponential absolute moment, hence uniqueness of this scalar measure.

For sufficiently close positive times $`u,v`$, the analytic function
$`v\mapsto\int e^{-(v-u)z}\,d\sigma_u^q(z)`$ has exactly the derivatives of $`A_v(q^2)`$ at $`u`$. Equality near $`u`$ and differentiation identify all moments at $`v`$. The scalar measures are determinate there, so
```math
\sigma_v^q(dz)=e^{-(v-u)z}\sigma_u^q(dz).
\quad\text{(23)}\quad
```
A common smaller time radius on any compact interior interval follows from (20); a finite chain of overlapping neighborhoods extends (23) between any two positive times.

Fix $`s>0`$ and put $`\tau_q=e^{sz}\sigma_s^q`$. To see that this is a finite measure with the correct initial moments, use (23) and let $`u\downarrow0`$. On $`z\ge0`$, the even-moment integrands $`z^{2n}e^{(s-u)z}`$ increase monotonically. On $`z<0`$, they are dominated by their value at one fixed earlier positive time. Their limits therefore have moments $`A_0(q^2h^{2n})`$. Bounds by neighboring even powers handle the odd moments. In particular $`\tau_q`$ is finite and represents the entire initial scalar sequence $`L_\mu(q^2h^n)`$.

The hypothesis now identifies $`\tau_q=h_*(q^2\mu)`$. Evaluating (23) at total mass gives
$`A_t(q^2)=\int q^2e^{-th}\,d\mu`$. Polarization gives (22) for every polynomial, and its value at one is the normalizer. ∎

Two readily checked sufficient conditions are useful. If $`|h|\le M`$ almost surely under $`\mu`$, every weighted energy measure has support in $`[-M,M]`$ and is determinate. This conclusion does not require compact joint support. If instead $`\int e^{a|h|}\,d\mu<\infty`$ for some $`a>0`$, Cauchy–Schwarz with $`q^4`$ gives an exponential absolute moment for every weighted energy measure at rate $`a/2`$, and hence the same determinacy. The weighted integrals needed for a path are then finite at least for $`0\le t<a/2`$.

The exact forward domain for a specified initial law is the set of times at which
$`\int q^2e^{-th}\,d\mu<\infty`$ for every polynomial $`q`$. On the interior of any such interval starting at zero, the normalized tilt satisfies (1). To justify differentiation, bracket an interior time by two nearby times and split according to the sign of $`h`$; the two endpoint weights dominate the derivative with each fixed polynomial factor. At zero use an available positive endpoint on $`h<0`$ and the original moments on $`h\ge0`$. Thus if $`T_\mu`$ is the supremum of these open forward intervals, the actual path exists on $`[0,T_\mu)`$. The supremum is not automatically an admissible endpoint. Theorem 13 precludes a square-positive continuation beyond a true weighted-integrability obstruction under its determinacy hypothesis.

### 6.2 Algebraic degeneracy is preserved exactly

**Corollary 14 (null ideals and finite Gram ranks).** Every normalized square-positive solution of the autonomous hierarchy, even without an assumed initial representing measure, satisfies
```math
I_t:=\{q:L_t(q^2)=0\}=I_0
\quad(0\le t\lt{}T).
\quad\text{(24)}\quad
```
For every fixed finite polynomial family, its Gram matrix has the same kernel and rank throughout the interval.

**Proof.** Construct the scalar $`\sigma_s^q`$ and its boundary measure $`\tau_q`$ as in Theorem 13; this construction used positivity and continuity, not the initial representation or determinacy hypothesis. Their masses are respectively $`A_s(q^2)`$ and $`A_0(q^2)`$, and $`\tau_q=e^{sz}\sigma_s^q`$. Multiplication by a strictly positive finite function has zero total mass exactly when the original positive measure is zero. This proves both directions of (24).

Cauchy–Schwarz shows that a null polynomial pairs to zero with every polynomial. In particular,
$`L(q^2r^2)=L(q\cdot qr^2)=0`$, so the null space is an ideal. The kernel of the Gram matrix for $`p_1,\ldots,p_N`$ consists of coefficient vectors whose polynomial $`\sum c_i p_i`$ lies in that ideal. Equation (24) gives the conclusion. ∎

The result concerns an exact kernel, not uniform eigenvalue bounds or conditioning. Nor does it prevent a rank change in an infinite-time limit. It strengthens a merely forward-persistence claim: no polynomial null relation can appear or disappear at a finite time inside the admitted interval.

The fixed-polynomial null ideal need not persist after transport is added to pure killing. Take F(x)=(x−1)^4/4 and the negative-gradient characteristic X(t)=1−(1+2t)^(−1/2) starting at zero, for t≥0. Direct differentiation gives X′=−F′(X), and X(t)>0 for every t>0. Positive killing followed by normalization leaves the one-atom law δ_X(t), so L₀(x²)=0 while L_t(x²)=X(t)²>0. The zero set of this fixed polynomial has therefore lost its full mass under the moving law. This does not challenge Corollary 14: its pure-killing equation A′_t(p)=−A_t(Fp), with no spatial transport, has been replaced by A′_t(p)=A_t(−F′p′−Fp). Nor is this a statement about whether a regular flow preserves Lebesgue-null sets. The relation x−X(t)=0 remains valid at the moving atom, but it is a time-dependent polynomial rather than the same null polynomial at every time. These are ordinary consequences of the displayed characteristic, not an executed symbolic control or a general transport-and-killing representation theorem. [AFTER2384-NINTH25-202](../research/t20-v6-20261012/sources/bec5b6e438f261f46e14bcb76d2ef4f3f23580db309d018a3ffb81376b239f1a/check_exact.py#L149-L159) [AFTER2384-NINTH25-207](../research/t20-v6-20261012/sources/bfc758edda4fe5492f42a28d58f122986060b5446d637a5b860ffb690503f3d7/check_controls.py#L126-L137)

Transport can also change a finite Gram rank at a finite time when an atom escapes and its weight vanishes sufficiently rapidly. For 0≤t<1, set X=(1−t)⁻¹, C=exp((1−(1−t)⁻³)/3), and μ_t=(δ₀+Cδ_X)/(1+C); set μ_t=δ₀ for t≥1. Then X′=X² and C′=−X⁴C. The unnormalized moments m_k=1_{k=0}+CX^k obey m′_k=k m_{k+1}−m_{k+4}, and the normalized moments q_k=m_k/(1+C) obey q′_k=kq_{k+1}−q_{k+4}+q₄q_k. Every fixed CX^k and all its time derivatives tend to zero at t=1: each derivative is the same exponential times a polynomial in X. Thus the moment path extends smoothly and satisfies this transport-and-killing hierarchy across the join. For the polynomial family (1,x), the normalized Gram determinant is CX²/(1+C)²>0 before the join and zero thereafter. This is a rank-two to rank-one change for the displayed positive laws, not a counterexample to the pure-killing corollary or to a transport theorem requiring globally controlled characteristics. The symbolic program specifies local identities; the exponential-dominates-polynomials argument supplies the join here without executing it or claiming general uniqueness. [AFTER2634-EIGHTH25-198](../research/t20-v6-20261012/sources/e1d60cd158f994e172b0b3e0c55895cd8c3f79f239b64602f27192d69d05b62d/check_exact.py#L5-L30)

The transport-preservation guide reports two distinct finite-atomic continuation repairs. One uses complete two-sided characteristics with the proof’s regularity assumptions and a locally uniform finite-rank promise. The other replaces two-sided completeness by forward completeness and a global lower bound on killing on each finite horizon; it reports uniqueness and injectivity, with recovery only on the actual forward image, not surjectivity onto all finite laws. Its stated coercive autonomous polynomial gradient/selection application still requires the rank promise. The same guide distinguishes forward noninjective escape from a separate reverse-inflow nonuniqueness construction under reversed coefficients. These are source-reported theorem contracts: the guide does not supply their full proofs or regularity conditions, and neither the concrete escape calculation nor this reading establishes those universal results anew. [After3884 ninth25 source 219, lines 7–15](../research/t20-v6-20261012/sources/38728d0f27d605c84ff671649fa344888171cccaa4b2d993780db446cb0fb782/README.md#L7-L15)

### 6.3 Examples separating the hypotheses

With $`\mu=N(0,1)`$ and $`h=x`$, the normalizer is $`e^{t^2/2}`$ and the tilted law is $`N(-t,1)`$ for all $`t\ge0`$. With the same initial law and $`h=-x^2`$, instead,
```math
Z(t)=(1-2t)^{-1/2},\qquad
L_t(x^{2n})=(2n-1)!!(1-2t)^{-n},
\quad 0\le t<1/2.
```
The energy has an initial exponential absolute moment, so Theorem 13 applies. The actual divergence at $`t=1/2`$ cannot be crossed by another finite coordinatewise square-positive solution with the same initial law and hierarchy.

Bounded energy does not imply joint-law identification. Let $`X`$ take $`\pm1`$ equally, let an independent $`Y`$ have either lognormal law (8), and set $`h=X`$. The normalizer is $`\cosh t`$ and
```math
L_t(X^aY^b)=e^{b^2/2}
\begin{cases}
1,&a\text{ even},\\
-\tanh t,&a\text{ odd}.
\end{cases}
```
Both distinct joint laws give the same full path. The weighted energy distributions are supported on two points, so Theorem 13 identifies the dynamics for each proposed initial law without identifying which joint law was chosen.

Signed energies also invalidate a nonnegative-derivative shortcut even on finite support. For atoms $`(0,1),(1/2,1/2),(1,0)`$ with weights $`(1/2,1/3,1/6)`$ and energy $`h=x-y`$, the weights at $`t=\log2`$ are $`(12,4,1)/17`$, with mean $`(3,14)/17`$ and energy mean $`-11/17`$. For $`q=1-x`$, the unnormalized derivative $`A_0'(q^2)`$ is $`1/2>0`$, not nonpositive. The same finite support admits nonlinear signed energy $`x^3-3y`$, with values $`-3,-11/8,1`$, so no linearity of the energy is being assumed.

On a compact initial support, every polynomial energy is bounded there. The same support persists, and any competing joint measure with the same moments is confined to a compact box by its high even moments; compact polynomial density then gives uniqueness. Applying Theorem 13 successively therefore allows locally finite piecewise-autonomous **signed** schedules. Their actual law is $`e^{-\int_0^t h_sds}\mu`$ after normalization. For the preceding three atoms, applying $`h=x-y`$ for duration $`\log2`$ and then $`-h`$ for duration $`\log3`$ gives weights $`(4,4,3)/11`$. This conclusion does not assert a theorem for arbitrary continuously changing signed polynomials on noncompact supports.

The finite compact-support control makes a continuously changing, noncoercive example explicit. Fix atoms (0,0,0), (1,2,−1), (2,−1,3) with weights (1/2,1/3,1/6), and let P(x)=x(x−1)(x−2), U(x)=(9x−5x²)/2 and V(x)=(5x²−7x)/2. Every polynomial observable on these atoms is represented in R[x]/(P), after y=U(x) and v=V(x); the three Lagrange idempotents therefore cover the whole finite evaluation algebra rather than just a tested list of degrees. For h=x², setting z=e^(−t) gives unnormalized masses (1/2,z/3,z⁴/6). At t=log 2 their normalized weights are (48,16,1)/65 and coordinate means are (18,31,−13)/65. The unnormalized square form is (3q₀²+2zq₁²+z⁴q₂²)/6, and the initial square form minus this form is (2(1−z)q₁²+(1−z⁴)q₂²)/6, nonnegative for t≥0. More generally h_t=(x+t)² gives masses proportional to w_j exp(−j²t−jt²−t³/3); direct differentiation yields dL_t(q)/dt=−L_t(h_tq)+L_t(h_t)L_t(q) for every observable on these three atoms. The common t³/3 factor cancels on normalization. This supplies an actual finite-law path despite the undamped ambient coordinates, not the unreceived infinite-dimensional preservation theorem or a newly executed symbolic check. [AFTER1634-F25-084](../research/t20-v6-20261012/sources/4e2b0cf75cd6011935334995b2aa1a83acf5a1bb21811c511880ad7a33638d8b/check_controls.py#L18-L96)

The flat construction with $`b=1-\varepsilon e^{-1/t}`$ also works algebraically for $`h=x`$ on the line, but its negative $`L_t(x^2)`$ excludes square positivity. Such a solution is not a counterexample to Theorem 13 or Corollary 14. This section incorporates [the corrected signed-energy proof][signed-source]; its [earlier edition][signed-earlier-source] and [independent reviews][signed-review-source] retain their distinct historical evidence boundaries.



<a id="signed-energy-proof-and-evidence-scope"></a>

### 6.4 The theorem and its historical corroboration

The author and preservation guides for signed autonomous energy describe the weighted-energy argument, finite-horizon control and null-ideal consequence already proved in §§6.1–6.3. They supply an additional source-role clarification, not a second origin for those results. In particular, bounded energy gives a global weighting path, while compact joint support supplies the stronger law-uniqueness conclusion; the two assumptions should not be merged. The persistent Gram kernel is an exact algebraic invariant, not a uniform lower bound on positive eigenvalues. [GUIDE105-G004] [GUIDE105-G067]

The guides expressly classify the proof-route check as participating work, rather than independent review of the final artifact. Their exact symbolic controls use neither random sampling nor a finite degree cutoff as a proof of the universal theorem. Their references to a full result, retained inputs and execution reports identify historical dependencies. They do not add a new formal-kernel execution to the ordinary proof displayed here. [GUIDE105-G004] [GUIDE105-G067]


## 7. Time-dependent damping and cumulative control

Instantaneous coercivity is stronger than the dynamics needs. A succession of rank-one dampings may control every direction cumulatively, even though no single instantaneous energy does.

### 7.1 Cumulative SOS coercivity

Let $`h_t`$ be polynomials whose coefficients are continuous in time and whose degrees are bounded on each finite time interval. Assume that on every such interval a continuous scalar $`\beta(t)`$ can be chosen so that
$`g_t=h_t+\beta(t)`$ is SOS. Write
```math
K_{s,t}(x)=\int_s^t g_u(x)\,du,\qquad R(x)=|x|^2.
```
Assume that for each $`t>0`$ there is $`c(t)>0`$ with
```math
K_{0,t}-c(t)R\ \text{SOS}.
\quad\text{(25)}\quad
```
No regularity of the chosen $`c`$, no lower bound proportional to $`t`$, and no coercivity on every subinterval is assumed.

**Theorem 15 (cumulative damping).** Every normalized square-positive coordinatewise $`C^1`$ solution of
```math
L_t'(p)=-L_t(h_tp)+L_t(h_t)L_t(p)
\quad\text{(26)}\quad
```
under these assumptions has the form
```math
L_t(p)=\frac{\int p(x)e^{-H_t(x)}\,d\mu(x)}
             {\int e^{-H_t(x)}\,d\mu(x)},
\qquad H_t=\int_0^t h_u\,du,
\quad\text{(27)}\quad
```
for a unique $`\mu\in\mathcal P_\infty(\mathbb R^d)`$ attached to the complete path. Every positive-time record is determinate. The paths from a fixed valid initial record are in bijection with its representing laws.

**Proof.** Fix a finite horizon and its scalar shift. Put
$`a(t)=\exp(-\int_0^tL_u(g_u)\,du)`$ and $`A_t=a(t)L_t`$.
Then $`A_t'(p)=-A_t(g_tp)`$ and $`0<a(t)\le1`$.

**Finite backward expansion.** Repeatedly integrate
$`A_s(p)=A_t(p)+\int_s^tA_u(pg_u)\,du`$. For every finite $`N`$ this gives
```math
A_s(p)=\sum_{k=0}^{N}\frac{A_t(pK_{s,t}^{\,k})}{k!}+E_{N+1}(s,t;p),
\quad\text{(28)}\quad
```
where
```math
E_m(s,t;p)=
 \int_{s\le u_1\le\cdots\le u_m\le t}
 A_{u_m}\!\left(p\prod_{j=1}^{m}g_{u_j}\right)
 \,du_1\cdots du_m.
```
The remainder functional is evaluated at the **latest** time $`u_m`$. At each finite stage, continuous coefficients and bounded degree justify ordinary finite-dimensional integration. In the terminal terms the polynomial factors commute, so integration over the ordered simplex is $`1/k!`$ times integration over the cube, producing $`K_{s,t}^k`$. No convergent infinite operator expansion has been assumed.

For $`p=q^2`$, the remainder is nonnegative, since products of SOS polynomials are SOS. Let $`c=c(t)`$. Because $`K_{0,t}-cR`$ is SOS,
$`K_{0,t}^n-c^nR^n`$ is SOS by the difference-of-powers factorization. Hence
```math
\sum_{n=0}^{N}\frac{c^n}{n!}A_t(q^2R^n)\le A_0(q^2).
\quad\text{(29)}\quad
```
The coordinate moments obey
$`L_t(x_i^{2n})\le n!/[a(t)c^n]`$.
The multivariate Carleman existence and uniqueness theorem therefore supplies a unique positive-time probability $`\rho_t`$. Let $`\nu_t=a(t)\rho_t`$. Taking the **whole partial sum** in (29) and then using monotone convergence gives the endpoint estimate
```math
\int q^2e^{cR}\,d\nu_t\le A_0(q^2).
\quad\text{(30)}\quad
```
Using only the separate factorial bounds would prove this at smaller rates, not automatically at the endpoint $`c`$.

**From polynomial coordinates to a weak measure equation.** On an interior interval $`[\eta,H]`$, each $`A_t(q^2R^n)`$ is nonincreasing, because its derivative is the negative of an SOS evaluation. Thus the same Gaussian bound with $`c=c(\eta)`$ holds uniformly throughout that interval.

For $`\xi\in\mathbb R^d`$, approximate $`e^{i\xi\cdot x}`$ by its Taylor polynomial of degree $`N`$. With $`k=N+1`$, its integrated remainder is at most
```math
\frac{|\xi|^k\sqrt{k!}}{k!\,c^{k/2}}.
```
If $`|g_t(x)|\le B(1+|x|^D)`$ uniformly on this interval, the derivative remainder is at most
```math
\frac{B|\xi|^k}{k!}
\left(\frac{\sqrt{k!}}{c^{k/2}}
      +\frac{\sqrt{(k+D)!}}{c^{(k+D)/2}}\right).
\quad\text{(31)}\quad
```
Both tend to zero uniformly for $`t`$ and for $`\xi`$ in a compact set. For the last term, the ratio is
$`|\xi|\sqrt{k+D+1}/(\sqrt c\,(k+1))\to0`$.
Taking limits in the differentiated polynomial identities gives
```math
\frac{d}{dt}\int e^{i\xi\cdot x}\,d\nu_t
 =-\int g_t(x)e^{i\xi\cdot x}\,d\nu_t.
```
The Fourier transforms are jointly continuous. Fourier inversion now yields
$`\frac d{dt}\int\phi\,d\nu_t=-\int g_t\phi\,d\nu_t`$ for $`\phi\in C_c^\infty`$. The exchange with the Fourier integral uses the frequency-independent bounds $`\nu_t(1)\le1`$ and $`|\int g_te^{i\xi\cdot x}d\nu_t|\le A_t(g_t)`$, which are locally bounded. It does not integrate the growing estimate (31) over all frequencies.

For a time-varying test $`\psi_t`$ with common compact support, continuous time derivative, and with both $`\psi_t`$ and $`\partial_t\psi_t`$ smooth in space, the difference quotient gives
```math
\frac d{dt}\int\psi_t\,d\nu_t
 =\int(\partial_t\psi_t-g_t\psi_t)\,d\nu_t.
```
Choose $`\psi_u=\phi e^{K_{s,u}}`$. Its derivative cancels the energy term, giving
```math
\nu_s=e^{K_{s,t}}\nu_t,\qquad 0\lt{}s\lt{}t\lt{}T.
\quad\text{(32)}\quad
```
Initially this is equality against compactly supported tests. Both sides are locally finite positive measures, so exhaustion by compact sets makes it a global equality and proves finiteness of the right side.

**Recovery of the boundary law.** Let $`s\downarrow0`$ in (32). Since $`g_u\ge0`$, the weights increase to $`e^{K_{0,t}}`$. Monotone convergence for $`q^2`$ and continuity of $`A_s(q^2)`$ give
$`\mu=e^{K_{0,t}}\nu_t`$ with $`\mu(1)=1`$ and every polynomial square moment. Polarization recovers all coordinates. Undoing the scalar shift gives (27). Positive-time determinacy and inverse weighting make this $`\mu`$ unique for the whole path.

Conversely, $`e^{-H_t}\le\exp(\int_0^t|\beta(u)|du)`$ on each finite horizon. Polynomial domination and the local degree bound justify (26) for every initial law with all moments, including the boundary derivative. This proves the stated bijection. ∎

Only the supplied schedule is classified. A global extension follows when an appropriate schedule is supplied globally; the theorem does not choose future controls.

A related elementary point explains integration of SOS polynomials without selecting time-dependent square factors. In a fixed degree bound, write an SOS polynomial as $`z_m^{\mathsf T}Qz_m`$ with $`Q\ge0`$ and $`z_m`$ the monomials through degree $`m`$. The matrix
$`B=\int_{|x|\le1}z_mz_m^{\mathsf T}\,dx`$ is positive definite. Coefficient convergence bounds $`\mathrm{tr}(QB)`$, hence bounds $`Q`$. A convergent subsequence of these Gram matrices has a positive semidefinite limit. The SOS cone of bounded degree is therefore closed. Riemann sums and closure show that an integral of continuous bounded-degree SOS polynomials is SOS. Neither this fact nor Theorem 15 requires continuous choices of their individual square factors.

A two-atom moving example explains why the autonomous even-derivative argument cannot simply replace the time-ordered proof. On 0≤t≤1/5 set g_t(x)=(x−t)²+1/25 and U_t(x)=tx²−t²x+t³/3+t/25. Then ∂_tU_t=g_t and g_t−x²/2=(x−2t)²/2+1/25−t²≥0. Starting with equal mass at −1 and 0, define Z(t)=[exp(−U_t(−1))+exp(−U_t(0))]/2. This is an actual positive finite-law normalizer, and Z″ is the positive exponential weighted sum of g_t²−∂_tg_t. At t=1/10 those two coefficients are −51/80 and −79/400, so Z″<0 despite the uniform quadratic lower bound on g_t. The normalized atom-weight ratio exp(−t−t²) also genuinely changes. This does not contradict cumulative SOS coercivity: the additional time derivative is precisely what prevents importing the autonomous derivative-sign identity. The source requests these exact checks alongside Volterra and Fourier identities; no execution or new general reconstruction theorem is asserted. [G24–25-136](../research/t20-v6-20261012/sources/151cbf2ad4426a7688e53a44d3fb6e74273259bd3e388c4276dbad59cdb906b8/check_controls.py#L15-L45)

### 7.2 Rank-one rates with full cumulative control

For $`g_t(x,y)=(x+ty)^2`$,
```math
K_{0,t}=tx^2+t^2xy+\frac{t^3}{3}y^2.
```
Its matrix has determinant $`t^4/12`$ and trace $`t+t^3/3`$, so it is positive definite for every $`t>0`$. A completely explicit SOS certificate is
```math
c(t)=\frac{t^3}{4(t^2+3)},\qquad
a(t)=\frac{3t(t^2+4)}{4(t^2+3)},
```
```math
K_{0,t}-c(t)(x^2+y^2)
 =a(t)\left(x+\frac{2t(t^2+3)}{3(t^2+4)}y\right)^2
  +\frac{t^5}{12(t^2+3)(t^2+4)}y^2.
\quad\text{(33)}\quad
```
At each instant the energy vanishes along $`\lambda(-t,1)`$, so no scalar shift can make it dominate a positive radial quadratic there. Moreover $`c(t)`$ is of order $`t^3`$ at zero, not bounded below by a positive multiple of $`t`$. Thus this example lies genuinely beyond instantaneous radial coercivity.

For rotating rank-one energy $`(x\cos t+y\sin t)^2`$, the cumulative eigenvalues are $`(t\pm|\sin t|)/2`$, both positive for $`t>0`$. Control need not continue rotating. If
$`g_t=(x+\min(t,1)y)^2`$, then after time one every later subinterval has only rank-one cumulative energy, while
```math
K_{0,t}-\frac1{16}(x^2+y^2)
 =\frac{15}{16}\left(x+\frac8{15}y\right)^2
   +\frac{y^2}{240}+(t-1)(x+y)^2,\qquad t\ge1.
```
The earlier accumulated control is enough. Finally, the rank of the cumulative energy matrix is not the covariance rank of the law: an initial point mass remains a point mass with zero covariance.

### 7.3 Polynomial coordinate transport

A genuine drift can be included when it arises from a specified polynomial change of coordinates with polynomial inverse. Let $`\Phi_t`$ and $`\Psi_t`$ be inverse polynomial automorphisms, with $`\Phi_0=\mathrm{id}`$, locally bounded degrees and $`C^1`$ coefficients. Put
$`v_t=(\partial_t\Phi_t)\circ\Psi_t`$.
Suppose the pulled-back energy $`k_t=h_t\circ\Phi_t`$ satisfies Theorem 15. A square-positive functional solving
```math
L_t'(p)=L_t(v_t\cdot\nabla p)-L_t(h_tp)+L_t(h_t)L_t(p)
\quad\text{(34)}\quad
```
then has the law
```math
(\Phi_t)_*\left(
 \frac{e^{-\int_0^t k_s\,ds}\mu}
      {\int e^{-\int_0^t k_s\,ds}\,d\mu}
\right).
\quad\text{(35)}\quad
```

Indeed, set $`M_t(q)=L_t(q\circ\Psi_t)`$. The inverse relation gives
$`\partial_t(q\circ\Psi_t)+v_t\cdot\nabla(q\circ\Psi_t)=0`$.
The two transport terms cancel in (34), leaving exactly the hierarchy for $`k_t`$. Polynomial composition preserves square positivity. Apply Theorem 15, then push the resulting law forward. Any competitor with the same current moments pulls back, through the polynomial inverse, to a competitor for the determinate pulled-back law, proving determinacy. Gaussian control belongs to the pulled-back coordinates and need not be an ordinary Gaussian tail in the current coordinates.

For example,
$`\Phi_t(u,z)=(u,z+tu^m)`$ has inverse $`\Psi_t(x,y)=(x,y-tx^m)`$ and drift $`v_t=(0,x^m)`$. Taking
$`h_t(x,y)=[x+t(y-tx^m)]^2`$ gives
$`k_t(u,z)=(u+tz)^2`$, so (33) supplies the required cumulative control. General polynomial vector fields need not have polynomial global flows or polynomial inverses; no such generalization is asserted.

For an affine flow Φ_t(y)=F_t y+d_t generated by a supplied continuous affine velocity, local radial SOS domination transfers explicitly. On a compact time window choose σ>0 and D with |F_t y|≥σ|y| and |d_t|≤D. If h_t+C−c|x|² is SOS with c>0 uniformly there, then h_t(F_t y+d_t)+C+cD²−(cσ²/2)|y|² equals [h_t(F_t y+d_t)+C−c|F_t y+d_t|²]+(c/2)|F_t y+2d_t|²+(c/2)(|F_t y|²−σ²|y|²)+c(D²−|d_t|²). Every term is SOS, including the positive-semidefinite quadratic form and nonnegative constant. This supplies a sufficient affine instance of the pulled-back domination condition, not its automatic preservation by arbitrary polynomial flows. With locally bounded polynomial degree, continuous coefficients and all initial absolute polynomial moments, the source review also justifies the converse differentiation on compact windows. Its sign check distinguishes the weak generator v·∇−h from the density equation ∂tν=−div(vν)−hν: writing instead ∂tν=−v·∇ν+rν requires h=−r−div v. Constant divergence cancels on normalization; spatially varying divergence cannot generally be discarded. Future velocity and killing schedules remain supplied data, and the review’s controls are not new executions here. [AFTER3384-FOURTH25-094](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/0b047139447eda7f2d427d68490c56c01ad159613db8362cca41b93e94e76125/AFFINE_EXTENSION_REVIEW.md#L9-L40) [AFTER3384-FOURTH25-094](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/0b047139447eda7f2d427d68490c56c01ad159613db8362cca41b93e94e76125/AFFINE_EXTENSION_REVIEW.md#L42-L52)

A polynomial inverse can preserve joint determinacy even when an ordinary coordinate Carleman test fails. For an integer m≥3 take Φ_t(u,z)=(u,z+tu^m), Ψ_t(x,y)=(x,y−tx^m) and h_t(x,y)=x²+(y−tx^m)². The pulled-back energy is u²+z² and the drift is (0,x^m). For fixed t>0, the curve y=tx^m gives h_t+C−c(x²+y²)=(1−c)x²−ct²x^(2m)+C→−∞ for every c>0 and finite C, so original-coordinate quadratic domination fails even though h_t is coercive. Start with density π⁻¹exp(−u²−z²). After weighting, U and Z are independent centered Gaussians with variance σ_t²=1/[2(1+t)], and Y=Z+tU^m. Every nonzero term in the expansion of E[Y^(2n)] is nonnegative, hence E[Y^(2n)]≥t^(2n)σ_t^(2mn)(2mn−1)!!. Since (2mn−1)!!≥(mn)!≥(mn/e)^(mn), the Carleman term is at most t⁻¹σ_t^(−m)(e/(mn))^(m/2), whose series converges. The polynomial inverse nevertheless transfers determinacy of the full joint law. This is failure of a sufficient coordinate test, not proof of marginal indeterminacy; neither the estimate nor its constant is uniform as t↓0. The argument is ordinary analysis, with no fresh execution of the reported finite controls. [S30:L65–106](../research/t20-v6-20261012/sources/29f870391139cc1aa7a058a60623a40e2f09f2d1111f5c534f4ad282dd2c7dea/REVIEW.md#L65-L106)

The full argument, its examples, and this transport result incorporate [the cumulative damping proof][cumulative-source]. The [independent review][cumulative-review-source] matters particularly for the smooth time-varying test step: spatial smoothness of the time derivative is included explicitly above.



<a id="moving-objective-continuation-and-order"></a>

### 7.4 Frozen coercivity does not bound moving characteristics

The cumulative-damping theorem concerns a specified multiplication hierarchy; the polynomial-transport extension additionally requires a supplied global polynomial change of coordinates. General moving-gradient characteristics have a separate lifetime question. The escape guides report a smoothly changing, predetermined objective schedule whose frozen losses are coercive, yet whose characteristic escapes in finite time while the actual loss decreases. The stronger nonnegative example uses sum-of-squares frozen losses, has loss tending to zero, and retains positive surviving mass. It preserves the older signed example and the accepted common-energy continuation result. [GUIDE105-G001] [GUIDE105-G018]

There is no contradiction between these statements. Coercivity at each fixed time says that the sublevel sets of that time's loss are bounded. It does not give one compact set containing the relevant sublevels at every time approaching the escape horizon. The center or shape of the controlled region can move. Along a moving objective, a decreasing scalar value therefore does not by itself bound the trajectory in the spatial coordinates.

A fixed coercive Gronwall control would provide a different premise. Suppose a nonnegative coercive $C^1$ function $G$ obeyed, along the characteristics on a finite interval,

```math
\frac{d}{dt}G(x(t))\le a(t)G(x(t))+b(t),
```

with integrable $a,b$ and a finite initial value. Multiplying by $e^{-\int_0^t a}$ and integrating bounds $G(x(t))$ up to that horizon. Coercivity then confines the trajectory to a bounded sublevel. Subject to the usual local continuation hypotheses for the vector field, finite-time escape is impossible. Thus an actual escaping example rules out such a fixed coercive control; testing a finite collection of polynomial candidates would not establish that universal exclusion. This is the ordinary Gronwall reasoning identified in both guides, not a claim that a symbolic search exhausted all $C^1$ functions. [GUIDE105-G001] [GUIDE105-G018]

A constant-rate Gronwall comparison must also distinguish its terminal estimate from a uniform bound over the interval. If H(t)≤H₀e^(Ct) for 0≤t≤T, with H₀≥0 and any finite real C, then sup₀≤t≤T H(t)≤H₀e^(max(C,0)T). Replacing the right-hand side by H₀e^(CT) as a uniform bound is generally false when C<0, since the initial value need not lie below that smaller terminal bound. Assuming C≥0 is another valid repair. The received geometry reconciliation reports exactly this sign correction in its identified escape source, replacing exp(CT)H(2) by exp(max(C,0)T)H(2); it says the counterexample and theorem conclusion survive. This preserves the reported error without attributing it to the general integrating-factor argument above. The underlying escape proof was not reopened or executed here. [AFTER3384-FIFTH25-115](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/research-v6/early_remaining/geometry_review_completion/REPORT.md#L9-L11) [AFTER3384-FIFTH25-115](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/research-v6/early_remaining/geometry_review_completion/REPORT.md#L17-L21)

The guides do not supply their exact schedules or the full characteristic construction. Those remain unreceived proof dependencies. The reported escape consequently must not be redescribed as a newly proved endpoint moment counterexample or a failure of law representation before escape. It also does not refute the common-energy theorem, whose uniform control is precisely what the counterexample lacks. [GUIDE105-G001]

The separate exact-control body specifies the nonnegative moving fixture. Let f(s)=1−5s^5, a(s)=s−s^6 and V_s(x)=(x^4−a(s)x^5)²/2, with s′=−f(s), s(0)=1/2 and x=1/s while 0<s≤1/2. Its identities give x′=−∂_xV_s(x), V_s(1/s)=s²/2 and 27/32≤f≤1, so the schedule reaches its zero boundary within 16/27 while the candidate trajectory escapes and its moving loss tends to zero. Both x=0 and x=1/a(s) are global zeroes, but the orbit is not itself a zero: its distance from the moving zero is s^4/(1−s^5). The endpoint frozen loss is x^8/2 and diverges on that orbit. The integrated killing is bounded between 1/48 and 2/81, preserving positive unnormalized mass. The source also retains the external-work term in the moving energy chain rule; deleting it gives a false identity. Its exact algebra/sign controls do not replace the separate written inverse-schedule regularity and universal Gronwall arguments. [G23-151](../research/t20-v6-20261012/sources/178b01a82090cb6e754a4d0b567304d5e80d6bbb9592aee95f9f9b1d2dedbead/check_independent.py#L12-L65)

The signed moving fixture makes a different boundary explicit with a quartic rather than a nonnegative loss. For s=1−t, 0≤t<1, set V_s(x)=x²/2−(3s+s²)x³/3+s³x⁴/4 and X(t)=s⁻². Direct differentiation gives X′=−∂ₓV_s(X)=2s⁻³ and X(0)=1. Every frozen V_s is coercive, including V₀=x²/2, but V_s(X)=s⁻⁴/6−3s⁻⁵/4 tends to −∞ and has time derivative 2s⁻⁵/3−15s⁻⁶/4<0. The partial time derivative at the orbit is instead 2s⁻⁵/3+s⁻⁶/4>0; subtracting the gradient square 4s⁻⁶ gives the total derivative. Thus decreasing moving energy is compatible with finite-time spatial escape, without deleting the external-work term. Before t=1 the normalized law δ_X has positive-semidefinite rank-one Hankel moment matrix mᵢⱼ=s⁻²⁽ⁱ⁺ʲ⁾ and first moment s⁻²; its endpoint divergence is not a failure of law representation at earlier times. The integrated killing is 19/144+s⁻³/18−3s⁻⁴/16, which tends to −∞, so this signed example must not inherit the preceding nonnegative fixture’s bounded-killing argument. These explicit identities do not constitute a newly executed symbolic check or a universal search excluding every common coercive control. [AFTER1634-N9-207](../research/t20-v6-20261012/sources/5ddfd3e29765a9982388c0333505348f7658d7f132248bc8c86f48c5929acc54/check_exact.py#L14-L60)

Confinement has a separate limit even for a fixed polynomial control. The independent algebra body includes the vector field b(x,y)=(−y,x) with H=1+x²+y². Here b·∇H=0 and H²−(x²+y²)=(x²+y²)²+(x²+y²)+1 is a sum of polynomial squares, so the coercive control bounds every orbit. Its displayed solution is (x cos t−y sin t, x sin t+y cos t); from (1,0) it runs around the unit circle and has no limit. That last conclusion follows directly by comparing times 2πn and (2n+1)π, rather than from a finite symbolic check. Thus this broader polynomial-vector-field example separates a coercive control and nonnegative dissipation from convergence to a stationary point. It is not a counterexample to a theorem requiring the particular negative-gradient field: the rotation is not −∇H. The same source separately checks genuine mobility dissipation for b=−BᵀB∇F as ‖B∇F‖², keeping that stronger structure distinct. Its identities and adversarial controls were not executed here and do not establish a general transport-and-killing existence or convergence theorem. [AFTER1384-S10-184](../research/t20-v6-20261012/sources/3b12d94ac378d2dd7447619e7f4a31342e489bfaa15fe3f65eb39c51ffcfb12c/check_independent.py#L40-L59)

The independent sphere-well control gives a different limitation within genuine negative-gradient dynamics. For F(x)=(|x|²−1)²/4 and R=|x|², the radial equation is R′=2R(1−R), with R(t)=e²ᵗR(0)/[1+(e²ᵗ−1)R(0)]. The origin remains stationary at energy 1/4, although the unit sphere has energy zero. Thus confinement and gradient dissipation do not by themselves imply convergence to a global minimizer. The same control writes the accumulated killing as K(t)=t/4−log H(t)/8−(R(t)−R(0))/8, where H(t)=1+(e²ᵗ−1)R(0); differentiation gives K′=F along the characteristic and K(0)=0. A constant added killing rate multiplies unnormalized mass by its exponential decay factor but cancels from normalized moments. These explicit identities do not establish a general moment-representation, global analytic uniqueness or convergence theorem, and the symbolic requests were not executed.

A finite double-well control shows why endpoint merging must retain exponential accumulated cost. For F(x)=(x²−1)²/4 and x′=x(1−x²), particles at −1 and 1 stay fixed, while the particle starting at 2 follows X(t)=2/√(4−3e^(−2t)) and ends at 1. Its total killing cost is I=(3−log 4)/8>0, obtained by integrating (x²−1)/(4x) from 1 to 2. Starting with equal mass at −1,1,2 and writing a=e^(−I), the final label weights are (1,1,a)/(2+a), so the endpoint mass at 1 is (1+a)/(2+a). Averaging I arithmetically within that endpoint fibre before exponentiation would instead give mass 2√a/(1+2√a). Their positive difference has numerator (1−√a)² over the common positive denominator. The correct fibre factor is (1+a)/2 and its effective cost is −log((1+a)/2), equal to the tilted conditional KL cost plus tilted conditional transient cost. Merging preserves that combined variational quantity, not either term separately. Adding a stationary particle at zero gives a genuinely higher-energy losing basin; the remaining reference masses stay 1/4 rather than being silently renormalized. These are direct consequences of the displayed finite formulas, not a general convergence theorem or a newly executed symbolic check. [AFTER1884-E25-197](../research/t20-v6-20261012/sources/7c5b3c05634f7aaf2fc49ed66544c7d6d26856e489e856a4b4f75629c0d4e712/check_independent.py#L49-L77) [AFTER1884-E25-197](../research/t20-v6-20261012/sources/7c5b3c05634f7aaf2fc49ed66544c7d6d26856e489e856a4b4f75629c0d4e712/check_independent.py#L79-L101)

The separate nonconvex gradient/selection packet reports a broader finite-support endpoint result for positive atomic initial laws and coercive polynomial potentials: convergence to the occupied trajectories' critical endpoints, finite integrated excess energy, surviving label masses, losing exponential prefactors and the merged limiting law. Its winning energy is the least endpoint energy among occupied basins, not a guarantee of finding an unoccupied global minimizer. Its forward extension begins with a supplied Borel law and may retain infinite support; it is not reverse realization of an arbitrary moment hierarchy. Label-weight convergence, convergence of moving physical laws in total variation, and continuity of the limiting selection map remain different questions. The received README does not reproduce the full analytic hypotheses or proof of that extension. Its reported symbolic controls supplement ordinary analysis, including classical Łojasiewicz and related arguments; they establish no basin solver, computable rate, discrete-integrator convergence or kernel theorem here. [AFTER3384-SECOND25-041](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/07418d5bbb5afe7c6dddb25adaea2b323ecda8f67cb40921f72a8800cd79ab51/README.md#L1-L11) [AFTER3384-SECOND25-041](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/07418d5bbb5afe7c6dddb25adaea2b323ecda8f67cb40921f72a8800cd79ab51/README.md#L15-L23)

The same distinction survives an infinite arithmetic conditional cost. In the scalar gradient flow for F(x)=x²/2, start at xₙ=2√(n log 2) with probabilities μₙ=1/[n(n+1)], n≥1. Every particle ends at zero and its accumulated cost is Iₙ=n log 2. Telescoping gives Σμₙ=1, while ΣμₙIₙ diverges. Nevertheless the exponential fibre factor is R=Σμₙ2^(−n)=1−log 2>0, so the effective endpoint cost −log R is finite. Under the tilted probabilities μₙ2^(−n)/R, the mean cost is (log 2)(2 log 2−1)/R, also finite; the log-density identity then gives KL(tilted‖μ)+E_tilted I=−log R. Thus replacing exponential averaging by the arithmetic mean would turn a finite effective cost into infinity even in this explicit quadratic-flow example. The source requests symbolic summation checks of these convergent identities, not a general arbitrary-law limit theorem, and it was not executed. [AFTER1884-E25-197](../research/t20-v6-20261012/sources/7c5b3c05634f7aaf2fc49ed66544c7d6d26856e489e856a4b4f75629c0d4e712/check_independent.py#L103-L121)

The general entropy transport has an exact conditional form once the independently established gradient-limit quantities are supplied: a probability μ, measurable endpoint map q, finite nonnegative transient cost I, selected basin S=q⁻¹(C), and A=∫S e^(−I)dμ>0. Then π*=1S e^(−I)μ/A uniquely minimizes KL(π‖μ)+∫I dπ over π≪μ with π(S)=1. For finite objective, the logarithmic-density identity gives KL(π‖μ)+∫I dπ=KL(π‖π*)−log A; the minimizer is admissible since I e^(−I)≤1/e. With ν=q#μ and r=Eμ[e^(−I)∣q], one has 0<r≤1 ν-almost everywhere and ρ*=q#π*=1C rν/A. Thus the endpoint objective uses J_eff=−log r, has the same unique minimizer ρ* and optimum −log A, and is not obtained by replacing J_eff with Eμ[I∣q]. Conditional Jensen gives J_eff≤Eμ[I∣q], with equality only for conditionally constant I; an infinite conditional arithmetic mean cannot equal the finite effective cost. Conditional expectation is defined almost everywhere, not as an assumed pointwise probability at each null endpoint. This establishes transport of the variational structure; the existence of q and I and the dynamic cumulative-gap identity remain inherited analytic premises, not consequences of entropy algebra or a finite control. [After3634 DISCOVERY 209](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/251d825754c3bcdc7611bf8e133759a87e9b763a1d90d3c3700d64e930b897e5/RESULT.md#L7-L73)

<a id="after3134-tenth25-common-energy-clock"></a>

A common polynomial energy gives a first-order moment estimate even when the transport and killing coefficients are only continuous in time. On a prescribed finite horizon assume common finite polynomial bases, a fixed coercive SOS polynomial H≥1, constants C,D≥0 and κ>0, and SOS certificates CH−b_t·∇H and K_t−κH, where K_t=V_t+D. Let the normalized square-positive full hierarchy satisfy L′_t(p)=L_t(b_t·∇p−V_t p)+L_t(V_t)L_t(p), with every polynomial coordinate C¹ through zero. Set a(t)=exp(−∫₀ᵗL_u(K_u)du), A_t=a(t)L_t and B_n(t)=exp(−Cnt)A_t(H^n). For n≥1 direct differentiation gives B′_n=−n exp(−Cnt)A_t(H^(n−1)(CH−b_t·∇H))−exp(−Cnt)A_t(K_tH^n)≤−κexp(Ct)B_(n+1); the mass equation gives the same inequality for n=0. Every discarded product is SOS, so no evaluation of a merely pointwise nonnegative polynomial is being assumed. In the clock θ(t)=κ∫₀ᵗexp(Cu)du, positivity and repeated integration yield 1≥θ(t)^n B_n(t)/n!, and hence A_t(H^n)≤n!r_C(t)^(−n) for 0<t≤T, with r_C(t)=κ(1−exp(−Ct))/C for C>0 and r_0(t)=κt. No coefficient derivative or smoothly varying SOS decomposition enters. The estimate alone supplies neither a joint representing law nor the compact-test PDE and characteristic identification needed for a reverse lift; those remain separate proof steps in the reviewed successor. Summing this bound justifies subcritical exponential rates, not its endpoint rate by a divergent series. [AFTER3134-TENTH25-242](https://github.com/theislampill/orthemology/blob/345f62310fd4895c26a20acb47ffb6b978667258/research/t20-v6-20261012/sources/04a4223bc4666a986b8c3a3c085913715a4a02ea7adb47b92dfbe5fd764f5930/REVIEW.md?plain=1#L7-L39) [AFTER3134-TENTH25-242](https://github.com/theislampill/orthemology/blob/345f62310fd4895c26a20acb47ffb6b978667258/research/t20-v6-20261012/sources/04a4223bc4666a986b8c3a3c085913715a4a02ea7adb47b92dfbe5fd764f5930/REVIEW.md?plain=1#L57-L65)

<a id="after3134-tenth25-c1-not-c2"></a>

Continuous coefficients genuinely permit less than twice differentiable moment paths. On [0,1] take H=K=1+x², V=K, b_t(x)=|t−1/2|x, C=κ=1 and D=0. The required remainders are K−κH=0 and CH−b_tH′=1+(1−2|t−1/2|)x², both SOS on this horizon. Starting from a nonzero point z, the normalized Dirac path has position x(t)=z exp(g(t)), where g(t)=t/2−t²/2 up to 1/2 and g(t)=t²/2−t/2+1/4 thereafter. The values and first derivatives agree at the join, but x″ jumps by 2z exp(1/8). Every polynomial moment is C¹ and the first moment is not C². This direct calculation prevents a proof from silently differentiating the time coefficients or moment coordinates twice under the preceding contract. It is a finite-horizon regularity discriminator reported in the independent review, not a new symbolic replay or an assertion about arbitrary schedules. [AFTER3134-TENTH25-242](https://github.com/theislampill/orthemology/blob/345f62310fd4895c26a20acb47ffb6b978667258/research/t20-v6-20261012/sources/04a4223bc4666a986b8c3a3c085913715a4a02ea7adb47b92dfbe5fd764f5930/REVIEW.md?plain=1#L79-L88)

### 7.5 Ordered transport differs from pure reweighting

The order neutrality in (5) and (27) comes from multiplication of scalar weights. A moving transport operator changes where those weights act. The moving-objective guide reports, for its specified transport-and-selection operators, compact initial support and sufficiently short common times, that the first order-sensitive term is a transport commutator. The direct killing contribution cancels at that order. This does not make all reaction effects vanish at higher orders. [GUIDE105-G057]

The ordered-control continuation makes the distinction between formal and actual expansions explicit. Formal finite operator jets have identity constant term; its projective separation ranges over all finitely supported laws and polynomial outputs. Actual finite-order asymptotics require a fixed finite control, compact initial support and a common compact set containing the relevant characteristics. The reported quadratic protocols have positive durations and are forward complete, but this does not establish convergence of an unrestricted infinite operator series. Nor does projective separation mean that every different raw control word has a different action. [GUIDE105-G059]

The exact operators and universal separation proof are not contained in these guides. Their scoped claims refine the operation contract without supplying empirical meanings for the objectives or a global classification of all schedules. Their classical operator-series ancestry remains source-owned. The preservation record distinguishes mathematical controls from hash and count checks, and distinguishes excluded full-paper byte checks from unchanged mathematical identities. None of those accounting facts supplies renewed paper reading or an additional independent proof. [GUIDE105-G057] [GUIDE105-G059]

The independent moving-order controls supply the explicit operator B_Fp=−∇F·∇p−Fp. Their three-coordinate expansion gives [B_F,B_G]p=(Hess(G)∇F−Hess(F)∇G)·∇p, so this commutator annihilates 1; independent drift and killing fields do not in general share that scalar cancellation. In the shifted-quadratic fixture F(x)=x²/2 and G(x)=(x−a)²/2, write q=e^(−t). The physical F-then-G endpoint minus G-then-F endpoint is a(1−q)². With a=1 and initial law (δ_0+2δ_2)/3, the exact control expressions put the normalized x²-observable difference at (8/3)t²+O(t³), while the difference of the second label's weights first returns as −(4/9)t³+O(t⁴). Thus second-order cancellation of direct killing is not all-order reaction neutrality. These are specified exact algebraic controls alongside a separate author replay, hash and seven-control count audit; reading them supplies no replay result or proof for unrestricted schedules. [G23-126](../research/t20-v6-20261012/sources/13d29866361ee843a7b161accdc7b3de42bd4e315a708e30c91e9efea05aced1/check_independent.py#L29-L101)

The independent moving-order review also supplies the analytic bridge behind that second-order comparison. For physical F followed by G, L_G(t)L_F(t) on measures is dual to T_F(t)T_G(t) on observables, fixing the sign. The product rule in every finite dimension cancels the second-derivative and scalar terms and gives [B_F,B_G]p=(Hess(G)∇F−Hess(F)∇G)·∇p. With polynomial objectives and observable and compact initial support, a sufficiently small common time keeps both-stage characteristics in one compact neighborhood; smooth ODE dependence bounds third derivatives there and yields a uniform O(t³) remainder, which may be integrated. Linearity and homogeneity make intermediate normalization cancel exactly. Since the commutator annihilates 1, the two unnormalized masses first differ only at O(t³), so division preserves the displayed t² coefficient without a missing mean-subtraction term. This is a local observable expansion for supplied compactly supported laws, not a total-variation derivative of moving Dirac laws, arbitrary-law estimate, all-order reaction cancellation or global commutation theorem. The review's reported controls were not rerun. [AFTER3384-SECOND25-049](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/07dedeae7b12f2e9e9012fabed9acb0ba1ceb8df6c900da163255c93ea94631c/REVIEW.md#L17-L63)

The ordered-control body supplies a distinct cubic comparison for symmetric protocols. For the free-word jets P=e^(tA/2)e^(tB)e^(tA/2) and Q=e^(tB/2)e^(tA)e^(tB/2), all terms through degree two agree and the cubic difference is −[A+B,[A,B]]/8. Substituting B_Fp=−xp′−x²p/2 and B_Gp=−(x−a)p′−(x−a)²p/2 gives the cubic operator Dp=−ap′/4+(a²/8−ax/4)p. Normalization therefore retains μ(Dp)−μ(p)μ(D1), not μ(Dp) alone. For the mean observable of a finitely supported probability law the cubic difference is −a(1+Var_μ X)/4: it is −a/4 on a Dirac law and −a/2 on the equal mixture at −1 and 1. The exact stage formulas separately give endpoint difference a(q−1)³(q+1) and logweight difference a(2x−a)(q−1)³(q+1)(q⁴+1)/4, with q=e^(−t/2). Thus direct killing cancellation at the first commutator does not remove the nonconstant mass term at this nested order. These are the displayed finite algebra and quadratic-flow expressions, not a newly executed symbolic result or a convergence theorem for an unrestricted operator series. [AFTER1634-S6-144](../research/t20-v6-20261012/sources/56bf57b8f5b79915b10840a0dc41f30a231d1a08a994c60891e983521050e294/check.py#L13-L38) [AFTER1634-S6-144](../research/t20-v6-20261012/sources/56bf57b8f5b79915b10840a0dc41f30a231d1a08a994c60891e983521050e294/check.py#L45-L102)

A separate three-coordinate control makes the normalized Lie convention explicit. With L=(u,v,1−u−v) and arbitrary real 3×3 operators B,C, let V_A be the first two coordinates of LA−(LA1)L. The requested symbolic identity is DV_C·V_B−DV_B·V_C=V_(BC−CB). The identity matrix gives the zero field, whereas diag(1,2,3) gives a nonzero field, so coordinate-dependent diagonal multiplication is not automatically a common normalization gauge. Nor can the scalar identity be killed by a nontrivial unital associative quotient: an ideal containing I contains B=IB for every B. These finite-dimensional algebraic controls support the distinction between normalized Lie behavior and associative multiplication; they do not prove an all-dimensional projective-separation classification, positivity preservation, realizability or global flow existence, and no execution is claimed. [AFTER1634-S6-148](../research/t20-v6-20261012/sources/572d85442af4e6c42a718aaf0feb565a3340dc61c7aff72d6648eebecfbdd8b6/check.py#L1-L16)

The independent ordered-control source distinguishes a linear lift from an algebra embedding. For B_Hp=−H′p′−Hp, the vector field −H′∂x−Hz∂z applied to z p gives z B_Hp, but p↦z p is not multiplicative: (z p)(z q)=z²pq rather than z pq. Likewise, testing normalized invisibility only on Dirac laws is insufficient. Multiplication D=M_x has μ(Dp)−μ(p)μ(D1)=0 on every Dirac law, yet on μ=(δ_−1+δ_1)/2 and p=x this quantity is 1. Thus the all-finitely-supported-law qualification in the separation claim cannot be replaced by testing points alone. The same body specifies an order-four noncommuting formal-jet control in which a common scalar factor changes unnormalized mass and cancels from normalized cross-products. These finite identities supplement the already displayed cubic protocol calculation; they supply neither an executed symbolic verification nor an unrestricted infinite-series or global-flow result. [AFTER1884-Q25-092](../research/t20-v6-20261012/sources/7081c6125c2774b9b62ff0ade370e0387efc63f23669ea661ce0f5425c64c5dd/independent_checks.py#L68-L186)


## 8. A fixed controlled subspace and hidden coordinates

Write the state as $`(z,y)\in\mathbb R^r\times\mathbb R^k`$, with $`r\ge1`$. Suppose the SOS energies $`g_t(z)`$ depend only on the controlled coordinates, and
```math
K_t(z)=\int_0^t g_u(z)\,du,\qquad
K_t-c(t)|z|^2\ \text{SOS},\quad c(t)>0\ (t>0).
\quad\text{(36)}\quad
```
The full functional still acts on **all** polynomials in $`z`$ and $`y`$, and is assumed square-positive on that entire algebra. The schedule has the same coefficient continuity and local degree bounds as in §7. An admissible scalar shift may be made as before.

Partial control does not justify asserting joint existence first and disintegrating afterward. The following construction instead extracts the parts that can be represented without that assertion.

### 8.1 Canonical signed measures on the controlled space

**Lemma 16 (controlled projections).** For every such square-positive hierarchy and every hidden polynomial $`b(y)`$, there is a canonical finite signed measure $`\sigma_{t,b}`$ on $`\mathbb R^r`$ at each positive time, with
```math
\int f(z)\,d\sigma_{t,b}(z)=A_t(f(z)b(y))
\quad\text{for every polynomial }f.
\quad\text{(37)}\quad
```
For hidden squares these measures are positive. On every compact interior interval they have uniform Gaussian absolute-moment bounds and satisfy
```math
\sigma_{u,b}=e^{K_s-K_u}\sigma_{s,b}
\quad(s,u>0).
\quad\text{(38)}\quad
```

**Proof.** The same finite Volterra expansion as (28) gives
$`\sum_{n=0}^N c(t)^n A_t(b(y)^2|z|^{2n})/n!\le A_0(b^2)`$.
The controlled functional $`f\mapsto A_t(f(z)b(y)^2)`$ is square-positive. If its mass is zero it is identically zero by Cauchy–Schwarz. Otherwise normalization and the factorial bounds give Carleman in all $`r`$ controlled coordinates, so there is a unique positive representative $`\tau_t^b`$, with
$`\int e^{c(t)|z|^2}\,d\tau_t^b\le A_0(b^2)`$.

For an arbitrary hidden polynomial $`b`$, define
```math
\sigma_{t,b}=\frac{\tau_t^{\,b+1}-\tau_t^{\,b-1}}4.
```
It has the moments (37), and
```math
\int e^{c(t)|z|^2}\,d|\sigma_{t,b}|
 \le M_b,\qquad M_b=\frac{A_0(b^2)+1}{2}.
\quad\text{(39)}\quad
```
A finite signed measure with a Gaussian absolute moment is determined by its polynomial moments. Indeed, its Fourier transform has an everywhere convergent Taylor expansion, using the same factorial estimates as in (31). Thus polarization gives a unique signed measure, is linear in $`b`$, and agrees with the positive representative when $`b`$ is a square.

For $`t\ge\eta>0`$, the mixed square bounds at $`\eta`$ propagate because $`A_t(b^2|z|^{2n})`$ is nonincreasing. Hence (39) holds uniformly with $`c=c(\eta)`$. Apply the Fourier argument of Theorem 15 in the $`z`$ variables alone to $`A_t(f(z)b(y))`$. With $`|g_t(z)|\le B(1+|z|^D)`$, the integrated derivative remainders are bounded by $`M_b`$ times the expression in (31), and the Fourier derivative itself has the frequency-independent bound
$`BM_b(1+\sqrt{D!}\,c^{-D/2})`$.
Consequently
$`\partial_t\sigma_{t,b}=-g_t\sigma_{t,b}`$ against compact smooth tests. Compactly supported integrating factors give (38) locally as signed measures. Equality on a compact exhaustion identifies the full signed measures; their finite total variations, rather than an unproved exchange of an unbounded weight with an integral, supply the global conclusion. ∎

This proof does not choose any family of joint measures. The scalar projections are canonically fixed by the mixed moment record.

### 8.2 One positive-time law is enough, and when it is automatic

**Theorem 17 (persistence and the one-hidden-coordinate threshold).** Under (36), if the full joint record has a representative at one positive time, then the entire path is the record of
```math
\rho_t=\frac{e^{-K_t(z)}\mu(dz,dy)}
                 {\int e^{-K_t(z)}\,d\mu}
\quad\text{(40)}\quad
```
for some $`\mu\in\mathcal P_\infty(\mathbb R^{r+k})`$. Every representative at that time gives exactly one such lift. Positive-time joint representability is therefore an all-or-none property along the path.

For $`k=0`$, representation is automatic and unique at every positive time. For $`k=1`$, representation is automatic, but it may not be unique. For $`k\ge2`$, the one-positive-time representation hypothesis cannot be dropped.

**Proof.** Suppose $`\rho_s`$ represents $`L_s`$ and put $`\nu_s=a(s)\rho_s`$. Its controlled projection weighted by any hidden polynomial is the canonical $`\sigma_{s,b}`$: the Gaussian bounds follow from the full partial-sum estimate, and signed uniqueness identifies it. Define the positive measure
$`\nu_u=e^{K_s-K_u}\nu_s`$ for any $`u>0`$.

Its mass is finite and equals $`A_u(1)`$ by (38) with $`b=1`$. For each hidden even monomial $`y^{2\alpha}`$, positivity and (38) identify its controlled projection with $`\sigma_{u,y^{2\alpha}}`$. Monotone integration of $`|z|^{2m}`$ against this positive measure gives finite mixed even moments. Cauchy–Schwarz therefore gives every absolute mixed polynomial moment. Only after that integrability is established may signed mixed moments be transported; (38) then gives all coordinates $`A_u`$.

As $`u\downarrow0`$, the positive weights increase to $`e^{K_s}`$. Monotone convergence for polynomial squares and continuity of the corresponding coordinates give
$`\mu=e^{K_s}\nu_s`$, with mass one and all moments. This proves (40) and its inverse correspondence.

For $`k=0`$, Theorem 15 applies. For $`k=1`$, the full positive functional has Carleman bounds in $`r=d-1`$ coordinates. The multivariate Carleman existence theorem therefore supplies a joint measure; it does not promise determinacy in the remaining coordinate. This proves automatic existence in that case. The counterexamples in §9 prove the final assertion for $`k\ge2`$. ∎

With no controlled coordinates and exactly one hidden coordinate, a purely scalar-time energy gives a stationary Hamburger moment problem: existence follows from positivity, while uniqueness can still fail. This degenerate case is not a radial-control theorem.

There is a distinct direct proof for quadratic controlled energies that is useful to retain. Suppose $`g_t(z)=z^{\mathsf T}Q_tz`$ with $`Q_t\ge0`$ and continuous. On an interior compact interval choose $`C`$ with $`g_t\le C|z|^2`$ in the SOS order and write $`B=C|z|^2`$. The identity
```math
B^m-\prod_{j=1}^{m}g_{u_j}
 =\sum_{i=1}^{m}B^{m-i}(B-g_{u_i})
        \prod_{j\lt i}g_{u_j}
```
is SOS. Uniform Gaussian factorial bounds therefore imply
```math
A_v\!\left(q^2\prod_{j=1}^{m}g_{u_j}\right)
 \le m!(C/c)^m A_0(q^2).
```
The backward Volterra remainder has functional time $`u_m`$, as in (28). The analogous forward, alternating expansion has functional time $`u_1`$, the **earliest** time. The simplex volume makes both remainders at most
$`A_0(q^2)(C|t-s|/c)^m`$.
For $`C|t-s|<c`$, they tend to zero. Monotone convergence in the backward expansion and domination by $`q^2e^{K_{s,t}}`$ in the forward expansion give both exponential transport identities for any endpoint representative. Patching finitely many such intervals and then taking the boundary limit proves the lift without assuming joint determinacy.

This argument explains why both time directions are needed when representatives are nonunique. It is also specifically quadratic: an energy such as $`g_t(z)=z^4+t^2z^2`$ has cumulative energy $`tz^4+t^3z^2/3`$, but cannot be bounded by $`Cz^2`$. Lemmas 16–17 cover it through the Fourier projection argument, without importing that false quadratic bound. They reconcile [the original partial-control theorem][partial-control-source], [the general SOS extension][partial-sos-source], and [the arbitrary-hidden persistence theorem][hidden-persistence-source].

### 8.3 Exact information retained by fixed-subspace operations

For an actual initial law define the finite signed measures
```math
m_{\mu,\alpha}
  =(\pi_z)_*(y^\alpha\mu),
\qquad \alpha\in\mathbb N^k.
\quad\text{(41)}\quad
```
They record the controlled distribution and all hidden polynomial averages conditional on the controlled variable, in an integrated form.

**Proposition 18 (fixed-subspace continuation equivalence).** Two initial laws with all moments have the same full positive-time moment record under one schedule satisfying (36) if and only if
$`m_{\mu,\alpha}=m_{\nu,\alpha}`$ for every $`\alpha`$. This condition is also equivalent to equality of their full paths under every such schedule acting on the same controlled subspace. It identifies their moment continuation, not necessarily their joint laws.

**Proof.** At positive time the signed controlled measures weighted by $`y^\alpha`$ have a Gaussian absolute moment. Equality of all mixed moments identifies these signed measures by Fourier uniqueness. For normalized laws this says
$`Z_\mu^{-1}e^{-K_t}m_{\mu,\alpha}=Z_\nu^{-1}e^{-K_t}m_{\nu,\alpha}`$.
Invert the positive weight on these already known finite measures. For $`\alpha=0`$, integration over the controlled space gives $`1/Z_\mu=1/Z_\nu`$, since both initial laws are probabilities. This removes the scalar factor for every $`\alpha`$ and proves (41). Conversely, (41) gives every damped mixed moment and normalizer directly for any allowed controlled schedule. ∎

Thus a complete path has a unique joint lift exactly when its record is determinate at one positive time. An extension along the same supplied controlled space is unique as a **moment path**: every such extension contains the old positive-time representative and must obey the same canonical signed-projection transport. It need not identify the original joint law.

A useful sufficient condition for joint identification is determinacy of the hidden conditional law for almost every controlled value. Equality of (41) gives equal controlled marginals and, outside one common null set for the countable hidden monomials, equal conditional hidden moments. Conditional determinacy then identifies the conditional laws. No necessity statement is inferred from this argument.

An indeterminate hidden marginal does not prevent conditional identification. Let $`Z`$ be Gaussian and let $`Y=e^Z`$. Its lognormal marginal is indeterminate, but the conditional law of $`Y`$ given $`Z=z`$ is the point mass at $`e^z`$. The measures $`m_0=\gamma`$, $`m_1=e^z\gamma`$, and $`m_2=e^{2z}\gamma`$ already force the relation: any compatible joint law satisfies
$`\int(y-e^z)^2=0`$.
The nonpolynomial cross integral is legitimate because the specified conditional signed measure gives $`\int ye^z=\int e^{2z}d\gamma`$, with finiteness supplied by Cauchy–Schwarz. Under $`g_t=(1+t)z^2`$, the conditional graph persists while the hidden marginal remains a nondegenerate lognormal.

Conversely, full-support ambiguity is possible. Let $`\eta_\pm=(\mu_\pm+\gamma_1)/2`$, where (8) is embedded on the real line and $`\gamma_1`$ is a standard Gaussian. Then $`\gamma_r\otimes\eta_\pm`$ are distinct full-support joint laws with all the same mixed moments, and every fixed-subspace controlled schedule leaves their hidden factors untouched. Rank-one controlled matrices at different times may fail to commute as matrices; the scalar polynomials in the weighting factors still commute. These are different algebraic questions.

### 8.4 Enlarging the allowed operations can reveal hidden distinctions

The preceding equivalence depends on the declared controlled subspace. At a positive time $`s`$, the last example has the form
$`\zeta_s\otimes\eta_\pm`$, with a Gaussian exponential moment in the controlled variables. Activate the previously hidden coordinate by applying $`e^{-\varepsilon y^2}`$, $`\varepsilon>0`$. The resulting laws remain distinct: equal normalized hidden factors would, after inverse multiplication by $`e^{\varepsilon y^2}`$ and normalization, identify $`\eta_+`$ and $`\eta_-`$.

The new joint laws have a Gaussian exponential moment in every coordinate. They are therefore moment-determinate, so distinctness now implies a difference in at least one finite polynomial moment. This proves existence of a finite distinguishing record, not a uniform degree or a practical discovery algorithm. It does not contradict Proposition 18, because activating $`y`$ changes the admitted operation family. The complete activation argument is incorporated from [the public activation proof][activation-source].



## 9. Sharp failure with two hidden coordinates

The distinction between squares and all nonnegative polynomials is essential, not an artifact of a truncated matrix calculation. We first construct a functional on the **whole** polynomial algebra, then place it inside the dynamics.

A separate degree-scoped certificate isolates a finite version of the positivity distinction in three variables. Parameterizing every polynomial of degree at most two as a quadratic, the written moment-form argument gives Lambda(p²)>0 for each nonzero such p. Its Choi-Lam witness has degree at most four, is nonnegative at every real point, and has Lambda value −2. Consequently no functional positive on all nonnegative quartics can agree with these data through degree four. This is a truncated-degree obstruction and does not establish strict square positivity on the whole algebra or construct an extension of the finite data. The coefficient, parameterization and scalar-nonnegativity interfaces remain imported, and the requested axiom prints are not received verification. [AFTER750-F50-238](../research/t20-v6-20261012/sources/dbbcd76b73bc428023b113e8a047359576c5abd822f9219ab179d1275476645a/Certificate.lean#L8-L100)

The supplementary heat control evolves that same finite-degree obstruction without constructing an all-degree functional. Define Tₜp=Σₖ tᵏΔᵏp/k! on polynomials and f=1−4xyz+x²y²+x²z²+y²z². Its finite sum gives Tₜf=f+4t(x²+y²+z²)+12t², and at t=1/9 the displayed decomposition is 31/27+(xy−2z/3)²+(xz−2y/3)²+(yz−2x/3)². Adding 4(t−1/9)(x²+y²+z²)+12(t²−1/81) gives an SOS for t≥1/9. Under fₐ(x,y,z)=f(ax,ay,az), a≠0, the scaling relation Tₜfₐ=(T_{a²t}f)(ax,ay,az) provides the corresponding displayed SOS at 1/(9a²). This is a sufficient entry time; the body supplies no lower-bound proof making it minimal, so its divergence as a→0 alone proves no absence of an earlier uniform entry time. For the already specified degree-four L, the same formula gives L(Tₜf)=−2+48t+12t², hence −3797/2500 at t=1/100. The strictly negative value still precludes a positive representing measure for that heat-transformed finite record. The program’s sample square-heat identities, matrix checks and inverse-heat tests were not executed and do not establish infinite-dimensional positivity, functional existence or an all-degree extension. [AFTER1634-F5-113](../research/t20-v6-20261012/sources/52e487b8946ece4e8d08bb9882ab978e33498a796c73a56ac55f300f9624a45e/check_controls.py#L28-L93) [AFTER1634-F5-113](../research/t20-v6-20261012/sources/52e487b8946ece4e8d08bb9882ab978e33498a796c73a56ac55f300f9624a45e/check_controls.py#L126-L168)

The separate truncated review supplies the missing uniform-window counterexample by scaling the functional and the witness together, not merely by observing a sufficient SOS entry time. On polynomials of degree at most four in three variables, set Λ(1)=1, Λ(x_i²)=4, Λ(x_i⁴)=50, Λ(x_i²x_j²)=1 for i≠j, Λ(xyz)=3/2, and every other nonconstant monomial value to zero. Its quadratic moment matrix splits into a block whose Schur complement has eigenvalues 4,49,49 and three blocks ((4,3/2),(3/2,1)); hence it is strictly positive definite. For f=1−4xyz+x²y²+x²z²+y²z²≥0, Λ(H_t f)=−2+48t+12t². Fix any finite T≥0, let S_a p(x)=p(ax), Λ_a=Λ∘S_a and f_a=S_(1/a)f, and choose a>0 with a²≥100T. Heat scaling gives Λ_a(H_T f_a)=−2+48T/a²+12T²/a⁴<0. Yet L=Λ_a∘H_T satisfies L∘H_(−T)=Λ_a, strictly positive on every nonzero square of degree at most four, because dilation preserves the quadratic-polynomial domain and the finite heat exponentials are inverse. Thus every fixed backward-heat window admits a nonmoment truncated L passing that strict-square test. This does not refute a pointwise theorem with polynomial-dependent time, construct an all-degree extension, or evolve an assumed measure backward. The ordinary finite-dimensional argument is distinct from the review's reported symbolic executions, which were not repeated here. [AFTER3384-EIGHTH25-193, lines 5–34](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/122a055dd09e341625a7d65d2ffaacad373f68e28178cddc08f05b8fcb67baee/TRUNCATED_DIAGNOSTIC_REVIEW.md#L5-L34) [AFTER3384-EIGHTH25-193, lines 36–57](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/122a055dd09e341625a7d65d2ffaacad373f68e28178cddc08f05b8fcb67baee/TRUNCATED_DIAGNOSTIC_REVIEW.md#L36-L57) [AFTER3384-EIGHTH25-193, lines 59–63](https://github.com/theislampill/orthemology/blob/3d8d6f6386d676bd14343940edb158a3489169e1/research/t20-v6-20261012/sources/122a055dd09e341625a7d65d2ffaacad373f68e28178cddc08f05b8fcb67baee/TRUNCATED_DIAGNOSTIC_REVIEW.md#L59-L63)

### 9.1 A complete strictly square-positive functional without a measure

**Theorem 19 (an explicit nonmoment functional).** There is a normalized functional $`\Lambda:\mathbb R[u,v]\to\mathbb R`$, with computable dyadic values on every monomial, such that $`\Lambda(p^2)>0`$ for every nonzero polynomial $`p`$, but
```math
F(u,v)=1+u^4v^2+u^2v^4-u^2v^2\ge\frac34,
\qquad \Lambda(F)=-1.
\quad\text{(42)}\quad
```
Consequently $`\Lambda`$ has no positive representing measure.

Keeping an arbitrarily long finite prefix of these moments does not retain strict positivity on every nonzero square. If moments of total degree above N are set to zero, the resulting functional still agrees on every exponent of degree at most N, but sends the square of the nonzero monomial with exponent (N+1,0) to zero. This works for every finite N, whereas the full functional is positive on every nonzero polynomial square without a degree premise. The cutoff argument excludes strict positivity of that particular truncation, not all possible extensions or even nonnegative square positivity; its exponent-code and functional-evaluation equations remain supplied dependencies. [A750-F50-006](../research/t20-v6-20261012/sources/ae91d32c8f068ba757eb1987c3b52d3444059e76695ca181804a4ca016efd0e8/PositiveChecks.lean#L19-L54)

**Proof.** Order the first ten monomial exponents as
```math
(0,0),(2,1),(1,2),(1,1),(1,0),(0,1),
(2,0),(0,2),(3,0),(0,3).
```
For total degree $`a+b\ge4`$, assign index
$`m(a,b)=b+1+(a+b)(a+b+1)/2`$. This orders successive degree blocks, giving a bijection with the positive integers.

If two distinct exponents have an integral midpoint, that midpoint occurs before the later exponent. In degrees at least four, either its total degree is smaller, or its second coordinate lies strictly between the two second coordinates in the same degree block. The exceptional low-degree pairs, stated as index pairs followed by their midpoint index, are
```math
(1,7;5),(1,8;6),(2,6;4),(2,10;3),(3,5;4),
(3,9;2),(5,9;7),(6,10;8),(7,8;4).
```
They exhaust the pairs in the parity classes
$`\{1,7,8\},\{2,6,10\},\{3,5,9\},\{4\}`$.
Thus all required off-diagonal entries below are already defined when their later index is reached.

Set $`j_1=j_2=j_3=1`$, $`j_4=4`$, and $`A_4=\mathrm{diag}(1,1,1,4)`$, with $`B_4=A_4^{-1}`$. For basis exponents $`p_i,p_j`$, the intended entry is zero when their sum has an odd coordinate, and otherwise is $`j_{m((p_i+p_j)/2)}`$. Suppose the first $`n-1`$ diagonal choices and matrices are constructed. Let $`v_n`$ be the already determined off-diagonal column, and put
```math
w_n=B_{n-1}v_n,\quad
q_n=v_n^{\mathsf T}w_n,\quad j_n=1+q_n,
```
```math
A_n=
\begin{pmatrix}
A_{n-1}&v_n\\
v_n^{\mathsf T}&1+q_n
\end{pmatrix},
\qquad
B_n=
\begin{pmatrix}
B_{n-1}+w_nw_n^{\mathsf T}&-w_n\\
-w_n^{\mathsf T}&1
\end{pmatrix}.
\quad\text{(43)}\quad
```
Direct block multiplication proves $`A_nB_n=I`$. The quadratic form identity
```math
(a,t)A_n(a,t)^{\mathsf T}
 =(a+t w_n)^{\mathsf T}A_{n-1}(a+t w_n)+t^2
```
proves strict positive definiteness by induction. The Schur complement is one, so $`\det A_n=4`$. All entries are dyadic and computed by finite rational operations; there is no unbounded search for a positive completion.

The independent ordinary review supplies a second all-stage construction of this same sequence. With the earlier moments fixed and det A_(n−1)=4, midpoint precedence fixes every off-diagonal entry of the next symmetric block C_n(t). Expanding only its new diagonal gives det C_n(t)=det C_n(0)+4t. Hence t=[4−det C_n(0)]/4 is dyadic and forces determinant four using one fixed nonzero divisor. Starting from diag(1,1,1,4), all leading principal determinants are then 1,1,1,4,4,…, so Sylvester’s criterion proves positive definiteness at every stage. For a fixed old block and border there is exactly one such t; the Schur construction also has determinant four, so induction identifies the two sequences at every index, not just a computed prefix. This independent mathematical route is distinct from the review’s finite Bareiss checks and its then scalar-only Lean replay; it neither replaces the full-algebra argument nor narrows the later formalization described below. [AFTER3884-FIRST25-S25, lines 90–102](../research/t20-v6-20261012/sources/2926c2a925563612e152fdd93b6f3bd295bb4a8f9b8f603a0d563011c5e7bd7d/REVIEW.md#L90-L102) [AFTER3884-FIRST25-S25, lines 136–156](../research/t20-v6-20261012/sources/2926c2a925563612e152fdd93b6f3bd295bb4a8f9b8f603a0d563011c5e7bd7d/REVIEW.md#L136-L156)

The FalseSchurNoSlack variant removes the one from the lower-right entry in its completed-square and positivity statements, using vᵀw with Aw=v while retaining a +t² term in the claimed square. The nonzero vector (−w,1) then has quadratic value zero, so that block is not strictly positive definite. Its later inverse theorem separately retains the correct entry 1+vᵀBv and is not refuted by this zero-slack calculation. The current construction’s Schur complement one is therefore substantive; these are exact algebraic distinctions, not newly observed compiler results. [AF750-Q4-178](../research/t20-v6-20261012/sources/ce83b6dee57ee82b4d6d34d4c301bd7d2e19e902057f7f9f06c53a200e8b0b42/FalseSchurNoSlack.lean#L14-L76) [AF750-Q4-178](../research/t20-v6-20261012/sources/ce83b6dee57ee82b4d6d34d4c301bd7d2e19e902057f7f9f06c53a200e8b0b42/FalseSchurNoSlack.lean#L109-L136)

Define $`\Lambda(u^av^b)=0`$ if either exponent is odd, and otherwise define it as $`j_{m(a/2,b/2)}`$. Midpoint precedence makes every finite Gram block agree with the corresponding $`A_n`$. A nonzero polynomial uses a finite number of these basis monomials, so its square has strictly positive evaluation. Also $`\Lambda(1)=1`$ and the four terms of $`F`$ have values $`1,1,1,4`$, giving $`\Lambda(F)=-1`$.

To verify nonnegativity, put $`s=u^2+v^2`$. Then
$`F=1+u^2v^2(s-1)`$. For $`s\ge1`$ this is at least one. For $`s\le1`$, the bounds $`u^2v^2\le s^2/4\le1/4`$ and $`1-s\le1`$ give $`F\ge3/4`$. A positive measure could not integrate it to $`-1`$. ∎

Neither a large finite positive prefix nor setting an uncomputed tail to zero proves this theorem. The recursive diagonal choices need not be monotone; the predecessor computation has $`j_{11}=479723268580926`$ and $`j_{12}=5/4`$. A zero tail after the ten-term prefix can even give a negative square. The full recurrence and the proof that every polynomial lies in a compatible positive block are the essential ingredients.

The seed ordering and positive nonmoment witness belong to the classical construction discussed by [Schmüdgen](#references), *The Moment Problem*, Propositions 13.4–13.5, with attribution there to J. Friedrich. The explicit Schur-complement recurrence is the public constructive treatment incorporated from [the full algebraic proof][nonmoment-source]; this exposition does not claim a new discovery.

The formal status has also advanced beyond an early scalar-only certificate. The received later [formalization result][full-formal-source], its [independent review][full-formal-review-source], and the actual [final Lean declaration][countermodel-lean-source] establish the scope of a construction on $`\mathrm{MvPolynomial}(\mathrm{Fin}\ 2,\mathbb R)`$: a full linear functional, normalization, strict positivity for every nonzero polynomial square, the pointwise witness bound, and its negative evaluation. This is stronger than merely checking the four scalar witness values. The executable dyadic algorithm, determinant identity, and measure-integration contradiction remain distinct ordinary mathematical claims. The present chapter has not rerun that kernel build; its formal sources and verification inputs remain independently necessary.

### 9.2 Strict positivity can persist without any joint law

Apply Theorem 19 in two hidden coordinates and tensor it with Gaussian laws in any additional hidden coordinates. Denote the resulting hidden functional by $`\Lambda_k`$, $`k\ge2`$. Under an arbitrary controlled schedule satisfying (36), define
```math
A_t(p)=\int
 \Lambda_k\!\bigl(p(z,\cdot)\bigr)e^{-K_t(z)}\,d\gamma_r(z),
\qquad
L_t=\frac{A_t}{A_t(1)}.
\quad\text{(44)}\quad
```
Every evaluation is a finite sum of Gaussian polynomial integrals. Dominated differentiation proves the hierarchy. For a nonzero joint polynomial, its hidden polynomial is nonzero on a nonempty open set of the remaining variables; the Gaussian measure gives that set positive mass and the hidden functional is strictly square-positive there. Hence $`L_t(p^2)>0`$ for every nonzero $`p`$. Yet $`L_t(F)=-1`$ for every time, so no joint law exists.

This example is not necessarily stationary. Freeze a time at which the controlled energy is nonconstant. The derivative of its expectation, holding that polynomial fixed while differentiating, is minus its variance under the actual controlled Gaussian tilt, and is strictly negative. One must not include a time derivative of the polynomial itself in this diagnostic. Cumulative radial control ensures that the energy is nonconstant at some time.

This proves the sharpness of the hidden-coordinate count in Theorem 17. It does not yet start from a valid joint record. The following stronger construction does; it incorporates [the full hidden-boundary argument][hidden-boundary-source] rather than treating (44) as the answer to a different question.

### 9.3 A positive measure can dominate a nonmoment functional

The next auxiliary construction explains how an initial genuine law can conceal the nonmoment component.

**Lemma 20 (signed moment realization).** Every real array $`(c_\alpha)_{\alpha\in\mathbb N^k}`$ is the polynomial moment array of a finite signed atomic measure with every absolute polynomial moment. If $`c_0=1`$, it can be written as $`P-N`$, with $`P,N`$ positive, $`P(1)=1+N(1)`$, and $`N(1)\le1/2`$.

**Proof.** Begin with $`c_0\delta_0`$. For a multiindex $`|\alpha|=n\ge1`$ and integer $`R\ge1`$, define
```math
D_{\alpha,R}
 =\frac1{\alpha!\,R^n}
   \sum_{0\le j\le\alpha}
    (-1)^{n-|j|}\binom{\alpha}{j}\delta_{Rj}.
\quad\text{(45)}\quad
```
Repeated finite differences give
$`\int x^\beta\,dD_{\alpha,R}=\delta_{\alpha\beta}`$ whenever $`|\beta|\le n`$. Indeed, a lower total degree has some coordinate below its difference order; at equal degree, the only surviving multiindex is $`\beta=\alpha`$, with value one. For $`m\ge0`$,
```math
\int |x|^m\,d|D_{\alpha,R}|
 \le\frac{2^n n^m}{\alpha!}\,R^{m-n}.
\quad\text{(46)}\quad
```

Suppose degrees below $`n`$ have already been matched. Let $`r_\alpha`$ be the degree-$`n`$ residuals, put
$`B_n=\sum_{|\alpha|=n}|r_\alpha|2^n/\alpha!`$, and choose a strictly increasing integer
$`R_n\ge\max(1,2^n n^{n-1}B_n)`$.
The block $`\rho_n=\sum_{|\alpha|=n}r_\alpha D_{\alpha,R_n}`$ corrects that degree without changing lower degrees. For every $`m<n`$, (46) gives
$`\int|x|^m\,d|\rho_n|\le2^{-n}`$.
Thus the series of blocks converges in total variation, and for each fixed absolute moment its tail is summable. Later blocks have zero contribution to every already fixed moment, so the resulting signed measure has exactly the prescribed array.

When $`c_0=1`$, combine coincident atoms within each finite block before taking its positive and negative parts. Each block has total mass zero; therefore its negative mass is half its total variation and at most $`2^{-n-1}`$. Set
$`P=\delta_0+\sum\rho_n^+`$ and $`N=\sum\rho_n^-`$. This gives the required masses and moments. ∎

Apply the lemma to the functional $`\Lambda`$ in Theorem 19. The positive measure $`P`$ dominates that functional on squares, because $`\Lambda=P-N`$ and $`N`$ is positive. Tensor with Gaussian laws for extra hidden coordinates if needed. Write $`n_0=N(1)`$ and $`C=1+n_0`$, so $`1<C\le3/2`$; the strict inequality follows because $`N=0`$ would make $`\Lambda`$ a positive measure.

### 9.4 Immediate loss of joint representability from a genuine initial law

**Theorem 21 (valid-initial escape).** With at least two hidden coordinates, there are normalized, strictly square-positive, coordinatewise $`C^1`$ hierarchies satisfying (36) (smooth for autonomous energies) whose initial record is represented by a genuine probability with all moments, but which have no representing measure at any positive time. Their initial record is indeterminate. The theorem makes no such assertion for a determinate joint initial record.

**Proof.** On one controlled coordinate, let $`\alpha_1`$ be the continuous standard lognormal law. Define the discrete law
```math
\beta_1=\frac1S\sum_{j\in\mathbb Z}e^{-j^2/2}\delta_{e^j},
\qquad S=\sum_{j\in\mathbb Z}e^{-j^2/2}.
\quad\text{(47)}\quad
```
For every integer $`m\ge0`$, shifting the index in the sum gives
$`\int z^m\,d\beta_1=e^{m^2/2}=\int z^m\,d\alpha_1`$.
Tensor both with the same Gaussian in the other $`r-1`$ controlled coordinates, obtaining $`\alpha,\beta`$. They have equal moments and are mutually singular: for
$`E=\{z:z_1=e^j\text{ for some }j\in\mathbb Z\}`$,
$`\alpha(E)=0`$ and $`\beta(E^c)=0`$.

Use the positive measures $`P_k,N_k`$ from Lemma 20, with $`\Lambda_k=P_k-N_k`$, and put
```math
\alpha_t=e^{-K_t}\alpha,\quad \beta_t=e^{-K_t}\beta,
\qquad
A_t=\frac{\alpha_t\otimes\Lambda_k+\beta_t\otimes N_k}{C},
\qquad L_t=\frac{A_t}{A_t(1)}.
\quad\text{(48)}\quad
```
The expression defines a polynomial functional; it is not asserted to be a positive joint measure. Its mass
$`A_t(1)=(\alpha_t(1)+n_0\beta_t(1))/C`$ is positive. Strict positivity on every nonzero square follows from the first tensor term: the controlled law has positive density on an open half-space, the remaining Gaussian factors are positive on open sets, and $`\Lambda`$ is strictly square-positive. The second term is positive. Finite polynomial expansion and domination by the original all-moment measures justify the hierarchy and all needed derivatives.

At zero, the equal controlled moments make (48) agree on every polynomial with the genuine probability
$`\mu_0=\alpha\otimes(P_k/C)`$.
It also agrees with $`\beta\otimes(P_k/C)`$. Those two laws are distinct, so the initial record is indeterminate.

Fix $`t>0`$. If a positive measure $`\nu`$ represented $`A_t`$, then the controlled exponential moment obtained from its moments would be finite, because $`K_t\ge c|z|^2`$. The measure
$`\sigma=(\pi_z)_*(F\nu)`$ would be positive, since $`F\ge3/4`$. Cauchy–Schwarz with $`F^2`$ gives a Gaussian absolute moment for $`\sigma`$ at a smaller rate. Its polynomial moments, from (48), are those of
```math
w_t=\frac{-\alpha_t+N_k(F)\beta_t}{C}.
\quad\text{(49)}\quad
```
The latter signed measure also has a Gaussian absolute moment. Signed moment uniqueness therefore gives $`\sigma=w_t`$. But
$`w_t(E^c)=-\alpha_t(1)/C<0`$, contradicting positivity. Hence no positive-time representative exists. ∎

The genuine initial law $`\mu_0`$ also has its ordinary tilt, which is a second, realizable hierarchy with the same initial record. For autonomous controlled energy, both paths are smooth and all their initial derivatives agree, because repeated hierarchy differentiation uses only initial polynomial moments. Thus full initial jets do not exclude this escape. The all-or-none statement of Theorem 17 concerns **positive times** and does not turn a valid boundary point into a positive-time representative.

There is also a finite polynomial separator at every positive time. Let $`m_t=\alpha_t+\beta_t`$. Polynomials are dense in $`L^2(m_t)`$: a function orthogonal to them would define a signed measure with a Gaussian absolute moment, by Cauchy–Schwarz, and with all moments zero; Fourier uniqueness makes that measure zero. Choose a nonzero smooth controlled function $`\phi`$ supported in a strip $`1<z_1<e`$. The discrete measure gives it zero mass while the continuous measure gives positive mass. Thus $`\int\phi^2\,dw_t<0`$. Approximate $`\phi`$ in $`L^2(m_t)`$ by polynomials $`q_n`$. The density of $`w_t`$ relative to $`m_t`$ is bounded, and $`q_n^2\to\phi^2`$ in $`L^1(m_t)`$, so some $`q_n`$ satisfies
$`L_t(q_n(z)^2F(y))<0`$ although $`q_n^2F\ge0`$ pointwise. This is an existence proof for a finite separator. Its later effective and explicit refinements appear in §10.

The signed-moment construction and the escape theorem incorporate [the genuine-initial escape proof][valid-initial-escape-source]. The earlier permanently invalid path (44) remains a useful independent control; it is not substituted for this stronger result.

### 9.5 Every fixed finite prefix can remain genuinely valid

**Theorem 22 (finite-prefix validity delay).** Let $`L_t`$ be a normalized polynomial-coordinate path continuous at zero. Suppose $`L_0`$ is an actual all-moment probability functional and $`L_0(q^2)>0`$ for every nonzero polynomial $`q`$. For each total degree $`D`$, there is $`\varepsilon_D>0`$ such that, for $`0\le t<\varepsilon_D`$, the restriction of $`L_t`$ to degree at most $`D`$ is represented by a probability on at most
$`\binom{d+D}{D}`$ atoms. Moreover $`L_t(P)>0`$ for every nonzero globally nonnegative polynomial of degree at most $`D`$.

**Proof.** Let $`V_D`$ be the finite-dimensional coefficient space of those polynomials, and let $`C_D`$ be its closed cone of globally nonnegative polynomials. A nonzero $`P\in C_D`$ has $`L_0(P)>0`$: otherwise positivity of the representing measure would give $`P=0`$ almost surely and thus $`L_0(P^2)=0`$, contrary to strict square positivity. The intersection of $`C_D`$ with the coefficient unit sphere is compact. Hence $`L_0`$ has a positive minimum $`\delta_D`$ there. Coordinate continuity makes the dual norm of $`L_t-L_0`$ less than $`\delta_D/2`$ for sufficiently small $`t`$. This proves strict positivity uniformly on that cone.

Let $`v_D(x)`$ be the vector of monomials through degree $`D`$, and let $`M_D`$ be the conic hull of its evaluation vectors. Its dual cone is exactly $`C_D`$, so finite-dimensional separation gives $`\overline{M_D}=C_D^*`$. The strict margin just obtained places the moment vector of $`L_t`$ in the interior of $`C_D^*`$. This is an ordinary full-dimensional interior: the evaluation vectors span the space, since a polynomial vanishing at every point is zero.

For a full-dimensional convex set, the interior of its closure equals its interior. One direct proof chooses a small simplex around an interior point, approximates its vertices by points of the original convex set, and keeps the point inside the perturbed simplex by continuity of the positive barycentric coordinates. Thus this moment vector belongs to $`M_D`$ itself, not merely to its closure. Conic Carathéodory reduces its representation to at most $`\dim V_D=\binom{d+D}{D}`$ evaluation vectors. The constant coordinate is one, so their nonnegative weights sum to one. ∎

Apply this theorem to (48). At every positive time the complete record is invalid, yet each fixed finite degree remains exactly representable on its own initial interval. The least degree of **any** nonnegative polynomial separator therefore tends to infinity as time approaches zero. This strengthens the corresponding conclusion for separators of the special form $`q^2F`$. The finite representing laws need not be compatible across degrees, have a common support, or extend to a joint representing law. No effective bound on $`\varepsilon_D`$ is claimed.

The theorem also covers odd $`D`$ and $`D=0`$; it does not require the cone of nonnegative polynomials itself to span $`V_D`$. The full finite-prefix proof and its later completed review are incorporated from [the finite-prefix refinement][finite-prefix-source] and [its independent review][finite-prefix-review-source]. An earlier pending-review label does not override that received successor.



<a id="polynomial-obstruction-and-measure-bridge"></a>

### 9.6 A polynomial obstruction and an unbuilt measure bridge

The distinction between polynomial positivity and measure representation also fixes the scope of formal corroboration. The development-intermediates guide explicitly excludes its exploratory files from every successful compiled-module list. Its direct measure-theory bridge stopped at an unavailable import before that file was checked; the reported missing dependency closure was not rebuilt. The unsuccessful lemma probes likewise carry no theorem qualification. [GUIDE105-G079]

The mathematical implication remains straightforward: if a positive Borel measure represented a functional, every everywhere nonnegative integrable polynomial would have nonnegative integral. A negative value on such a polynomial therefore excludes representation. The guide assigns that conclusion to an ordinary corollary of a checked polynomial obstruction, not to a separately checked measure-theory theorem. The full ordinary arguments in §§9.1–9.5 stand on their stated assumptions; this historical failed import neither refutes them nor extends their formal verification scope. [GUIDE105-G079]

There is also an obstruction to repairing every truncated nonnegative polynomial by one fixed filtered linear operator. On the finite-dimensional space of polynomials of degree at most 2d, let P be the globally nonnegative cone and S the SOS cone, with P≠S. Suppose T=mI+N is real linear, m>0, and N strictly lowers degree. For D_a f(x)=f(ax), the component of D_(1/a)ND_a from degree k to degree j<k is a^(k−j)N_jk, so D_(1/a)TD_a tends to mI as a↓0. Dilations and inverse dilations preserve both cones. If T(P)⊆S, every conjugate would map P into S; the closedness of S proved above would imply mP⊆S and hence P=S, a contradiction. Convolution by a positive measure of nonzero finite mass m and moments through degree 2d has exactly this scalar-leading form by polynomial Taylor expansion. The statement is not a prohibition on every positive linear operator: Gaussian averaging followed by multiplication by the constant polynomial sends P into S but has zero associated-graded action in positive degrees. [AFTER3634-FOURTH25-088](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1c1c89a83d884a563c6e3f7b0b80a975255d9e4017120ae479bc540d2b14fb66/FILTERED_OPERATOR_REVIEW.md#L7-L27)

The same argument gives a strict-square-positive countercertificate at this truncated scope. Degree lowering makes N nilpotent and T invertible by a finite geometric sum. Choose f∈P with Tf∉S. Separation from the closed convex cone S gives a linear Λ nonnegative on S with Λ(Tf)<0. Adding a sufficiently small positive multiple of nondegenerate Gaussian integration preserves that negative value and makes Λ strictly positive on every nonzero SOS polynomial. Set L=Λ∘T. Then L∘T^(−1)=Λ is strictly square-positive, but L(f)<0, excluding a positive representing measure for L. This does not assert pointwise nonnegativity of Tf, extension of either functional to the whole polynomial algebra, an effective separation algorithm, or a result for polynomial-dependent transformations or degree-raising coercive dynamics. The received item is an ordinary proof review with an explicitly repaired linearity premise, not a fresh kernel or executable verification. [AFTER3634-FOURTH25-088](https://github.com/theislampill/orthemology/blob/fc268be53bcadc98e0f2257ef5ea6d46d90cd5d4/research/t20-v6-20261012/sources/1c1c89a83d884a563c6e3f7b0b80a975255d9e4017120ae479bc540d2b14fb66/FILTERED_OPERATOR_REVIEW.md#L7-L27)


## 10. Effective recovery and finite certificates

The preceding existence and uniqueness theorems concern exact mathematical records. They neither supply a practical finite-data reconstruction method nor make validity or determinacy decidable. Some effective statements are nevertheless available under explicit input promises.

### 10.1 Computing an actual determinate law from all its moments

A **uniform moment name** is an oracle which, on input $`(r,k)`$, returns a rational number within $`2^{-k}`$ of the $`r`$th moment. Giving a finite prefix, or giving separate nonuniform existence claims for each moment, is weaker.

**Theorem 23 (promised determinate recovery).** Given a uniform moment name, promised to be the valid moments of a Stieltjes-determinate probability $`\mu\in\mathcal P_\infty([0,\infty))`$, one can compute the law in the weak topology and in ordinary $`W_1`$, every normalized tilt by $`e^{-tx}`$ for computable $`t\ge0`$, all its polynomial moments, and any finite set of its time derivatives. The procedure is uniform under the promises; it does not decide validity or determinacy and has no asserted practical complexity bound.

**Proof.** Compactify by $`y=x/(1+x)`$ and work in the probability measures on $`[0,1]`$ with their $`W_1`$ metric. This is effectively compact. Explicitly, move a probability onto the grid $`j/n`$, then round the first $`n`$ weights down to multiples of $`1/Q`$ and place the remainder at the final grid point. The resulting finite list of rational atomic laws is a $`(1/n+n/Q)`$ net. By refining nets and checking a positive margin, finite covers by rational open balls can be semidecided; a genuine finite cover has a positive Lebesgue margin.

Define the continuous clipping functions
```math
c_N(y)=\min\!\left(\frac{y}{1-y},N\right),\quad c_N(1)=N.
```
They are Lipschitz with constant $`(1+N)^2`$, and $`c_N^r`$ has Lipschitz constant $`rN^{r-1}(1+N)^2`$. The compactified representing fibre is exactly the set of probabilities $`\lambda`$ satisfying, for every $`r,N\ge1`$,
```math
m_r-\frac{m_{r+1}}N
 \le\int c_N^r\,d\lambda\le m_r.
\quad\text{(50)}\quad
```
The tail inequality $`x^r-\min(x,N)^r\le x^{r+1}/N`$ proves necessity. Conversely, the upper bound for $`r=1`$ excludes an atom at $`y=1`$. Monotone convergence and both bounds as $`N\to\infty`$ give exactly every prescribed moment.

Strict violations of (50) are semidecidable open conditions, by the uniform names and the explicit Lipschitz constants. Thus this fibre is an effectively closed subset of an effectively compact space. The determinacy promise makes it a singleton. To approximate its point, enumerate rational atomic centers $`q`$ and search for a finite cover of the whole probability space by $`B(q,\varepsilon)`$ together with finitely many enumerated open pieces of the fibre's complement. Such a cover certifies that the singleton lies in that ball. Some search terminates because there is a rational center close enough to the point. This is an explicit instance of effective compact singleton extraction; see [Galatolo, Hoyrup and Rojas](#references).

To recover a law on the original half-line, push the rational approximation through $`c_R`$. If $`H>m_1`$, the mass beyond $`R`$ is at most $`H/R`$, while compactified $`W_1`$ error is magnified by at most $`(1+R)^2`$ on the clipped part. For ordinary $`W_1`$, the discarded first-moment tail is at most $`m_2/R`$. Computable rational upper bounds on these moments therefore give an effective original-space approximation.

For tilted moments, let $`U>t`$ be rational and use the clipped integrand
$`c_R(y)^r e^{-t c_R(y)}`$. For $`r\ge1`$ it is bounded by $`R^r`$ and has the explicit Lipschitz bound
```math
\bigl[rR^{r-1}+UR^r\bigr]\bigl(1+R\bigr)^2.
\quad\text{(51)}\quad
```
For $`r=0`$ use $`U(1+R)^2`$. Changing $`t`$ by $`\Delta t`$ changes the clipped integral by at most $`R^{r+1}|\Delta t|`$. The unclipped tail error is at most $`2m_{r+1}/R`$ for $`r\ge1`$, and at most $`m_1/R`$ for $`r=0`$. This computes
$`A_r(t)=\int x^r e^{-tx}d\mu`$, including $`t=0`$ without trying to decide whether a real input is exactly zero.

Jensen's inequality gives $`Z(t)\ge e^{-Um_1}`$, so a computable positive rational lower bound $`D`$ is available. If numerator and denominator are approximated within $`\eta<D/2`$ and the true numerator is at most $`K`$, the quotient error is at most
$`2\eta/D+2K\eta/D^2`$. Hence every normalized moment is computable. The identity $`A_r'=-A_{r+1}`$ supplies finite derivatives. On bounded time intervals,
$`|A_r'|\le m_{r+1}`$ and
$`|m_r'|\le m_{r+1}/D+m_rm_1/D^2`$, providing effective continuity as well. The actual tilted law follows by weighted integration or by applying the same recovery argument to its now computed determinate moment record. ∎

One can equivalently place computable upper envelopes $`B_r>m_r`$ on all clipped integrals. On that effective compact class, the bound $`B_{r+1}/R`$ makes each unbounded moment a uniformly computable continuous functional. This is the tail control behind the proof, not an implicit appeal to computability of arbitrary unbounded integrals from weak convergence. The relevant effective integration framework is developed by [Hoyrup and Rojas](#references).

Computability need not come from a convergent Taylor series. The density $`\tfrac12e^{-\sqrt x}`$ on $`[0,\infty)`$ has moments $`(2r+1)!`$ and no positive exponential moment in $`x`$. It is nevertheless determinate. Given any competitor, symmetrize $`Y=\pm\sqrt X`$. For $`0<b<1`$, the even moment series gives
```math
E\cosh(bY)=\sum_{r=0}^{\infty}(2r+1)b^{2r}
          =\frac{1+b^2}{(1-b^2)^2}<\infty.
```
Both symmetric laws have an exponential absolute moment and the same moments, hence are equal; squaring identifies the original laws. Yet the ratio of successive absolute terms in the formal Laplace series is
$`|t|(2r+3)(2r+2)/(r+1)`$, tending to infinity. Theorem 23 computes the continuation despite zero Taylor radius at the origin.

A calibrated Fisher jet can be another input format, but only with its actual-law and fixed-parameter promises. If $`F(t)=\log Z(t)`$, $`q=-F'`$, and $`V=F''`$, then
```math
\kappa_1=q(0),\qquad
\kappa_n=(-1)^nV^{(n-2)}(0)\quad(n\ge2),
```
```math
m_{n+1}=\sum_{j=0}^{n}\binom nj\,\kappa_{j+1}m_{n-j},
\qquad m_0=1.
\quad\text{(52)}\quad
```
The second relation follows by differentiating the exponential generating identity between moments and cumulants coefficient by coefficient; only finitely many quantities enter each coefficient. It converts a uniform calibrated jet name into a moment name. An uncalibrated metric jet does not determine the missing mean or parameter scale, and no nonsingular inverse mean coordinate is automatically supplied.

There is a readout-only variant. If a computable continuous readout on an effectively compact representing fibre is promised constant there, its image is an effectively compact singleton and the same extraction computes that common value, even when the law is not unique. For the entire half-line mean continuation, constancy over the fibre is equivalent to determinacy, by Laplace uniqueness. Neither fibre constancy nor determinacy is decided by the extraction.

Two controls show why the promises matter. For any finite cutoff $`D`$, put $`n=D+1`$ and distribute the binomial weights $`\binom nj/2^{n-1}`$ on the even, respectively odd, integers $`j\in\{0,\ldots,n\}`$. Finite differences show equality of the first $`D`$ moments. Their probability generating functions are
$`[(1+z)^n\pm(1-z)^n]/2^n`$.
With $`h(z)=((1-z)/(1+z))^n`$, the difference of their logarithmic derivatives contains $`2h'(z)/(1-h(z)^2)`$, which is nonzero at $`z=1/2`$. Thus their damped means differ at $`t=\log2`$.

Moreover a weakly computable law need not have computable unbounded moments. For a machine that halts at a late stage $`j`$, use
$`(1-1/j)\delta_0+(1/j)\delta_j`$; if it never halts, use $`\delta_0`$. A finite simulation approximates the law weakly uniformly, because a late halt changes only mass at most $`1/j`$. Its mean, however, is the halting bit. This family does not provide the uniform moment name required above. Nor does Theorem 23 recover an indexed hidden $`\ell^1`$ representation from an unlabelled law. The complete argument is incorporated from [the exact original effectivity proof][effective-law-source], including the corrected bound (51).

### 10.2 What can be detected by enumerating negative witnesses?

Under the promise of an exact coercive hierarchy with computable coefficients and uniformly certified polynomial coordinates at rational times, Theorem 12 gives a semidecision for failure of realizability somewhere: if the path is not representable, it cannot be square-positive throughout. Some square evaluation is strictly negative. Continuity and finite dependence on polynomial coefficients give a rational time and rational-coefficient polynomial with the same strict sign. Dovetailing their certified upper bounds eventually finds such a witness. A negative boundary value also persists at a nearby positive time. This does not verify a positive path in finite time, decide the hierarchy promises, or provide a uniform degree or running time. It is different from the hidden-coordinate case, where **every** square may remain positive and a nonnegative nonsquare witness is needed.

For the explicit valid-initial escape (48), that second type of witness can also be searched effectively in one controlled coordinate with energy $`g=z^2`$ and two hidden coordinates. The Schur values are rational, and the finite-difference construction uses computable rational residuals and a least admissible integer radius at each step. For a hidden polynomial $`p`$ of degree $`d`$, the uncomputed positive/negative-block tail after degree $`M\ge d`$ is bounded by its coefficient-sum constant times $`2^{-M}`$. In particular,
$`N(F)`$ has a tail bound $`4\cdot2^{-M}`$, and $`n_0=N(1)`$ has bound $`2^{-M-1}`$.

Define at a fixed rational $`t>0`$
```math
I_m(t)=E[e^{mZ-te^{2Z}}],
\qquad
J_m(t)=\frac1S\sum_{j\in\mathbb Z}
 e^{-j^2/2+mj-te^{2j}}.
```
For $`R>m`$, the continuous tails are at most
$`2e^{m^2/2}e^{-(R-m)^2/2}`$. On $`[-R,R]`$, the integrand derivative is bounded by a computable multiple of
$`(m+2te^{2R}+R)e^{mR}`$, giving certified interval quadrature. If $`J+1\ge\max(1,4m)`$, the discrete tail is bounded by
```math
\frac{2e^{-(J+1)^2/4}}{1-e^{-(2J+3)/4}},
```
and $`S\ge1`$. Thus all these quantities and the full coordinates
```math
L_t(z^mu^av^b)=
\frac{\Lambda(u^av^b)I_m(t)+N(u^av^b)J_m(t)}
     {I_0(t)+n_0J_0(t)}
\quad\text{(53)}\quad
```
are uniformly computable. Jensen's inequality supplies the positive denominator bound
$`I_0+n_0J_0\ge(1+n_0)e^{-te^2}`$.

Set $`B=N(F)`$ and, for a rational polynomial $`q`$, put
```math
W_t(q)=-I_t(q^2)+B J_t(q^2),
\qquad
L_t(q^2F)=\frac{W_t(q)}{I_0+n_0J_0}.
\quad\text{(54)}\quad
```
The existence argument after Theorem 21 gives a real polynomial with negative $`W_t`$; finite-degree continuity gives a rational one. Enumerate rational polynomials and precision requests, dovetailing strict negative upper bounds. The search terminates at every fixed rational positive time. It is $`q^2F`$ that is nonnegative; $`q`$ need not be. If the certified intervals are $`W_t\in[w_l,w_h]`$ with $`w_h<0`$ and denominator $`D\in[d_l,d_h]`$ with $`d_l>0`$, the correct normalized interval is
```math
L_t(q^2F)\in[w_l/d_l,\ w_h/d_h].
\quad\text{(55)}\quad
```
The order of the denominator endpoints reflects the negative numerator.

This is a proof of a terminating search under exact input promises, not a claim that a generic search was executed here. The least degree can diverge near zero. For this special family, $`W_0(q)=(B-1)\int q^2d\alpha`$ and $`B-1=P(F)>0`$, so every fixed-degree quadratic form remains positive on some initial interval. Theorem 22 is stronger: it protects the entire finite truncated moment problem, not just the family (54). These effective refinements incorporate [the corrected witness-search proof][effective-escape-source] and preserve [its review's actual first corrections][effective-escape-review-source].

### 10.3 An actually computed sparse separator

The later public work goes beyond existence and a terminating-search proof. For $`t=1`$, it supplies the explicit polynomial
```math
H(z,u,v)=z^{2048}F(u,v),
\qquad
-3^{2097161}\lt{}L_1(H)<-\frac43.
\quad\text{(56)}\quad
```
It has four monomials, total degree $`2054`$, and is nonnegative everywhere. This is the square choice $`q=z^{1024}`$ in (54). The analytic bounds are given here, while the exact finite hidden-arithmetic input remains a separately retained computational dependency.

That input is the strict rational bound $`B=N(F)<2^{171}`$, obtained by summing the negative parts of the finite-difference blocks through degree six and adding the tail $`1/16`$. The exact radii used are
```math
\begin{aligned}
R_1&=1,& R_2&=544,& R_3&=5326848,\\
R_4&=1210631850670080,\\
R_5&=114502302747635522324083834880000,\\
R_6&=1631190472850543123295836647062767816302697363159516479654977517978.
\end{aligned}
```
Only Schur indices through ten are needed for this hidden polynomial. The finite atomic counts through degree six are $`0,5,7,13,19,26`$. The source and its independent review report exact rational reproduction of this bound. Their arithmetic input and checker are retained; reading the result and review does not constitute a fresh execution of those files.

For the continuous term, on $`x\in[69/20,7/2]`$ the exponent is bounded by
```math
2048x-e^{2x}-x^2/2
 >2048\frac{69}{20}-1097-\frac{49}{8}
 =\frac{238499}{40}>5962,
```
using $`e^7<1097`$. Since the interval length is $`1/20`$, $`1/\sqrt{2\pi}>1/3`$, and $`e^5>60`$,
```math
I_{2048}(1)>\frac{e^{5962}}{60}>e^{5957}.
```
For the lattice exponent $`h(j)=2048j-j^2/2-e^{2j}`$, the sum over $`j\le2`$ is less than $`2e^{4096}`$. At $`j=3`$, $`h(3)<5740`$ because $`e^6>400`$; at $`j=4`$, $`h(4)<5204`$ because $`e^8>2980`$. For $`j\ge4`$,
$`h(j+1)-h(j)=2048-j-1/2-(e^2-1)e^{2j}<-1`$.
Thus the remaining tail is less than $`2e^{5204}`$. The two outer contributions together are less than $`e^{5740}`$, since $`e^{536}>4`$. Dividing by $`S\ge1`$ yields
```math
J_{2048}(1)<2e^{5740}\lt{}e^{5741}.
```
Since $`2^{171}<e^{171}`$, the witness numerator satisfies
$`W_1<-e^{5957}+e^{5912}<-2`$.
The denominator is at most $`1+n_0\le3/2`$, so $`L_1(H)<-4/3`$.

For the lower bound, $`W_1\ge-I_{2048}(1)\ge-e^{2048^2/2}>-3^{2097152}`$.
Jensen gives the denominator at least $`I_0(1)\ge e^{-e^2}>e^{-9}>3^{-9}`$. Dividing gives the lower bound in (56). The elementary inequalities used above can all be certified by finite rational Taylor sums and geometric remainder bounds; the source uses orders $`12,20,30,40,50,60`$ for exponents $`1,2,5,6,7,8`$ respectively. No floating eigenvalue, quadrature estimate, or numerical sign guess enters this separator proof.

The [computed separator result][computed-separator-source] and [independent exact-arithmetic review][computed-separator-review-source] supersede the older statement that no actual separator had been computed. They do not turn this chapter's source receipt into a new run, a general complexity result, or a reason to discard its unique computational inputs.



## 11. What the consolidated results establish

A hierarchy is a record of how expectations must change. Its equations alone do not make the record a probability law, and a law-level existence theorem alone does not make the record identify its law. The results above give the following exact distinctions.

| State and operation class | Sufficient record or condition | Warranted conclusion |
|---|---|---|
| Known finite numerical support of size $`N`$ | Moments through degree $`N-1`$ | Exact finite closure and complete continuation under the specified linear controls |
| Fixed compact numerical support | All polynomial moments | Unique law and exact bounded exponential reweighting |
| Half-line linear damping | Actual realizability, or nonnegative hierarchy plus one positive-time representative | Unique initial law for each complete realizable path; multiple paths can share an indeterminate initial record |
| Half-line coordinate-positive hierarchy | Valid initial record satisfying Stieltjes–Carleman | Actual evolution forced; mere initial determinacy is insufficient |
| Autonomous coercive polynomial energy | Full square positivity and the full hierarchy | Joint existence, positive-time determinacy, and exact exponential tilt |
| Arbitrary signed polynomial energy | Full square positivity and determinacy of every initial square-weighted energy distribution | Exact tilt on its actual weighted-integrability horizon |
| Time-dependent SOS energy | Cumulative radial SOS control from the origin | Joint existence and positive-time determinacy, even with instantaneously rank-one rates |
| Fixed controlled subspace with one hidden coordinate | Full joint square positivity and cumulative control | Joint existence, possible ambiguity, and exact signed-projection continuation |
| Fixed controlled subspace with at least two hidden coordinates | The preceding conditions alone | No automatic joint existence; a valid initial record may lose it immediately |
| Uniform full scalar moment name | Promised validity and Stieltjes determinacy | Computable law and nonnegative tilt, without a finite validity test or complexity guarantee |

For actual laws under a fixed operation, inverse positive weighting preserves null sets. At the polynomial-functional level, Corollary 14 establishes the stronger algebraic null-ideal identity for every autonomous square-positive hierarchy, even before joint existence is known. Neither statement supplies quantitative stability. Likewise, the rank of a cumulative energy form measures which directions its weighting controls; it is not a covariance rank, a dimension of persons, or a count of independent scientific explanations.

The counterexamples also distinguish different failures. The lognormal pair gives two genuine laws with the same complete initial record and different future responses. The scalar atom-deletion example begins with a determinate law but preserves only coordinate positivity. The hidden-coordinate escape preserves strict positivity of every square and begins with a genuine **indeterminate** joint record. Its explicit nonsquare witness and the finite-prefix delay theorem show why arbitrarily many successful finite tests do not imply full realizability.

Some conditions can be checked within narrower models, but the general statements do not supply uniform finite certificates of success. No degree cutoff independent of the support is available for compact moment recovery. No uniform detecting degree near time zero follows for the escape examples. A computable complete record under a determinacy promise need not yield a stable or efficient inverse, and positive-time analyticity need not extend to the initial boundary. For the lognormal examples, $`\int e^{cX}d\mu=\infty`$ for every $`c>0`$: the term $`ce^z`$ overwhelms the Gaussian exponent in logarithmic coordinates. The bounded perturbations in (8) preserve this divergence. Thus forward nonnegative damping cannot be promoted to unrestricted signed amplification.

A point-concentration defect is also too coarse to distinguish the relevant unbounded states. If it is defined as $`1-\sup_x\mu(\{x\})`$, it equals one for every atomless law, including distinct continuous moment-equivalent laws and many determinate ones. It does not decide moment determinacy, continuation equivalence, or the admissibility of a new operation.

The exact hierarchy remains indispensable. For example, taking the flat function $`b=1-\varepsilon e^{-1/t}`$, setting the odd moments to zero and $`A_t(x^{2n})=(-1)^n b^{(n)}(t)`$ gives a formal solution for the coercive energy $`h=x^2`$ with initial record $`\delta_0`$. But $`A_t(x^4)=\varepsilon e^{-1/t}(2t-1)/t^4`$ is negative for $`0<t<1/2`$. Coercivity does not repair a violation of the square-positivity hypothesis. Conversely, with $`h=0`$, Theorem 19 gives a constant strictly square-positive nonmoment hierarchy; the lack of compact energy fibres is substantive.

The arguments here do not decide whether additional hypotheses can prevent hidden-coordinate escape from every **jointly determinate** initial law. They do not classify all noncoercive polynomial energies, general polynomial transport flows without polynomial inverses, or continuously varying signed schedules on unbounded state spaces. Those questions require their own hypotheses and evidence. The proofs do settle the previously narrower gaps addressed here: arbitrary coercive polynomial energies, general controlled SOS rates, all-or-none positive-time joint representation, the full nonmoment functional, an actual sparse escape certificate, and exact finite-prefix representability.

For Orthemology, these results provide a rigorous account of what a numerical tensor state does and does not preserve under corrective reweighting. They can support a theory of inquiry only after its state variables, observations, and admissible operations are specified. They do not establish that a tensor is a complete semantic state, that numerical symmetry identifies distinct cognitive roles, or that a finite-dimensional probability model constitutes the original unfinished n-person noetic field. The accepted papers retain their editions and scientific authority; constructive companions and broader geometric programmes remain distinct. The present contribution is the coherent mathematical treatment of this particular family of state, existence, continuation, and diagnostic problems.

## References

1. Marc Harper. *Information Geometry and Evolutionary Game Theory*. 2009. [arXiv:0911.1383](https://arxiv.org/abs/0911.1383), especially §§2.2–2.4 for the Fisher–Shahshahani setting.
2. Konrad Schmüdgen. *Ten Lectures on the Moment Problem*. 2020. [arXiv:2008.12698](https://arxiv.org/pdf/2008.12698). Theorems 1.9, 1.12, 1.15 and 2.7 supply the Haviland, Hamburger, Stieltjes and Stieltjes–Carleman statements; §2.1 treats indeterminate lognormal examples.
3. Mihai Putinar and Konrad Schmüdgen. *Multivariate Determinateness*. 2008. [arXiv:0810.0840](https://arxiv.org/pdf/0810.0840), Theorem 25 for the multivariate Carleman existence and uniqueness conditions. The stronger base hypothesis in Theorem 31 and Corollary 32 is kept separate.
4. Konrad Schmüdgen. *Chapter 12: The Moment Problem on Compact Semi-Algebraic Sets (Revised Version)*. 2023. [arXiv:2309.10052](https://arxiv.org/pdf/2309.10052), Corollary 12.34(iv).
5. Konrad Schmüdgen. *The Moment Problem*. Graduate Texts in Mathematics 277. Springer, 2017. [DOI:10.1007/978-3-319-64546-9](https://doi.org/10.1007/978-3-319-64546-9). Propositions 13.4–13.5 and the chapter's historical notes give the classical nonmoment-functional antecedent. [Public text](https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf).
6. Christian Berg and J. P. R. Christensen. “Density questions in the classical theory of moments.” *Annales de l'Institut Fourier* **31**(3), 99–114, 1981. [DOI:10.5802/aif.840](https://doi.org/10.5802/aif.840); [full text](https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf). Theorem 7 is the full-atom-deletion result used in Proposition 7.
7. Zenon Jan Jabłoński, Il Bong Jung and Jan Stochel. *A Non-hyponormal Operator Generating Stieltjes Moment Sequences*. 2011. [arXiv:1110.0249](https://arxiv.org/pdf/1110.0249), §2.1, especially the Krein extremal measure and its zero atom.
8. Markus Kuba and Alois Panholzer. *On Moment Sequences and Mixed Poisson Distributions*. 2014 author version. [Full text](https://www.dmg.tuwien.ac.at/kuba/preprintMomseq.pdf), Lemma 1. Its Hamburger Carleman formulation is distinguished from the Stieltjes transfer proved in Theorem 8.
9. Stefano Galatolo, Mathieu Hoyrup and Cristóbal Rojas. *Dynamics and Abstract Computability: Computing Invariant Measures*. [Author text](https://members.loria.fr/MHoyrup/computinvmeas.pdf), §2, especially Proposition 1, Remark 4 and Lemma 2.12 for effective compactness, singleton extraction and probability-measure spaces.
10. Mathieu Hoyrup and Cristóbal Rojas. *Computability of Probability Measures and Martin-Löf Randomness over Metric Spaces*. [Author text](https://members.loria.fr/MHoyrup/random_metric.pdf), especially §4.3 for effective integration.

The public Orthemology proofs cited in the text authenticate the particular statements and corrections consolidated here. They are linked at fixed historical editions so that the derivations can be compared without making historical file reconstruction part of ordinary reading. Full mathematical arguments are given above; the accompanying source-incorporation review distinguishes redundant prose from independently necessary formal, computational and review evidence.



[FORM] Orthemology, *Graded Representations, Witnessed Revision, and Inquiry Landscapes: A conditional mathematical extension of Orthemology*, version 1 research draft, 8 September 2026. [Exact public source][FORM]. Sections 1.1–1.4 develop its finite typed-record construction, degree-shift and contraction arguments, parity calculation and continuation boundaries. The source itself distinguishes these elementary conditional results from the production extractor, semantic interpretation and empirical comparison still needed for an application. The explicit history sum clarifies its infinite-event example. These finite record tensors are separate from the moment hierarchies studied in the rest of this chapter; neither construction completes the original unfinished N-person programme.

[activation-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/research-v6/type_collective/cumulative_damping_prose/ACTIVATION_BOUNDARY.md
[coercive-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/204f63e544b1afd9538230f95f8ebfbc613b9847c579dfb901de6d10e40ebb10/coercive-square-positivity-20261010__RESULT.md
[computed-separator-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/8e026e569b52b6495050111ce92a063291d298c6e496a13775c5fa222dc99ff6/COMPUTED_SEPARATOR_REVIEW.md
[computed-separator-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/b04978552464b25a93fe39c4a61ccf80dcf64bc04e17c23ff6fd6242667f1a20/RESULT.md
[coordinate-computation-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/862a4b005351c1f980e1daf2820d8d871fa16835d53029ce27941244d248915f/RESULT.md
[coordinate-counterexample-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/cafc520026c66f94442346ff308ed4e202d70e10be8963b8a24ad17bda4e1e0a/RESULT.md
[coordinate-diagnostic-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/5d0e97c5f4e50ac7981765292b6aa161076a4d0b6af7fbc46aa18e40bd89c2b2/DIAGNOSTIC.md
[countermodel-lean-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/7ebe9f1bc3b7e7e8d7fb966a5b0c82f7fa9a53d84e6d0887b260847fed1e443e/Countermodel.lean
[cumulative-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/6405258b6c2523f2e28d06d5cb9cb054fa876aa3744690856e79cc078dbd62ea/REVIEW.md
[cumulative-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a530a5341497e3416345a7ec325e986a7e54f2c254954f80fd32f1f596e6244f/RESULT.md
[effective-escape-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c4205f111e660f91a8f28f6987351af64f71dae95246c564055843e895132db4/REVIEW.md
[effective-escape-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/dbfb6e5190a12d943c4f2530350ad66760f1f093fe631b3c6884de5ab38d00d5/RESULT.md
[effective-law-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/9661eef2d88370d2d996e68f666777c6ac0ffb93155d102ec50873f155e91383/RESULT.md
[finite-prefix-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/477b75c8887e768f130b475f9e07516584e5780ce78f93d7a291c9fa0423d492/REVIEW.md
[finite-prefix-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/f7f06518e210b860502c0971aa9ad47a410198d84c519b149a49b953f67c242f/RESULT.md
[finite-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/03f027122c0a908f1f6bcfcc61951223ca1fca547d8599aac2aa3437e3c01a11/RESULT.md
[full-formal-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/e9f8ac99e4df6f23171028bcd3ef99eb562f69e2229e056ec3a13fbf3954ccec/REVIEW.md
[full-formal-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/d15611cd809d5aeeda80a124d1ef524b4ddf13f1b3fb1d55e2a51db49b6ecc97/RESULT.md
[hidden-boundary-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/12d3e23f4f01f934cce554503368ccc2755ad8cef9055c432380f7b6271abd3f/SHARP_HIDDEN_BOUNDARY.md
[hidden-persistence-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/cf9b6626b24329f8dd27d2ff2d78027ea4e222f45a6b7621209aa4d39b840fe3/RESULT.md
[moment-boundary-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a0fa9117ff47df9f07133c1ed49c682c7c2e73d20881e83f3c242dfb3faeb9e3/RESULT.md
[nonmoment-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/08fdec67591a4a0639fa4ca721293bd8c480ec405dcd1a7c5a08d3244aa84c80/PROOF.md
[partial-control-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/047ec278a738cdc018b7118113afa93a8fa6d0aa1a315d33440f2aa0586a53ea/RESULT.md
[partial-sos-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/9f20a6b0125b98a659d87b0a3758630b4e3ded99ba376e1bf4fbcc31d49765db/GENERAL_SOS_BRIDGE.md
[scalar-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c5aeeeed56b5bf5edfa9b87570249f142e3d1be9c06218d8007013c66f5eb688/RESULT.md
[signed-earlier-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/adbbea04d51ac90692d167c5d522fa4cda23558dcc2e093c6bcf76e24f3a3553/RESULT.md
[signed-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a297237142d62fb1cb655dc08844103f60044fa4035cc865aa11fa94d8d5b2f8/REVIEW.md
[signed-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/2ac90188cc0cb17d3bb80f3ba63d9dfe62742db5919cf86d7001c7e0baf39e55/RESULT.md
[tensor-review-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/448ace340a04d56aaa26b1cab0d7f720dcda56c3fe1a37bdff76c8375c30ad07/tensor-realizability-independent-review-20261010__REVIEW.md
[tensor-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a/tensor-realizability-extension-20261010__RESULT.md
[valid-initial-escape-source]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c6dc162591a6827b8ae09a3b0be902ee53573435ae5b4f4ecfb1fc66ed835ada/RESULT.md

[FORM]: https://github.com/theislampill/orthemology/blob/28679eaed33ee48cf0c5d15ba6dc3b27aac9067b/theory/lineages/h-formalisation/orthing_formalisation_v1.md


## Exact public sources for the additional discussion

These links identify the received public bodies at their immutable original revision. Their historical review and prospective statuses remain source-relative; this exposition performs no new source-program or formal execution.

- [Finite predicate-functor transport into Boolean tensors][R18-G273]. finite extensional transport with explicit hypotheses. Git blob `6bb2b13b32994328b207c064c91220f723bdd2ce`.

[R18-G273]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-live-20261009/checkpoints/CP08/t20-next-frontier-20261008/qualitative-tensor-transport/RESULT.md


## Source guides for the additional arguments and qualifications

These exact public guides identify the reported results, historical review scopes and dependencies used in the additional discussion. A guide citation does not claim receipt or renewed verification of every linked proof, primary source or execution record.

- [GUIDE105-G001] Pointwise-coercive changing-gradient escape: intermediate countercontrol.
- [GUIDE105-G002] Conditional entropy control.
- [GUIDE105-G004] Signed autonomous energy continuation.
- [GUIDE105-G005] Full-law coarse-graining packet.
- [GUIDE105-G007] Full-law coarse-graining: accepted intermediate component.
- [GUIDE105-G010] Untitled source guide.
- [GUIDE105-G011] Gaussian correction geometry: accepted intermediate component.
- [GUIDE105-G012] Entire-fixed-marginal endpoint action.
- [GUIDE105-G016] Correlated-target independent review.
- [GUIDE105-G018] Nonnegative moving-gradient escape.
- [GUIDE105-G019] Gaussian entropy transfer: portable accepted intermediate component.
- [GUIDE105-G029] Gaussian entropy transfer review packet.
- [GUIDE105-G035] Singular Gaussian entrance evidence.
- [GUIDE105-G038] Finite polynomial descriptor closure boundary.
- [GUIDE105-G046] Correlated-target fixed-marginal correction.
- [GUIDE105-G053] Fixed-marginal constrained correction.
- [GUIDE105-G057] Moving-objective order interface: intermediate evidence.
- [GUIDE105-G059] Ordered-control projective transport: intermediate preservation.
- [GUIDE105-G061] Quartic variance continuation: separate accepted supplement.
- [GUIDE105-G067] Signed autonomous energy continuation.
- [GUIDE105-G079] Unbuilt development intermediates.
- [GUIDE105-G083] Finite polynomial state closure: intermediate preservation.
- [GUIDE105-G094] Gaussian correction geometry: author packet.
- [GUIDE105-G101] Fixed marginal correction review packet.

[GUIDE105-G001]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/0174f088bc34d917efe251fb40e1bce4ad33f6896c14f08486edf360cce56fff/README.md
[GUIDE105-G002]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/03a89ae96e6612620b0312aaef1ecb907eff535f66d31d7a4d5dc6f226074e2d/README.md
[GUIDE105-G004]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/05602a7c8e1353961c33efecd62b7d955064901ca43315aca2c94e704fdbe0cc/README.md
[GUIDE105-G005]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/0a5cd3af281313de7821dddc9d12bfd5a05af6bd48d818ea29eff48f74893dd0/README.md
[GUIDE105-G007]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/0fc42ccc06a810a8fb6406ecaf00d4a110d2a1f46d4924fa4eab92859142bd61/README.md
[GUIDE105-G010]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/1587c146d95459a94d221faf0b67cb18215bc3d97eccf1256b82e9b05cc74d19/README.md
[GUIDE105-G011]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/1b6017227ffcf86072dc569a06cef3bc88ee6d5eab0c8dbf738d1c4c57fd6b82/README.md
[GUIDE105-G012]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/1cfb7b8d434f92d76f5c0e207659b8fe8b81e9f07cf0c67a9a03127fc526ccde/README.md
[GUIDE105-G016]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/280362da432793d6e725fcdab291bf2813f810e4a20832a688f1d966254a3390/README.md
[GUIDE105-G018]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/2a154bdf328fece5f778af435e1df1b277d9c688b1380c8fba34587e1f38f21c/README.md
[GUIDE105-G019]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/2b0b8b6a74b7fdc5ba1dbe6b46008caefa538e1d3b259ea04ed0e2b9585b307a/README.md
[GUIDE105-G029]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/5335293a33ddba5e10ceb44ec35dd91dbe86f23d107e784cfcb8fa68aafa4ca5/README.md
[GUIDE105-G035]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/6a76213d0f1df8a2f4e563d2f0fd1ce681823e8d4bdd8f3b2f0801df690fbb0b/README.md
[GUIDE105-G038]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/719293c172700fb5415668d1237d2be96be74c525451c3d448c7cbfdc2c2449a/README.md
[GUIDE105-G046]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/823138c702525d3e680a0ba9fab3e733e09179a32389c281902a33f0272e6d1c/README.md
[GUIDE105-G053]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/914c6786931bacf832a80d8e32941cfbebbdff66f2bc574aad48e5170989c782/README.md
[GUIDE105-G057]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/91ed8c74c0d53f66af3f9e0fbdbab51910bc4be92d20e46e866a4434aabb0307/README.md
[GUIDE105-G059]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/98c88347b4bd9e4f2d09ad892b7d9f209ff2e93a43965d710596f39f127f5dd9/README.md
[GUIDE105-G061]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/9c6ec5263abf1a42e0dea266078d87c572bfc92439236acbaa6bfc4c0ea13242/README.md
[GUIDE105-G067]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/a8c79cf80ba9fd5643dea744bfc6c9d679421404c9d0ada722e4f3626a76e2b7/README.md
[GUIDE105-G079]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/d0b24497a9ddf2b34f91483b7ee7cfb61acf1ec2430c0aecb5b61c32239b392a/README.md
[GUIDE105-G083]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/d5581d7beec9da984e667a2f66afd97cd98bc2ab2b94f1e76e743ba7ae41c856/README.md
[GUIDE105-G094]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/e2139a907c0af4aba7dd0e02d838bcef0d0cf521e478adf2bd338a9fa04673ba/README.md
[GUIDE105-G101]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/e9214d31a3dd05329d0cfde1745d3fe870a0f3c7690ed10f4aefa05f23d124c9/README.md
