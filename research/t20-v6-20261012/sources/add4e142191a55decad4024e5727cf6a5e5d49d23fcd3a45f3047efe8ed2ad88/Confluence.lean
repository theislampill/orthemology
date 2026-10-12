import Strictness

/- Direct complete-development proof for the actual 13-rule extended TRS.
   Proof organization adapted from retained P01Confluence/OpenDevelopments;
   no original file is edited or baseline imported. -/
namespace HomogeneousPERAdversarial
open Term
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

inductive Par : Term → Term → Prop where
  | i0 : Par .i .i
  | k0 : Par .k .k
  | s0 : Par .s .s
  | nu0 : Par .nu .nu
  | a00 : Par .a0 .a0
  | a10 : Par .a1 .a1
  | app : Par f f' → Par x x' → Par (f @@ x) (f' @@ x')
  | i : Par x x' → Par (.i @@ x) x'
  | k : Par x x' → Par y y' → Par (.k @@ x @@ y) x'
  | s : Par f f' → Par g g' → Par x x' →
      Par (.s @@ f @@ g @@ x) (f' @@ x' @@ (g' @@ x'))
  | nuAtom0 (f) : Par (.nu @@ f @@ .a0) .a0
  | nuAtom1 (f) : Par (.nu @@ f @@ .a1) .a1
  | nuFunction : FunWHNF v → Par f f' → Par v v' →
      Par (.nu @@ f @@ v) (f' @@ v')

theorem par_refl (t : Term) : Par t t := by
  induction t with
  | i => exact .i0
  | k => exact .k0
  | s => exact .s0
  | nu => exact .nu0
  | a0 => exact .a00
  | a1 => exact .a10
  | app f x hf hx => exact .app hf hx

def dev : Term → Term
  | .app .i x => dev x
  | .app (.app .k x) _ => dev x
  | .app (.app (.app .s f) g) x => dev f @@ dev x @@ (dev g @@ dev x)
  | .app (.app .nu _) .a0 => .a0
  | .app (.app .nu _) .a1 => .a1
  | .app (.app .nu f) .i => dev f @@ .i
  | .app (.app .nu f) .k => dev f @@ .k
  | .app (.app .nu f) (.app .k x) => dev f @@ (.k @@ dev x)
  | .app (.app .nu f) .s => dev f @@ .s
  | .app (.app .nu f) (.app .s x) => dev f @@ (.s @@ dev x)
  | .app (.app .nu f) (.app (.app .s x) y) => dev f @@ (.s @@ dev x @@ dev y)
  | .app (.app .nu f) .nu => dev f @@ .nu
  | .app (.app .nu f) (.app .nu x) => dev f @@ (.nu @@ dev x)
  | .app f x => dev f @@ dev x
  | t => t

theorem dev_nu_function (f) {v} (h : FunWHNF v) :
    dev (.nu @@ f @@ v) = dev f @@ dev v := by cases h <;> rfl

theorem par_i_form {u} (h : Par .i u) : u = .i := by cases h; rfl

theorem par_k_form {a u} (h : Par (.k @@ a) u) :
    ∃ a', u = .k @@ a' ∧ Par a a' := by
  cases h with
  | app hk ha => cases hk; exact ⟨_, rfl, ha⟩

theorem par_s1_form {a u} (h : Par (.s @@ a) u) :
    ∃ a', u = .s @@ a' ∧ Par a a' := by
  cases h with
  | app hs ha => cases hs; exact ⟨_, rfl, ha⟩

theorem par_s2_form {a b u} (h : Par (.s @@ a @@ b) u) :
    ∃ a' b', u = .s @@ a' @@ b' ∧ Par a a' ∧ Par b b' := by
  cases h with
  | app hs hb =>
      obtain ⟨a', rfl, ha⟩ := par_s1_form hs
      exact ⟨a', _, rfl, ha, hb⟩

theorem par_nu_form {a u} (h : Par (.nu @@ a) u) :
    ∃ a', u = .nu @@ a' ∧ Par a a' := by
  cases h with
  | app hn ha => cases hn; exact ⟨_, rfl, ha⟩

theorem par_k_args {a a'} (h : Par (.k @@ a) (.k @@ a')) : Par a a' := by
  cases h with
  | app hk ha => exact ha

theorem par_s2_args {a b a' b'}
    (h : Par (.s @@ a @@ b) (.s @@ a' @@ b')) : Par a a' ∧ Par b b' := by
  cases h with
  | app hs hb =>
      cases hs with
      | app hs ha => exact ⟨ha, hb⟩

theorem par_nu_args {a a'} (h : Par (.nu @@ a) (.nu @@ a')) : Par a a' := by
  cases h with
  | app hn ha => exact ha

theorem function_whnf_par {t u} (ht : FunWHNF t) (h : Par t u) : FunWHNF u := by
  cases ht with
  | i => cases h; exact .i
  | k => cases h; exact .k
  | s => cases h; exact .s
  | nu => cases h; exact .nu
  | kApp x => obtain ⟨_, rfl, _⟩ := par_k_form h; exact .kApp _
  | sApp x => obtain ⟨_, rfl, _⟩ := par_s1_form h; exact .sApp _
  | sApp2 x y => obtain ⟨_, _, rfl, _, _⟩ := par_s2_form h; exact .sApp2 _ _
  | nuApp x => obtain ⟨_, rfl, _⟩ := par_nu_form h; exact .nuApp _

theorem dev_nu_plain (a x : Term) (hx : ¬ Value x) :
    dev (.nu @@ a @@ x) = (.nu @@ dev a) @@ dev x := by
  cases x with
  | a0 => exact False.elim (hx .a0)
  | a1 => exact False.elim (hx .a1)
  | i => exact False.elim (hx (.fn .i))
  | k => exact False.elim (hx (.fn .k))
  | s => exact False.elim (hx (.fn .s))
  | nu => exact False.elim (hx (.fn .nu))
  | app c d =>
      cases c with
      | k => exact False.elim (hx (.fn (.kApp d)))
      | s => exact False.elim (hx (.fn (.sApp d)))
      | nu => exact False.elim (hx (.fn (.nuApp d)))
      | i | a0 | a1 => rfl
      | app e f =>
          cases e with
          | s => exact False.elim (hx (.fn (.sApp2 f d)))
          | i | k | nu | a0 | a1 | app => rfl

theorem dev_plain (f x : Term) (hi : f ≠ .i)
    (hk : ∀ a, f ≠ .k @@ a) (hs : ∀ a b, f ≠ .s @@ a @@ b)
    (hn : ∀ a, f = .nu @@ a → ¬ Value x) :
    dev (f @@ x) = dev f @@ dev x := by
  cases f with
  | i => exact False.elim (hi rfl)
  | k | s | nu | a0 | a1 => rfl
  | app a b =>
      cases a with
      | k => exact False.elim (hk b rfl)
      | nu => exact dev_nu_plain b x (hn b rfl)
      | i | s | a0 | a1 => rfl
      | app c d =>
          cases c with
          | s => exact False.elim (hs d b rfl)
          | i | k | nu | a0 | a1 | app => rfl

/-- Exact triangle law for the extended calculus, including all case rules. -/
theorem par_develop {t u} (h : Par t u) : Par u (dev t) := by
  induction h with
  | i0 => exact .i0
  | k0 => exact .k0
  | s0 => exact .s0
  | nu0 => exact .nu0
  | a00 => exact .a00
  | a10 => exact .a10
  | i h ih => exact ih
  | k hx hy ihx ihy => exact ihx
  | s hf hg hx ihf ihg ihx => exact .app (.app ihf ihx) (.app ihg ihx)
  | nuAtom0 => exact .a00
  | nuAtom1 => exact .a10
  | nuFunction hv hf hx ihf ihx =>
      rw [dev_nu_function _ hv]
      exact .app ihf ihx
  | @app f f' x x' hf hx ihf ihx =>
      by_cases hi : f = .i
      · subst f
        have e := par_i_form hf
        subst f'
        exact .i ihx
      · by_cases hk : ∃ a, f = .k @@ a
        · obtain ⟨a, rfl⟩ := hk
          obtain ⟨a', rfl, ha⟩ := par_k_form hf
          have hp : Par (.k @@ a') (.k @@ dev a) := by simpa only [dev] using ihf
          exact .k (par_k_args hp) ihx
        · by_cases hs : ∃ a b, f = .s @@ a @@ b
          · obtain ⟨a, b, rfl⟩ := hs
            obtain ⟨a', b', rfl, ha, hb⟩ := par_s2_form hf
            have hp : Par (.s @@ a' @@ b') (.s @@ dev a @@ dev b) := by
              simpa only [dev] using ihf
            have hh := par_s2_args hp
            exact .s hh.1 hh.2 ihx
          · by_cases hn : ∃ a, f = .nu @@ a ∧ Value x
            · obtain ⟨a, rfl, hv⟩ := hn
              obtain ⟨a', rfl, ha⟩ := par_nu_form hf
              have hp : Par (.nu @@ a') (.nu @@ dev a) := by simpa only [dev] using ihf
              cases hv with
              | a0 => cases hx; exact .nuAtom0 _
              | a1 => cases hx; exact .nuAtom1 _
              | fn hv =>
                  rw [dev_nu_function _ hv]
                  exact .nuFunction (function_whnf_par hv hx) (par_nu_args hp) ihx
            · rw [dev_plain f x hi (fun a e => hk ⟨a,e⟩)
                (fun a b e => hs ⟨a,b,e⟩) (fun a e hx => hn ⟨a,e,hx⟩)]
              exact .app ihf ihx

#print axioms par_develop
end HomogeneousPERAdversarial
