# Source audit revision with retained observation history

10 October 2026 UTC. Substantive T20 continuation in a new scratch-only research packet. No protected source, repository integration, accepted appraisal, or programme status is changed. The probability laws below are declared finite examples, not measurements of an actual source, person, theological claim, or state of warrant.

## Result and the precise increment

A source report can cease to deserve its old evidential weight without the fact that the report was observed disappearing from the evidence. The correct operation is to condition the joint observation model on the audit, or equivalently to replace the old report likelihood by its audit-conditioned likelihood together with the audit likelihood. Deletion is a special case of that replacement, with an exact condition.

Even the strongest natural audit-aware deletion rule can fail. That rule retains all other evidence, incorporates the audit under its correct joint model, and drops only the old report. It is exact precisely when the report is conditionally uninformative about the target after the retained evidence and audit are fixed. Merely learning that the report came from a random source is insufficient when the audit selection depends on that report and another informative signal.

The main finite example makes this distinction operational. A report initially raises a binary target probability from 1/2 to 7/10. An audit then certifies that this particular source was a fair randomizer and that an independent 4/5-accurate verifier disagreed. The correct posterior is 1/5. Deleting the report while retaining the audit gives 1/2; deleting its old factor while retaining the original report-conditioned audit likelihood gives 3/31. Both failures are exact. A positive replacement computes 1/5 without treating the withdrawn report as still trustworthy testimony.

This is classical Bayes, conditional independence, selection, and proper-score accounting specialized to an interface not implemented by the inspected accepted-evidence store. No new probability theorem or field-wide novelty is claimed. The useful addition is a complete source-audit update contract, its strongest-rival counterexample, exact executable controls, and a separately bounded zero-probability-audit obstruction.

## 1 Prior coverage was checked before making the claim

The relevant inherited sources are bound by bytes in INPUT_BINDINGS.json.

- Deep AX V2, §§1–5 and §8, already supplies architecture-conditioned joint source likelihoods, conditional-independence restrictions on multiplication, exact-copy invariance, and separate source/world/warrant gates. Section 2 explicitly permits zero likelihood under one candidate and excludes outcomes impossible under both. Its pinned Orthemology commit is 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c; the local file was rehashed to its recorded Git blob 4d5960413f16c1f9dab66c2b80ff48316352b804. [Pinned Deep AX](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_THEOREM_FILES/PMR-007_DEEP_ROUND_AX_SOURCE_TESTIMONY_LIKELIHOOD_AND_WORLD_GATE_V2.md).
- The prior provenance-learning RESULT §1 explicitly limits inverse-factor withdrawal to an accepted-evidence store and warns that informative selection/withdrawal history must be modelled. Its independent review §3 and independent_controls.py already contain a neutral report combined with a target-dependent selector. Thus neither the general warning nor the weaker example of an informative audit with a neutral report is new here.
- The warranted-learning RESULT §§6–8 already supplies proper Bregman score regret, information-minus-regret accounting, sequential conditional likelihoods, and the separation of likelihood correctness from coherence repair. The present packet applies those identities to a concrete deletion policy; it does not rediscover them.
- The evidence-withdrawal-warrant REPORT distinguishes access loss, invalid derivation, authority/permission withdrawal, premise defeat, and learning falsity. It specifically requires a separate channel for observed retraction or reliability failure and warns against erasing historical acquisition or current basing. Those semantic distinctions are inherited, not replaced by the finite examples.
- The reset/guarded-revision RESULT concerns certificate eligibility and finite status-state continuation. It expressly does not turn clearing a coordinate into erasure of actual knowledge.
- The inherited tensor continuation manuscript already has proper-marginal parity collisions, future inquiries that expose them, and action-sensitive state adequacy. Its parity-continuation discussion and the later tensor-moment RESULT §3 maintain the required operation scope; the latter explicitly distinguishes different semantic slots from repeated symmetric-power slots. The audit instantiation in §6 below uses these inherited distinctions and claims no new parity or tensor theorem.

The inspected records do not give the eventwise support-sensitive deletion criterion below, the audit-retaining deletion failure despite genuinely random source status, or the corresponding full revision implementation and score controls. This is a bounded comparison with these records, not an exhaustive search of every prior project file. A keyword sweep of accessible nearby research reports found no earlier null-audit regularization theorem; the existing null-evidence dynamics report concerns uninformative positive-probability observations, a different question.

The broad ancestry is classical. Rubin's original missing-data work treats when a data-observation mechanism can be ignored. The present equality is derived directly for the stated target and full-history experiment, and is not presented as a new general missing-at-random criterion. Only the abstract and bibliographical information of the [ETS author report](https://www.ets.org/research/policy_research_reports/publications/report/1975/hrri.html) were consulted here; no complete-paper reading credit is claimed.

## 2 One joint law and four different operations

Fix finite random variables:

    Θ  target state with a fixed meaning and time index
    B  retained background and other observations
    Y  the actual source report that was observed
    A  later audit information, including relevant audit selection/history

Use one declared joint law P. Conditional source status, shared reliability, provenance uncertainty, and additional verifier observations can be latent variables marginalized in this law. Their inclusion is a modelling commitment; a variable named “reliable” does not authenticate anything.

Fix a history B=b, Y=y, A=a with positive probability. Write N for normalization of a nonnegative vector of positive total mass. Define, where the relevant conditionals exist,

    p_b(θ) = P(θ | b)
    L_y(θ) = P(y | θ,b)
    K_a(θ) = P(a | θ,b,y)
    M_a(θ) = P(a | θ,b)
    J_ya(θ) = P(y,a | θ,b)
    L_y|a(θ) = P(y | θ,b,a).

On supported coordinates, the chain rule gives

    J_ya = L_y K_a = M_a L_y|a.

The posterior before the audit and the correct full-history posterior are

    q_old = N(p_b L_y),
    Q = P(Θ | b,y,a) = N(q_old K_a) = N(p_b J_ya).

No independence assumption is used. In particular K_a usually differs from M_a because Y is already in the conditioning history.

At a coordinate where a conditional factor is undefined because its conditioning event has zero probability, no arbitrary conditional value receives evidential meaning. Use the joint J_ya directly, or restrict the factorization to its supported coordinates. The joint expression for Q remains the primary definition.

Four outputs must be distinguished:

1. **Full-history update:** Q = N(p_b J_ya).
2. **Bare deletion:** q_bare = p_b, dropping both the report's discrimination and any new audit discrimination.
3. **Audit-aware deletion:** R = P(Θ | b,a) = N(p_b M_a). This is the strongest natural rule that retains the audit and other evidence but really forgets Y.
4. **Divide then use the old sequential audit:** S = N((q_old/L_y) K_a) = N(p_b K_a), when division is defined. This retains the conditional audit factor from a history that included Y after deleting Y's own factor. It is a different rule from R.

A purported deletion that reconstructs all the missing report/audit interaction and returns Q is a valid replacement in another factorization; it is not a rival to the full-history update. The dispute is not about the spelling of a factor. It concerns which information the resulting distribution actually conditions on.

## 3 Exact deletion conditions including support

### Proposition 1 Eventwise audit-aware deletion

For a positive-probability history (b,y,a), Q=R if and only if

    P(y | θ,b,a)

is constant for θ in the support of R. That constant is necessarily P(y | b,a)>0. Equivalently,

    J_ya(θ) = c M_a(θ)

on the support of p_b, for a single c>0. Coordinates with M_a(θ)=0 have J_ya(θ)=0 and impose no further restriction.

**Proof.** Put r=R. Bayes gives Q(θ)=r(θ)L_y|a(θ)/Σφ r(φ)L_y|a(φ). At every coordinate with r(θ)>0, Q(θ)=r(θ) is equivalent to the likelihood equalling the denominator. Conversely that equality on the support yields Q=r. The equivalent joint-likelihood form follows by multiplying by M_a. ∎

For all report outcomes y and audit histories (b,a) in the supported model, exact deletion is equivalent to Θ and Y being conditionally independent given (B,A). Eventwise equality for one observed y is weaker than that global condition. With a full-support p_b, the eventwise joint proportionality condition is also the exact condition for equality under every full-support prior on the same channel. With a restricted prior, only its relevant support matters; global constancy over impossible target states is unnecessary.

**Bare deletion.** Q=p_b holds exactly when J_ya is a positive constant on the support of p_b. Conditional irrelevance of Y after the audit alone does not establish this: A may remain informative.

**Divide then sequential audit.** Under positive L_y, S=Q holds exactly when L_y is constant on the support of N(p_b K_a). This is the ordinary normalized-likelihood cancellation criterion. It is generally unrelated to whether Y becomes uninformative after the audit. A sequential audit likelihood is not a freestanding replacement for the deleted report likelihood.

These are exact finite algebraic conditions, not empirical tests that establish a source's reliability. A fitted or assumed conditional-independence flag requires justification outside the theorem.

## 4 Positive revision without erasing the observation

The safe operation can use either factorization:

    Sequential:  Q = N(q_old P(a | Θ,b,y)).

    Audit first: r = P(Θ | b,a),
                 Q = N(r P(y | Θ,b,a)).

With a strictly positive old L_y and unchanged baseline p_b, an explicit replacement is

    Q = N((q_old / L_y) M_a L_y|a).

The old likelihood is removed as a calculation step, then the full new joint factor is supplied. Deleting the old factor alone is not the complete operation. When the revised report likelihood is constant on r's support, it cancels and audit-aware deletion is correct by Proposition 1.

This contract also distinguishes learning within a model from changing a misspecified model. If q_old was computed using a provisional likelihood L_old that was not the marginal of the now-adopted joint law, ordinary Bayesian conditioning from q_old need not give the newly adopted posterior. When the baseline remains valid and L_old>0, one can recompute N((q_old/L_old) J_new). If the prior, background likelihood, target meaning, or dependency model also changes, reconstruct from those revised premises. The new model needs its own grounds; the division does not justify it.

With old zeros, inverse-factor reconstruction is not defined on lost coordinates. Under one coherent joint law, later positive-probability conditioning cannot resurrect a state already impossible under the observed old history. A genuinely new model may allow such a state, but the old posterior alone cannot recover the needed prior mass. Store or otherwise retain the valid base model when such revisions are admitted.

## 5 Finite counterexamples and a positive control

### The strongest rival fails through audit selection

Let Θ be uniform on {0,1}. Let T independently be Good or Bad with probability 1/2 each. Given (Θ,T), generate a report Y and a verifier V independently:

    P(Y=Θ | Good)=9/10,
    P(Y=Θ | Bad)=1/2,
    P(V=Θ)=4/5.

Put D=1 exactly when V differs from Y. The audit reveals A=(T,D). In this synthetic experiment the status observation is exact; the verifier is explicitly fallible. This is not an assertion that real audits have either property.

Before the audit, Y=1 has likelihood 7/10 under Θ=1 and 3/10 under Θ=0, hence q_old(1)=7/10. Now observe A=(Bad,1).

For Θ=1:

    P(Y=1,Bad,D=1 | Θ=1) = (1/2)(1/2)(1/5) = 1/20.

For Θ=0:

    P(Y=1,Bad,D=1 | Θ=0) = (1/2)(1/2)(4/5) = 1/5.

Therefore Q(1)=(1/20)/(1/20+1/5)=1/5.

The audit alone has likelihood P(Bad,D=1 | Θ)=1/4 under either target state, so audit-aware deletion gives R(1)=1/2. This is not the weak mistake of forgetting that the audit has an informative marginal: its marginal really is neutral. The missing information is the relation between the known report and audit. Knowing Y=1 and D=1 reconstructs V=0. The now-discredited report is useful as a record of what was checked, without being endorsed as true testimony.

The exact replacement makes that dependence explicit:

    P(Y=1 | Θ=1,Bad,D=1)=1/5,
    P(Y=1 | Θ=0,Bad,D=1)=4/5.

The report was independent of Θ given Bad before the selector was observed, but is not independent after Bad and D are fixed. Conditional independence need not survive additional conditioning.

The valid sequential audit factors are

    P(Bad,D=1 | Θ=1,Y=1)=1/14,
    P(Bad,D=1 | Θ=0,Y=1)=2/3.

Updating q_old by these factors gives 1/5. Dividing out the old Y factor first and then multiplying these same sequential factors instead gives S(1)=3/31. Thus adding a conditionally correct audit factor does not rescue inverse-factor deletion when its conditioning context has been altered.

### An informative audit with a genuinely deletable report

This control was supplied by the parent and checked by the same joint-table engine. Let P(Bad | Θ=1)=3/4 and P(Bad | Θ=0)=1/4. A Good source reports Θ with accuracy 3/4; a Bad source is a fair coin. Observe Y=1 and then only the exact status Bad.

    P(Y=1 | Θ=1)=9/16,
    P(Y=1 | Θ=0)=5/16,
    q_old(1)=9/14,
    P(Θ=1 | Y=1,Bad)=P(Θ=1 | Bad)=3/4.

Deleting Y while retaining the audit is correct because the report is conditionally neutral. Bare deletion gives 1/2 and fails because status is informative. The predecessor review already contains the general neutral-report/informative-selector mechanism; this control illustrates Proposition 1 rather than claiming novelty for that mechanism.

### A positive deletion control

Return to the independent-status model of the first example, but let the audit reveal only Bad, with no D or other selective observation. Then

    P(Θ=1 | Y=1,Bad)=P(Θ=1 | Bad)=1/2.

Both report screening-off and audit neutrality hold, so bare deletion happens to be exact. This control shows that deletion is sometimes warranted by the stipulated channel; the result is not a blanket prohibition.

## 6 Shared calibration changes surviving reports too

Let Θ and T again be independent and uniform. Two distinct reports Y1,Y2 are independent conditional on (Θ,T), each accurate 9/10 for Good and 1/2 for Bad. The reports are not independent conditional on Θ alone because they share the unobserved T.

After Y1=Y2=1, the correct joint posterior is

    P(Θ=1 | Y1=1,Y2=1)=53/66.

An audit that reveals Bad changes it to 1/2. Merely deleting Y1 and retaining Y2's old marginal likelihood gives 7/10, which is wrong. Even beginning with a correctly factored chain likelihood does not save a local deletion rule that freezes the surviving old marginal.

The full audit-aware rule with B=Y2 remains valid: it computes P(Θ | Y2,Bad)=1/2, then checks whether Y1 supplies residual information. Here Y1 is neutral. Thus “no shared-calibration effect” is not an extra condition on Proposition 1; it is a required premise only for the narrower implementation that keeps every other old likelihood factor unchanged. A source-wide audit can revise a shared bridge used by multiple retained records.

### A currently neutral report can be needed for a future audit

The parent derived a further exact consequence of the main example, recorded in the companion TRIPLE_INTERACTION.md and its separate rational control. Condition on known Bad, and let the verifier accuracy be α in (0,1). Then Θ and Y are independent fair bits; D records whether the verifier disagreed with Y. Put ρ=2α−1. The joint law is

    P(Θ=t,Y=y,D=d) = [1+ρ(−1)^(t+y+d)]/8.

Every one-variable and two-variable marginal is uniform. The triple signed moment is E[(−1)^Θ(−1)^Y(−1)^D]=ρ, and

    P(Θ=1 | Y=y,D=d) = [1−ρ(−1)^(y+d)]/2.

Thus neither Y alone nor D alone changes the target posterior, while their joint observation does when ρ≠0. For ρ≠0 their relation also distinguishes this joint law from the fully independent law despite identical pair marginals; at α=1/2, ρ=0 and the full law itself is independent. The three-index array is an ordinary tensor with separately typed target, report, and audit slots. Marginalization contracts a slot against its all-ones covector, which erases the signed triple component. Contracting all three slots against their sign covectors recovers ρ. No symmetric-power identification of those roles, tensor-rank claim, metric, or gradient follows.

Before the audit, Y=0 and Y=1 have the same current posterior 1/2. After the same admitted future audit value d they require different target posteriors whenever ρ≠0. A state that forgot the report because its current likelihood was constant cannot implement that continuation exactly. This does not contradict the prior informative-root quotient: its action alphabet was fixed-factor activation, deactivation, and merge. It did not include new joint audit observations whose likelihood depends on the earlier report.

The squared-probability regret of deleting Y is ρ²/4 at every outcome, hence also in expectation; α=4/5 gives 9/100. The old parity and continuation mechanisms are inherited. The useful operation-level bridge is identifying a concrete audit channel in which a previously neutral source record becomes necessary for the allowed next update. It does not require retaining every conceivable history or establish an actual cognitive memory lower bound.

## 7 Proper-score cost of unsupported deletion

Let F be strictly convex, differentiable on the simplex interior and finite on the vertices, with the usual boundary extensions when used. Define loss at target θ as ℓ_F(s,θ)=D_F(e_θ,s). For distributions r,s, let R_F(r,s) be its expectation under r and H_F(r)=R_F(r,r). The inherited proper-score identity is

    R_F(r,s)=H_F(r)+D_F(r,s).

Assume the forecasts used here are in the score's admissible domain. If Q=P(Θ | B,Y,A) and R=P(Θ | B,A), then

    E[ℓ_F(R,Θ)−ℓ_F(Q,Θ)] = E[D_F(Q,R)] ≥ 0.

Because R=E[Q | B,A], the right side also equals E[F(Q)−F(R)]. Under strict convexity it vanishes exactly when Q=R almost surely. For F(q)=Σθ qθ log qθ it is the conditional mutual information I(Θ;Y | B,A). These are classical conditional Jensen/proper-score identities, supplied in this audit setting by the parent, not new information theory.

For the main selected-Bad event, use F(q)=||q||²/2. On a binary target the regret is the square of the difference in probabilities for Θ=1. Full Q=1/5 versus deletion R=1/2 gives conditional excess expected loss

    (1/5−1/2)²=9/100.

To separate learning from implementation, fix the actually observed old history h=(b,y). Let q_old=P(Θ | h), m_a=P(a | h), and let a revision implementation issue s_a. Then

    H_F(q_old)−Σa m_a R_F(Q_a,s_a)
      = Σa m_a D_F(Q_a,q_old) − Σa m_a D_F(Q_a,s_a).

The first term is information gained by the audit under the declared model. The second is regret from implementing the audit incorrectly. In particular, reducing confidence after an audit is not automatically an expected-score loss; the appropriate comparator is its full posterior.

An intentionally strong hybrid rival uses the exact full posterior on Good branches and deletes Y only on Bad branches, retaining the audit. Conditional on Y=1 in the main model, exact enumeration gives:

    audit information = 4453/48100,
    deletion regret = 9/200,
    net gain over the old forecast = 4577/96200.

The hybrid still improves overall expected score, yet is not the correct posterior implementation. Positive total gain therefore cannot certify every update step. Conversely, neither regret nor information in this synthetic law establishes an actual person's proper function, uptake, knowledge, or warrant.

## 8 A zero probability audit requires model revision

Deep AX already excludes conditioning on an outcome impossible under the entire candidate model. The positive accepted-factor store further excludes zero factors because it requires division. These restrictions have different scopes and should not be conflated.

Suppose an unchanged source model says that a particular certified failure A=1 is impossible. Observing such an event cannot be handled by ordinary conditioning in that model: its denominator is zero. Declaring a very small fallibility probability does not select a unique revised posterior.

### Proposition 2 Arbitrary limiting audit posterior

Fix a finite full-support target distribution p on at least two target states. Let P0(θ,A=0)=p(θ) and P0(θ,A=1)=0. For any desired target distribution q, choose ε>0 small enough that εq(θ)≤p(θ) for every θ, and define

    Pε(θ,A=1)=εq(θ),
    Pε(θ,A=0)=p(θ)−εq(θ).

Then Pε has the same target prior p, Pε(A=1)=ε, total variation distance TV(Pε,P0)=ε, and

    Pε(Θ | A=1)=q.

**Proof.** The entries are nonnegative and sum to one. Summing over A restores p. The A=1 mass is ε, so its normalized target distribution is q. The absolute mass changes on A=1 and A=0 each sum to ε, giving total variation ε. ∎

For any distinct q and q′, their corresponding model sequences converge to the very same P0 while retaining different audit-conditioned posteriors. Thus small total-variation regularization alone does not determine an answer. This parent-supplied finite construction is an elementary null-event conditioning discontinuity, not a new general probability result.

This boundary does not refute any earned claim of exceptionless veracity. It says that a fallibility likelihood model cannot be silently substituted for that claim, and that a purported counterinstance must be authenticated and interpreted before it creates the stipulated inconsistent evidence/model situation. The theorem concerns what follows after a null event is posited within a probability model, not whether a real source has failed.

## 9 Operational and epistemic distinctions

- **Authority or permission removal:** changes a status governing permitted use. A deterministic administrative intervention adds no target information by itself. An observed authority decision may be evidential if its actual decision mechanism is informative; then model that observation as A. Neither case erases observed Y.
- **Report invalidation:** specify what was learned. “Generated by a fair randomizer,” “wrongly attributed,” “inference invalid,” and “content demonstrably false” are different events with different likelihoods. A known adversarial binary reporter with accuracy 1/10 gives posterior 1/10 after Y=1, not 1/2. A correctly established false binary report Y=1 gives target Θ=0 in the stipulated model. Defect is not automatically neutrality.
- **Loss of access:** an artifact becomes unavailable. If Y remains in the subject's recorded history and access loss is conditionally uninformative, the posterior is unchanged. If actual memory is coarsened to M, the relevant forecast is P(Θ | M,A), a different information problem. This does not establish that any human has forgotten or retained a ground.
- **Conditioning on a new audit:** appends the observed audit event to the history under a justified joint channel. It can revise the relevance of old observations, including through selection and shared latent calibration, without pretending the old observations never occurred.
- **Model correction:** replaces unsupported modelling premises rather than conditioning within an unchanged law. Retain the model/version and indicate which base, likelihood, support, or semantic premises changed. The old posterior alone may not support recovery.

These distinctions inherit the prior withdrawal report's source-sensitive warning: removing a defective retrospective explanation need not remove an earlier genuine acquisition route, and loss of one available artifact does not establish loss of knowledge. The present models do not authenticate any actual acquisition or basing episode and do not supply a numerical warrant threshold.

## 10 A concrete implementation contract

1. Keep the target/version, observed report record, retained background, source/provenance dependencies, and audit observation separate from the current use/permission status.
2. Establish what the audit actually says and how it was selected or generated. Include report-dependent selection, shared calibration, and any verifier content needed by the joint law. Do not assume record identities imply probabilistic independence.
3. Check that the observed full history has positive probability under the adopted model. If it is impossible, report model/evidence incompatibility; do not divide zero or pick an arbitrary regularization as if uniquely mandated.
4. Recompute the full joint posterior, or update by the audit likelihood conditioned on the complete earlier history. An audit-first factorization must use the report likelihood conditioned on that audit.
5. Omit a report from the posterior computation only after establishing the eventwise conditional-neutrality condition, or explicitly label the resulting distribution as the chosen coarsened-information forecast rather than the full-history posterior.
6. If implementing inverse-factor replacement, verify positivity and that the baseline and other likelihood factors remain valid. A shared reliability revision may require recomputing a block of factors.
7. Track forecast regret against the full posterior under the justified model. Keep this evaluation separate from actual source authority, human uptake, correct basing, and current warrant.

This need not require storing an unlimited transcript. Any summary that preserves the needed full-history posterior, audit likelihoods, model/version, and admitted future revision behavior can suffice. No universal minimal-memory theorem is claimed for arbitrary future audit channels.

## 11 Verification and limits

Run python3 verify.py from this directory. It uses only Python's standard library and exact fractions. CONTROL_RESULTS.json records the output.

- The main selected-Bad, parent audit-only, positive deletion, independent administrative event, adversarial report, certified false report, shared-calibration, and proper-score controls pass.
- Exhaustive controls cover all 6,400 two-target, two-report, two-audit table specifications whose four entries in each target row are nonnegative integers 0,1,2, not all zero, normalized within the row. The 80 raw row specifications represent 65 distinct row distributions, hence 4,225 unique normalized channels. Across three full-support priors there are 68,688 positive event/prior cases, including 33,696 with a relevant zero likelihood. Each checks the deletion iff criterion and audit-first replacement. The 58,320 cases permitting inverse factors additionally check sequential updating, audit-aware factor deletion, and the divide-then-conditional-audit criterion.
- Twelve exact three-target perturbation controls preserve the prior, realize several distinct desired audit posteriors, and check total-variation distance equals ε. The universal null-audit conclusion rests on the written proof, not twelve tests.
- All eight initially bound local inputs are rehashed by verify.py to check that this investigation did not alter them. Deep AX's Git blob identity was independently matched before authoring.

These are written proofs with author-run exact finite controls. They are not proof-assistant/kernel certification, empirical source calibration, a psychological model, an actual-warrant verdict, protected integration, or T20 closure. Separate review status, if later supplied, must identify the exact reviewed snapshot.

Attribution: the parent supplied the informative status-only example, the conditional coarsening regret observation, the null-audit perturbation construction, and the triple-interaction continuation specialization. This worker supplied the report-dependent audit selection counterexample, the comparison of the two strongest deletion implementations, support-explicit revision exposition, shared-calibration control, exact enumeration, and source/coverage comparison. The independent reviewer identified the duplicate normalized-row counting clarification before this snapshot was frozen. All general probability, parity, continuation, and scoring mechanisms have classical ancestry.
