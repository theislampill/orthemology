/- Exact finite-syntax soundness for the separate saturated-subset model.
   Formation and scope premises are retained in the source derivations; the
   interpretation is defined for all raw types and needs no semantic admission. -/
import IntensionalIdentityModel
import IntensionalIdentityBridge

namespace P01AC.Intensional
open OrthemologyV2 OrthemologyV3 P01D
open P01F (cons)

/-- Literal zero padding, with each declaration interpreted before its binder. -/
def V : Tel → SEnv → Env → Prop
  | [], _, η => η = zeroEnv
  | A :: Γ, ρ, η => V Γ ρ (tail η) ∧ mem A ρ (tail η) (η 0)

@[simp] theorem V_nil (ρ : SEnv) (η : Env) : V [] ρ η ↔ η = zeroEnv := Iff.rfl

@[simp] theorem V_cons (A : Ty) (Γ : Tel) (ρ : SEnv) (a : Term) (η : Env) :
    V (A :: Γ) ρ (cons a η) ↔ V Γ ρ η ∧ mem A ρ η a := Iff.rfl

private theorem interp_wk_tail (A : Ty) (ρ : SEnv) (η : Env) :
    interp (wk A) ρ η = interp A ρ (tail η) := by
  simpa only [cons_head_tail] using interp_wk A ρ (tail η) (η 0)

/-- Lookup uses the source's repeated weakening, rather than list access. -/
theorem lookup_member {Γ n A} (h : Lookup Γ n A) {ρ η} (v : V Γ ρ η) :
    mem A ρ η (η n) := by
  induction h generalizing η with
  | zero =>
      unfold mem
      rw [interp_wk_tail]
      exact v.2
  | succ h ih =>
      unfold mem
      rw [interp_wk_tail]
      exact ih v.1

/-- Type weakening changes no term coordinate, including the literal padding. -/
theorem V_twk (Γ : Tel) (ρ : SEnv) (η : Env) (X : Sat) :
    V (twkTel Γ) (cons X ρ) η ↔ V Γ ρ η := by
  induction Γ generalizing η with
  | nil => exact Iff.rfl
  | cons A Γ ih =>
      change (V (twkTel Γ) (cons X ρ) (tail η) ∧
        mem (twk A) (cons X ρ) (tail η) (η 0)) ↔ _
      simp only [mem, interp_twk, ih]
      rfl

/-- The unary fundamental property of a source polynomial. -/
def SemanticHas (Γ : Tel) (p : Poly) (A : Ty) : Prop :=
  ∀ (ρ : SEnv) (η : Env), V Γ ρ η → mem A ρ η (eval p η)

theorem fundamental_var {Γ n A} (h : Lookup Γ n A) : SemanticHas Γ (.var n) A :=
  fun _ _ v => lookup_member h v

theorem fundamental_i {Γ A} : SemanticHas Γ (.atom .i) (arr A A) := by
  intro ρ η v
  unfold mem
  rw [interp_arr]
  exact i_realises _

theorem fundamental_k {Γ A B} : SemanticHas Γ (.atom .k) (arr A (arr B A)) := by
  intro ρ η v
  unfold mem
  simp only [interp_arr]
  exact k_realises _ _

theorem fundamental_s {Γ A B C} :
    SemanticHas Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) := by
  intro ρ η v
  unfold mem
  simp only [interp_arr]
  exact s_realises _ _ _

/-- Actual finite imports are handled uniformly for arbitrary frozen images. -/
theorem fundamental_finite {Γ C t} (τ : List Ty) (h : FiniteDerives t C) :
    SemanticHas Γ (.atom t) (tsubst (typeImages τ) (fin C)) := by
  intro ρ η v
  exact finite_mem h τ ρ η

theorem fundamental_all_intro {Γ B p} (h : SemanticHas (twkTel Γ) p B) :
    SemanticHas Γ p (.all B) := by
  intro ρ η v X
  exact h (cons X ρ) η ((V_twk Γ ρ η X).mpr v)

theorem fundamental_all_elim {Γ B A p} (h : SemanticHas Γ p (.all B)) :
    SemanticHas Γ p (tinst B A) := by
  intro ρ η v
  unfold mem
  rw [interp_tinst]
  exact h ρ η v (interp A ρ η)

theorem fundamental_raw_atom {Γ t} : SemanticHas Γ (.atom t) .raw :=
  fun _ _ _ => True.intro

theorem fundamental_raw_app {Γ f a} : SemanticHas Γ (.app f a) .raw :=
  fun _ _ _ => True.intro

theorem fundamental_pi_intro {Γ A B b} (h : SemanticHas (A :: Γ) b B) :
    SemanticHas Γ (abstract b) (.pi A B) := by
  intro ρ η v a ha
  exact (code_conversion (interp B ρ (cons a η))
    (P01Source.red_conv (abstraction_beta b η a))).mpr (h ρ (cons a η) ⟨v,ha⟩)

theorem fundamental_pi_elim {Γ A B f a} (hf : SemanticHas Γ f (.pi A B))
    (ha : SemanticHas Γ a A) : SemanticHas Γ (.app f a) (inst B a) := by
  intro ρ η v
  unfold mem
  rw [interp_inst]
  exact hf ρ η v (eval a η) (ha ρ η v)

theorem fundamental_sigma_intro {Γ A B a b} (ha : SemanticHas Γ a A)
    (hb : SemanticHas Γ b (inst B a)) : SemanticHas Γ (pairPoly a b) (.sigma A B) := by
  intro ρ η v
  have bmem := hb ρ η v
  unfold mem at bmem
  rw [interp_inst] at bmem
  exact ⟨eval a η, eval b η, ha ρ η v, bmem, Conv.refl _⟩

theorem fundamental_sigma_fst {Γ A B z} (hz : SemanticHas Γ z (.sigma A B)) :
    SemanticHas Γ (fstPoly z) A := by
  intro ρ η v
  obtain ⟨a,b,ha,hb,hz⟩ := hz ρ η v
  have c : Conv (firstTerm (eval z η)) a :=
    .trans (Conv.left hz .k) (pair_first a b)
  exact (code_conversion (interp A ρ η) c).mpr ha

theorem fundamental_sigma_snd {Γ A B z} (hz : SemanticHas Γ z (.sigma A B)) :
    SemanticHas Γ (sndPoly z) (inst B (fstPoly z)) := by
  intro ρ η v
  obtain ⟨a,b,ha,hb,hz⟩ := hz ρ η v
  have cf : Conv (firstTerm (eval z η)) a :=
    .trans (Conv.left hz .k) (pair_first a b)
  have cs : Conv (secondTerm (eval z η)) b :=
    .trans (Conv.left hz (.app .k .i)) (pair_second a b)
  have ce : interp B ρ (cons (firstTerm (eval z η)) η) = interp B ρ (cons a η) := by
    apply interp_coherent
    intro n
    cases n with
    | zero => exact cf
    | succ n => exact Conv.refl _
  unfold mem
  rw [interp_inst, eval_fst, ce]
  exact (code_conversion (interp B ρ (cons a η)) cs).mpr hb

/-- A semantic conversion premise is used only after the syntactic conversion
    theorem has proved it for every valuation. -/
theorem fundamental_identity_intro {Γ A p q} (hp : SemanticHas Γ p A)
    (hq : SemanticHas Γ q A) (pq : ∀ η, Conv (eval p η) (eval q η)) :
    SemanticHas Γ (.atom .i) (.identity A p q) :=
  fun ρ η v => ⟨hp ρ η v,hq ρ η v,pq η,Conv.refl _⟩

theorem fundamental_proof_erase {Γ p} : SemanticHas Γ p .raw :=
  fun _ _ _ => True.intro

/-- Based J transports both the proof and endpoint coordinates, in that order. -/
theorem fundamental_j {Γ A B x y e d}
    (he : SemanticHas Γ e (.identity A x y))
    (hd : SemanticHas Γ d (motiveAt B x (.atom .i))) :
    SemanticHas Γ (jPoly d y e) (motiveAt B y e) := by
  intro ρ η v
  have hi := he ρ η v
  have base := hd ρ η v
  have ce : interp B ρ (cons (eval e η) (cons (eval y η) η)) =
      interp B ρ (cons .i (cons (eval x η) η)) := by
    apply interp_coherent
    intro n
    cases n with
    | zero => exact hi.2.2.2
    | succ n =>
        cases n with
        | zero => exact Conv.symm hi.2.2.1
        | succ n => exact Conv.refl _
  unfold mem at base ⊢
  rw [interp_motiveAt] at base ⊢
  rw [ce]
  exact (code_conversion _ (P01Source.red_conv (eval_j d y e η))).mpr base

theorem fundamental_conv {Γ A p q} (hp : SemanticHas Γ p A)
    (pq : ∀ η, Conv (eval p η) (eval q η)) : SemanticHas Γ q A := by
  intro ρ η v
  exact (code_conversion _ (pq η)).mp (hp ρ η v)

/-- All eighteen actual typing constructors, by their mutual recursor.
    The formation/context motives are True: no model-law assumption is input. -/
theorem has_sound {Γ p A} (h : Has Γ p A) : SemanticHas Γ p A := by
  induction h using Has.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun _ _ _ => True) with
  | nil => trivial
  | ext => trivial
  | param => trivial
  | bottom => trivial
  | all => trivial
  | raw => trivial
  | pi => trivial
  | sigma => trivial
  | identity => trivial
  | var hA hv a => exact fundamental_var hv
  | i hA ht a t => exact fundamental_i
  | k hA hB ht a b t => exact fundamental_k
  | s hA hB hC ht a b c t => exact fundamental_s
  | finite τ bound hτ hA hf a t => exact fundamental_finite τ hf
  | allIntro hAll hp a p => exact fundamental_all_intro p
  | allElim hAll hA hTarget hp a x t p => exact fundamental_all_elim p
  | rawAtom => exact fundamental_raw_atom
  | rawApp => exact fundamental_raw_app
  | piIntro hA hb hs a b => exact fundamental_pi_intro b
  | piElim hPi ht hf ha pi t f a => exact fundamental_pi_elim f a
  | sigmaIntro hSigma ht ha hb s t a b => exact fundamental_sigma_intro a b
  | sigmaFst hA hSigma hz a s z => exact fundamental_sigma_fst z
  | sigmaSnd hSigma ht hz s t z => exact fundamental_sigma_snd z
  | identityIntro hId hp hq pq a p q =>
      exact fundamental_identity_intro p q (P01DF.polyConv_sound pq)
  | proofErase => exact fundamental_proof_erase
  | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
      exact fundamental_j e d
  | conv hA hp pq hs a p => exact fundamental_conv p (P01DF.polyConv_sound pq)

/-- Closed identity inhabitation forces conversion of its typed endpoints. -/
theorem closed_identity_conversion {r A p q} (h : Has [] r (.identity A p q)) :
    Conv (eval p zeroEnv) (eval q zeroEnv) :=
  (has_sound h (fun _ => Code.bottom) zeroEnv rfl).2.2.1

/-- All eighteen hypothetical typing constructors, by their mutual recursor.
    The formation/context motives are True: no model-law assumption is input. -/
theorem hasPlus_sound {Γ p A} (h : Plus.HasPlus Γ p A) : SemanticHas Γ p A := by
  induction h using Plus.HasPlus.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun _ _ _ => True) with
  | nil => trivial
  | ext => trivial
  | param => trivial
  | bottom => trivial
  | all => trivial
  | raw => trivial
  | pi => trivial
  | sigma => trivial
  | identity => trivial
  | var hA hv a => exact fundamental_var hv
  | i hA ht a t => exact fundamental_i
  | k hA hB ht a b t => exact fundamental_k
  | s hA hB hC ht a b c t => exact fundamental_s
  | finite τ bound hτ hA hf a t => exact fundamental_finite τ hf
  | allIntro hAll hp a p => exact fundamental_all_intro p
  | allElim hAll hA hTarget hp a x t p => exact fundamental_all_elim p
  | rawAtom => exact fundamental_raw_atom
  | rawApp => exact fundamental_raw_app
  | piIntro hA hb hs a b => exact fundamental_pi_intro b
  | piElim hPi ht hf ha pi t f a => exact fundamental_pi_elim f a
  | sigmaIntro hSigma ht ha hb s t a b => exact fundamental_sigma_intro a b
  | sigmaFst hA hSigma hz a s z => exact fundamental_sigma_fst z
  | sigmaSnd hSigma ht hz s t z => exact fundamental_sigma_snd z
  | identityIntro hId hp hq pq a p q =>
      exact fundamental_identity_intro p q (Plus.polyConvPlus_sound pq)
  | proofErase => exact fundamental_proof_erase
  | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
      exact fundamental_j e d
  | conv hA hp pq hs a p => exact fundamental_conv p (Plus.polyConvPlus_sound pq)

/-- The bridge extension retains the same closed-identity reflection. -/
theorem plus_closed_identity_conversion {r A p q}
    (h : Plus.HasPlus [] r (.identity A p q)) :
    Conv (eval p zeroEnv) (eval q zeroEnv) :=
  (hasPlus_sound h (fun _ => Code.bottom) zeroEnv rfl).2.2.1

end P01AC.Intensional
