import GlobalCountBudget

noncomputable section
namespace HiddenParity.Cost
open HiddenParity.Sufficiency
variable {S A : Type*} [DecidableEq S] [DecidableEq A]

/-- Every already-consumed source visit index occurs before the given finite
horizon. This finite version does not assume a recurrent/fair path. -/
theorem visit_index_before_horizon (x : ℕ → S) (s : S) (T k : ℕ)
    (hk : k < visitsBefore x s T) :
    ∃ t, t < T ∧ x t = s ∧ visitsBefore x s t = k := by
  have hex : ∃ t, k < visitsBefore x s t := ⟨T,hk⟩
  have hfirst := Nat.find_spec hex
  have hle := Nat.find_min' hex hk
  have hne : Nat.find hex ≠ 0 := by
    intro hz
    rw [hz] at hfirst
    change k < 0 at hfirst
    omega
  obtain ⟨t,ht⟩ := Nat.exists_eq_succ_of_ne_zero hne
  have hbefore := Nat.find_min hex (show t < Nat.find hex by omega)
  rw [ht,visitsBefore] at hfirst
  by_cases hs : x t = s
  · rw [if_pos hs] at hfirst
    exact ⟨t,by omega,hs,by omega⟩
  · rw [if_neg hs] at hfirst
    omega

/-- In one full round of departures from s, every active action occurs. The
entry offset is arbitrary and need not be zero after a mode/support change. -/
theorem finite_cycle_covers_menu (x : ℕ → S) (s : S)
    (F : Finset A) (fallback : A) (offset T : ℕ)
    (hvis : F.card ≤ visitsBefore x s T) (a : A) (ha : a ∈ F) :
    ∃ t, t < T ∧ x t = s ∧ cycleAction F fallback (offset+visitsBefore x s t) = a := by
  obtain ⟨j,hlo,hhi,hcycle⟩ := exists_near_cycle_barrier F fallback a ha offset
  have hk : j-offset < visitsBefore x s T := by omega
  obtain ⟨t,ht,hxs,hcount⟩ := visit_index_before_horizon x s T (j-offset) hk
  refine ⟨t,ht,hxs,?_⟩
  rw [hcount,show offset+(j-offset)=j by omega]
  exact hcycle

/-- Returning to the same source residue after a positive number of departures
forces at least a full active-menu round. -/
theorem returning_residue_has_full_round (d offset count : ℕ) (hcount : 0 < count)
    (hreturn : (offset+count)%d=offset%d) : d ≤ count := by
  have h : Nat.ModEq d (offset+count) (offset+0) := by simpa only [Nat.add_zero,Nat.ModEq] using hreturn
  have hc : Nat.ModEq d count 0 := Nat.ModEq.add_left_cancel (Nat.ModEq.refl offset) h
  have hdvd : d ∣ count := Nat.dvd_of_mod_eq_zero (by simpa only [Nat.ModEq,Nat.zero_mod] using hc)
  exact Nat.le_of_dvd hcount hdvd

/-- A positive source-containing closed rotor walk covers every retained
source action. This is a graph-cycle fact, not an assumed stochastic fairness
property of the controller. -/
theorem returning_rotor_covers_menu (x : ℕ → S) (s : S)
    (F : Finset A) (fallback : A) (offset T : ℕ)
    (hvis : 0 < visitsBefore x s T)
    (hreturn : (offset+visitsBefore x s T)%F.card=offset%F.card)
    (a : A) (ha : a ∈ F) :
    ∃ t, t < T ∧ x t = s ∧ cycleAction F fallback (offset+visitsBefore x s t) = a :=
  finite_cycle_covers_menu x s F fallback offset T
    (returning_residue_has_full_round F.card offset _ hvis hreturn) a ha

/-- Literal residue recursion agrees with the global offset plus local source
visits. This is the finite-state representation of the actual counter rule. -/
theorem rotor_residue_eq_visits (x : ℕ → S) (s : S) (d : ℕ)
    (residue : ℕ → ℕ)
    (hstep : ∀ n, residue (n+1) = (residue n + if x n=s then 1 else 0)%d)
    (T : ℕ) : residue T % d = (residue 0 + visitsBefore x s T)%d := by
  induction T with
  | zero => simp [visitsBefore]
  | succ T ih =>
      rw [hstep,Nat.mod_mod,visitsBefore]
      calc
        (residue T + if x T=s then 1 else 0)%d =
            (residue T%d + if x T=s then 1 else 0)%d  := by rw [Nat.mod_add_mod]
        _ = ((residue 0+visitsBefore x s T)%d + if x T=s then 1 else 0)%d := by rw [ih]
        _ = (residue 0+(visitsBefore x s T + if x T=s then 1 else 0))%d  := by rw [Nat.mod_add_mod,Nat.add_assoc]

/-- The residue identity needs the literal recursion only before the finite
horizon; a graph walk may end there. -/
theorem rotor_residue_eq_visits_upto (x : ℕ → S) (s : S) (d : ℕ)
    (residue : ℕ → ℕ) (T : ℕ)
    (hstep : ∀ n, n<T → residue (n+1) = (residue n + if x n=s then 1 else 0)%d) :
    residue T % d = (residue 0 + visitsBefore x s T)%d := by
  induction T with
  | zero => simp [visitsBefore]
  | succ T ih =>
      have hi := ih (fun n hn => hstep n (by omega))
      rw [hstep T (by omega),Nat.mod_mod,visitsBefore]
      calc
        (residue T + if x T=s then 1 else 0)%d =
            (residue T%d + if x T=s then 1 else 0)%d := by rw [Nat.mod_add_mod]
        _ = ((residue 0+visitsBefore x s T)%d + if x T=s then 1 else 0)%d := by rw [hi]
        _ = (residue 0+(visitsBefore x s T + if x T=s then 1 else 0))%d := by rw [Nat.mod_add_mod,Nat.add_assoc]

omit [DecidableEq A] in
/-- The actual source cycle depends only on the finite residue. -/
theorem cycleAction_mod (F : Finset A) (fallback : A) (n : ℕ) :
    cycleAction F fallback (n%F.card) = cycleAction F fallback n := by
  have hcard : Fintype.card F = F.card := Fintype.card_coe F
  simp only [cycleAction]
  split_ifs with h
  · simp only [hcard,Nat.mod_mod]
  · rfl

end HiddenParity.Cost
