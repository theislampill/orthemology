import Application
import ClosedProofCanonicalisation

/- Source reflection of generic-open compatible conversion. This proves closed-n
   source instances, not the universal bound-variable scalar-fusion judgment. -/
namespace ClosedScalarInstances
open OrthemologyV2 P01D P01AC
open P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (A End W Leaf scalarL scalarR c3 i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ImportedOpenTermTransport (interp embed)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

def reify : OpenTermStandardness.T → Poly
  | .var n => .var n
  | .i => .atom .i
  | .k => .atom .k
  | .s => .atom .s
  | .zero => .atom .zero
  | .one => .atom .one
  | .app f a => .app (reify f) (reify a)

theorem reify_conv {x y : OpenTermStandardness.T}
    (h : OpenTermStandardness.Conv x y) : PolyConvPlus (reify x) (reify y) := by
  induction h with
  | refl x => exact .refl _
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'
  | app h h' ih ih' => exact .app ih ih'
  | i x => exact .i _
  | k x y => exact .k _ _
  | s f g x => exact .s _ _ _

/-- The original bridge preserves source atoms rather than silently unpacking them. -/
theorem reify_embed (t : Term) : PolyConvPlus (.atom t) (reify (embed t)) := by
  induction t with
  | i | k | s | zero | one => exact .refl _
  | app f a ihf iha => exact (PolyConvPlus.bridge f a).trans (.app ihf iha)

/-- All original polynomial variables and atoms are retained up to actual conversion. -/
theorem reify_interp (p : Poly) :
    PolyConvPlus p (reify (interp p OpenTermStandardness.T.var)) := by
  induction p with
  | var n => exact .refl _
  | atom t => exact reify_embed t
  | app f a ihf iha => exact .app ihf iha

/-- Reflection at the generic source-variable valuation, not semantic completeness. -/
theorem generic_conversion_reflect {p q : Poly}
    (h : OpenTermStandardness.Conv
      (interp p OpenTermStandardness.T.var) (interp q OpenTermStandardness.T.var)) :
    PolyConvPlus p q :=
  (reify_interp p).trans ((reify_conv h).trans (reify_interp q).symm)

def scalarLeft (n : Poly) : Poly := .app (.app n (.var 1)) (.var 0)
def scalarRight (n : Poly) : Poly := .app (.app (.app FullPER.Application.originalQ n) (.var 1)) (.var 0)
def scalarInstance (n : Poly) : Ty := .all (.pi End (.pi A (.identity A (scalarLeft n) (scalarRight n))))
def c2 : Poly := abstract (abstract i)

theorem interp_closed {p : Poly} (hp : Scoped 0 p) (η ξ : Nat → OpenTermStandardness.T) :
    interp p η = interp p ξ := by
  induction p with
  | var n => exact False.elim (Nat.not_lt_zero n hp)
  | atom t => rfl
  | app f a ihf iha => exact congrArg₂ OpenTermStandardness.T.app (ihf hp.1) (iha hp.2)

theorem closed_church {n : Poly} (hn : HasE [] n N) :
    OpenTermStandardness.Church (interp n OpenTermStandardness.T.var) :=
by
  rw [interp_closed (ClosedProofCanonicalisation.has_scope hn) _ FullPER.zeroEnv]
  exact FullPER.fundamental hn FullPER.Application.emptyEnv _ _
    FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩

theorem iteration_interp (k : Nat) :
    interp (iterationPoly k) OpenTermStandardness.T.var =
      OpenTermStandardness.iter (.var 1) (.var 0) k := by
  induction k with
  | zero => rfl
  | succ k ih => exact congrArg (OpenTermStandardness.T.app (.var 1)) ih

/-- One finite count for each derivable closed source n; the source n is unchanged. -/
theorem source_uniform_iteration {n : Poly} (hn : HasE [] n N) :
    ∃ k, PolyConvPlus (scalarLeft n) (iterationPoly k) := by
  obtain ⟨k,hk⟩ := OpenTermStandardness.church_standard _ (closed_church hn)
  refine ⟨k,generic_conversion_reflect ?_⟩
  rw [iteration_interp]
  exact hk (.var 1) (.var 0)

/-- Actual source conversion for a closed-n instance with generic open f and a. -/
theorem closed_scalar_conversion {n : Poly} (hn : HasE [] n N) :
    PolyConvPlus (scalarLeft n) (scalarRight n) := by
  apply generic_conversion_reflect
  change OpenTermStandardness.Conv
    ((interp n OpenTermStandardness.T.var).app (.var 1) |>.app (.var 0))
    (((interp FullPER.Application.originalQ OpenTermStandardness.T.var).app
      (interp n OpenTermStandardness.T.var)).app (.var 1) |>.app (.var 0))
  rw [FullPER.Application.originalQ_eval]
  exact OpenTermStandardness.church_scalar_fusion _ (closed_church hn) _ _

/-- Finite iteration can be typed independently of any typing for n in this context. -/
theorem iteration_has (k : Nat) : Has [A,End] (iterationPoly k) A := by
  have hΓ : Ctx [End] := .ext .nil (ExactScalarFusion.End_form .nil)
  have hΔ : Ctx [A,End] := .ext hΓ (ExactScalarFusion.A_form hΓ)
  induction k with
  | zero => exact .var (.param hΔ) .zero
  | succ k ih =>
    exact EffectiveCompleteness.app_has (ExactScalarFusion.End_form hΔ)
      (ExactScalarFusion.A_form hΔ)
      (.var (ExactScalarFusion.End_form hΔ) (.succ .zero)) ih

theorem scalarLeft_scoped {n : Poly} (hn : Scoped 0 n) : Scoped 2 (scalarLeft n) :=
  ⟨⟨scoped_mono hn (Nat.zero_le 2),Nat.lt_succ_self 1⟩,Nat.zero_lt_succ 1⟩

theorem scalarRight_scoped {n : Poly} (hn : Scoped 0 n) : Scoped 2 (scalarRight n) :=
  ⟨⟨⟨scoped_mono (has_scoped P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has)
    (Nat.zero_le 2),scoped_mono hn (Nat.zero_le 2)⟩,Nat.lt_succ_self 1⟩,Nat.zero_lt_succ 1⟩

/-- The actual conversion rule types the original scalar endpoints. No HasE
    weakening principle or syntactic completeness is assumed. -/
theorem scalar_endpoints {n : Poly} (hn : HasE [] n N) :
    HasE [A,End] (scalarLeft n) A ∧ HasE [A,End] (scalarRight n) A := by
  obtain ⟨k,hk⟩ := source_uniform_iteration hn
  have hΔ : Ctx [A,End] := .ext (.ext .nil (ExactScalarFusion.End_form .nil))
    (ExactScalarFusion.A_form (.ext .nil (ExactScalarFusion.End_form .nil)))
  have ha := form_inclusion (ExactScalarFusion.A_form hΔ)
  have hs := ClosedProofCanonicalisation.has_scope hn
  have hl : HasE [A,End] (scalarLeft n) A :=
    .conv ha (has_inclusion (iteration_has k)) hk.symm (scalarLeft_scoped hs)
  exact ⟨hl,.conv ha hl (closed_scalar_conversion hn) (scalarRight_scoped hs)⟩

/-- A real open-source scalar identity for every derivable closed n. -/
theorem scalar_identity {n : Poly} (hn : HasE [] n N) :
    HasE [A,End] i (.identity A (scalarLeft n) (scalarRight n)) := by
  obtain ⟨hl,hr⟩ := scalar_endpoints hn
  have ha := ClosedProofCanonicalisation.formed hl
  exact .identityIntro (.identity ha hl hr) hl hr (closed_scalar_conversion hn)

/-- External quantification over closed derivations is discharged by a finite
    HasE proof for each n. This is not one proof with a bound n:N variable. -/
theorem closed_scalar_instance {n : Poly} (hn : HasE [] n N) :
    HasE [] c2 (scalarInstance n) := by
  have leaf := scalar_identity hn
  have hleaf := ClosedProofCanonicalisation.formed leaf
  have he := form_inclusion (ExactScalarFusion.End_form (Γ := []) .nil)
  have ha := form_inclusion (ExactScalarFusion.A_form
    (Ctx.ext .nil (ExactScalarFusion.End_form .nil)))
  have inner := FormE.pi ha hleaf
  have outer := FormE.pi he inner
  exact .allIntro (.all .nil outer)
    (.piIntro outer (.piIntro inner leaf (scoped_abstract trivial))
      (scoped_abstract (scoped_abstract trivial)))

/-- The instance type is literal substitution into the body of the frozen W. -/
theorem scalarInstance_exact {n : Poly} (hn : Scoped 0 n) :
    inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n =
      scalarInstance n := by
  have hq := has_scoped P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has
  simp [scalarInstance, scalarLeft, scalarRight, Leaf, scalarL, scalarR,
    A, End, arr, inst, wk, subst, psub, pup, P01F.cons, pren,
    ExactScalarFusion.psub_closed hn, ExactScalarFusion.psub_closed hq,
    FullPER.Application.originalQ]

theorem c3_apply (n : Poly) : PolyConvPlus (.app c3 n) c2 := by
  simpa [c3,c2,i,abstract,freeZero,drop,pren,psub] using
    (PolyConvPlus.k (abstract (abstract i)) n)

/-- The original fixed witness applied to each closed source n has the actual
    substituted body of W(originalQ). No outer Πn introduction is asserted. -/
theorem closed_scalar_instance_exact {n : Poly} (hn : HasE [] n N) :
    HasE [] (.app c3 n)
      (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n) := by
  rw [scalarInstance_exact (ClosedProofCanonicalisation.has_scope hn)]
  have h := closed_scalar_instance hn
  exact .conv (ClosedProofCanonicalisation.formed h) h (c3_apply n).symm
    ⟨ExactScalarFusion.c3_scoped 0,ClosedProofCanonicalisation.has_scope hn⟩

#print axioms generic_conversion_reflect
#print axioms source_uniform_iteration
#print axioms closed_scalar_conversion
#print axioms scalar_identity
#print axioms closed_scalar_instance
#print axioms closed_scalar_instance_exact
end ClosedScalarInstances
