import FiniteClosedClass
import FiniteRotorCoverage

noncomputable section
namespace HiddenParity.Cost
open HiddenParity.Sufficiency FiniteChainHitting
variable {Q S A : Type*} [Fintype Q] [DecidableEq Q] [DecidableEq S] [DecidableEq A]

/-- A closed rotor class contains every active action at each of its physical
source states. Local edge/counter equations imply coverage; no fair policy or
recurrent stochastic path is assumed. The residue at entry is arbitrary. -/
theorem rotor_closed_class_covers_menu
    (edge : Q → Q → Prop) [DecidableRel edge]
    (source : Q → S) (action : Q → A) (menu : S → Finset A) (fallback : A)
    (residue : Q → S → ℕ) (C : Finset Q) (hC : ClosedClass edge C)
    (hNext : ∀ q ∈ C, ∃ q', edge q q')
    (hAction : ∀ q ∈ C, action q = cycleAction (menu (source q)) fallback (residue q (source q)))
    (hRotor : ∀ q ∈ C, ∀ q', edge q q' → ∀ s,
      residue q' s = (residue q s + if source q=s then 1 else 0)%(menu s).card)
    (q₀ : Q) (hq₀ : q₀ ∈ C) (a : A) (ha : a ∈ menu (source q₀)) :
    ∃ q ∈ C, source q=source q₀ ∧ action q=a := by
  obtain ⟨q₁,hEdge⟩ := hNext q₀ hq₀
  have hq₁ := hC.2.1 q₀ hq₀ q₁ hEdge
  obtain ⟨n,_,hpath⟩ := reachable_short_path edge q₁ q₀ (hC.2.2 q₁ hq₁ q₀ hq₀)
  have hcycle : Path edge q₀ q₀ (n+1) := Path.cons hEdge hpath
  obtain ⟨w,hw0,hwN,hwe⟩ := hcycle.exists_walk
  have hwC : ∀ t, t ≤ n+1 → w t ∈ C := by
    intro t
    induction t with
    | zero => intro _; simpa only [hw0] using hq₀
    | succ t ih =>
        intro ht
        exact hC.2.1 (w t) (ih (by omega)) (w (t+1)) (hwe t (by omega))
  let x : ℕ → S := fun t => source (w t)
  let s := source q₀
  let r : ℕ → ℕ := fun t => residue (w t) s
  have hstep : ∀ t, t<n+1 → r (t+1) = (r t + if x t=s then 1 else 0)%(menu s).card := by
    intro t ht
    exact hRotor (w t) (hwC t (by omega)) (w (t+1)) (hwe t ht) s
  have hres : ∀ t, t ≤ n+1 → r t % (menu s).card =
      (r 0+visitsBefore x s t)%(menu s).card := by
    intro t ht
    exact rotor_residue_eq_visits_upto x s (menu s).card r t (fun k hk => hstep k (by omega))
  have hx0 : x 0=s := by simp only [x,s,hw0]
  have hvisit : 0 < visitsBefore x s (n+1) := by
    have hmono := visitsBefore_mono x s (show 1 ≤ n+1 by omega)
    have h1 : visitsBefore x s 1 = 1 := by simp [visitsBefore,hx0]
    omega
  have hrreturn : r (n+1)=r 0 := by simp only [r,hw0,hwN]
  have hreturn : (r 0+visitsBefore x s (n+1))%(menu s).card = r 0%(menu s).card := by
    have hh := hres (n+1) le_rfl
    rw [hrreturn] at hh
    exact hh.symm
  obtain ⟨t,ht,hxt,hact⟩ := returning_rotor_covers_menu x s (menu s) fallback (r 0) (n+1)
    hvisit hreturn a ha
  refine ⟨w t,hwC t (by omega),hxt,?_⟩
  rw [hAction (w t) (hwC t (by omega))]
  change cycleAction (menu (x t)) fallback (residue (w t) (x t))=a
  rw [hxt]
  change cycleAction (menu s) fallback (r t)=a
  calc
    cycleAction (menu s) fallback (r t) = cycleAction (menu s) fallback (r t%(menu s).card) :=
      (cycleAction_mod (menu s) fallback (r t)).symm
    _ = cycleAction (menu s) fallback ((r 0+visitsBefore x s t)%(menu s).card) := by rw [hres t (by omega)]
    _ = cycleAction (menu s) fallback (r 0+visitsBefore x s t) := cycleAction_mod _ _ _
    _ = a := hact

namespace FiniteChainHitting
omit [DecidableEq Q] in
/-- Normalization supplies a positive successor at every augmented vertex. -/
theorem rows_positive_successor (P : Rows Q) (s : Q) : ∃ t, 0 < P.row s t := by
  by_contra h
  push_neg at h
  have hs : (∑ t, P.row s t) ≤ 0 := Finset.sum_nonpos (fun t _ => h t)
  rw [P.normalized] at hs
  norm_num at hs
end FiniteChainHitting

end HiddenParity.Cost
