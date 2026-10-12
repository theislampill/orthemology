# Coalescence, compositional closure, and retained provenance

7 October 2026. New T20 application of ordinary algebra and inherited H continuation criteria. The completed origin report and the reactive-law checkpoint remain unchanged. No metaphysical refutation, pure-mathematical novelty, repository mutation, or owner closure is claimed.

## Findings first, with the typing premise in front

The actual reactive causal interface is **Setting_A × Setting_B → CreatedOutput**. It is not automatically a binary operation on one carrier. An expression such as F(F(a,b),c) needs an explicit **output-code-to-aggregate-summary re-encoding**. It must not feed a created effect back as an original act or turn a group of actors into another original agent.

Conditional on that additional compositional interpretation:

1. An associative idempotent operation with every left and right translation **surjective** has at most one element. Unique reactive responses and commutativity are unnecessary. Thus the three-label reactive law cannot satisfy those conditions on one closed carrier.
2. The exact inherited law is nonassociative: F(F(0,0),1)=2, while F(0,F(0,1))=1. It cannot be a surjective homomorphic image of an associative rich aggregation.
3. It **does** have an exact provenance-bearing computational-tree lift. Retaining grouping makes evaluation a homomorphism. Forgetting grouping fails on the displayed triple. Therefore no impossibility of every rich lift has been proved.
4. Rational mean supplies a different, stronger all-arity rival at the visible-target level. Unique-act-ID records retain provenance under compatible union; a fresh own act can achieve every rational target in each fixed finite peer context. But mean alone is not sufficient for continuation, and sum/count alone is not sufficient for arbitrary alias-aware merging or named suppression.
5. A sharper anonymous ternary obstruction survives without associativity or full label covariance, but a bounded owner-group extension preserves the original binary table and per-slot reactivity by retaining ownership roles.
6. The rational repair is a **changed law and target repertoire**, not a faithful embedding of the original three-label midpoint table. A direct Z3 sum/count repair becomes undefined at counts divisible by three. Full bags avoid some information loss but do not automatically settle all-arity selection or power.

The useful new bridge is exact: a present created-output projection can preserve present success while failing the particular update, admission, and provenance questions the continuation requires. That is an application of the inherited H criterion, not its rediscovery.

## 1. What associativity would mean here

The three positive targets remain Q0={e0}, Q1={e1}, Q2={e0,e1}. Zero is an active target code, not nonbeing. In the retained model each bearer has a setting indexed by its solo-output code. Joint production is

F(a,b)=2(a+b) mod 3.

For this algebraic test alone, identify each created-target **code** with a proposed summary code S for a group of intrinsic input settings. The extra compositional requirement says that two aggregate descriptions can be replaced by their summary codes and combined by the same F without changing the final output. This is the proposed closure whose consequences we test; it is not already part of the two-source model.

Associativity is well motivated for **computational grouping of one fixed unordered input collection**: a choice of parentheses in an analysis should not change what that collection describes. It is also a normal property of compatible record union. It is not a general law of successive efficient causation. The order and grouping of real processes can alter conditions and results. Nor does a two-original, one-act-each proposal automatically include a third composable input.

The numerical separating case below uses three distinct act-description tokens but only bearers A and B. This avoids postulating a third original. Nevertheless it still adds an aggregation/composition scope beyond one current act per original. The no-go is conditional on that scope and re-encoding. It cannot be promoted to an original-agency refutation without warrant for them.

## 2. The exact algebraic obstruction

Let f:X×X→X be associative and idempotent. Suppose every left translation is onto. For fixed a and b, choose x with f(a,x)=b. Then

f(a,b)=f(a,f(a,x))=f(f(a,a),x)=f(a,x)=b.

So f must be right projection. If every right translation is also onto, for any a,b choose x with f(x,a)=b. Right projection makes that value a, hence a=b. The carrier is therefore a subsingleton; if nonempty, a singleton.

This directly covers an associative idempotent quasigroup. More importantly, it covers the weaker power condition actually needed by the rival: existence of a response for every fixed peer and target, without uniqueness. No finite-cardinality premise is used. The theorem does not say that nonassociative idempotent reactive laws are inconsistent.

The retained three-label implementation was imported unchanged. It has 18 associativity failures among its 27 triples. One witness suffices:

- First summarize 0 and 0: their code is 0; combine with 1 to get 2.
- First summarize 0 and 1: their code is 2; combine with 0 to get 1.

These final codes denote different complete created sets in the inherited catalogue. The calculation is a real separating case for the proposed summary interpretation, not another declaration that output keys might hide provenance.

The general proof and the concrete witness are checked in `src/Composition.lean`. Their mathematics is elementary and familiar. The cited quasigroup source already supplies the relevant bijective-translation definition and affine idempotence construction; no new Latin-square result is claimed. [Jedlička, Stanovský and Vojtěchovský, definitions and affine construction](https://cs.du.edu/~petr/data/papers/distributive_and_trimedial_quasigroups_of_order_243.pdf)

## 3. Which richer operation can descend to this exact law?

### A general impossibility for associative homomorphic lifts

Suppose rich states H have associative combination ⊙, and π:H→S is onto. If

π(h⊙k)=F(π(h),π(k))

for every relevant pair, associativity passes through π. Choosing preimages of a,b,c gives F(F(a,b),c)=F(a,F(b,c)). Hence the nonassociative three-label F has no such associative onto lift.

This is the standard homomorphic-image argument, checked here as `associative_image` and `no_associative_onto_lift`. It rules out a **particular package**: associative rich aggregation, the same F on coarse summaries, and a faithful onto composition map. It does not rule out rich aggregation with a final readout that is not itself compositionally closed.

For partial compatible union, the total-operation theorem cannot simply be invoked wholesale. But if the three required preimages and intermediate unions are mutually compatible, imposing that same homomorphism equation on those pairs gives the same separating contradiction. The problem does not disappear merely by calling union partial.

### A positive exact map, with its cost

Take provenance-bearing binary trees whose leaves are labelled intrinsic-act descriptions. A leaf carries an act identifier, bearer and setting. Define E at a leaf by its setting and recursively define

E(Node(t,u))=F(E(t),E(u)).

This is an onto homomorphism from the computational tree operation Node to F. The internal nodes are calculation structure, not new intrinsic agents or asserted created intermediate effects. `tree_evaluation_hom` and `tree_evaluation_onto` check the map.

Choose leaves alpha1:A/0, beta:B/0, alpha2:A/1. Both bracketings have exactly the same flattened multiset of leaves, but their evaluations are 2 and 1. Thus E does not factor through flattening to that unordered bag. The precise information lost is the grouping that fixes the computation's effective weights. If such grouping is physically irrelevant, this lift is not an adequate account of the intended unordered production. If grouping belongs to the actual law, it must be retained and explained.

The distinction matters: **provenance retention is possible; associative output-only reduction is what fails.**

## 4. Stronger rational repair with unique actual-act identity

A different candidate uses rational setting labels. Each rational labels a positive source-neutral created profile; 0 remains a positive label and only the empty input has no output. Rational labels are neither physical amounts of divine work nor positive/negative quantities of created matter.

A rich state is a finite map

act identifier ↦ (bearer, intrinsic setting, intended target).

Only A and B are represented as original bearers. Several records may be distinct acts of the same bearer. The mean of the settings is the visible created-target code. All participating root identities are retained in the map and extracted separately from the output.

Compatible union of maps is commutative, associative on compatible triples, and idempotent as **record merge**. Conflicting descriptions of one act ID are rejected. Restricting to finite submaps of one globally consistent assignment yields an ordinary total semilattice, but that restriction must not silently remove the changing-setting contexts used by the ability claim.

### Aliasing is not additional agency

Merging a record for alpha with another copy of that same alpha leaves one act. Merging distinct alpha:A/q and beta:B/q produces two records even though the settings coincide. Both visible means are q. The richer actual support differs.

Thus two kinds of idempotence must not be confused:

- Repeating a representation of the **same act** is idempotent even at the full map level.
- Adding a **different real act** with the same setting is idempotent only at the visible-mean level; the full map gains that act.

Count and provenance are metadata describing intrinsic exercises in this candidate. Their retention does not by itself add created entities, a mixer, or another original agent. Conversely, if a physical implementation really introduces created inputs or mechanisms, they must enter its created-history accounting. Neither ontology follows merely from using a dictionary.

### Full contextual response survives at the visible interface

If a fixed finite peer state contains n acts with settings summing to s, a fresh A-act with setting

x=(n+1)q−s

makes the resulting mean q. The same construction works with roles exchanged. Rational closure provides the standing setting repertoire. The ordinary same-goal policy selects q for each bearer; at (q,q), the created profile is q and both stored intentions and own-activity ends hold. Suppressing beta while retaining alpha preserves q and alpha's own end. Supports change {A,B}→{A}, and the complete rich state changes.

This response is not one fixed setting that guarantees q against arbitrary peer changes. It is not a secret sequential strategy: knowing the fixed peer context is the same epistemic condition as in the earlier contextual-power test. Nor does the construction establish that every such context is an admissible perfectly wise world.

The code binds own-end satisfaction to the **stored goals** of the relevant bearer's acts. Merely passing a matching target to a participation function does not override an incompatible recorded intention. Tests include that negative control.

### Why there is no contradiction with the no-go

The properties now occur at different signatures:

- Compatible full-state merge is associative/idempotent.
- Full reactive controllability concerns the **visible mean**.
- A full-state translation is not onto: merging any own records with a retained peer record cannot produce a state lacking that peer record.
- Mean is not a homomorphism into an unweighted binary midpoint operation over arbitrary groups of different size.

One may not combine associativity from the full map with surjectivity from its visible projection and pretend the theorem's single-carrier hypotheses have been met.

The construction establishes the stated algebraic abilities and reduced participation interpretation. It does not reproduce the richer cognition model, establish unrestricted omniscience, prove source-faithful original efficacy, or derive the wisdom of the policy. Equal per-act weighting also needs a real individuation convention: arbitrarily splitting one act-description into two cannot be treated as adding two new actual acts. Unique-ID alias control prevents duplicate records, but is not a metaphysical theory of act granularity.

## 5. Exactly what output-only and intermediate summaries lose

### Mean alone loses continuation weights

Let h={alpha:A/0}, h'={alpha:A/0,beta:B/0}. Both visible means are 0. Append the same fresh alpha2:A/1:

- h becomes mean 1/2.
- h' becomes mean 1/3.

No function of the present mean alone can predict that continuation. Likewise, to achieve future target 1 by one fresh act, the required settings are 2 and 3 respectively. Present target equivalence does not preserve the next response-selection problem.

### Sum/count repairs disjoint append, with an exact commuting map

Define r(h)=(s,n). For disjoint act maps,

r(h∪k)=(s_h+s_k,n_h+n_k).

This is a genuine homomorphism on that declared disjoint composition class. The output is s/n for n>0. In mean/count coordinates the induced operation is weighted averaging with weight n, not repeated unweighted midpoint. These states retain what is needed for repeated disjoint additions, and their aggregation is associative. The full (s,n) state is not idempotent under addition of distinct equal-setting acts.

This positive repair is scope-sensitive. A fixed fresh-ID append commutes on a domain where that identifier is absent. Sum/count alone does not establish that freshness condition for arbitrary commands.

### Even sum/count plus root support loses arbitrary alias-aware merging

Take x={alpha:A/2} and y={beta:A/2}. Both have summary (2,1), the same root support {A}, and visible mean 2. Merge each with the same compatible z={alpha:A/2,gamma:B/4}:

- x∪z has two actual acts, sum 6 and mean 3.
- y∪z has three actual acts, sum 8 and mean 8/3.

Thus **no arbitrary summary-only update**, not merely the naive additive formula, can implement all compatible alias-aware merges. The omitted fact is whether the incoming identifier already names an act in the state. The full ID map repairs it.

### Named suppression and action admission need more again

Maps {alpha:A/0,beta:B/2} and {alpha:A/1,beta:B/1} have equal sum/count, root support and mean. Suppressing the alpha record leaves means 2 and 1. Per-act settings are needed for that named intervention.

Maps {alpha:A/0} and {alpha2:A/0} also have equal summaries and root support, but differ on whether alpha is a fresh available identifier. Thus the admitted continuation menu need not descend to sum/count even where the output and a pre-authorized disjoint update do.

These are different losses: grouping, multiplicity/weight, overlap identity, per-act setting, root attribution, and permitted continuation are not interchangeable pieces of provenance. The full ID map is sufficient at this declared interface, not proved globally minimal. No finite-dimensional impossibility is inferred; unrestricted encodings, including infinite-precision ones, are outside this claim.

## 6. Can the rational repair preserve the original Z3 law?

Not by a noncollapsed midpoint embedding. Let v0,v1,v2 in a rational vector space represent the three original labels. Preserving F(0,1)=2 and F(0,2)=1 requires

2v2=v0+v1, and 2v1=v0+v2.

Subtracting gives 3(v2−v1)=0, so v1=v2, then v0=v1. Every homomorphism of that form collapses the three labels. An exact rational row-reduction control checks these linear equations. This is a general algebraic argument, not just the failure of the natural inclusion 0,1,2 into the rationals.

The rational mean model therefore changes both the law and its available target/setting family. It preserves the important **pattern** of contextual response, diagonal agreement, own-end success and nonexclusive provenance. It does not preserve the original complete table or its particular three event-set catalogue. It is a new rival repair, not a transport theorem for the original model.

Alternatively retain Z3 and store (sum modulo 3,count). A mean is defined when count is invertible modulo 3, including one and two acts. At count three the inverse does not exist. More decisively, unanimous bags 000,111,222 all have summary (0,3). No decoder of that summary can give their required distinct unanimous outputs. This obstruction does not affect the original two-act model; it affects the proposed unrestricted n-ary extension.

Retaining the complete setting multiset distinguishes those unanimous bags. It still does not automatically supply an all-arity law. If readout depends only on that unordered multiset and remains equivariant under all permutations of the three outcome labels, the balanced bag {0,1,2} is fixed by every permutation while no single output label is. A deterministic total decoder is impossible under those conditions. The abstract fixed-input/no-fixed-output lemma is checked in Lean.

The three abstract labels are not semantically interchangeable in every respect: Q2 has two created events, whereas Q0 and Q1 each have one. Event-renaming e0↔e1 only swaps 0 and 1 and fixes 2. A concrete total extension keeps the exact one/two-act law, then uses the union of the represented solo event sets for bags of three or more acts. It preserves unanimity, unordered-act symmetry and that event-renaming symmetry; it selects Q2 on the balanced bag. It breaks the stronger abstract S3 symmetry. It also loses full higher-arity reactivity: against two fixed setting-0 acts, changing a third setting yields only Q0 or Q2, never Q1. This is a checked positive selection rule and a checked ability failure, not an exhaustion of alternative decoders.

Full act/bearer provenance can support an additional selection rule that breaks the relevant symmetry; grouping can also select an output. Those are additional features, not an unnoticed contradiction. Source-neutral **output content** does not mean that a law is forbidden to consult actor roles. No universal impossibility of every provenance-sensitive finite extension is claimed; the bounded positive owner-group construction below illustrates the distinction. Such a rule must separately re-establish whichever reactive abilities and symmetries are required.

### A sharper ternary obstruction, with a positive ownership control

After the initial report was drafted, the parent independently found a stronger finite obstruction. This lane independently enumerated the same narrow class: ten unordered triples over three labels, three unanimous values fixed, seven values free, hence 3^7=2,187 symmetric idempotent ternary tables. None makes every fixed-pair translation onto all three labels. This result needs **neither associativity nor full output-label covariance**.

There is a short complete proof. By renaming the labels of the candidate table for the proof, let f(0,1,2)=0. This is not an assumption that the table itself is equivariant. Symmetry and the permutation property of every fixed-pair translation give:

1. f(0,1,1) cannot be 0, because f(0,1,2)=0; it cannot be 1, because f(1,1,1)=1. Therefore it is 2.
2. The fixed pair (1,1) now forces f(1,1,2)=0.
3. The fixed pair (1,2) has the same value 0 at third inputs 0 and 1, contradicting bijectivity.

Onto is equivalent to bijective for these three-element translations. The proof covers the specified symmetric ternary class completely, not all higher-arity laws or all models of two original bearers. Full **per-act-slot** response while all other slots are fixed can be stronger than a bearer's power to change several of its own acts together. Input-slot anonymity is also a substantive requirement when the slots have different ownership roles.

A positive control makes that last assumption explicit. For three slots owned (A,A,B), average the two A-settings within A, then average that result with B's setting. Over Z3 this gives

G(x,y,z)=x+y+2z mod 3.

It is unanimous/idempotent, surjective in each slot, and symmetric between A's two slots. Swapping the names A and B while preserving the ownership partition leaves the owner-group construction unchanged. It is not anonymous across an A-slot and the B-slot. With exactly one act per bearer it recovers the original binary F, so this is a **faithful bounded provenance-sensitive extension**, unlike the rational midpoint embedding rejected above.

The code tests the exact owner-group map and all 27 ternary inputs. The two owner-tagged states A:0,A:0,B:1 and A:1,A:0,B:0 have the same unordered setting multiset but yield 2 and 1. Ownership information is therefore essential to this decoder. Compatible ID-map union still aggregates the descriptions associatively; the final decoder does not factor through settings-only flattening or through the original F as an output-only compositional law.

This extension remains partial where an active owner's act count is divisible by three. It does not establish every arity, every act-individuation convention, or perfected original agency. Owner metadata is not an additional created entity or a third original. The result sharply narrows the obstruction: anonymous symmetric ternary reactivity fails in the three-label class, while the disclosed ownership-sensitive typed interface survives at the tested scope.

## 7. Concrete transport to inherited H continuation interfaces

The historical source at commit fd0903d99d657c35e32fddcc8864d2a77930cf40 was directly inspected through the retained Git object. H-formalisation Theorem 4.2/Corollary 4.3 already give the fibre criterion; Theorem 11.2 requires the represented update, target and inquiry landscape all to descend. Its composition discussion explicitly warns about shared evidence, aliases and duplicate obligations. These are inherited ordinary results. [H-formalisation](https://github.com/theislampill/orthemology/blob/fd0903d99d657c35e32fddcc8864d2a77930cf40/theory/lineages/h-formalisation/orthing_formalisation_v1.md)

Here is the actual deterministic application:

- D: compatible finite act-record maps.
- r0: current visible mean.
- q: current created-profile code.
- F_c: union with a declared compatible incoming map c, or a specified fresh append on its eligible domain.
- l: the permitted fresh-ID command menu, if admission is part of the required interface.

The mean-equal states in §5 violate constancy of r0∘F_c. Therefore there is no descended update preserving the next mean. The sum/count map r1 positively commutes with disjoint append, but the alias and freshness witnesses show failures for broader F_c and l. Full per-ID maps retain the information required by those exact operations. This is an actual map, commuting equation, and separating counterexample; it is not an analogy between theology and an audit vocabulary.

The H-continuation supplement's closure under admitted continuations is the broader methodological ancestor. Its finite-state linear-observable, stochastic and dimension theorems are not imported into this unbounded rational map model. [Continuation supplement](https://github.com/theislampill/orthemology/blob/fd0903d99d657c35e32fddcc8864d2a77930cf40/theory/lineages/h-continuation/continuation_complete_orthing.md)

The prior `causal-abstraction/RESULT.md` already applies the same fibre idea to causal-route and intervention loss. New credit here is the specific reactive-law composition application and the positive bounded repair. The T08 shared-root overview was checked for ancestry: its source-store aliasing obstructs a literal label-state pullback and motivates a scoped alternative simulation. Our act-ID example is not that controller theorem or a new independent discovery of alias hazards. No map from its runtime into the present causal model has been supplied, and no T08 acceptance or replay claim is inherited.

## 8. Philosophical result and remaining warrant

The source's nonabsorption and whole-original-efficacy arguments are not equivalent to associativity. Majmu's stronger objection is already about two unchanged genuine productive agents; it need not wait for a third composable slot. Conversely, the reactive rival need not accept an output-only associative summary merely because it uses the same code set for solo settings and results.

The defensible new verdict is conditional:

- The exact three-label rival fails a proposed associative, output-only compositional extension.
- Rich descriptions can retain the distinctions that extension discards.
- A rational all-arity law repairs visible contextual power with associative bookkeeping, but its semantics and target family change.
- Preserving actual support in records does not make support into an extra created object, nor establish that this primitive joint manifestation is a perfected original exercise.

The remaining obligations are the independent metaphysical meaning of the primitive law, real act individuation, any intended grouping/weighting, admissible intervention policies, and the source's norm of actual original efficacy. Associativity does not settle them without a warranted typed composition contract.

## 9. Verification scope

Nine Lean declarations compile with only ordinary foundations (`propext` where reported), no custom axioms or sorry. Twenty-seven Python checks pass, importing the exact reactive law unchanged. The rational response formula and vector-space collapse have ordinary general proofs above; finite checks verify their displayed implementations and witnesses, not every metaphysical interpretation.

An independent reviewer checked the algebra, the computational lift, and the first sixteen executable controls. Its qualifications led to the explicit partial-union scope, general collapse proof, stronger alias witness, balanced-bag symmetry condition and stored-intention negative test. The final twenty-seven tests and Lean replay were rerun by this lane; no independent final replay is claimed.

Prospective events, input hashes, outputs and commands accompany this report. Earlier source archives, the completed origin lane, and protected state were not modified.
