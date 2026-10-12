import CodedScope

/- Exact finite tagged-code recognition for the four retained syntax sorts.
   No source Primcodable instance, arbitrary encoding, or Computable premise. -/
namespace ExactSyntaxValidity
open Encodable SourceFamilyComputability CodedScope
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000

theorem primrec_list_all {α β} [Primcodable α] [Primcodable β]
    {f : α → List β} {p : α → β → Bool} (hf : Primrec f) (hp : Primrec₂ p) :
    Primrec (fun a => (f a).all (p a)) := by
  apply (Primrec.list_foldr hf (Primrec.const true)
    (Primrec.and.comp (hp.comp Primrec.fst (Primrec.fst.comp Primrec.snd))
      (Primrec.snd.comp Primrec.snd)).to₂).of_eq
  intro a
  induction f a with
  | nil => rfl
  | cons b bs ih => simp only [List.foldr_cons, List.all_cons, ih]

theorem primrec_list_filter {α β} [Primcodable α] [Primcodable β]
    {f : α → List β} {p : α → β → Bool} (hf : Primrec f) (hp : Primrec₂ p) :
    Primrec (fun a => (f a).filter (p a)) := by
  apply (Primrec.list_foldr hf (Primrec.const [])
    (Primrec.cond (hp.comp Primrec.fst (Primrec.fst.comp Primrec.snd))
      (Primrec.list_cons.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd))
      (Primrec.snd.comp Primrec.snd)).to₂).of_eq
  intro a
  induction f a with
  | nil => rfl
  | cons b bs ih => simp only [List.foldr_cons, List.filter_cons, ih]; cases p a b <;> rfl

/-- A generic sorted, bounded dependency evaluator on natural syntax codes. -/
def evaluate (shape : Nat × Nat → Bool) (children : Nat × Nat → List (Nat × Nat))
    (b : Nat × Nat) : Bool :=
  shape b && (children b).all (fun d =>
    if _h : d.2 < b.2 then evaluate shape children d else false)
termination_by b.2

def boundedChildren (children : Nat × Nat → List (Nat × Nat)) (b : Nat × Nat) :
    List (Nat × Nat) := (children b).filter (fun d => decide (d.2 < b.2))

theorem primrec_evaluate {shape : Nat × Nat → Bool}
    {children : Nat × Nat → List (Nat × Nat)}
    (hs : Primrec shape) (hc : Primrec children) : Primrec (evaluate shape children) := by
  let bounds : Nat × Nat → Bool := fun b => (children b).all (fun d => decide (d.2 < b.2))
  have hb : Primrec bounds := primrec_list_all hc
    (Primrec.nat_lt.comp₂ (Primrec.snd.comp₂ Primrec₂.right) (Primrec.snd.comp₂ Primrec₂.left))
  have hd : Primrec (boundedChildren children) := primrec_list_filter hc
    (Primrec.nat_lt.comp₂ (Primrec.snd.comp₂ Primrec₂.right) (Primrec.snd.comp₂ Primrec₂.left))
  apply Primrec.nat_omega_rec' (evaluate shape children) (m := Prod.snd) (l := boundedChildren children)
    (g := fun b vals => some (shape b && bounds b && vals.all id)) Primrec.snd hd
  · exact Primrec.option_some.comp₂
      ((Primrec.and.comp (Primrec.and.comp (hs.comp Primrec.fst) (hb.comp Primrec.fst))
        (primrec_list_all Primrec.snd Primrec₂.right)).to₂)
  · intro b d hd
    exact of_decide_eq_true (List.mem_filter.mp hd).2
  · intro b
    rw [evaluate]
    congr 1
    apply Bool.eq_iff_iff.mpr
    simp only [bounds, List.all_map, Function.comp_apply, id_eq, Bool.and_eq_true, List.all_eq_true,
      boundedChildren, List.mem_filter, and_imp,
      decide_eq_true_eq, dite_eq_ite]
    constructor
    · rintro ⟨⟨hshape, hbounds⟩, hvals⟩
      refine ⟨hshape, ?_⟩
      intro d hd
      have hlt := hbounds d hd
      simp only [hlt, ↓reduceIte]
      exact hvals d hd hlt
    · rintro ⟨hshape, hvals⟩
      refine ⟨⟨hshape, ?_⟩, ?_⟩
      · intro d hd
        have hv := hvals d hd
        split_ifs at hv with h
        · exact h
      · intro d hd hlt
        simpa only [hlt, ↓reduceIte] using hvals d hd

/-- Specification theorem for a recursively generated sorted language. -/
theorem evaluate_exact {shape : Nat × Nat → Bool}
    {children : Nat × Nat → List (Nat × Nat)} {P : Nat × Nat → Prop}
    (rule : ∀ b, P b ↔ shape b = true ∧ ∀ d ∈ children b, P d)
    (bounds : ∀ b, shape b = true → ∀ d ∈ children b, d.2 < b.2)
    (b : Nat × Nat) : evaluate shape children b = true ↔ P b := by
  induction h : b.2 using Nat.strong_induction_on generalizing b with
  | h n ih =>
    rw [evaluate, rule]
    simp only [Bool.and_eq_true, List.all_eq_true]
    constructor
    · rintro ⟨hs, he⟩
      refine ⟨hs, ?_⟩
      intro d hd
      have hlt := bounds b hs d hd
      have hr := he d hd
      simp only [hlt, ↓reduceDIte] at hr
      exact (ih d.2 (by omega) d rfl).mp hr
    · rintro ⟨hs, hp⟩
      refine ⟨hs, ?_⟩
      intro d hd
      have hlt := bounds b hs d hd
      simp only [hlt, ↓reduceDIte]
      exact (ih d.2 (by omega) d rfl).mpr (hp d hd)

end ExactSyntaxValidity
