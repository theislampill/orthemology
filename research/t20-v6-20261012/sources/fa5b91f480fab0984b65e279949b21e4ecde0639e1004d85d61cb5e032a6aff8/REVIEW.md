# Independent scientific review: tagged Sigma boundary

Verdict: PASS, restricted to source derivability and the explicitly exhibited semantic models.

## Result and exact scope

Let SigmaRaw = Sigma Raw Raw and Eta = Pi z:SigmaRaw. Id_SigmaRaw(z, pair(fst z)(snd z)). For the unchanged P01AC.ExtensionalRepair.HasE grammar, no source polynomial inhabits R -> Eta, and none inhabits R -> (Eta -> Bottom), where R is the exact SourceRigidity.Rigidity type. Boundary.relative_independence records these two all-polynomial exclusions. Boundary.no_eta_under_rigidity additionally gives the direct open-telescope exclusion with both R and the pair variable present.

Eta is a constant-fibre instance of the general dependent-pair eta schema. Refuting this instance suffices to refute a universal schema; it does not assert failure at every dependent-pair type. The independent ReviewControls proves formation of Eta and both conditional targets, so noninhabitation is not an ill-formed-type artifact. It proves an actual HasE pair inhabitant of SigmaRaw.

## Model audit

TaggedPER is a separate namespace, not a mutation of FullPER or of the source syntax. The only interpretation change is the added conjunct tag(z) iff tag(w) at Sigma, where tag(z) means Conv z (pair(fst z)(snd z)). Raw is literally the inherited operational conversion relation. All still quantifies over every conversion-saturated PER. Pi and identity retain their original definitions. No reduced type-quantifier domain or artificial Raw collapse is involved.

The conversion-invariance lemma tag_congr is correctly oriented, pair introduction always produces a tagged value, and the extra predicate is independent of the type and term environments. This makes substitution, mixed substitution, and environment transport compatible. The dependent Sigma PER proof explicitly transports the second component along related first coordinates; symmetry, transitivity and saturation retain the tag condition. The new fundamental_sigma_snd correctly extracts the second-component relation rather than the added tag.

The mutual FormE/HasE recursors cover every constructor in the exact source: finite derivations, impredicative introduction/elimination, raw operations, dependent Pi/Sigma, identity introduction, proof erasure, J, source conversion, Pi extensionality, and All extensionality. Formation coherence is derived by that induction, not injected as a source premise. The original J proof uses the derived transport law across its actual theta context and remains applicable. There is no primitive Sigma eta rule to invalidate the new model, but this absence alone is not the nonderivability argument: complete source soundness plus the concrete counterexample supplies that argument.

## Concrete separator and positive controls

I belongs to SigmaRaw reflexively. Its projections convert to K and K I. The canonical reconstruction has the same projections. Nevertheless I is not tagged. Applying a purported conversion I ~ pair(K)(K I) to the inert zero term would convert zero to zero K (K I); these are syntactically different normal forms under the inherited open SKI operational relation. OpenDevelopments.normal_unique excludes this conversion. This is an operational separation, not a cardinality or informal free-model claim.

Canonical pairs satisfy eta in the tagged model (ReviewControls.canonical_eta). The same ghost satisfies eta in the original FullPER model (ReviewControls.old_model_eta_at_ghost). Boundary.full_eta_valid validates the entire Eta type there using K I. The exact interpretations of R in FullPER and TaggedPER are definitionally equal, and the inherited whole-type rigidity proof supplies a fixed realizing polynomial at arbitrary environments. R validity is not inferred merely from one compiler example or a pointwise computational observation.

Independent controls establish that componentwise equality alone cannot construct the tagged Sigma relation, and that reflexivity cannot prove the separating raw conversion. Both intentionally invalid Lean files fail compilation. Raw and All exactness are also positively checked. Thus equal projection observations fail to separate the modeled Sigma identity relation. This is precisely an equality-completeness boundary for the listed observations.

## Interpretation limits

The tagged Sigma relation is a countermodel to derivability from the actual rules, including the explicit R hypothesis. It is not asserted to be an equally intended interpretation of dependent-pair identity, nor a defeater of an intended semantic Sigma eta principle. Inherited P01PER.sigma_eta is a semantic theorem for its original componentwise interpretation, not an additional HasE constructor or a source derivation.

The result distinguishes source-strength credit from representational or ontological warrant. It does not refute the independently established inductive/initial natural-number results, establish any physical continuation principle, or license a metaphysical inference. Additional eta or projection-completeness assumptions would need their own explicit source rule or justification. No such extension is adopted here.

## Replay and preservation

ReviewControls and the two frozen author modules were freshly compiled using Lean 4.19.0 with --trust=0. The author sources were copied into this review's sources directory and compared against the freeze after replay. Existing reviewed baseline objects and OpenDevelopments were reused read-only; no baseline rebuild or protected modification occurred. All successful reported theorem closures use only propext, Classical.choice, and Quot.sound, with some controls axiom-free. Exact source and object hashes, commands, exit codes, and log hashes are in REVIEW_RECEIPT.json and RETAINED_OBJECTS.json. The first trial encountered an outdated OpenDevelopments search path; this was corrected to the author's frozen reviewed path before the final reproducible run.
