# Exact theorem map

All new theorems are in namespace `AttributionKernel`. α is an arbitrary finite
label type with decidable equality, m = Fintype.card α. No theorem below is a
bounded enumeration. Normal classical/logical axioms are permitted; no custom
axiom or desired cardinal theorem is assumed.

## Accepted Theorem A
- `RootImage.cross_image_identity`: equation (1), counting an actual Option-valued
  root image and a separate one-root bridge contribution.
- `RootImage.robust_iff`: exact equation (3), forall B≥1,c≥1,c≤m,P,R, forall all
  c-subsets A. Includes P∩R empty. Proof constructs A inside I if c≤|I| and
  extends I to A otherwise; sufficient direction derives a collapse bound.
- `ImageMinima.sharp_nonempty_minimum`: equation (2), universal lower bound and
  attaining A for every nonempty I. Its natural-number `|I|-c+1` is exactly the
  source's max(1, integer(|I|)-c+1).
- `ImageMinima.forced_bridge_iff` and `disjoint_zero_fault_iff`: the all-parameter
  forced-bridge corner and precise failure of the B≥1 conclusion at B=0.

## Accepted Theorem B
- `Availability.tainted_label_budget`: any root fault set pulls back to at most
  |S|+|A|-1 labels, from a proved root-image collapse bound.
- `maximal_taint_realizable`: every k-set T yields an A of exactly c labels and
  S contained in actualRoots A of exactly B roots, with pullback exactly T.
- `available_iff`: universal actual-world availability iff every k-set is avoided.
  It uses the weaker auxiliary k≤m parameter restriction; the
  central theorem uses the original B<m-c+1 and obtains k<m.

## Accepted Theorem C
- `FixedFamilies.fixed_contract_iff`: real-root safety/availability contract is
  exactly the proved label-family contract, preserving fixed F/G scope.
- `label_fixed_family_lower`: arbitrary, possibly nonuniform F/G imply m≥3k+1.
  The proof chooses a k-set T and allowed P avoiding T, so |P|≤m-k. It chooses
  min(k,|P|) labels U of P and an allowed R avoiding U (extend U to a k-set).
  Then |P∩R|≤|P|-min(k,|P|), contradicting >k unless m≥3k+1. This is equivalent
  to the accepted two-maximal-taint-set obstruction, without uniformity.
- `label_threshold_upper`: all (m-k)-subsets attain the bound.
- `fixed_family_feasible_iff`: central all-parameter existence iff, retaining
  B≥1,c≥1,c≤m,B<m-c+1 and every P∈F,R∈G safe in every compatible map.
- `Availability.actual_root_count`: n=m-c+1, explicitly different from labels.

## Representation correspondence, not an extra assumption
- `MapTransport.ExactOneClassMap A ρ` says the equality fibers of ρ are precisely
  A and the singleton labels outside A. `canonical_exact` proves the Option
  map has that property.
- `arbitrary_map_shared_card` transports every such ρ, with arbitrary decidable
  root-name type, to the same shared-root count. Only nonempty A is required.
- `arbitrary_faults_pullback` and `canonical_faults_pushforward` preserve cardinality,
  image membership and each label's fault membership in both directions.
- `arbitrary_map_available_iff` proves availability is invariant under this root
  renaming. Real fault sets are restricted to the actual image on both sides.
- `Correspondence.old_shared_card_correspondence` identifies this count with the
  accepted `UnknownRootAttribution.rootOf` representative-index map.
- `booleanLabels_card` matches Finset cardinality to the unchanged accepted
  recursive `ChargedInterlock.card`; `old_robust_iff` restates the sharp iff using
  those exact original Bool/Nat definitions, including all original predicates.

## Fixed scope and exclusions

F and G are Set (Finset α), existentially chosen once outside all map/fault
quantifiers. No later map evidence changes them. A Set-of-Finsets presentation
admits every finite-universe fixed family, including nonuniform families and
empty sets, without presuming threshold structure. The proofs do not silently
identify independent roots with interface labels.

This closes the combinatorial/cardinality content of accepted A–C under the
stated static map interface. It does not encode the retained dynamic-interlock
physical service, authorization, coherence or temporal semantics. It does not
prove that a real system satisfies those premises, enlarge fixed R5, or establish
covering/search optimality (accepted E). Separate work may deepen E; none is
claimed by this packet. D's operational cancellation story is likewise not
closed by this packet's cardinal results.
