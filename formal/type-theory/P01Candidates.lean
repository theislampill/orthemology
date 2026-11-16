/- Direct finite-source strong normalisation. Candidate membership is deliberately
   NOT closed under backwards conversion; canonical Code is left unchanged.
   Complete authored attempt-0003 proof candidate; UNCOMPILED at 4.19.0. -/
import P01TypeAlgebra
import P01SNReflection
import BoundaryResults
namespace P01Candidates
open OrthemologyV2 OrthemologyV3
open P01F (cons)
abbrev SN (t : Term) := Acc (fun u t => Step t u) t

def Neutral : Term → Prop
  | .i | .k | .s => False
  | .app .k _ | .app .s _ | .app (.app .s _) _ => False
  | _ => True

theorem neutral_app {f : Term} (h : Neutral f) (x) : Neutral (.app f x) := by
  cases f <;> simp_all [Neutral]
  case app a b => cases a <;> simp_all [Neutral]

theorem neutral_successor {f x u} (nf : Neutral f) (h : Step (.app f x) u) :
    (∃ g, Step f g ∧ u = .app g x) ∨
    (∃ y, Step x y ∧ u = .app f y) := by
  cases h with
  | i x => exact False.elim nf
  | k x y => exact False.elim nf
  | s f g x => exact False.elim nf
  | left h x => exact Or.inl ⟨_, h, rfl⟩
  | right f h => exact Or.inr ⟨_, h, rfl⟩

theorem sn_step {t u} (h : SN t) (r : Step t u) : SN u := h.inv r

theorem sn_red {t u} (h : SN t) (r : Red t u) : SN u := by
  induction r with
  | refl => exact h
  | tail s r ih => exact ih (sn_step h s)

theorem sn_function {f x} (h : SN (.app f x)) : SN f :=
  P01SNReflection.positive_simulation_reflects_SN Step Step
    (fun f => .app f x) (fun s => ⟨_, .left s x, .refl _⟩) h

structure Candidate where
  mem : Term → Prop
  normal : ∀ {t}, mem t → SN t
  descend : ∀ {t u}, mem t → Step t u → mem u
  expand : ∀ {t}, Neutral t → (∀ u, Step t u → mem u) → mem t

@[ext] theorem candidate_ext {P Q : Candidate} (h : ∀t, P.mem t ↔ Q.mem t) : P = Q := by
  have e : P.mem = Q.mem := funext fun t => propext (h t)
  cases P; cases Q; cases e; rfl

def snCandidate : Candidate where
  mem := SN
  normal := id
  descend := sn_step
  expand := fun _ h => Acc.intro _ h

theorem zero_mem (P : Candidate) : P.mem .zero := by
  apply P.expand (show Neutral .zero from True.intro)
  intro u h; cases h

theorem descend_red (P : Candidate) {t u} (h : P.mem t) (r : Red t u) : P.mem u := by
  induction r with
  | refl => exact h
  | tail s r ih => exact ih (P.descend h s)

def arrow (P Q : Candidate) : Candidate where
  mem := fun f => ∀ x, P.mem x → Q.mem (.app f x)
  normal := fun h => sn_function (Q.normal (h .zero (zero_mem P)))
  descend := fun h r x hx => Q.descend (h x hx) (.left r x)
  expand := by
    intro f nf hr x hx
    have aux : ∀ x, SN x → P.mem x → Q.mem (.app f x) := by
      intro x hs
      induction hs with
      | intro x next ih =>
          intro px
          apply Q.expand (neutral_app nf x)
          intro u hu
          rcases neutral_successor nf hu with ⟨g, hg, rfl⟩ | ⟨y, hy, rfl⟩
          · exact hr g hg x px
          · exact ih y hy (P.descend px hy)
    exact aux x (P.normal hx) hx

def intersection {ι : Type} (i₀ : ι) (F : ι → Candidate) : Candidate where
  mem := fun t => ∀ i, (F i).mem t
  normal := fun h => (F i₀).normal (h i₀)
  descend := fun h r i => (F i).descend (h i) r
  expand := fun nt hr i => (F i).expand nt (fun u r => hr u r i)

/-- Neutral redex inversion is proved in raw source theory. -/
theorem i_successor {x u} (h : Step (.app .i x) u) :
    u = x ∨ ∃ y, Step x y ∧ u = .app .i y := by
  cases h with
  | i x => exact Or.inl rfl
  | left h x => cases h
  | right f h => exact Or.inr ⟨_, h, rfl⟩

theorem k_successor {x y u} (h : Step (.app (.app .k x) y) u) :
    u = x ∨ (∃ x', Step x x' ∧ u = .app (.app .k x') y) ∨
      (∃ y', Step y y' ∧ u = .app (.app .k x) y') := by
  cases h with
  | k x y => exact Or.inl rfl
  | left h y =>
      cases h with
      | left h x => cases h
      | right k h => exact Or.inr (Or.inl ⟨_, h, rfl⟩)
  | right f h => exact Or.inr (Or.inr ⟨_, h, rfl⟩)

theorem s_successor {f g x u} (h : Step (.app (.app (.app .s f) g) x) u) :
    u = .app (.app f x) (.app g x) ∨
    (∃ f', Step f f' ∧ u = .app (.app (.app .s f') g) x) ∨
    (∃ g', Step g g' ∧ u = .app (.app (.app .s f) g') x) ∨
    (∃ x', Step x x' ∧ u = .app (.app (.app .s f) g) x') := by
  cases h with
  | s f g x => exact Or.inl rfl
  | left h x =>
      cases h with
      | left h g =>
          cases h with
          | left h f => cases h
          | right s h => exact Or.inr (Or.inl ⟨_, h, rfl⟩)
      | right sf h => exact Or.inr (Or.inr (Or.inl ⟨_, h, rfl⟩))
  | right sfg h => exact Or.inr (Or.inr (Or.inr ⟨_, h, rfl⟩))

theorem i_expand (P : Candidate) {x} (hx : P.mem x) : P.mem (.app .i x) := by
  have aux : ∀ x, SN x → P.mem x → P.mem (.app .i x) := by
    intro x hs
    induction hs with
    | intro x next ih =>
        intro px
        apply P.expand (show Neutral (.app .i x) from True.intro)
        intro u hu
        rcases i_successor hu with rfl | ⟨y, hy, rfl⟩
        · exact px
        · exact ih y hy (P.descend px hy)
  exact aux x (P.normal hx) hx

theorem k_expand (P : Candidate) {x y} (hx : P.mem x) (hy : SN y) :
    P.mem (.app (.app .k x) y) := by
  have aux : ∀ x, SN x → P.mem x → ∀ y, SN y → P.mem (.app (.app .k x) y) := by
    intro x hs
    induction hs with
    | intro x next ih =>
        intro px y hy
        induction hy with
        | intro y yn yi =>
            apply P.expand (show Neutral (.app (.app .k x) y) from True.intro)
            intro u hu
            rcases k_successor hu with rfl | ⟨x', hx', rfl⟩ | ⟨y', hy', rfl⟩
            · exact px
            · exact ih x' hx' (P.descend px hx') y (Acc.intro y yn)
            · exact yi y' hy'
  exact aux x (P.normal hx) hx y hy

theorem s_expand (P : Candidate) {f g x}
    (hf : SN f) (hg : SN g) (hx : SN x)
    (hp : P.mem (.app (.app f x) (.app g x))) :
    P.mem (.app (.app (.app .s f) g) x) := by
  have aux : ∀ f, SN f → ∀ g, SN g → ∀ x, SN x →
      P.mem (.app (.app f x) (.app g x)) →
      P.mem (.app (.app (.app .s f) g) x) := by
    intro f hf
    induction hf with
    | intro f fn fi =>
        intro g hg
        induction hg with
        | intro g gn gi =>
            intro x hx
            induction hx with
            | intro x xn xi =>
                intro hp
                apply P.expand (show Neutral (.app (.app (.app .s f) g) x) from True.intro)
                intro u hu
                rcases s_successor hu with rfl | ⟨f', hf', rfl⟩ |
                    ⟨g', hg', rfl⟩ | ⟨x', hx', rfl⟩
                · exact hp
                · exact fi f' hf' g (Acc.intro g gn) x (Acc.intro x xn)
                    (P.descend hp (.left (.left hf' x) (.app g x)))
                · exact gi g' hg' x (Acc.intro x xn)
                    (P.descend hp (.right (.app f x) (.left hg' x)))
                · exact xi x' hx' (P.descend
                    (P.descend hp (.left (.right f hx') (.app g x)))
                    (.right (.app f x') (.right g hx')))
  exact aux f hf g hg x hx hp

theorem i_member (P) : (arrow P P).mem .i := fun x hx => i_expand P hx

theorem k_member (P Q) : (arrow P (arrow Q P)).mem .k :=
  fun x hx y hy => k_expand P hx (Q.normal hy)

theorem s_member (P Q R) :
    (arrow (arrow P (arrow Q R)) (arrow (arrow P Q) (arrow P R))).mem .s := by
  intro f hf g hg x hx
  apply s_expand R ((arrow P (arrow Q R)).normal hf)
    ((arrow P Q).normal hg) (P.normal hx)
  exact hf x hx (.app g x) (hg x hx)

def interpret : TypeCode → (Nat → Candidate) → Candidate
  | .var n, ρ => ρ n
  | .bottom, _ => snCandidate
  | .arrow A B, ρ => arrow (interpret A ρ) (interpret B ρ)
  | .all B, ρ => intersection snCandidate (fun P => interpret B (cons P ρ))

theorem rename_interpret (A : TypeCode) : ∀ r ρ,
    interpret (rename r A) ρ = interpret A (fun n => ρ (r n)) := by
  induction A with
  | var n => intro r ρ; rfl
  | bottom => intro r ρ; rfl
  | arrow A B ha hb => intro r ρ; simp only [rename, interpret, ha, hb]
  | all B ih =>
      intro r ρ
      apply candidate_ext
      intro t
      change (∀ P, (interpret (rename (liftRen r) B) (cons P ρ)).mem t) ↔ _
      have e : ∀ P, (fun n => cons P ρ (liftRen r n)) =
          cons P (fun n => ρ (r n)) := by intro P; funext n; cases n <;> rfl
      simp only [ih, e]
      rfl

theorem substitute_interpret (A : TypeCode) : ∀ σ ρ,
    interpret (substitute σ A) ρ = interpret A (fun n => interpret (σ n) ρ) := by
  induction A with
  | var n => intro σ ρ; rfl
  | bottom => intro σ ρ; rfl
  | arrow A B ha hb => intro σ ρ; simp only [substitute, interpret, ha, hb]
  | all B ih =>
      intro σ ρ
      apply candidate_ext
      intro t
      change (∀ P, (interpret (substitute (upSub σ) B) (cons P ρ)).mem t) ↔ _
      have e : ∀ P, (fun n => interpret (upSub σ n) (cons P ρ)) =
          cons P (fun n => interpret (σ n) ρ) := by
        intro P; funext n
        cases n with
        | zero => rfl
        | succ n =>
            change interpret (rename Nat.succ (σ n)) (cons P ρ) = _
            rw [rename_interpret]; rfl
      simp only [ih, e]
      rfl

theorem instantiate_interpret (B A : TypeCode) (ρ : Nat → Candidate) :
    interpret (instantiateType B A) ρ = interpret B (cons (interpret A ρ) ρ) := by
  unfold instantiateType
  rw [substitute_interpret]
  apply congrArg (interpret B)
  funext n; cases n <;> rfl

/-- Direct reducibility interpretation covers every constructor, independently
    of the System-F route and without interpreting semantic Codes as candidates. -/
theorem finite_reducibility {t A} (h : FiniteDerives t A) :
    ∀ ρ, (interpret A ρ).mem t := by
  induction h with
  | i A => intro ρ; exact i_member _
  | k A B => intro ρ; exact k_member _ _
  | s A B C => intro ρ; exact s_member _ _ _
  | app hf hx ihf ihx => intro ρ; exact ihf ρ _ (ihx ρ)
  | allI h ih => intro ρ P; exact ih (cons P ρ)
  | allE h A ih => intro ρ; rw [instantiate_interpret]; exact ih ρ (interpret A ρ)
  | reduce h r ih => intro ρ; exact descend_red _ (ih ρ) r

theorem finite_SN {t A} (h : FiniteDerives t A) : SN t :=
  (interpret A (fun _ => snCandidate)).normal (finite_reducibility h _)
end P01Candidates
