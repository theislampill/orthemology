import PythonExprBounds

namespace P02.PythonExpr

def ResourceFault (f : Fault) : Prop :=
  f = .stepLimit ∨ f = .integerStorage ∨ f = .exponentStorage

def OnlyResource {α : Type} : Result α → Prop
  | .ok _ => True
  | .error err => ResourceFault err.fault

theorem onlyResource_bind {α β : Type} (x : Result α) (f : α → Result β)
    (hx : OnlyResource x) (hf : ∀ a, OnlyResource (f a)) : OnlyResource (x >>= f) := by
  cases x with
  | error err => exact hx
  | ok a => exact hf a

theorem tick_only_resource (m : Meter) : OnlyResource (tick m) := by
  cases h : m.limit <;> simp [tick, h, OnlyResource, ResourceFault]
  split_ifs <;> simp [OnlyResource, ResourceFault]

theorem check_only_resource (m : Meter) (n : ℕ) : OnlyResource (check m n) := by
  cases h : m.maxBits <;> simp [check, h, OnlyResource, ResourceFault]
  split_ifs <;> simp [OnlyResource, ResourceFault]

theorem power_only_resource (m : Meter) (n : ℕ) : OnlyResource (power m n) := by
  cases h : m.maxBits <;> simp [power, h, OnlyResource, ResourceFault]
  split_ifs <;> simp [OnlyResource, ResourceFault]

theorem reference_only_resource (d : Dictionary) (e : PyExpr) (m : Meter) :
    OnlyResource (reference d e m) := by
  induction e generalizing m with
  | constant n =>
      apply onlyResource_bind _ _ (tick_only_resource m)
      intro m
      apply onlyResource_bind _ _ (check_only_resource m n)
      intro v
      trivial
  | reg r =>
      apply onlyResource_bind _ _ (tick_only_resource m)
      intro m
      trivial
  | pow2 a ih =>
      apply onlyResource_bind _ _ (tick_only_resource m)
      intro m
      apply onlyResource_bind _ _ (ih m)
      rintro ⟨av,am⟩
      apply onlyResource_bind _ _ (tick_only_resource am)
      intro bm
      apply onlyResource_bind _ _ (power_only_resource bm av)
      intro v
      trivial
  | binary op a b iha ihb =>
      apply onlyResource_bind _ _ (tick_only_resource m)
      intro m
      apply onlyResource_bind _ _ (iha m)
      rintro ⟨av,am⟩
      apply onlyResource_bind _ _ (ihb am)
      rintro ⟨bv,bm⟩
      apply onlyResource_bind _ _ (tick_only_resource bm)
      intro cm
      apply onlyResource_bind _ _ (check_only_resource cm (binaryValue op av bv))
      intro v
      trivial

/-- Starting from a well-formed expression, finite meter limits may stop the
machine, but neither pop underflow nor the final singleton check can fail. -/
theorem expression_failure_is_resource (d : Dictionary) (e : PyExpr) (m : Meter)
    (err : Failure) (h : expression d e m = .error err) : ResourceFault err.fault := by
  have hr := reference_only_resource d e m
  rw [← expression_eq_reference, h] at hr
  exact hr

theorem expression_no_stack_failure (d : Dictionary) (e : PyExpr) (m : Meter)
    (err : Failure) (h : expression d e m = .error err) :
    err.fault ≠ .valueStackUnderflow ∧ err.fault ≠ .stackInvariant := by
  have hf := expression_failure_is_resource d e m err h
  rcases hf with h | h | h <;> simp [h]

/-- Any two successful budget settings agree on the value. This statement does
not assert that success persists when a bound is changed. -/
theorem expression_success_values_agree (d : Dictionary) (e : PyExpr)
    (m₁ m₂ out₁ out₂ : Meter) (v₁ v₂ : ℕ)
    (h₁ : expression d e m₁ = .ok (v₁,out₁))
    (h₂ : expression d e m₂ = .ok (v₂,out₂)) : v₁ = v₂ :=
  (expression_success_sound d e m₁ out₁ v₁ h₁).trans
    (expression_success_sound d e m₂ out₂ v₂ h₂).symm

end P02.PythonExpr
