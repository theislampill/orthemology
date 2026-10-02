import P02A2.AllNParity
import P02A2.FiniteLaw
import Mathlib

/-! UNEXECUTED. Bind the recursive all-n counts to actual enumerated bit words,
not merely an arithmetic recurrence. Every mask has its original coordinate
order; a free mask coordinate denotes an omitted observable. -/
namespace P02A2.ParityBridge
open P02A2.AllNParity

def fits : List (Option Bool) → List Bool → Bool
  | [], [] => true
  | none::ms, _::xs => fits ms xs
  | some a::ms, b::xs => (a == b) && fits ms xs
  | _, _ => false

theorem solutions_mem {b : Bool} {ms : List (Option Bool)} {xs : List Bool} :
    xs ∈ solutions b ms ↔ fits ms xs = true ∧ P02A2.FiniteLaw.parity xs = b := by
  induction ms generalizing b xs with
  | nil => cases xs <;> cases b <;> simp [solutions, fits, P02A2.FiniteLaw.parity]
  | cons m ms ih =>
    cases xs with
    | nil => cases m <;> simp [solutions, fits]
    | cons x xs =>
      cases m with
      | none => cases x <;> cases b <;>
          simp [solutions, fits, P02A2.FiniteLaw.parity, ih]
      | some a => cases a <;> cases x <;> cases b <;>
          simp [solutions, fits, P02A2.FiniteLaw.parity, ih]

theorem fits_length {ms : List (Option Bool)} {xs : List Bool} (h : fits ms xs = true) :
    xs.length = ms.length := by
  induction ms generalizing xs with
  | nil => cases xs <;> simp_all [fits]
  | cons m ms ih =>
    cases xs with
    | nil => simp [fits] at h
    | cons x xs =>
      have ht : fits ms xs = true := by
        cases m with
        | none => exact h
        | some a => exact (Bool.and_eq_true_iff.mp h).2
      simp [ih ht]

theorem solutions_nodup (b : Bool) (ms : List (Option Bool)) :
    (solutions b ms).Nodup := by
  induction ms generalizing b with
  | nil => cases b <;> simp [solutions]
  | cons m ms ih =>
    cases m with
    | some a =>
      exact (ih _).map (by intro xs ys he; exact List.cons.inj he |>.2)
    | none =>
      rw [solutions, List.nodup_append]
      refine ⟨?_, ?_, ?_⟩
      · exact (ih b).map (by intro xs ys he; exact List.cons.inj he |>.2)
      · exact (ih (!b)).map (by intro xs ys he; exact List.cons.inj he |>.2)
      · intro xs hx hy
        rcases List.mem_map.mp hx with ⟨a, _, ha⟩
        rcases List.mem_map.mp hy with ⟨c, _, hc⟩
        have hf : (false : Bool) = true := List.cons.inj (ha.trans hc.symm) |>.1
        cases hf

theorem unrestricted_fits (xs : List Bool) : fits (List.replicate xs.length none) xs = true := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simpa [fits, List.replicate_succ] using ih

theorem solutions_filter (b : Bool) (ms : List (Option Bool)) :
    ((solutions b (List.replicate ms.length none)).filter (fits ms)).Perm (solutions b ms) := by
  apply (List.perm_ext_iff_of_nodup ((solutions_nodup b _).filter _) (solutions_nodup b ms)).mpr
  intro xs
  simp only [List.mem_filter, solutions_mem]
  constructor
  · rintro ⟨⟨_, hp⟩, hm⟩
    exact ⟨hm, hp⟩
  · rintro ⟨hm, hp⟩
    refine ⟨⟨?_, hp⟩, hm⟩
    rw [← fits_length hm]
    exact unrestricted_fits xs

noncomputable def probability (xs : List (List Bool)) (event : List Bool → Bool) : ℚ :=
  ((xs.filter event).length : ℚ)/(xs.length : ℚ)

theorem general_proper_probability (b : Bool) (ms : List (Option Bool))
    (h : 0 < free ms) :
    probability (solutions b (List.replicate ms.length none)) (fits ms) =
      1/(2:ℚ)^(fixed ms) := by
  unfold probability
  rw [(solutions_filter b ms).length_eq, solutions_length, solutions_length]
  exact proper_mask_marginal b ms h

theorem parity_target_probability (n : ℕ) (hn : 1 ≤ n) (b : Bool) :
    probability (solutions b (List.replicate n none))
      (fun xs => P02A2.FiniteLaw.parity xs == b) = 1 := by
  have hf : (solutions b (List.replicate n none)).filter
      (fun xs => P02A2.FiniteLaw.parity xs == b) = solutions b (List.replicate n none) := by
    apply List.filter_eq_self.mpr
    intro xs hx
    simp [(solutions_mem.mp hx).2]
  unfold probability
  rw [hf, solutions_length, full_parity_count n hn b]
  have hne : (2^(n-1) : ℚ) ≠ 0 := pow_ne_zero _ (by norm_num)
  norm_num only [Nat.cast_pow, Nat.cast_ofNat]
  exact div_self hne

-- Explicit finite mixture probabilities. This definition is the pushforward
-- of the mixture of uniform list positions and one extra point; it does not
-- assume that a mixture is uniform on the union of its support.
noncomputable def mixtureProbability (xs : List (List Bool)) (z : List Bool)
    (a : ℚ) (event : List Bool → Bool) : ℚ :=
  (1-a)*probability xs event + a*(if event z then 1 else 0)

theorem mixture_proper_profile (b : Bool) (ms : List (Option Bool)) (h : 0 < free ms)
    (z : List Bool) (a : ℚ) :
    mixtureProbability (solutions b (List.replicate ms.length none)) z a (fits ms) =
      (1-a)/(2:ℚ)^(fixed ms) + a*(if fits ms z then 1 else 0) := by
  unfold mixtureProbability
  rw [general_proper_probability b ms h]
  ring
end P02A2.ParityBridge
