import ClosedScalarInstances

/- Complete developments on the actual open SKI carrier. The parallel relation
   and triangle proof port the inherited P01Source construction, with only the
   required inert-variable case added. This is not normal-order reduction. -/
namespace OpenDevelopments
open OpenTermStandardness (T Conv iter)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

inductive Par : T → T → Prop where
  | var0 (n : Nat) : Par (.var n) (.var n)
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

theorem par_refl (t : T) : Par t t := by
  induction t with
  | var n => exact .var0 n
  | i => exact .i0
  | k => exact .k0
  | s => exact .s0
  | zero => exact .z0
  | one => exact .o0
  | app f x hf hx => exact .app hf hx

def dev : T → T
  | .app .i x => dev x
  | .app (.app .k x) _ => dev x
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

theorem dev_plain (f x : T) (hi : f ≠ .i)
    (hk : ∀ a, f ≠ .app .k a) (hs : ∀ a b, f ≠ .app (.app .s a) b) :
    dev (.app f x) = .app (dev f) (dev x) := by
  cases f with
  | var n => rfl
  | i => exact False.elim (hi rfl)
  | k => rfl
  | s => rfl
  | zero => rfl
  | one => rfl
  | app a b =>
      cases a with
      | var n => rfl
      | i => rfl
      | k => exact False.elim (hk b rfl)
      | s => rfl
      | zero => rfl
      | one => rfl
      | app c d =>
          cases c with
          | s => exact False.elim (hs d b rfl)
          | var n => rfl
          | i => rfl
          | k => rfl
          | zero => rfl
          | one => rfl
          | app e g => rfl

/-- Every parallel reduct develops to the same complete development. -/
theorem par_develop {t u} (h : Par t u) : Par u (dev t) := by
  induction h with
  | var0 n => exact .var0 n
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


/-- Repeated application of the exact triangle law makes development monotone. -/
theorem dev_mono {t u : T} (h : Par t u) : Par (dev t) (dev u) :=
  par_develop (par_develop h)

def run : Nat → T → T
  | 0, t => t
  | k + 1, t => run k (dev t)

theorem run_mono {t u : T} (h : Par t u) (k : Nat) : Par (run k t) (run k u) := by
  induction k generalizing t u with
  | zero => exact h
  | succ k ih => exact ih (dev_mono h)

/-- The exact compatible SKI contraction relation on the same open T. -/
inductive Step : T → T → Prop where
  | i (x) : Step (.app .i x) x
  | k (x y) : Step (.app (.app .k x) y) x
  | s (f g x) : Step (.app (.app (.app .s f) g) x) (.app (.app f x) (.app g x))
  | left : Step f g → (x : T) → Step (.app f x) (.app g x)
  | right : (f : T) → Step x y → Step (.app f x) (.app f y)

def RedexFree (t : T) : Prop := ∀ u, ¬ Step t u

/-- Normality for the parallel relation includes reflexivity, but no proper reduct. -/
def Normal (t : T) : Prop := ∀ u, Par t u → u = t

def Reaches (normalForm t : T) : Prop := ∃ k, run k t = normalForm

/-- Ordinary absence of any compatible redex implies the parallel rigidity used
    below. In particular, no fixed-point-of-dev test is treated as normality. -/
theorem redexFree_normal {t : T} (hn : RedexFree t) : Normal t := by
  have aux : ∀ {t u : T}, Par t u → RedexFree t → u = t := by
    intro t u hp
    induction hp with
    | var0 n | i0 | k0 | s0 | z0 | o0 => intro _; rfl
    | app hf hx ihf ihx =>
      intro hn
      exact congrArg₂ T.app (ihf (fun v h => hn _ (.left h _)))
        (ihx (fun v h => hn _ (.right _ h)))
    | i h ih => intro hn; exact False.elim (hn _ (.i _))
    | k h k ih ik => intro hn; exact False.elim (hn _ (.k _ _))
    | s hf hg hx ihf ihg ihx => intro hn; exact False.elim (hn _ (.s _ _ _))
  exact fun u hp => aux hp hn


/-- Triangle cofinality, requiring weak normalization only. No accessibility or
    strong-normalization premise occurs in this strategy theorem. -/
theorem reaches_par_iff {z t u : T} (hz : Normal z) (h : Par t u) :
    Reaches z t ↔ Reaches z u := by
  constructor
  · rintro ⟨k, hk⟩
    have hp := run_mono h k
    rw [hk] at hp
    exact ⟨k, hz _ hp⟩
  · rintro ⟨k, hk⟩
    have hp := run_mono (par_develop h) k
    rw [hk] at hp
    exact ⟨k+1, hz _ hp⟩

inductive Chain : T → T → Prop where
  | refl (t) : Chain t t
  | par : Par t u → Chain t u
  | symm : Chain t u → Chain u t
  | trans : Chain t u → Chain u v → Chain t v

theorem Chain.left {t u : T} (h : Chain t u) (x : T) :
    Chain (.app t x) (.app u x) := by
  induction h with
  | refl t => exact .refl _
  | par h => exact .par (.app h (par_refl x))
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

theorem Chain.right (t : T) {x y : T} (h : Chain x y) :
    Chain (.app t x) (.app t y) := by
  induction h with
  | refl t => exact .refl _
  | par h => exact .par (.app (par_refl t) h)
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

theorem conv_chain {t u : T} (h : Conv t u) : Chain t u := by
  induction h with
  | refl t => exact .refl _
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik
  | app h k ih ik => exact (ih.left _).trans (Chain.right _ ik)
  | i x => exact .par (.i (par_refl x))
  | k x y => exact .par (.k (par_refl x) (par_refl y))
  | s f g x => exact .par (.s (par_refl f) (par_refl g) (par_refl x))

theorem reaches_chain_iff {z t u : T} (hz : Normal z) (h : Chain t u) :
    Reaches z t ↔ Reaches z u := by
  induction h with
  | refl t => exact Iff.rfl
  | par h => exact reaches_par_iff hz h
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik

/-- Every term convertible to a normal form reaches it by this exact executable
    development sequence. This is stronger than termination only for SN inputs. -/
theorem development_complete {z t : T} (hz : Normal z) (h : Conv t z) :
    ∃ k, run k t = z :=
  (reaches_chain_iff hz (conv_chain h)).mpr ⟨0,rfl⟩

theorem iter_normal (k : Nat) : Normal (iter (.var 1) (.var 0) k) := by
  induction k with
  | zero => intro u h; cases h; rfl
  | succ k ih =>
    intro u h
    cases h with
    | app hf hx =>
      cases hf
      rw [ih _ hx]
      rfl

/-- Concrete development is itself witnessed by compatible conversion. -/
theorem par_conv {t u : T} (h : Par t u) : Conv t u := by
  induction h with
  | var0 n | i0 | k0 | s0 | z0 | o0 => exact .refl _
  | app h k ih ik => exact .app ih ik
  | i h ih => exact (Conv.i _).trans ih
  | k h k ih ik => exact (Conv.k _ _).trans ih
  | s hf hg hx ihf ihg ihx =>
    exact (Conv.s _ _ _).trans (.app (.app ihf ihx) (.app ihg ihx))

theorem dev_conv (t : T) : Conv t (dev t) := par_conv (par_develop (par_refl t))

theorem run_conv (k : Nat) (t : T) : Conv t (run k t) := by
  induction k generalizing t with
  | zero => exact .refl _
  | succ k ih => exact (dev_conv t).trans (ih (dev t))

/-- Executable structural readback, retaining a checked syntax equality. -/
def readIteration : (t : T) → Option { k : Nat // t = iter (.var 1) (.var 0) k }
  | .var 0 => some ⟨0,rfl⟩
  | .app (.var 1) a => match readIteration a with
      | none => none
      | some ⟨k,h⟩ => some ⟨k+1, congrArg (T.app (.var 1)) h⟩
  | _ => none

theorem readIteration_iter (k : Nat) :
    (readIteration (iter (.var 1) (.var 0) k)).isSome = true := by
  induction k with
  | zero => rfl
  | succ k ih =>
    cases h : readIteration (iter (.var 1) (.var 0) k) with
    | none => simp [h] at ih
    | some value => simp only [iter, readIteration, h, Option.isSome_some]

theorem run_normal (k : Nat) {z : T} (hz : Normal z) : run k z = z := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change run k (dev z) = z
    rw [hz _ (par_develop (par_refl z))]
    exact ih

theorem normal_unique {t u : T} (ht : Normal t) (hu : Normal u) (h : Conv t u) : t = u := by
  obtain ⟨k,hk⟩ := development_complete hu h
  rw [run_normal k ht] at hk
  exact hk

theorem iter_injective {m n : Nat}
    (h : iter (.var 1) (.var 0) m = iter (.var 1) (.var 0) n) : m = n := by
  induction m generalizing n with
  | zero => cases n with
    | zero => rfl
    | succ n => cases h
  | succ m ih => cases n with
    | zero => cases h
    | succ n => exact congrArg Nat.succ (ih (T.app.inj h).2)

theorem iter_conv_injective {m n : Nat}
    (h : Conv (iter (.var 1) (.var 0) m) (iter (.var 1) (.var 0) n)) : m = n :=
  iter_injective (normal_unique (iter_normal m) (iter_normal n) h)

open P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N iterationPoly)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft scalarRight)

/-- For every supplied actual closed HasE input, both literal scalar endpoints
    reach one generic-open iteration under this deterministic strategy. -/
theorem closed_HasE_development_terminates {n : Poly} (hn : HasE [] n N) :
    ∃ k l r,
      run l (interp (scalarLeft n) T.var) = iter (.var 1) (.var 0) k ∧
      run r (interp (scalarRight n) T.var) = iter (.var 1) (.var 0) k := by
  obtain ⟨k, hk⟩ := OpenTermStandardness.church_standard _
    (ClosedScalarInstances.closed_church hn)
  have hl : Conv (interp (scalarLeft n) T.var) (iter (.var 1) (.var 0) k) :=
    hk (.var 1) (.var 0)
  have hr : Conv (interp (scalarRight n) T.var) (iter (.var 1) (.var 0) k) := by
    have hs := ClosedScalarInstances.closed_scalar_conversion hn
    have hs' := ImportedOpenTermTransport.source_plus_sound hs T.var
    exact hs'.symm.trans hl
  obtain ⟨l, hl'⟩ := development_complete (iter_normal k) hl
  obtain ⟨r, hr'⟩ := development_complete (iter_normal k) hr
  exact ⟨k,l,r,hl',hr'⟩

theorem closed_HasE_readback_exists {n : Poly} (hn : HasE [] n N) :
    ∃ r, (readIteration (run r (interp (scalarLeft n) T.var))).isSome = true := by
  obtain ⟨k,l,r,hl,hr⟩ := closed_HasE_development_terminates hn
  exact ⟨l, hl ▸ readIteration_iter k⟩

/-- A computable unbounded search, not Classical.choose. Nat.find inspects the
    decidable structural readback after each finite development count. HasE and
    its normalization theorem are erased proof arguments, not runtime oracles. -/
def extractIteration (n : Poly) (hn : HasE [] n N) :
    { k : Nat // P01AC.Intensional.Plus.PolyConvPlus (scalarLeft n) (iterationPoly k) } := by
  have h := closed_HasE_readback_exists hn
  let r := Nat.find h
  let result := (readIteration (run r (interp (scalarLeft n) T.var))).get (Nat.find_spec h)
  refine ⟨result.val, ClosedScalarInstances.generic_conversion_reflect ?_⟩
  rw [ClosedScalarInstances.iteration_interp]
  have hc := run_conv r (interp (scalarLeft n) T.var)
  rw [result.property] at hc
  exact hc

/-- The extracted count is the unique generic-open count, hence the uniform count
    already supplied by Church standardness; no bare-n numeral claim is made. -/
theorem extractIteration_uniform (n : Poly) (hn : HasE [] n N) :
    ∀ f a, Conv ((interp n T.var).app f |>.app a)
      (iter f a (extractIteration n hn).val) := by
  obtain ⟨k,hk⟩ := OpenTermStandardness.church_standard _ (ClosedScalarInstances.closed_church hn)
  have he := ImportedOpenTermTransport.source_plus_sound (extractIteration n hn).property T.var
  rw [ClosedScalarInstances.iteration_interp] at he
  have eq := iter_conv_injective ((hk (.var 1) (.var 0)).symm.trans he)
  exact eq ▸ hk

#print axioms extractIteration
#print axioms extractIteration_uniform
#print axioms development_complete
#print axioms closed_HasE_development_terminates
end OpenDevelopments
