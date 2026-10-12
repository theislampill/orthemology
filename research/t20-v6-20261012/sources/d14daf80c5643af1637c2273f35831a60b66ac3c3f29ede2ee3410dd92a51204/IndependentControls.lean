import ComputationLaws
namespace ComputationIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

-- Zero is original Has, with no rigidity premise.
example {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hs : Has Γ s (dependentStepType P)) :
    Has Γ ident (.identity (inst P zero) (sectionBody p s zero) p) :=
  section_zero_law hc hP hp hs

-- Successor is a fiber-correct propositional HasE identity under arbitrary HasE rigidity.
example {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hs : Has Γ s (dependentStepType P)) (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    ∃ e, HasE Γ e (.identity (inst P (.app P01AC.BooleanPrimitive.succPoly n))
      (sectionBody p s (.app P01AC.BooleanPrimitive.succPoly n))
      (.app (.app s n) (sectionBody p s n))) :=
  section_successor_law hc hP hp hs hr hn

-- Raw beta computes at the projected fold index, not an unproved raw equation at n.
example (p s n : Poly) : P01DF.PolyConv
    (sectionBody p s (.app P01AC.BooleanPrimitive.succPoly n))
    (.app (.app s (fstPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p))))
      (sectionBody p s n)) := section_succ_beta p s n

#print axioms section_successor_law
#print axioms section_zero_law
end ComputationIndependentReview
