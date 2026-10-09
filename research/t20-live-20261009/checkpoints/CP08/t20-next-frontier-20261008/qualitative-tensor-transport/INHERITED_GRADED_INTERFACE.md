---
title: "Graded Representations, Witnessed Revision, and Inquiry Landscapes"
subtitle: "A conditional mathematical extension of Orthemology"
author: "Research synthesis from the accompanying dialogue"
date: "8 September 2026 · Version 1 · Research draft"
lang: en-GB
abstract: >-
  We formalise a representation-first extension of Orthemology in which a
  concrete episode has a declared, finite-support typed tensor representation,
  while the representation language leaves interaction degree open. We construct
  a faithful finite-record channel, characterise target-preserving compression,
  and give witnessed revision rules that retain obligation history. A separate
  inquiry landscape records prospective feasibility and supports explicit
  countermodels of result-correct but opportunity-reducing closure. An optional
  finite-game declaration yields classical mixed Nash existence and a quantitative
  surrogate-payoff regret bound. Coupled-energy, residual, quotient and hybrid
  certificates identify mathematical mechanisms that could support bounded
  dynamical applications. The proofs are conditional ordinary mathematics:
  no tensor ontology, empirical validation, repository adoption, or proof-assistant
  certification is claimed.
---

# Scope and the fixed headline

**An orthing is a process type; an orthing episode is a concrete token. Tensor structure enters through a declared representation, not through an identification of the episode with a tensor. The representation language leaves interaction degree open; every represented episode has finite typed support. Dynamics may change both represented state and the constrained landscape of later admissible inquiries.**

The three principal layers remain

$$
\mathsf{Orthing}_A,\qquad
\rho_A(e)\in T_{\mathcal T}(V),\qquad
\mathcal L_t,
$$

with episode tokens $e\in E_A$, a declared map $\rho_A:E_A\to T_{\mathcal T}(V)$, and a distinct historical ecology $\Gamma_t^\mu$. Neither the algebra nor a Nash equilibrium is the ontology of an episode.

This document develops the three agreed research tasks: define a tensor representation over the episode signature; define witnessed degree-lowering operations; and define the inquiry landscape independently of the ecology. It also formalises the optional strategic layer, the closure externality, the bounded reflexivity of the dialogue, and the potentially transferable dynamical mechanisms that motivated the discussion.

## Status, evidence, and authority

This is a **mathematical research draft**, not an adopted repository extension, a proof-assistant development, an empirical validation, or a claim of general mathematical novelty. Definitions introduced here are proposals. Propositions are proved in ordinary mathematical prose under stated assumptions. Standard results and elementary constructions retain their existing mathematical ancestry. The accompanying finite verification script checks selected examples; it is not a substitute for the proofs.

The repository basis was checked through the GitHub connector on 8 September 2026. The observed `main` head was

`f50dc1aee52356cc6adbef342387576b02afc124`.

The canonical core, notation registry, T300, tensor-programme note, corrective-transition decision, ecology decision, and sound-descent comparison provide the principal repository constraints [R1–R7]. Some application documents retain historical candidate banners. Their presence in the merged tree is not treated as scientific adoption. No repository, issue, branch, or owner-controlled ledger was changed to produce this draft.

Three kinds of statement must be distinguished throughout. **Source reports** say what the repository, uploaded Euler manuscript, or supplied excerpts state. **Definitions and constructions** supply the present proposed model. **Proved consequences** follow from that model; they do not establish that a real research community, human cognitive process, or software runtime satisfies its assumptions. A fourth category, **conditional transfer**, identifies a reusable mathematical mechanism together with the missing instantiation conditions.

## What the document establishes

The central results are a faithful finite-record encoding construction; a fibre criterion for target-preserving compression; an exact arbitrary-arity parity obstruction; a witness-composition invariant for obligation history; countermodels separating result correctness from future inquiry value; a conditional Nash existence theorem with a quantitative regret-transport bound; and continuous, discrete, coupled-energy, and hybrid stability certificates.

These results make the proposal mathematically usable without claiming that tensor degree is intrinsic, that an equilibrium is reached, that admissibility entails truth, or that fluid singularity theory has already been transferred to Orthemology.

# Repository objects and the representation interface

## Process, token, record, and representation

The repository distinguishes the process type *orthing* from a dated, situated episode token. Its canonical signature is a structured record, not just the value of a classification function [R1, §§1–2]. In its notation, schematically,

$$
\begin{aligned}
e=\langle &\mathrm{id};m,\kappa,v;x,H;\alpha,w,A,T,t;\\
&\vec\mu,\mathrm{MetaTok},\pi;\vec C,\hat p;r;\mathrm{estatus};\\
&\mathcal Q_e;\delta_e;\mathrm{hand}_{\rm in},\mathrm{hand}_{\rm out};
 a,\mathrm{Succ}\rangle.
\end{aligned}
$$

Here $\mathcal Q_e$ is a claim ledger, whereas $\delta_e$ records obligation dispositions. Evidence, authority to act, inferred profiles, and actual profiles are distinct. Successors are labelled lineage edges and need not be unique. An ordered trace is required where the declared pathway assessment needs it; exhaustive logging of every event is not a universal requirement [R1, §§2.2–2.2a].

We use $\mathsf{Orthing}_A$ for the process type. The symbol $\mathcal O$ is left to the repository's universal ortheme universe, with $\mathcal O_A$ its analysis-relative repertoire [R2]. The proposed tensor map is one member of a declared representation family, not a replacement for that family.

**Definition 2.1 — Representation declaration.** A declaration $\mathfrak R$ fixes a scalar field, typed factor spaces, admissible typed words, finite record extraction, interaction extraction, required preserved observables, and permitted representation changes. Its identity and version are recorded. More explicitly the representation is $\rho_{A,\mathfrak R}$; we retain the agreed shorthand $\rho_A$ only while $\mathfrak R$ is fixed.

No vector-space structure on $E_A$ is assumed. Thus $\rho_A$ is initially a map of sets. The expression $e+f$ is not defined merely because $\rho_A(e)+\rho_A(f)$ is defined.

## The finiteness assumption is about the declared view

**Assumption F.** For each episode in the chosen domain, the declaration provides a finite, well-typed record view $\xi_A(e)$ and finitely many selected interaction occurrences, each with finitely many arguments.

A finite handle to a differential equation, an infinite candidate family, or a worldly object is not a finite enumeration of everything that handle denotes. Reference targets need not be recursively expanded. A finite-record encoder preserves the declared record and its references; it does not prove completeness concerning the world.

Assumption F permits a total map on the selected $E_A$. Where a canonical object has no such available view, use a declared subdomain or a partial encoder. Finiteness must not be obtained by silently deleting unknown or inaccessible material.

## Signature-to-encoding contract

The following is the proposed extraction interface, not a new canonical repository schema.

| Signature group | What the finite view retains |
|:--|:--|
| Identity and occurrence | Episode identifier; occurrence identity and version; typed reference to $m$. |
| Observation and evidence | $x$; ordered entries of $H$; evidence IDs, scope, provenance, validity, and sequence position. |
| Actor and authority | Executor $\alpha$; acting warrant $w$; distinct binding authority where applicable. |
| Analysis and task | Analysis identity/version; task reference; representation-declaration identity/version. |
| Governing configuration | Rule references, versions and precedence; concrete metaorthemmata and their bindings. |
| Procedure and trace | Executed policy; declared trace granularity; ordered state/update references. |
| Candidates and placement | Separate typed candidate families; one inferred partial profile; unresolved axes. |
| Routing and verification | Route; per-claim evidence status; verification scope and non-claims. |
| Claims and obligations | Separate claim ledger and residual ledger; each obligation's identity and disposition. |
| Handoffs and successors | Packet identity/version; sending/receiving references; action-labelled successor edges. |

Empty containers, absent fields, objectively inapplicable values, epistemic unknowns, and missing evidence receive distinct tags wherever the source contract distinguishes them. They are not all encoded by the zero vector. This is important because algebraic zero otherwise has no way to say which kind of absence was intended.

# Typed words, grading, and finite actualisation

## The ambient algebra

Fix the field $\mathbb R$ and a set $\mathcal T$ of semantic role types. Let $V_\tau$ be a vector space for each $\tau\in\mathcal T$, and put

$$
V=\bigoplus_{\tau\in\mathcal T}V_\tau,
\qquad
T_{\mathcal T}(V):=T(V)=\bigoplus_{n\geq0}V^{\otimes n},
\qquad V^{\otimes0}=\mathbb R.
$$

This is the algebraic tensor algebra. Multiplication is concatenation of tensor factors. Its universal property concerns extension of a linear map on $V$ to an algebra map; it does not automatically turn an application-specific workflow composition into tensor multiplication [M1].

For a finite word $w=(\tau_1,\ldots,\tau_n)$, set

$$
V_w=V_{\tau_1}\otimes\cdots\otimes V_{\tau_n},\qquad |w|=n.
$$

Write $\epsilon$ for the empty word and $V_\epsilon=\mathbb R$. Distribution of tensor product over direct sums gives the word decomposition

$$
T(V)\cong\bigoplus_{w\in\mathcal T^*}V_w.
$$

Let $j_w$ and $P_w$ be its inclusion and projection maps. Let $P_n$ project to total degree $n$.

A declaration chooses $W_A^{\rm word}\subseteq\mathcal T^*$ and uses

$$
\mathsf H_A=\bigoplus_{w\in W_A^{\rm word}}V_w\subseteq T(V).
$$

The superscript distinguishes this word set from the repository's warrant repertoire $\mathcal W_A$. The frozen shorthand $W_A$ refers to $W_A^{\rm word}$ in this document only. If $W_A^{\rm word}$ is not closed under concatenation, $\mathsf H_A$ is a graded subspace, **not necessarily a subalgebra**. The set of admissible episode representations inside it need not be a linear subspace at all.

## Multi-degree does not retain order

For a word $w$, define $\mathbf d(w)\in\mathbb N^{(\mathcal T)}$ by counting each type's occurrences. We use $\mathbf d$, rather than the repository's actor symbol $\alpha$, for this multi-degree.

The full multi-degree component is

$$
T_{\mathbf d}(V)
=\bigoplus_{\substack{w\in\mathcal T^*\\\mathbf d(w)=\mathbf d}}V_w.
$$

It is not, without further identifications, just one sorted product $\bigotimes_\tau V_\tau^{\otimes d_\tau}$. For example, actor–evidence–claim and evidence–actor–claim occupy distinct word summands. There is a canonical factor-permuting linear isomorphism between the corresponding vector spaces, but the existence of an isomorphism does not identify their semantic roles. Symmetrisation is permitted only after a separate interchangeability argument.

## The actualisation theorem

**Definition 3.1 — Active support and degree profile.** For a declared representation $\rho_A:E_A\to\mathsf H_A$, set

$$
\begin{aligned}
S_A(e)&=\{w:P_w\rho_A(e)\neq0\},\\
c_{A,w}(e)&=P_w\rho_A(e),\\
\operatorname{Deg}_A(e)&=\{|w|:w\in S_A(e)\},\\
N_A(e)&=\max\bigl(\{0\}\cup\operatorname{Deg}_A(e)\bigr).
\end{aligned}
$$

The added $0$ makes $N_A(e)$ defined for the zero representation. Nonzero scalar components have degree zero. We distinguish selected interaction occurrences from **nonzero algebraic support**: cancellation can remove a component in a signed representation. The positive record construction below avoids cancellation of retained record atoms.

**Proposition 3.2 — Finite actualisation.** Every $\rho_A(e)$ has a unique finite word decomposition

$$
\rho_A(e)=\sum_{w\in S_A(e)}j_w c_{A,w}(e),
\qquad S_A(e)\text{ finite},\quad N_A(e)<\infty.
$$

Consequently $e\mapsto S_A(e)$ is a map $E_A\to\mathcal P_{\rm fin}(W_A^{\rm word})$.

*Proof.* An element of a direct sum has finitely many nonzero coordinates. The word summands are independent, so the projections recover those coordinates uniquely. A finite set of finite word lengths has a finite maximum, with the stipulated convention for empty support. $\square$

The substantive modelling work is to supply $\rho_A$ and its adequacy conditions. Once its codomain is the algebraic direct sum, finite support is a consequence of that choice, not an empirical discovery.

The actualisation chain is therefore

$$
\begin{aligned}
\mathsf{Orthing}_A
&\leadsto (\rho_A:E_A\to T_{\mathcal T}(V))\\
&\leadsto e\in E_A
\leadsto S_A(e)
\leadsto\sum_{w\in S_A(e)}j_wc_{A,w}(e).
\end{aligned}
$$

No single infinite tensor is being collapsed. The representation language can admit words of every finite length. A particular analysis may restrict that language, and the actual range of $\rho_A$ may be bounded even when the ambient language is not. Thus neither $\sup_eN_A(e)=\infty$ nor the necessity of arbitrarily large degree has been proved.

## Degree, size, rank, and audit level

Adding a second evidence–claim pair can increase the number of coefficients within one degree-two component without changing its degree. A new three-way dependency can introduce degree three. Conversely a discharge can change a status coefficient while leaving all degrees unchanged.

Tensor order counts factors in a chosen factorisation; tensor rank counts the number of simple tensors needed in a decomposition. Neither is the number of stored facts. Audit level, number of players, derivative order in a Sobolev estimate, and frequency scale in a PDE are separate indices. Any correspondence between them is additional structure, not a consequence of the word “order”.

# A concrete representation of the episode record

## A faithful record channel

Let $\mathscr D_A$ be the declared finite-record domain. Specify a canonical finite atomisation $\operatorname{At}(d)$: each atom records a typed field path and value, including container markers and indices for ordered sequences. References are represented by their typed identifiers and versions. Assume atomisation is injective on $\mathscr D_A$. This can be implemented for finite structured records by recording the node kind at every path, every leaf value with its scalar type, and every list index. Map key order is either normalised or explicitly represented according to the contract.

Let $X_{\rm rec}$ be the set of possible atoms and let

$$
V_{\rm rec}=\mathbb R^{(X_{\rm rec})}
$$

be the free vector space with basis $[a]_{\rm rec}$. Define

$$
\eta_A(d)=\sum_{a\in\operatorname{At}(d)}[a]_{\rm rec}.
$$

Different occurrences have distinct paths or explicit occurrence identifiers. An actual repeated list value therefore does not disappear through set deduplication. The entire record channel has tensor degree one, even if the record is large. This deliberately demonstrates why degree is not intrinsic record complexity.

## An interaction channel

Let $\Lambda_A$ be a registry of relation signatures. A signature $\lambda$ specifies an arity $n_\lambda$ and an ordered list of argument types. Give each argument role its own tagged type $(\lambda,j,\tau_{\lambda,j})$. Tagging keeps different relations with the same argument sorts from being conflated.

For every episode, a declared extractor produces a finite set $\mathscr I_A(e)$ of interaction occurrences. An occurrence $r$ has signature $\lambda(r)$, values $v_{r,1},\ldots,v_{r,n_r}$, an occurrence identifier, and a coefficient $a_r$. Define

$$
\iota_A(e)=\sum_{r\in\mathscr I_A(e)}a_r
\bigotimes_{j=1}^{n_r}[r,v_{r,j}]_{(\lambda(r),j,\tau_{\lambda(r),j})}.
$$

The occurrence identifier is basis metadata, not an extra semantic argument. Keeping it in the role labels preserves shared incidence across factors. It may be omitted only if the resulting loss of multiplicity or identity is acceptable for the declared task. The selected relations must be justified by the analysis; this construction does not manufacture them from co-occurrence.

Include the record type in $\mathcal T$ but exclude it from the interaction-role types. Then define the proposed map

$$
\boxed{\rho_A(e)=\eta_A(\xi_A(e))+\iota_A(e).}
$$

**Proposition 4.1 — Faithfulness to the declared finite view.** Under Assumption F and injective atomisation, $\rho_A(e)$ is algebraically well-defined and has finite word support. It determines $\xi_A(e)$ exactly. If $\xi_A$ is injective on the selected episode domain, then $\rho_A$ is injective on that domain.

*Proof.* Both sums have finitely many finite tensors. Projection to the distinguished record summand recovers $\eta_A(\xi_A(e))$. Independence of the record basis recovers every retained atom. Injective atomisation reconstructs the record view. If that view separates episodes, so does the representation. $\square$

This is a preservation construction, not a compression result. The basis can be large or infinite across episodes; equality of referenced identifiers does not authenticate their referents. Encoding records injectively supplies no independent test of source truth, efficient computation, predictive gain, or faithful modelling of a worldly process.

## Example: one finite episode view

Consider a synthetic record with one claim $q$, two evidence items $h_1,h_2$, an actor $a$, a case-bound configuration $\bar\mu$, a route $r$, and an unresolved obligation $b$. Suppose the declaration extracts supports, assessments, and route-authorisation interactions:

$$
\begin{aligned}
\rho_A(e)=\eta_A(\xi_A(e))
&+[h_1]\otimes[q]+[h_2]\otimes[q]\\
&+[a]\otimes[h_1]\otimes[q]\\
&+[\bar\mu]\otimes[h_1]\otimes[q]\otimes[r].
\end{aligned}
$$

The role tags and occurrence IDs are suppressed only for readability. The degree profile is $\{1,2,3,4\}$. The two support edges share one typed-word component. The unresolved status of $b$ remains in the record channel; the displayed tensor does not claim $q$ true or $b$ resolved.

This is an explicit instance of finite-support actualisation, not an encoding of the entire present chat and not a submitted repository episode.

## When a compressed representation is adequate

**Theorem 4.2 — Fibre criterion for preserving a target.** Let $D$ be any set, $r:D\to Y$ a representation, and $q:D\to Z$ a declared observable. There exists a decoder $\bar q:r(D)\to Z$ with

$$q=\bar q\circ r$$

if and only if

$$r(d)=r(d')\quad\Longrightarrow\quad q(d)=q(d')$$

for all $d,d'\in D$.

*Proof.* Factorisation makes $q$ equal on every fibre of $r$. Conversely define $\bar q(y)$ to be the unique value of $q$ on $r^{-1}(\{y\})$. Each such fibre is nonempty for $y\in r(D)$, and fibre constancy makes the definition unambiguous. $\square$

For a family of required observables, apply the theorem to their product. This is an elementary set-theoretic factorisation criterion, not a new general theorem. In Orthemology it gives an exact meaning to “this representation retains the distinctions needed for this assessment”. It does not prove that the declared observable is the correct one for the world.

**Corollary 4.3 — Representation transport.** A compression $c:r(D)\to Y'$ preserves $q$ exactly when $q$ is constant on fibres of $c\circ r$. Calling $c$ a contraction, projection, summary, or neural embedding does not settle this condition.

## Change of basis and semantic composition

For linear isomorphisms $g_\tau:V_\tau\to V'_\tau$, the direct-sum map induces

$$
T(g)|_{V_w}=g_{\tau_1}\otimes\cdots\otimes g_{\tau_n}.
$$

It preserves each word type and degree. A representation change is equivariant when $\rho'_A=T(g)\rho_A$ on the admitted domain. Basis relabellings satisfy this equation for the free-basis construction. Arbitrary semantic relabellings do not become justified merely because a linear isomorphism exists.

To represent a workflow composition $e\circ f$ by tensor multiplication, one would additionally need

$$\rho_A(e\circ f)=\rho_A(e)\rho_A(f)$$

where that composition is defined, or an explicitly specified alternative intertwining law. Shared evidence, aliasing, authority constraints and duplicate obligations can prevent naive concatenation from having that meaning. The construction above makes no blanket homomorphism claim.

# Higher-order information: a precise role for tensors

The repository's repaired T300 uses parity to show that lower-order marginal profiles can miss a declared higher-order target [R3]. The following proof makes its tensor mechanism explicit.

**Theorem 5.1 — Proper marginals can miss the entire parity distinction.** For any $n\geq2$, define distributions on $\{0,1\}^n$ by

$$
P_\pm(x)=2^{-n}\bigl(1\pm(-1)^{x_1+\cdots+x_n}\bigr).
$$

They are uniform on the even and odd parity classes respectively. Every proper-subset marginal of $P_+$ equals the corresponding marginal of $P_-$. Nevertheless their parity expectations are $+1$ and $-1$.

*Proof.* If a coordinate is summed out, the two terms of the alternating sign cancel. Thus for every proper $J\subsetneq\{1,\ldots,n\}$, the marginal is the uniform distribution $2^{-|J|}$. The sign $(-1)^{\sum x_i}$ is constantly $+1$ on the support of $P_+$ and $-1$ on the support of $P_-$. $\square$

Let $v_0,v_1$ be the basis of $\mathbb R^2$. Regard a distribution as its coefficient tensor. Then

$$
P_+-P_-=2^{1-n}(v_0-v_1)^{\otimes n}.
$$

Marginalisation in coordinate $j$ is contraction against the augmentation covector $\varepsilon(v_0)=\varepsilon(v_1)=1$. Since $\varepsilon(v_0-v_1)=0$, every proper marginal annihilates the difference. By contrast the covector $\psi(v_0)=1$, $\psi(v_1)=-1$ detects it through $\psi^{\otimes n}$.

**Corollary 5.2 — No fixed marginal order is universally sufficient in this class.** For any finite $r\geq0$, choose $n>\max\{r,1\}$. No decoder using only marginals of order at most $r$ can recover parity for both distributions.

*Proof.* Their represented marginal data agree while their target values differ. Apply Theorem 4.2. $\square$

Three restrictions are essential. The construction is a standard higher-order interaction example, not general mathematical novelty. It is not a theorem that real episodes require globally unbounded degree. And it does not rule out a target-specific low-dimensional representation: a single parity statistic is sufficient for the parity target. In fact the displayed difference tensor has tensor rank one while having order $n$. Large interaction order is not large tensor rank.

The defensible conclusion is conditional: **if the declared representation is restricted to lower-order marginals, consequential higher-order information can be lost.** Whether tensors outperform relations, hypergraphs, text, or other representations remains a separate question. The repository's representation programme is not promoted by this example [R4].

# Witnessed revision and degree-lowering

## Algebraic degree shifts

Let $H=\bigoplus_{n\geq0}H_n$ be a graded vector space. A linear map $D_k:H\to H$ has degree $k\in\mathbb Z$ when $D_k(H_n)\subseteq H_{n+k}$, interpreting negative-index spaces as zero.

**Proposition 6.1 — Local finiteness of degree-shift decomposition.** Every linear map $D:H\to H$ has the pointwise decomposition

$$
D=\sum_{k\in\mathbb Z}D^{[k]},\qquad
D^{[k]}(v)=\sum_{n\geq0}P_{n+k}D(P_nv).
$$

For each fixed $v\in H$, only finitely many summands contribute. Conversely, an arbitrary proposed family $(D_k)$ defines a map $H\to H$ by this sum only when it is pointwise locally finite, or when some separately declared convergence/completion structure makes sense of an infinite sum.

*Proof.* The vector $v$ has finite input-degree support. Each $D(P_nv)$ has finite output-degree support because it belongs to $H$. The finite union of these output supports gives only finitely many differences $k$ between input and output degrees. Summing all corresponding projections recovers $D(v)$. For the converse, without local finiteness the proposed sum need not be an algebraic direct-sum element. $\square$

A state-dependent revision need not be linear. A witnessed rewrite, branch, conditional gate, or schema update is more generally a partial map or relation on admissible encoded states. The linear degree-shift decomposition applies only after linearity has actually been established.

## There is no structure-free, nonzero deletion functional

For a covector $\varphi\in V_{\tau_j}^*$ there is a well-defined contraction

$$
C_{j,\varphi}(v_1\otimes\cdots\otimes v_n)
=\varphi(v_j)
 v_1\otimes\cdots\widehat{v_j}\cdots\otimes v_n.
$$

The hat denotes omission. The choice of $\varphi$ is substantive.

**Proposition 6.2 — No nonzero covector invariant under all basis changes.** If $W$ is a real vector space and $\ell:W\to\mathbb R$ is linear with $\ell\circ g=\ell$ for every $g\in\operatorname{GL}(W)$, then $\ell=0$.

*Proof.* Take $g=2\operatorname{id}_W$. Then $2\ell=\ell$, so $\ell=0$. $\square$

A free vector space on a specified set does have a distinguished augmentation $[x]\mapsto1$ relative to that basis. Probability marginalisation uses precisely such added structure. The proposition forbids structure-free deletion; it does not forbid useful, declared contractions.

**Counterexample 6.3 — Contraction is not sufficient for warranted discharge.** Let $d_0,d_1$ be different basis vectors, with $\varphi(d_0)=\varphi(d_1)=1$. Contraction maps both $v\otimes d_0$ and $v\otimes d_1$ to $v$. If a required observable distinguishes the two evidence states, it no longer factors through the contracted representation. Thus even a perfectly linear contraction can erase a consequential distinction. Theorem 4.2, not the name of the operator, decides target preservation.

## Active state is not the historical ledger

Represent a governed runtime state by

$$z=(x,B,\mathscr H),$$

where $x$ is its active represented state, $B$ its current obligation records, and $\mathscr H$ its retained history. A transition has an explicit witness

$$z\xrightarrow{h}_A z'.$$

The witness records input/output identities and versions; governing analysis and representation versions; the operation and any contraction/evaluation parameters; its authority; evidence and certificate references; treatment of affected obligations; required preserved observables; and the post-operation reread/disposition. This is a proposed mathematical interface aligned with the repository's transition-witness discipline [R5]. It is not an assertion that a record bearing those field names is valid evidence.

**Definition 6.4 — Coverage and retention.** A witness is *record-valid* when:

1. every old obligation remains addressable in the new history with its identity and previous status;
2. each old live obligation either persists live, is replaced by explicitly linked successor obligations, or has an explicit authorised disposition;
3. resolution has a referenced resolution certificate, transfer has a destination and transfer witness, and supersession has a lineage witness;
4. history is extended rather than silently overwritten; all mandatory hard constraints and declared preservation checks are met.

“Deferred”, “owner-assigned”, “risk-accepted”, and “transferred” are not synonyms for “proved resolved”. An obligation may leave the local active set while remaining live elsewhere. A discharge witness must retain that distinction.

*Semantic validity* additionally requires the substantive truth and applicability of the witness's claims. A shape check cannot produce that truth. We write $\operatorname{RecValid}_A(h)$ and $\operatorname{SemValid}_A(h)$ separately.

**Theorem 6.5 — Compositional no-disappearance invariant.** Suppose a finite transition sequence $z_0\xrightarrow{h_1}_A\cdots\xrightarrow{h_m}_Az_m$ has record-valid witnesses. Every obligation recorded at $z_0$ remains addressable in $z_m$'s retained history and has a traceable chain of persistence, replacement, or disposition. If each substantive disposition is also semantically valid, the chain contains no unwarranted disposition relative to the declared contract.

*Proof.* The one-step claim is the coverage-and-retention condition. If an obligation persists or has successors, the next witness covers those current records while retaining their predecessor links. If it was terminally dispositioned, the historical entry and its witness are retained. Induction on the finite sequence gives addressability and a finite lineage chain. The semantic conclusion uses the semantic validity of each link, not merely its presence. $\square$

## A witnessed degree-lowering map

A local active reduction may be modelled by

$$
(x,B,\mathscr H)\longmapsto
\bigl(C_{j,\varphi}x,B',\mathscr H\mathbin{\|}(h,x,B)\bigr),
$$

on a guarded domain where the old active object and witness can be retained or referenced faithfully. The concatenation symbol denotes history extension. If the tensor $x$ records a claim together with an evidence factor, the active view may contract that factor after the claim's permitted disposition is established. The old evidence remains in history or in an authenticated referenced artifact.

The active tensor degree can decrease while the full episode-record representation grows. This is not a contradiction: active simplification and historical preservation are different operations. Nor is a changed obligation status inherently a degree change. The same typed relation can persist with a new status coefficient. “Degree-lowering” denotes the effect of a chosen representation operation, not an intrinsic measure of epistemic improvement.

# Inquiry landscapes and closure externalities

## Historical ecology, current state, and prospective inquiry

Let $\mathscr Z_A$ be a declared environment-state space, distinct from any optional latent-model state space. A state $z$ may include the current record, publicly available information, access rights, resources, governing configuration, and historical ecology. Let

$$\gamma_A:\mathscr Z_A\to\mathscr G_A^\mu$$

extract its historical ecology graph. Its codomain contains the kinds of typed nodes and edges described by the repository's ecology model [R6].

Independently, let $\mathscr J_A$ be a universe of finitely described inquiry structures. An element $q\in\mathscr J_A$ can be a next action or a bounded contingent inquiry plan; the interpretation is fixed by $A$. Specify a feasibility predicate

$$\operatorname{Feas}_A(z,q)\in\{0,1\}$$

covering the relevant resource, authority, dependency, information-access and timing conditions. Define

$$
\boxed{\mathcal L_A(z)=\{q\in\mathscr J_A:\operatorname{Feas}_A(z,q)=1\}.}
$$

Thus $\Gamma_t^\mu=\gamma_A(z_t)$ is retrospective/historical structure and $\mathcal L_t=\mathcal L_A(z_t)$ is prospective feasibility. They are different object types. A sufficiently detailed ecology model plus additional rules may help compute a landscape; the distinction does not demand statistical or logical independence between them.

The total landscape can be infinite even when each inquiry structure has finite support. An agent's estimate $\widehat{\mathcal L}_{A,\alpha,t}$ is a further object: limited knowledge of which inquiries are feasible is not identical to actual feasibility.

## Supports do not determine feasible inquiry

One can attach to every $q$ a finite typed support $\operatorname{sh}_A(q)$. But $\mathcal L_A(z)$ is not in general recoverable from the set of available degrees or supports. Two inquiries can have the same typed shape and different evidence, recipients, costs, authorisations, or outcomes.

**Proposition 7.1 — Shape alone need not determine admissibility.** There are states $z$ and inquiries $q_1,q_2$ with $\operatorname{sh}_A(q_1)=\operatorname{sh}_A(q_2)$ but $q_1\in\mathcal L_A(z)$ and $q_2\notin\mathcal L_A(z)$.

*Proof.* Take two identically shaped source-access inquiries. Let one source be accessible under the state's permission record and the other require an absent permission. The shape is the same and the feasibility predicate differs. $\square$

Accordingly the landscape is a constrained set of inquiry objects, potentially decorated by supports; it is not merely a set of grades. It is not assumed closed under addition. Two separately feasible inquiries may jointly exceed a resource limit.

## Landscape evolution with a fixed analysis

Let $F_A:\mathscr Z_A\times\mathscr A_A\rightrightarrows\mathscr Z_A$ be a declared state-transition relation. An executed closure action $a_e$ gives some $z'\in F_A(z,a_e)$. It then induces

$$
\bigl(\gamma_A(z),\mathcal L_A(z),e\bigr)
\longmapsto
\bigl(\gamma_A(z'),\mathcal L_A(z'),e'\bigr).
$$

The episode $e'$ is an explicitly related successor episode or record version, not an erasure of the identity of $e$. The notation leaves $A$ fixed. A change to the analysis is a separately recorded transition and may require its own transport conditions.

Under a fixed universe of identified inquiry objects, set

$$
C_e=\mathcal L_A(z)\setminus\mathcal L_A(z'),\qquad
N_e=\mathcal L_A(z')\setminus\mathcal L_A(z).
$$

Then the identity

$$\mathcal L_A(z')=(\mathcal L_A(z)\setminus C_e)\cup N_e$$

is exact. It is bookkeeping, not by itself evidence that $e$ caused every difference, that a difference is harmful, or that the identity of an inquiry survives a changed information state. Causal attribution needs a comparison of alternative transitions from the same relevant pre-state.

Publishing a theorem may end the opportunity for a particular actor to discover it independently *before seeing that disclosure*. It does not prohibit learning the proof, discovering another proof, extracting its mechanism later, or opening new problems. This is the bounded interpretation of the resource concern supplied in the screenshot [C2], not a literal axiom that mathematics has a finite non-renewable stock.

## Assessing value without equating it with cardinality

Fix a horizon $h$, an admissible inquiry-plan subset $\mathscr J_A^h$, and a bounded value functional $J_A(z,q)$. Include a stop option of value zero. Define

$$
\operatorname{Opt}_{A,h}(z)
=\sup\bigl(\{0\}\cup
\{J_A(z,q):q\in\mathcal L_A(z)\cap\mathscr J_A^h\}\bigr).
$$

The horizon, costs, uncertainty and whose interests are counted belong to the declaration. With multi-objective or incomparable values, retain a partial order or attainable-value set rather than inventing a scalar ranking.

For alternative closure actions $a$ and $b$ from the same state, one useful declared comparison is

$$
\operatorname{Tot}_{A,h}(z,a)
=R_A^{\rm imm}(z,a)+\operatorname{Opt}_{A,h}(F_A(z,a)),
$$

when the transition is single-valued. A stochastic or set-valued transition requires a declared expectation, worst-case, or other comparison rule. Neither this scalar nor landscape size replaces hard admissibility constraints.

**Proposition 7.2 — Result correctness does not determine future option value.** There exists a finite model with two admissible closure actions, both producing the same correct theorem, but different post-closure option values. The difference can have either sign relative to the pre-state.

*Proof.* Let the initial inquiry landscape contain an independent-discovery option of value $6$. Let a thin closure and an expository closure both establish the same true result. After the thin closure, only a reconstruction option of value $2$ is available. After the expository closure, a transferable-mechanism option of value $10$ is available. Assign both actions the same immediate reward and make both admissible. Correctness is identical, while option value changes by $-4$ and $+4$. Relabelling the two post-states reverses their ordering without changing correctness. $\square$

This is a constructed countermodel, not a measured claim about the authors, the research community, or AI-assisted mathematics. The screenshot motivates the question; it does not supply the values.

**Proposition 7.3 — Landscape contraction is not necessarily harm.** There are strict inclusions $\mathcal L_A(z')\subsetneq\mathcal L_A(z)$ with equal option value; there are also landscapes with fewer inquiries but greater option value.

*Proof.* Removing an option valued below a retained maximiser leaves the supremum unchanged. For the second claim, replace any number of low-value alternatives by one higher-value option. $\square$

Closing a refuted route can improve inquiry by removing waste. The normative task is not to preserve the maximum number of open possibilities; it is to assess the consequences of closure under the declared values and constraints. A result-correct closure and an epistemically valuable closure are separately assessable, but no universal value ordering is derived here.

# The optional strategic layer

## A game declaration is additional structure

The frozen strategic hierarchy is retained:

$$
\begin{aligned}
\rho_A(e)
&\xrightarrow{\text{additional strategic declaration}}
G_A(e;\mathcal L)\\
&\leadsto\prod_{i\in I}\Delta(S_i)
\leadsto BR_A
\leadsto NE_A(e;\mathcal L).
\end{aligned}
$$

The first arrow is not a consequence of tensor structure. It records a modelling act. Non-strategic factors such as evidence and obligations do not become players. Nor must one first tensorise an episode in order to define a game.

**Definition 8.1 — Finite strategic declaration.** A declaration specifies a nonempty finite player set $I$, nonempty finite strategy sets $S_i$, and finite real payoff functions $U_i:\prod_jS_j\to\mathbb R$. It also identifies which contextual data determine these objects, which informational assumptions justify the chosen normal form, and how payoffs are interpreted.

We write $G_A(e;\mathcal L)$ when those data are determined by the displayed arguments together with the fixed declaration. Otherwise use the fuller environment argument $G_A(e;z)$. By Theorem 4.2, replacing $z$ by only $(e,\mathcal L_A(z))$ is licensed exactly when the game data are constant on those fibres. A landscape's admissibility set alone need not determine payoffs.

A finite extensive-form or Bayesian situation can sometimes be converted to a finite normal form by taking complete contingent plans as strategies. In that case the information structure must be preserved in the construction and its provenance; it is not absent simply because the final normal form stores only strategy sets and payoffs. Bare action labels generally do not reconstruct that structure.

## Cartesian strategy product versus tensor product

Enumerate $S_i=\{s_{i1},\ldots,s_{im_i}\}$ and let $P_i=\mathbb R^{S_i}$ be the vector space with basis $[s_i]$. Pure configurations lie in the Cartesian product $\prod_iS_i$, not in a tensor product by definition. There is, however, the multilinear embedding

$$
(s_1,\ldots,s_n)\longmapsto[s_1]\otimes\cdots\otimes[s_n].
$$

The payoff array is naturally a covariant tensor

$$
U_i\in\bigotimes_{j=1}^nP_j^*\cong
\mathbb R^{m_1\times\cdots\times m_n}
$$

after the strategy bases are chosen. Mixed strategies satisfy $p_i\in\Delta(S_i)$, and independent mixing produces the probability tensor $p_1\otimes\cdots\otimes p_n$. The expected payoff is

$$
\begin{aligned}
u_i(p)&=\langle U_i,p_1\otimes\cdots\otimes p_n\rangle\\
&=\sum_{s\in\prod_jS_j}U_i(s)\prod_jp_j(s_j).
\end{aligned}
$$

Here the tensorial law genuinely does work: expectation is multilinear in the independently mixed strategies. A general joint distribution need not factor this way; correlated play is different structure.

## Joint feasibility must not be silently lost

The finite normal-form theorem requires fixed, nonempty, individual strategy sets and defined real payoffs for every joint profile. But Orthemology's hard constraints can couple players.

**Counterexample 8.2 — Individually admissible choices can violate joint constraints.** Two actors each choose whether to use a single exclusive resource. Each has choices $\{0,1\}$, while feasible joint choices are

$$F=\{(0,0),(1,0),(0,1)\}.$$

Independent mixed strategies with both actors choosing $1$ with positive probability assign positive probability to forbidden $(1,1)$.

To apply the finite-game result without violating a hard constraint, exhibit a product of strategy sets contained in the feasible region, or explicitly represent a protocol/allocator that makes all joint choices well-defined and admissible. Alternatively analyse a constrained or generalised game with its own existence conditions. Merely attaching a large finite penalty to a forbidden outcome does not make the outcome impossible or authorise it.

## Mixed Nash existence

For $p\in\mathcal P:=\prod_i\Delta(S_i)$, define

$$
BR_i(p_{-i})=
\operatorname*{arg\,max}_{q_i\in\Delta(S_i)}u_i(q_i,p_{-i}),
\qquad BR(p)=\prod_iBR_i(p_{-i}).
$$

**Theorem 8.3 — Conditional finite-episode Nash theorem.** Every game satisfying Definition 8.1 has a nonempty compact set of mixed Nash equilibria

$$NE_A(e;\mathcal L)=\{p\in\mathcal P:p\in BR(p)\}\neq\varnothing.$$

*Proof.* The finite product $\mathcal P$ is nonempty, compact and convex. Expected payoffs are continuous and affine in a player's own mixture. Hence each best-response set is nonempty, compact and convex. Its graph is closed: if opponents' profiles and best responses converge, the defining payoff inequalities pass to the limit by continuity. Compactness of the codomain gives upper hemicontinuity. The product correspondence therefore satisfies Kakutani's fixed-point theorem. Its fixed-point set is closed in compact $\mathcal P$, hence compact. $\square$

This is the standard Nash–Kakutani argument [M2–M3], applied conditionally to the declared finite game. It is not a new existence theorem. Pure equilibria need not exist, equilibria need not be unique, and the proof supplies neither an equilibrium-selection rule nor a convergence theorem for play.

No universal player count is required. The result is applied separately to each declared finite game. Nonempty strategy sets matter: an empty action set does not give a nonempty simplex. Infinite action sets require appropriate additional assumptions; some continuous finite-dimensional settings still use Kakutani, while other settings require extensions.

## Equivariance and quantitative certificates

**Proposition 8.4 — Strategic relabelling invariance.** Bijective strategy relabellings transport Nash equilibria bijectively. The same holds if, in addition, each player's payoff is transformed by a positive affine map $u'_i=a_iu_i+b_i$, with $a_i>0$.

*Proof.* Relabellings biject the available unilateral deviations. Positive affine transformations preserve every comparison between a player's payoff and that player's unilateral-deviation payoff. Thus the Nash inequalities hold before the transformation exactly when they hold after it. $\square$

This does not identify payoff adequacy with mathematical invariance. Whether the scoring rule represents legitimate interests remains outside the relabelling theorem.

Define player $i$'s unilateral regret by

$$
\operatorname{Reg}_i^U(p)=
\max_{s_i\in S_i}u_i(s_i,p_{-i})-u_i(p).
$$

It is nonnegative, and $p$ is Nash exactly when all regrets vanish. Pure deviations suffice because mixed-deviation payoffs are convex combinations.

**Proposition 8.5 — Robust regret transport.** Let two games on the same finite strategy product satisfy

$$\max_s|U_i(s)-\widetilde U_i(s)|\leq\varepsilon_i.$$

If $\operatorname{Reg}_i^{\widetilde U}(p)\leq\delta_i$, then

$$\operatorname{Reg}_i^U(p)\leq\delta_i+2\varepsilon_i.$$

*Proof.* Every mixed payoff changes by at most $\varepsilon_i$, because it is an average of entries. The deviating payoff can increase by at most $\varepsilon_i$, and the current payoff can decrease by at most $\varepsilon_i$. Take the maximum over deviations. $\square$

This is one explicit bridge from a certified surrogate payoff tensor to an approximate equilibrium claim. It does not imply that the exact equilibrium tuple varies continuously or that a learned payoff tensor models real preferences correctly.

## Equilibrium change with the analysis fixed

**Proposition 8.6 — Publication can change equilibrium through feasibility alone.** There is a fixed analysis and a finite two-player family in which a result-correct publication changes the strategy sets and hence the equilibrium, without changing the analysis.

*Proof.* The analysis declares a public state bit $k$ indicating whether the theorem is disclosed. Each researcher has strategies $D$ (independent pre-disclosure discovery) and $S$ (stop). When $k=0$, both are admissible and payoffs are $1$ for $D$ and $0$ for $S$, independently of the other player. The unique equilibrium is $(D,D)$. A correct publication sets $k=1$, making $D$ inadmissible by its declared meaning, while $S$ remains. The unique equilibrium is now $(S,S)$. The player definitions, feasibility rule and payoff rule remain fixed; the environment state changed. $\square$

Comparison of these equilibria uses the common strategy labels $\{D,S\}$, extending mixtures by zero on unavailable strategies. If player sets also change, comparisons require explicit player/strategy transport maps or a tagged common ambient space. Raw inequality between equilibrium sets of different types is not a meaningful structural comparison.

Landscape change **can**, but need not, change the game; game change **can**, but need not, change equilibrium. An inaccessible source unrelated to all strategic choices may leave the game unchanged. Removing a strictly dominated unused option can leave its equilibrium unchanged.

## A publication-race countermodel

For a second synthetic example, two players choose rapid disclosure $F$ or mechanism-rich exposition $E$. Let the payoff pairs be

| Player 1 / Player 2 | $F$ | $E$ |
|:--|:--:|:--:|
| $F$ | $(2,2)$ | $(5,0)$ |
| $E$ | $(0,5)$ | $(4,4)$ |

For either opponent action, $F$ is strictly better individually. Hence $(F,F)$ is the unique mixed as well as pure equilibrium, although $(E,E)$ gives both players a larger payoff. Declare every outcome to publish the same correct theorem, and separately let $J_A(E,E)=10$ and $J_A(F,F)=2$ represent future mechanism value. The example separates truth, private incentives, and prospective inquiry value.

These numbers are illustrative, not empirical estimates or imputations of motive to Tao, Buckmaster, Alpöge, or any other researcher. A Nash equilibrium is not warrant, moral approval, pathway adequacy, scientific adoption, or a prediction that these choices will occur.

The dialogue itself has no declared payoff functions or contingent strategy sets. This example does not retroactively turn the dialogue into an observed Nash game.

# Warrant transport and heterogeneous proof pipelines

## A conditional theorem is not its instantiated conclusion

Let $P_1,\ldots,P_m$ be hypotheses and let $Q$ be a conclusion. A checked derivation of

$$P_1\land\cdots\land P_m\Longrightarrow Q$$

is a different artifact from certificates establishing the $P_j$ for a particular target. The scoped inference to $Q$ needs both, with matching target, model, version, domain and interpretation. A list of checked algebraic lemmas does not imply that all hypotheses of a PDE existence theorem have been discharged.

The uploaded Euler manuscript explicitly separates an approximate profile, a conditional stability framework, remaining numerical certifications, and a continuation/reconstruction requirement [F1, pp. 13–15, 48–55]. Its proof of an invariant energy ball applies while an admissible solution exists and the estimates remain valid. The manuscript itself notes that all-time rescaled existence needs a separate local well-posedness and continuation argument [F1, pp. 52–53]. These qualifications are retained here.

**Definition 9.1 — A scoped bridge record.** A bridge identifies its input artifact and output claim, exact object versions, mathematical relation, error bounds if applicable, hypotheses, discharged certificates, and remaining obligations. An unverified bridge is an obligation, not an arrow carrying completed warrant.

## A simple robust transport theorem

**Proposition 9.2 — Margin transport across a surrogate.** Let $(X,d)$ be a metric space, let $f:X\to\mathbb R$ be $K$-Lipschitz, and suppose a surrogate $s$ and target $x$ satisfy $d(x,s)\leq\epsilon$. If a certified evaluation gives

$$f(s)\geq m-\eta,$$

then

$$f(x)\geq m-\eta-K\epsilon.$$

In particular $f(x)>0$ if $m>\eta+K\epsilon$.

*Proof.* The Lipschitz bound gives $f(x)\geq f(s)-Kd(x,s)$. Substitute the certified bounds. $\square$

A small representation error alone does not preserve an arbitrary predicate: the sign predicate at zero is an immediate counterexample when no positive margin is available. A contraction or conversion requires a property-specific stability argument.

## Discovery and certification need not target the same object

The diagram on page 33 of the uploaded paper separates PINN discovery, spline representation, interval certificates and the stability proof. A key detail is that the spline becomes the reference object on which residuals and analytic constants are evaluated [F1, pp. 31–33].

Accordingly the logical pattern can be

$$
\begin{aligned}
\text{network proposes }s
&\leadsto\text{ certified properties of }s\\
&\leadsto\exists x\text{ satisfying the target equations near }s.
\end{aligned}
$$

It need not be “prove a theorem about the spline and transport it back to make the original neural network an exact solution”. Certification may bypass the network entirely once the explicit candidate has been selected. If the claim instead concerns the original network, an appropriate network-to-surrogate bound is required.

This distinction repairs an over-broad suggestion in the dialogue. The transferable mechanism is **untrusted or opaque search followed by independently checkable explicit certificates**, not a blanket licence to identify the searched object, the certified object, and the object whose existence is concluded.

# Dynamical mechanisms: what can be transferred mathematically

## Source scope and the Navier–Stokes motivation

The supplied Tao excerpts describe a low-to-high-frequency amplification programme for smoothly forced fluid equations and distinguish extraction of mathematical mechanisms from merely obtaining another result [C3]. The present work does not verify the Alpöge–Buckmaster proofs or their Lean dependency closure. The public `fluid_lean` repository was located, but no full build or theorem-to-paper audit was performed [F3]. The NYU PDFs could not be retrieved for full review in this execution.

The separately uploaded Ganeshram–Duruisseaux–Anandkumar manuscript supplies the directly inspected source for rescaling, optimised weights, two-level estimates, local concentration, and the conditional invariant-ball argument [F1]. Its public author announcement presents the unforced Euler construction as evidence and a route towards a proof, not a completed Navier–Stokes theorem [F2]. Nothing below depends on a claim that either programme has solved Navier–Stokes.

One source-based correction to the earlier discussion is important: the official Clay problem has zero-forcing global-existence alternatives and breakdown alternatives permitting smooth forcing with specified decay conditions. Thus “only an unforced Navier–Stokes result could qualify” would be too strong. A forced Euler theorem is nevertheless not a Navier–Stokes theorem, and an arbitrary smooth force does not automatically satisfy the Clay conditions [F4, pp. 1–2].

The mechanisms below are mostly standard analysis reorganised for this proposed interface. Their relevance does not require waiting for an NS solution. A future successful solution could supply sharper or more general estimates, but its added contribution would have to be identified rather than presumed.

## A dynamical realisation is an extra declaration

The repository's G1 describes governed, feasibility-first, order-theoretic correction. Its G2 refers specifically to literal differentiable gradient-flow structure and remains conditional [R7]. A literal dynamical system need not be a gradient flow. Developing one is not automatically a G2 promotion in the repository's narrower sense.

For a bounded subsystem, a possible realisation is a hybrid state space

$$\mathscr X_A=\coprod_{\sigma\in\Sigma_A}X_\sigma,$$

where $\sigma$ labels a declared finite support/structural regime and $X_\sigma$ is a finite-dimensional domain of coefficients. Within a regime,

$$\dot x=F_\sigma(x,\vartheta),\qquad
\dot\vartheta=\epsilon_{\rm time}H_\sigma(x,\vartheta),$$

while witnessed reset maps implement discrete changes of structure. The archive and the environment state remain explicit. This is only one candidate mathematical realisation; it does not require treating every episode as continuous or finite-dimensional.

To instantiate it, supply the state interpretation, admissibility region, vector fields, regularity and existence assumptions, guards, reset witnesses, time interpretation, observables and modelling-error bounds. A general vector field is not $-\nabla V$ unless a metric and potential actually make that identity hold. A partial order is not automatically a differentiable potential.

## Coupled-energy control

The uploaded manuscript combines low-order damping with high-order control rather than requiring either estimate alone to control every term [F1, pp. 49, 56, 65–67]. The following abstract lemma extracts that mechanism without importing its PDE-specific coefficients.

**Theorem 10.1 — Two-level damping criterion.** Let $X(t),Y(t)\geq0$ be differentiable and suppose

$$
\frac12\dot X\leq-aX+bY,\qquad
\frac12\dot Y\leq cX-dY,
$$

where $a,d>0$ and $b,c\geq0$. There exists $\lambda_E>0$ such that $V=X+\lambda_EY$ has a strict estimate

$$\frac12\dot V\leq-\gamma V\quad\text{for some }\gamma>0$$

by this combination of bounds whenever $ad>bc$. More precisely, a weight with both resulting coefficients positive exists **if and only if** $ad>bc$; for any such weight one can take

$$\gamma=\min\{a-\lambda_Ec,\ d-b/\lambda_E\}.$$

*Proof.* Addition gives

$$\tfrac12\dot V\leq-(a-\lambda_Ec)X-(\lambda_Ed-b)Y.$$

Both coefficients are positive exactly when $\lambda_E>b/d$ and, if $c>0$, $\lambda_E<a/c$. With $c>0$ this interval is nonempty exactly when $ad>bc$. If $c=0$, any $\lambda_E>b/d$ works and $ad>bc=0$ already holds. The displayed minimum gives the claimed comparison with $V$. $\square$

Integrating yields $V(t)\leq e^{-2\gamma t}V(0)$ on the interval of validity. If a model also requires $\lambda_E\leq1$, the feasible interval must intersect $(0,1]$; that restriction is not implied by $ad>bc$.

This is a conditional design criterion for coupled diagnostics. It is not permission to compensate for a violated hard constraint by improving a different score. Analytic error terms can be absorbed in an estimate; missing authority or concealed evidence remains inadmissible.

## Residuals impose a nonzero error scale

**Theorem 10.2 — Certified invariant error ball.** Let $E(t)\geq0$ be continuous, with $E(t)^2$ differentiable, and suppose throughout an admissible regime, including any first boundary-contact state,

$$\frac12\frac{d}{dt}E^2\leq-aE^2+bE^3+rE,$$

where $a>0$, $b,r\geq0$. If an admissible radius $\delta>0$ satisfies

$$\boxed{b\delta+r/\delta<a,}$$

then $E(0)<\delta$ implies $E(t)<\delta$ for as long as the trajectory exists and the estimate remains valid.

*Proof.* At a first contact with $E=\delta$, the left derivative of $E^2$ is nonnegative. The differential inequality instead gives

$$\tfrac12(E^2)'\leq-\delta^2(a-b\delta-r/\delta)<0,$$

a contradiction. $\square$

This is the generic structure of the conditional stability criterion in the uploaded paper [F1, Theorem S1 and Appendix I]. It does not certify that paper's constants.

**Corollary 10.3 — Radius feasibility.** If $b,r>0$ and there are no additional radius restrictions, a radius exists exactly when

$$a>2\sqrt{br}.$$

The optimal radius for the left-hand side is $\delta_{\rm opt}=\sqrt{r/b}$. Equivalently, with strict inequality, the allowed radii form the interval between the two positive roots of $b\delta^2-a\delta+r=0$.

*Proof.* For every $\delta>0$, $b\delta+r/\delta\geq2\sqrt{br}$, with equality exactly at $\sqrt{r/b}$. Multiplying by $\delta$ gives the quadratic form. $\square$

With additional admissibility bounds, optimise over the allowed radii, not over all positive radii. If $r=0$, sufficiently small radii work for finite $b$; if $b=0<r$, the requirement is $\delta>r/a$. Thus “make the error neighbourhood arbitrarily small” is not a universal repair when a nonzero residual persists.

For example $a=3,b=r=1,\delta=1$ gives strict margin $1$. With $a=b=r=1$, no positive radius works. These are abstract constants, not numerical estimates from Euler or from this conversation.

## Continuation is separate from invariance

Theorem 10.2 controls an existing trajectory. To infer existence for all future time, a separate continuation condition is needed. For a finite-dimensional locally Lipschitz vector field on an open domain, remaining in a compact subset of that domain supplies the usual continuation mechanism. An error bound need not supply that compact containment, especially in infinite dimensions or near an excluded boundary.

The same distinction applies to witnessed discrete systems. Every permitted transition may preserve a safety property while the system still reaches a state with no permitted successor. Safety is not liveness, and either is different from successful resolution.

## Local exceptions require concentration control

**Proposition 10.4 — Localised loss can be absorbed only quantitatively.** Suppose an analytic contribution satisfies

$$Q(f)\leq-aX+(a+b)M_B,$$

where $a>0$, $b\geq0$, $X$ is a global low-order quantity, and $M_B$ is the contribution concentrated in an exceptional region. If

$$M_B\leq m_0X+m_1Y,$$

then

$$Q(f)\leq-\bigl(a-(a+b)m_0\bigr)X+(a+b)m_1Y.$$

The resulting low-order coefficient is positive only if $a>(a+b)m_0$; the $Y$ loss requires a compensating bound, for example Theorem 10.1.

*Proof.* Substitute the concentration bound and collect coefficients. $\square$

Small region size is not enough. For a measurable set $B$ of positive finite measure, $f=\mathbf1_B/\sqrt{|B|}$ has unit $L^2$ mass entirely inside $B$, however small $|B|$ is. The uploaded paper makes precisely this distinction when localising its low-order loss [F1, pp. 61–66].

The prospective Orthemological use is to quantify whether a small set of unresolved issues can carry most of a declared risk functional. No numerical concentration law for epistemic risk is supplied here. In particular, a small count of unresolved obligations is not itself such a law.

## A discrete robust-correction certificate

**Theorem 10.5 — Discrete residual bound.** Suppose $V_m\geq0$ and

$$V_{m+1}\leq qV_m+r,\qquad 0\leq q<1,\quad r\geq0.$$

Then

$$V_m\leq q^mV_0+r\frac{1-q^m}{1-q}.$$

Every sublevel $V\leq R$ with $R\geq r/(1-q)$ is forward invariant under the assumed transitions.

*Proof.* Iterate the inequality and sum the finite geometric series. If $V_m\leq R$, then $V_{m+1}\leq qR+r\leq R$. $\square$

To apply this to a corrective runtime, $V$ must measure a declared substantive error or burden, not merely its displayed count. Provenance retention and hard admissibility must be established separately. The theorem concerns the transitions for which its bound holds, not arbitrary revisions.

## Fast/slow coupling and amplification

The dialogue identified multiscale amplification as a possible source of transferable mechanisms. The supplied Tao excerpt concerns frequency scales; frequency scales are not automatically identical to fast and slow epistemic timescales [C3]. The following elementary model isolates only the amplification structure:

$$\dot b=-\lambda b,\qquad
\dot f=(-d+\kappa b)f,
\qquad b(0)=B>0,$$

with $\lambda,d,\kappa>0$. Direct integration gives

$$b(t)=Be^{-\lambda t},\qquad
f(t)=f(0)\exp\!\left[-dt+\frac{\kappa B}{\lambda}(1-e^{-\lambda t})\right].$$

When $\kappa B>d$, the second component is initially amplified, peaks at

$$t_{\rm peak}=\lambda^{-1}\log(\kappa B/d),$$

and eventually decays. This shows how a decaying background can temporarily amplify a subordinate component. It does not prove a cross-scale relay, an infinite cascade, or blowup.

**Counterexample 10.6 — Small feedback is not automatically negligible.** For

$$\binom{\dot x}{\dot y}=
\begin{pmatrix}-1&K\\ \epsilon&-1\end{pmatrix}\binom{x}{y},
\qquad K,\epsilon>0,$$

the eigenvalues are $-1\pm\sqrt{K\epsilon}$. An arbitrarily small $\epsilon$ is destabilising if $K\epsilon>1$. A nearly triangular description therefore needs a quantitative product-of-gains bound, not merely the phrase “little feedback”.

An Orthemological model of amplified local defects or corrections must identify the actual interacting state variables, gains, feedback and timescale separation. Nothing here equates low frequency with a metaortheme or high frequency with an episode.

## Symmetry, quotient dynamics, and meaningful change

**Proposition 10.7 — Dynamics descend to an admissible quotient.** Let a group $K$ act on a state space $X$, and let $F:X\to X$ be equivariant: $F(gx)=gF(x)$. Then

$$\overline F([x])=[F(x)]$$

is well-defined on the orbit space $X/K$. An observable $q$ descends to the quotient exactly when it is constant on every orbit.

*Proof.* If $x'=gx$, equivariance gives $F(x')=gF(x)$, so the output orbits agree. The observable statement is Theorem 4.2 applied to the orbit projection. $\square$

This is the precise condition behind treating a coordinate relabelling as neutral rather than as substantive change. For differentiable modulation one needs additional regularity and an appropriate slice or gauge condition. Arbitrary analysis-version changes are not symmetries: they can change targets, constraints and observables.

## Rescaling must retain reconstruction data

**Counterexample 10.8 — A stable normalised shape can hide finite-time blowup.** The scalar equation $\dot x=x^2$, $x(0)=x_0>0$, has

$$x(t)=\frac{x_0}{1-x_0t},\qquad 0\leq t<1/x_0.$$

Set $s=-\log(1-x_0t)$ and $\widehat x=e^{-s}x/x_0$. Then $\widehat x(s)=1$ for every $s\geq0$, while

$$t(s)=\frac{1-e^{-s}}{x_0}\longrightarrow\frac1{x_0}.$$

The normalised profile is constant, but the original variable becomes unbounded at finite time. Thus a normalisation of growing episode complexity, resource consumption, or burden accumulation must retain the relevant scale and clock if conclusions concern the original process. One cannot quotient away harmful growth and then infer safety from the quotient alone. This is the mathematical lesson of the uploaded paper's explicit reconstruction step [F1, pp. 52–53, 102–103].

## Continuation through a family of models

**Proposition 10.9 — Uniform barrier transfer across a parameter family.** Let $\theta\in[0,1]$ index a family of systems. Suppose each admits an error estimate of Theorem 10.2 with constants $a_\theta,b_\theta,r_\theta$. If a common admissible radius $\delta$ and $\gamma>0$ satisfy

$$a_\theta-b_\theta\delta-r_\theta/\delta\geq\gamma
\quad\text{for all }\theta\in[0,1],$$

then the same error ball is forward invariant for every family member, while its trajectory and estimates exist.

*Proof.* Apply the same first-contact contradiction with the uniform positive margin. $\square$

This does not establish existence of a continuous branch of profiles, nondegeneracy of an implicit equation, or convergence at the endpoint. The simple family $\dot x=-(1-2\theta)x$ is stable for $\theta<1/2$ and unstable for $\theta>1/2$; solving the easy endpoint supplies no uniform stability margin. Removing forcing or adding viscosity in a fluid construction likewise needs its own analytic control, not just a parameter label.

## Hybrid safety and the infinite-event boundary

**Proposition 10.10 — Safety under flows and witnessed resets.** In each regime $\sigma$, let $\mathscr S_\sigma$ be a declared safe set. Suppose every continuous segment preserves $\mathscr S_\sigma$, and every enabled witnessed reset maps its safe guard into the successor safe set. Then every finite concatenation of such flow segments and resets preserves safety.

*Proof.* Apply segment invariance followed by reset preservation and induct on the number of resets. $\square$

To obtain a statement at every finite physical time, also rule out an unhandled accumulation of infinitely many resets, or define and verify an admissible continuation at the accumulation time. For instance, appending one factor at times $1-2^{-m}$ gives finite degree after each event, but infinitely many events accumulate at time $1$. The resulting infinite-support formal sum need not lie in algebraic $T(V)$. Finite actualisation at each stage does not supply a finite limiting episode at an accumulation point.

Finally, stability is not correctness. In $\dot x=x-x^3$, both $x=1$ and $x=-1$ are attracting equilibria, while $x=0$ is repelling. A declared target can approve one attracting state and reject the other. A robust pathological basin is a meaningful object of study only once the target, topology and dynamics are specified.

# Future-safe compression and the integrated architecture

## Current sufficiency need not survive a new inquiry

The landscape layer reveals a stronger preservation question than retaining today's verdict: will the retained representation still support the inquiries that later become live?

**Proposition 11.1 — Present adequacy does not imply future adequacy.** A representation can preserve every currently required observable while failing to preserve an observable introduced by a later inquiry.

*Proof.* Take $D=\{d_0,d_1\}$ and a constant representation $r(d_0)=r(d_1)$. Let the current required observable be $q_0\equiv0$, which factors through $r$. A later inquiry requires $q_1(d_0)=0$, $q_1(d_1)=1$. It does not factor through $r$, by Theorem 4.2. $\square$

This is not a demand to retain every possible distinction forever. It shows that a guarantee of future adequacy must declare which future observables or inquiry horizon it covers. Unrestricted future demands can defeat a presently justified compression.

## Exact quotient dynamics require more than an accurate snapshot

**Theorem 11.2 — Future-safe quotient criterion.** Let $D$ be a state space, $r:D\to Y$ a representation, $F:D\to D$ a deterministic update, $q:D\to Z$ a target observable, and $\ell:D\to\mathcal P(\mathscr J)$ an inquiry-landscape map. The following are equivalent:

(a) there exist maps on $r(D)$ satisfying

$$
\overline F\circ r=r\circ F,\qquad
\overline q\circ r=q,\qquad
\overline\ell\circ r=\ell;
$$

(b) each of $r\circ F$, $q$, and $\ell$ is constant on fibres of $r$.

Under these conditions, for every finite $m$,

$$
\begin{aligned}
r(F^m(d))&=\overline F^{\,m}(r(d)),\\
q(F^m(d))&=\overline q(\overline F^{\,m}(r(d))),\\
\ell(F^m(d))&=\overline\ell(\overline F^{\,m}(r(d))).
\end{aligned}
$$

*Proof.* Apply Theorem 4.2 separately to the three maps. The iteration identity follows by induction, using the first commuting equation. Substituting it into the other two equations gives the remaining identities. $\square$

This is a standard congruence/factorisation argument, not a new general theory of state abstraction. It is a useful exact contract here: preserve the target, preserve the evolution of the representation, and preserve the relevant inquiry landscape. Snapshot agreement alone verifies none of the future conditions. Stochastic or nondeterministic systems require a suitable probabilistic or relational counterpart rather than this deterministic equation by fiat.

## Synthesis theorem

**Theorem 11.3 — Conditional compatibility of the layers.** Fix an analysis $A$, a representation declaration satisfying Assumption F, and a finite sequence of canonical episode records with record-valid transition witnesses. Suppose the environment and landscape maps are specified, and wherever a game is used its declaration satisfies Definition 8.1 and the required joint-feasibility condition. Then:

- every episode representation has finite typed support;
- every initially recorded obligation remains historically traceable through the sequence;
- each represented state has its declared inquiry landscape, independently typed from its ecology;
- every declared finite game has a mixed Nash equilibrium;
- when a chosen compression satisfies Theorem 11.2, its finite-horizon target and landscape dynamics commute with the represented updates.

*Proof.* Use Proposition 3.2, Theorem 6.5, the definition of $\mathcal L_A$, Theorem 8.3, and Theorem 11.2 respectively. Their conclusions concern different typed objects and therefore do not require identifying an episode with a tensor, a landscape with an ecology, or a Nash equilibrium with a verdict. $\square$

This compatibility theorem does **not** imply that the game's equilibria are played, that the target is true, that all witnessed claims are semantically valid, that the landscape improves, that infinite-time execution exists, or that the chosen tensor encoding is superior. Those conclusions would require their respective additional premises.

## What would make tensor structure substantively useful?

The record channel establishes representability but not a computational advantage. Tensors earn more than storage value where the declared operators actually respect their multilinear structure. In this draft two such cases are explicit: probability marginalisation/parity detection in Section 5 and mixed-payoff contraction in Section 8. Further candidates include typed contractions that preserve required observables and equivariant transformations that commute with the update rule.

The prospective test is not whether an episode can be encoded in an array. It is whether the chosen factorisation yields a target-preserving calculation, identifiable interaction, useful compression, efficient search, or certified bound that a comparator fails to achieve at the declared cost. No such comparative experiment has been performed here. A fixed-degree encoding into a sufficiently large basis also remains possible, so any claim of *required* high tensor degree must constrain the allowed representation family.

# Bounded reflexivity of the dialogue

## Informal occurrence versus canonical episode record

Let $c$ denote the supplied conversational history. It contains ordered claims, corrections, cited constraints, rejected formulations, retained distinctions, and residual questions. It informally instantiates the process of developing and auditing the present proposal [C1]. It has not, merely for that reason, been registered as a canonical element of $E_A$.

A registration/encoding procedure would have the form

$$
\operatorname{Reg}_A:
(c,\text{identity, scope, versions, witnesses, evidence})
\rightharpoonup E_A.
$$

Its domain requires the relevant episode-signature conditions. Ecology registration is another act; a registered ecology node is not asserted here to be a universal prerequisite for every canonical episode. Similarly the existence of two speakers is not a game declaration, and mathematical support-selection formulas are not an already executed tensorisation of the full chat.

## Reification without self-certification

The canonical core's reification embedding is

$$\iota_n:E^{(n)}\hookrightarrow\mathcal M^{(n+1)},$$

where an episode is considered as the object of a higher audit [R1, §1]. At the informal level the dialogue repeatedly did this: earlier answers became later objects of criticism. The following correspondence is retrospective description, not a fabricated execution log.

| Conversational event | Bounded interpretation |
|:--|:--|
| Enthusiastic analogy was challenged | A previous reasoning output became an audit object. |
| Overcorrection towards irrelevance was challenged | The issue was reconsidered without treating caution as a refutation of overlap. |
| “An orthing is a tensor” was retired | Process/token/representation distinctions were made explicit. |
| Homogeneity was relaxed | One episode could represent several interaction orders. |
| Slot order and discharge were qualified | Word types and preservation witnesses became explicit requirements. |
| Nash was made conditional | Actors and interaction factors were not automatically equated with game players. |
| Fixed-analysis landscape change was recognised | Environment changes were separated from analysis-version events. |
| The chat's own status was bounded | Informal exemplification was not promoted to a canonical record, tensor, game, or theory validation. |

No binary score $\operatorname{ResultCorrect}(c)=1$ is inferred for the conversation as a whole. Retaining a conclusion while improving its reasoning does not prove that conclusion true. Likewise repeated agreement about a proposed freeze is not a kernel check or a repository-adoption act.

**Proposition 12.1 — Reification alone supplies no truth upgrade.** An injective map from episodes to higher-level audit objects does not entail the validity of the episodes' conclusions.

*Proof.* Take any set of episodes containing one with a false conclusion. Map it injectively into a disjoint copy of that set regarded as audit objects. Injectivity preserves identity and distinguishes objects; it changes no truth value. $\square$

A higher audit needs its own evidence, standards and checked inferences. A self-referential topic does not exempt it from those obligations. The reflexive claim that survives is simply: **the proposal was developed through a process that exhibited several of the distinctions it proposes to represent.**

# Disposition and remaining research obligations

## The three tasks have concrete candidate answers

**First: define $\rho_A$ on the actual episode signature.** Section 2 specifies the interface to the source record. Section 4 gives a finite atomisation plus a typed interaction extractor and proves faithfulness to the declared view. A production application still needs a versioned extractor against the repository's actual schemas, a declared interaction registry, and the task-specific required observables. The generic encoding theorem does not choose those semantics.

**Second: define witnessed degree-lowering/discharge operators.** Section 6 gives contraction operators, a counterexample to unwarranted contraction, and a guarded transition interface preserving obligation history. A production system must specify which witnesses are authoritative and which source-level claims they establish. Active simplification does not erase the record.

**Third: define $\mathcal L_t$ independently of $\Gamma_t^\mu$.** Section 7 defines it by a feasibility predicate on finite inquiry objects in a full environment state. It distinguishes actual, estimated, and shape-level landscapes. Quantitative judgments about research externalities require a declared value functional and evidence about alternative closure pathways.

These are candidate mathematical constructions and proof obligations, not newly admitted experimental arms. The existing controller/representation labels are untouched; in particular there is no new “representation G” [R4].

## A usable next mathematical target

A bounded instantiation could select a small family of synthetic episode records, a handful of relation signatures, an explicit obligation ledger, and a finite set of inquiry actions. It could then test whether the chosen interaction representation preserves the target observables and future inquiry options under a specified update rule. The preservation criterion is Theorem 11.2; the toy strategic layer can be checked by exact regret calculations; and a discrete robustness objective can be tested against Theorem 10.5.

This does not require asserting that all orthing is tensorial, that all correction is gradient descent, or that all communication is Nash play. It also does not require waiting for an NS solution. A future fluid result would be helpful to this programme only insofar as a particular estimate or mechanism can be instantiated with its hypotheses verified.

## Final mathematical boundary

The retained headline is unchanged:

> An orthing admits an analysis-declared graded tensor representation whose possible interaction degree is open at the schema level and whose realisation in each concrete episode has finite typed support.

The additional layers remain conditional:

$$
\begin{gathered}
\text{tensor representation}\neq\text{episode ontology},\\
\text{tensor product}\neq\text{Cartesian strategy product},\\
\text{record-valid witness}\neq\text{semantic warrant},\\
\text{equilibrium}\neq\text{truth or pathway adequacy},\\
\Gamma_t^\mu\neq\mathcal L_t,\\
\text{invariant existing trajectory}\neq\text{global continuation},\\
\text{informal reflexive example}\neq\text{theory validation}.
\end{gathered}
$$

# Appendix A — Adjudication of formulations from the dialogue

The following table preserves the correction history instead of silently laundering preliminary claims into the final theory.

| Earlier formulation | Final disposition |
|:--|:--|
| An orthing is an indefinite-degree tensor | Retired. Degree is open in a declared representation language; an episode is not identified with its image. |
| Every episode is homogeneous | Retired. Finite word support can occupy several degrees. |
| Multi-degree identifies one typed product | Qualified. The complete component includes all typed words with those counts. |
| More evidence necessarily raises degree | Rejected. It can add coefficients within an existing word component. |
| $D=\sum_kD_k$ is automatically well-defined | Qualified by pointwise local finiteness or separately declared completion/convergence. |
| Degree reduction is warranted discharge | Rejected as an implication. Contraction can lose a required distinction; a semantic witness and retention contract are needed. |
| The landscape is a linear direct sum | Retired. It is a constrained set of inquiry objects; supports and grades are derived descriptors. |
| Fewer possible inquiries means worse closure | Rejected. Values, costs and constraints, not cardinality alone, determine the comparison. |
| Finite typed support gives Nash | Rejected. A finite strategic declaration and appropriate joint feasibility are additional assumptions. |
| Every continuous strategy game needs a different theorem | Qualified. Some remain within finite-dimensional Kakutani under extra hypotheses. |
| Normal form cannot represent information | Qualified. A justified normal-form reduction may encode contingent plans; the reduction must retain the information structure. |
| Publication necessarily changes $A$ | Rejected. The environment and landscape can change under a fixed analysis. |
| Every landscape change moves equilibrium | Rejected. The implication is possible, not necessary; comparison also needs common types or transport maps. |
| Only unforced NS can satisfy the Clay challenge | Corrected using [F4]. Its breakdown alternatives permit forcing under specific regularity/decay conditions. |
| Normalised stability proves original safety | Rejected. Reconstruction scales and the time map can retain a singularity. |
| The chat is already a canonical tensor/game episode | Rejected. It is an informal exemplar; the relevant records and declarations have not been instantiated for it. |

These are technical qualifications of the frozen headline, not a replacement headline and not an assertion that earlier source documents made all these claims.

# Appendix B — Result and dependency register

| Result | Dependencies and status |
|:--|:--|
| Proposition 3.2: finite actualisation | Algebraic direct-sum definition; exact structural consequence. |
| Proposition 4.1: faithful finite-record view | Assumption F, injective atomisation, disjoint record channel; proposed construction. |
| Theorem 4.2 and Corollary 4.3: adequate compression | Fibre constancy; standard elementary factorisation. |
| Theorem 5.1 and Corollary 5.2: parity obstruction | Exact binary distributions; standard mathematics, repository T300 connection. |
| Proposition 6.1: degree-shift decomposition | Linear endomorphism of an algebraic direct sum; pointwise local finiteness. |
| Proposition 6.2 and Counterexample 6.3 | Linear algebra; no structure-free nonzero deletion and no automatic semantic preservation. |
| Theorem 6.5: obligation traceability | Explicit retention/coverage witness contract; finite induction. |
| Propositions 7.1–7.3: landscape/value separations | Constructed finite models, declared feasibility and value; no empirical claims. |
| Theorem 8.3: finite mixed Nash existence | Nonempty finite sets, finite real payoffs, full normal-form product, Kakutani; classical. |
| Propositions 8.4–8.6: strategic transport/change | Nash inequalities, uniform payoff error, explicit finite state-change model. |
| Proposition 9.2: surrogate margin | Metric error plus Lipschitz constant plus certified margin; elementary bound. |
| Theorem 10.1: coupled-energy criterion | Nonnegative energies and declared differential bounds; standard energy method. |
| Theorem 10.2 and Corollary 10.3 | Existing trajectory, boundary-valid estimate, admissible radius; standard barrier calculation. |
| Proposition 10.4 | Explicit concentration bound; algebraic absorption, not an epistemic risk law. |
| Theorem 10.5 | A declared discrete recurrence; geometric-series bound. |
| Propositions 10.7, 10.9, 10.10 | Equivariance; uniform parameter margins; safe flow/reset hypotheses. |
| Propositions 11.1 and Theorem 11.2 | Fibre criterion and deterministic update; future-safe abstraction contract. |
| Theorem 11.3 | Composition of the stated layer-specific results; no promotion across layers. |
| Proposition 12.1 | Injective reification changes no truth predicate; elementary countermodel. |

The proof obligations for the intended real-world applications remain distinct from these mathematical derivations. In particular no source-world bridge, empirical programme, formal proof-assistant check, or repository adoption is asserted.

# Appendix C — Source register and provenance

Repository references below are pinned to the observed head

`f50dc1aee52356cc6adbef342387576b02afc124`.

Their paths identify public sources; the present package does not redistribute a full repository snapshot. The following items were read through the connector during this production pass. Earlier dialogue supplied additional contextual excerpts, but no new claim depends on treating those as a later adopted authority.

**[R1] Orthemology, canonical formal core.** *Orthemic Core Formalization — Orthing, Episodes, Metaorthemes, Pathway Adequacy*. `theory/orthemic-core-formalization.md`, especially §§1–2.2a. Process/token distinction, episode signature, reification and record/trace separation. Git blob: `34effd9e917b5372e53d03a71e052fd38050490c`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/theory/orthemic-core-formalization.md).

**[R2] Orthemology, notation registry.** `docs/notation-registry.yaml`. Inspected symbol registry and relevant render entries. Git blob: `6964d65a613d9687d8c00a07b1826fff60e8b70d`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/docs/notation-registry.yaml).

**[R3] Orthemology, AR8R-T300.** *Lower-order alignment can be blind to causal restoration*. `docs/project-closure/ar8r-v11/theorems/ar8r-t300-lower-order-alignment-blind-restoration.md`. Exact parity construction and scope restrictions. Git blob: `d13c504037255a6bd1a0a8c8d10aa3c6ae7baf3d`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/docs/project-closure/ar8r-v11/theorems/ar8r-t300-lower-order-alignment-blind-restoration.md).

**[R4] Orthemology, tensor programme.** *Tensor representations and the Bitter Lesson challenger*. `docs/project-closure/ar8r-v11/programs/tensor-and-bitter-lesson.md`. Representation/ontology boundary, distinct controller and representation labels, and unresolved experiment-arm specification. Git blob: `73c1c3dc54d4f3a8ed8358029c492984eab1af87`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/docs/project-closure/ar8r-v11/programs/tensor-and-bitter-lesson.md).

**[R5] Orthemology, Decision 0033.** *Governed corrective search and transition witness*. `docs/decisions/0033-governed-corrective-search-and-transition-witness.md`. No hidden obligation deletion, separate soundness and admissibility, and fast/slow revision discipline. Git blob: `66f1c9c1a2cda1678b835913e1268eec9345e675`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/docs/decisions/0033-governed-corrective-search-and-transition-witness.md).

**[R6] Orthemology, Decision 0032.** *Governed metaorthemic ecology and source dependence*. `docs/decisions/0032-governed-metaorthemic-ecology-and-source-dependence.md`. Typed historical graph and distinction between propagation and warrant. Git blob: `33919d8ea7a20c7cdcc3961cf7b2b4f3474f9d44`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/docs/decisions/0032-governed-metaorthemic-ecology-and-source-dependence.md).

**[R7] Orthemology, sound-descent comparison.** *Sound descent: G0 / G1 / G2 model comparison*. `applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md`. Feasibility-first order-theoretic correction, two timescales, and requirements for literal gradient dynamics. Git blob: `0929ef49e847b3bcfd5847600a6a80c46283f2f7`. [Pinned source](https://github.com/theislampill/orthemology/blob/f50dc1aee52356cc6adbef342387576b02afc124/applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md).

**[F1] Adarsh Ganeshram, Valentin Duruisseaux and Anima Anandkumar.** *Stable Singularity of the Euler Equations on $\mathbb R^3$*. User-supplied `Euler.pdf`, 107 pages, September 2026 manuscript. The provided text was available in full; the sections used here and relevant diagrams/equations were specifically inspected. Printed page references are used. Uploaded-file SHA-256:

`f0164c40fad09a646412acec95f7908ea6b2fd61d16b809954a4048665fb5f78`.

The authors' [public manuscript](https://anima-ai.org/wp-content/uploads/2026/09/Euler.pdf) was also accessible through web parsing; byte identity with that online version was not independently established. No end-to-end theorem or Lean audit of this source was performed.

**[F2] Anima Anandkumar.** “Stable Singularity of the Euler Equations on $\mathbb R^3$ without forcing.” Author announcement, 7 September 2026; accessed 8 September 2026. Used only to corroborate the scope of the announced candidate programme. [Author page](https://anima-ai.org/2026/09/07/stable-singularity-of-the-euler-equations-on-r3-without-forcing/).

**[F3] Tristan Buckmaster, public repository.** `tristanbuckmaster/fluid_lean`. Repository metadata and root contents inspected through GitHub on 8 September 2026. The inspected root contained `affinecore`, `boussinesq-blowup` and `euler-blowup`. No full build, dependency audit, or proof-scope certification was conducted. [Repository](https://github.com/tristanbuckmaster/fluid_lean). The separately linked NYU statement/Euler/Boussinesq PDFs were not retrievable for full review during this execution; the mechanism description attributed to Tao remains grounded in the supplied excerpt [C3].

**[F4] Charles L. Fefferman.** *Existence and Smoothness of the Navier–Stokes Equation*. Clay Mathematics Institute problem statement, including the four alternatives (A)–(D), pp. 1–2. Primary source inspected to keep forcing and target variants precise. [Official statement](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).

**[M1] The mathlib community.** *Mathlib.LinearAlgebra.TensorAlgebra.Basic*. Official documentation, accessed 8 September 2026. Used for the tensor-algebra universal-property reference, not as verification of this draft. [Documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/TensorAlgebra/Basic.html).

**[M2] John F. Nash, Jr.** “Equilibrium points in n-person games.” *Proceedings of the National Academy of Sciences* 36(1), 48–49, 1950. DOI: 10.1073/pnas.36.1.48. Primary publication record and indexed text inspected; the argument is reproduced here in self-contained form. [Publication](https://doi.org/10.1073/pnas.36.1.48).

**[M3] Shizuo Kakutani.** “A generalization of Brouwer's fixed point theorem.” *Duke Mathematical Journal* 8(3), 457–459, 1941. DOI: 10.1215/S0012-7094-41-00838-4. Standard theorem imported in Theorem 8.3, not reproved. The original full text was not inspected in this production pass; the formulation was checked against the [official Lean project statement](https://lean-lang.org/eval/problems/kakutani_fixed_point/) and the use in Nash's primary publication [M2].

**[C1] The accompanying user–assistant dialogue.** Primary provenance for the frozen headline, actualisation chain, witnessed-discharge proposal, landscape/game separation, and bounded-reflexivity instruction. The present document is a formalisation of the settled formulation, not a claim that the entire dialogue was already a canonical episode record. No separate complete transcript archive is included.

**[C2] User-supplied screenshot.** The screenshot describes poorly extracted solutions as potentially recovering less mathematical value from open problems. It is used as supplied contextual motivation. Its visible crop does not itself show an author or post identifier; independent authorship and the original post's complete context were not established. No historical “first time” claim is adopted.

**[C3] User-supplied excerpts attributed to Terence Tao and Tristan Buckmaster.** They motivate the distinction between low-to-high-frequency amplification and the separate PINN/stability route, and the interest in extracting mechanisms. The original Tao post text was not independently retrieved from the JavaScript-only profile in this pass. No verbatim quotation beyond short phrases is needed for the mathematical arguments.

# Appendix D — Verification scope

The companion `verify_examples.py` uses exact rational arithmetic where relevant. It checks finite record atomisation, typed-word/order distinctions, parity marginals, target-erasing contraction, obligation-retention counterexamples, the finite publication games, the regret bound, and rational instances of the coupled-energy and invariant-radius inequalities. Its declared finite ranges and results appear in `verification.json`.

The delivered execution passed all **11 test groups**. Selected exact ranges are:

| Finite check | Executed scope |
|:--|:--|
| Record channel | 19 distinct synthetic records; exact round trips and no cross-record collisions. |
| Parity marginals | Arities 2–8; all 501 proper-subset marginals, comprising 9,329 marginal entries. |
| Fibre criterion | 256 pairs of binary representation/target maps on four states. |
| Regret transport | 32,400 payoff-perturbation/profile cases on a rational mixture grid. |
| Coupled-energy weights | 1,764 coefficient choices: 1,073 positive-weight cases and 691 empty intervals. |
| Discrete residual estimate | 1,116 exact recurrence/time instances. |
| Future-safe quotient | 65,536 finite-map cases, including 6,144 compatible cases checked through seven iterates per starting state. |

The other groups cover word order, witnessed history retention, finite games, and landscape countermodels. These are different finite denominators, not a single empirical sample of orthing episodes.

These checks establish only that the stated implementations and examples meet those tests. They do not machine-check the proofs, validate a causal model of research, instantiate every canonical episode field, or certify either fluid manuscript. The source and output provenance are recorded separately in `provenance.json` and `MANIFEST.sha256`.

The LaTeX and Markdown contain the same substantive manuscript. The PDF is compiled from the delivered LaTeX. The package contains no font files and no claimed Lean proof. Version 1 is a bounded research artifact for review, not an authorised change to repository theory or experimental status.
