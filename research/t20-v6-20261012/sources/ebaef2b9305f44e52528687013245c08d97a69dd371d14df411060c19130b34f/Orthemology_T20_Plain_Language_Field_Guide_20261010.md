# Orthemology T20 — a plain-language field guide

**Scope:** 62 distinct research-archive names found among the attached standalone ZIPs and the 27 nested ZIPs of `T20bigupdate.zip`, plus the current conversation's summaries. Several packages are cumulative, share antecedents, or add verification rather than independent discoveries. This is a *study map*, not a fresh line-by-line proof audit, Lean replay, specialist novelty review, empirical validation, or owner acceptance. **T20 remains open.**

## The two-minute version

Think of a scientific investigation as a living notebook. It contains claims, observations, where the observations came from, beliefs about them, rules for drawing conclusions, and questions that may be asked tomorrow.

Orthemology asks: **How do we get things right; how do we know when we've got them right; and how can the investigation change without losing the information that made it trustworthy?**

The recent T20 mathematics asks seven related questions:

1. **Evidence:** When does a report matter, especially after we learn it was unreliable?
2. **Compression:** How much of an enormous information record can we throw away without making a later question unanswerable?
3. **Correction:** Can we repair incoherent beliefs without corrupting what the evidence actually says?
4. **Inquiry:** Which next test or proof is worth doing, and what does it really cost?
5. **Proof systems:** What happens when a claim is true in a model but the available formal rules cannot prove it?
6. **Infinite information:** When do complete measurements determine hidden reality, and when can we compute that reality?
7. **Philosophical foundations:** What warrants speaking of original causation, knowledge, will, wisdom, and rightful authority?

The surprising achievement is not that all seven have been solved. It's that individual results are beginning to **constrain and improve the others**.

## Story 1 — A discredited witness can still provide useful information

Imagine Witness A gives a number. You discover Witness A was generating numbers randomly. Does that mean you must delete the number from your notebook?

Not necessarily. Suppose another audit reports how Witness A's output was correlated with a different, genuinely informative measurement. Even if A was not a trustworthy witness, the *observed random number* may still be essential for understanding the audit. In Dot's exact finite example, retaining the report and its audit yielded a posterior of **1/5**, whereas deleting the report while retaining the audit gave **1/2**.

**Lesson:** *Defeating a source's authority is not the same operation as erasing an observed event.* Updating, withdrawing a claim, forgetting a source record, and changing a rule are all different.

The mathematical work specifies when information can be forgotten while preserving present or future corrected answers. The source work investigates parallel distinctions: a defeated argument need not erase all other grounds of knowledge.

**Not established:** an algorithm that authenticates arbitrary witnesses or certifies real-world epistemic warrant from probabilities alone.

## Story 2 — A photograph of the present is not a recording of the future

Imagine two video games whose dashboards both read **60% complete**. They may be at different levels, have different equipment, and require different next actions. The same dashboard number does not tell you how the games will evolve.

This is the central intuition behind Orthemology's **continuation** research. Two rich states can agree under a compressed representation, yet produce different answers after the next permitted operation.

**Tensors** help preserve relationships involving several variables at once. The older parity examples show that even *all* lower-order observations can agree while a higher-order relation differs. Later work proves finite-support cases where a sufficiently rich hierarchy of retained interaction tensors preserves *every permitted future correction*. It also gives sharp counterexamples showing why preserving a current value—or even its immediate rate of change—can be insufficient.

A separate, stronger point emerges in the audit research: storing the answer you would give *after* every audit may still not tell you whether the audit is **worth performing**, because you also need the probabilities of the possible audit outcomes. In one fixed-cost example, that omission reverses the optimal decision.

**Lesson:** A good summary must be sufficient for the **future questions and operations you care about**, not merely faithful to the present answer.

**Not established:** a universal small memory that answers every possible future question, or a claim that all applications must use high-order tensors.

## Story 3 — Tidying a belief is not the same as learning

Suppose someone writes the probabilities of three mutually exclusive possibilities as 0.6, 0.5 and 0.2. They add to 1.3, so the bookkeeping is incoherent. A geometric rule can move these numbers towards a valid total of 1.

Orthemology's earlier scoring-rule work contains genuine Hessian/Bregman mathematics showing a direction of local improvement under its assumptions. Dot then asked two important questions:

- Does that correction **stay inside an allowed region**, or can it hit a forbidden boundary?
- If you retain only the sum, have you kept enough information to predict the correction?

For coordinate-separable Hessian models, requiring all-start safety plus a self-predicting sum under the original clock selects a special logarithmic/negative-Shannon family for at least three coordinates. But Dot subsequently removed the separability assumption and discovered a broader **nonseparable** family permitting radial normalisation, including quadratic/Brier-compatible coherent geometry.

Then Dot made the stronger challenge: *A mathematically consistent repair can distort correct Bayesian learning.* An uninformative observation should not change the relative beliefs about hypotheses merely because a repair procedure was applied. This motivated conditions for evidence-compatible updating and for model correction to commute with conditioning.

Under stronger stochastic-channel contraction conditions, KL geometry is selected within the specified class; under weaker normalisation requirements, it isn't. This is **a hierarchy of assumptions**, not a contradiction between successive theorems.

More recent work treats observations that eliminate possibilities entirely, and the geometry of their resulting **faces**. It also warns that apparently consistent pairwise probability records—even with a positive-definite covariance matrix—may fail to describe *any* genuine joint probability law.

**Lesson:** *Mathematical downhill motion ≠ correct evidence updating ≠ warranted knowledge*. The chosen geometric model has to retain the actual relevant structure and respect source, support and authority conditions.

**Not established:** a general experimentally validated Riemannian model of human cognition, or a universal metric for every DAEE state.

## Story 4 — Which proof, test or investigation should we perform next?

Imagine two ways to prove a claim. One needs no new sources but takes 10 units of checking. The other needs one further piece of evidence, then takes only 2 units altogether. The route with the *fewest missing facts* is not necessarily the least expensive or most worthwhile.

Dot developed formal finite proof catalogues, including **ordered source-support guards**, actual proof witnesses, and distinctions between paying for a repeated proof step each time and paying once for a reused lemma. Lean verifies some source-level proof-compilation components, whereas other general or cost-hardness arguments have written proofs and executable checks.

The cost question becomes hard when different proofs share steps: two routes that are separately cheapest need not form the cheapest combined proof. Higher-order overlaps can matter; simple pairwise overlap summaries can lose the cost of a three-way shared step.

The inquiry work asks the analogous question for experiments. An investigation may be informative but expensive. To decide whether to run it, you may need branch probabilities and consequences, not just future conditional answers. Some stochastic inquiries can eventually terminate with an error-free answer; superficially similar representations may not preserve that possibility.

**Lesson:** The goal is *least costly warranted resolution under declared rules*, not minimum activity, minimum number of premises, or automatic confidence.

**Not established:** a fast universal proof optimiser, unrestricted natural-language debate oracle, or validity of the premises that the formal checker was supplied.

## Story 5 — A true identity may be beyond the current proof rules

Think of a small calculator whose instructions let it add and multiply but not divide. Some numerical relations hold in its intended interpretation, yet the calculator's available instruction language cannot derive them.

This is the intuition behind the **HasE** type-theoretic programme. The original compiler identity held in the specified intended full-PER interpretation, but Dot's countermodels establish that neither the literal identity nor its negation is derivable in the **unchanged** HasE calculus. This is a precise expressivity/completeness limit, not a claim that the identity is mathematically false.

The next work asks which further principle would let the system prove the needed claims. It distinguishes a **rigidity** principle (in a suitable sense, preserving zero and successor determines an iteration) from a **dependent-pair reconstruction** principle (roughly, a pair can be identified with the pair formed from its projections).

Dot has Lean-checked conditional dependent induction, recursor uniqueness, substitution across the full HasE rules, and related construction results. Most recently, models separate the two **specified literal completion principles**: fixing one does not automatically give you the other. This is not a proof that every possible extended completion scheme is independent.

**Lesson:** *True in the intended model*, *provable from the current rules*, and *provable after adding an explicit principle* are three different achievements. Formalising the distinction stops a theorem from claiming more than the calculus earned.

**Not established:** global completeness for all type-theoretic identities, automatic adoption of new axioms, or a theorem that the philosophical reality being modelled follows from a Lean proof.

## Story 6 — Knowing every measurement doesn't always tell you how reality changes

Imagine identifying a hidden distribution of objects from measurements called *moments* (roughly, repeated weighted averages such as mean, squared mean and higher powers).

For known finite support, enough moments recover the hidden weights; this programme has Lean-checked finite algebraic recovery and the existence of projections that separate finitely many distinct vectors over an infinite field.

But with unbounded support, two different probability laws can have **all the same moments**, yet differ when new observations change the weighting. That can produce different future trajectories. Even agreement of *every derivative* at one geometric endpoint can fail to identify a continuation.

Dot then investigated what *extra information* repairs this: compact-support conditions, exponential-tail bounds, effective names of moments, an appropriate Laplace-type transform, and valid probability-law interpretations.

The most recent classification says that, for a stated normalised moment-evolution equation, every admissible evolution arises from an initial law via exponential reweighting. Its possible evolutions correspond exactly to the possible laws with the initial moments. If the initial moments uniquely determine the law, the evolution is unique **within the stated realisable class**.

Computability introduces another question. Uniqueness doesn't invariably provide a computable answer without a justified effective input representation. Under a particularly precise half-line contract—uniform computable moment names, actual valid probability law and a **promise of determinacy**—Dot later proves a positive computable-recovery theorem, without needing a positive exponential tail. This improves the earlier narrower results rather than contradicting their different impossibility examples.

The stationary-law work makes a similar distinction: approximate equilibrium, the existence of an equilibrium, uniqueness, and the ability to compute an equilibrium are not identical.

**Lesson:** *Enough information in principle* and *enough effective information for an algorithm* are different. A tidy finite model can miss what happens at infinity or at a boundary.

**Not established:** an unrestricted algorithm to recover any arbitrary hidden law, or guaranteed validity of a proposed probability evolution from positive-looking coordinates alone.

## Story 7 — The affirmative philosophical programme is still there

Alongside all this mathematics, Dot has continued reading Ibn Taymiyyah and Ibn al-Qayyim to investigate objective orthability, actual original sourcehood, intrinsic necessity, unique original productive efficacy, Knowledge, Will, Wisdom, warranted recognition and binding authority.

The recent source work investigates **particular, intentionally wise acts** rather than treating 'wise' as an unspecified label. It distinguishes a fitting purpose from mere fortunate outcome; an intrinsic divine act from a creature supplying perfection; a standing capacity or foreknowledge from the occurrence of a particular response; and an actual command from mere advice or an earlier absence of prohibition.

The particular source passages are used to explain named examples: wise mediation, self-praise, repentance-conditioned rejoicing, rightful undertaking and the reasons behind particular acts. Dot also recovered earlier developed arguments when a new narrow case might otherwise have been mistaken for a large reopened gap.

**Lesson:** The positive metaphysical programme isn't just waiting for the mathematical work to finish. The two programmes are interacting: philosophical questions reveal distinctions the mathematics ought to preserve, while formal mathematics tests the consequences of proposed distinctions.

**Not established:** an unconditional Lean proof of one Creator, exhaustive explanation of every particular divine act, or a complete philosophical argument from all the newly formalised mathematics to actuality.

## Three timeline corrections worth remembering

**'The log score is the only one.'** True only for the original *specified separable, safe, original-clock scalar-closed* class. A broader nonseparable class allows other coherent geometries. Stronger information-monotonicity requirements reselect KL for a different reason.

**'The original HasE identity is still open.'** That was an earlier checkpoint state. Later the exact unchanged-calculus target was proved independent (neither it nor its negation derivable), and Dot moved to characterising the missing conditional completion principles.

**'An infinite moment record cannot recover the law.'** Too broad. Several models exhibit nonuniqueness or noncomputability, but later theorems give effective recovery under stronger named representation/determinacy promises. Always carry the quantified domain and representation assumptions.

## A good mental picture of how the pieces fit

```text
REAL CASE / CLAIM
      ↓
What was observed, by whom, through which sources?
      ↓
What information must be kept for the next question?
      ↓
What do the evidence rules permit us to infer or change?
      ↓
Can a geometric / statistical correction preserve that meaning?
      ↓
What should we investigate or prove next, at what cost?
      ↓
Can our proof language actually certify the needed conclusion?
      ↓
Retain the result, negative controls, open assumptions and history
      ↺ new questions and corrections
```

The arrows are a *conceptual learning map*, **not** a single verified software pipeline that currently integrates all of T20.

## Five-word glossary

- **Orthing:** a governed investigation and handling process.
- **Orthability:** conditions for something to be correctly distinguished or evaluated.
- **Noetic:** concerning knowing, understanding, reasoning and judgement.
- **Tensor:** a structured mathematical container for multiway relations or interactions; type and semantics matter.
- **Hessian / Riemannian metric:** mathematical tools for measuring local shape and steepness in a chosen smooth model.
- **Gradient correction:** change along a direction that lowers a stated objective; not automatically a truth-improving step.
- **Moment:** a numerical aggregate of a distribution, often an integral of a power.
- **Continuation:** what future answers or dynamics can be recovered from what we retain now.
- **PER / HasE:** a specified mathematical interpretation / original formal type-and-identity calculus in T20.
- **Rigidity:** an additional specified principle connecting a structure's defining operations with uniqueness of its behaviour.

## What to believe about the evidence

The attached archives preserve **mixed verification statuses**. Some named formal subresults have Lean 4.19.0 checks and source-bound replay records; other theorems have ordinary mathematical proofs plus exact Python/SymPy controls; Arabic-source arguments have passage-specific source reviews; some statements are hypotheses, counterexamples or application proposals. Internal AI reviews are not external human specialist reviews. ZIP CRCs and manifests establish integrity, not theorem truth. Most newest research is **not yet adopted as repository mainline**. Nothing in this guide declares T20 complete.

---

## Archive lookup: grouped by research story

The following is a **navigation index**, not a list of novel theorems. A few packets cover multiple stories and are placed under their principal subject for convenience.

### 1. Proof search, evidence contracts and investigation cost (5 archive names)

- `T20_Constructive_Proof_Compiler_and_Knowledge_Update_20261009(1).zip`
- `T20_Guarded_Proof_Compilation_Verification_Supplement_20261009(1).zip`
- `T20_Guarded_Shared_Proof_Attainment_Supplement_20261009(1).zip`
- `T20_Shared_Proof_Cost_and_Information_Update_20261009(1).zip`
- `T20_Resumed_Research_Intermediate_Checkpoint24_20261009(1).zip`

### 2. Evidence provenance, audit, learning and inquiry value (6 archive names)

- `T20_Source_Audit_Revision_Intermediate_20261010.zip`
- `T20_Audit_Continuation_Transport_Intermediate_20261010.zip`
- `T20_Posterior_Inquiry_Value_Intermediate_20261010.zip`
- `T20_Exact_Reset_Continuation_Reviewed_20261009.zip`
- `active-t20-evidence-revision-checkpoint-20261009.zip`
- `stochastic-inquiry-cumulative-evidence-20261010.zip`

### 3. Geometry, tensor interaction and Bayesian correction (10 archive names)

- `T20_Hessian_Admissibility_Research_Checkpoint_20261009(1).zip`
- `T20_Nonseparable_Bayes_Repair_Reviewed_20261009.zip`
- `T20_Information_Noetic_Tensor_Transport_Reviewed_20261009.zip`
- `channel-natural-repair-intermediate-20261009.zip`
- `T20_Channel_Tensor_Research_Evidence_20261010.zip`
- `T20_Constraint_Research_20261010.zip`
- `T20_Leafwise_Geometry_and_Wise_Means_20261010.zip`
- `T20_Hierarchical_Marginal_and_Event_Feasibility_20261010.zip`
- `T20_Facial_Geometry_and_Evidence_Commutation_20261010.zip`
- `Fisher_Endpoint_Geometry_Evidence_20261010.zip`

### 4. Moments, hidden distributions, dynamics and computability (8 archive names)

- `Capped_Tensor_Recovery_Evidence_20261010.zip`
- `Determinate_Moment_Effectivity_Evidence_20261010.zip`
- `Exponential_Tail_Effectivity_Evidence_20261010.zip`
- `Effective_Stationary_Selection_Evidence_20261010.zip`
- `Realizable_Moment_Dynamics_Evidence_20261010.zip`
- `finite-moment-recovery-source-and-evidence.zip`
- `T20_Separating_Projection_Lean_Reviewed_20261009.zip`
- `T20_Source_Measure_Continuation_Intermediate_20261009.zip`

### 5. Formal type theory, identity and completion (22 archive names)

- `Actual_E_Dependent_Induction_Evidence_20261010.zip`
- `Actual_E_Sigma_Elimination_Evidence_20261010.zip`
- `Actual_HasE_Dependent_Substitution_Evidence_20261010.zip`
- `Actual_HasE_Mixed_Substitution_Evidence_20261010.zip`
- `Completion_Principle_Separation_Evidence_20261010.zip`
- `Conditional_Dependent_Section_Evidence_20261010.zip`
- `Conditional_Unit_And_Fold_Transfer_Evidence_20261010.zip`
- `Generic_Rigidity_And_Literature_Evidence_20261010.zip`
- `Induction_Rigidity_Converse_Evidence_20261010.zip`
- `Multi_Front_Successor_Evidence_20261010.zip`
- `Rigidity_Uniqueness_Complete_Branch_Evidence_20261010.zip`
- `Sigma_Tag_Boundary_Evidence_20261010.zip`
- `T20_Finite_Raw_And_Typed_Observers_Evidence_20261010.zip`
- `T20_Henkin_Model_And_Source_Independence_Evidence_20261010.zip`
- `T20_Structured_Context_And_Local_Correction_Evidence_20261010.zip`
- `hase-closed-church-completeness-evidence-20261010.zip`
- `hase-complete-development-extractor-20261010.zip`
- `hase-source-continuation-20261010.zip`
- `hase-type-completion-evidence-20261010-v2.zip`
- `hase-type-completion-evidence-20261010-v3.zip`
- `hase-type-completion-evidence-20261010.zip`
- `type-extension-preservation-20261010.zip`

### 6. Affirmative philosophical and Arabic-source work (9 archive names)

- `Immanent_Self_Praise_Evidence_20261010.zip`
- `Repentance_Response_Condition_Evidence_20261010.zip`
- `Responsive_Receptivity_Recovery_Evidence_20261010.zip`
- `T20_Conditional_Recipient_Right_Source_Evidence_20261010.zip`
- `T20_Intrinsic_Succession_Application_Evidence_20261010.zip`
- `T20_Particular_Determination_Source_Packet_20261010.zip`
- `T20_Particular_Explanation_Research_Evidence_20261010.zip`
- `T20_Wise_Reason_Application_Evidence_20261010.zip`
- `active-t20-source-successor-checkpoint-20261009.zip`

### 7. DAEE application and assurance (2 archive names)

- `Interpretation_Repair_Assurance_Evidence_20261010.zip`
- `noetic-recognition-guard-intermediate-20261009.zip`

**Reading suggestion:** start with the seven stories above. Only use the specific archive group when you want to check its assumptions, counterexamples, Lean claims, or source citations. A cumulative package may duplicate predecessor evidence; do not add package counts as discovery counts.
