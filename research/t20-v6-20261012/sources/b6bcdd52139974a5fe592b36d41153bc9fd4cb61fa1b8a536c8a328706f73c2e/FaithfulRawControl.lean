import CaseOperational

/- Additional scope diagnostic only. The homogeneous model and frozen core are
   unchanged. This specific witness nu fails if conversion itself is quantified. -/
namespace FaithfulRawControl
open CaseOperational
infixl:70 " @@ " => T.app

set_option maxHeartbeats 1000000

def skk : T := .s @@ .k @@ .k
def seed : T := .a0 @@ .a0

def Arrow (R S : T → T → Prop) (f g : T) : Prop :=
  ∀ x y, R x y → S (f @@ x) (g @@ y)

theorem skk_beta (x : T) : Conv (skk @@ x) x :=
  .trans (.s .k .k x) (.k x (.k @@ x))

/-- The input endomaps are related at the conversion arrow even though
    their unapplied raw normal forms are different. -/
theorem i_skk_arrow : Arrow Conv Conv .i skk := by
  intro x y hxy
  exact .trans (.i x) (.trans hxy (.symm (skk_beta y)))

def Normal (t : T) : Prop := ∀ u, ¬ Step t u

theorem i_normal : Normal .i := by intro u h; cases h

theorem skk_normal : Normal skk := by
  intro u h
  cases h with
  | left h _ =>
      cases h with
      | left h _ => cases h
      | right _ h => cases h
  | right _ h => cases h

theorem seed_normal : Normal seed := by
  intro u h
  cases h with
  | left h _ => cases h
  | right _ h => cases h

/-- The stuck atom application matches none of the ten nu case rules. -/
theorem nu_seed_normal {f : T} (hf : Normal f) : Normal (.nu @@ f @@ seed) := by
  intro u h
  cases h with
  | nuF _ hv => cases hv
  | left h _ =>
      cases h with
      | left h _ => cases h
      | right _ h => exact hf _ h
  | right _ h => exact seed_normal _ h

theorem normal_red {t u : T} (ht : Normal t) (h : Red t u) : u = t := by
  cases h with
  | refl => rfl
  | tail hs _ => exact False.elim (ht _ hs)

theorem normal_convertible_equal {t u : T} (ht : Normal t) (hu : Normal u)
    (h : Conv t u) : t = u := by
  obtain ⟨w, htw, huw⟩ := conv_join h
  exact (normal_red ht htw).symm.trans (normal_red hu huw)

/-- Concrete failure of extensionality on the faithful Raw carrier. -/
theorem nu_outputs_not_convertible :
    ¬ Conv (.nu @@ .i @@ seed) (.nu @@ skk @@ seed) := by
  intro h
  have he := normal_convertible_equal (nu_seed_normal i_normal)
    (nu_seed_normal skk_normal) h
  cases he

/-- Any Church interpretation quantifying over conversion itself rejects this
    particular nu. This says nothing universal about other Raw-faithful models. -/
theorem nu_not_church_at_conversion :
    ¬ Arrow (Arrow Conv Conv) (Arrow Conv Conv) .nu .nu := by
  intro hn
  exact nu_outputs_not_convertible (hn .i skk i_skk_arrow seed seed (.refl _))

/-- The seed is a legitimate Raw=conversion element but neither value tag. -/
theorem seed_neither_tag : ¬ AtomVal seed ∧ ¬ FunVal seed := by
  have hhead : ¬ FunVal .a0 := atom_not_fun (Or.inl (.refl _))
  constructor
  · intro h
    exact hhead (head_origin (Or.inl h))
  · intro h
    exact hhead (head_origin (Or.inr h))

#print axioms i_skk_arrow
#print axioms nu_outputs_not_convertible
#print axioms nu_not_church_at_conversion
#print axioms seed_neither_tag
end FaithfulRawControl
