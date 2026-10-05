/- Kernel-checked statements corresponding to §§8–9 of the accepted written
   Fourteenth identity proof. HasPlus is hypothetical and separately named;
   none of these theorems modifies the inherited P01AC calculus. -/
import IntensionalIdentityRelations
import IntensionalIdentityWitness

namespace P01AC.Intensional
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- No polynomial whatsoever inhabits the separating type in current Has. -/
theorem separation_no_has (r : Poly) : ¬ P01AC.Has [] r separationB := by
  intro h
  exact separation_contradiction (closed_identity_conversion h)

/-- The same global obstruction survives the exact atom/application bridge. -/
theorem separation_no_hasPlus (r : Poly) : ¬ Plus.HasPlus [] r separationB := by
  intro h
  exact separation_contradiction (plus_closed_identity_conversion h)

theorem separationA_formPlus : Plus.FormPlus [] separationA :=
  Plus.form_inclusion separationA_form

theorem separationP_hasPlus : Plus.HasPlus [] separationP separationA :=
  Plus.has_inclusion separationP_has

theorem separationQ_hasPlus : Plus.HasPlus [] separationQ separationA :=
  Plus.has_inclusion separationQ_has

theorem separationB_formPlus : Plus.FormPlus [] separationB :=
  Plus.form_inclusion separationB_form

/-- One explicit formed, closed type is fully inhabited by the unchanged F/G
    semantics and has no syntactic inhabitant in either exact rule system. -/
theorem intensional_identity_separation :
    P01AC.Form [] separationB ∧ Plus.FormPlus [] separationB ∧
    P01AC.Has [] separationP separationA ∧ P01AC.Has [] separationQ separationA ∧
    Plus.HasPlus [] separationP separationA ∧ Plus.HasPlus [] separationQ separationA ∧
    Scoped 0 separationP ∧ Scoped 0 separationQ ∧ Scoped 0 separationE ∧
    TyScoped 0 separationB ∧ TyParamScoped 0 separationB ∧
    (∀ ρ : OEnv, F separationB ρ zeroEnv (eval separationE zeroEnv) (eval separationE zeroEnv)) ∧
    (∀ r : REnv, G separationB r zeroEnv zeroEnv (eval separationE zeroEnv) (eval separationE zeroEnv)) ∧
    (¬ ∃ p, P01AC.Has [] p separationB) ∧
    (¬ ∃ p, Plus.HasPlus [] p separationB) := by
  refine ⟨separationB_form, separationB_formPlus, separationP_has, separationQ_has,
    separationP_hasPlus, separationQ_hasPlus, separationP_scoped, separationQ_scoped,
    separationE_scoped, separationB_scoped, separationB_type_scoped,
    fun ρ => separation_F ρ zeroEnv, fun r => separation_G r zeroEnv zeroEnv, ?_, ?_⟩
  · rintro ⟨p,hp⟩; exact separation_no_has p hp
  · rintro ⟨p,hp⟩; exact separation_no_hasPlus p hp

/-- At the exact five hypotheses, raw conversion supplies the common identity
    witness. The carrier may contain free type parameters. -/
theorem closed_identity_intro_iff {C : Ty} {p q : Poly}
    (hC : Plus.FormPlus [] C)
    (hp : Plus.HasPlus [] p C) (hq : Plus.HasPlus [] q C)
    (sp : Scoped 0 p) (sq : Scoped 0 q) :
    Plus.HasPlus [] (.atom .i) (.identity C p q) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv) := by
  constructor
  · exact plus_closed_identity_conversion
  · intro h
    exact .identityIntro (.identity hC hp hq) hp hq
      ((Plus.closed_conversion_iff sp sq).mpr h)

/-- Closed typed identity inhabitation is exactly conversion of its evaluated
    endpoints in the precise hypothetical HasPlus extension. -/
theorem closed_typed_identity_iff {C : Ty} {p q : Poly}
    (hC : Plus.FormPlus [] C)
    (hp : Plus.HasPlus [] p C) (hq : Plus.HasPlus [] q C)
    (sp : Scoped 0 p) (sq : Scoped 0 q) :
    (∃ r, Plus.HasPlus [] r (.identity C p q)) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv) := by
  constructor
  · rintro ⟨r,hr⟩
    exact plus_closed_identity_conversion hr
  · intro h
    exact ⟨.atom .i, (closed_identity_intro_iff hC hp hq sp sq).mpr h⟩

/-- All three statements of the written criterion, with formation recorded. -/
theorem closed_typed_identity_characterisation {C : Ty} {p q : Poly}
    (hC : Plus.FormPlus [] C)
    (hp : Plus.HasPlus [] p C) (hq : Plus.HasPlus [] q C)
    (sp : Scoped 0 p) (sq : Scoped 0 q) :
    Plus.FormPlus [] (.identity C p q) ∧
    ((∃ r, Plus.HasPlus [] r (.identity C p q)) ↔
      Plus.HasPlus [] (.atom .i) (.identity C p q)) ∧
    (Plus.HasPlus [] (.atom .i) (.identity C p q) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv)) := by
  refine ⟨.identity hC hp hq, ?_, closed_identity_intro_iff hC hp hq sp sq⟩
  constructor
  · intro h
    exact (closed_identity_intro_iff hC hp hq sp sq).mpr
      ((closed_typed_identity_iff hC hp hq sp sq).mp h)
  · intro h
    exact ⟨.atom .i,h⟩

end P01AC.Intensional
