import Std

/-! A concrete closed SKI + two atoms + case combinator term model.
This file is standalone. It assumes no algebra, confluence, or head-origin axiom. -/
namespace CaseOperational

inductive T where
  | i | k | s | a0 | a1 | nu
  | app : T → T → T
  deriving DecidableEq, Repr

inductive RawFun : T → Prop where
  | i : RawFun .i
  | k : RawFun .k
  | k1 (x) : RawFun (.app .k x)
  | s : RawFun .s
  | s1 (x) : RawFun (.app .s x)
  | s2 (x y) : RawFun (.app (.app .s x) y)
  | nu : RawFun .nu
  | nu1 (x) : RawFun (.app .nu x)

instance (t : T) : Decidable (RawFun t) := by
  cases t with
  | i => exact .isTrue .i
  | k => exact .isTrue .k
  | s => exact .isTrue .s
  | nu => exact .isTrue .nu
  | a0 => exact .isFalse (by intro h; cases h)
  | a1 => exact .isFalse (by intro h; cases h)
  | app f x =>
      cases f with
      | k => exact .isTrue (.k1 x)
      | s => exact .isTrue (.s1 x)
      | nu => exact .isTrue (.nu1 x)
      | i => exact .isFalse (by intro h; cases h)
      | a0 => exact .isFalse (by intro h; cases h)
      | a1 => exact .isFalse (by intro h; cases h)
      | app g y =>
          cases g with
          | s => exact .isTrue (.s2 y x)
          | i => exact .isFalse (by intro h; cases h)
          | k => exact .isFalse (by intro h; cases h)
          | nu => exact .isFalse (by intro h; cases h)
          | a0 => exact .isFalse (by intro h; cases h)
          | a1 => exact .isFalse (by intro h; cases h)
          | app h z => exact .isFalse (by intro h; cases h)

inductive Step : T → T → Prop where
  | i (x) : Step (.app .i x) x
  | k (x y) : Step (.app (.app .k x) y) x
  | s (f g x) : Step (.app (.app (.app .s f) g) x) (.app (.app f x) (.app g x))
  | nu0 (f) : Step (.app (.app .nu f) .a0) .a0
  | nu1 (f) : Step (.app (.app .nu f) .a1) .a1
  | nuF (f) {v} : RawFun v → Step (.app (.app .nu f) v) (.app f v)
  | left {f g} : Step f g → (x : T) → Step (.app f x) (.app g x)
  | right (f) {x y} : Step x y → Step (.app f x) (.app f y)

inductive Star {α : Type} (R : α → α → Prop) : α → α → Prop where
  | refl (t) : Star R t t
  | tail {t u v} : R t u → Star R u v → Star R t v
abbrev Red := Star Step

inductive Conv : T → T → Prop where
  | refl (t) : Conv t t
  | step {t u} : Step t u → Conv t u
  | symm {t u} : Conv t u → Conv u t
  | trans {t u v} : Conv t u → Conv u v → Conv t v

inductive Par : T → T → Prop where
  | i0 : Par .i .i
  | k0 : Par .k .k
  | s0 : Par .s .s
  | a0 : Par .a0 .a0
  | a1 : Par .a1 .a1
  | nu : Par .nu .nu
  | app {f f' x x'} : Par f f' → Par x x' → Par (.app f x) (.app f' x')
  | i {x x'} : Par x x' → Par (.app .i x) x'
  | k {x x' y y'} : Par x x' → Par y y' → Par (.app (.app .k x) y) x'
  | s {f f' g g' x x'} : Par f f' → Par g g' → Par x x' →
      Par (.app (.app (.app .s f) g) x) (.app (.app f' x') (.app g' x'))
  | nu0 {f f'} : Par f f' → Par (.app (.app .nu f) .a0) .a0
  | nu1 {f f'} : Par f f' → Par (.app (.app .nu f) .a1) .a1
  | nuF {f f' v v'} : Par f f' → Par v v' → RawFun v →
      Par (.app (.app .nu f) v) (.app f' v')

theorem par_refl (t : T) : Par t t := by
  induction t with
  | i => exact .i0
  | k => exact .k0
  | s => exact .s0
  | a0 => exact .a0
  | a1 => exact .a1
  | nu => exact .nu
  | app f x hf hx => exact .app hf hx

def dev : T → T
  | .app .i x => dev x
  | .app (.app .k x) _ => dev x
  | .app (.app (.app .s f) g) x => .app (.app (dev f) (dev x)) (.app (dev g) (dev x))
  | .app (.app .nu _) .a0 => .a0
  | .app (.app .nu _) .a1 => .a1
  | .app (.app .nu f) v =>
      if RawFun v then .app (dev f) (dev v) else .app (.app .nu (dev f)) (dev v)
  | .app f x => .app (dev f) (dev x)
  | t => t

theorem par_i_form {u} (h : Par .i u) : u = .i := by cases h; rfl
theorem par_a0_form {u} (h : Par .a0 u) : u = .a0 := by cases h; rfl
theorem par_a1_form {u} (h : Par .a1 u) : u = .a1 := by cases h; rfl

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

theorem par_nu_form {a u} (h : Par (.app .nu a) u) :
    ∃ a', u = .app .nu a' ∧ Par a a' := by
  cases h with
  | app hn ha => cases hn; exact ⟨_, rfl, ha⟩

theorem par_k_args {a a'} (h : Par (.app .k a) (.app .k a')) : Par a a' := by
  cases h with
  | app hk ha => exact ha

theorem par_s2_args {a b a' b'}
    (h : Par (.app (.app .s a) b) (.app (.app .s a') b')) : Par a a' ∧ Par b b' := by
  cases h with
  | app hs hb =>
      cases hs with
      | app hs ha => exact ⟨ha, hb⟩

theorem par_nu_args {a a'} (h : Par (.app .nu a) (.app .nu a')) : Par a a' := by
  cases h with
  | app hn ha => exact ha

theorem par_fun {v v'} (hv : RawFun v) (h : Par v v') : RawFun v' := by
  cases hv with
  | i => cases h; exact .i
  | k => cases h; exact .k
  | s => cases h; exact .s
  | nu => cases h; exact .nu
  | k1 x => obtain ⟨x', rfl, _⟩ := par_k_form h; exact .k1 x'
  | s1 x => obtain ⟨x', rfl, _⟩ := par_s1_form h; exact .s1 x'
  | s2 x y => obtain ⟨x', y', rfl, _, _⟩ := par_s2_form h; exact .s2 x' y'
  | nu1 x => obtain ⟨x', rfl, _⟩ := par_nu_form h; exact .nu1 x'

theorem dev_nu_fun (f) {v} (hv : RawFun v) :
    dev (.app (.app .nu f) v) = .app (dev f) (dev v) := by
  cases hv <;> simp only [dev, ↓reduceIte] <;> rfl

theorem dev_nu_plain (f v) (h0 : v ≠ .a0) (h1 : v ≠ .a1) (hv : ¬RawFun v) :
    dev (.app (.app .nu f) v) = .app (.app .nu (dev f)) (dev v) := by
  cases v <;> simp_all only [dev, ↓reduceIte]
  all_goals contradiction

theorem dev_plain (f x : T) (hi : f ≠ .i)
    (hk : ∀ a, f ≠ .app .k a) (hs : ∀ a b, f ≠ .app (.app .s a) b)
    (hn : ∀ a, f ≠ .app .nu a) :
    dev (.app f x) = .app (dev f) (dev x) := by
  cases f with
  | i => exact False.elim (hi rfl)
  | k => rfl
  | s => rfl
  | a0 => rfl
  | a1 => rfl
  | nu => rfl
  | app a b =>
      cases a with
      | i => rfl
      | k => exact False.elim (hk b rfl)
      | s => rfl
      | a0 => rfl
      | a1 => rfl
      | nu => exact False.elim (hn b rfl)
      | app c d =>
          cases c with
          | s => exact False.elim (hs d b rfl)
          | i => rfl
          | k => rfl
          | a0 => rfl
          | a1 => rfl
          | nu => rfl
          | app e g => rfl

/-- Parallel developments have a common, explicitly computed target. -/
theorem par_develop {t u} (h : Par t u) : Par u (dev t) := by
  induction h with
  | i0 => exact .i0
  | k0 => exact .k0
  | s0 => exact .s0
  | a0 => exact .a0
  | a1 => exact .a1
  | nu => exact .nu
  | i h ih => exact ih
  | k hx hy ihx ihy => exact ihx
  | s hf hg hx ihf ihg ihx => exact .app (.app ihf ihx) (.app ihg ihx)
  | nu0 hf ihf => exact .a0
  | nu1 hf ihf => exact .a1
  | nuF hf hv hfun ihf ihv =>
      rw [dev_nu_fun _ hfun]
      exact .app ihf ihv
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
          · by_cases hn : ∃ a, f = .app .nu a
            · obtain ⟨a, rfl⟩ := hn
              obtain ⟨a', rfl, ha⟩ := par_nu_form hf
              have hp : Par (.app .nu a') (.app .nu (dev a)) := by
                simpa only [dev] using ihf
              have ih := par_nu_args hp
              by_cases h0 : x = .a0
              · subst x
                have e := par_a0_form hx
                subst x'
                exact .nu0 ih
              · by_cases h1 : x = .a1
                · subst x
                  have e := par_a1_form hx
                  subst x'
                  exact .nu1 ih
                · by_cases hv : RawFun x
                  · rw [dev_nu_fun _ hv]
                    exact .nuF ih ihx (par_fun hv hx)
                  · rw [dev_nu_plain _ _ h0 h1 hv]
                    exact .app (.app .nu ih) ihx
            · rw [dev_plain f x hi (fun a e => hk ⟨a,e⟩)
                (fun a b e => hs ⟨a,b,e⟩) (fun a e => hn ⟨a,e⟩)]
              exact .app ihf ihx


theorem par_diamond {t u v} (h : Par t u) (k : Par t v) :
    ∃ w, Par u w ∧ Par v w := ⟨dev t, par_develop h, par_develop k⟩

theorem star_trans {α : Type} {R : α → α → Prop} {t u v}
    (h : Star R t u) (k : Star R u v) : Star R t v := by
  induction h with
  | refl => exact k
  | tail h r ih => exact .tail h (ih k)

theorem red_one {t u} (h : Step t u) : Red t u := .tail h (.refl _)

theorem red_left {f g} (h : Red f g) (x) : Red (.app f x) (.app g x) := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact .tail (.left h x) ih

theorem red_right (f) {x y} (h : Red x y) : Red (.app f x) (.app f y) := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact .tail (.right f h) ih

theorem red_app {f g x y} (h : Red f g) (k : Red x y) :
    Red (.app f x) (.app g y) := star_trans (red_left h x) (red_right g k)

theorem par_red {t u} (h : Par t u) : Red t u := by
  induction h with
  | i0 => exact .refl _
  | k0 => exact .refl _
  | s0 => exact .refl _
  | a0 => exact .refl _
  | a1 => exact .refl _
  | nu => exact .refl _
  | app h k ih ik => exact red_app ih ik
  | i h ih => exact .tail (.i _) ih
  | k hx hy ihx ihy => exact .tail (.k _ _) ihx
  | s hf hg hx ihf ihg ihx =>
      exact .tail (.s _ _ _) (red_app (red_app ihf ihx) (red_app ihg ihx))
  | nu0 hf ihf => exact red_one (.nu0 _)
  | nu1 hf ihf => exact red_one (.nu1 _)
  | nuF hf hv hfun ihf ihv => exact .tail (.nuF _ hfun) (red_app ihf ihv)

theorem step_par {t u} (h : Step t u) : Par t u := by
  induction h with
  | i x => exact .i (par_refl x)
  | k x y => exact .k (par_refl x) (par_refl y)
  | s f g x => exact .s (par_refl f) (par_refl g) (par_refl x)
  | nu0 f => exact .nu0 (par_refl f)
  | nu1 f => exact .nu1 (par_refl f)
  | nuF f hv => exact .nuF (par_refl f) (par_refl _) hv
  | left h x ih => exact .app ih (par_refl x)
  | right f h ih => exact .app (par_refl f) ih

abbrev PStar := Star Par

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
  | tail h r ih => exact star_trans (par_red h) ih

/-- Compatible reduction for the exact thirteen-rule TRS is confluent. -/
theorem confluence {t u v} (h : Red t u) (k : Red t v) :
    ∃ w, Red u w ∧ Red v w := by
  obtain ⟨w, hu, hv⟩ := pstar_confluence (red_pstar h) (red_pstar k)
  exact ⟨w, pstar_red hu, pstar_red hv⟩

theorem conv_join {t u} (h : Conv t u) : ∃ w, Red t w ∧ Red u w := by
  induction h with
  | refl => exact ⟨_, .refl _, .refl _⟩
  | step h => exact ⟨_, red_one h, .refl _⟩
  | symm h ih => obtain ⟨w, ht, hu⟩ := ih; exact ⟨w, hu, ht⟩
  | trans h k ih ik =>
      obtain ⟨a, ht, hu⟩ := ih
      obtain ⟨b, hu', hv⟩ := ik
      obtain ⟨w, ha, hb⟩ := confluence hu hu'
      exact ⟨w, star_trans ht ha, star_trans hv hb⟩

theorem red_conv {t u} (h : Red t u) : Conv t u := by
  induction h with
  | refl => exact .refl _
  | tail s r ih => exact .trans (.step s) ih

theorem Conv.left {f g} (h : Conv f g) (x) : Conv (.app f x) (.app g x) := by
  induction h with
  | refl => exact .refl _
  | step h => exact .step (.left h x)
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

theorem Conv.right (f) {x y} (h : Conv x y) : Conv (.app f x) (.app f y) := by
  induction h with
  | refl => exact .refl _
  | step h => exact .step (.right f h)
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

theorem Conv.app {f g x y} (h : Conv f g) (k : Conv x y) :
    Conv (.app f x) (.app g y) := .trans (h.left x) (k.right g)

theorem Conv.i (x) : Conv (.app .i x) x := .step (.i x)
theorem Conv.k (x y) : Conv (.app (.app .k x) y) x := .step (.k x y)
theorem Conv.s (f g x) : Conv (.app (.app (.app .s f) g) x)
    (.app (.app f x) (.app g x)) := .step (.s f g x)

inductive RawValue : T → Prop where
  | a0 : RawValue .a0
  | a1 : RawValue .a1
  | fn {v} : RawFun v → RawValue v

def AtomVal (t : T) : Prop := Conv t .a0 ∨ Conv t .a1
def FunVal (t : T) : Prop := ∃ v, RawFun v ∧ Conv t v

theorem raw_fun_val {t} (h : RawFun t) : FunVal t := ⟨t, h, .refl _⟩
theorem funVal_back {t u} (h : Conv t u) : FunVal u → FunVal t := by
  rintro ⟨v, hv, huv⟩
  exact ⟨v, hv, .trans h huv⟩

theorem rawValue_app_left {t a} (h : RawValue (.app t a)) : RawFun t := by
  cases h with
  | fn h =>
      cases h with
      | k1 _ => exact .k
      | s1 _ => exact .s
      | s2 _ _ => exact .s1 _
      | nu1 _ => exact .nu

/-- The first root contraction has a function prefix; without one the
    final weak-head application's left prefix is already a function. -/
theorem application_strictness {z v} (h : Red z v) (hv : RawValue v) :
    ∀ t a, z = .app t a → ∃ w, Red t w ∧ RawFun w := by
  induction h with
  | refl z =>
      intro t a hz
      subst z
      exact ⟨t, .refl _, rawValue_app_left hv⟩
  | @tail z u v hs hr ih =>
      intro t a hz
      subst z
      cases hs with
      | i _ => exact ⟨_, .refl _, .i⟩
      | k x y => exact ⟨_, .refl _, .k1 _⟩
      | s f g x => exact ⟨_, .refl _, .s2 _ _⟩
      | nu0 f => exact ⟨_, .refl _, .nu1 _⟩
      | nu1 f => exact ⟨_, .refl _, .nu1 _⟩
      | nuF f _ => exact ⟨_, .refl _, .nu1 _⟩
      | left h _ =>
          obtain ⟨w, hw, hf⟩ := ih hv _ _ rfl
          exact ⟨w, .tail h hw, hf⟩
      | right _ h => exact ih hv _ _ rfl

theorem rawFun_step {t u} (ht : RawFun t) (h : Step t u) : RawFun u :=
  par_fun ht (step_par h)

theorem rawValue_step {t u} (ht : RawValue t) (h : Step t u) : RawValue u := by
  cases ht with
  | a0 => cases h
  | a1 => cases h
  | fn hf => exact .fn (rawFun_step hf h)

theorem rawValue_red {t u} (ht : RawValue t) (h : Red t u) : RawValue u := by
  induction h with
  | refl => exact ht
  | tail hs hr ih => exact ih (rawValue_step ht hs)

theorem application_conv_value {t a v} (h : Conv (.app t a) v)
    (hv : RawValue v) : FunVal t := by
  obtain ⟨w, ht, hvw⟩ := conv_join h
  obtain ⟨u, hu, hf⟩ := application_strictness ht (rawValue_red hv hvw) t a rfl
  exact ⟨u, hf, red_conv hu⟩

/-- Exact conversion-level head-origin theorem. -/
theorem head_origin {t a} : (AtomVal (.app t a) ∨ FunVal (.app t a)) → FunVal t := by
  rintro ((h0 | h1) | ⟨v, hv, h⟩)
  · exact application_conv_value h0 .a0
  · exact application_conv_value h1 .a1
  · exact application_conv_value h (.fn hv)

theorem a0_red {t} (h : Red .a0 t) : t = .a0 := by
  cases h with
  | refl => rfl
  | tail h _ => cases h

theorem a1_red {t} (h : Red .a1 t) : t = .a1 := by
  cases h with
  | refl => rfl
  | tail h _ => cases h

theorem atom_distinct : ¬Conv .a0 .a1 := by
  intro h
  obtain ⟨w, h0, h1⟩ := conv_join h
  have e := (a0_red h0).symm.trans (a1_red h1)
  cases e

theorem rawFun_red {t u} (ht : RawFun t) (h : Red t u) : RawFun u := by
  induction h with
  | refl => exact ht
  | tail hs hr ih => exact ih (rawFun_step ht hs)

theorem atom_not_fun {t} (ha : AtomVal t) : ¬ FunVal t := by
  rintro ⟨v, hv, htv⟩
  rcases ha with h0 | h1
  · obtain ⟨w, hw0, hwv⟩ := conv_join (.trans (.symm h0) htv)
    have hfun := rawFun_red hv hwv
    rw [a0_red hw0] at hfun
    cases hfun
  · obtain ⟨w, hw1, hwv⟩ := conv_join (.trans (.symm h1) htv)
    have hfun := rawFun_red hv hwv
    rw [a1_red hw1] at hfun
    cases hfun

theorem nu_atom0 (f) : Conv (.app (.app .nu f) .a0) .a0 := .step (.nu0 f)
theorem nu_atom1 (f) : Conv (.app (.app .nu f) .a1) .a1 := .step (.nu1 f)

theorem nu_fun (f) {v} (hv : FunVal v) :
    Conv (.app (.app .nu f) v) (.app f v) := by
  obtain ⟨w, hw, hvw⟩ := hv
  exact .trans (hvw.right (.app .nu f))
    (.trans (.step (.nuF f hw)) ((Conv.symm hvw).right f))

#print axioms confluence
#print axioms conv_join
#print axioms head_origin
#print axioms atom_distinct
#print axioms atom_not_fun
#print axioms nu_fun

end CaseOperational
