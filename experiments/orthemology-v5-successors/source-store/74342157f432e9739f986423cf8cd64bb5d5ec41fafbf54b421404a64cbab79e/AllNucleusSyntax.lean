/- Literal-code translation of the accepted nucleus grammar. -/
import AllStructuralRename
import TypedStructural
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem form_arr {Γ A B} (ha : Form Γ A) (hb : Form Γ B) : Form Γ (arr A B) :=
  .pi ha (form_wk hb (form_ctx ha) ha)

theorem form_fin (C : TypeCode) {Γ : Tel} (hc : Ctx Γ) : Form Γ (fin C) := by
  induction C generalizing Γ with
  | var n => exact .param hc
  | bottom => exact .bottom hc
  | arrow A B ha hb => exact form_arr (ha hc) (hb hc)
  | all B ih => exact .all hc (ih (ctx_twk hc))

theorem fin_tsubst_congr (C : TypeCode) (τ υ : Nat → Ty)
    (h : ∀ n, n < finSupport C → τ n = υ n) : tsubst τ (fin C) = tsubst υ (fin C) := by
  induction C generalizing τ υ with
  | var n => exact h n (Nat.lt_succ_self n)
  | bottom => rfl
  | arrow A B ha hb =>
      simp only [fin,tsubst_arr]
      rw [ha τ υ (fun n hn => h n (Nat.lt_of_lt_of_le hn (Nat.le_max_left _ _))),
          hb τ υ (fun n hn => h n (Nat.lt_of_lt_of_le hn (Nat.le_max_right _ _)))]
  | all B ih =>
      change Ty.all (tsubst (tup τ) (fin B)) = Ty.all (tsubst (tup υ) (fin B))
      congr 1
      apply ih
      intro n hn
      cases n with
      | zero => rfl
      | succ n =>
          change twk (τ n) = twk (υ n)
          rw [h n (by change n < finSupport B - 1; omega)]

def finiteIdentity (C : TypeCode) : List Ty := (List.range (finSupport C)).map Ty.param

theorem finiteIdentity_length (C : TypeCode) : (finiteIdentity C).length = finSupport C := by
  simp [finiteIdentity]

theorem finiteIdentity_get (C : TypeCode) {n : Nat} (h : n < finSupport C) :
    typeImages (finiteIdentity C) n = .param n := by
  have gen : ∀ (xs : List Nat) n (hn : n < xs.length), typeImages (xs.map Ty.param) n = .param (xs[n]'hn) := by
    intro xs
    induction xs with
    | nil => intro n hn; exact False.elim (Nat.not_lt_zero n hn)
    | cons x xs ih =>
        intro n hn; cases n with
        | zero => rfl
        | succ n => exact ih n (Nat.lt_of_succ_lt_succ hn)
  exact (gen (List.range (finSupport C)) n (by simpa using h)).trans
    (congrArg Ty.param (List.getElem_range (by simpa using h)))

theorem finiteIdentity_action (C : TypeCode) : tsubst (typeImages (finiteIdentity C)) (fin C) = fin C := by
  rw [fin_tsubst_congr C _ Ty.param (fun n hn => finiteIdentity_get C hn)]
  exact mixed_id _

theorem finite_import {Γ C t} (hc : Ctx Γ) (h : FiniteDerives t C) : Has Γ (.atom t) (fin C) := by
  have hi : ∀ n, n < (finiteIdentity C).length → Form Γ (typeImages (finiteIdentity C) n) := by
    intro n hn
    rw [finiteIdentity_get C (by simpa only [finiteIdentity_length] using hn)]
    exact .param hc
  have hf : Form Γ (tsubst (typeImages (finiteIdentity C)) (fin C)) := by
    rw [finiteIdentity_action]; exact form_fin C hc
  simpa only [finiteIdentity_action] using Has.finite (finiteIdentity C) (by rw [finiteIdentity_length]; exact Nat.le_refl _) hi hf h

namespace Nucleus

def translate : P01TC.Ty → Ty
  | .param n => .param n
  | .bottom => .bottom
  | .allFinite C => .all (fin C)
  | .raw => .raw
  | .pi A B => .pi (translate A) (translate B)
  | .sigma A B => .sigma (translate A) (translate B)
  | .identity A p q => .identity (translate A) p q

def telescope (Γ : P01TC.Tel) : Tel := Γ.map translate

theorem translate_subst (A : P01TC.Ty) (σ : Nat → Poly) :
    translate (P01TC.subst σ A) = subst σ (translate A) := by
  induction A generalizing σ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | allFinite C => simp only [P01TC.subst,translate,subst,subst_fin]
  | pi A B ha hb => simp only [P01TC.subst,translate,subst,ha,hb]
  | sigma A B ha hb => simp only [P01TC.subst,translate,subst,ha,hb]
  | identity A p q ha => simp only [P01TC.subst,translate,subst,ha]

theorem translate_wk (A : P01TC.Ty) : translate (P01TC.wk A) = wk (translate A) := translate_subst A _
theorem translate_inst (B : P01TC.Ty) (a : Poly) :
    translate (P01TC.inst B a) = inst (translate B) a := translate_subst B _
theorem translate_motiveAt (B : P01TC.Ty) (y e : Poly) :
    translate (P01TC.motiveAt B y e) = motiveAt (translate B) y e := translate_subst B _
theorem translate_arr (A B : P01TC.Ty) : translate (P01TC.arr A B) = arr (translate A) (translate B) := by
  simp only [P01TC.arr,translate,translate_wk,arr]
theorem translate_fin (C : TypeCode) : translate (P01TC.fin C) = fin C := by
  induction C with
  | var n => rfl
  | bottom => rfl
  | all B ih => rfl
  | arrow A B ha hb => simp only [P01TC.fin,translate_arr,ha,hb,fin]
theorem telescope_theta (Γ : P01TC.Tel) (A : P01TC.Ty) (x : Poly) :
    telescope (P01TC.theta Γ A x) = theta (telescope Γ) (translate A) x := by
  simp only [P01TC.theta,telescope,List.map_cons,translate,translate_wk,theta]

theorem scoped_agrees (n : Nat) (p : Poly) : P01TC.Scoped n p ↔ Scoped n p := by
  induction p with
  | var k => exact Iff.rfl
  | atom t => exact Iff.rfl
  | app f a hf ha => exact and_congr hf ha

theorem lookup {Γ n A} (h : P01TC.Lookup Γ n A) : Lookup (telescope Γ) n (translate A) := by
  induction h with
  | zero => simpa only [telescope,List.map_cons,translate_wk] using (Lookup.zero (A := translate _) (Γ := telescope _))
  | succ h ih => simpa only [telescope,List.map_cons,translate_wk] using Lookup.succ ih

end Nucleus
end P01AC
