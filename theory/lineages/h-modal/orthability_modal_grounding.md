---
title: "Orthability and Necessary Being"
subtitle: "Modal support, concrete grounding, and the common-bearer frontier"
author: "Research synthesis for the Orthemology project"
date: "8 September 2026 — research supplement 02 / v2"
abstract: |
  This follow-up moves from continuation-complete representations to the modal and metaphysical argument itself. It separates necessary truth, necessary instantiation, necessary existence of one bearer, uniform underivability, and necessity in itself. Two actual-explanation routes give positive, explicitly conditional necessary-existence theorems; a stronger possible-dependence theorem identifies the extra structure needed for uniform underivability. A finite support calculus then isolates the difference between indispensable individuals and non-removable joint support. Minimal cuts characterise modal failure, determine the exact interaction arity required for a universal modal audit, and give a sharp worst-case query count. An infinite extension states the compactness and recombination assumptions needed to extract a necessarily active support. Conservative modal constructions preserve the operational findings while withholding necessary individual or mental bearers, and a joint impersonal-root model survives even several strengthened grounding premises. An essential-ownership route to a necessary mental bearer is reconstructed, with knowledge requiring a further truth-linked condition. A modal-collapse analysis keeps necessary existence compatible with contingent effects and distinguishes the further attribute and revelation claims. Primary philosophical and Arabic-text comparisons constrain the interpretations. Ordinary proofs, exact finite checks, and three locally checked natural-deduction certificates support the formal results, not the truth of their metaphysical premises. The deliverable advances the premise and countermodel frontier; it does not claim a completed world-directed Necessary-Being proof, general novelty, or a certified meniscus breach.
---

# Research target and substantive advance

This is the requested modal and metaphysical successor to *Continuation-Complete Orthings* [I1]. The target is a contribution **to Orthemology's orthability-to-Necessary-Being programme**, not another use of the framework to classify a fluid proof.

The earlier supplement asked which information a representation must retain to evaluate its permitted continuations. Here the central question is different:

> What additional, precisely identifiable conditions allow the reality of evaluable orthing to support a conclusion about an actual, necessary, underived, and ultimately knowing ground?

A positive answer must not turn a necessary condition into an entity merely by naming it; exchange a world-dependent witness for one necessarily existing individual; infer a mind from a representation's tensor shape; or make a desired conclusion true by putting it into a definition. A negative answer must not merely repeat that a premise is missing. It should identify the obstructing architecture, prove what it preserves, and show which alternative mechanism would exclude it.

The principal advances of this packet are fourfold. First, it supplies complete conditional deductions of necessary concrete actuality, with two genuinely different explanatory routes and an additional cross-world foundation result. Second, it introduces a modal support audit with sharp information bounds: exactly which joint absences must be ruled out, at what arity, and with how many worst-case questions. Third, it constructs integrated controls rather than relying only on isolated predicate deletions. Fourth, it analyses the transition to a knower and the preservation of contingency, including a source-sensitive comparison with arguments that actually attempt these steps.

## The inherited boundary

The representation-first headline is unchanged:

$$
\mathsf{Orthing}_A,\qquad e\in E_A,\qquad
\rho_A:E_A\longrightarrow T_{\mathcal T}(V).
$$

The symbol $\mathcal O$ remains reserved for the ortheme universe. A finite-support tensor representation is not an orthing's ontology. The objective prospective landscape $\mathcal L_t$, its information-relative certifiable subset, and the historical ecology $\Gamma_t^\mu$ remain distinct. Nash structure is optional and declared. The prior continuation and information-dimension results are retained at their original scope; none is now promoted into a metaphysical premise.

The new modal notation below is an extension-specific language. In particular, a selected set of possible worlds is not silently identified with the complete metaphysically possible domain, and a source-labelled proposition is not silently made true.

## Inputs, authority, and scope of work

The local inputs are both previous research packages, the supplied Euler and Navier–Stokes PDFs, the discussion and screenshot, and the two-page CDC campaign prompt [I1–I6]. The CDC document is used for its research discipline: distinguish approach families, preserve rival routes, reject equivalent-strength hidden lemmas, demand exact statements, and test failures before declaring completion. Its description of an eight-hour, 64-agent run is not an account of this execution. No concurrent research agents were available or used. The present work is a single-assistant campaign with separately implemented checkers, not independent-agent peer review.

The repository basis was freshly pinned to `f50dc1aee52356cc6adbef342387576b02afc124`. Targeted reads covered the companion argument, its later authority qualification, the bridge ledger, R5, the meniscus charter, and relevant existing proposals [R1–R9]. This is not an audit of every repository file. No repository, issue, branch, release, or owner ledger was changed.

The source distinction matters. The companion's historical positive language is qualified by the later Track T and B0–B16 owners. They do not currently certify a deductive Necessary-Being result. These are the starting statuses, not prohibitions on new reasoning. The results below are new candidate work relative to the delivered packet; they do not retrospectively change historical authority.

## Exact objectives

We separate the following targets rather than using “Necessary Being” as one undifferentiated conclusion:

$$
\begin{aligned}
\mathsf{NB}_{\exists}&:\quad\text{some concrete actual bearer exists necessarily};\\
\mathsf{NB}_{\mathrm{u}}&:\quad\text{some such bearer is underived throughout the modal scope};\\
\mathsf{NB}_{\mathrm{ess}}&:\quad\text{necessity in itself under a defended theory of essence};\\
\mathsf{NB}_{\mathrm{k}}&:\quad\text{a necessary bearer is genuinely knowing};\\
\mathsf{NB}_{\mathrm{int}}&:\quad\text{the relevant grounding and attribute roles belong to one bearer}.
\end{aligned}
$$

Universal Creatorhood, Life, Wisdom, Speech, an actual disclosure, and identification with the authenticated revealed referent are further claims. A proof of the first line is not a proof of all later lines.

This does not presuppose that a theological argument must be empirically rather than rationally warranted. Independent warrant may be a priori, experiential, source-based, or revelational where appropriate. The requirement is to identify and defend it, not to require a laboratory experiment for every metaphysical premise.

# A typed modal language

## Worlds, existence, and actuality

Let $\mathbb W$ be a nonempty set of accessible alternatives containing the actual world $\omega_*$. Let $\mathbb D$ be an outer domain of candidate bearers, with explicit existence predicate

$$
\operatorname{Ex}(\omega,g).
$$

Quantifying over $g\in\mathbb D$ does not assert that $g$ exists in any world. Existence is stated by $\operatorname{Ex}$. For the concrete-grounding routes, the candidate sort is expressly a sort of potentially concrete actualisers, not abstract proposition-types. Where this interpretation is not warranted, the theorem remains a theorem about a formal sort.

At the distinguished evaluation point, write

$$
\Box_*\varphi:=\forall\omega\in\mathbb W\;\varphi(\omega),
\qquad
\Diamond_*\varphi:=\exists\omega\in\mathbb W\;\varphi(\omega).
$$

This is sufficient for the main arguments. It does not assume S5. A general Kripke relation can be used by taking $\mathbb W$ to be the successors of $\omega_*$; the actual-world inclusion is then a reflexivity condition at that point. Stronger modal principles are introduced only where separately stated.

Define

$$
\mathsf N_{\exists}(g):=\Box_*\operatorname{Ex}(\omega,g).
$$

An actually existing $g$ is modally contingent in this sense if $\neg\mathsf N_{\exists}(g)$: there is an accessible alternative in which it does not exist. This is a de re claim about the same individual, not about a role occupied by potentially different individuals.

Let $h\prec_\omega g$ mean that $g$'s existence or relevant existential efficacy is derived from $h$ **in one fixed explanatory respect**. The intended grounding relation is not identical to epistemic warrant, a proof-premise relation, temporal succession, or a software dependency. A model can represent these relations, but their interpretation must be supplied independently.

Write

$$
\mathsf{Root}_\omega(g)
 :=\operatorname{Ex}(\omega,g)\land
   \neg\exists h\,(h\prec_\omega g),
$$

and

$$
\mathsf N_{\mathrm u}(g):=\Box_*\mathsf{Root}_\omega(g).
$$

Uniform underivability is stronger than actual underivability together with necessary existence. Necessity in itself, denoted $\mathsf N_{\mathrm{ess}}$, is not defined away as either formula. The intended essential or source-theological meaning needs its own interpretation. In particular, modal invariance of existence does not automatically settle what explains that existence or what belongs to the individual's essence [P6].

## Five modal levels that must not be exchanged

For an evaluability condition $q$ and an alleged bearer relation $H(\omega,g,q)$, distinguish:

$$
q(\omega_*),\quad
\Box_*q,\quad
\Box_*\exists g\,H(\omega,g,q),\quad
\exists g\,\Box_*H(\omega,g,q),\quad
\exists g\,\mathsf N_{\mathrm{ess}}(g).
$$

The third formula allows a different bearer in every world. The fourth does not. The fifth additionally makes a claim about intrinsic necessity, rather than merely a pattern of occurrence or role occupancy.

**Countermodel 1 — Rotating witnesses.** Take two worlds and two individuals. Only $a$ exists at the first world, only $b$ at the second, and the existent individual bears $q$ there. Then $\Box_*\exists g\,H(\omega,g,q)$ is true and $\exists g\Box_*\operatorname{Ex}(\omega,g)$ is false. Both worlds may contain objectively correct evaluations and complete local reasoning practices. This is a formal countermodel; it is not by itself a verdict that those worlds are metaphysically possible.

**Countermodel 2 — Rotating roots.** Let both $a$ and $b$ exist in both worlds. At the first world, $a\prec b$; at the second, $b\prec a$. Each world has a finite, acyclic dependence order and a unique underived root. Both individuals exist necessarily. Neither is underived throughout the two-world scope. Thus worldwise foundation and unique roots do not alone yield $\mathsf{NB}_{\mathrm u}$.

## Necessitation is not premise promotion

From actual evaluability and a valid conditional

$$
\operatorname{Eval}(\omega_*) ,\qquad
\Box_*(\operatorname{Eval}\to q)
$$

one obtains $q(\omega_*)$. One does not thereby obtain $\Box_*q$. A modal rule of necessitation applies to a theorem of the relevant logic, not to every actual, contingent premise used during reasoning.

Likewise, $\Diamond_*\Box_*P$ is not generally equivalent to $\Box_*P$. Under S5 it is, which means that simply postulating possible necessary existence there does not supply an independent reason for the desired conclusion. The existential identity and domain clauses also have to be preserved. A modal-ontological route is a legitimate separate programme, but its possibility premise cannot be treated as a cheap substitute for the grounding argument.

# What the transcendental launch establishes

The repository distinguishes local analysis-relative aptness, objective conditions of evaluability, and created representations or applications [R1]. Preserve that distinction. Denote the objective family by $\mathsf{OrthabilityO}$ without treating it as a new entity.

The strongest plausible starting point is not merely “people produce classifications.” It is that some evaluations really are true: a particular inference is invalid, a distinction is real, an error is an error even when the relevant actor endorses it. This realism provides a substantive explanandum. It is stronger than observing agreement, and it does not require identifying truth with a chosen scoring rule.

A modest transcendental implication can then be stated:

$$
\text{an actually true evaluation}
\Longrightarrow
\text{the determinations required for its truth actually obtain}.
$$

What those determinations are depends on the evaluated claim. A modal evaluation, such as reliability across a specified class of alternatives, carries its modal conditions; a token's mere existence does not automatically carry absolute metaphysical modality.

## The anti-total-generation argument

An account that purports to generate **every** condition of determinacy through a determinate process already uses at least the distinction between its inputs and outputs, the identity of the process, and a condition distinguishing successful production from failure. This blocks the claim that the same complete structure is both wholly absent and wholly responsible for its own determinate production in the same respect.

This is not yet an existence proof of a positive external ground. It distinguishes a defective construction account from other possibilities: ungrounded determinate reality, primitive powers, an infinite dependence structure, a non-generative account of conditions, or an underived ground. Nor does a metalanguage's need for coherent description automatically make that metalanguage an ontologically prior entity.

The later source-Horn calculus makes the limited no-bootstrap claim exact. It will show that no positive least-closure construction produces content without a seed or an explicitly seed-like rule. That result is about its declared generative semantics. Whether an ontological account must obey those semantics is precisely a bridge to defend, not a conclusion of the code.

## The productive change in route

We should not demand that the negative no-self-generation result, by itself, yield a positive ground. There are other routes into a necessary-existence conclusion. Two are developed next:

- an **actual-ancestry route**, starting from an actual concrete bearer and a non-self-sufficient contingent existence principle;
- a **total-explanation route**, starting from the contingent existential totality and a full explanation that projects to its members.

Both are cosmological side routes entered through the actuality of orthing. Neither is silently relabelled as the original transcendental argument. They can supply a ground for further investigation while leaving the distinctive grounding of truth, normativity, and intelligibility open.

# Positive route I: actual ancestry

## The theorem

Fix a nonempty set $C$ of actually existing concrete candidates, containing the relevant ancestor cone of an actual orthing bearer. Use the restriction of $\prec_{\omega_*}$ to $C$.

**Theorem 1 — Necessary actuality in a complete well-founded ancestor cone.** Assume:

1. Every member of $C$ exists concretely at $\omega_*$.
2. The relation $\prec_{\omega_*}$ is well-founded on $C$: every nonempty subset of $C$ has a member with no predecessor in that subset.
3. Every $g\in C$ with $\neg\mathsf N_{\exists}(g)$ has a predecessor $h\in C$.
4. The cone includes every predecessor capable of changing the relevant root classification.

Then some $g\in C$ is an actual underived concrete bearer and satisfies $\mathsf N_{\exists}(g)$.

*Proof.* Well-foundedness applied to the nonempty set $C$ gives a member $g$ with no predecessor in $C$. If $\neg\mathsf N_{\exists}(g)$, assumption 3 supplies such a predecessor, a contradiction. Hence $\mathsf N_{\exists}(g)$. Assumption 1 supplies actual concreteness, and assumption 4 prevents an omitted outside predecessor from invalidating the root classification. $\square$

This is a complete conditional proof of $\mathsf{NB}_{\exists}$. It does not make an uncaused object necessary by definition. It uses the independently stated thesis that an actually existing contingent candidate cannot be existentially self-sufficient in the declared respect.

The quantified inference core—actual root, contingent-dependence principle, and the meaning of root—has a 21-node natural-deduction certificate. The general well-foundedness argument is a paper proof, not part of that certificate.

## What does the work

The relevant principle is

$$
\operatorname{Ex}(\omega_*,g)\land\neg\mathsf N_{\exists}(g)
\Longrightarrow
\exists h\; h\prec_{\omega_*}g.
$$

It is more than the denial that an object causes itself. The latter still allows an uncaused contingent thing. It is also more than the claim that contingent existence is intelligible or distinguishable from nonexistence. A determinate truth can be posited as brute without formal contradiction. The principle is an explanatory commitment: contingent existence has a non-self-sufficient actuality requiring a further actual ground.

This is a serious positive metaphysical proposal. Its supporting rationale is that a nature compatible with absence does not, merely by that compatibility, account for its actual instantiation. Its strongest rival replies that determinateness of actuality need not be accompanied by an additional sufficient existential explanation. The theorem identifies that disagreement rather than resolving it by calling the rival unintelligible.

Well-foundedness is another substantive premise. It is not established by a finite episode trace, a finite proof tree, a finite simulation, or the algebraic tensor algebra. It applies to existential dependence in the specified respect, not to every temporal sequence. Moreover, philosophical foundationalism need not always mean that every possible presentation of every grounding chain terminates; more nuanced structures have been studied [P4]. The present theorem uses the exact mathematical minimal-element condition stated above.

## A narrower sufficient condition and honest minimality

The inference only needs a genuine root in a complete actual cone. Full well-foundedness is one sufficient way of obtaining it, not a necessary condition for the existence of any root. A structure can contain a root together with an unrelated infinite descending chain. We therefore do **not** describe the four-premise package as globally deletion-minimal across all possible proofs.

At the exact inference core, however, each ingredient has a clear role: an actual root must exist; its rootedness must exclude the relevant predecessor; and non-necessary actuality must require such a predecessor. The last two contradict contingent-root status. Concreteness is in the subject matter of the premise, not manufactured by the proof.

## Countermodels and scope

A single uncaused contingent actual object satisfies actual existence and foundation but violates the contingent-dependence principle. An infinite chain $\cdots\prec g_2\prec g_1\prec g_0$, all actual and contingent, satisfies predecessor dependence but lacks foundation. A truncated graph may falsely exhibit a root when its real predecessor lies outside the represented cone. An abstract foundation does not establish a concrete actualiser. A temporal sequence is not automatically a chain in the existential grounding relation.

Even the successful conclusion supplies only actual underivability plus necessary existence. Countermodel 2 shows why it does not yet supply uniform underivability, much less a particular theory of essential necessity, one common bearer, or a mind.

## An essential-necessity variant

A source tradition may classify every actual candidate as either necessary in itself or existentially possible in itself, with the latter requiring a further actualiser. If that taxonomy and dependence principle are independently defended, the same well-founded argument yields an actually necessary-in-itself root.

Formally, for any predicate $\Phi$, a nonempty well-founded cone in which every $\neg\Phi$ member has a predecessor contains a minimal $\Phi$ member. Substituting $\mathsf N_{\mathrm{ess}}$ is therefore mathematically valid **only with the corresponding essential-contingency premise**. It is not licensed merely because the modal-existence version was proved first. This parametric observation prevents an equivocation; it does not constitute a new proof of the source's essential taxonomy.

# Positive route II: a full explanation of contingent existence

The second route does not assume that every dependence chain is well-founded.

Let

$$
C_*:=\{g\in\mathbb D:\operatorname{Ex}(\omega_*,g)
                         \land\neg\mathsf N_{\exists}(g)\}.
$$

Freeze this actual-world selection across alternatives and define the content

$$
\tau(\omega):=\forall g\in C_*\;\operatorname{Ex}(\omega,g).
$$

This is the joint existential content of the actual contingent candidates. It is not the material tautology “all actual things actually exist,” nor an additional concrete aggregate created by notation. $C_*$ is fixed at the actual world; its members can be absent elsewhere. If $C_*\ne\varnothing$, then $\tau$ is true actually and false at some alternative, since any selected contingent member has an absence witness.

Let $\operatorname{TG}(g,\tau)$ mean that $g$ gives a full actual existential explanation of this content, and $\operatorname{GE}(g,h)$ mean that it explains $h$'s existence in the same relevant respect.

**Theorem 2 — A complete actual explanation is not one of its contingent members.** Suppose:

$$
\exists g\,[\operatorname{Ex}(\omega_*,g)\land
                 \operatorname{Concrete}(g)\land\operatorname{TG}(g,\tau)],
$$

and the explanation projects to every selected member,

$$
\operatorname{TG}(g,\tau)\Longrightarrow
       \forall h\in C_*\;\operatorname{GE}(g,h),
$$

while complete same-respect self-explanation is excluded for every candidate,

$$
\forall g\;\neg\operatorname{GE}(g,g).
$$

Then some actual concrete total explanator exists necessarily.

*Proof.* Choose the actual concrete explanator $g$. If it were not necessarily existent, it would belong to $C_*$. Projection would then give $\operatorname{GE}(g,g)$, contrary to the third premise. Therefore $\mathsf N_{\exists}(g)$. $\square$

The predicate $\operatorname{TG}$ must retain its full explanatory meaning. Merely possessing a true sentence about the totality, causing one component, describing a conjunction, or being an ancestor of each member is not automatically a full existential explanation. The component-projection premise is also substantive for the chosen kind of explanation.

If there are no actual contingent members, an independently supplied actual concrete witness already satisfies $\mathsf N_{\exists}$. Thus the two cases can be stated without assuming the contingent totality is always nonempty.

## Why this is a distinct route

The theorem tolerates infinite, cyclic, or non-well-founded structures elsewhere, provided a full explanation of the selected existential totality exists and projects as stipulated. It replaces the local foundation premise by a **global explanatory-totality premise**. It therefore does not solve the regress dispute for free: the rival may deny that such a total explanation is available, or reject the alleged projection in the relevant explanatory category.

The proof is recognisably related to cosmological totality arguments, including the concern that explanations of each member in a series need not explain the series' existence [P1]. It is not a new general proof of theism. Its contribution here is to keep the exact source of positive existence, domain completeness, self-explanation exclusion, and necessity classification visible.

An 18-node natural-deduction certificate checks the core inference from the three displayed premise schemas. Exact finite enumeration separately tests 33,032 structures over up to three entities; 753 satisfy its premises. Neither exercise verifies that the actual universe's contingent-existence totality has the proposed explanation.

## A source-sensitive comparison

The Arabic Asfahani commentary distinguishes mere necessary-existence conclusions from establishing a Maker, and separately discusses originated or dependent actuality [P3]. Our use is narrow: the necessary-existence theorem is one stage, not already the full theological conclusion. The text also criticises a particular attempted unity proof; this packet does not attribute that criticised proof to Ibn Taymiyya as his endorsement.

The primary transcription and the existing repository dossier [R8] are not identical kinds of evidence. The former improves access to the wording; neither by itself proves the metaphysical premises are true. Printed-edition pagination and specialist source interpretation remain distinct from successful text retrieval.

# A stronger modal foundation theorem

The difference between actual rootedness and uniform underivability deserves a positive treatment, not only a warning.

Let

$$
\mathbb D_\Diamond
 =\{g:\exists\omega\in\mathbb W\;\operatorname{Ex}(\omega,g)\}
$$

be a nonempty domain of potentially concrete candidates. Assume $\prec_\omega$ has existing endpoints. Define the possible-dependence relation

$$
h\prec_\Diamond g
\quad\Longleftrightarrow\quad
\exists\omega\in\mathbb W\;h\prec_\omega g.
$$

**Theorem 3 — Uniform underivability from possible-dependence foundation.** Assume $\prec_\Diamond$ is well-founded on the complete domain $\mathbb D_\Diamond$, and that for every world,

$$
\operatorname{Ex}(\omega,g)\land\neg\mathsf N_{\exists}(g)
\Longrightarrow
\exists h\;h\prec_\omega g.
$$

Then some concrete candidate satisfies $\mathsf N_{\mathrm u}$.

*Proof.* Select a $\prec_\Diamond$-minimal member $g$ of the nonempty domain. It exists at some world $\omega$. If it were modally contingent, the displayed principle would provide an actual predecessor there and therefore a $\prec_\Diamond$ predecessor, a contradiction. Thus $g$ exists in every world. Its minimality excludes a predecessor in any world. Consequently $\Box_*\mathsf{Root}_\omega(g)$. $\square$

This theorem is stronger than Theorem 1, but its foundation assumption is also stronger. Countermodel 2 has well-founded dependence separately in each world, yet the union of possible edges contains the two-cycle $a\prec_\Diamond b\prec_\Diamond a$. It therefore fails precisely the additional premise.

A finite directed graph can certify acyclicity of a represented possible-dependence relation. It cannot establish completeness of the metaphysical alternatives or of the relation. An essentialist account of origin or existential dependence might supply independent reasons for restrictions on cross-world dependence. Such reasons must be argued; ordinary per-world acyclicity does not supply them.

The theorem yields a modal proxy for nonderivative necessity. It still does not settle whether existence belongs to the bearer's essence in the intended source sense. Essence is not simply any property that happens to hold in all worlds [P6]. This refinement protects the positive argument from claiming more than it proved.

# Finitary source supports: conjunction is not ancestry

The grounding routes concern actual explanation. The next calculus makes a different, expressly formal object precise: the support structure of a declared generative or inferential account. It may be given a metaphysical interpretation only through an additional faithful mapping.

Let $X$ be a finite set of atoms and $P\subseteq X$ a set of declared seed sources. A rule is

$$
B\longrightarrow x,\qquad B\subseteq X,
$$

read conjunctively: every atom in $B$ is required for that application. For a seed set $S\subseteq P$, define $\operatorname{Cl}(S)$ as the least set containing $S$ and closed under the rules.

An empty-antecedent rule is an explicit autonomous axiom or source. It is not permitted to hide inside a claim that the construction began with no source at all.

For a target atom $q$, define its minimal seed-support family

$$
\mathscr S_q
 =\min_{\subseteq}\{C\subseteq P:q\in\operatorname{Cl}(C)\}.
$$

This is an antichain. A support is a jointly sufficient seed set under the declared rules. Distinct minimal supports are alternatives; atoms inside one support are conjunctive requirements.

**Theorem 4 — Exact support semantics.** For every $S\subseteq P$,

$$
q\in\operatorname{Cl}(S)
\quad\Longleftrightarrow\quad
\exists C\in\mathscr S_q\;(C\subseteq S).
$$

*Proof.* If such a $C$ exists, closure monotonicity gives the result. Conversely, if $q\in\operatorname{Cl}(S)$, the finite family of sufficient subsets of $S$ has a minimal member; this belongs to $\mathscr S_q$. $\square$

The full families can also be computed without enumerating all seed assignments. Initialise a declared seed $p$ with support $\{p\}$. For each rule, form unions of one support from each antecedent, add them to the head's family, and discard supersets. Iterating reaches a fixed point because there are finitely many antichains of subsets of $P$. Induction on derivation height proves soundness; induction on the stages of least closure proves completeness. The independent implementation in this packet was compared with direct closure over 4,096 finite systems.

## No bootstrap from unseeded positive cycles

With no empty-antecedent rule and no seed, $\operatorname{Cl}(\varnothing)=\varnothing$. The empty set is already closed. Thus $a\to b$ and $b\to a$ do not produce either atom by least-closure generation.

The same equations can have a larger fixed point. Adopting a coinductive rather than least-generative semantics changes the question. The calculation therefore refutes unseeded **least-generative production**, not every coherentist or non-well-founded ontology. Arguments that cycles are always metaphysically vicious need more than this calculation; that issue has substantive philosophical opponents [P5].

## Conjunctive outside contributors

A graph edge recording that $g$ is an ancestor of $q$ does not establish that $g$ alone is sufficient for $q$. Under $\{a,b\}\to q$, the minimal support is $\{a,b\}$, not either singleton. The repository's existing unique-lineage-root theorem already requires extra sufficiency and external-input guards before interpreting a root as a sufficient actualiser [R7].

The support calculus supplies an explicit way to expose those guards. If every required non-root atom has a rule whose antecedents are strictly earlier in a well-founded, source-complete order, well-founded induction generates each atom from root supports. Finite antecedents produce finite proof trees. A unique root then suffices **in that complete rule model**. Without an adequate rule for a conjunctive prerequisite, root ancestry is not enough.

For contingent rule applicability, introduce a declared gate atom into the antecedent. Treating every operative causal rule as modally fixed is a substantive assumption. The formal validity of an inference schema, the existence of a rule representation, and the world's satisfaction of a causal law remain different objects.

# Modal support and the joint-absence obstruction

This section gives a complete finite model of modal support. It does not assume that the model's worlds exhaust metaphysical reality.

Let $P$ now denote a finite set of rigidly identified candidate contributors, with $|P|=n$. Let $S_\omega\subseteq P$ be the contributors active at world $\omega$. Fix a nonempty antichain $\mathscr S$ of nonempty minimal supports. Assume the target's support semantics is exact:

$$
q(\omega)
\quad\Longleftrightarrow\quad
\exists C\in\mathscr S\;(C\subseteq S_\omega).
\tag{S}
$$

The family could have been obtained from Theorem 4. More generally it is a declared monotone support law. Inhibitory or nonmonotone mechanisms require a richer encoding or a different calculus; they are not silently covered by (S).

Define the joint-absence complex

$$
\Delta_{\neg}
 :=\{D\subseteq P:\exists\omega\in\mathbb W,
                         \ D\cap S_\omega=\varnothing\}.
$$

A set belongs to this family when its contributors can be absent **together**. The family is downward closed and contains the empty set. It is not automatically closed under unions.

The minimal blocker family is

$$
\mathscr B(\mathscr S)
 :=\min_{\subseteq}\{H\subseteq P:
                     H\cap C\ne\varnothing\text{ for every }C\in\mathscr S\}.
$$

These are the minimal sets whose simultaneous absence destroys every support. This is standard hypergraph-transversal or blocker structure [P7]. The direction matters: supports identify what can suffice; blockers identify what can disable all alternatives.

**Theorem 5 — Modal support/blocker duality.** Under (S),

$$
\boxed{
\Box_*q
\quad\Longleftrightarrow\quad
\mathscr B(\mathscr S)\cap\Delta_{\neg}=\varnothing.
}
$$

*Proof.* If $q$ is false at a world, its active set contains no support. Its absent set intersects every support and therefore contains a minimal blocker $H$. The same world witnesses $H\in\Delta_{\neg}$. Conversely, if a blocker $H$ can be jointly absent, every support loses at least one member at that world, and (S) makes $q$ false. $\square$

This is an exact characterisation of the declared support model. It does not claim that non-derivability in a formal system means metaphysical impossibility, or that a causal support family can be read directly from the syntax of an argument.

## Necessary conditions need not select a necessary contributor

A singleton $\{p\}$ is a blocker exactly when $p$ belongs to every minimal support. Such a $p$ is indispensable. If $q$ is necessary, Theorem 5 excludes the possibility of $p$'s absence, so $p$ is active at every world.

But blockers need not be singletons. A necessary target can be sustained by several individually dispensable contributors whose **joint** absence is impossible.

**Countermodel 3 — Alternative support without any necessary individual.** Take

$$
\mathscr S=\{\{a\},\{b,c\}\},\qquad
S_{\omega_0}=\{a\},\quad S_{\omega_1}=\{b,c\}.
$$

The target holds in both worlds. The minimal blockers are $\{a,b\}$ and $\{a,c\}$. Neither blocker can be jointly absent, although each contributor is absent somewhere. Consequently no contributor is necessarily active.

A related arbitrarily high-order example takes $P$ of size $n\ge2$, supports all singletons, and worlds all nonempty active subsets. Every proper set of contributors can be jointly absent; the whole set cannot. The target “some contributor is active” is necessary, but no contributor is individually necessary.

This is a modal, not probabilistic, phenomenon. There is no probability measure in the construction. Mixing strategies independently or identifying pairwise statistical independence would not establish metaphysical compossibility of all the absences.

## Activation and concrete existence

A necessary active label is not yet a necessary concrete being. A faithful interpretation must provide a fixed map

$$
\beta:P\longrightarrow\mathbb D,
$$

with $\beta(p)$ concrete in the intended sense and

$$
p\in S_\omega\Longrightarrow\operatorname{Ex}(\omega,\beta(p)).
$$

Then necessary activation implies necessary existence of that fixed bearer. If the label denotes a repeatable role and the occupant varies with $\omega$, this implication to one individual is unavailable. If the label denotes a proposition or law-type, concreteness has not been supplied. These are interpretation conditions, not algebraic consequences of the blocker theorem.

# Exact modal auditing from incomplete information

The previous supplement quantified what a moment summary cannot determine about future expectations. Here we quantify a different loss: what finite-order information about possible joint absences cannot determine about a modal support claim.

Suppose the support family $\mathscr S$ is known, but $\Delta_{\neg}$ is only known through its **complete $k$-skeleton**

$$
K=\{D\in\Delta_{\neg}:|D|\le k\}.
$$

“Complete” is essential. This records which sets of size at most $k$ are possible joint absences **and** which are not. An unqueried set is not silently counted as impossible.

Define

$$
\Delta_{\mathrm{lo}}:=K,
$$

$$
\Delta_{\mathrm{hi}}
 :=\{D\subseteq P:\text{every }B\subseteq D\text{ with }|B|\le k
                                    \text{ belongs to }K\}.
$$

Both are downward-closed families with the given $k$-skeleton.

**Theorem 6 — Exact completion trichotomy.** Every absence complex consistent with $K$ lies between $\Delta_{\mathrm{lo}}$ and $\Delta_{\mathrm{hi}}$. Moreover:

1. If $\mathscr B(\mathscr S)\cap\Delta_{\mathrm{hi}}=\varnothing$, then every compatible completion makes $q$ necessary.
2. If $\mathscr B(\mathscr S)\cap\Delta_{\mathrm{lo}}\ne\varnothing$, then every compatible completion makes $q$ non-necessary.
3. Otherwise, there are compatible completions with opposite verdicts.

*Proof.* A compatible downset must contain its prescribed small faces, giving the lower inclusion. If it contains $D$, it contains every small subset of $D$, giving the upper inclusion. The lower and upper families themselves have the prescribed skeleton: for a set $D$ with $|D|\le k$, membership in the upper family requires, in particular, $D\in K$; downward closure gives the converse.

For any finite downset $\Delta$ containing $\varnothing$, take one world for each maximal face $D$ and set its active contributors to $P\setminus D$. The resulting absence complex is exactly $\Delta$. Thus the lower and upper completions are realised by finite modal structures. Apply Theorem 5 and monotonicity of blocker intersection. In the third case the lower completion has no possible blocker and the upper completion has one, giving opposite verdicts. $\square$

This is an explicit countermodel generator. It is stronger than saying “more information may be needed”: it computes the two extremes and identifies a blocking joint absence whose status the current evidence fails to settle.

## The exact arity required

Assume the target is nonconstant under unconstrained activation: it has a nonempty support family, no empty support, and therefore a nonempty blocker family. Define

$$
 r(\mathscr S):=\max_{H\in\mathscr B(\mathscr S)}|H|.
$$

**Theorem 7 — Sharp modal interaction arity.** Complete joint-absence information through order $r(\mathscr S)$ determines $\Box_*q$ for every absence complex. No smaller uniform order suffices.

*Proof.* The positive statement follows because all minimal blockers have size at most $r(\mathscr S)$, and their membership can be read from that skeleton.

For sharpness, take a minimal blocker $H$ with $|H|>k$. Let

$$
\Delta_0=\{D:D\subsetneq H\},\qquad
\Delta_1=\{D:D\subseteq H\}.
$$

Their complete $k$-skeletons agree. No subset of $H$ other than $H$ is a blocker, by minimality. Nor can another minimal blocker be a proper subset of $H$. Thus $\Delta_0$ contains no blocker, while $\Delta_1$ contains $H$. Both are realised by the construction in Theorem 6. Their necessity verdicts differ. $\square$

This degree measures the size of a consequential joint-absence test. It is not a theorem about the intrinsic tensor degree of an orthing, the number of minds in an argument, or the number of players in a game.

## The exact worst-case number of questions

Now permit a query of any set $D\subseteq P$ to an oracle that answers whether $D\in\Delta_{\neg}$. The oracle is a mathematical idealisation, not an available procedure for deciding metaphysical possibility.

**Theorem 8 — Sharp deterministic modal-query complexity.** With the support family fixed and nonconstant, the worst-case number of membership queries required by a deterministic exact algorithm to decide $\Box_*q$ over all absence complexes is

$$
\boxed{Q(\mathscr S)=|\mathscr B(\mathscr S)|.}
$$

*Proof.* Query each minimal blocker. A positive answer refutes necessity; negative answers for all blockers establish it. This gives the upper bound.

For the lower bound, let

$$
\Delta_0
 =\{D\subseteq P:\text{no minimal blocker is contained in }D\}.
$$

This is the maximal absence complex making $q$ necessary. For any minimal blocker $H$, all its proper subsets belong to $\Delta_0$, so

$$
\Delta_H=\Delta_0\cup\{H\}
$$

is also a downset. It makes $q$ non-necessary and differs from $\Delta_0$ on exactly the query $H$. Run any deterministic exact algorithm on $\Delta_0$. If it does not query some minimal blocker $H$, it receives the same answers on $\Delta_H$ and returns the same verdict, which must be wrong in one case. Hence it must query every minimal blocker on this input. $\square$

This is a worst-case query lower bound, not an efficient general algorithm for enumerating blockers. Their number can be exponential, and producing minimal transversals is itself a separate algorithmic problem [P7]. No arbitrary hypergraph problem has been made polynomial by counting its output.

## A finite mixed-strategy game of rival testing

The same obstruction family gives an explicit game, rather than merely an invocation of Nash existence. Fix $m=|\mathscr B(\mathscr S)|\ge1$ and promise that the unknown absence complex is either the safe $\Delta_0$ in Theorem 8 or one of its $m$ alternatives $\Delta_H$. An auditor may ask at most $b$ questions, where $0\le b\le m$, then announce whether $q$ is necessary. An adversary chooses one of those formal models. The auditor's payoff is one for a correct classification and zero otherwise; the adversary minimises that payoff.

The players are the auditor and the adversarial model selector. Contributors, modal alternatives, and truth itself have not been turned into agents. No prior over actual metaphysical reality is asserted.

**Proposition 1 — Exact mixed equilibrium of the bounded audit game.** The game's minimax success probability is

$$
\boxed{v(m,b)=\frac{m}{2m-b}.}
$$

An optimal auditor queries a uniformly chosen $b$-subset of minimal blockers. On a positive answer it declares non-necessity; after all negative answers it declares necessity with probability $m/(2m-b)$. An optimal adversary assigns probability $(m-b)/(2m-b)$ to the safe model and $1/(2m-b)$ to each unsafe model.

*Proof.* A non-blocker query has identical answers in every promised model and cannot help. A positive blocker answer identifies an unsafe model. Thus a deterministic strategy can be represented by its set of questions on the all-negative path and its default verdict there; querying fewer than $b$ is no advantage.

For the proposed auditor, safe-model success is $\alpha=m/(2m-b)$. For any unsafe model, its unique distinguishing blocker is queried with probability $b/m$. Its success is therefore

$$
\frac bm+\left(1-\frac bm\right)(1-\alpha)
=\frac m{2m-b}.
$$

Against the proposed adversary, a pure auditor defaulting to non-necessity succeeds with probability $m/(2m-b)$. One defaulting to necessity succeeds on the safe model and on the $b$ queried unsafe models, again with total probability $m/(2m-b)$. Thus neither player can improve by a unilateral deviation: the strategies form a saddle point, hence a mixed Nash equilibrium of this declared zero-sum game. $\square$

For example, with $m=56$ unresolved minimal cuts and budget $b=28$, even the optimal strategy guarantees only $2/3$ classification success over the promised adversarial family. This is not a probability that a metaphysical conclusion is true. It is the value of a deliberately specified finite diagnostic game.

**Exact-warrant corollary.** If false certificates of necessity are forbidden, no strategy with a strict budget $b<m$ can issue a positive necessity certificate with positive probability on the safe model while remaining correct on every promised alternative. Any all-negative branch omitting $H$ is also possible in $\Delta_H$; declaring necessity on it would be a false certificate there.

Randomisation can allocate inquiry effort and improve a bounded-error decision. It cannot convert incomplete modal information into an exception-free warrant. This extends the predecessor's strategic identification analysis using the very same modal countermodels that control the ground argument. It is an elementary decision-game construction with a complete proof, not a claim that Nash equilibria establish necessary beings.

## Threshold examples

For the condition “at least $s$ of $n$ contributors are active,” minimal supports are the $s$-subsets and minimal blockers are the $(n-s+1)$-subsets. Therefore

$$
 r=n-s+1,\qquad Q=\binom n{n-s+1}.
$$

For eight contributors:

| Required active contributors | Required joint-absence arity | Worst-case exact queries |
|---|---:|---:|
| At least one | 8 | 1 |
| At least two | 7 | 8 |
| At least four | 5 | 56 |
| At least seven | 2 | 28 |
| All eight | 1 | 8 |

Arity and query count are different costs. Knowing that each source is individually contingent answers the singleton questions. It does not in general answer the joint questions that determine whether all support can fail together.

# Positive support extraction: recombination and compactness

The preceding countermodels do not make witness extraction impossible. They identify structural hypotheses under which it becomes valid.

## Finite absence recombination

Define the necessarily active contributors by

$$
N:=\bigcap_{\omega\in\mathbb W}S_\omega.
$$

Assume that the absence complex is closed under finite unions. Since $P$ is finite, this means that independently possible absence sets can be jointly realised throughout this declared family.

**Theorem 9 — Necessary support under finite recombination.** If $\Delta_{\neg}$ is union-closed, then under (S),

$$
\boxed{
\Box_*q
\quad\Longleftrightarrow\quad
\exists C\in\mathscr S\;(C\subseteq N).
}
$$

*Proof.* Let $D=\bigcup\Delta_{\neg}$. Finiteness and union closure give $D\in\Delta_{\neg}$. A contributor belongs to $D$ exactly when it is not necessarily active, so $D=P\setminus N$. Some world therefore has all non-necessary contributors absent. If $q$ is necessary, an active support at that world is contained in $N$. The converse follows immediately: a support contained in $N$ is active at every world. $\square$

A nonempty such support contains at least one necessarily active contributor. With the fixed concrete-bearer interpretation specified above, a necessarily existing concrete bearer follows. This is a positive result; the burden is the recombination and interpretation premises.

## Why recombination cannot be smuggled in

For the special claim “some contributor exists,” the schema

$$
\left(\forall p\;\Diamond_*\neg\operatorname{Ex}(p)\right)
\Longrightarrow
\Diamond_*\left(\forall p\;\neg\operatorname{Ex}(p)\right)
$$

is exactly the kind of step whose contraposition yields a necessary individual. It cannot be advertised as a harmless consequence of individual contingency. It excludes the rotating-support models by adding the very joint-absence property they lack.

Union closure is a general structural principle, not literally the conclusion “a necessary being exists.” Nevertheless, it requires independent warrant over the relevant sources. Entangled causal constraints, necessary disjunctions, or relations among possibilities can invalidate it. Criticising a finite mixed-strategy model for lacking independence does not prove that metaphysical worlds must exhibit product independence.

There is philosophical prior work on recombination principles and grounding, including interactions between recombination and grounding entailments [P8]. The present theorem is a finite support specialisation, not a claim that this conceptual relationship has been discovered for the first time.

## An infinite extension

The original schema allows no fixed global bound on possible finite interaction degree. It does not automatically supply a compact global space. To handle infinitely many contributors, state that additional requirement explicitly.

Let $P$ be any set. Let $\mathbb W$ be a nonempty compact topological space. For each contributor $p$, assume

$$
A_p:=\{\omega:p\in S_\omega\}
$$

is open. Let $\mathscr S$ be a family of nonempty **finite** supports, and suppose their activation regions cover $\mathbb W$:

$$
\mathbb W=\bigcup_{C\in\mathscr S}\bigcap_{p\in C}A_p.
$$

Finally, assume every finite set of individually non-necessary contributors can be jointly absent at some world.

**Theorem 10 — Compact necessary-support extraction.** Under these assumptions, some support consists entirely of necessarily active contributors.

*Proof.* Each support region is open because the support is finite. Compactness gives a finite subcover, using supports $C_1,\ldots,C_m$. Their union $P_0$ is finite. Let $D\subseteq P_0$ contain precisely its non-necessary contributors. The finite joint-absence assumption supplies a world where every member of $D$ is absent. Some $C_j$ covers that world, and therefore contains no member of $D$. Every member of $C_j$ is necessarily active. $\square$

The conclusion transfers to a necessary concrete bearer only through the fixed-bearer existence bridge. It does not collapse a plurality of necessary contributors into one bearer.

## What fails without the hypotheses

For noncompact $\mathbb W=\mathbb N$ with the discrete topology, let contributor $p_i$ be active only at world $i$. Singletons support $q$ at every world, and every finite collection of contributors can be jointly absent. No contributor is necessarily active. The open cover has no finite subcover.

For compact $\mathbb W=\mathbb N\cup\{\infty\}$ with the one-point compactification topology, let each contributor be active only at its matching point. Again every finite set can be jointly absent and the target is covered. The activation set $\{\infty\}$ is not open, so the theorem does not apply.

Logical compactness is also different from the claimed topological premise about the intended worlds. Obtaining a model in an enlarged semantic class does not establish that its new world is a metaphysically possible alternative. No finite input file, finite episode, or support tensor establishes the compactness premise.

# A conservative modal construction

The previous packet's exact continuation statistics do not by themselves determine the identity or necessity of the objects that realise the operational structure. The following construction states that limitation for an entire language, not only a single omitted predicate.

Let $\mathfrak A$ be a nonempty world-local relational structure, with sorts for operational states, actors, records, observations, actions, and any specified finite or infinite histories. Its vocabulary may include correctness, a reference norm, semantic relations, deterministic or stochastic transitions, and the declared strategic layer. Their interpretations are held fixed; correctness need not be whatever an actor currently endorses.

Take at least two worlds. At world $\omega$, realise each concrete bearer $d$ by a tagged copy $(\omega,d)$, and define

$$
\operatorname{Ex}(\omega,(\omega',d))
\quad\Longleftrightarrow\quad \omega=\omega'.
$$

Interpret every world-local relation and operation through the map $d\mapsto(\omega,d)$. Mathematical code values or truth values may be kept as a separate abstract sort; this does not make a concrete code carrier necessary.

**Theorem 11 — Worldwise conservative realisation.** Every world-local sentence of $\mathfrak A$, with concrete quantifiers restricted to the locally existing copies, has the same truth value in every copied world as in $\mathfrak A$. Compare the copied model with a shared-carrier bundle having a copy of $\mathfrak A$ at each world over the same modal frame. The two bundles also agree on Boolean and modal combinations of closed local sentences. Yet no tagged concrete bearer in the copied model exists at every world.

*Proof.* The tagging map is an isomorphism of the world-local structures. Atomic formulas are preserved by construction. Boolean connectives preserve truth under the induction hypothesis; local quantifiers are preserved by the bijection between the original sort and its existing copies. Thus all local first-order sentences are preserved. Closed local sentences receive the same world-indexed truth assignment in the two bundles, so induction also preserves their modal combinations on the shared frame. Finally, each concrete copy exists only at its own tagged world and fails to exist at another. $\square$

The theorem does not cover de re formulas that hold an individual fixed across modal operators, essential-ownership clauses, or premises already asserting a necessary concrete entity. Those are the precise places where the extension can cease to preserve a richer metaphysical theory.

## Why this is more than an appeal to unspecified missing information

One can retain all the previous model's state distinctions, exact predictions, continuation-observable span, query outcomes, and game payoffs. The local actualisation of that structure remains accurate. What varies is its cross-world concrete realisation.

Thus improving operational completeness does not automatically remove the modal ambiguity. This is not a denial that operative truth requires objective conditions. Both copies can instantiate the same truth conditions without those conditions being identified with one necessarily existing concrete carrier.

Nor does the proof establish that the copied structures describe metaphysically possible worlds. It establishes that the chosen local theory cannot exclude them. An additional metaphysical premise may do so, but must be represented and defended as such.

The statement is a conservative-extension/isomorphism construction with ordinary model-theoretic ancestry. It is not a universal theorem against natural theology, an argument that consciousness is computational, or a proof that no necessary being exists. It supplies a precise limit on what can be inherited from the predecessor packet without adding a de re bridge.

# From a necessary condition to a necessary mental bearer

The intellectual route should be evaluated in its strongest form. Necessary content, a represented formula, and a concrete thought are not interchangeable.

Let $c$ be content, $t$ a particular alleged thought or attribute, and $g$ its bearer. A content can be expressed in different tokens. A token can exist without being true. A true formula does not become a concrete intentional state merely because a semantic model assigns it a truth value.

## The indispensable-bearer theorem

**Theorem 12 — Fixed essential ownership.** Suppose a particular $t$ exists necessarily and there is a fixed $g$ such that

$$
\Box_*\bigl(\operatorname{Ex}(\omega,t)
\to[\operatorname{Ex}(\omega,g)\land\operatorname{Own}(\omega,g,t)]\bigr).
$$

Then $g$ exists necessarily. If the ownership condition additionally implies that $g$ is genuinely mental whenever it owns $t$, then $g$ is mental throughout the modal scope.

*Proof.* At any $\omega$, necessary existence supplies $\operatorname{Ex}(\omega,t)$. The fixed ownership conditional supplies $\operatorname{Ex}(\omega,g)$ and the ownership fact, with the same $g$. Since $\omega$ was arbitrary, necessity follows. The mental conclusion uses its separately stated implication at each world. $\square$

The six-node certificate in the package checks the fixed-bearer inference core. It does not verify that a logical law is a concrete thought or that its owner is essential to it.

**Knowledge is a further step.** Owning a thought is not, by itself, knowing its content. Even a true thought need not amount to knowledge merely by being true. For a content $c$, a knowledge strengthening needs an independently warranted condition linking the particular ownership, truth, and non-accidental epistemic standing to $\operatorname{Knows}(\omega,g,c)$. If that condition holds throughout the modal scope, the same argument yields worldwise knowledge of $c$. It does not yield omniscience or understanding from a bare $\operatorname{Mental}$ predicate. This is an additional guard, not an unmentioned conclusion of Theorem 12.


## Fair comparison with Anderson and Welty

Anderson and Welty argue from necessary logical truths to necessarily existing intentional thoughts and then to their essential mental owner [P2]. Their footnote 31 explicitly discusses the possibility that contingent thinkers vary from world to world; they do **not** simply overlook the quantifier problem. Their response uses the identity of a necessarily existing thought and its essential ownership. They also distinguish their conclusion from a proof of numerical uniqueness.

The live dispute is therefore not whether Theorem 12 is valid. It is whether the realist and intentional ontology needed for its antecedent is established: whether necessary logical content is an existent intentional item of the relevant kind, whether it is the same item across worlds, and whether its identity requires this owner. A rival can preserve necessary truth while denying that ontological identification.

That route is compatible with Orthemology only if its particular thought/attribute and bearer maps are explicit. Treating a derived tensor component or a language-independent rule schema as $t$ would not discharge them. A source-relative doctrine of uncreated Knowledge can supply a different, explicitly theological account of the bearer relation, but it must not be silently substituted for the independently defended antecedent of a neutral argument.

## The stronger intellectual-adequacy proposal

A different argument says that a ground adequate to truth, normativity, and intelligibility must itself understand those things. This deserves a substantive defence rather than a purely syntactic dismissal. Its appeal is that objective reason-responsiveness, intentional aboutness, and assessment of fitting reasons are not obviously exhausted by regular causal correlation.

But two inferences must still be separated. An effect having a capacity does not by logic alone force its ultimate cause to instantiate that very capacity in the same mode. And a system's ability to implement a correct relation does not by definition constitute understanding. To establish the intellectual conclusion, the argument must defend an appropriate adequacy principle and exclude the proposed impersonal, powers-based, primitive-norm, and teleosemantic alternatives in that exact respect.

Neither a payoff-maximising policy nor the exponential information requirement in [I1] supplies this premise. Those results concern what an evaluation can recover, not the intentional nature of the ground that makes truth or evaluation possible.

## A non-question-begging specification of the remaining test

The relevant task is not “find a predicate called knowledge and place it on the root.” It is to identify an independently intelligible feature of objective cognitive normativity, show that every successful rival must instantiate it, and prove that its adequate ground cannot be wholly non-intellectual. The ground must then be identified with the necessary bearer already derived, rather than introducing an unrelated knower.

This criterion does not demand a criterion-free tribunal or preclude first principles. It demands that the proposed feature not be defined as “whatever only a divine intellect can supply.” Otherwise the desired conclusion has been inserted at the start.

# Unity, common bearers, and the strength of coordination

Necessary existence, sufficiency for one effect, universality of explanatory scope, and numerical unity are separate claims. A complete ascent must show where each enters.

## What common ancestry can establish

**Proposition 2 — Unique root under upstream directedness.** Let a nonempty complete dependency domain be well-founded, and let its reflexive-transitive predecessor relation be upstream-directed: any two members have a common ancestor. Then the domain has a unique root, and that root is an ancestor of every member.

*Proof.* For any member, well-foundedness of its nonempty ancestor set gives a root ancestor. If two roots existed, a common ancestor of them would have to equal each, since neither has a proper predecessor. They coincide. Every member's root ancestor is therefore the unique root. The converse, that a universal root provides common ancestors, is immediate. $\square$

The finite-DAG version is already present in Deep J [R7]; the present statement is a well-founded extension of the same argument, not a new general uniqueness mechanism. It can be combined with Theorem 1 or 3 at the corresponding scope.

But an edge recording derivational inheritance is not automatically sufficient causation. The support calculus must account for jointly required contributors. Nor is one root vertex automatically one simple subject: a coarse node may name an aggregate. Identity, granularity, and complete actualiser semantics cannot be recovered from a root count alone.

## Joint roles require a joint bearer

Let $R$ be a finite set of attribute roles, and $\operatorname{Host}(g,r)$ specify which bearer instantiates which role. Then

$$
\forall r\in R\;\exists g\;\operatorname{Host}(g,r)
$$

does not entail

$$
\exists g\;\forall r\in R\;\operatorname{Host}(g,r).
$$

**Proposition 3 — Arbitrarily high-order common-bearer obstruction.** For every $n\ge2$, there is a model in which every proper subset of $n$ roles is jointly borne, but no individual bears all $n$ roles.

*Proof.* Let the roles be $r_1,\ldots,r_n$ and the bearers be $b_1,\ldots,b_n$. Give $b_i$ every role except $r_i$. A proper role set omits some $r_i$, so $b_i$ bears that entire set. Every bearer nevertheless lacks a role from the full set. $\square$

This can hold with every $b_i$ necessarily existing. Thus even necessity of the available bearers plus all proper-subfamily co-instantiation does not settle one common bearer. It is not a claim that such plural grounds are metaphysically possible; it is an exact obstruction to the proposed inference under the declared incidence information.

A genuine positive co-instantiation argument is possible with additional structure. For example, let actual candidate bearers form a compact space, let each role's eligible-bearer set be closed, and assume every finite family of these sets has a common member. Compactness gives a common bearer of all roles. The theorem is standard. Its application requires an independently warranted topology, closed eligibility sets, an exhaustive actual candidate domain, and the finite-intersection property; none follows from a tensor encoding.

## Why coordinated wills do not prove one will

The strongest plurality argument should not be weakened to the claim that multiple agents sometimes disagree. Consider a common outcome space $Y$ with at least two alternatives. Suppose each of $n\ge2$ putatively unrestricted agents independently chooses a desired outcome $y_i$, and every choice must be fully efficacious on the same final outcome.

**Proposition 4 — Joint unrestricted-efficacy compatibility.** A joint choice can be fully realised for all agents exactly when all $y_i$ agree. Therefore unrestricted independent choice over $Y^n$ is incompatible with guaranteeing all agents' complete efficacy on the same outcome.

*Proof.* Complete efficacy requires a single $y$ with $y=y_i$ for every $i$. Such a $y$ exists exactly for diagonal profiles. Because $|Y|\ge2$ and $n\ge2$, the full Cartesian product contains non-diagonal profiles. $\square$

This excludes **independent unrestricted rival sovereignty** under the stipulated common-result semantics. It does not exclude multiple necessarily concordant wills, noncompeting domains, constrained plural powers, or a common coordinating ground. Excluding those alternatives requires an additional argument. A correlated equilibrium or perfect actual agreement is not evidence of one mind.

This distinction also limits the import of the earlier finite games. They can expose incompatible joint demands or missing strategic information. Their equilibrium conditions do not decide numerical unity, identity of an actualiser, or the modal independence of divine wills.

# Necessary existence without collapse of contingency

A positive necessary-ground argument must explain how its conclusion relates to genuinely contingent effects. The distinction is not cosmetic. Necessary existence of a bearer is not necessity of every state, action, or effect of that bearer.

## The exact collapse theorem

Let facts be interpreted at worlds. Suppose a finitary derivation uses seed facts $P$ and rules $B\to q$. Assume every seed fact is necessary and every used rule is modally valid in the strong necessitating sense

$$
\Box_*\left(\bigwedge_{b\in B}b\to q\right).
$$

**Theorem 13 — Necessity propagates through necessitating finite support.** Every fact with a finite derivation from those seeds is necessary.

*Proof.* Induct on derivation height. Seed facts are necessary by assumption. At a rule application, each antecedent holds in every world by induction; the rule conditional holds there too; therefore its conclusion holds in every world. Finite derivations exhaust the least closure. $\square$

Consequently, a contingent effect cannot simultaneously have a complete derivation from wholly necessary seed **facts** through wholly necessitating rules. At least one of those requirements must be rejected or qualified.

The theorem must not be misapplied to Theorem 1. That theorem gives necessary existence of an entity. It does not give necessity of every fact concerning that entity. An extra inference identifying the complete actualising condition with the mere existence of the root would be doing the work.

## A lawful contingency-preserving pattern

The following package can be coherent:

$$
\Box_*\operatorname{Ex}(g),\qquad
\operatorname{Will}_{\omega_*}(g,q),\qquad
\Box_*\bigl(\operatorname{Will}(g,q)\to q\bigr),
$$

while $\operatorname{Will}(g,q)$ and $q$ are contingent. The premise does not say that the same willing occurs at every world.

This does not finish the explanation of that willing. A theory must still account for its actuality and its appropriate relation to the necessary bearer. Possible proposals include non-necessitating agent explanation, a contingent but explained exercise of power, rejection of universal grounding necessitarianism, or a defended necessitarian view of the outcome. Merely naming “Will” is not itself an explanation; conversely, the absence of logical necessitation does not by definition mean absence of explanation.

There are primary philosophical arguments on both sides. Pruss distinguishes sufficiency of explanation from deductive entailment; Trogdon defends a necessity connection for full grounds; Pearce develops a rationalist argument requiring grounding indeterminism [P9–P11]. The finitary theorem here identifies the formal pressure point. It does not claim to originate that debate or to settle which conception of explanation is correct.

## Knowledge of contingent truths

**Proposition 5 — A necessary knower need not make every known truth necessary.** In an extensional possible-world model, necessary existence and worldwise omniscience are compatible with contingent truths.

*Construction and verification.* Let $\mathbb W$ have at least two worlds, let $g$ exist at every world, and use $\mathcal P(\mathbb W)$ as the proposition algebra. For each proposition $Q\subseteq\mathbb W$, define

$$
\operatorname{True}(\omega,Q)\iff\omega\in Q,
\qquad
\operatorname{Knows}(\omega,g,Q)\iff\omega\in Q.
$$

At every world, $g$ knows every truth in this algebra and no falsehood. A nonempty proper $Q$ is nevertheless contingent. Thus

$$
\Box_*\forall Q\,[\operatorname{True}(Q)\to\operatorname{Knows}(g,Q)]
$$

is not the claim that every actually known $Q$ is necessarily true. $\square$

This is a consistency model of the displayed knowledge conditions, not a reduction of subjective understanding to a truth table, a proof that such a knower exists, or a complete metaphysics of omniscience. The executable model instantiates the construction on two worlds and four propositions; the general construction is on paper.

## Why essential necessity is still separate

A necessarily existing bearer may have contingent relational or action facts. Conversely, an object may necessarily exist because of a necessary dependence on another; necessary existence alone does not establish aseity. Actual underivability, uniform underivability, essence-based necessity, and necessary intrinsic character must therefore remain distinct.

This is not an argument against divine immutability or any particular doctrine of attributes. It identifies the propositions that an account must relate. A doctrine can distinguish an enduring attribute from particular acts or objects of that attribute; its exact source semantics then matters. A formal model that fails to encode the distinction cannot adjudicate the doctrine by noticing a changing Boolean output.

# Three integrated model tests

Isolated countermodels can conceal conflicts between premises that arise when the programme is combined. We therefore construct common models retaining the same operative state, truth, update, and strategic structure while changing the metaphysical carrier conditions.

The shared operational core has a binary state, the actions `keep` and `flip`, a fixed reference truth predicate, accurate represented evaluations, and a complete local history. Every finite continuation is evaluated exactly: successive flips have the parity prescribed by the action sequence. A declared two-player game rewards each player's matching the reference target bit, so its unique equilibrium is both players matching that bit. No equilibrium is used as a truthmaker.

The model cards in `verification/integrated_models.json` also preserve the existence and content of source records while **not** assuming their theological authentication. This distinction is explicit. The models do not pretend to satisfy a premise asserting an authenticated divine disclosure while denying its content.

## Model J1: rotating contingent actual roots

Each of two worlds has its own concrete root, agent, and record. The root is the common bearer of the local operative order and efficacy, and it grounds the local agent and record. Each world's graph is finite, source-complete at the declared granularity, and acyclic. The operational core is correct in each world. Every concrete individual is absent at the other world.

This model preserves actual evaluability and actual foundation, but fails the contingent-existence dependence premise at the root. Thus it does not refute Theorem 1. It identifies precisely why actual rootedness alone does not supply necessary existence.

## Model J2: a necessary impersonal unified ground

Let a concrete $g$ exist in both worlds. At each world it grounds that world's contingent agent and record. Give $g$ the formal roles of intrinsic operative order and effective power, but not mentality or volition. Each world's actual dependence cone is finite, complete, and acyclic, with $g$ its unique root. Every actual contingent entity has a predecessor. The union of possible dependence edges is also acyclic.

The model therefore satisfies both the actual-ancestry and uniform-foundation premise packages. It has a necessarily existing, uniformly underived, common order-and-efficacy bearer. It does **not** have a necessary mental bearer.

This is stronger than a control that merely splits order and power into unrelated resources. At the level of the declared formal conditions it permits their co-instantiation in one impersonal root. It still does not establish that an impersonal ground can really account for objective reason-responsiveness. A defended intellectual-adequacy premise may exclude it. That premise is not among the conditions the model is claimed to satisfy.

## Model J3: a necessary personal ground with contingent effects

Retain the same existence and grounding structure, but make $g$ mental and volitional. Interpret its knowledge by Proposition 5 and allow its particular willing and the corresponding effect to differ between worlds. Both the necessary-ground conditions and the contingent effect are satisfied.

This model shows that the route is not forced into modal collapse by its necessary-existence conclusion. It does not prove mentality by stipulation: mentality is what distinguishes this additional positive model from J2. A proof selecting J3 over J2 requires evidence or argument for that distinction.

## Joint comparison

| Property | J1 | J2 | J3 |
|---|:---:|:---:|:---:|
| Actual concrete evaluative activity | Yes | Yes | Yes |
| Accurate local continuation evaluation | Yes | Yes | Yes |
| Complete acyclic actual dependence cone | Yes | Yes | Yes |
| Every actual contingent member has a parent | No | Yes | Yes |
| Necessary concrete root | No | Yes | Yes |
| Uniform underivability of that root | No | Yes | Yes |
| World-local common order/efficacy bearer | Yes | Yes | Yes |
| Necessary mental bearer | No | No | Yes |
| Contingent effects remain | Yes | Yes | Yes |
| Theological source authentication assumed | No | No | No |

The code checks these interpreted properties and 1,022 finite operational continuation cases per model. The general continuation identity is proved by induction, not by enumerating all possible lengths.

## The general extension behind J2

For precision, let $\Sigma_{\mathrm{op}}$ be a world-local many-sorted language with its own carrier sort. The outer existence, existential-dependence, and root predicates are not in that language. Local mental predicates, if present, describe the old carriers and remain unchanged. The expansion adds an outer bearer sort and injections of the local carriers; it does not enlarge the old quantified sorts or replace their causal relations.

**Theorem 14 — Operational preservation with a necessary impersonal root.** Every nonempty $\Sigma_{\mathrm{op}}$ structure has an expansion of this stated kind that preserves its world-local theory and provides a necessary, uniformly underived impersonal root for its copied concrete carriers.

*Construction and proof.* Use the tagged local copies from Theorem 11, but add one new outer concrete bearer $g$ existing at every world. At each world, place $g$ before every locally existing carrier in a new, expressly typed existential-dependence relation. Add no incoming edge to $g$ and no other edges in this relation. All local operational sorts and relations are interpreted exactly as before; their truth is therefore preserved by the same induction. Every copied carrier is contingent and has the actual predecessor $g$. The possible-dependence relation is a star and is well-founded. Assign the root the new order-and-efficacy roles and withhold mentality. The interpretations satisfy the displayed structural premise packages. $\square$

The expansion is conservative over the specified operational language, not over a language that already includes an independently warranted principle forcing the root to be mental. The new grounding relation does not replace a distinct old causal or epistemic relation. A source-faithful world interpretation of its explanatory meaning remains a separate burden.

This is a scoped integrated non-entailment result, not a proof of the metaphysical possibility of impersonal origins. It also is not a complete certification of R5 over every strongest source, noetic, and metaphysical premise ever proposed in the repository. What is established is exact: operational adequacy plus the strengthened necessary-root packages still does not force the mental conclusion in this typed formal class.

# Attribute ascent and the source/world interface

The argument can be continued without pretending that each later predicate has already been obtained. The following is an ordered programme of actual implications and the specific premises they need.

## Knowledge, power, will, and life

Theorem 12 can establish a necessary mental owner under its actual thought-and-ownership premises. Theorem 1 or 3 can establish a necessary ground under their different dependence premises. To identify these witnesses requires a **common-bearer argument**. Two existence proofs do not by themselves refer to the same individual.

Effective actualisation can warrant an appropriate power predicate when power is explicitly the capacity for that actualisation. It does not automatically warrant unrestricted power over every metaphysically possible object. The domain of efficacy must be stated.

Contingent specification is not identical to will. A selector function can be deterministic, stochastic, externally parameterised, or impersonal. A volitional conclusion requires an account under which the relevant selection is attributable to an agent's intention, not merely a map's output. If the actualiser is already shown to be knowing and agentive, that may support such an account, but the inference is not supplied by the existence of alternatives alone.

A life predicate relevant to the theological ascent is not biological metabolism or the fact that a process is running. The source and metaphysical meaning must be given. A defended principle relating actual knowledge and will to living subjecthood can yield life at that scope; a finite automaton with a `life` label cannot.

## Wisdom is not a scalar score

A root possessing knowledge, effective power, and volition does not automatically act wisely merely because its actions are internally coordinated. Wisdom includes the appropriate relation to ends, reasons, and fittingness. A criterion defining every successful selection as wise would erase the very distinction that Orthemology is trying to explain.

The prior packet's refusal to treat burden count as a sound potential is relevant here only as a diagnostic analogy. Neither a Lyapunov functional nor a Nash payoff is a proof of objective teleology or divine Wisdom. The new metaphysical work must establish the fittingness relation and its bearing on the identified subject.

## Guarded a-fortiori reasoning

The source-internal perfection route can be expressed without turning it into a neutral theorem. A guarded schema has the form

$$
\begin{aligned}
&\operatorname{EstablishedCreator}(g)\land
\operatorname{PurePerfection}(P)\land
\operatorname{NoCreatureDefect}(P)\\
&\qquad\land\operatorname{ApplicableAwlaBridge}(g,P)
\Longrightarrow P(g).
\end{aligned}
$$

The substantive work lies in the guards: establishing the Creator, characterising the perfection without importing creaturely deficiency, and justifying the a-fortiori relation. This is not arbitrary property copying from effects to causes. The relevant Arabic discussion supplies a source-internal guarded perfection argument [P3]; its mere citation does not independently discharge those guards.

The source lane is not inferior because it uses revelation or tradition-specific first principles. It is a different epistemic route. Its claims should be defended under their real premises rather than marketed as consequences of a neutral finite model.

## Speech, occurrence, and identification

A capacity for intentional disclosure is not a proof that disclosure occurred. An occurrence is not yet a proof of the content, wording, recipient, or identity of its source. A source name or a text's self-attribution is not automatically its authentication.

The ascent therefore keeps separate:

$$
\text{capacity}\ \to\ \text{actual disclosure}\ \to\
\text{authenticated content}\ \to\ \text{identified revealed referent}.
$$

Each arrow has its own evidence. The B0–B16 ledger already records these distinctions [R3]. The new modal-support mathematics does not overwrite them. It can clarify whether the evidence rules out the relevant alternatives; it cannot supply an unobserved revelational event.

The Arabic primary-text discussion and the existing translated-primary dossier both require care about which claims the author endorses, reports, or criticises. They also support the practical decision not to treat an unspecified “necessary existent” as already identical to the fully characterised Creator [P3; R8].

# What this contributes beyond continuation completeness

The earlier supplement answered a universal predictive question inside a fixed finite reference model. Its exact observables and laws cannot automatically identify that model's metaphysical realisation. The present work adds a different interface:

$$
\begin{gathered}
\text{retained operational information}\\
\downarrow\ \text{declared interpretation and modal audit}\\
\text{modal support information}\\
\downarrow\ \text{separately warranted bridges}\\
\text{ground and bearer claims}.
\end{gathered}
$$

The arrows indicate research interfaces, not automatic entailments. Theorems 5–8 specify when information about a support model decides its necessity claim. Theorems 1–3 give actual explanatory routes into necessary actuality. Theorem 12 gives an essential-owner route into a necessary mental bearer; a knowledge conclusion additionally requires its truth-linked guard. Theorems 11 and 14 show where operational completeness leaves these questions open.

## The new certificate requirement

A proposed metaphysical inference that relies on a finite source-support representation should identify at least:

**The interpreted source family.** Are its elements propositions, laws, acts, roles, or rigid concrete individuals? What warrants the interpretation and its completeness?

**The support law.** Is the relation conjunctive, alternative, inhibitory, causal, semantic, or merely evidential? Is the support family fixed across the modal alternatives, or must applicability gates be included?

**The absence scope.** Which joint absences have been established as possible or impossible, and under which modality? Which tests remain unqueried rather than negative?

**The target.** Is the conclusion necessary truth, necessary instantiation, a fixed necessarily existent bearer, uniform underivability, essential necessity, or a common knowing subject?

These are not merely documentation fields. In the finite class, the blocker and completion theorems calculate exactly when the target is determined and exhibit a countermodel when it is not.

## A precise inherited-information boundary

Probability-one occurrence is not metaphysical necessity. A finite high-order moment certificate is not a coabsence certificate over possible worlds. An exact observational decoder can return the right conclusion inside every supplied reference state while failing to determine whether its concrete realiser could have been absent.

Conversely, a modal ground theorem is not itself a certificate of practical diagnosis, communication, or restoration. The individual who exists necessarily under the theorem's premises has not thereby been connected to a particular recipient's beliefs, behaviour, or uptake. Those tasks still consume the actual continuation and evidence machinery of [I1].

This keeps the two supplements complementary. The first identifies what a process must remember; the second identifies what its metaphysical conclusion must additionally presuppose or establish.

## What was not obtained from Navier–Stokes

The supplied fluid materials motivate rigorous attention to retained interactions, effective dependencies, and the difference between an abstract result and its target interpretation. They do not prove sufficient reason, metaphysical foundation, essential ownership, or divine mentality. The methods in this packet are modal logic, order theory, finite support duality, topology, and model construction. No hypothetical NS solution is assumed, and no PDE estimate is used as a substitute for a metaphysical bridge.

The key research gain is not the prestige of a physical problem. It is a sharper method for distinguishing a mathematically valid derivation from a semantically adequate metaphysical argument, while still developing the positive argument as far as its explicit premises permit.

# Philosophical adjudication and the current meniscus frontier

A theorem's truth under assumptions is only one part of the requested work. The premises also need philosophical assessment. The most consequential disputes are now localised more precisely than in the original bridge list.

## Actual necessary actuality is a defensible positive candidate, not a derived default

The actual-ancestry route does not need the existence of an independent abstract field of all possibility, S5, or a necessarily occurring orthing episode. It starts from a concrete actuality and a dependence principle restricted to the relevant existential cone. This is a meaningful advantage over inferring a necessary being from a formal object's universal description.

Its strongest remaining challenge is the conjunction of contingent-dependence and a suitable foundation or root premise. A brute contingent actuality denies the first. A genuinely non-well-founded dependence system denies the second. Neither is formally refuted by calling an account explanatory. Their explanatory costs can be argued, but a comparative judgement is not automatically a deductive elimination.

Hume's dialogue supplies a classic objection to the move from explained individuals to a further explanation of a whole, alongside an objection to alleged demonstrative necessity [P12]. We do not assume that conceivability establishes metaphysical possibility, or that a dialogue character's claim settles the debate. The objection identifies where the totality route needs a defended explanatory principle rather than a mere aggregate label.

## The stronger target requires a stronger modal relation

The rotating-root control shows that even worldwise unique roots do not establish one uniformly underived individual. Theorem 3 answers positively under well-founded possible-dependence. That condition is a genuine cross-world constraint, not an automatic consequence of local acyclicity.

An essentialist account may independently support such a constraint in the precise relation of existential derivation. A causal relation between changing states need not. Establishing the correct dependence kind and its cross-world rigidity is therefore a substantive task with a concrete test: can the account exclude the rotating-root and cross-world infinite-dependence structures without assuming the desired uniformly necessary root?

## The intellectual joint remains the decisive common-bearer test

The essential-owner route is valid and nontrivial as a philosophical programme. Its antecedents are not supplied by the mere truth of logical laws, by encoded intentional vocabulary, or by computational complexity. Its positive strength depends on defending the ontology and identity of the alleged necessary intentional item.

The impersonal unified-root model makes the alternative demanding rather than trivial. It already provides a necessary, underived, common order-and-efficacy bearer at the formal level. A successful intellectual bridge must show why such an interpretation is inadequate to the actual objective reason relation, not merely why multiple disconnected resources look inelegant.

This is also the place where a source-authenticated and a neutral route may diverge. A source can provide genuine substantive information about a bearer if its authority and interpretation are established. It must not be treated as mere syntax; neither may its attribution be assumed true without acknowledging the source premise.

## A common bearer is not selected by explanatory economy alone

Unification and simplicity can rationally influence an explanatory comparison. But counting one node rather than three depends on granularity, and naming an entire structure “one source” does not prove one subject. A coordinated plural account can be complex or explanatorily costly without being contradictory. A purported refutation must identify the violated condition, rather than substitute aesthetic dislike for a contradiction.

The arity and query results give a useful discipline: agreement on many partial roles need not settle the joint claim. The relevant common-bearer question must be tested at its actual interaction scope.

## Status against MEN-7 and MEN-8

MEN-7 asks for a dependency-minimal, non-question-begging bridge surviving the relevant alternatives. This packet provides complete conditional bridges to necessary actuality and a stronger uniform-root result; it gives their countermodels and makes their metaphysical warrant obligations explicit. It does not claim to have independently established every antecedent. Full well-foundedness is not falsely labelled the unique minimal premise.

MEN-8 asks for a serious integrated common-model test. Theorem 14 and Model J2 preserve the operational findings together with strengthened necessary-root conditions while withholding mentality. This is an integrated formal control over an explicitly stated theory fragment. It is not a certification that every strongest source-authenticated or essentialist premise in the entire project has been jointly satisfied.

The sharp modal audit supplies an additional candidate contribution: a necessary support claim has an exact obstruction family, exact universal information arity, exact completion test, and exact worst-case query count in the declared finite class. These are proof-backed advances over the delivered continuation packet. They remain closely related to classical blocker and monotone Boolean structure; no independent general-novelty determination has been made.

**Current research verdict:** the positive derivational frontier and the integrated countermodel frontier both advance. A complete world-directed, source-faithful Necessary-Being and attribute ascent is not claimed. A field-level meniscus breach, defeat of every R5 rival, or repository adoption is not self-certified by this delivery.

## The narrowed next mathematical and philosophical burden

The most promising positive continuation is no longer “add more tensor or Nash terminology.” It is to defend one of two substantive bridges with source and metaphysical adequacy intact:

> A properly typed existential dependence principle, with an independently warranted actual or modal foundation, sufficient for necessity in the intended sense; or a necessary intentional item with a defensible essential-bearer relation, then a principled identification of that bearer with the existential ground.

The support calculus now tells us exactly which joint alternatives such an argument must exclude. The modal-collapse analysis tells us what it must not accidentally necessitate. The integrated models tell us which impersonal and plural interpretations survive the formal conditions already obtained. This is a constructive research boundary, not a declaration that further proof is impossible.

# Appendix A — Approach-family campaign and actual outcomes

This register records the mechanisms actually pursued. It does not describe 64 independent agents or claim an eight-hour run. The CDC prompt was guidance for diversity, exactness, and adversarial persistence, not a licence to assert a proof that had not survived checking.

| Family | Mechanism pursued | Strongest obtained result | Main surviving burden |
|---|---|---|---|
| A | Transcendental/no-bootstrap | Exact distinction between least generation and circular fixed points; actual evaluation supplies its actual conditions. | Positive ontological grounding does not follow merely from failure of total self-production. |
| B | Actual dependence and foundation | Theorem 1; actual concrete necessary root under the declared cone premises. | Defend contingent dependence and actual foundation in the intended explanatory relation. |
| C | Contingent totality | Theorem 2; full existential explanation cannot itself be a selected contingent member. | Warrant total explanation and member projection; preserve complete domain scope. |
| D | Cross-world dependency | Theorem 3; uniform underivability from possible-dependence foundation. | Warrant global modal foundation; worldwise foundation alone fails. |
| E | Hypergraph support and modal cuts | Theorems 4–9; exact completion, arity, query count, and recombination result. | Establish the actual support and modal-absence semantics. |
| F | Topological/global witness | Theorem 10; finite necessary support under compact cover and finite recombination. | Compactness, openness, and joint absence are not supplied by finite episodes. |
| G | Intentional ontology/essential ownership | Theorem 12; a fixed essential owner of a necessary item exists necessarily. | Necessary content must really be the same intentional item; identify its owner with the ground. |
| H | Model-theoretic joint controls | Theorems 11 and 14; rotating-carrier and impersonal unified-root models. | Formal consistency is not metaphysical possibility; richer premises may exclude the models. |
| I | Explanation and contingency | Theorem 13; exact collapse condition and a contingency-preserving necessary-knower construction. | A substantive account of contingent acts and explanation. |
| J | Strategic adversarial inquiry | Proposition 1; exact saddle point of a finite modal-audit game. | Correct classification probability is not exception-free warrant or world truth. |
| K | Source-critical attribute ascent | Arabic-wording checks, author/quoted-opponent separation, typed attribute and revelation stages. | Edition-level verification and justification of source/world premises. |

The variants were compared before being combined. A root was not simply declared necessary; the contingent-dependence premise was isolated. The totality route was not concealed inside the local-foundation theorem. The essential-owner argument was not rejected for a quantifier error its authors explicitly address. The possible-dependence result was introduced only after the rotating-root countermodel showed a real gap.

No route was promoted merely because it restated the target. In particular, an unexplained S5 possibility-of-necessary-existence premise, a definition making every adequate ground mental, and an unargued assumption that all contingent contributors can jointly disappear were not counted as completed bridges.

# Appendix B — Claim and premise crosswalk

## New result types

The theorem labels are local to this supplement. They do not allocate repository theorem identities.

| Local result | Formal contribution | Ancestry/status |
|---|---|---|
| T1 | Complete actual cone plus contingent dependence and foundation yields necessary actual root. | Standard foundational/contrapositive mechanism; new explicit deployment and scope repair here. |
| T2 | Total existential explanation plus projection and no self-explanation yields necessity. | Classical totality-style cosmological mechanism; separately typed and certified inference core. |
| T3 | Possible-dependence foundation yields uniform underivability. | Well-founded minimality applied to a modal union; exact strengthened hypothesis made explicit. General novelty not established. |
| T4 | Minimal seed supports exactly characterise finite positive closure. | Standard Horn/antichain construction. |
| T5 | Necessary supported target iff no minimal cut can jointly disappear. | Standard blocker mechanism, interpreted in the declared modal support class. |
| T6 | Exact lower/upper completion trichotomy from a complete $k$-skeleton. | Direct finite downset construction; independently proved here. |
| T7 | Maximum minimal-cut size is the sharp universal audit arity. | Consequence of T5–T6 with an explicit adversarial pair. |
| T8 | Minimal-cut count is exact worst-case deterministic query complexity. | Elementary decision-tree adversary; no claim of efficient blocker enumeration. |
| T9 | Union-closed coabsence yields an all-necessary support. | Finite recombination specialisation. |
| T10 | Compact open support cover plus finite coabsence yields a necessary support. | Standard compactness mechanism with explicit interpretation guards. |
| T11 | Local operational theory survives worldwise contingent-carrier copying. | Isomorphism/conservative-extension construction. |
| T12 | Necessary fixed item plus essential owner implies necessary owner. | Standard de re inference; comparison with actual theistic-conceptual arguments. |
| T13 | Necessary seed facts and necessitating rules make derived facts necessary. | Standard closure of necessity; no novel modal-collapse thesis. |
| T14 | A separate outer-grounding expansion preserves a local theory with an impersonal necessary root. | Scoped integrated model extension, not a complete metaphysical rival validation. |
| P2–P5 | Root unity, role-cohosting obstruction, joint-will compatibility, and contingent-knowledge model. | Elementary or standard mechanisms; limits are part of each statement. |
| P1 | Bounded modal-audit game has value $m/(2m-b)$ and an explicit mixed equilibrium. | Exact finite strategic calculation; no metaphysical probability interpretation. |

## Effect on the repository bridge programme

The source ledger [R3] distinguishes B0–B16. The following is a crosswalk, not a revision of its statuses.

**B0–B1, formal non-self-grounding and world reflection.** The no-bootstrap calculus clarifies the least-generative claim. Actual evaluability remains a real starting premise. A transition from semantic presupposition to positive ontic ground still needs a defended interpretation.

**B2–B3, positive ground and terminality.** T1 and T2 offer different complete conditional routes. T1 uses actual foundation; T2 uses full total explanation. Neither predicate is merely inferred from an open problem's having a determinate answer.

**B4–B5, necessity and external actuality.** T1 derives modal necessary existence of a concrete actual root within its premise package. T3 strengthens the conclusion to uniform underivability under stronger cross-world foundation. A source's necessity-in-itself notion remains separately interpreted. Concreteness comes from the actualiser domain, not from an abstract order acquiring an existence flag.

**B6–B8, common bearer and intellectual/personal character.** P2 can establish root uniqueness at a complete directed scope. P3 and J2 show why this does not automatically establish common mental attributes. T12 is a separate positive mental-bearer route; knowledge additionally requires a truth-linked epistemic guard. Its ontology and identity bridge remain substantive.

**B9–B11, Will, Power, Wisdom.** The effective-ability, intentional-selection, and fitting-end claims stay distinct. P4 identifies a precise incompatibility of independently unrestricted sovereign choices, not a proof against every coordinated plurality. T13 protects the difference between a necessary bearer and a necessarily occurring act.

**B12–B16, source, revelation, a-fortiori predication, and identification.** The Arabic-primary transcription check improves the source-contact layer only. The authentic-source premise, semantic eligibility of attribute inference, occurrence of Speech, and identification with the revealed referent are not discharged by graph or modal enumeration.

## What a world-directed proof still needs

A complete proof of $\mathsf{NB}_{\exists}$ by T1 needs true actual-existence, dependence, domain, and root/foundation premises. A complete proof by T2 needs a true full explanation of the relevant contingent-existence content, projection, and no complete self-explanation. T3 additionally needs the warranted possible-dependence relation, not a graph built only from currently observed alternatives.

For $\mathsf{NB}_{\mathrm{k}}$ and $\mathsf{NB}_{\mathrm{int}}$, the adequate intellectual or intentional-ownership premise, the further knowledge condition where needed, and common-bearer identification must be defended. More extensive numerical checks of the same formal structures will not by themselves make those philosophical premises true.

# Appendix C — Verification, formal certificates, and review

## Exact executable checks

All finite calculations use explicit finite structures. The principal support and modal checks use integer bit masks and exact Boolean logic; the audit-game calculations use rational arithmetic. No floating-point optimisation result is being mistaken for a proof of a modal claim.

| Verification group | Exact scope and result |
|---|---|
| Horn compiler | 4,096 systems; 41,472 comparisons of support-family semantics with direct least closure. |
| Blocker duality | 199 antichains; 2,880 valuation checks. |
| Modal completion | 78,775 completion audits; 28,474 direct necessity equivalences. |
| Sharp arity and query witnesses | 199 support families; 963 lower-arity witness pairs; 490 indispensable-query alternatives. |
| Recombination | 194 nonempty downward-closed complexes; 2,880 implication checks. |
| Joint-absence family | Arities 2–10; 2,035 proper faces checked. |
| Actual-ancestry finite instances | 13,227 satisfying models; 62,581 target-cone checks. All labelled loopless digraphs through four vertices, and fixed-topological-order DAGs on five. |
| Quantifier/rigid-witness matrices | 5,050 matrices; 1,930 rotating-witness controls; 19,406 rigid-witness checks. |
| Role-cohosting family | Arities 2–12; 8,177 proper role sets. |
| Collapse/noncollapse | 16 finite valuation checks and a two-world knowledge model. |
| Joint wills | 481 finite choice profiles. |
| Conservative-copy examples | 70 local isomorphism checks; the general language theorem is a paper proof. |
| Threshold formulas | 36 parameter cases. |
| Uniform modal foundation | 6,309 structures; 511 satisfy the global premises; 577 uniform-root checks. |
| Total explanation | 33,032 structures; 753 satisfy the premise package. |
| Integrated model cards | Three models; 1,022 operational continuations each, plus displayed predicate and game checks. |
| Modal audit games | 54 finite games; 18,432 payoff entries and 2,428 exact best-response equalities. |

These counts overlap in mathematical objects across some groups. They are not a count of independent empirical observations or independent confirmations. The infinite countermodels, compactness theorem, general language constructions, and unbounded finite-family theorems are supported by the written proofs, not by exhaustive enumeration of infinite domains.

## Three checked natural-deduction certificates

The package contains a small, inspectable many-sorted first-order natural-deduction checker and three explicit proof certificates. The checker computes each conclusion from its premises, tracks labelled open assumptions, checks quantifier eigenvariables and sort-preserving substitution, and rejects unlicensed inference rules.

The checked cores are:

- actual root plus contingent dependence gives an actual necessarily existent bearer: 21 nodes;
- a fixed indispensable bearer of a necessary condition exists necessarily: 6 nodes;
- complete total explanation of contingent existence cannot itself be contingent: 18 nodes.

The necessity predicate is expanded as a quantification over worlds, not left as an uninterpreted atom called `Necessary`. The first certificate retains the existence of an actual root as an open premise; well-foundedness supplying that root is proved in the manuscript. The certificates check inference, not the metaphysical truth or completeness of the premises.

Eleven negative controls are rejected: altered final targets for all three proofs; illicit generalisation; escaping an existential witness; world/entity sort substitution; variable capture; an undisclosed open premise; a wrong modus-ponens antecedent; an invented oracle rule; and a dishonest intermediate conclusion.

**This is not Lean verification.** A Lean installation was not available in the execution environment; attempted access to an official binary did not produce an executable runtime. No successful Lean parse, elaboration, comparator replay, or kernel check is claimed. The local checker is itself newly authored and not independently audited. Its source, certificates, exact assumptions, and rejection tests are supplied for inspection.

## Self-review and corrections made

The review here is self-review, not an independent cold audit or distinct fresh rereview. It identified and preserved the following material qualifications.

The actual-root conclusion was separated from uniform underivability and essential necessity. The totality formula freezes actual contingent membership rather than becoming a vacuous material implication. The modal audit's skeleton was required to include negative as well as positive answers. The oracle query lower bound was separated from blocker enumeration cost. The independent strategic game received an explicit payoff and countermodel family. Operational conservativity was restricted to an exact separate signature rather than the vague condition “unless something conflicts.”

The source comparison also corrected a tempting misdescription: Anderson and Welty do address rotating thinkers. The Ibn Taymiyya source was not used to endorse a unity proof he is criticising. The Arabic interface's displayed page number was not equated with independently verified printed-edition pagination.

No property of these fixtures verifies the source-world bridge, human proper function, actual mental uptake, universal Creatorhood, or a revealed identification.

# Appendix D — Source register and evidential distinctions

## Supplied materials

**[I1]** *Continuation-Complete Orthings*, research supplement v1, 8 September 2026; the supplied `orthing_continuation_frontier_v1.zip`, PDF, LaTeX, and Markdown. The Markdown was the principal mathematical reading copy. Its moment duality, continuation closure, information bounds, strategic identification, and coordination results are the predecessor, not new results of this supplement.

**[I2]** *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, version 1, supplied `orthing_formalisation_v1.zip` and corresponding source formats. The representation-first distinctions and earlier discharge and landscape constructions are retained.

**[I3]** *Prompt Used for “A Proof of the Cycle Double Cover Conjecture”*, supplied two-page `cdc_prompt(2).pdf`. Both pages were read and rendered. It supplies campaign heuristics, not mathematical support for Necessary Being. Its claims about a particular model or successful CDC proof were not independently verified here and are not premises of this work.

**[I4]** Charles L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, supplied six-page PDF including errata. It specifies a PDE target, not a solution or a metaphysical conclusion. Its role is inherited methodological context. Official locator: <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>.

**[I5]** Adarsh Ganeshram, Valentin Duruisseaux, and Anima Anandkumar, *Stable Singularity of the Euler Equations on R3*, supplied 107-page `Euler.pdf`. The previous packet's reading and the supplied text are retained as methodological context concerning representation and certification. No new full proof audit, numerical certification, or Lean replay of that paper was performed in this modal campaign.

**[I6]** The supplied conversation, Tao quotation and screenshot, and the owner's frozen distinctions. These establish the research question and the agreed representation boundary. They are not independent evidence of a philosophical theorem or a world's metaphysical possibility.

## Repository basis

All repository paths below are pinned to commit `f50dc1aee52356cc6adbef342387576b02afc124` of `theislampill/orthemology`. Full permanent URLs and returned blob identifiers are supplied in the accompanying provenance register. Historical or proposal statuses remain historical or proposal statuses; access to a file is not its scientific adoption.

**[R1]** `companion/orthability-and-the-ground-of-intelligibility.md`. The principal school-neutral companion, with its objective-evaluability, anti-total-emergence, intellectual, and attribute arguments. Its original distinction from both a standard contingency argument and a modal-ontological argument controls our classification of the new side routes.

**[R2]** `docs/project-closure/ar8r-v11/programs/track-t-authority-and-bridge-status.md`. The current scope of Track T's accepted negative and conditional claims; not a completed necessary-ground proof.

**[R3]** `docs/project-closure/ar8r-v11/programs/AR8R-TRANSCENDENTAL-BRIDGE-AND-RIVAL-LEDGER-V11.yaml`. B0–B16 bridge owners, rival and premise status. The crosswalk above does not amend this ledger.

**[R4]** `docs/project-closure/ar8r-v11/programs/ar8r-r5-minimal-nonintegration-control.md`. Scope of the common-model withholding programme and what would be required to defeat it.

**[R5]** `docs/project-closure/ar8r-v11/programs/candidate-n-r5-track-t-and-source-ascent.md`. Candidate N, root/role transports, common-bearer conditions, and surviving impersonal/plural rivals. These are prior project work, not newly recovered here.

**[R6]** `docs/project-closure/ar8r-v11/programs/AR8R-ORTHEMOLOGY-MENISCUS-MILESTONE-ARCHITECTURE-V1.md`. M10–M13, MEN-7/MEN-8, the anti-microresult rules, and source/formal/world distinctions; an owner programme charter, not a result certificate.

**[R7]** `docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_THEOREM_FILES/PMR-007_DEEP_ROUND_J_COMMON_ANCESTRY_AND_UNDERIVED_ACTUALIZER_UNITY_V2.md`. Standard finite-DAG root theorem, conditional sufficiency guards, and common-bearer limitations.

**[R8]** `docs/project-closure/ar8r-v11/post-merge-pmr001-source/PMR_M3_01_CANDIDATE.md`. Necessary existence, originator, attributes, and Creator are separately typed. Its original proof uses declared predicates and does not itself establish cross-world necessity. The present world-explicit deductions are additional candidate work, not a renaming of its guarded predicate rules.

**[R9]** `docs/project-closure/ar8r-v11/programs/p597-p620-source-ascent-status.md`. Later source-ascent status and continued external verification and review burdens. Also consulted: `companion/orthemic-modal-metaphysical-assessment.md` for the wider modal boundary.

## Primary philosophical and mathematical sources

**[P1] Gottfried Wilhelm Leibniz.** *On the Ultimate Origination of Things* (23 November 1697), primary work in translation, manuscript locator LH 4, 1, 10, fols. 2–4. Author-text translation retrieved in indexed form; a separate Inters page did not open fully. The relevant comparison is the difference between reasons inside a series and a sufficient reason for its existence. We do not adopt Leibniz's complete subsequent metaphysics. <https://www.leibniz-translations.com/ultimateorigination>.

**[P2] James N. Anderson and Greg Welty.** “The Lord of Non-Contradiction: An Argument for God from Logic,” *Philosophia Christi* 13(2), 2011; author-hosted 22-page manuscript. The paper's sections and footnotes 31–33 were read; relevant PDF pages were inspected visually. This is primary philosophical ancestry for the intentional-item and essential-owner route, not a completed argument adopted by Orthemology. <https://www.proginosko.com/docs/The_Lord_of_Non-Contradiction.pdf>.

**[P3] Ibn Taymiyya.** *Commentary on the Asfahani Creed*, Arabic primary work accessed through digital transcriptions. The Usul record names editor Muhammad ibn Riyad al-Ahmad, al-Maktaba al-Asriyya, Beirut, first edition, 1425 AH. Its interface URL ends in `/94` but the displayed footer reads `1 / 98`; no scanned printed page was verified. The incipit and exact URL are therefore the reliable retrieval locators, not an asserted printed page number. The passage distinguishes a concrete necessary existent from a merely mental unrestricted universal. The longer Wikisource transcription was consulted at the discussions of necessary existence versus Maker, the criticised unity proof, and perfection predication. These are transcription-level Arabic checks, not a critical-edition authentication. <https://usul.ai/t/sharh-caqida-isfahaniyya/94>. The accompanying source register preserves the full Wikisource locator and short Arabic anchors.

**[P4] Olley Pearson.** “Grounding, Well-Foundedness, and Terminating Chains,” *Philosophia* 51 (2023), 1539–1554; published online in 2022. The primary article was consulted for the distinction between mathematical termination and more nuanced foundational structures. It does not justify assuming our particular grounding relation is well-founded. DOI `10.1007/s11406-022-00593-x`. <https://link.springer.com/article/10.1007/s11406-022-00593-x>.

**[P5] Ricki Bliss.** “Viciousness and Circles of Ground,” *Metaphilosophy*, 2014. Primary publisher abstract/bibliographic evidence was consulted; full argument verification is not claimed. This records a serious challenge to automatic dismissal of circular ground, not a proof of any circle's adequacy. DOI `10.1111/meta.12072`.

**[P6] Edward N. Zalta.** “Essence and Modality,” *Mind* 115(459) (2006), 659–693. Author-hosted abstract consulted, including its treatment of Fine's counterexamples and its own differentiated response. The source motivates not treating modal invariance as an unexamined definition of essence; a full-paper review is not claimed. <https://mally.stanford.edu/abstracts/essence.html>.

**[P7] Endre Boros, Vladimir Gurvich, Martin Milanič, and Yushi Uno.** “Conformal Hypergraphs: Duality and Implications for the Upper Clique Transversal Problem,” *Journal of Graph Theory* 109(4) (2025), 466–480; arXiv `2309.00098`. The primary definitions of minimal transversals and dual hypergraphs were inspected. The modal consequences in this supplement are separately proved; standard blocker structure is not claimed as new. DOI `10.1002/jgt.23238`. <https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.23238>.

**[P8] Roberto Loss.** “Grounds, Roots and Abysses,” *Thought*, 2016. Primary publisher abstract consulted. Its treatment of recombination and grounding marks direct conceptual prior art; no theorem-specific full-text claim is made. DOI `10.1002/tht3.192`.

**[P9] Alexander R. Pruss.** Author-hosted treatment of the Leibnizian cosmological argument, including discussion of explanatory sufficiency and entailment. Relevant indexed passages were retrieved; opening the full author page timed out. This is not reported as a full monograph or chapter review. <https://alexanderpruss.com/papers/LCA.html>.

**[P10] Kelly Trogdon.** “Grounding: Necessary or Contingent?” *Pacific Philosophical Quarterly* 94(4) (2013), 465–485. Primary abstract read. It defends modal entailment by full grounds through substantive epistemic and essence principles, rather than treating that entailment as trivial. DOI `10.1111/papq.12009`.

**[P11] Kenneth L. Pearce.** “Metaphysical Rationalism Requires Grounding Indeterminism,” *Journal of the American Philosophical Association* 11(2) (2025), 303–322. Primary full text consulted, particularly explanatory autonomy, necessary existence, and the relation between rationalism and necessitation. This is close prior art for the explanatory pressure addressed in our modal-collapse section; no novelty is claimed for that general philosophical thesis. DOI `10.1017/apa.2024.17`.

**[P12] David Hume.** *Dialogues Concerning Natural Religion*, Part IX, primary text in the Hume Texts Online edition. The Demea, Cleanthes, and Philo speeches are distinguished; no speech is automatically treated as the author's final endorsement. Sections 9.3 and 9.5–9.10 provide the relevant contingency, totality, and necessity dialectic. <https://davidhume.org/texts/d/9>.

## Prior-art and source limits

No general novelty is claimed for minimal-element arguments, totality cosmological reasoning, Horn closure, blocker duality, compactness, isomorphism preservation, essential-owner inference, or the modal-collapse observation. The modal-completion audit, exact arity/query calculations, and their combined use in the present grounding programme were worked out and checked here, but a comprehensive historical priority determination was not completed.

The primary source search was used to challenge and improve the argument, not to search for a purported ready-made solution to the CDC task. The source register distinguishes full-text, abstract, indexed-excerpt, transcription, and repository evidence. Unread or inaccessible details have not been silently supplied from general knowledge.

# Appendix E — Reproduction and delivery boundary

The accompanying Markdown is the mathematical reading source. The supplied build script regenerates the LaTeX from it using Pandoc and the included template/filter, then compiles the PDF with XeLaTeX. Fonts are referenced as installed dependencies, not distributed in the archive.

Run the verification scripts independently of the document build. They write explicit JSON receipts with scopes and counts. The natural-deduction certificate generator and checker are separate modules, but were authored in this same campaign and do not constitute independent scientific review.

The provenance manifest binds the predecessor archives and all supplied PDF inputs by SHA-256. The repository references are pinned to the observed commit, with returned blob identifiers recorded where available. The new package is an additive successor: it does not overwrite either previous research archive, alter any repository theorem, or claim that the conversation has been retroactively registered as a canonical episode.

The delivery's strongest status is: **ordinary formal proofs under explicit hypotheses, exact finite and rational verification, a locally checked inference core, and a source-sensitive modal/metaphysical research advance**. What remains open is not concealed: the world-directed warrant for the central metaphysical premises, the intellectual/common-bearer bridge, and independent specialist adjudication of the integrated candidate.
