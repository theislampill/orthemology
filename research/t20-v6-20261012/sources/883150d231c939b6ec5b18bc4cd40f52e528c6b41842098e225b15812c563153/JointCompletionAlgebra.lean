import JointSyntax

namespace JointCompletion.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open SigmaCompletion RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem trename_N (r : Nat → Nat) : trename r N = N := rfl

theorem trename_branchType (P : Ty) (r : Nat → Nat) :
    trename r (branchType P) = branchType (trename r P) :=
  (subst_trename P SigmaCompletion.pairSub r).symm

theorem trename_dependentStepType (P : Ty) (r : Nat → Nat) :
    trename r (dependentStepType P) = dependentStepType (trename r P) := by
  simp only [dependentStepType, trename, trename_N, trename_arr, successorFamily,
    subst_trename]

theorem branchAt_scoped {n : Nat} {d a b : Poly}
    (hd : Scoped (n+2) d) (ha : Scoped n a) (hb : Scoped n b) :
    Scoped n (branchAt d a b) :=
  scoped_subst hd (scopedSub_cons hb (scopedSub_cons ha (scopedSub_id n)))

theorem zero_subst (σ : Nat → Poly) : psub σ SourceRigidity.zero = SourceRigidity.zero :=
  P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped (inputNumeral_has 0)) σ

theorem zero_scoped (n : Nat) : Scoped n SourceRigidity.zero :=
  scoped_mono (P01AC.has_scoped (inputNumeral_has 0)) (Nat.zero_le n)

theorem succPoly_scoped (n : Nat) : Scoped n succPoly :=
  scoped_mono (P01AC.has_scoped succ_has) (Nat.zero_le n)

theorem sectionBody_scoped {k : Nat} {p s n : Poly}
    (hp : Scoped k p) (hs : Scoped k s) (hn : Scoped k n) :
    Scoped k (sectionBody p s n) := by
  apply scoped_snd
  refine ⟨⟨hn, ?_⟩, scoped_pair (zero_scoped k) hp⟩
  apply scoped_abstract
  apply scoped_pair
  · exact ⟨succPoly_scoped (k+1), scoped_fst (Nat.zero_lt_succ k)⟩
  · exact ⟨⟨scoped_wk hs, scoped_fst (Nat.zero_lt_succ k)⟩,
      scoped_snd (Nat.zero_lt_succ k)⟩

theorem sectionPoly_scoped {k : Nat} {p s : Poly}
    (hp : Scoped k p) (hs : Scoped k s) : Scoped k (sectionPoly p s) :=
  scoped_abstract (sectionBody_scoped (scoped_wk hp) (scoped_wk hs) (Nat.zero_lt_succ k))

theorem branchType_subst (P : Ty) (σ : Nat → Poly) :
    subst (pup (pup σ)) (branchType P) = branchType (subst (pup σ) P) := by
  simp only [branchType, subst_comp]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
    simp only [pairSub, pup, cons, psub, pren, psub_comp]

theorem branchAt_subst (d a b : Poly) (σ : Nat → Poly) :
    psub σ (branchAt d a b) =
      branchAt (psub (pup (pup σ)) d) (psub σ a) (psub σ b) := by
  simp only [branchAt, psub_comp]
  congr 1
  funext n
  cases n with
  | zero => rfl
  | succ n =>
    cases n with
    | zero => rfl
    | succ n =>
      change σ n = psub (cons (psub σ b) (cons (psub σ a) Poly.var))
        (pren Nat.succ (pren Nat.succ (σ n)))
      rw [P01DF.Syntactic.polynomial_shift_cancel,
        P01DF.Syntactic.polynomial_shift_cancel, psub_id]

theorem successorFamily_subst (P : Ty) (σ : Nat → Poly) :
    subst (pup σ) (successorFamily P) = successorFamily (subst (pup σ) P) := by
  simp only [successorFamily, subst_comp]
  congr 1
  funext n
  cases n with
  | zero =>
    simp only [cons, pup, psub,
      P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)]
  | succ n =>
    simp only [cons, pup, psub, pren, psub_comp]

theorem dependentStepType_subst (P : Ty) (σ : Nat → Poly) :
    subst σ (dependentStepType P) = dependentStepType (subst (pup σ) P) := by
  simp only [dependentStepType, subst, N_subst, subst_arr, successorFamily_subst]

theorem nextIndex_subst (σ : Nat → Poly) : psub (pup σ) nextIndex = nextIndex := by
  simp only [nextIndex, fstPoly, psub, pup,
    P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)]

theorem totalStep_subst (d : Poly) (σ : Nat → Poly) :
    psub σ (totalStep d) = totalStep (psub (pup σ) d) := by
  rw [totalStep, ← abstraction_naturality]
  simp only [P01DF.Syntactic.polynomial_pair, nextIndex_subst]
  rfl

theorem uncurriedStep_subst (s : Poly) (σ : Nat → Poly) :
    psub (pup σ) (uncurriedStep s) = uncurriedStep (psub σ s) := by
  simp only [uncurriedStep, psub, fstPoly, sndPoly, pup,
    P01DF.Syntactic.polynomial_shift_substitution]

theorem totalSeed_subst (p : Poly) (σ : Nat → Poly) :
    psub σ (totalSeed p) = totalSeed (psub σ p) := by
  simp only [totalSeed, P01DF.Syntactic.polynomial_pair,
    P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped (inputNumeral_has 0))]

theorem sectionBody_subst (p s n : Poly) (σ : Nat → Poly) :
    psub σ (sectionBody p s n) = sectionBody (psub σ p) (psub σ s) (psub σ n) := by
  simp only [sectionBody, sndPoly, psub, totalStep_subst, uncurriedStep_subst,
    totalSeed_subst]

theorem sectionPoly_subst (p s : Poly) (σ : Nat → Poly) :
    psub σ (sectionPoly p s) = sectionPoly (psub σ p) (psub σ s) := by
  rw [sectionPoly, ← abstraction_naturality]
  simp only [sectionBody_subst, P01DF.Syntactic.polynomial_shift_substitution, psub, pup]
  rfl

/-- Term-variable renaming is the variable-image special case of substitution. -/
theorem branchType_rename (P : Ty) (r : Nat → Nat) :
    subst (renSub (liftRen (liftRen r))) (branchType P) =
      branchType (subst (renSub (liftRen r)) P) := by
  simpa only [renSub_lift] using branchType_subst P (renSub r)

theorem branchAt_rename (d a b : Poly) (r : Nat → Nat) :
    pren r (branchAt d a b) =
      branchAt (pren (liftRen (liftRen r)) d) (pren r a) (pren r b) := by
  change psub (renSub r) (branchAt d a b) =
    branchAt (psub (renSub (liftRen (liftRen r))) d) (psub (renSub r) a) (psub (renSub r) b)
  simpa only [renSub_lift] using branchAt_subst d a b (renSub r)

theorem dependentStepType_rename (P : Ty) (r : Nat → Nat) :
    subst (renSub r) (dependentStepType P) =
      dependentStepType (subst (renSub (liftRen r)) P) := by
  simpa only [renSub_lift] using dependentStepType_subst P (renSub r)

theorem sectionPoly_rename (p s : Poly) (r : Nat → Nat) :
    pren r (sectionPoly p s) = sectionPoly (pren r p) (pren r s) :=
  sectionPoly_subst p s (renSub r)

#print axioms trename_N
#print axioms trename_branchType
#print axioms trename_dependentStepType
#print axioms branchAt_scoped
#print axioms sectionPoly_scoped
#print axioms branchType_subst
#print axioms branchAt_subst
#print axioms dependentStepType_subst
#print axioms sectionPoly_subst
#print axioms branchType_rename
#print axioms branchAt_rename
#print axioms dependentStepType_rename
#print axioms sectionPoly_rename

end JointCompletion.Structural
