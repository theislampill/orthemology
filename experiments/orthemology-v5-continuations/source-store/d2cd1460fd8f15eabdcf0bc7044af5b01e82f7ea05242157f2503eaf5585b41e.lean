/- A separate post-seal projection to unchanged canonical unary Code.
   Exact squares are restricted to the constructors/premises proved below. -/
import P01DependentRepresentation
namespace P01DF
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- Forget relational equality, retaining exactly the PER's domain. -/
def carrierCode (P : PER) : Code where
  accepts := P.dom
  stable := by
    intro t u h
    exact ⟨fun ht => P.raw (.step h) (.step h) ht,
      fun hu => P.raw (.symm (.step h)) (.symm (.step h)) hu⟩

theorem carrier_code_ext {A B : Code} (h : ∀ t, A.accepts t ↔ B.accepts t) : A = B := by
  have he : A.accepts = B.accepts := funext fun t => propext (h t)
  cases A; cases B; cases he; rfl

theorem raw_carrier_is_top : carrierCode rawPER = Code.top := by
  apply carrier_code_ext
  intro t
  exact ⟨fun _ => True.intro,fun _ => Conv.refl t⟩

def carrierFamily (B : Term → PER) (h : ∀ {x y}, Conv x y → B x = B y) : CoherentFamily where
  fibre := fun x => carrierCode (B x)
  coherent := by
    intro x y hxy t
    rw [h hxy]

/-- A raw-domain Pi imposes no additional cross-argument equality beyond its
    unary dependent Code: related arguments are raw-convertible. -/
theorem raw_pi_carrier_square (B : Term → PER)
    (h : ∀ {x y}, Conv x y → B x = B y) :
    carrierCode (PiPER rawPER B h) = dependentPi (carrierCode rawPER) (carrierFamily B h) := by
  apply carrier_code_ext
  intro f
  constructor
  · intro hf x hx
    exact hf x x hx
  · intro hf x y hxy
    exact (B x).raw (.refl _) (Conv.right f hxy) (hf x (.refl _))

/-- Sigma's represented-pair carrier square is valid for an arbitrary domain
    PER when both its PER coherence and global raw coherence are supplied. -/
theorem sigma_carrier_square (P : PER) (B : Term → PER)
    (hp : ∀ {x y}, P.rel x y → B x = B y)
    (hc : ∀ {x y}, Conv x y → B x = B y) :
    carrierCode (SigmaPER P B hp) = dependentSigma (carrierCode P) (carrierFamily B hc) := by
  apply carrier_code_ext
  intro z
  constructor
  · intro hz
    exact ⟨firstTerm z,secondTerm z,hz.2.2.1,hz.2.2.2,hz.1⟩
  · rintro ⟨x,y,hx,hy,hz⟩
    exact (SigmaPER P B hp).raw hz.symm hz.symm (sigma_pair hx hy)

theorem raw_sigma_carrier_square (B : Term → PER)
    (h : ∀ {x y}, Conv x y → B x = B y) :
    carrierCode (SigmaPER rawPER B h) =
      dependentSigma (carrierCode rawPER) (carrierFamily B h) :=
  sigma_carrier_square rawPER B h h

theorem raw_identity_carrier_square (x y : Term) :
    carrierCode (IdPER rawPER x y) = equalityCode (carrierCode rawPER) x y := by
  apply carrier_code_ext
  intro p
  constructor
  · intro h; exact ⟨.refl _,.refl _,h.1,h.2.1⟩
  · intro h; exact ⟨h.2.2.1,h.2.2.2,h.2.2.2⟩

def projectedBody (ρ : OEnv) (η : Env) (B : Ty) : CoherentFamily :=
  carrierFamily (fun x => ((interpret B).run (cons x η)).obj ρ)
    (fun h => congrArg (fun M : Model => M.obj ρ)
      (interpret_index_transport B (index_cons (index_refl η) h)))

/-- Literal canonical dependentPi of the projected, syntactically generated
    fibres. No global equality for every constructor is implied. -/
theorem syntax_pi_carrier_square (ρ : OEnv) (η : Env) (B : Ty) :
    carrierCode (((interpret (.pi B)).run η).obj ρ) =
      dependentPi Code.top (projectedBody ρ η B) := by
  have he := raw_pi_carrier_square
    (fun x => ((interpret B).run (cons x η)).obj ρ)
    (fun h => congrArg (fun M : Model => M.obj ρ)
      (interpret_index_transport B (index_cons (index_refl η) h)))
  rw [raw_carrier_is_top] at he
  exact he

theorem syntax_sigma_carrier_square (ρ : OEnv) (η : Env) (B : Ty) :
    carrierCode (((interpret (.sigma B)).run η).obj ρ) =
      dependentSigma Code.top (projectedBody ρ η B) := by
  have he := raw_sigma_carrier_square
    (fun x => ((interpret B).run (cons x η)).obj ρ)
    (fun h => congrArg (fun M : Model => M.obj ρ)
      (interpret_index_transport B (index_cons (index_refl η) h)))
  rw [raw_carrier_is_top] at he
  exact he

theorem syntax_identity_carrier_square (ρ : OEnv) (η : Env) (p q : Poly) :
    carrierCode (((interpret (.identity p q)).run η).obj ρ) =
      equalityCode Code.top (eval p η) (eval q η) := by
  change carrierCode (IdPER rawPER _ _) = _
  rw [raw_identity_carrier_square,raw_carrier_is_top]

/-- This is a source-preserving admission theorem to actual canonical Code,
    with exactly the unchanged compiled source term. -/
theorem canonical_pi_admission {p B} (h : Has p (.pi B)) (ρ : OEnv) (η : Env) :
    (dependentPi Code.top (projectedBody ρ η B)).accepts (eval p η) := by
  rw [← syntax_pi_carrier_square]
  exact unary_soundness h ρ η

theorem canonical_sigma_admission {p B} (h : Has p (.sigma B)) (ρ : OEnv) (η : Env) :
    (dependentSigma Code.top (projectedBody ρ η B)).accepts (eval p η) := by
  rw [← syntax_sigma_carrier_square]
  exact unary_soundness h ρ η

theorem canonical_identity_admission {p x y} (h : Has p (.identity x y)) (ρ : OEnv) (η : Env) :
    (equalityCode Code.top (eval x η) (eval y η)).accepts (eval p η) := by
  rw [← syntax_identity_carrier_square ρ]
  exact unary_soundness h ρ η

/-- General arrows forget a substantive relational extensionality condition. -/
theorem arrow_carrier_inclusion (P Q : PER) {f : Term}
    (h : (carrierCode (ArrPER P Q)).accepts f) :
    (Code.arrow (carrierCode P) (carrierCode Q)).accepts f :=
  fun x hx => h x x hx

theorem arbitrary_arrow_reverse_projection_fails :
    ∃ (P Q : PER) (f : Term),
      (Code.arrow (carrierCode P) (carrierCode Q)).accepts f ∧
      ¬ (carrierCode (ArrPER P Q)).accepts f := by
  refine ⟨totalPER,rawPER,.i,?_,?_⟩
  · intro x hx; exact Conv.refl _
  · intro h
    have he := h .i skk True.intro
    exact P01Source.I_SKK_not_convertible
      ((Conv.step (.i .i)).symm.trans (he.trans (Conv.step (.i skk))))

/-- Conversely, canonical raw equality always implies PER identity after
    forgetting, but relational identity need not imply raw equality. -/
theorem canonical_identity_inclusion (P : PER) {x y p : Term}
    (h : (equalityCode (carrierCode P) x y).accepts p) :
    (carrierCode (IdPER P x y)).accepts p :=
  ⟨P.raw (.refl _) h.2.2.1 h.1,h.2.2.2,h.2.2.2⟩

theorem arbitrary_identity_forward_projection_fails (ρ : OEnv) :
    ∃ (P : PER) (x y p : Term),
      (carrierCode (IdPER P x y)).accepts p ∧
      ¬ (equalityCode (carrierCode P) x y).accepts p := by
  let P := (P01R.interpret identityCode).obj ρ
  have hxy : P.rel .i skk := ((P01R.interpret identityCode).identity ρ _ _).mp
    (recursive_polymorphic_I_skk (diagEnv ρ))
  refine ⟨P,.i,skk,.i,⟨hxy,.refl _,.refl _⟩,?_⟩
  intro h
  exact P01Source.I_SKK_not_convertible h.2.2.1

end P01DF
