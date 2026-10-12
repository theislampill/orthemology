import JointSyntax

namespace JointCertificates
open P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def scopedDecidable : (n : Nat) → (p : Poly) → Decidable (Scoped n p)
  | n, .var k => inferInstanceAs (Decidable (k < n))
  | _, .atom _ => isTrue trivial
  | n, .app f a =>
    letI := scopedDecidable n f
    letI := scopedDecidable n a
    inferInstanceAs (Decidable (Scoped n f ∧ Scoped n a))
instance (n : Nat) (p : Poly) : Decidable (Scoped n p) := scopedDecidable n p

def typeScopedDecidable : (n : Nat) → (A : Ty) → Decidable (TyScoped n A)
  | _, .param _ => isTrue trivial
  | _, .bottom => isTrue trivial
  | _, .raw => isTrue trivial
  | n, .all B => typeScopedDecidable n B
  | n, .pi A B | n, .sigma A B =>
    letI := typeScopedDecidable n A
    letI := typeScopedDecidable (n+1) B
    inferInstanceAs (Decidable (TyScoped n A ∧ TyScoped (n+1) B))
  | n, .identity A p q =>
    letI := typeScopedDecidable n A
    inferInstanceAs (Decidable (TyScoped n A ∧ Scoped n p ∧ Scoped n q))
instance (n : Nat) (A : Ty) : Decidable (TyScoped n A) := typeScopedDecidable n A

inductive Claim where
  | ctxJ : Tel → Claim
  | formJ : Tel → Ty → Claim
  | hasJ : Tel → Poly → Ty → Claim
  | ctxE : Tel → Claim
  | formE : Tel → Ty → Claim
  | hasE : Tel → Poly → Ty → Claim
  deriving DecidableEq

def Claim.denote : Claim → Prop
  | .ctxJ Γ => JointCompletion.CtxJ Γ
  | .formJ Γ A => JointCompletion.FormJ Γ A
  | .hasJ Γ p A => JointCompletion.HasJ Γ p A
  | .ctxE Γ => P01AC.ExtensionalRepair.CtxE Γ
  | .formE Γ A => P01AC.ExtensionalRepair.FormE Γ A
  | .hasE Γ p A => P01AC.ExtensionalRepair.HasE Γ p A

def All {α : Type} (P : α → Prop) : List α → Prop
  | [] => True
  | x :: xs => P x ∧ All P xs

theorem all_iff_mem {α : Type} (P : α → Prop) (xs : List α) :
    All P xs ↔ ∀ x ∈ xs, P x := by
  induction xs with
  | nil => simp [All]
  | cons x xs ih => simp [All, ih]

theorem all_append {α : Type} (P : α → Prop) (xs ys : List α) :
    All P (xs ++ ys) ↔ All P xs ∧ All P ys := by
  simp [all_iff_mem, List.mem_append, or_imp, forall_and]

theorem all_ofFn {α : Type} {n : Nat} (P : α → Prop) (f : Fin n → α) :
    All P (List.ofFn f) ↔ ∀ i, P (f i) := by
  simp [all_iff_mem, List.mem_ofFn]

inductive Certificate (R : Type) where
  | node : R → List (Certificate R) → Certificate R

namespace Certificate
variable {R : Type}

def rule : Certificate R → R | .node r _ => r
def children : Certificate R → List (Certificate R) | .node _ cs => cs

def check (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool) :
    Certificate R → Bool
  | .node r cs => side r && decide (cs.map (fun c => conclusion c.rule) = premises r) &&
      cs.attach.all (fun c => check conclusion premises side c.val)
termination_by c => sizeOf c
decreasing_by
  have h := List.sizeOf_lt_of_mem c.property
  simp only [Certificate.node.sizeOf_spec] at *
  omega

/-- Equation form without membership-proof annotations, for kernel reduction
of concrete accepted/rejected certificate examples. -/
theorem check_node (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (r : R) (cs : List (Certificate R)) :
    check conclusion premises side (.node r cs) =
      (side r && decide (cs.map (fun c => conclusion c.rule) = premises r) &&
        cs.all (fun c => check conclusion premises side c)) := by
  rw [check]
  congr 1
  apply Bool.eq_iff_iff.mpr
  simp only [List.all_eq_true, List.mem_attach, forall_true_left, Subtype.forall]

 theorem check_sound (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (localSound : ∀ r, side r = true → All Claim.denote (premises r) → (conclusion r).denote)
    (c : Certificate R) (h : check conclusion premises side c = true) :
    (conclusion c.rule).denote := by
  cases hc : c with
  | node r cs =>
    rw [hc] at h
    simp only [check, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at h
    apply localSound r h.1.1
    rw [← h.1.2]
    apply (all_iff_mem _ _).mpr
    intro j hj
    obtain ⟨child,hchild,rfl⟩ := List.mem_map.mp hj
    exact check_sound conclusion premises side localSound child
      (h.2 ⟨child,hchild⟩ (List.mem_attach _ _))
termination_by sizeOf c
 decreasing_by
  have hh := List.sizeOf_lt_of_mem hchild
  simp only [hc, Certificate.node.sizeOf_spec] at *
  omega

/-- A requested root is checked explicitly, as well as every internal child. -/
def checkRoot (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (c : Certificate R) (j : Claim) : Bool :=
  check conclusion premises side c && decide (conclusion c.rule = j)

def Proved (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (j : Claim) : Prop := ∃ c, checkRoot conclusion premises side c j = true

theorem checkRoot_sound (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (localSound : ∀ r, side r = true → All Claim.denote (premises r) → (conclusion r).denote)
    (c : Certificate R) (j : Claim) (h : checkRoot conclusion premises side c j = true) : j.denote := by
  simp only [checkRoot, Bool.and_eq_true, decide_eq_true_eq] at h
  exact h.2 ▸ check_sound conclusion premises side localSound c h.1

theorem select_children (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (js : List Claim) (h : All (Proved conclusion premises side) js) :
    ∃ cs : List (Certificate R), cs.map (fun c => conclusion c.rule) = js ∧
      ∀ c ∈ cs, check conclusion premises side c = true := by
  induction js with
  | nil => exact ⟨[],rfl,by simp⟩
  | cons j js ih =>
    obtain ⟨c,hc⟩ := h.1
    simp only [checkRoot, Bool.and_eq_true, decide_eq_true_eq] at hc
    obtain ⟨cs,hs,ha⟩ := ih h.2
    refine ⟨c::cs, by simp only [List.map_cons, hc.2, hs], ?_⟩
    intro d hd
    rcases List.mem_cons.mp hd with rfl | hd
    · exact hc.1
    · exact ha d hd

theorem proved_rule (conclusion : R → Claim) (premises : R → List Claim) (side : R → Bool)
    (r : R) (hs : side r = true) (hp : All (Proved conclusion premises side) (premises r)) :
    Proved conclusion premises side (conclusion r) := by
  obtain ⟨cs,hcs,ha⟩ := select_children conclusion premises side (premises r) hp
  refine ⟨.node r cs, ?_⟩
  simp only [rule] at hcs
  simp only [checkRoot, check, rule, hs, hcs, decide_true, Bool.true_and, Bool.and_true,
    List.all_eq_true]
  intro c _
  exact ha c.val c.property

end Certificate
end JointCertificates
