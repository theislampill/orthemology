import TypedObserver
import InternalGraph

namespace TypedStructuredObserver
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly inputNumeral_has app_has)
open P01AC.BooleanPrimitive (closed_has N_subst)
open P01AC.ExtensionalRepair.InternalGraph (poly_beta pair_first)
open P01F (cons)
set_option maxRecDepth 8192

/-- These are exact open source conversion proofs, not observations only at Raw. -/
theorem numeral_apply (k : Nat) (f a : Poly) : P01DF.PolyConv
    (.app (.app (inputNumeral k) f) a)
    (psub (cons a Poly.var) (psub (pup (cons f Poly.var)) (iterationPoly k))) := by
  have h1 := poly_beta (abstract (iterationPoly k)) f
  have h2 := poly_beta (psub (pup (cons f Poly.var)) (iterationPoly k)) a
  simp only [← abstraction_naturality] at h1
  exact (P01DF.PolyConv.app h1 (.refl a)).trans h2

theorem numeral_zero_apply (f a : Poly) :
    P01DF.PolyConv (.app (.app (inputNumeral 0) f) a) a := by
  simpa only [iterationPoly, psub, pup, cons] using numeral_apply 0 f a

theorem numeral_one_apply (f a : Poly) :
    P01DF.PolyConv (.app (.app (inputNumeral 1) f) a) (.app f a) := by
  simpa [iterationPoly, psub, pup, cons, pren, psub_comp] using numeral_apply 1 f a

theorem step_beta (f s : Poly) : P01DF.PolyConv (.app (step f) s)
    (pairPoly (.app f (fstPoly s)) (.atom .i)) := by
  have h := poly_beta (body f) s
  simpa [step, body, pairPoly, fstPoly, psub, pren, psub_comp, cons] using h

theorem zero_observation (f a : Poly) :
    P01DF.PolyConv (observe (inputNumeral 0) f a) a :=
  (P01DF.PolyConv.app (numeral_zero_apply (step f) (seed a)) (.refl _)).trans
    (pair_first a (.atom .i))

theorem one_observation (f a : Poly) :
    P01DF.PolyConv (observe (inputNumeral 1) f a) (.app f a) := by
  have hn := P01DF.PolyConv.app (numeral_one_apply (step f) (seed a)) (.refl (.atom .k))
  have hb := P01DF.PolyConv.app (step_beta f (seed a)) (.refl (.atom .k))
  exact hn.trans (hb.trans ((InternalGraph.pair_first _ _).trans
    (.app (.refl f) (pair_first a (.atom .i)))))

theorem numeral_observer_has {Γ B f a} (k : Nat)
    (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    Has Γ (observe (inputNumeral k) f a) B :=
  observe_has (closed_has (inputNumeral_has k) N_subst (form_ctx (has_form ha))) hf ha

theorem zero_source_identity {Γ B f a}
    (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    HasE Γ (.atom .i) (.identity B (observe (inputNumeral 0) f a) a) := by
  have ho := has_inclusion (numeral_observer_has 0 hf ha)
  have ha' := has_inclusion ha
  exact .identityIntro (.identity (form_inclusion (has_form ha)) ho ha') ho ha'
    (Intensional.Plus.polyConv_inclusion (zero_observation f a))

theorem one_source_identity {Γ B f a}
    (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    HasE Γ (.atom .i) (.identity B (observe (inputNumeral 1) f a) (.app f a)) := by
  have ho := has_inclusion (numeral_observer_has 1 hf ha)
  have hfa := has_inclusion (app_has (has_form hf) (has_form ha) hf ha)
  exact .identityIntro (.identity (form_inclusion (has_form ha)) ho hfa) ho hfa
    (Intensional.Plus.polyConv_inclusion (one_observation f a))

/-- The source permits distinct named B-values and a typed update f:B→B.
No Raw declarations occur. Their semantic values need not be source-definable. -/
def ProbeContext : Tel := [.param 0, arr (.param 0) (.param 0), N]

theorem probe_context : Ctx ProbeContext := by
  have cn : Ctx [N] := .ext .nil (EffectiveCompleteness.N_form .nil)
  have cf : Ctx [arr (.param 0) (.param 0), N] :=
    .ext cn (form_arr (.param cn) (.param cn))
  exact .ext cf (.param cf)

theorem probe_a : Has ProbeContext (.var 0) (.param 0) := .var (.param probe_context) .zero

theorem probe_f : Has ProbeContext (.var 1) (arr (.param 0) (.param 0)) :=
  .var (form_arr (.param probe_context) (.param probe_context)) (.succ .zero)

theorem probe_n : Has ProbeContext (.var 2) N :=
  .var (EffectiveCompleteness.N_form probe_context) (.succ (.succ .zero))

theorem probe_all :
    HasE ProbeContext (observe (.var 2) (.var 1) (.var 0)) (.all (.param 1)) :=
  has_inclusion (observe_all_has probe_n probe_f probe_a)

theorem probe_zero_identity : HasE ProbeContext (.atom .i)
    (.identity (.param 0) (observe (inputNumeral 0) (.var 1) (.var 0)) (.var 0)) :=
  zero_source_identity probe_f probe_a

theorem probe_one_identity : HasE ProbeContext (.atom .i)
    (.identity (.param 0) (observe (inputNumeral 1) (.var 1) (.var 0))
      (.app (.var 1) (.var 0))) := one_source_identity probe_f probe_a


/-- A constant B-endomap is supplied by typed K applied to b, not by assuming
that the candidate contains the entire function space. -/
def constUpdate (b : Poly) : Poly := .app (.atom .k) b

theorem constUpdate_has {Γ B b} (hb : Has Γ b B) :
    Has Γ (constUpdate b) (arr B B) := by
  have hB := has_form hb
  have hBB := form_arr hB hB
  exact app_has (form_arr hB hBB) hBB (.k hB hB (form_arr hB hBB)) hb

theorem one_constant_observation (a b : Poly) :
    P01DF.PolyConv (observe (inputNumeral 1) (constUpdate b) a) b :=
  (one_observation (constUpdate b) a).trans (.k b a)

theorem one_constant_source_identity {Γ B a b}
    (ha : Has Γ a B) (hb : Has Γ b B) :
    HasE Γ (.atom .i) (.identity B
      (observe (inputNumeral 1) (constUpdate b) a) b) := by
  have ho := has_inclusion (numeral_observer_has 1 (constUpdate_has hb) ha)
  have hb' := has_inclusion hb
  exact .identityIntro (.identity (form_inclusion (has_form hb)) ho hb') ho hb'
    (Intensional.Plus.polyConv_inclusion (one_constant_observation a b))

#print axioms constUpdate_has
#print axioms one_constant_source_identity

#print axioms zero_observation
#print axioms one_observation
#print axioms zero_source_identity
#print axioms one_source_identity
#print axioms probe_all
#print axioms probe_zero_identity
#print axioms probe_one_identity
end TypedStructuredObserver
