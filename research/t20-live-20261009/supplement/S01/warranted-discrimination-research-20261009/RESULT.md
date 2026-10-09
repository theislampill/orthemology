# Warranted completion with proof-sensitive memory and inquiry cost

9 October 2026. Restricted constructive mathematics for T20. No repository change, integration, scientific-adoption decision, or programme closure.

## Result

In a finite, persistent-evidence model, the information that must survive a reduction is computable from the actual premises of admissible proofs. For each scoped verdict, retain the undominated pairs

\[
  (\text{premise tokens still missing},\;\text{cost of checking the proof}).
\]

This **weighted residual-certificate frontier** determines exactly which subsequent evidence acquisitions permit that verdict and at what terminal verification cost. Equality of the frontiers is also necessary when all finite sequences of the declared single-token acquisitions remain available. The frontier updates without replaying the entire history. Coupled to the permitted query model, it preserves the exact optimal worst-case cost of substantive resolution.

This is stronger than retaining the answer, the truth values of the premises, or the present set of licensed verdicts. With one rule requiring n distinct attestations, there are exactly 2^n different future-completion profiles, although the current proof-availability bit has only two values. The distinguishing continuations are ordinary sequences of at most n single-token retrievals.

The second result is an exact completion test. For a finite menu of persistent, order-independent, one-use tests, there is a strategy guaranteeing a proof-bearing substantive verdict if and only if every feasible full response transcript supplies the support of at least one admissible certificate. A finite Bellman recurrence then gives the optimum, charging both acquisition and terminal verification. Failure is failure of warranted completion under this contract, not proof that the target is false.

These results are new developments relative to the retained packet, not claims to invent certificate complexity, positive proof provenance, residual-language methods, Pareto reduction, or dynamic programming. Their contribution is an explicit, constructive bridge between the packet's source/rule distinctions and its continuation and cost questions.

## 1. What is inherited

The actual retained texts, rather than the owner's retrospective synopsis alone, supply these inputs:

- *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, §§3–4: ordered typed representations, distinct record and interaction channels, and Theorem 4.2's elementary fibre criterion. Its §5 parity example is an information obstruction, not an epistemic licensing rule.
- The same manuscript, §6: record-valid witnesses and semantically valid witnesses are different. Theorem 6.5 preserves lineage only under the stated record conditions and gives substantive validity only when every substantive link is valid.
- The same manuscript, §§7 and 9: prospective inquiry feasibility includes access, authority, resource and dependency constraints; a conditional proof does not establish its application premises; unverified bridges remain obligations.
- *Continuation-Complete Orthings*, Theorems 1–2 and Proposition 9: exact moment defect, action–observation continuation, continuous full-law dimension, and augmentation. The source already includes local fibre certificates and adaptive feedback. It expressly says prediction sufficiency need not preserve provenance and that coordinate count is not acquisition cost. The present result does not rediscover those facts.
- *Necessary truth sensitivity and operative factive grounds*, including its nineteen-line System R derivation: known contents actually used in competent inference are additional epistemic premises. A correct proof written by an observer beside an assenter does not establish the assenter's operative basing.

Pinned source and actual read ranges are in SOURCES.json. No omitted source is treated as exhausted. The graph-continuation work is an inherited example of permitted-action sensitivity; its Steiner formula is not required for the proofs below.

## 2. A restricted semantic and proof contract

### 2.1 Targets and statuses

Fix a claim identity and version, a finite declared semantics, admissible source commitments, and a finite set V of **scoped output records**. An output can concern positive support, independently supported negation, an inconsistent specified premise set, a syntax/type failure, a semantically ambiguous expression, or the absence of a certificate in a specified finite search space at an identified inventory/time snapshot. Such a negative diagnosis is about that fixed snapshot, not an invariant claim that no future evidence can support the target. These are different output types. They are not forced into one mutually exclusive partition: for example, a claim can be both currently unsupported and semantically underdetermined.

The task specifies a substantive goal set G⊆V. An always-available `defer` or `unresolved` record does not count as success unless that bounded diagnosis was itself the requested goal. A licence to state 'no proof was found in this catalogue' does not licence 'false'. Nor is failure to find a countermodel a proof of truth. A formula's satisfiability under an interpretation is not evidence that the interpretation is faithful or metaphysically possible.

### 2.2 Evidence is not a truth oracle

Let E be a finite set of distinguishable evidence tokens. Each token identifies its content, source or acquisition route, target/version, applicable scope and authentication conditions. Tokens need not be independent probabilistic samples. Distinct tokens in the examples discharge distinct premise obligations; copying one token does not create another premise or independent source.

K⊆E is the currently accessible authenticated inventory. Authentication establishes the declared identity and integrity conditions, not the truth of every assertion inside the artifact. The source commitments determining what an authenticated token supports remain explicit premises of the analysis. A test may return raw text and deliver no usable token. A separate authentication or interpretation step must then be represented before that text can discharge a premise.

Fix a finite catalogue Γ of admitted valid derivation templates generated from an explicit finite bounded proof grammar, or supplied as individually inspectable finite derivations. Their rule/scope well-formedness is established at catalogue admission. Under the supported-input conditions below, each terminal instantiation/check is guaranteed to succeed; its cost is still paid when executed. An unvalidated or potentially failing candidate is not admitted under this contract: checking it would require an additional outcome-bearing transition. For π∈Γ, record:

- Sπ⊆E: the evidence leaves actually cited in this derivation;
- vπ∈V: its exact scoped conclusion;
- κπ≥0: its finite real declared terminal assembly/checking cost;
- the derivation itself and its rule, interpretation and version references.

The catalogue is not an arbitrary list of true answers. Its supports are extracted from finite derivations. For an acyclic positive rule system they can be compiled recursively: evidence leaves contribute singleton supports; combining premises takes unions; alternative derivations take alternatives. Shared leaves are not counted twice. The catalogue can be incomplete for the logic; all optima below are relative to it and its expressly permitted alternatives.

### 2.3 Conditional soundness and production

Assume that evidence admitted to K meets the specified source commitments and that each rule preserves the declared judgement when its premises are supported. Induction on a proof object then establishes the ordinary conditional soundness lemma: if Sπ⊆K and π passes the rule/scope checker, producing π warrants vπ **relative to those commitments**. The induction does not authenticate its own leaves or certify the philosophical adequacy of the rule system.

Availability of the leaves makes π eligible for checking. It does not say checking has already occurred. The protocol completes only when it produces and checks a selected π, paying κπ. A previously checked reusable certificate can have its own token and expressly priced reuse rule. An unexecuted terminal instantiation is not silently assigned zero checking cost. Query prices include any authentication charged at acquisition; terminal prices cover the final derivation. Optimising the internal scheduling and reuse of arbitrary proof fragments is outside this restricted model.

A system-produced, checked derivation supplies an explicit procedural dependency on its cited premises. It does not prove that a human observer believes its conclusion, uses those premises, functions properly, or has knowledge. The retained System R result remains conditional on its genuine knowing and basing premises.

### 2.4 Persistence assumptions

During one inquiry, valid acquired tokens remain valid and accessible; acquiring more does not revoke earlier tokens or invalidate existing proofs; supports are reusable sets, not consumable multisets; the catalogue, semantics, source commitments and prices are fixed. Expiry, defeat, source withdrawal, order-sensitive permission, resource consumption and semantic revision require an expanded state/transition model. They are not covered by monotonicity below.

## 3. The canonical residual-certificate theorem

For each v and current inventory K, form

\[
 A_v(K)=\{(S_\pi\setminus K,\kappa_\pi):\pi\in\Gamma,\ v_\pi=v\}.
\]

Say (D,k) dominates (D',k') when D⊆D' and k≤k'. Remove duplicate pairs and every strictly dominated pair. Call the resulting finite antichain Rv(K). Retain an actual derivation reference behind every retained pair; different derivations having the same pair are interchangeable only for the stated cost-and-availability observation, not for every possible provenance question.

For additional evidence U⊆E, define

\[
 F_{K,v}(U)=\min\{\kappa_\pi:S_\pi\subseteq K\cup U,\ v_\pi=v\},
 \qquad\min\varnothing=+\infty.
\]

This is the least cost of an available terminal certificate, not a claim that the certificate is already checked.

**Theorem 1 — Canonical proof-sensitive continuation.**

1. F(K,v)(U)=min{k:(D,k)∈Rv(K), D⊆U}.
2. Rv(K)=Rv(K') for every v if and only if F(K,v)(U)=F(K',v)(U) for every v and every U⊆E.
3. Acquiring T updates the frontier exactly by replacing each (D,k) with (D\T,k) and deleting dominated pairs. In particular residualization is a congruence: equal frontiers remain equal after every common acquisition.
4. Therefore the tuple (Rv(K))v is the coarsest quotient of inventories preserving every specified verdict's least terminal checking cost after every additional evidence set. This is uniqueness of the normalized antichain and of the equivalence classes, not of the choice of encoding.

*Proof.* Eligibility is Sπ⊆K∪U iff Sπ\K⊆U. A dominated pair cannot improve the minimum, proving 1.

For necessity in 2, recover a frontier directly from its cost function f:

\[
 \{(D,f(D)): f(D)<\infty\text{ and }f(D\setminus\{d\})>f(D)
                           \text{ for every }d\in D\}.
\]

The condition for D=∅ is vacuous. If (D,k) is undominated then f(D)=k; a value ≤k on a proper subset would give a dominating pair. Conversely, if the displayed condition holds, some attaining catalogue pair has support contained in D and cost f(D); any proper containment contradicts the condition, so that pair is (D,f(D)) and is undominated. Immediate subsets suffice by monotonicity. Thus the function determines precisely its frontier. Sufficiency is 1.

For 3, (Sπ\K)\T=Sπ\(K∪T). Previously discarded dominance survives subtraction, since D⊆D' implies D\T⊆D'\T and costs do not change. Applying minimization before or after subtraction therefore gives the same frontier. Equivalently F(K∪T,v)(U)=F(K,v)(T∪U).

For 4, any summary which decodes every F(K,v)(U) must distinguish inventories with different such functions. Part 2 identifies exactly those equivalence classes. Parts 1 and 3 construct a sufficient updating summary. ∎

### Permitted-context qualification

The necessity claim quantifies over all U. It is operationally exact when every token can be retrieved by its declared single-token action, finite sequences remain permitted, and previously acquired tokens can be retrieved again if a comparison context calls for them. Any U is then supplied by a sequence of |U| actions; no magical one-step evidence oracle is assumed.

For a smaller actual inquiry menu, equality of these frontiers remains sufficient but can be unnecessarily fine. The coarsest actual quotient tests only continuations allowed by that menu, together with their costs and response possibilities. A token that can never arrive cannot justify a distinguishing continuation. The planning theorem below retains these constraints explicitly.

### What this reduction does not erase

The frontier is a decision summary. It does not by itself preserve original artifacts, complete proof objects, all provenance distinctions, or a history of revisions. The system must still retain or retrieve the referenced evidence and proof when executing the terminal check. If retrieval costs money or time, it belongs in the acquisition/verification price or in explicit actions. A summary containing a missing-token set without recoverable evidence is not a proof.

Consequently the theorem is not a minimum physical RAM claim in a system with a free external archive. The memory count below is a count of distinguishable continuation-control states when the retained representation is the sole source for those decisions. An archive that can supply the distinction is part of the retained representation; recomputing from it can reduce active RAM at a separately specified access cost.

## 4. Exact cost and completion under permitted tests

Let Ω be a finite nonempty set of response scenarios. They describe how permitted tests respond, not oracle truth labels. Each test a in a finite menu Q has a deterministic response oa(x) for x∈Ω, a finite nonnegative real acquisition/authentication cost ca, and a finite token payload τ(a,o)⊆E. Responses may deliver no admissible token. No test is used twice. Tests remain available regardless of earlier outcomes, and their response and payload are order-independent. These are substantive assumptions, not consequences of finiteness.

A state is (K,B,Q), where B⊆Ω is the nonempty set of scenarios consistent with the responses seen so far and Q the remaining menu. For a feasible response o define B(a,o)={x∈B:oa(x)=o}. Its successor is

\[
 (K\cup\tau(a,o),\ B(a,o),\ Q\setminus\{a\}).
\]

Let tG(K)=min{κπ:Sπ⊆K, vπ∈G}. A deterministic adaptive policy chooses either a terminal certificate to check or a remaining test, using only its accumulated responses. Equivalently, randomization may be allowed if the cost maximum also ranges over every policy random choice. Worst-case expected cost under private randomization is a different objective and is not covered by this recurrence. All scenarios in B must terminate with a checked G-certificate. Its cost is the worst-case sum of executed test prices plus the one final certificate price. Offline catalogue compilation and optimal-policy search are not included in this execution cost; no polynomial planning algorithm is claimed. Exact executable planning additionally requires effectively represented and comparable prices, such as the rational prices used in the checks; for arbitrary finite real prices the theorem states a mathematical minimum.

**Theorem 2 — Exact completion and least execution cost.** The minimum guaranteed cost satisfies

\[
 D(K,B,Q)=\min\left\{
 t_G(K),\ \min_{a\in Q}\left[c_a+
 \max_{o:B(a,o)\ne\varnothing}
 D(K\cup\tau(a,o),B(a,o),Q\setminus\{a\})\right]\right\}.
\]

Empty minima are +∞. The recurrence is finite and attains every finite optimum. For

\[
 K_x^{\rm all}=K\cup\bigcup_{a\in Q}\tau(a,o_a(x)),
\]

finite guaranteed resolution exists exactly when

\[
 \forall x\in B\ \exists\pi\in\Gamma:\quad
 v_\pi\in G\quad\text{and}\quad S_\pi\subseteq K_x^{\rm all}.
\]

Finally, for equal B and Q, replacing K by its complete per-verdict residual frontier preserves D and admits the same cost-optimal test actions and abstract terminal verdict/cost choices. The realizing concrete certificate IDs may differ between inventories. A proof/evidence reconstruction channel must still supply a genuine terminal witness.

*Proof.* Induct on |Q|. A successful policy either stops with an eligible certificate, costing at least tG(K), or first chooses some a. An adversarial feasible response selects a successor whose optimal remaining cost is the displayed maximum. Conversely choose a minimizing action and recursively optimal successor policies, or a minimizing terminal proof. The finite catalogue and finite branching attain each finite minimum. The induction proves the recurrence and optimality. Even when a certificate is available, another test can be better if it supplies a much cheaper proof; hence the recurrence does not force immediate stopping.

For necessity of the completion criterion, follow a successful strategy in scenario x. Persistence and order independence ensure that its acquired support is contained in Kx(all). Its terminal certificate is therefore available there. For sufficiency, execute all remaining tests in any fixed order. Each full transcript determines the same payload inventory for every scenario in that transcript's response fibre. The displayed condition guarantees some G-proof in that inventory, which can be selected by inspecting the fixed catalogue. Verify it. There are finitely many scenarios and finite prices, so the maximum cost is finite.

For the final statement, frontiers determine tG and update identically under every payload by Theorem 1. The same B,Q give the same actions, prices and feasible responses. Induction in the recurrence proves equal values, test-action choices, and abstract terminal verdict/cost choices; it does not identify the concrete terminal proof objects. ∎

This is a restricted complete test, not a refutation oracle. An x with no full-transcript certificate is a precise obstruction to this protocol's promised warranted completion. It need not be a metaphysical possibility, a false target, or a defeater of knowledge held by a person through some other route. If the task is to identify whether that missing case is semantically admissible, that question needs its own evidence and scope.

## 5. Sharp controls and reusable consequences

### 5.1 Same displayed information, different entitlement

Let r be an unauthenticated copied report saying P, and let e be an authenticated report of the same P from the source accepted by the analysis. A rule allows e, together with a separately justified bridge b proving P⇒Q, to support Q. It does not allow r to substitute for e. Compare an authenticated-evidence history with K1={e,b} to a history displaying raw report r but having only K2={b} in its usable inventory. The raw report remains outside K2. A projection of the displayed content shows the same P and P⇒Q in both histories. Nevertheless a Q-proof is available only in K1. If all remaining inquiries merely repeat r, K2 has no permitted completion while K1 can finish after checking the proof.

No claim is made that authentication alone creates truth or that every unauthenticated claim is false. The example isolates a separately declared evidential entitlement. Adding a new trustworthy route for P can repair K2. It is the route-sensitive evidence/rule contract, not the choice of vector or tensor notation, that creates the distinction.

### 5.2 Two current licence states, exactly 2^n future states

Take E={e1,…,en} and one admissible proof of v whose support is E and whose checking price is k≥0. The tokens discharge n distinct scoped premises. Each token has a permanently available unit-cost retrieval action. Then

\[
 R_v(K)=\{(E\setminus K,k)\}.
\]

Every one of the 2^n inventories has a different frontier. Directly, for K≠K', choose an orientation with some e∈K\K' and retrieve, in any order, exactly the tokens in E\K. This is at most n single-token actions. The common continuation completes K and leaves e missing from K'. If only the opposite difference is nonempty, interchange the histories.

Thus any exact finite-state representation for all these continuations needs at least 2^n distinguishable states, or n bits in a fixed-length binary state encoding. Storing K attains the bound. The current availability bit is 1 only when K=E and 0 otherwise, so it has only two values. The optimal fresh acquisition cost from K is n−|K|+k, which alone also loses distinctions between equally sized inventories. Neither the current licence nor the current cheapest cost suffices for all future specified continuations.

This is a residual monotone-Boolean-function construction, not a new universal information-dimension theorem. Truth of the proposition and its ordinary probability law can be identical across these histories while the evidence inventory differs. The result concerns warrant-control state, not a theorem that the target itself contains n bits of truth information.

### 5.3 Minimal support is insufficient when verification is priced

Suppose π1 needs {a} and costs 10 to check, whereas π2 needs {a,b} and costs 1. The larger support cannot be thrown away as logically redundant: if K={a} and b costs 1 to retrieve, obtaining b and checking π2 costs 2, while immediately checking π1 costs 10. The empty-inventory frontier keeps both ({a},10) and ({a,b},1); after acquiring a, its residual pairs are (∅,10) and ({b},1). This is why counting missing evidence alone can choose the wrong investigation.

### 5.4 A certificate can be cheap while finding it is expensive

There are n possible witness locations. Exactly one contains an authenticated refutation witness, and test i inspects location i at unit cost. All positive-witness proofs have the same finite terminal checking price k. A positive result yields token wi, any one of which supports the same scoped refutation; negative results give no refutation token. Every realised certificate needs only one witness. Nevertheless the exact guaranteed search cost is n, plus terminal checking: an adversary can put the witness in the last uninspected location. Inspecting all locations attains the bound. This n lower bound is for obtaining an actual positive witness token under the declared catalogue. If the independently warranted exactly-one promise plus n−1 negative results is instead admitted as a rule certifying the target without inspecting the last witness, that different catalogue can resolve it earlier. Negative findings and a promise do not acquire that inferential licence merely by appearing in the response model.

This standard certificate/search separation gives a practical warning: the existence of one decisive counterexample does not bound the effort to locate it. Conversely, receiving a well-formed, independently authenticated counterexample may make further broad investigation unnecessary.

### 5.5 Coordinate dimension does not price acquisition

The inherited augmentation formula counts independent continuous statistics of a law. The present model prices obtaining identified tokens and checking scoped proofs. A single admissible test can return a large evidence bundle; a single missing trusted premise can be impossible to obtain, or arbitrarily costly. Rescaling its price changes D without changing any observable span or dimension. Therefore no general conversion from the inherited rank increment to execution cost follows without a declared acquisition-and-verification model. This is not a rival statistical sampling campaign.

## 6. Finite semantic alternatives: when clarification is enough

The framework can resolve a genuine semantic task without interpreting arbitrary natural language. Fix a finite justified interpretation family I for the submitted claim version. For each i∈I, qi is its precise content. A separate admissible proof sJ can establish that the intended interpretation lies in nonempty J⊆I. Refutation proofs for qi must use the same intended domain and proposition version; merely exhibiting some unrelated interpretation with a countermodel does not suffice.

Use the explicit rule:

  sJ and proofs of ¬qj for every j∈J imply `the intended content of this version is refuted`.

**Proposition 3 — Semantic cover compilation.** For this rule, if sJ has support A and the selected refutation of each qj has support Cj, the resulting proof has support

\[
 A\cup\bigcup_{j\in J}C_j.
\]

Taking all admissible J, all their semantic proofs, and all their premise-proof choices gives exactly the proof supports generated by that rule. Shared evidence is counted once. Rule/assembly checking costs are attached to the actual combined proof, not inferred from support cardinality.

*Proof.* Every rule instance has precisely these premises, so its leaf set is their union. Conversely any listed combination instantiates the rule. Soundness follows because the actual intended interpretation lies in J and its corresponding negation is among the established premises. ∎

For example, with two admissible meanings, direct refutation requires evidence for both unless one certificate covers both. A warranted clarification establishing the first meaning permits the first refutation alone, but the clarification proof is an additional premise. A cheap interpretation change invented by the investigator supplies no such certificate. The least-cost choice among common refutation, separate refutations, and clarification-plus-refutation is then a concrete application of Theorem 2.

This is a limited operational gain: semantic work, evidential work and verification can be priced separately, and an unsupported reinterpretation cannot erase the original task or manufacture a cheaper conclusion. It does not oblige anyone to investigate every imaginable interpretation. Which interpretations are admissible and which claim is being assessed are substantive inputs, not conclusions of the optimizer.

### 6.1 A T20 scope-substitution control

Suppose a retained derivation concludes a result about `complete original production` under interpretation σ0, and a proposed application uses the same displayed words for a different explanatory relation σ1. The original proof object has target (q0,σ0), while the new goal has target (q1,σ1). Without an admitted interpretation-transport proof t, the first certificate is ineligible for the second goal. With such a proof, a combined certificate has the union of the original support and t’s support, and an explicitly priced additional check. A summary that records only untagged proof availability can merge a state with the needed transport evidence and one without it, potentially changing finite completion into an impossible one. Erasing tags alone need not erase a transport token that is separately retained; the failure is precisely the indicated lossy summary.

This does not establish that any particular actual T20 reformulation changes the meaning, nor that a copied label makes either interpretation faithful. The philosophical/source inquiry must establish whether the proposed semantic bridge is warranted. The formal consequence is useful in either direction: a genuine bridge permits economical reuse; its absence cannot be repaired by treating identical vocabulary as identical content.

## 7. Revision and failure boundaries

The evidence and proof identities include the claim and analysis version. A certificate for q0 stays a certificate for q0. To transport it to q1, add a separately warranted semantic-equivalence or implication bridge with its own support and scope; otherwise compile a different target catalogue. Retaining the old certificate and the revision edge then invokes the inherited no-disappearance invariant. The present result does not establish semantic equivalence by comparing strings or making a tensor isomorphism.

The persistence restrictions are sharp. If a proof needs p and q, test a obtains p but expires q, while test b obtains q but expires p, the union of all historically returned tokens is {p,q}. Starting from empty active inventory, no reachable active inventory contains both. A union-of-payloads completion test would wrongly predict success. Similarly, consumption makes repeated use a multiset/linear-resource question, and an unanticipated defeater can invalidate a formerly admissible derivation. In those settings the Bellman method can still be applied to a correctly expanded finite state, but the simple residual-set update and full-transcript criterion are not asserted.

A faithful archive also need not make evidence presently usable. Retrieval, source validation, changed standards and target-version checking may remain necessary. Conversely no absence of a complete epistemological reduction is inferred to defeat ordinary first-order knowledge. The output is a conditional theory of one explicit proof-producing inquiry protocol.

## 8. What is earned, and what it enables next

The earned extension is constructive: the proof rules compile a cost-sensitive completion summary; the summary has an exact characterization and sharp state lower bound; permitted tests yield an exact feasibility criterion and optimum; the semantic-cover rule makes clarification a legitimate, costed alternative to indiscriminate refutation. The checks exercise these claims without substituting enumeration for their proofs.

This offers a reusable discipline for the live foundational arguments. Separate the affirmative derivation from the evidence for its source, semantic and inferential bridges; identify which missing premise tokens would actually permit the next scoped inference; ask only queries capable of supplying them or a genuinely alternative proof; and preserve the original claim's verdict across later reinterpretation. For example, the retained relevant conditional proof can discharge a logical derivation node while its genuine knowing-and-use premises remain distinct application nodes. Filling the first does not silently fill the others.

The same discipline does not decide the Necessary Being, uniqueness or attribute-ascent arguments by itself, change their existing appraisal, or give every merely formulable objection a new investigative entitlement. Those substantive judgements remain with the ongoing affirmative philosophical work.

The next step justified by this theorem would be one small, independently supported instantiation from an actual T20 argument: identify its bounded rule graph and live missing evidence, then compare legitimate next inquiries. Before doing so, the source-trust commitments, admissible semantic family and inference licences must be defended on their own terms. A bigger arbitrary catalogue would not improve that warrant.

## 9. Mathematical ancestry and verification status

Positive provenance already records how outputs depend on alternative and joint premises. Green, Karvounarakis and Tannen's *Provenance Semirings* (PODS 2007), especially §§2–4, is an important antecedent; our persistent support sets forget multiplicity and most full proof structure. The residual construction is a finite monotone-function/residual-language method. Certificate complexity and decision-tree search are established subjects; Buhrman and de Wolf's survey is a reference for their standard distinction. The Bellman recursion is ordinary finite decision-tree optimization, not a newly invented general algorithm.

The contribution is their explicit scoped combination with the retained Orthemology contracts, including priced final verification, version-sensitive semantic cover and the refusal to upgrade observational determination into epistemic warrant. General originality beyond this development is not established.

Proof status: written general proofs; independently reviewed at the stated revision; deterministic exact finite checks in verify.py. No Lean/kernel certification, empirical cost calibration, implementation rollout, or universal natural-language capability is claimed.

References:

- [Retained representation manuscript](https://github.com/theislampill/orthemology/blob/main/theory/lineages/h-formalisation/orthing_formalisation_v1.md), actual local retained version identified in SOURCES.json.
- [Pinned continuation manuscript](https://github.com/theislampill/orthemology/blob/3a0bdeaa1394c656245cae9599adcb143e885059/theory/lineages/h-continuation/continuation_complete_orthing.md).
- [Green, Karvounarakis and Tannen, Provenance Semirings](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf), §§2–4 consulted; no whole-paper read claimed.
- [Buhrman and de Wolf, Complexity Measures and Decision Tree Complexity: A Survey](https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf), certificate and decision-tree definitions consulted; no whole-paper read claimed.
