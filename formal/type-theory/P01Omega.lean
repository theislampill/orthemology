/- Exact all-reduct Omega invariant; no finite census substituted for proof.
   New authored attempt-0003 proof candidate; UNCOMPILED at 4.19.0. -/
import P01Confluence
import NormalisationAndNumerals
namespace P01Source
open OrthemologyV2 OrthemologyV3

def tower : Nat → Term
  | 0 => duplicator
  | n+1 => .app .i (tower n)

def omegaShape (m n : Nat) := Term.app (tower m) (tower n)

theorem duplicator_normal : Normal duplicator := by
  intro u h
  cases h with
  | left h i =>
      cases h with
      | left h i => cases h
      | right s h => cases h
  | right si h => cases h

theorem tower_step {n u} (h : Step (tower n) u) :
    ∃ m, n = m+1 ∧ u = tower m := by
  induction n generalizing u with
  | zero => exact False.elim (duplicator_normal u h)
  | succ n ih =>
      rcases P01Candidates.i_successor h with rfl | ⟨v, hv, rfl⟩
      · exact ⟨n, rfl, rfl⟩
      · obtain ⟨m, rfl, rfl⟩ := ih hv
        exact ⟨m+1, rfl, rfl⟩

theorem shape_step {m n u} (h : Step (omegaShape m n) u) :
    ∃ a b, u = omegaShape a b := by
  cases m with
  | zero =>
      rcases P01Candidates.s_successor h with rfl | ⟨f, hf, e⟩ |
          ⟨g, hg, e⟩ | ⟨x, hx, rfl⟩
      · exact ⟨n+1, n+1, rfl⟩
      · cases hf
      · cases hg
      · obtain ⟨a, rfl, rfl⟩ := tower_step hx
        exact ⟨0, a, rfl⟩
  | succ m =>
      cases h with
      | left h x =>
          obtain ⟨a, ha, rfl⟩ := tower_step h
          exact ⟨a, n, rfl⟩
      | right f h =>
          obtain ⟨a, ha, rfl⟩ := tower_step h
          exact ⟨m+1, a, rfl⟩

theorem shape_has_step (m n : Nat) : ∃u, Step (omegaShape m n) u := by
  cases m with
  | zero => exact ⟨_, Step.s .i .i (tower n)⟩
  | succ m => exact ⟨_, Step.left (Step.i (tower m)) (tower n)⟩

theorem shape_red {m n u} (r : Red (omegaShape m n) u) :
    ∃a b, u = omegaShape a b := by
  have aux : ∀ {t u}, Red t u → (∃a b, t = omegaShape a b) →
      ∃a b, u = omegaShape a b := by
    intro t u r
    induction r with
    | refl => exact id
    | tail h r ih =>
        rintro ⟨a,b,rfl⟩
        exact ih (shape_step h)
  exact aux r ⟨m,n,rfl⟩

theorem omega_no_normal_reduct {u} (r : Red omega u) : ¬ Normal u := by
  have r' : Red (omegaShape 0 0) u := r
  obtain ⟨a,b,rfl⟩ := shape_red r'
  obtain ⟨v,hv⟩ := shape_has_step a b
  exact fun hn => hn v hv

/-- Unconditional nonrepresentability modulo *source* conversion, using direct
    reducibility and source Church-Rosser, not target-conversion reflection. -/
theorem omega_no_finite_representative :
    ¬ ∃u A, FiniteDerives u A ∧ Conv omega u := by
  rintro ⟨u,A,hu,hc⟩
  obtain ⟨n,hr,hn⟩ := finite_normal_form hu
  have hc' : Conv omega n := .trans hc (red_conv hr)
  obtain ⟨w,hw,hnw⟩ := conv_join hc'
  have e : w = n := normal_red hn hnw
  subst w
  exact omega_no_normal_reduct hw hn

/-- This is membership in the unchanged canonical semantic Code, in contrast to
    the normalisation-only candidate interpretation of its bottom tag. -/
theorem omega_semantic_bottom_arrow : (Code.arrow Code.bottom Code.bottom).accepts omega := by
  intro x hx
  exact False.elim hx
end P01Source
