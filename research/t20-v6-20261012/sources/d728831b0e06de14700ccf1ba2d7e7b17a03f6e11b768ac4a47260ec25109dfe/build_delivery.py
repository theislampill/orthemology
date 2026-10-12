from __future__ import annotations
import csv,hashlib,html,json,re,shutil,subprocess,sys,zipfile
from pathlib import Path
R=Path('private-locator:1a21b068f7983766df37');P=R/'package'
for d in ('research','audits','verification','ledgers','sources','extracted'): (P/d).mkdir(parents=True,exist_ok=True)
def load(name,default):
 try:return json.loads((P/name).read_text())
 except Exception:return default
# Refuse to let Python optimisation turn the checks into no-ops.
v=P/'verification/verify_synthesis.py'
if v.exists():
 s=v.read_text()
 if 'Optimised Python disables this verifier' not in s:
  s=s.replace("if __name__=='__main__':\n", "if __name__=='__main__':\n    if not __debug__:raise RuntimeError('Optimised Python disables this verifier; use ordinary Python.')\n")
  v.write_text(s)
 try:
  proc=subprocess.run([sys.executable,str(v)],capture_output=True,text=True,timeout=160)
  (P/'verification/execution_stdout.txt').write_text(proc.stdout);(P/'verification/execution_stderr.txt').write_text(proc.stderr)
 except Exception as e:(P/'verification/execution_error.txt').write_text(repr(e))
coverage=load('ledgers/coverage.json',{'inventory_files':'NOT_ESTABLISHED','text_or_pdf_extraction_lines':'NOT_ESTABLISHED'})
github=load('ledgers/github_scope.json',{'complete_tree_acquired':False,'current_pin_verified':False})
results=load('verification/results.json',{'status':'NOT_ESTABLISHED'})
report=r'''# Orthemology: evidence-limited composition, equilibrium, and continuation
## Staged consolidation and research packet — 12 September 2026

**Disposition: PARTIAL — NOT APPROVED AS THE REQUESTED EXHAUSTIVE CONSOLIDATION.**

This packet preserves work that can be used in the next pass. It does not certify that every line of the repository and every attachment has received a fresh semantic and adversarial reading. Acquisition, extraction, duplicate detection, and test execution are distinguished from that reading. The requested completion gate remains open. This is not a declaration of a meniscus break, a repository amendment, a peer-reviewed result, or independent verification.

The report has two substantive purposes. First, it consolidates the load-bearing distinctions supported by the source passages already available in the conversation. Second, it develops a conditional, executable route from incomplete information about a finite game to a warranted equilibrium certificate, with explicit results about evidence cost, destructive inquiry, convergence, and probabilistic concentration. These developments are new to this delivery; whether the ZIP frontiers or other repository files already contain equivalent results remains a source-review obligation.

The collection scripts do not execute repository code or modify GitHub. Raw source material is not trusted as an instruction stream. Font files are not distributed. Source omissions, download errors, excluded members, and incomplete discussions are recorded rather than silently converted into empty results.

## 1. What this delivery establishes, and what it does not

The achieved mathematical contribution is an integrated specification and proof package for **evidence-limited equilibrium synthesis**. An agent need not identify every detail of a reference game before acting. It needs evidence sufficient to select a candidate that is acceptable in every reference situation still compatible with its information. This moves beyond the unqualified sentence “an equilibrium exists” without assuming that the correct equilibrium is already observable, reachable, or naturally selected.

Four results organise that contribution:

1. Unilateral incentive differences, rather than absolute payoff levels, can be the right observables for equilibrium preservation.
2. A finite library of candidate profiles turns warranted equilibrium selection into a relation-valued adaptive inquiry problem. For strictly positive approximation tolerance, an explicit rational grid can make the candidate library complete under bounded-payoff assumptions.
3. When inquiry changes the observation machinery or the world, labelled beliefs preserve the original target and distinguish genuine access improvement from destructive loss.
4. Exact potential alignment supports conditional results about finite improvement paths and logit concentration. Neither result establishes a physical principle-of-least-action explanation, and neither identifies a correlated distribution of visited states with independent mixed-strategy play.

The packet does **not** establish that the complete source corpus has been read, that all source claims have been adjudicated, that the physical-to-agent bridge has been instantiated, or that this formulation outperforms a strong conventional decision-theoretic and game-theoretic baseline. Those are different targets. The audits retain them as open findings.

### Evidence classes used here

**Source-supported:** a claim is attributed to an identified source passage or section already available in the conversation. This is not a new complete-document review.

**Derived:** an argument in this report follows from expressly stated mathematical hypotheses. Its application to a real process is a separate matter.

**Executed finite check:** a computation is reported only through the accompanying execution receipt, with its scope. A passing example is not a proof of all cases.

**Proposed:** a modelling choice, research construction, test design, or project direction is offered for review. It is not treated as adopted repository doctrine.

**Open:** missing evidence, incomplete review, an unproved premise, or an unperformed comparison remains unresolved. Labelling a finding does not resolve it.

## 2. Corpus, version, and coverage boundaries

The requested attachment set comprises the Last Moat third edition; the Orthing graded formalisation; the continuation frontier ZIP; the modal/metaphysical frontier ZIP; Information, Composition, and Self-Revision v5; and The Cost of a Decisive Revision. The earlier conversation image is included in the acquisition inventory when present.

The repository named in the conversation is `theislampill/orthemology`. The previously observed revision was `f50dc1aee52356cc6adbef342387576b02afc124`. The acquisition ledger records whether a current branch read succeeded, which revision was actually acquired, and whether a historical fallback was used. A fallback is not called current. A downloaded tree is not called a review of its commit history, issue comments, or pull-request deliberations.

Exact byte duplicates are retained as distinct provenance entries. They can reduce repeated mechanical work, but do not erase differences in context, authority, or version. PDF text extraction can scramble mathematical symbols, reading order, and tables. A successful extraction does not discharge page-image inspection where the semantics depend on those features.

The queue in `ledgers/semantic_review_queue.jsonl` gives contiguous source ranges. Its pending status is deliberate. A future reviewer must provide a substantive receipt for each range; opening a file, counting its lines, searching keywords, or generating this queue is not such a receipt. Original textual line numbers and extracted PDF line numbers are different coordinate systems. Page markers are retained in extracted PDFs so that ambiguities can be checked visually.

The prior assistant's assertion that both ZIPs had been completely unpacked and examined is not accepted as a coverage certificate. Nor is a failed keyword search evidence that an idea does not occur under another formulation. The canonical status and exact intended meniscus criteria must be recovered from the actual project instructions and their amendment history before an overall success verdict is issued.

## 3. The common problem across the sources

The corpus repeatedly separates a representation of a system from the system, a possible construction from an actual construction, and a favourable result from the evidence needed to warrant that result. This is not merely terminological caution. Each separation changes the admissible inference or computation.

The graded formalisation distinguishes an orthing process type, a concrete episode, its finite record, and an analysis-declared representation. An episode is not made into a tensor merely by choosing tensor coordinates. Typed tensor structure becomes substantively useful when an operation respects it: mixed-payoff expectation, marginalisation, a justified contraction, or an equivariant update. [F1 §§2–6, 11]

Information, Composition, and Self-Revision asks when local records determine a property of the realised joint system. Exact local projections can be compatible with several global compositions. Joining the records yields the largest compatible relation, not proof that the actual coupling is that relation. A joint invariant can require information absent from every proper local marginal. [F2 §§1–3]

The Cost of a Decisive Revision separates identifiability from affordability. Even when available observations could decide a question, the required observation tree can exceed the budget. Conversely, a retained record can eliminate further observation costs for a particular question without being universally sufficient for every later question. [F3 §§1–3]

The Last Moat separates a behavioural contract, physical realisations of that contract, an adequate export of current state, and an actual maintained continuation. Two correct machines and a correct bit channel do not necessarily preserve the current execution. Joint interfaces, support, input ordering, progress, and state distinctions matter. [F4 §§6, 12–18]

The recurring mathematical form is therefore:

```
world/process -> available record -> permissible inference or intervention
                       |
                       +-> what distinctions remain unresolved?
                       +-> what additional action could resolve them?
                       +-> what must survive that action?
```

This diagram is a synthesis of the inspected passages, not a universal ontology. It does not imply that every problem is finite, fully observable, a game, or a tensor computation.

## 4. A consolidated set of distinctions

### 4.1 Type, token, record, and representation

An operational type, an occurrence of that type, a record of the occurrence, and a representation of the record can have different identity and equality conditions. An injective record encoding preserves the chosen record; it does not establish the truth of its claims or the completeness of its observation of the world. A degree-one free-basis encoding can retain a very large record, so tensor degree is not an intrinsic measure of organisational complexity. [F1 §§2–4]

### 4.2 Inference, authority, and actual outcome

A technically valid prediction is not permission to act. Permission to conduct an experiment is not admission of the candidate produced by the experiment. A well-formed receipt is not evidence that its asserted measurement actually occurred. Correctness of a result and adequacy of the route to it remain separately assessable. [F1 §§6, 9; F2 §5.5; F3 §§1, 3]

### 4.3 Local descriptions and realised composition

Local compatibility does not select the actual global relation. If the joint relation is K and the natural join of its retained local projections is J, then K is contained in J. A predicate true throughout K but not throughout J is not determined by that local baseline. This can reflect a genuine interaction restriction without establishing metaphysical irreducibility from a complete microdescription. [F2 §§1–3, 6]

### 4.4 Actual feasibility and estimated feasibility

Defining a landscape by a feasibility predicate does not provide an algorithm that knows the actual feasible landscape. A bounded interpreter can have an incomplete or mistaken estimate. More observations may revise that estimate without changing physical feasibility; constructing an interface may instead change what is reachable. These must not be counted as the same kind of progress. [F1 §7; F4 §§17–18]

### 4.5 Existence, warranted selection, reachability, and maintenance

An acceptable state can exist but remain unidentified. It can be identified but unreachable with the available actions. It can be reached but not maintained. It can be maintained safely while making no required progress. Each transition between these claims needs a distinct premise or witness. [F1 §§8–11; F4 §§14, 18]

### 4.6 Stable objectives and changing purposes

Locally justified improvements can cycle if the objective changes between steps. There is no contradiction in every step improving its predecessor's objective while the joint state of objective and artefact returns to its starting point. A common well-founded progress relation, or a suitable invariant objective for the declared transition system, must do additional work. [F3 §3]

### 4.7 Independent mixed play and distributions over visited states

The probability tensor of independent mixed strategies factors into the players' marginal distributions. A distribution over joint schedules need not factor. Shared randomisation, communication, correlated observations, and the stationary distribution of a learning process can produce non-product laws. None may be substituted for independent mixed Nash play without checking the relevant incentive conditions. [F1 §8.2; F2 §3]

## 5. Correcting the morning-game formulation

The conversation's morning example requires more than labels such as “bathroom first.” Distinct actions include food preparation, drink preparation, showering, toothbrush preparation, eating, drinking, and toothbrush use. Combining food and drink into a single task is an explicit simplification, not the unique correct model. Whether one person can prepare something for the other, whether a kettle runs unattended, and whether brushing and showering can share a bathroom all change the feasible policies.

For a fixed finite horizon and time resolution, a pure strategy can be a complete contingent plan: what to attempt after each permitted observation history. A mixed strategy is a probability distribution over such plans. Randomisation at information sets is a behavioural strategy; its relationship to mixed normal-form plans requires the relevant information structure, rather than an automatic identification.

Preparation precedes the corresponding consumption or use. Shared resources couple the two people's feasible actions. One cannot generally obtain the legal joint space by independently filtering each person's schedules and taking a Cartesian product. The formalisation gives exactly this obstruction: individually available uses of an exclusive resource can jointly violate its capacity. [F1 §8.3]

A conventional finite-game construction is possible when a declared resource protocol makes every joint strategic profile well-defined. For example, both may request the shower, and a queue rule determines which request is served first and what waiting cost occurs. The request profile is admissible; simultaneous exclusive use is not. A large finite penalty assigned to impossible simultaneous use is not an implementation of the queue.

Once the players, strategies, protocol, and payoffs are specified, the finite-game Nash theorem applies. It guarantees an equilibrium in mixed-strategy space, which includes pure strategies as point distributions. It does not guarantee a nondegenerate mixture, a unique equilibrium, or actual convergence of the couple's learning process. [F1 §§8.1–8.4]

The illustrative thirty-ordering count in the conversation concerned only five tasks and two precedence constraints. It was not an enumeration of the full morning policy space, a capacity-aware joint schedule space, or the normal form of the information-sensitive interaction. The numerical mixtures were examples of distributions, not solved equilibria.

## 6. Mathematical setting for the proposed development

Fix a finite nonempty set W of possible reference situations. The actual reference situation is assumed to be one member of W. In each w, a declared finite game G_w has the same nonempty strategy sets S_i and a real payoff U_i^w on every joint pure profile. The common strategy labels have fixed meanings. A separately specified protocol and feasibility contract resolve resource conflicts. Changing strategy sets or labels requires an additional transport declaration; the following formulas do not silently compare different games' coordinates.

Let p be an independent mixed profile. Define unilateral regret by

```
R_i^w(p) = max over a_i in S_i of
           E[U_i^w(a_i, s_-i)] - E[U_i^w(s_i, s_-i)].
```

Both expectations use the appropriate marginal product distributions. This quantity is nonnegative. The profile is a Nash equilibrium exactly when every regret is zero, and an epsilon-equilibrium when every regret is at most epsilon. Pure deviations suffice because the payoff of a mixed deviation is a convex combination of its pure-deviation payoffs. [F1 §8.5]

The inquiry controller does not initially know w. It has a nonempty belief B contained in W and may perform authorised observations. This is an epistemic possibility set, not necessarily a Bayesian posterior. Whether probabilistic uncertainty is additionally modelled must be stated.

Let C be a finite nonempty library of candidate mixed profiles and associated operational certificates. Define the acceptable-candidate relation by

```
Good(w) = { c in C :
            c is feasible under the declared protocol and reference situation w,
            c respects the required operational contract,
            R_i^w(c) <= epsilon for every player i }.
```

This formulation deliberately keeps feasibility and strategic incentives separate. It also makes the scope of a finite library explicit: failure to find a candidate in C does not prove that no acceptable profile exists outside C.

## 7. Result A: preserve unilateral gains, not arbitrary payoff levels

For each player i, own actions a and b, and opponents' pure profile t, define

```
D_i^w(a,b,t) = U_i^w(a,t) - U_i^w(b,t).
```

**Exact preservation statement.** Suppose two reference situations have identical D_i arrays for every player, action pair, and opponents' profile. Then they have identical regret functions on all independent mixed profiles and therefore the same mixed Nash set.

**Proof.** The advantage of the pure deviation a from a mixed profile p is

```
sum over b,t of p_i(b) p_-i(t) D_i^w(a,b,t).
```

Identical gain arrays make every such deviation advantage identical. Taking the maximum over a gives equal regret. The zero sets of all player regrets are consequently equal.

In particular, adding an arbitrary opponents-only term b_i(t) to U_i does not change these differences. Exact raw-payoff reconstruction can therefore demand information irrelevant to the equilibrium question. This does not make every payoff transformation harmless: own-action-dependent changes can alter incentives. Positive rescaling preserves exact best responses but changes the numerical interpretation of a fixed regret tolerance unless the tolerance is transported too.

**Error version.** If corresponding unilateral-gain arrays differ by at most eta_i uniformly, then the players' regret functions differ by at most eta_i uniformly over mixed profiles. Each pure-deviation advantage is a convex average of gain entries, so its discrepancy is at most eta_i; the maximum operation cannot increase that uniform discrepancy.

The source's payoff-error certificate is recovered as a special case: a uniform entrywise payoff error epsilon_i induces a gain error at most 2 epsilon_i. A surrogate delta_i-regret certificate then yields a true regret bound delta_i + 2 epsilon_i. [F1 §8.5]

**Boundary.** Equal gain arrays are sufficient to preserve Nash and necessary to recover those exact arrays from a representation. They are not necessary merely to preserve the equilibrium set. Two different games can have the same Nash set for other reasons. The required observable must be chosen to match the actual claim.

## 8. Result B: equilibrium existence does not ensure a common warranted choice

Define the candidates warranted at a nonempty belief B by

```
Common(B) = intersection over w in B of Good(w).
```

A controller may immediately return c exactly when c belongs to Common(B). This is a relation-valued certificate, not necessarily identification of w or a uniquely determined answer.

**Counterexample.** There are two players and two actions, 0 and 1. A hidden mode theta is either 0 or 1. In game theta, each player's payoff is one when their own action equals theta and zero otherwise. Each game has a unique Nash profile: (0,0) in mode 0, and (1,1) in mode 1. A blind record that is identical in both modes does not warrant either exact equilibrium.

This is not a failure of Nash existence. Each game has an equilibrium, but the intersection of their equilibrium sets is empty. The quantifiers differ:

```
for every compatible game, there exists an equilibrium
```

does not imply

```
there exists one profile that is an equilibrium in every compatible game.
```

For a player who chooses action 0 with probability p, the regrets in the two modes are 1-p and p. The smallest worst-mode regret is therefore 1/2, attained at p=1/2. Applying this to both players gives an exact blind minimax bound: no common profile has uniform regret below 1/2. An accurate one-bit observation of theta permits zero regret.

Conversely, several different games can share an acceptable candidate. In that case no additional observation is needed for that decision, even if much of the game's payoff tensor remains unknown. This is why “identify the whole game first” is unnecessarily strong in general.

## 9. Result C: a finite candidate library for positive tolerance

A finite library may miss an exact mixed equilibrium whose coordinates do not belong to the library. This cannot be repaired merely by invoking finite-game existence. A positive approximation tolerance permits a constructive alternative.

Assume every pure payoff in every compatible game has absolute value at most M. If two mixed profiles p and q satisfy the per-player bounds

```
||p_i - q_i||_1 <= delta_i,
```

then

```
R_i(q) <= R_i(p) + M delta_i + 2 M sum_{j != i} delta_j.
```

**Proof.** Telescope the difference between the two product distributions one factor at a time. Their l1 distance is at most the sum of the marginal l1 distances. A payoff bounded in absolute value by M therefore changes in expectation by at most M times that sum. For a fixed unilateral deviation, only opponents' distributions vary; its payoff changes by at most M times the opponents' sum. The baseline payoff changes by at most M times the full sum. Subtract, then maximise over deviations.

For a player with m_i actions, choose a positive integer denominator k. Round down the first m_i-1 probabilities to multiples of 1/k and place the remaining mass on the final action. The resulting probability vector is valid and has l1 error less than or equal to 2(m_i-1)/k. Consequently, a sufficient common denominator for approximating every exact equilibrium within regret tolerance epsilon>0 is

```
k >= (4 M / epsilon) sum_i (m_i - 1).
```

The resulting rational grid is finite. Combined with finite-game existence, it supplies at least one epsilon-equilibrium candidate for every compatible bounded-payoff game on the fixed strategy product. It can be extremely large; this is a completeness construction, not an efficiency claim. The case M=0 is trivial. Empty strategy sets and undefined joint payoffs remain excluded.

This result closes a specific logical gap in the relation-valued inquiry construction: for positive epsilon and the stated uniform bound, the candidate library need not be an arbitrary guess. It still does not imply that one candidate works across every currently indistinguishable game, or that its operational feasibility is uniform across worlds. Those conditions remain separate.

## 10. Result D: the minimum evidence cost of warranted equilibrium selection

First consider nondestructive exact observations. Each available probe h has a fixed positive cost c_h and a known deterministic response h(w). Probes remain available, do not change w, and have the same meanings during the decision. The probe models themselves are premises, not free empirical discoveries.

For a nonempty belief B, define

```
V(B) = 0, if Common(B) is nonempty;

V(B) = min over h that split B of
       [ c_h + max over observed y in h(B) of V(B intersect h^{-1}(y)) ],
       otherwise.
```

An empty minimum is infinity. Empty beliefs are inconsistencies, not certificates. An informative probe produces proper sub-beliefs, so the recursion is well-founded on finite B.

**Theorem.** V(B) is the minimum worst-case total probe cost of a deterministic, uniformly sound controller that returns an acceptable candidate on every reference situation in B. Infinity means that no such controller exists in the declared probe-and-candidate model.

**Lower-bound proof.** If no candidate is common, a sound controller cannot stop. Its first useful probe splits B. On each possible answer it must solve the corresponding residual problem; that continuation costs at least the recursively defined value. Its worst-case total cost is therefore at least the displayed expression for its first probe, and hence at least the minimum.

**Attainment proof.** If Common(B) is nonempty, return any member. Otherwise choose a minimising probe when the value is finite and attach recursively optimal controllers on its proper residual beliefs. Induction on belief size proves sound termination and achieves the bound. If every first-probe option has an infinite branch, no uniformly terminating controller exists.

This is a relation-valued extension of the source's Boolean decision-tree argument. It uses established finite decision-tree reasoning; no general historical novelty is claimed. Its project-specific role is to price the evidence required for a strategic certificate while allowing several acceptable outputs and preserving the feasibility contract. [F3 §§1–2]

A retained record r with unchanged meaning selects the initial fibre B_r before additional probe costs are incurred. Before the record value is known, the worst-case additional cost is the maximum of V(B_r) over its nonempty fibres. After its value is known, only that fibre's value matters.

The theorem does not include the computational cost of solving this recursion, constructing the game, verifying the probes, or maintaining the runtime. A budget sufficient for the next probe is not necessarily sufficient for the whole policy. Random, noisy, destructive, or time-varying probes require other models.

## 11. Result E: self-revision can open access or destroy the target

When an action changes the observing method or the environment, the nondestructive recursion is no longer sufficient. A current state may no longer identify the original target. The correct finite model retains pairs

```
(current operative state, original reference situation).
```

A belief contains the pairs still compatible with the observation history. An action updates the current coordinate and leaves the original reference label intact; the resulting observation selects a successor belief. For a retrospective decision, terminal beliefs are those for which one candidate is acceptable for every retained original situation. For a candidate that will actually be executed, strengthen the terminal predicate to `Accept(current_state, original_situation, candidate)`: it must preserve the original strategic target while also satisfying current feasibility and the current operational contract in every retained pair. An experiment that consumes a required resource must not leave a stale initial-feasibility certificate in force. This is the relation-valued counterpart of the labelled-belief construction in the self-revision source. [F2 §5.3]

Let W0 be the set of terminal beliefs. Repeatedly add any belief for which there is a legal action whose every possible observation successor has already been added. The union is the sure finite-termination region in the stipulated finite deterministic, exact-observation model.

**Sufficiency.** At a positive-rank belief, choose an action whose successors have smaller rank. The rank strictly decreases until a terminal belief is reached.

**Necessity.** A sound controller terminating for every possibility in a finite belief has a finite maximum run length. At length zero it must be terminal. Induction on that maximum length places each predecessor in the backward-reachable region.

Legal action means legal in every remaining possibility unless the model explicitly represents an observable refusal. An unavailable or prohibited experiment cannot be introduced as a free branch. Infinite state, stochastic observation, unmodelled drift, and changing meanings are outside this result.

The source's reconnection example shows a positive case: a method with only local parity-blind records can connect to an accurate joint observation and then decide. The actual observation supplies the distinction. Reconnecting does not create information by self-endorsement. [F2 §5.2]

Its destructive-experiment example shows the opposite. Three initially indistinguishable situations are pairwise distinguishable by some experiment, but either possible first experiment can irreversibly merge two situations requiring opposite original answers. No uniform decision policy exists. Pairwise separability is not a substitute for a safe sequential strategy. [F2 §5.3]

Applied to the morning problem, an experiment can change more than knowledge: using all the hot water, consuming a shared ingredient, or making someone late can alter the problem being evaluated. A repeated-morning experiment may instead treat the next day as a new reference episode under a stable distribution. Either choice needs an explicit model. A post-intervention payoff cannot automatically be treated as a measurement of an unchanged counterfactual game.

## 12. Result F: certified improvements in a fixed potential game

Now suppose the true game is fixed, its joint pure-profile set is finite, and it has an ordinal improvement potential: every strictly profitable unilateral change strictly decreases a real-valued function C on that finite profile set. This is a substantive alignment assumption, not a consequence of general friendliness, homogeneous needs, or tensor notation.

Assume changes are accepted one player at a time and only when a valid gain certificate establishes a strictly positive unilateral payoff improvement. Then every accepted change strictly decreases C. No joint profile can recur. There are at most |S|-1 accepted changes.

This finite-move bound alone does not establish that the final state is Nash: a controller might simply stop examining available improvements. Add a progress condition: whenever a strictly improving deviation remains available at a retained profile, the controller eventually evaluates and correctly admits some such deviation. Under this condition, the final retained profile must be a pure Nash equilibrium. Otherwise its profitable deviation would force another accepted change.

One sufficient way to establish the progress condition is fair repeated examination with valid uncertainty intervals whose widths eventually become small enough to distinguish every positive gain at a retained profile. Merely running random experiments for an unspecified duration does not by itself supply that condition. Constant noise or an unaffordable evidence obligation can leave the controller unable to certify an improvement.

This theorem concerns accepted changes and the pure-profile process. A pure Nash profile is a point in mixed-strategy space, but the theorem does not explain convergence to a nondegenerate mixed equilibrium. Nor does it give a finite stopping certificate when the uncertainty intervals can never distinguish a zero gain from an arbitrarily small positive one.

The construction relates to the source's common well-founded order requirement. It makes the joint objective and unilateral update discipline explicit, rather than assuming that separate local improvements necessarily compose. [F3 §3]

## 13. Result G: a precise probabilistic tendency under logit exploration

The user's original claim was a likely tendency under compatible cooperation, stable constraints, perturbation, and payoff evaluation, not an assertion that a Nash fixed point follows deductively from physical least action. A probabilistic model should therefore be stated as such.

Take a finite game on the full strategy product. Suppose a common effective cost C has the exact unilateral-difference property

```
U_i(a_i,s_-i) - U_i(b_i,s_-i)
  = -C(a_i,s_-i) + C(b_i,s_-i).
```

At each update, choose one player using a fixed positive probability. Holding the other players' current actions fixed, choose that player's new action with probability proportional to exp(-beta C), where beta is a finite positive inverse-noise parameter. This rule is random-scan logit updating. Its behavioural mechanism is stipulated, not derived from physiology or microscopic mechanics.

**Theorem.** The distribution over joint pure states

```
pi_beta(s) = exp(-beta C(s)) / sum_t exp(-beta C(t))
```

is stationary. Because every action has positive conditional probability and the full Cartesian profile graph is connected by unilateral changes, the chain is irreducible; its self-transition probabilities make it aperiodic. These are properties of this declared finite update model, not of every constrained resource game.

**Detailed-balance proof.** For two distinct profiles differing only in player i, the probability of selecting i is the same in both directions. The conditional normalisation sums over the same opponent-fixed slice. Multiplying the transition probability by pi_beta gives the same product of the two exponential weights in either direction. Transitions changing more than one coordinate have probability zero both ways. Summing the pairwise balance identities proves stationarity.

Let M0 be the set of global cost minimisers, m its size, and N the number of pure profiles. If there are non-minimisers, let gap be the smallest positive difference between their cost and the minimum. Define

```
r_beta = ((N-m)/m) exp(-beta gap).
```

Then

```
pi_beta(not M0) <= r_beta / (1+r_beta).
```

Every minimiser has the maximum exponential weight. Every other profile has weight at most that maximum times exp(-beta gap). Bound the ratio of outside mass to minimiser mass and convert that ratio into a probability. Since a unilateral improvement would reduce C, every global minimiser is a pure Nash equilibrium. Thus this model supplies a quantitative stationary-probability tendency toward a subset of Nash states as beta grows.

**The qualifications are part of the result.** At fixed finite beta, exploratory moves retain positive probability; the process does not necessarily settle permanently. A limit of stationary distributions as beta grows is not a theorem about an arbitrary cooling schedule over time. The stationary distribution is a law over joint visited states, not generally the product distribution of independently mixed Nash strategies. Its marginals cannot be multiplied without changing the law. This result supplies a conditional probabilistic bridge, not a physical least-action derivation or a universal convergence mechanism.

## 14. A concolic stress case: cooperation is not enough to select the dynamics

Consider two high-level morning plans, 0 and 1, with common cost

```
                 Other: 0   Other: 1
Self: 0              2          0
Self: 1              0          2
```

Interpret different plans as avoiding the shared bottleneck. This is a simplified strategic slice of the workflow, not a replacement for all preparation, consumption, and resource details.

Both off-diagonal profiles are pure Nash equilibria. Independent equal mixing is also a Nash equilibrium: against a half-and-half opponent, both actions have the same expected cost. Nevertheless, the update mechanism changes the trajectory.

With simultaneous best responses, (0,0) changes to (1,1), which changes back to (0,0). Each player chooses a best response to the previous opponent action, but the simultaneous changes recreate the conflict. With asynchronous strict improvement, one player changes first and the system reaches an off-diagonal equilibrium.

Under the usual two-population payoff-replicator equations for the equivalent payoff-one-for-mismatch game, let p and q be the probabilities of action 0:

```
p_dot = p(1-p)(1-2q)
q_dot = q(1-q)(1-2p).
```

The linearisation at (1/2,1/2) is

```
[  0   -1/2 ]
[ -1/2   0  ].
```

Its eigenvalues are +1/2 and -1/2. The mixed equilibrium is a saddle for this stated dynamics: exact symmetric motion can approach it, while an asymmetric perturbation has an unstable direction. A cooperative potential game can therefore favour a pure equilibrium rather than robustly select its interior mixed equilibrium.

For random-scan logit updating with beta=log(2) and the cost table above, the exact stationary probabilities, in order 00,01,10,11, are

```
(1/10, 2/5, 2/5, 1/10).
```

The conflict probability is 1/5. Both stationary marginal distributions are half-and-half, but independently multiplying those marginals would give conflict probability 1/2. This is a concrete witness to the distinction between a distribution over learning states and an independent mixed-strategy profile.

The symbolic case split is now explicit: synchronous versus asynchronous updates; strict improvement versus persistent exploration; common potential versus changing objectives; identified versus unidentified payoffs; product mixtures versus correlated joint laws. The finite verification script instantiates these branches and checks countermodels. This is bounded concrete-and-symbolic analysis, not a claim to have run a general SMT-based concolic engine over the complete repository.

## 15. The variational-to-strategic research obligation

The preceding results locate a possible mathematical route for the conversation's intuition:

```
physically realised constraints and feedback
    -> an effective behavioural cost and observation model
    -> an identified or sufficiently certified reference game
    -> a specified adaptive update mechanism
    -> conditional equilibrium accessibility or concentration.
```

The report supplies parts of the last three arrows in explicitly finite models. It does not supply the first arrow. It also does not replace that arrow with a claim that nature minimises whichever scalar the analyst finds convenient.

A meaningful physical-to-agent bridge would require at least a specified physical process, a projection to the relevant agent state, an account of observations and feasible interventions, an effective cost with interpretable units or comparisons, and a relation between physical/behavioural variations and unilateral payoff differences. It would then need to show that the real update mechanism has the properties used in the convergence or concentration theorem.

An illustrative sufficient alignment condition is equality, or justified positive rescaling, between unilateral payoff changes and negative effective-cost changes. That is an object one can try to measure, model, or falsify. It is not made true by naming the cost an “action.” A cross-level projection can preserve a target's value while failing to preserve its dynamics or the ordering of interventions.

The source's G1/G2 distinction is useful here. Feasibility-first, order-ranked corrective movement is not automatically literal differentiable gradient flow. Even a legitimate dynamical realisation need not be a gradient flow. A state space, metric, potential, vector field, and convergence conditions must be supplied where that stronger interpretation is intended. [F1 §10.2; R2]

This leaves the user's “likely by” proposal in the right category: a substantive explanatory hypothesis with a testable family of intermediate mechanisms. Not having completed that explanatory bridge does not refute the hypothesis. Having supplied the finite-game and learning theorems does not confirm it empirically.

## 16. How the continuation and Last Moat strands constrain the proposal

An equilibrium certificate is a claim about a reference configuration. If the game, resource allocator, timing regime, preferences, or observation semantics changes, the certificate can become stale. The self-revision source's version-bound receipt example gives the relevant pattern: match the receipt to the actual current candidate and perform the guard check at the boundary where the verdict takes effect. A prior matching read does not suffice if relevant state can change before publication. [F2 §5.4]

The Last Moat supplies the operational analogue. A realisation must implement the abstract transition rule and its operative readout; migration must preserve the consequential current state; subsequent execution must remain inside the certified domain. The composition is evaluated at the joint realisation, not by pretending that every constituent separately implements the whole contract. [F4 §§6, 14]

For strategic learning this means that carrying a policy description to another implementation is not enough. The new implementation must preserve the required action meanings, observation interface, update state, randomness contract when relevant, and resource protocol. A saved probability vector without the machinery needed to execute its actions is a stored description, not continued agency.

Likewise, a stable scheduling arrangement may fail a progress requirement. The household could avoid resource conflicts by never entering the bathroom. A viable safe set can contain an idle loop. A progress rank or another liveness condition is needed when the contract requires everyone actually to finish. [F4 §18]

These are constructive restrictions: they tell a candidate implementation what to demonstrate. They are not reasons to discard the strategic pathway or treat every uncompleted certificate as impossibility.

## 17. Consequences for the project trajectory

The strongest defensible direction is to make the source's separate mathematical layers compose at a **specific consequential target**. Merely adding another tensor notation or a catalogue of analogies would not do that. The candidate target in this packet is:

> From incomplete but explicitly modelled evidence about a finite resource-mediated game, determine whether a feasible candidate can be warranted, how much additional observation is needed, which observation actions preserve the original target, and which update mechanisms support the stated stability claim.

This target joins the representation/fibre results, higher-order composition obstructions, inquiry-cost results, strategic regret certificates, and continuation obligations. It also produces concrete negative witnesses rather than an unrestricted optimism or a blanket refusal to connect levels.

The proposed measurable outputs are not “more intelligence” or “more emergence.” They are the rate of false equilibrium certificates, the number and cost of observations, the ability to retain a consequential higher-order distinction, the handling of destructive probes, the validity of evidence after revision, and completion of the declared operational task.

A matched baseline must receive the same information, computational allowance, and available actions. At least one baseline should already use ordinary contracts, belief-state reasoning, finite-game regret checks, and appropriate learning dynamics. Comparing the proposal only with an uninformed scheduler would manufacture an advantage. The Last Moat already warns against treating a weak local-check baseline as the whole of established formal methods. [F4 §12.5]

A genuine project advance could be a stronger bound, a target-preserving reduction with lower total cost, a new independently warranted instance, or a prospectively demonstrated error reduction under the project's own declared gate. The exact meniscus criterion and its authority remain to be recovered from the complete source review. This packet cannot promote its own target into the canonical criterion.

The modal/metaphysical lane remains a separate high-priority review item. An operational quotient, a stable equilibrium, or a physically implemented contract does not alone settle necessary being, substance, essence, consciousness, or causal completeness. Conversely, operational mathematics need not be irrelevant to those questions: a valid bridge would name the modal interpretation, its premises, and the consequence actually preserved. The two frontier archives must be examined in full before their stronger results or limits are reported as adjudicated.

## 18. What the executable checks are designed to cover

The custom verifier uses exact rational arithmetic for finite payoff and transition calculations. It exercises all 256 binary-payoff two-player, two-action games on a declared nine-profile rational grid. That family has an equilibrium on the chosen grid; this bounded fact is not general completeness of a nine-point library.

It compares direct expected-payoff deviations with the regret formula, checks invariance under opponents-only payoff shifts, and tests the uniform two-epsilon payoff-perturbation bound. It compares the relation-valued Bellman calculation against a separate enumeration of two-level concrete decision trees on three-world problems, including worlds with no acceptable library candidate.

It explores strict-improvement paths in all 81 common-cost two-by-two games with costs in {0,1,2}. It checks detailed balance exactly for two rational exponential-weight bases. It reconstructs the synchronous cycle, the mixed-equilibrium saddle determinant, and the difference between a Gibbs joint law and the product of its marginals. It also runs the reconnection and destructive-inquiry belief examples.

The receipt records execution status, actual counts, interpreter information, and the script hash. An exception is recorded as a failure rather than omitted. The verifier rejects optimised Python because disabling its assertions would invalidate the test procedure. The script is an author-created example checker, not an independent proof assistant or a validation of the complete source corpus.

## 19. Two-pass audits and the refusal to self-certify completeness

### Cycle 1 — read-only coverage and advancement audit

The audit distinguishes three questions: have the bytes been acquired; have they been read semantically; and has the proposed synthesis been checked against them? Mechanical acquisition does not answer the latter two. The source queue has not been supplied with fresh range-by-range semantic receipts. Comprehensive ZIP, repository, and image-dependent mathematical review therefore remains a blocking finding.

The advancement component is positive but bounded: this report gives explicit certificate-selection, evidence-cost, grid-completeness, and learning-dynamics arguments. Its novelty relative to the entire supplied corpus is not established. Its compatibility with every canonical source amendment has not been audited. No claim of overall success follows.

### Cycle 1 — adversarial substance audit

The audit challenged the candidate on candidate-library incompleteness; common-equilibrium quantifier exchange; hard resource constraints; destructive observation; changing objectives; synchronised update cycles; zero-gain stopping; cost-model omissions; independent versus correlated probability laws; fixed-temperature versus cooling limits; physical-action identification; and unverified source coverage.

The local mathematical refinements are incorporated in Sections 6–16. Finite-library completeness is restricted to positive tolerance with a bounded-payoff grid construction. The inquiry theorem stops on a common acceptable candidate rather than requiring full identification. Active inquiries retain original-world labels. Potential convergence has an explicit progress premise. Logit concentration is a statement about stationary joint-state laws, not automatic nondegenerate mixed Nash convergence. Physical alignment remains an uninstantiated premise.

### Cycle 2 — repeated read-only audit

The coverage gate still fails. A more careful report cannot retrospectively supply the missing source read. The improved partial packet is therefore not relabelled an exhaustive approved consolidation. The machine audit can verify unchanged source hashes and consistent status reporting; it cannot manufacture the missing semantic receipts.

### Cycle 2 — repeated adversarial audit

The refined local arguments have been checked for the particular errors listed above, and the executable models provide additional bounded consistency evidence when their receipt passes. This is not an all-source adversarial clearance. The source-completeness finding, corpus-relative novelty, empirical bridge, and matched-baseline assessment remain open.

Both audit cycles are same-assistant self-audits. No independent human reviewer, separate model agent, or proof-assistant kernel is claimed. No finite checklist guarantees that every possible criticism has been found. The overall status is **PARTIAL / REQUESTED TWO-PASS COMPLETION GATE NOT PASSED**.

## 20. Explicit remaining work

The highest-priority source work is to read the canonical core, notation registry, operative decisions and amendment chains, the actual meniscus research prompts, and both frontier archives. This determines whether the proposed synthesis is already present, whether it contradicts a stronger result, and what the project's actual acceptance target is.

Every remaining source range then requires a receipt recording its claims, assumptions, definitions, dependencies, version/authority status, relationship to the consolidation, and adversarial findings. Duplicate renderings may share a substantive reading only after equivalence is verified and the relationship is recorded; an apparent duplicate filename is insufficient.

Mathematical extraction errors must be resolved from page images, especially quantifier order, inequality direction, operator domains, and table entries. Source executable checks must be read before execution. Their claimed counts, use of assertions, provenance, and relationship to the prose should be independently reconciled. Historical passing tests cannot be treated as a new run.

The proposed results need a corpus-relative comparison and an external prior-art check before any novelty assertion. The physical-to-agent mechanism needs a particular instance or an explicitly conditional interpretation, not another unnamed arrow. A matched prospective benchmark is needed for superiority claims. Repository adoption requires the owner's actual process; the local archive changes none of it.

Finally, repeat both requested audits after these obligations have been worked through. A remaining blocking finding must keep the overall gate open. The continuation prompt supplied with the archive carries these obligations forward without claiming they have been discharged.

## 21. Source reference map

**F1.** `orthing_formalisation_v1(1).pdf`, actual title *Graded Representations, Witnessed Revision, and Inquiry Landscapes*, Version 1, 8 September 2026, 35 PDF pages. Particularly §§2–8, 9–11, and the result/dependency register. Source evidence was supplied in the preceding conversation under the citation base `turn0file1`.

**F2.** `information-composition-and-self-revision-v5(1).pdf`, *Information, Composition, and Self-Revision: Local Descriptions and Operative Access*, 12 pages. Particularly §§1–5. Source evidence base: `turn0file2`.

**F3.** `the-cost-of-a-decisive-revision(1).pdf`, *The Cost of a Decisive Revision: Evidence, Reuse, and Self-Application*, 4 pages. Particularly §§1–4. Source evidence base: `turn0file3`.

**F4.** `The_Last_Moat_Edition_3(3).pdf`, *The Last Moat: Physical Realisability, Cross-Substrate Communication, and Holarchic Agency*, Edition 3, 10 September 2026, 58 pages. Particularly §§6, 10–18, and the evidence ledger. Source evidence base: `turn0file0`.

**F5.** `orthing_continuation_frontier_v1.zip`. Included in the requested corpus. Full fresh semantic review is pending; descriptions from the prior assistant are not promoted into source findings here.

**F6.** `orthing_modal_metaphysical_frontier_v2(1).zip`. Included in the requested corpus. Full fresh semantic review is pending; its modal and metaphysical claims are not adjudicated by this packet.

**R1.** `docs/project-closure/ar8r-v11/programs/tensor-and-bitter-lesson.md`, previously fetched at `f50dc1aee52356cc6adbef342387576b02afc124`. Distinguishes representations from ontology, controller and representation labels, and prospective evidence gates.

**R2.** `applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md`, previously fetched at the same pin. Distinguishes G0 metaphor, G1 order-ranked correction, and conditional G2 literal gradient dynamics. Historical candidate banners must be interpreted with subsequent decisions rather than used alone as a current-status verdict.

**R3.** `docs/decisions/0012-reference-model-semantic-contract.md`, previously fetched at the same pin. Contains the analysis declaration and explicitly bounded validation scope.

**R4.** `docs/project-closure/ar8r-v11/theorems/ar8r-t300-lower-order-alignment-blind-restoration.md`, previously fetched at the same pin. Supplies the bounded parity distinction and its scope limits.

These references identify the support used by this report. They are not a bibliography asserting that every document has just been completely reviewed. The acquisition inventory is authoritative for what bytes are actually included; the semantic queue is authoritative for what still lacks a fresh range-level receipt.
'''
# The machine section makes no claim beyond actual locally available receipts.
machine='''\n## Appendix A. Machine-recorded state for this packet\n\n```json\n'''+json.dumps({'coverage':coverage,'github_acquisition':github,'new_verification':results},indent=2)+'''\n```\n\nThe records above do not upgrade source semantics. The separate audit receipts preserve that distinction.\n'''
report+=machine
(P/'REPORT.md').write_text(report,encoding='utf-8')
# Preserve a preliminary outline, explicitly NOT a retrospectively invented approved draft.
(P/'research/PRELIMINARY_OUTLINE.md').write_text('''# Preliminary mathematical outline retained for audit context\n\nStatus: unapproved planning outline, not a source finding or completed review.\n\nThe initial proposed chain was: identify consequential unilateral gains; select a candidate common to compatible games; price adaptive inquiry; preserve original targets through changing observation methods; then study potential-aligned improvement and logit exploration.\n\nThe outline did not yet supply a finite candidate completeness condition, a destructive-inquiry state model, a progress premise for finite improvement paths, or a distinction between logit joint-state distributions and independent mixed Nash play. The report supplies those qualifications. This retained outline is not evidence that an earlier complete manuscript was independently audited.\n''')
findings=[
 ('A001','BLOCKING','Full fresh line-by-line source coverage is unestablished.','OPEN','Complete every semantic review queue range and page-image obligation.'),
 ('A002','BLOCKING','Both frontier ZIPs need fresh substantive and adversarial review.','OPEN','Reconcile their actual contents with this report; do not rely on the prior assistant claim.'),
 ('A003','BLOCKING','Canonical meniscus criterion and amendment/authority chain not fully reviewed.','OPEN','Read the operative research prompts, core, decisions and later amendments.'),
 ('A004','MAJOR','Current tree, historical fallback, discussion metadata and all-history coverage differ.','OPEN','Use acquisition ledger, repair missing reads, and record precise source scope.'),
 ('B001','MAJOR','A finite candidate library may omit exact mixed equilibria.','LOCAL_REFINEMENT_COMPLETED','Section 9 supplies a positive-tolerance bounded-payoff grid; exact-library completeness remains conditional.'),
 ('B002','MAJOR','Per-world equilibrium existence need not yield a common warranted profile.','LOCAL_REFINEMENT_COMPLETED','Section 8 gives the hidden-mode counterexample and exact blind regret lower bound.'),
 ('B003','MAJOR','Independent feasible schedules need not be jointly feasible.','LOCAL_REFINEMENT_COMPLETED','Sections 5–6 require an explicit total resource protocol and separate feasibility predicate.'),
 ('B004','MAJOR','Destructive probes invalidate nondestructive evidence recursion.','LOCAL_REFINEMENT_COMPLETED','Sections 10–11 separate the models and retain original situation labels.'),
 ('B005','MAJOR','Finite improvements do not imply Nash without continued examination.','LOCAL_REFINEMENT_COMPLETED','Section 12 adds the progress/certification premise and distinguishes absorption from recognition.'),
 ('B006','MAJOR','Cooperative synchronous updates can cycle.','LOCAL_REFINEMENT_COMPLETED','Section 14 gives a concrete two-state cycle; the improvement theorem is asynchronous.'),
 ('B007','MAJOR','Interior mixed Nash need not be an attracting state.','LOCAL_REFINEMENT_COMPLETED','Section 14 computes the saddle linearisation; no interior-selection theorem is claimed.'),
 ('B008','MAJOR','Stationary joint-state law is not independent mixed play.','LOCAL_REFINEMENT_COMPLETED','Sections 13–14 distinguish the laws with exact 1/5 versus 1/2 conflict probabilities.'),
 ('B009','MAJOR','Fixed-temperature stationary concentration is not arbitrary cooling convergence.','LOCAL_REFINEMENT_COMPLETED','Section 13 states the limit and persistent exploration separately.'),
 ('B010','MAJOR','Effective cost alignment is not a physical least-action derivation.','OPEN_INSTANCE','Section 15 retains the physical bridge as a specific modelling and evidence obligation.'),
 ('B011','MAJOR','A conventional reformulation may not advance the canonical meniscus criterion.','OPEN_COMPARISON','Compare with all source results and a strong matched baseline; no novelty/superiority claim.'),
 ('B012','MAJOR','Machine tests can be mistaken for general proof or source review.','LOCAL_REFINEMENT_COMPLETED','Section 18 and verifier receipt bound the claim; optimised Python is rejected.'),
 ('B013','MAJOR','New source-independent code must not be called a corpus concolic audit.','LOCAL_REFINEMENT_COMPLETED','Section 14 names the finite concrete/symbolic scope; no SMT/full-code claim.'),
 ('A005','BLOCKING','Source-page mathematical extraction and source-code validation remain unaudited.','OPEN','Inspect relevant page images and read source tests before execution.'),
 ('B015','MAJOR','After a destructive intervention, initial strategic acceptability need not imply current feasibility.','LOCAL_REFINEMENT_COMPLETED','Section 11 now distinguishes retrospective targets from operational acceptance on current-state/original-situation pairs.'),
 ('B014','MAJOR','Same-assistant audits are not independent review.','LOCAL_REFINEMENT_COMPLETED','Section 19 explicitly states reviewer provenance.'),
]
with (P/'audits/findings.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['id','severity','finding','disposition','resolution_or_remaining_obligation']);w.writerows(findings)
report_hash=hashlib.sha256((P/'REPORT.md').read_bytes()).hexdigest()
for cycle in (1,2):
 for mode in ('coverage','adversarial'):
  obj={'cycle':cycle,'pass':mode,'reviewer':'same assistant; no independent reviewer claimed','candidate_sha256':report_hash if cycle==2 else None,'source_modification_authorised':False,'overall_requested_gate':'NOT_PASSED','source_line_by_line_review_complete':False,'disposition':'PARTIAL_STAGED_DELIVERY','new_finite_verification_status':results.get('status','NOT_ESTABLISHED'),'finding_ids':[x[0] for x in findings if (x[0].startswith('A') if mode=='coverage' else x[0].startswith('B'))],'note':'Cycle 1 records substantive planning-stage challenges. Cycle 2 assesses the refined local report while preserving the still-blocking all-source coverage finding. This is not an invented independent audit approval.'}
  (P/f'audits/cycle_{cycle}_{mode}.json').write_text(json.dumps(obj,indent=2))
# Read-only integrity audit of the acquired source bytes.
source_rows=load('ledgers/source_inventory.json',[]);changed=[];missing=[]
for row in source_rows:
 p=P/row['source_path']
 if not p.is_file():missing.append(row['source_path'])
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:changed.append(row['source_path'])
(P/'audits/read_only_integrity.json').write_text(json.dumps({'source_files_checked':len(source_rows),'changed':changed,'missing':missing,'byte_integrity_status':'PASS' if source_rows and not changed and not missing else 'NOT_ESTABLISHED_OR_FAIL','semantic_coverage_status':'INCOMPLETE','report_sha256':report_hash},indent=2))
# A navigational line map does NOT assert those lines received independent review.
lines=report.splitlines();heads=[]
for i,l in enumerate(lines,1):
 if l.startswith('#'):heads.append({'line':i,'heading':l.lstrip('# ').strip()})
(P/'ledgers/report_line_map.json').write_text(json.dumps({'report_sha256':report_hash,'line_count':len(lines),'headings':heads,'status':'NAVIGATION_NOT_A_SEMANTIC_REVIEW_CERTIFICATE'},indent=2))
(P/'research/REPORT_NUMBERED.txt').write_text('\n'.join(f'{i:05d} | {l}' for i,l in enumerate(lines,1))+'\n')
continue_prompt=r'''# Continuation prompt — do not treat the staged packet as completed

Continue the user's requested exhaustive consolidation of `theislampill/orthemology` and all supplied attachments. This archive is a PARTIAL research packet. Its requested line-by-line/two-pass completion gate has NOT passed. Do not describe acquisition, extraction, keyword search, or a generated queue as semantic review.

First inspect `README.md`, `REPORT.md`, `ledgers/coverage.json`, `ledgers/github_scope.json`, `ledgers/acquisition_events.json`, `audits/findings.csv`, all four audit-cycle receipts, and `verification/results.json`. Verify `SHA256SUMS` and identify any distribution exclusions. Recover the actual current repository through GitHub and pin it; distinguish current acquisition from historical fallback. Work read-only unless the owner separately authorises a repository change.

Read every line of every requested source. `ledgers/semantic_review_queue.jsonl` is the starting queue, not proof of completion. For each contiguous range, record actual semantic findings: definitions, claims, assumptions, proof dependencies, status/authority, evidence, tensions with other sources, counterexamples, and the exact report section affected. Resolve PDF extraction ambiguity from the corresponding page images. Do not use OCR when native text and page vision suffice. Do not silently discard binary, archived, duplicate, historical, or conflicting material. Identify what each contributes and how it is handled.

Prioritise the canonical core and notation registry; operative decisions and their amendments; actual meniscus/convergence research prompts; both frontier archives in full; and the four supplied PDFs. Then complete every remaining repository source range. Read source tests before executing them and reconcile the claimed verification scope with actual implementations. A passing assertion-disabled run is not verification. Do not infer a repository-wide absence from a keyword miss.

Substantively adjudicate the proposed evidence-limited equilibrium synthesis in REPORT §§6–16. Check whether the frontier archives already contain equal or stronger results. Check every proof, especially rational-grid completeness, relation-valued evidence cost, destructive-inquiry labels, potential-improvement progress, logit detailed balance, and the distinction between a stationary joint law and independent mixed Nash play. Preserve the user's claim as a probabilistic/explanatory hypothesis; do not substitute a direct PoLA-implies-Nash claim. Develop the actual project trajectory under its recovered canonical meniscus criterion, not a self-selected replacement.

Run the included exact verifier in ordinary Python and record its hash and actual results. Extend it with independently specified counterexamples and tests for any new claim. Its present success, if recorded, concerns only its synthetic finite models. It does not certify full source reading, the physical bridge, empirical benefit, independent novelty, or adoption.

Before delivery, conduct (1) a read-only coverage/substantive advancement audit against the full source reading and (2) an adversarial audit of the original material and composed candidate. Work every finding through; distinguish actual resolution from an explicitly still-open obligation. Refine the deliverable, then run BOTH audits again. Do not make a gate pass by narrowing the original request or reclassifying unreviewed material as irrelevant. Same-assistant audits must not be called independent review.

Deliver the refined report, all evidence and source-to-claim maps, runnable checks and receipts, both audit histories, resolution records, unchanged source provenance, and a self-contained archive. Do not distribute font files or secrets. If full completion remains impossible in the current pass, preserve ALL work and a precise remaining queue, explain why the overall gate is still open, and provide the next continuation prompt. Never claim ultima facie success merely because files were created or tests passed.
'''
(P/'CONTINUE.md').write_text(continue_prompt)
(P/'README.md').write_text('''# Orthemology staged research archive\n\n**Overall status: PARTIAL; requested exhaustive line-by-line and recursive two-pass approval NOT achieved.**\n\nStart with REPORT.md or REPORT.html. The report contains a substantive conditional development, not an all-source completion claim. CONTINUE.md carries the owner's original requirement and the precise unfinished work forward.\n\n## Contents\n\n- `sources/`: source bytes and safely unpacked archive members actually acquired; consult acquisition logs for omissions.\n- `extracted/`: PDF text with page markers; extraction is not mathematical or semantic validation.\n- `ledgers/`: acquisition pin, source hashes, counts, duplicates, pending semantic ranges, and report line navigation.\n- `research/`: numbered report and preliminary outline.\n- `verification/`: new exact finite checker and execution receipts, if execution completed.\n- `audits/`: both audit cycles, finding dispositions and read-only byte-integrity check.\n\nRun the new checker with `python verification/verify_synthesis.py` from an ordinary, non-optimised Python interpreter. It uses the standard library only. It executes no repository code and makes no network requests.\n\n`SHA256SUMS` covers files distributed in this archive except itself. `ledgers/distribution_exclusions.json` records font/security/archive exclusions where applicable. Original source manifests may include acquired files omitted from redistribution; this is disclosed rather than silently called a complete snapshot.\n\nMachine-indexed lines are not semantically reviewed lines. The coverage ledger deliberately refuses to count them as such. The exact meniscus criterion, complete ZIP/repository review, corpus-relative novelty, and physical/empirical bridge remain outstanding.\n''')
# Self-contained HTML: no network-loaded renderer or font assets.
try:
 import markdown
 body=markdown.markdown(report,extensions=['tables','fenced_code','toc'])
except Exception:
 chunks=[];code=False;para=[]
 def flush():
  if para:chunks.append('<p>'+html.escape(' '.join(para))+'</p>');para.clear()
 for line in lines:
  if line.startswith('```'):
   flush();chunks.append('</code></pre>' if code else '<pre><code>');code=not code
  elif code:chunks.append(html.escape(line)+'\n')
  elif line.startswith('#'):
   flush();n=min(6,len(line)-len(line.lstrip('#')));chunks.append(f'<h{n}>'+html.escape(line.lstrip('# ').strip())+f'</h{n}>')
  elif not line.strip():flush()
  else:para.append(line)
 flush();body='\n'.join(chunks)
style='''body{font-family:system-ui,Arial,sans-serif;max-width:1000px;margin:48px auto;padding:0 28px;color:#182333;line-height:1.62;background:#fff}h1{font-size:2.25rem;line-height:1.15;color:#16344d}h2{margin-top:2.3rem;border-top:1px solid #ced9df;padding-top:1rem;font-size:1.55rem;color:#16344d}h3{font-size:1.2rem;color:#234b60}pre{background:#f2f5f7;border-left:3px solid #7b96a6;padding:16px;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;font-size:.86rem;line-height:1.5}code{font-family:ui-monospace,Consolas,monospace}table{border-collapse:collapse;width:100%}td,th{padding:8px;border-bottom:1px solid #d8e1e7;text-align:left}a{color:#174f70}strong{font-weight:650}@media print{body{max-width:none;margin:0;font-size:10pt;padding:0}h2,h3{break-after:avoid}pre{break-inside:avoid}a{color:inherit}}'''
(P/'REPORT.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Orthemology — staged consolidation</title><style>'+style+'</style><body>'+body+'</body></html>')
# Include reproducible acquisition/build scripts, not tools' private reasoning.
for name in ('acquire.py','build_delivery.py'):
 q=R/name
 if q.exists():shutil.copy2(q,P/'research'/name)
# Scan nested ZIPs for fonts rather than hiding font files in the outer archive.
font_suffix={'.ttf','.otf','.woff','.woff2','.eot','.pfb','.pfa','.ttc'}
exclusions=[];eligible=[]
def nested_font(data,depth=0):
 if depth>5:return True
 try:
  import io
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   for i in z.infolist():
    if Path(i.filename).suffix.lower() in font_suffix:return True
    if i.filename.lower().endswith('.zip') and nested_font(z.read(i),depth+1):return True
  return False
 except Exception:return True
for q in sorted(P.rglob('*')):
 if not q.is_file() or q.name=='SHA256SUMS':continue
 why=None
 if q.suffix.lower() in font_suffix:why='font file not distributed'
 elif q.suffix.lower()=='.zip' and nested_font(q.read_bytes()):why='nested archive could contain fonts or cannot be safely inspected'
 elif q.suffix.lower() in {'.gz','.tgz','.bz2','.xz','.7z','.rar'}:why='opaque nested compressed archive omitted; retained in acquisition record when present'
 else:
  try:
   t=q.read_text('utf-8')
   if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\s+[A-Za-z0-9+/=\s]{80,}',t):why='possible private key material not redistributed'
  except (UnicodeDecodeError,OSError):pass
 if why:exclusions.append({'path':str(q.relative_to(P)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'reason':why})
 else:eligible.append(q)
x=P/'ledgers/distribution_exclusions.json';x.write_text(json.dumps(exclusions,indent=2));eligible=[q for q in eligible if q!=x]+[x]
checks=''.join(hashlib.sha256(q.read_bytes()).hexdigest()+'  '+str(q.relative_to(P))+'\n' for q in sorted(eligible))
(P/'SHA256SUMS').write_text(checks);eligible.append(P/'SHA256SUMS')
outputs={
 'report_markdown':Path('private-locator:3ed23eaa542a29749f5f'),
 'report_html':Path('private-locator:5aab4b953069cafe0dde'),
 'continuation_prompt':Path('private-locator:c8c3fd6582f02430f6e5'),
 'archive':Path('private-locator:8114b57b243302702d3e')}
shutil.copy2(P/'REPORT.md',outputs['report_markdown']);shutil.copy2(P/'REPORT.html',outputs['report_html']);shutil.copy2(P/'CONTINUE.md',outputs['continuation_prompt'])
with zipfile.ZipFile(outputs['archive'],'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for q in sorted(set(eligible)):z.write(q,arcname='orthemology_stage1/'+str(q.relative_to(P)))
with zipfile.ZipFile(outputs['archive']) as z:
 bad=z.testzip()
 if bad:raise RuntimeError('Archive CRC verification failed: '+bad)
 names=z.namelist();assert 'orthemology_stage1/REPORT.md' in names and 'orthemology_stage1/CONTINUE.md' in names
receipt={'overall':'PARTIAL_NOT_APPROVED','verification_status':results.get('status'),'files':{k:{'path':str(v),'bytes':v.stat().st_size,'sha256':hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in outputs.items()},'source_coverage':coverage,'repository':github,'distribution_exclusions':len(exclusions),'archive_members':len(names)}
Path('private-locator:25b1649c89cfd2f2635e').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
