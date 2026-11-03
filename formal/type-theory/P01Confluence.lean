/- Raw compatible SKI confluence: source-theoretic parallel developments.
   No lambda-conversion reflection, extensionality, or typing premise.
   New authored attempt-0003 proof candidate; UNCOMPILED at 4.19.0. -/
import P01Candidates
namespace P01Source
open OrthemologyV2 OrthemologyV3

inductive Par : Term → Term → Prop where
  | i0 : Par .i .i
  | k0 : Par .k .k
  | s0 : Par .s .s
  | z0 : Par .zero .zero
  | o0 : Par .one .one
  | app {f f' x x'} : Par f f' → Par x x' → Par (.app f x) (.app f' x')
  | i {x x'} : Par x x' → Par (.app .i x) x'
  | k {x x' y y'} : Par x x' → Par y y' → Par (.app (.app .k x) y) x'
  | s {f f' g g' x x'} : Par f f' → Par g g' → Par x x' →
      Par (.app (.app (.app .s f) g) x) (.app (.app f' x') (.app g' x'))

theorem par_refl (t : Term) : Par t t := by
  induction t with
  | i => exact .i0
  | k => exact .k0
  | s => exact .s0
  | zero => exact .z0
  | one => exact .o0
  | app f x hf hx => exact .app hf hx

def dev : Term → Term
  | .app .i x => dev x
  | .app (.app .k x) y => dev x
  | .app (.app (.app .s f) g) x => .app (.app (dev f) (dev x)) (.app (dev g) (dev x))
  | .app f x => .app (dev f) (dev x)
  | t => t

theorem par_i_form {u} (h : Par .i u) : u = .i := by cases h; rfl

theorem par_k_form {a u} (h : Par (.app .k a) u) :
    ∃ a', u = .app .k a' ∧ Par a a' := by
  cases h with
  | app hk ha => cases hk; exact ⟨_, rfl, ha⟩

theorem par_s1_form {a u} (h : Par (.app .s a) u) :
    ∃ a', u = .app .s a' ∧ Par a a' := by
  cases h with
  | app hs ha => cases hs; exact ⟨_, rfl, ha⟩

theorem par_s2_form {a b u} (h : Par (.app (.app .s a) b) u) :
    ∃ a' b', u = .app (.app .s a') b' ∧ Par a a' ∧ Par b b' := by
  cases h with
  | app hs hb =>
      obtain ⟨a', rfl, ha⟩ := par_s1_form hs
      exact ⟨a', _, rfl, ha, hb⟩

theorem par_k_args {a a'} (h : Par (.app .k a) (.app .k a')) : Par a a' := by
  cases h with
  | app hk ha => exact ha

theorem par_s2_args {a b a' b'}
    (h : Par (.app (.app .s a) b) (.app (.app .s a') b')) : Par a a' ∧ Par b b' := by
  cases h with
  | app hs hb =>
      cases hs with
      | app hs ha => exact ⟨ha, hb⟩

theorem dev_plain (f x : Term) (hi : f ≠ .i)
    (hk : ∀ a, f ≠ .app .k a) (hs : ∀ a b, f ≠ .app (.app .s a) b) :
    dev (.app f x) = .app (dev f) (dev x) := by
  cases f with
  | i => exact False.elim (hi rfl)
  | k => rfl
  | s => rfl
  | zero => rfl
  | one => rfl
  | app a b =>
      cases a with
      | i => rfl
      | k => exact False.elim (hk b rfl)
      | s => rfl
      | zero => rfl
      | one => rfl
      | app c d =>
          cases c with
          | s => exact False.elim (hs d b rfl)
          | i => rfl
          | k => rfl
          | zero => rfl
          | one => rfl
          | app e g => rfl

/-- Every parallel reduct develops to the same complete development. -/
theorem par_develop {t u} (h : Par t u) : Par u (dev t) := by
  induction h with
  | i0 => exact .i0
  | k0 => exact .k0
  | s0 => exact .s0
  | z0 => exact .z0
  | o0 => exact .o0
  | i h ih => exact ih
  | k hx hy ihx ihy => exact ihx
  | s hf hg hx ihf ihg ihx => exact .app (.app ihf ihx) (.app ihg ihx)
  | @app f f' x x' hf hx ihf ihx =>
      by_cases hi : f = .i
      · subst f
        have e := par_i_form hf
        subst f'
        exact .i ihx
      · by_cases hk : ∃ a, f = .app .k a
        · obtain ⟨a, rfl⟩ := hk
          obtain ⟨a', rfl, ha⟩ := par_k_form hf
          have hp : Par (.app .k a') (.app .k (dev a)) := by
            simpa only [dev] using ihf
          exact .k (par_k_args hp) ihx
        · by_cases hs : ∃ a b, f = .app (.app .s a) b
          · obtain ⟨a, b, rfl⟩ := hs
            obtain ⟨a', b', rfl, ha, hb⟩ := par_s2_form hf
            have hp : Par (.app (.app .s a') b') (.app (.app .s (dev a)) (dev b)) := by
              simpa only [dev] using ihf
            have hh := par_s2_args hp
            exact .s hh.1 hh.2 ihx
          · rw [dev_plain f x hi (fun a e => hk ⟨a,e⟩) (fun a b e => hs ⟨a,b,e⟩)]
            exact .app ihf ihx

theorem par_diamond {t u v} (h : Par t u) (k : Par t v) :
    ∃ w, Par u w ∧ Par v w := ⟨dev t, par_develop h, par_develop k⟩

theorem red_trans {t u v} (h : Red t u) (k : Red u v) : Red t v := by
  induction h with
  | refl => exact k
  | tail h r ih => exact .tail h (ih k)

theorem red_right (f) {x y} (h : Red x y) : Red (.app f x) (.app f y) := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact .tail (.right f h) ih

theorem red_app {f g x y} (h : Red f g) (k : Red x y) :
    Red (.app f x) (.app g y) := red_trans (Red.left h x) (red_right g k)

theorem par_red {t u} (h : Par t u) : Red t u := by
  induction h with
  | i0 => exact .refl _
  | k0 => exact .refl _
  | s0 => exact .refl _
  | z0 => exact .refl _
  | o0 => exact .refl _
  | app h k ih ik => exact red_app ih ik
  | i h ih => exact .tail (.i _) ih
  | k h k ih ik => exact .tail (.k _ _) ih
  | s hf hg hx ihf ihg ihx =>
      exact red_trans (red_app (red_app (red_app (.refl .s) ihf) ihg) ihx)
        (Red.one (.s _ _ _))

theorem step_par {t u} (h : Step t u) : Par t u := by
  induction h with
  | i x => exact .i (par_refl x)
  | k x y => exact .k (par_refl x) (par_refl y)
  | s f g x => exact .s (par_refl f) (par_refl g) (par_refl x)
  | left h x ih => exact .app ih (par_refl x)
  | right f h ih => exact .app (par_refl f) ih

abbrev PStar := P01SNReflection.Star Par

theorem pstar_trans {t u v} (h : PStar t u) (k : PStar u v) : PStar t v := by
  induction h with
  | refl => exact k
  | tail h r ih => exact .tail h (ih k)

theorem strip {t u v} (h : Par t u) (r : PStar t v) :
    ∃ w, PStar u w ∧ Par v w := by
  induction r generalizing u with
  | refl => exact ⟨u, .refl _, h⟩
  | tail s r ih =>
      obtain ⟨z, hz, kz⟩ := par_diamond h s
      obtain ⟨w, hw, kw⟩ := ih kz
      exact ⟨w, .tail hz hw, kw⟩

theorem pstar_confluence {t u v} (h : PStar t u) (k : PStar t v) :
    ∃ w, PStar u w ∧ PStar v w := by
  induction h generalizing v with
  | refl => exact ⟨v, k, .refl _⟩
  | tail s r ih =>
      obtain ⟨z, hz, kz⟩ := strip s k
      obtain ⟨w, hw, kw⟩ := ih hz
      exact ⟨w, hw, .tail kz kw⟩

theorem red_pstar {t u} (h : Red t u) : PStar t u := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact .tail (step_par h) ih

theorem pstar_red {t u} (h : PStar t u) : Red t u := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact red_trans (par_red h) ih

theorem confluence {t u v} (h : Red t u) (k : Red t v) :
    ∃ w, Red u w ∧ Red v w := by
  obtain ⟨w, hu, hv⟩ := pstar_confluence (red_pstar h) (red_pstar k)
  exact ⟨w, pstar_red hu, pstar_red hv⟩

theorem conv_join {t u} (h : Conv t u) : ∃ w, Red t w ∧ Red u w := by
  induction h with
  | refl => exact ⟨_, .refl _, .refl _⟩
  | step h => exact ⟨_, Red.one h, .refl _⟩
  | symm h ih => obtain ⟨w, ht, hu⟩ := ih; exact ⟨w, hu, ht⟩
  | trans h k ih ik =>
      obtain ⟨a, ht, hu⟩ := ih
      obtain ⟨b, hu', hv⟩ := ik
      obtain ⟨w, ha, hb⟩ := confluence hu hu'
      exact ⟨w, red_trans ht ha, red_trans hv hb⟩

def Normal (t : Term) := ∀ u, ¬ Step t u

theorem normal_red {t u} (h : Normal t) (r : Red t u) : u = t := by
  cases r with
  | refl => rfl
  | tail s r => exact False.elim (h _ s)

theorem normal_exists {t} (h : P01Candidates.SN t) : ∃n, Red t n ∧ Normal n := by
  induction h with
  | intro t next ih =>
      by_cases hn : Normal t
      · exact ⟨t, .refl _, hn⟩
      · have he : ∃ u, Step t u := by simpa only [Normal, not_forall, not_not] using hn
        obtain ⟨u, hu⟩ := he
        obtain ⟨n, hr, hn⟩ := ih u hu
        exact ⟨n, .tail hu hr, hn⟩

theorem normal_unique {t u} (ht : Normal t) (hu : Normal u) (h : Conv t u) : t = u := by
  obtain ⟨w, hw, kw⟩ := conv_join h
  exact (normal_red ht hw).symm.trans (normal_red hu kw)

theorem red_conv {t u} (h : Red t u) : Conv t u := by
  induction h with
  | refl => exact .refl _
  | tail s r ih => exact .trans (.step s) ih

/-- Normal forms characterize precisely raw source conversion. -/
theorem conversion_by_normal_forms {t u n m} (ht : Red t n) (hu : Red u m)
    (hn : Normal n) (hm : Normal m) : Conv t u ↔ n = m := by
  constructor
  · intro h
    exact normal_unique hn hm (.trans (.symm (red_conv ht)) (.trans h (red_conv hu)))
  · intro e; subst m
    exact .trans (red_conv ht) (.symm (red_conv hu))

theorem finite_normal_form {t A} (h : FiniteDerives t A) :
    ∃ n, Red t n ∧ Normal n := normal_exists (P01Candidates.finite_SN h)

/-- Minimal counterexample to target-conversion reflection: distinct raw normal
    forms remain unequal despite their beta-convertible translations. -/
theorem I_SKK_not_convertible : ¬ Conv .i (.app (.app .s .k) .k) := by
  intro h
  have hi : Normal .i := by intro u hu; cases hu
  have hs : Normal (.app (.app .s .k) .k) := by
    intro u hu
    cases hu with
    | left h k =>
        cases h with
        | left h k => cases h
        | right s h => cases h
    | right sk h => cases h
  have e := normal_unique hi hs h
  cases e
end P01Source
