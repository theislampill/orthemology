/- Literal positive controls for the syntax-generated typed telescope nucleus.
   The raw I/SKK obstruction is inherited unchanged. -/
import AllStructural
import AllSoundness
import P01DependentControls

namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- The finite parameter leaf from the frozen design. -/
def alpha : Ty := fin (.var 0)

def typedPair : Poly := pairPoly (.var 0) (.atom .i)
def typedPairType : Ty := .sigma alpha (.identity alpha (.var 1) (.var 0))

private theorem constant_carrier_pair_form (A : Ty)
    (hA : ∀ Γ, Ctx Γ → Form Γ A) (hw : wk A = A) :
    Form [A] (.sigma A (.identity A (.var 1) (.var 0))) := by
  have c1 : Ctx [A] := .ext .nil (hA [] .nil)
  have c2 : Ctx [A,A] := .ext c1 (hA [A] c1)
  have v0 : Has [A,A] (.var 0) A :=
    .var (hA [A,A] c2) (by simpa only [hw] using (Lookup.zero (A := A) (Γ := [A])))
  have v1 : Has [A,A] (.var 1) A :=
    .var (hA [A,A] c2) (by simpa only [hw] using
      (Lookup.succ (B := A) (Lookup.zero (A := A) (Γ := []))))
  exact .sigma (hA [A] c1) (.identity (hA [A,A] c2) v1 v0)

private theorem constant_carrier_pair_has (A : Ty)
    (hA : ∀ Γ, Ctx Γ → Form Γ A) (hs : ∀ σ, subst σ A = A) :
    Has [A] typedPair (.sigma A (.identity A (.var 1) (.var 0))) := by
  have hw : wk A = A := hs _
  have c1 : Ctx [A] := .ext .nil (hA [] .nil)
  have v0 : Has [A] (.var 0) A :=
    .var (hA [A] c1) (by simpa only [hw] using (Lookup.zero (A := A) (Γ := [])))
  have hId : Form [A] (.identity A (.var 0) (.var 0)) :=
    .identity (hA [A] c1) v0 v0
  have hInst : inst (.identity A (.var 1) (.var 0)) (.var 0) =
      .identity A (.var 0) (.var 0) := by
    simp only [inst, subst, hs, psub, cons]
  apply Has.sigmaIntro (constant_carrier_pair_form A hA hw)
  · rw [hInst]; exact hId
  · exact v0
  · rw [hInst]
    exact .identityIntro hId v0 v0 (.refl _)

theorem typed_pair_form : Form [alpha] typedPairType :=
  constant_carrier_pair_form alpha (fun _ h => .param h) rfl

/-- The displayed open pair has a finite syntactic derivation. -/
theorem typed_pair_has : Has [alpha] (pairPoly (.var 0) (.atom .i)) typedPairType :=
  constant_carrier_pair_has alpha (fun _ h => .param h) (fun _ => rfl)

theorem typed_pair_abstraction_form : Form [] (.pi alpha typedPairType) :=
  .pi (.param .nil) typed_pair_form

/-- Literal bracket abstraction, with no new object-language All binder. -/
theorem typed_pair_abstraction_has :
    Has [] (abstract (pairPoly (.var 0) (.atom .i))) (.pi alpha typedPairType) :=
  .piIntro typed_pair_abstraction_form typed_pair_has
    (scoped_abstract (scoped_pair (by exact Nat.zero_lt_succ 0) trivial))

/-- The pair theorem is uniformly heterogeneous, for arbitrary PER parameters. -/
theorem typed_pair_related (r : REnv) (x y : Term) (hxy : r.rel 0 x y) :
    G typedPairType r (cons x zeroEnv) (cons y zeroEnv)
      (pairTerm x .i) (pairTerm y .i) :=
  fundamental typed_pair_has r _ _ ⟨⟨rfl,rfl⟩,hxy⟩

theorem typed_pair_abstraction_related (r : REnv) :
    G (.pi alpha typedPairType) r zeroEnv zeroEnv
      (eval (abstract typedPair) zeroEnv) (eval (abstract typedPair) zeroEnv) :=
  fundamental typed_pair_abstraction_has r _ _ ⟨rfl,rfl⟩

/- The literal two-coordinate J example from design section 6. -/
def jContext : Tel := [.identity alpha (.var 1) (.var 0), alpha, alpha]
def jProofType : Ty := .identity alpha (.var 2) (.var 1)
def jMotive : Ty :=
  .sigma (.identity alpha (.var 4) (.var 1))
    (.identity .raw (.var 1) (.atom .i))
def jBaseType : Ty :=
  .sigma (.identity alpha (.var 2) (.var 2))
    (.identity .raw (.atom .i) (.atom .i))
def jTargetType : Ty :=
  .sigma (.identity alpha (.var 2) (.var 1))
    (.identity .raw (.var 1) (.atom .i))
def jBase : Poly := pairPoly (.atom .i) (.atom .i)
def literalJ : Poly := jPoly jBase (.var 1) (.var 0)

theorem j_context_formed : Ctx jContext := by
  have c1 : Ctx [alpha] := .ext .nil (.param .nil)
  have c2 : Ctx [alpha,alpha] := .ext c1 (.param c1)
  exact .ext c2 (.identity (.param c2)
    (.var (.param c2) (.succ .zero)) (.var (.param c2) .zero))

theorem j_x_has : Has jContext (.var 2) alpha :=
  .var (.param j_context_formed) (.succ (.succ .zero))

theorem j_y_has : Has jContext (.var 1) alpha :=
  .var (.param j_context_formed) (.succ .zero)

theorem j_proof_form : Form jContext jProofType :=
  .identity (.param j_context_formed) j_x_has j_y_has

theorem j_e_has : Has jContext (.var 0) jProofType :=
  .var j_proof_form .zero

private theorem raw_identity_from_proof {Γ : Tel} {A : Ty} {x y p : Poly}
    (hΓ : Ctx Γ) (hId : Form Γ (.identity A x y))
    (hp : Has Γ p (.identity A x y)) :
    Form Γ (.identity .raw p (.atom .i)) :=
  .identity (.raw hΓ) (.proofErase (.raw hΓ) hId hp) (.rawAtom (.raw hΓ))

theorem j_motive_form : Form (theta jContext alpha (.var 2)) jMotive := by
  let Θ := theta jContext alpha (.var 2)
  have hΘ : Ctx Θ := ctx_theta j_context_formed (.param j_context_formed) j_x_has
  have hx : Has Θ (.var 4) alpha :=
    .var (.param hΘ) (.succ (.succ (.succ (.succ .zero))))
  have hy : Has Θ (.var 1) alpha := .var (.param hΘ) (.succ .zero)
  have hP : Form Θ (.identity alpha (.var 4) (.var 1)) :=
    .identity (.param hΘ) hx hy
  have hz : Has Θ (.var 0) (.identity alpha (.var 4) (.var 1)) := .var hP .zero
  have hBody := raw_identity_from_proof (.ext hΘ hP)
    (form_wk hP hΘ hP) (has_wk hz hΘ hP)
  exact .sigma hP hBody

/-- Both motive coordinates are substituted literally, including the Sigma binder. -/
theorem j_motive_base_exact :
    motiveAt jMotive (.var 2) (.atom .i) = jBaseType := rfl

theorem j_motive_target_exact :
    motiveAt jMotive (.var 1) (.var 0) = jTargetType := rfl

theorem j_base_form : Form jContext jBaseType := by
  have hP : Form jContext (.identity alpha (.var 2) (.var 2)) :=
    .identity (.param j_context_formed) j_x_has j_x_has
  have c := Ctx.ext j_context_formed hP
  exact .sigma hP (.identity (.raw c) (.rawAtom (.raw c)) (.rawAtom (.raw c)))

theorem j_target_form : Form jContext jTargetType := by
  have hBody := raw_identity_from_proof (.ext j_context_formed j_proof_form)
    (form_wk j_proof_form j_context_formed j_proof_form)
    (has_wk j_e_has j_context_formed j_proof_form)
  exact .sigma j_proof_form hBody

theorem j_base_has : Has jContext jBase jBaseType := by
  have hP : Form jContext (.identity alpha (.var 2) (.var 2)) :=
    .identity (.param j_context_formed) j_x_has j_x_has
  have hi : Has jContext (.atom .i) (.identity alpha (.var 2) (.var 2)) :=
    .identityIntro hP j_x_has j_x_has (.refl _)
  have hR : Form jContext (.identity .raw (.atom .i) (.atom .i)) :=
    .identity (.raw j_context_formed) (.rawAtom (.raw j_context_formed))
      (.rawAtom (.raw j_context_formed))
  exact .sigmaIntro j_base_form hR hi
    (.identityIntro hR (.rawAtom (.raw j_context_formed))
      (.rawAtom (.raw j_context_formed)) (.refl _))

/-- Syntactic J at exactly the endpoint-and-proof-dependent displayed target. -/
theorem literal_j_has : Has jContext literalJ jTargetType := by
  have hBase : Form jContext (motiveAt jMotive (.var 2) (.atom .i)) := j_base_form
  have hTarget : Form jContext (motiveAt jMotive (.var 1) (.var 0)) := j_target_form
  exact .j (.param j_context_formed) j_motive_form j_proof_form
    hBase hTarget j_x_has j_y_has j_e_has j_base_has

theorem literal_j_related : Fundamental jContext literalJ jTargetType :=
  fundamental literal_j_has

/- Two raw fibres are both inhabited, yet extensionally different. -/
def rawFibreType : Ty := .sigma .raw (.identity .raw (.var 1) (.var 0))

theorem raw_fibre_form : Form [.raw] rawFibreType :=
  constant_carrier_pair_form .raw (fun _ h => .raw h) rfl

theorem raw_fibre_pair_has : Has [.raw] typedPair rawFibreType :=
  constant_carrier_pair_has .raw (fun _ h => .raw h) (fun _ => rfl)

theorem raw_fibre_inhabited (ρ : OEnv) (x : Term) :
    F rawFibreType ρ (cons x zeroEnv) (pairTerm x .i) (pairTerm x .i) :=
  unary_fundamental raw_fibre_pair_has (η := cons x zeroEnv) (ξ := cons x zeroEnv)
    ⟨⟨rfl,rfl⟩,Conv.refl x⟩

/-- In particular, the I and SKK fibres are nonempty, but not equal relations. -/
theorem raw_fibres_nonempty_and_vary (ρ : OEnv) :
    F rawFibreType ρ (cons .i zeroEnv) (pairTerm .i .i) (pairTerm .i .i) ∧
    F rawFibreType ρ (cons P01DF.skk zeroEnv)
      (pairTerm P01DF.skk .i) (pairTerm P01DF.skk .i) ∧
    ¬ F rawFibreType ρ (cons P01DF.skk zeroEnv) (pairTerm .i .i) (pairTerm .i .i) := by
  refine ⟨raw_fibre_inhabited ρ .i,raw_fibre_inhabited ρ P01DF.skk,?_⟩
  intro h
  have hbad : Conv P01DF.skk (firstTerm (pairTerm .i .i)) := h.2.2.2.1
  exact P01Source.I_SKK_not_convertible (hbad.trans (pair_first .i .i)).symm

/- The accepted non-raw-refining identity PER is a positive typed control. -/
def identityParameters (ρ : OEnv) : OEnv := fun _ => (P01R.interpret identityCode).obj ρ

theorem identity_parameters_I_SKK (ρ : OEnv) :
    (identityParameters ρ 0).rel .i P01DF.skk :=
  ((P01R.interpret identityCode).identity ρ _ _).mp
    (recursive_polymorphic_I_skk (diagEnv ρ))

/-- The endpoint changes from I to SKK, and the proof changes from I to I I. -/
def concreteJEnv : Env :=
  cons (.app .i .i) (cons P01DF.skk (cons .i zeroEnv))

theorem concrete_j_environment_related (ρ : OEnv) :
    E jContext (identityParameters ρ) concreteJEnv concreteJEnv := by
  have h := identity_parameters_I_SKK ρ
  exact ⟨⟨⟨⟨rfl,rfl⟩,PER.left h⟩,PER.right h⟩,
    h,Conv.step (.i .i),Conv.step (.i .i)⟩

/-- The exact J derivation works at a non-raw-refining carrier and a genuinely
    nonliteral reflexivity proof, exercising both motive coordinates. -/
theorem concrete_j_nonraw_proof_control (ρ : OEnv) :
    F jTargetType (identityParameters ρ) concreteJEnv
      (eval literalJ concreteJEnv) (eval literalJ concreteJEnv) ∧
    ¬ Conv (concreteJEnv 2) (concreteJEnv 1) ∧
    Conv (concreteJEnv 0) .i ∧ concreteJEnv 0 ≠ .i := by
  refine ⟨?_,P01Source.I_SKK_not_convertible,Conv.step (.i .i),?_⟩
  · exact unary_fundamental literal_j_has (concrete_j_environment_related ρ)
  · intro h
    cases h

theorem typed_pair_I_SKK_related (ρ : OEnv) :
    G typedPairType (diagEnv (identityParameters ρ))
      (cons .i zeroEnv) (cons P01DF.skk zeroEnv)
      (pairTerm .i .i) (pairTerm P01DF.skk .i) :=
  typed_pair_related _ _ _ (identity_parameters_I_SKK ρ)

/-- The positive typed pair does not identify source conversion with PER equality. -/
theorem typed_pair_I_SKK_control (ρ : OEnv) :
    G typedPairType (diagEnv (identityParameters ρ))
      (cons .i zeroEnv) (cons P01DF.skk zeroEnv)
      (pairTerm .i .i) (pairTerm P01DF.skk .i) ∧ ¬ Conv .i P01DF.skk :=
  ⟨typed_pair_I_SKK_related ρ,P01Source.I_SKK_not_convertible⟩

/-- Exactly the old raw family obstruction; no arbitrary-link transport is added. -/
theorem mandatory_raw_family_obstruction_unchanged (ρ : OEnv) :
    ∃ (P Q : PER) (R : Link P Q) (x y : Term), R.rel x y ∧
      (IdPER rawPER x .i).dom .i ∧ ¬ (IdPER rawPER y .i).dom .i :=
  P01DF.heterogeneous_index_transport_fails ρ

end P01AC
