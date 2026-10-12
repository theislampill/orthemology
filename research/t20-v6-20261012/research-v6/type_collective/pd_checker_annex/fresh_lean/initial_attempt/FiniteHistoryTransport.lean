import CheckerStateObservation

namespace PDCheckerFiniteHistory
noncomputable section

abbrev History (A O : Type*) := List (A × O)

def step {S A O : Type*} (K : S → A → PMF (O × S))
    (policy : History A O → PMF A) (law : PMF (History A O × S)) :
    PMF (History A O × S) :=
  law.bind fun hs => (policy hs.1).bind fun a =>
    (K hs.2 a).map fun rs => (hs.1 ++ [(a, rs.1)], rs.2)

def eraseHistory {X S A O : Type*} (e : X → S)
    (hx : History A O × X) : History A O × S := (hx.1, e hx.2)

theorem step_erasure {X S A O : Type*}
    (J : X → A → PMF (O × X)) (K : S → A → PMF (O × S)) (e : X → S)
    (rows : ∀ x a, (J x a).map (fun rx => (rx.1, e rx.2)) = K (e x) a)
    (policy : History A O → PMF A) (law : PMF (History A O × X)) :
    (step J policy law).map (eraseHistory e) =
      step K policy (law.map (eraseHistory e)) := by
  unfold step
  rw [PMF.map_bind, PMF.bind_map]
  apply congrArg (PMF.bind law)
  funext hx
  rw [PMF.map_bind]
  apply congrArg (PMF.bind (policy hx.1))
  funext a
  rw [PMF.map_comp]
  change (J hx.2 a).map (fun rx => (hx.1 ++ [(a, rx.1)], e rx.2)) = _
  rw [← rows hx.2 a, PMF.map_comp]
  rfl

def finiteLaw {S A O : Type*} (K : S → A → PMF (O × S))
    (policy : History A O → PMF A) (initial : PMF S) : ℕ → PMF (History A O × S)
  | 0 => initial.map fun s => ([], s)
  | n + 1 => step K policy (finiteLaw K policy initial n)

theorem finite_history_erasure {X S A O : Type*}
    (J : X → A → PMF (O × X)) (K : S → A → PMF (O × S)) (e : X → S)
    (rows : ∀ x a, (J x a).map (fun rx => (rx.1, e rx.2)) = K (e x) a)
    (policy : History A O → PMF A) (nu : PMF X) (mu : PMF S)
    (initial : nu.map e = mu) (n : ℕ) :
    (finiteLaw J policy nu n).map (eraseHistory e) = finiteLaw K policy mu n := by
  induction n with
  | zero =>
    simp only [finiteLaw, PMF.map_comp]
    rw [← initial, PMF.map_comp]
    rfl
  | succ n ih =>
    simp only [finiteLaw]
    rw [step_erasure J K e rows policy, ih]

def observedLift {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : PDChecker.Machine Q Γ) (x : PDChecker.LiftState m Q Γ)
    (a : PDChecker.Action Γ) : PMF (PDChecker.Receipt × PDChecker.LiftState m Q Γ) :=
  (PDChecker.liftedKernel M x a).map fun y => (PDChecker.observe y, y)

theorem actual_checker_finite_history {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    [Nonempty (Fin m)] (M : PDChecker.Machine Q Γ)
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m)
    (policy : History (PDChecker.Action Γ) PDChecker.Receipt → PMF (PDChecker.Action Γ))
    (n : ℕ) :
    (finiteLaw (observedLift M) policy (PDChecker.initialLiftBelief tape q0 h0) n).map
      (eraseHistory PDChecker.erase) =
      finiteLaw (PDChecker.kernel M) policy (PDChecker.initialBelief tape q0 h0) n := by
  apply finite_history_erasure
  · intro x a
    simp only [observedLift, PMF.map_comp]
    exact PDChecker.lifted_joint_row_exact M x a
  · exact PDChecker.initial_lift_erases tape q0 h0

theorem actual_checker_observable_history {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    [Nonempty (Fin m)] (M : PDChecker.Machine Q Γ)
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m)
    (policy : History (PDChecker.Action Γ) PDChecker.Receipt → PMF (PDChecker.Action Γ))
    (n : ℕ) :
    (finiteLaw (observedLift M) policy (PDChecker.initialLiftBelief tape q0 h0) n).map Prod.fst =
      (finiteLaw (PDChecker.kernel M) policy (PDChecker.initialBelief tape q0 h0) n).map Prod.fst := by
  rw [← actual_checker_finite_history M tape q0 h0 policy n, PMF.map_comp]
  rfl

-- A pre-action receipt changes an observation-history policy when supplied on one side only.
def initialSensitivePolicy (receipts : List PDChecker.Receipt) : PMF Bool :=
  PMF.pure (!receipts.isEmpty)

theorem misaligned_initial_receipt_changes_action :
    initialSensitivePolicy [] ≠ initialSensitivePolicy [.ordinary] := by
  intro h
  have hv := congrArg (fun p : PMF Bool => p false) h
  simp [initialSensitivePolicy, PMF.pure_apply] at hv

#print axioms step_erasure
#print axioms finite_history_erasure
#print axioms actual_checker_finite_history
#print axioms actual_checker_observable_history
#print axioms misaligned_initial_receipt_changes_action

end
end PDCheckerFiniteHistory
