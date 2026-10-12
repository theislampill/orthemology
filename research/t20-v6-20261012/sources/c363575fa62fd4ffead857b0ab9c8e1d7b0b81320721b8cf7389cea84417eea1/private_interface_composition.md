# Composing migration interfaces without turning private memory into public warrant

**Status:** a successor refinement of `stochastic_refinement.md`. The original all-public-mode contract remains the default checker mode. This extension preserves the same full-marginal, source-adversary, eligibility and semantic premises. It adds an explicit information boundary rather than declaring every remembered virtual action public.

## 1. A private/public mode split

Replace the all-public mode z by a finite controller-available mode q∈Q and a declared projection π:Q→P. Only p=π(q) is public. The observation reconstruction η(q,o), abstract-action menu M(q,o), action translation τ(q,o,a), and private update

`q' = u(q,o,a,b,o')`

may use q and the controller's remembered virtual action a. Destination warrant has the form

`J_B(π(q),o,b)`.

To make the projection genuinely public, require that a function v exists with

`π(u(q,o,a,b,o')) = v(π(q),o,b,o')`

on all used transition entries. Thus different private histories with the same public mode, actual action and new observation cannot produce different next public modes. The initial q is a declared deterministic function of the initial public observation, as in the original implementation. Private randomized initialization could be added with a full initial-law contract but is not implemented here.

**SR1-P.** Under this split and the other clauses of SR1, the same destination construction and almost-sure transfer theorem hold.

**Proof.** The destination can use q and its own remembered virtual actions, so the reconstructed source history is available to its controller. In the joint measure proof those variables are retained in the destination controller history; they do not require observing hidden source state. Inductively, π(q) is a function of the actual public trace because its initial value is public and v updates it from public data. Warrant is checked only at that projection. All exact marginal equations and badness reflection are unchanged. Consequently SR1's gluing and adversarial marginalization proofs apply. ∎

The default checker takes π to be the identity, recovering the original all-public contract. Supplying a nontrivial `public_projection` opts into this explicitly different contract. It does not bypass the public-warrant requirement.

## 2. Why the all-public class alone is not composition-closed

Consider three plants with two virtual actions 0 and 1.

- A has state x∈{0,1}, observes x, and action a sets the next state to a.
- B has state y∈{0,1}, observes only a constant o, and action b sets the next state to b.
- C has one state, one observation o and one actual action `tick`.

All states are safe/good and all displayed actions are licensed in this structural counterexample. Initial A and B states are 0.

The A→B interface executes b=a and uses public mode q=y, updated to the publicly executed B action b. It reconstructs A's observation as q. Its relation is {(0,0,0),(1,1,1)} and every step coupling is deterministic.

The B→C interface translates both B actions to `tick`, needs only one constant public mode, and reconstructs B's constant observation. Its relation pairs either B state with C's single state. Again all full couplings exist.

In the composite, the controller remembers the virtual B action, but C's public trace reveals only repeated `tick` and o. The A-state-tracking mode is therefore private at C. Requiring it to be public fails: two possible virtual actions at the same time yield different A observations while the actual C public history is identical. This defeats full-observation reconstruction for the supplied two-action interface; it is not a claim that no particular constant policy could migrate.

A private product mode repairs the composition. Its public projection is the constant C-side public mode. The actual C warrant depends only on that projection and `tick`, never on the privately retained virtual action.

## 3. SR2: compositional exact refinement

Let I₁ be a valid split interface A→B with private mode q and public projection π₁; let I₂ be a valid split interface B→C with private mode r and public projection π₂. The middle model must be the same model, including its kernels, meanings and initial law. For the implemented constructor these structures must be exactly equal, not merely claimed equivalent.

Assume action-menu compatibility: for every relevant q,r,o_C and every a in the first interface's menu, the translated B action belongs to the second interface's abstract-action menu. If this fails, restricting the menu would require a new source-policy conformance proof; the constructor rejects rather than silently restricting it.

Use private product mode m=(q,r), with public projection

`π(m)=π₂(r)`.

For o=o_C(w), define

`o_B = η₂(r,o)`

`η(m,o) = η₁(q,o_B)`

`b = τ₁(q,o_B,a)`

`c = τ₂(r,o,b)`.

After observing o', update

`r' = u₂(r,o,b,c,o')`

`o_B' = η₂(r',o')`

`q' = u₁(q,o_B,a,b,o_B')`.

The composed relation is

`R_AC = {(x,w,(q,r)) : exists y, (x,y,q)∈R_AB and (y,w,r)∈R_BC}`.

Initial modes are composed in the same order: first reconstruct the initial B observation from C, then initialize q. The source controller retains any additional memory it already needed.

**Theorem SR2.** These formulas define a valid split refinement A→C, preserving source-to-destination badness and safety reflection and the final destination's independently supplied warrant. Almost-sure restoration transfers under the same robust source-policy assumptions. No intermediate hidden plant state need be observed by the implemented controller.

### Local coupling proof

Fix a related triple (x,w,(q,r)), a compatible source action a, and a C disturbance kernel. Choose a middle witness y of the composed relation. The second certificate supplies a B disturbance kernel P_B and a full coupling κ_BC of P_B and the chosen P_C. The first certificate, for that same B kernel, supplies a source kernel P_A and a full coupling κ_AB of P_A and P_B.

For P_B(y')>0 define the triple mass

`λ(x',y',w') = κ_AB(x',y') κ_BC(y',w') / P_B(y')`.

Terms at zero middle mass are zero, because both couplings have zero mass there. Summing λ over y' gives κ_AC(x',w'). Then

`Σ_{w'}κ_AC(x',w') = Σ_{y'}κ_AB(x',y') = P_A(x')`

and symmetrically `Σ_{x'}κ_AC(x',w')=P_C(w')`. These are full probability laws, not normalized favourable subsets.

Whenever λ>0, the second relation ensures that the reconstructed next B observation equals the actual o_B(y'). Therefore the displayed q',r' updates are exactly those used by the two component certificates. Both component successor relations hold at that same y', proving membership in R_AC. The intermediate witness may be chosen for the mathematical certificate; the public/private controller formula does not consult it.

Initial couplings glue by the identical formula using the common middle initial marginal. This is why two independently declared but unequal B priors cannot be silently composed.

### Information, authority and memory proof

Observation identities compose through the middle witness. The product update is available to the controller because it knows q,r,a and its own virtual b. The projected next public state π₂(r') is public by I₂'s projection consistency, independent of whether b is public at C. Bad_C⇒Bad_B⇒Bad_A and Safe_A⇒Safe_B⇒Safe_C compose pointwise. C's warrant remains J_C(π₂(r),o_C,c); a valid middle warrant is not substituted for actual C authorization.

Thus SR1-P applies. If the original source controller has an M-state implementation with deterministic history-updated memory and fresh current-action draws, the composed implementation uses at most |Q||R|M controller-memory states under the same observation-storage convention. A randomized-memory implementation requires a separate check that the behavioral action kernel is preserved under the declared adversary’s memory exposure; no pre-sampled future coins may be silently exposed. This finite bound does not apply to a source policy whose memory was already unbounded. ∎

## 4. Scope of readout preservation

The constructor checks equality of the middle observation map, kernels, eligibility set, bad/safe labels and initial law. It composes the badness/safety claims just proved. It does not infer an arbitrary task's identity from those labels. Optional readout relations must be supplied and checked for the desired A→C claim. If two readout relations are meant to compose existentially through the very same middle witness, that can be proved separately; replacing them with output-label equality would be a stronger unearned claim.

All currentness, provenance-root interpretation and normative warrants remain model inputs. Composition of correct conditional probability kernels cannot establish that independently acquired evidence actually has those kernels, or that the final action has institutional or normative permission.

## 5. Reproducible checks

The extended `verify_refinement(c, public_projection=...)` checks public-projection coverage, projected update consistency and warrant at the public projection. Three red-first tests check the genuinely private positive control, rejection of falsely declared public modes, and missing projection entries.

`refinement_composition.py` implements the finite interface formulas and independently re-verifies the resulting contract. Its `glue_couplings` checks full exact laws and equal middle marginals. Three additional tests check the all-public-to-private composition counterexample, reject inconsistent middle initial laws, and verify a nontrivial rational gluing by hand-computed masses. The six-module test suite passes 34 tests.

`probe_refinement_composition.py` additionally builds seeded three-plant compositions with hidden clones, two modes and adversarial kernel menus. It constructs each local composite law directly from the two component witnesses, then checks full marginals and composed relation support independently of the composite checker's new transportation solve. Counts and results are recorded in `refinement_composition_results.json`.

Reproduce:

```sh
python -m unittest test_restoration test_migration test_correlation test_stochastic_refinement test_private_refinement test_refinement_composition
python probe_stochastic_refinement.py
python probe_refinement_composition.py
```

The gluing formula and compositional simulation ancestry are standard. The research contribution here is a scoped bridge and an exposed information/authority failure mode, not a claim of new probability theory or first discovery of transitivity. [Haesaert–Soudjani–Abate, probabilistic simulation and transitivity](https://arxiv.org/pdf/1605.09557).
