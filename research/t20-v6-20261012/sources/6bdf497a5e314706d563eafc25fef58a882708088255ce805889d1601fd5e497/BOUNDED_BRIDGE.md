# Realized-menu erasure is not harmless averaging

## Owners and scope

This is a new exact finite calculation on the **inherited** S6F-15 shared-random action-disclosure construction, read in POSITIVE_ERROR_FRONTIERS.md §5, and its timing distinction in S6F-18 TIMING_RESOURCE_BOUNDARIES.md. S6F-16 supplies the inherited globally optimal private-codebook value. Source IDs and exact public/original hashes are in SOURCE_BINDINGS.json. No general minimax frontier is newly proved here; no deployment, source authentication, moral permission, or new v4 proof is claimed.

The model has eight authenticated action roots labelled 0,…,7, a fixed corrupt set C of size three chosen before the fresh public seed, an informed cooperative sender who knows C, and a receiver required to execute one root. Acting at a corrupt root is damage. The two labels designate actions/lotteries, not assertions of certain safety. Both parties know the realized shared menu when the original sender chooses. Sender truth/cooperation, referent binding, action effects and the fault epoch are independently supplied premises.

## Original shared protocol

Sample an unordered two-root set T uniformly from the 28 possibilities. Order it increasingly as (min T,max T), with those actions assigned message labels 0 and 1. The sender sees C and T and selects an intact menu entry if one exists. Damage occurs precisely when T⊆C. Therefore every fixed three-set C has damage probability

    choose(3,2)/choose(8,2) = 3/28.

This is the inherited source's construction and optimal value, not new credit.

## A particular erasure transformation

Erase T before the sender chooses. Replace decoder 0 and decoder 1 by their respective *averaged* root distributions. The sender still knows C and may choose the better of those two fixed rows; the receiver privately samples that row. For root i∈{0,…,7},

    p_0(i)=(7−i)/28,     p_1(i)=i/28.

Indeed, i is the minimum of 7−i two-element sets and the maximum of i sets. Both rows sum to one. The transformation preserves each decoder's pre-message averaged action law. It deletes the joint shared resource that made the message selectable after seeing the actual menu.

For a three-set C, let s=Σ_(i∈C)i. Its two corruption masses are (21−s)/28 and s/28. The informed sender's minimum risk is

    min(s,21−s)/28.

Since s is an integer, this is at most 10/28. The set {0,3,7} has s=10, so the maximum is attained and the transformed protocol's exact minimax risk is

    10/28 = 5/14.

The increase over 3/28 is 1/4. This is a calculation for this **particular sorted-label averaging transformation**, not the best private protocol, and not a claim that every menu erasure gives 5/14. Randomly ordering the same menus before averaging would produce two uniform rows and value 3/8, a different transformation.

## The other values must not be conflated

- Original shared menu, C committed before seed: 3/28.
- This erased/sorted-averaged codebook: 5/14.
- Reoptimized private fixed-codebook problem: 1/4. The inherited complete frontier proves optimality; two disjoint four-root uniform rows attain it.
- The **unchanged original** random two-root menu exposed before choosing C: 1, since a three-set can include both menu roots.
- Reoptimized corruption-after-public-codebook game: 1/4, by S6F-18.
- Reoptimized corruption-after-full-message-before-private-draw game: 3/8.
- Corruption after the chosen root is exposed, before execution: 1.

The transformation changes which information the informed sender has at message choice. The latter schedules instead change when the adversary can act. Keeping these distinct is essential.

## Exact relationship to v4

The v4 occurrence sidecar preserves a specified deterministic record-view operation contract. It is not a theorem that equal message alphabet sizes or equal unconditional decoder marginals preserve every signaling game. PT-20's positive source realization preserves joint-reply fibres under the required conditional seed law. ET-17 retains one model across a complete policy. Those are compatible with this failure test: replacing E_T[min_m p_(T,m)(C)] by min_m E_T[p_(T,m)(C)] is not a valid contract homomorphism merely because averaged rows agree.

The proper operational refinement must state: who knows the actual menu; when message choice occurs; when C is committed; what becomes public before execution; which root the chosen label denotes; and whether its causal integrity persists. No amount of copying a source record supplies these premises automatically. Conversely, when the complete relevant joint/conditional contract is preserved, this example supplies no obstruction.

## Fresh evidence

CONTROL_CHECK.py uses exact Fraction arithmetic and explicit exception checks. It enumerates all 56 three-root fault sets and all 28 menus, verifies 3/28 for every fixed C, verifies 5/14 for the averaged rows, checks the four-root partition and inherited formula instance at 1/4, and verifies that every exposed menu is contained in a permitted corrupt set. It also provides a two-root equal-marginals/different-joint-loss diagnostic and the inherited carrier/root copy arithmetic.

Normal and optimized Python outputs are byte-identical. Their receipts are CONTROLS.normal.json and CONTROLS.optimized.json. This is fresh finite arithmetic verification, with a written finite proof above. It is not fresh verification of S6F-16's external partition-Kneser theorem, a fresh Lean proof, or an independent review of this new calculation.
