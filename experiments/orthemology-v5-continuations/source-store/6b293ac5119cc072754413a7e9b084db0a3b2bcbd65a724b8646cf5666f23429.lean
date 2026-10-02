/- Structural costs of the actual validated JSON/tagged-tuple representation.
Counts include container nodes, field-name dictionary keys, rule/tag strings,
and integer leaves, just as boundaries.bound_tree does. Aliases are unfolded
by occurrence. Host allocation/time and JSON lexical-byte guards stay separate. -/
import SourceCheckerProofs
namespace P03Source
open OrthemologyV2 OrthemologyV3

structure Shape where
  nodes : Nat
  height : Nat
  integersFit : Bool
  deriving Repr, DecidableEq

def typeShape : TypeCode → Shape
  | .var n => ⟨3, 1, decide (n < 2^256)⟩
  | .bottom => ⟨2, 1, true⟩
  | .arrow A B =>
      let a := typeShape A; let b := typeShape B
      ⟨2+a.nodes+b.nodes, 1+max a.height b.height, a.integersFit && b.integersFit⟩
  | .all A => let a := typeShape A; ⟨2+a.nodes, 1+a.height, a.integersFit⟩

def termShape : Term → Shape
  | .app f x =>
      let a := termShape f; let b := termShape x
      ⟨2+a.nodes+b.nodes, 1+max a.height b.height, true⟩
  | _ => ⟨2, 1, true⟩

def traceShape (trace : List Term) : Shape :=
  ⟨1+(trace.map (fun t => (termShape t).nodes)).foldl Nat.add 0,
   match trace with
   | [] => 0
   | _ => 1+(trace.map (fun t => (termShape t).height)).foldl max 0,
   true⟩

def proofShape : SourceProof → Shape
  | .i A => let a := typeShape A; ⟨4+a.nodes, 1+a.height, a.integersFit⟩
  | .k A B => let a := typeShape A; let b := typeShape B
      ⟨5+a.nodes+b.nodes, 1+max a.height b.height, a.integersFit && b.integersFit⟩
  | .s A B C => let a := typeShape A; let b := typeShape B; let c := typeShape C
      ⟨6+a.nodes+b.nodes+c.nodes, 1+max a.height (max b.height c.height),
       a.integersFit && b.integersFit && c.integersFit⟩
  | .app p q => let a := proofShape p; let b := proofShape q
      ⟨5+a.nodes+b.nodes, 1+max a.height b.height, a.integersFit && b.integersFit⟩
  | .allI p => let a := proofShape p; ⟨4+a.nodes, 1+a.height, a.integersFit⟩
  | .allE p A => let a := proofShape p; let b := typeShape A
      ⟨5+a.nodes+b.nodes, 1+max a.height b.height, a.integersFit && b.integersFit⟩
  | .reduce p trace => let a := proofShape p; let b := traceShape trace
      ⟨5+a.nodes+b.nodes, 1+max a.height b.height, a.integersFit⟩

def shapeFits (s : Shape) : Bool :=
  decide (s.nodes ≤ 20000) && decide (s.height ≤ 100) && s.integersFit

def outputCost (v : Term × TypeCode) : Nat := (termShape v.1).nodes + (typeShape v.2).nodes

def finish (v : Term × TypeCode) (prior : Nat) : Option ((Term × TypeCode) × Nat) :=
  let total := prior + outputCost v
  if shapeFits (termShape v.1) && shapeFits (typeShape v.2) && decide (total ≤ 2000000)
  then some (v, total) else none

/-- A resource-aware source evaluator. It independently retains plain outputs
and the actual aggregate structural work charge of every successful subtree.
No branch uses the target Cert checker or sourceCheckCore to make its decision. -/
def sourceRun (d : Nat) : SourceProof → Option ((Term × TypeCode) × Nat)
  | .i A => if sourceScoped d A then finish (.i, .arrow A A) 0 else none
  | .k A B => if sourceScoped d A && sourceScoped d B then
      finish (.k, .arrow A (.arrow B A)) 0 else none
  | .s A B C => if sourceScoped d A && sourceScoped d B && sourceScoped d C then
      finish (.s, .arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C))) 0 else none
  | .app p q =>
      match sourceRun d p, sourceRun d q with
      | some ((f, .arrow A B), fp), some ((x, X), xp) =>
          if A = X then finish (.app f x, B) (fp+xp) else none
      | _, _ => none
  | .allI p =>
      match sourceRun (d+1) p with
      | some ((t, B), work) => finish (t, .all B) work
      | none => none
  | .allE p A =>
      if sourceScoped d A then
        match sourceRun d p with
        | some ((t, .all B), work) =>
            let result := sourceSubstitute B A 0
            if sourceScoped d result then finish (t, result) work else none
        | _ => none
      else none
  | .reduce p trace =>
      match sourceRun d p with
      | some ((t, A), work) =>
          match sourceTrace t trace with
          | some u => finish (u, A) work
          | none => none
      | none => none

/-- Public validated-AST entry: exact initial type-depth and transport structure
bounds are refusals, not assumptions converting invalid input to success. -/
def sourceCheck (d : Nat) (p : SourceProof) : Option (Term × TypeCode) :=
  if decide (d ≤ 100) && shapeFits (proofShape p)
  then (sourceRun d p).map Prod.fst else none

theorem finish_value {v : Term × TypeCode} {prior work : Nat} {out : Term × TypeCode}
    (h : finish v prior = some (out, work)) : v = out := by
  simp only [finish] at h
  split at h
  next hy => exact congrArg (fun x => x.1) (Option.some.inj h)
  next hn => contradiction

theorem sourceRun_refines_core (p : SourceProof) (d : Nat) (out : Term × TypeCode) (work : Nat)
    (h : sourceRun d p = some (out, work)) : sourceCheckCore d p = some out := by
  induction p generalizing d out work with
  | i A =>
      simp only [sourceRun] at h
      split at h
      next hs => have hv := finish_value h; simp [sourceCheckCore, hs, hv]
      next hn => contradiction
  | k A B =>
      simp only [sourceRun] at h
      split at h
      next hs => have hv := finish_value h; simp [sourceCheckCore, hs, hv]
      next hn => contradiction
  | s A B C =>
      simp only [sourceRun] at h
      split at h
      next hs => have hv := finish_value h; simp [sourceCheckCore, hs, hv]
      next hn => contradiction
  | app p q ihp ihq =>
      simp only [sourceRun] at h
      cases hp : sourceRun d p with
      | none => simp [hp] at h
      | some pv =>
          rcases pv with ⟨⟨f, FT⟩, pw⟩
          cases hq : sourceRun d q with
          | none => simp [hp, hq] at h
          | some qv =>
              rcases qv with ⟨⟨x, X⟩, qw⟩
              cases FT with
              | var n => simp [hp, hq] at h
              | bottom => simp [hp, hq] at h
              | all A => simp [hp, hq] at h
              | arrow A B =>
                  simp only [hp, hq] at h
                  split at h
                  next he =>
                    have hv := finish_value h
                    simp [sourceCheckCore, ihp d (f, .arrow A B) pw hp, ihq d (x, X) qw hq, he, hv]
                  next hn => contradiction
  | allI p ih =>
      simp only [sourceRun] at h
      cases hp : sourceRun (d+1) p with
      | none => simp [hp] at h
      | some pv =>
          rcases pv with ⟨⟨t, A⟩, pw⟩
          simp only [hp] at h
          have hv := finish_value h
          simp [sourceCheckCore, ih (d+1) (t,A) pw hp, hv]
  | allE p A ih =>
      simp only [sourceRun] at h
      split at h
      next hs =>
        cases hp : sourceRun d p with
        | none => simp [hp] at h
        | some pv =>
            rcases pv with ⟨⟨t, T⟩, pw⟩
            cases T with
            | var n => simp [hp] at h
            | bottom => simp [hp] at h
            | arrow B C => simp [hp] at h
            | all B =>
                simp only [hp] at h
                split at h
                next hscope =>
                  have hv := finish_value h
                  simp [sourceCheckCore, hs, ih d (t,.all B) pw hp, hscope, hv]
                next hn => contradiction
      next hn => contradiction
  | reduce p trace ih =>
      simp only [sourceRun] at h
      cases hp : sourceRun d p with
      | none => simp [hp] at h
      | some pv =>
          rcases pv with ⟨⟨t,A⟩, pw⟩
          simp only [hp] at h
          cases ht : sourceTrace t trace with
          | none => simp [ht] at h
          | some u =>
              simp only [ht] at h
              have hv := finish_value h
              simp [sourceCheckCore, ih d (t,A) pw hp, ht, Option.map, hv]

theorem sourceCheck_refines_core {p : SourceProof} {d : Nat} {out : Term × TypeCode}
    (h : sourceCheck d p = some out) : sourceCheckCore d p = some out := by
  simp only [sourceCheck] at h
  split at h
  next hs =>
    cases hr : sourceRun d p with
    | none => simp [hr] at h
    | some result =>
        rcases result with ⟨value, work⟩
        simp only [hr, Option.map, Option.some.injEq] at h
        subst out
        exact sourceRun_refines_core p d value work hr
  next hn => contradiction

/-- The requested positive constructor square includes all runtime resource
refusals represented above and matches target acceptance AND output term/type. -/
theorem source_checker_constructor_erasure_square (p : SourceProof) (d : Nat) (out : Term × TypeCode)
    (h : sourceCheck d p = some out) :
    ∃ v, check d (encode p) = some v ∧ v.term = out.1 ∧ v.ty = out.2 := by
  obtain ⟨v,hv,ev⟩ := source_core_export_square p d out (sourceCheck_refines_core h)
  exact ⟨v,hv,congrArg Prod.fst ev,congrArg Prod.snd ev⟩

theorem source_checker_sound (p : SourceProof) (d : Nat) (out : Term × TypeCode)
    (h : sourceCheck d p = some out) (rho : Nat → Code) :
    (interpret out.2 rho).accepts out.1 := by
  obtain ⟨v,hv,ht,ha⟩ := source_checker_constructor_erasure_square p d out h
  have hs := checked_sound v rho
  rwa [ht,ha] at hs

#print axioms source_checker_constructor_erasure_square
#print axioms source_checker_sound
end P03Source
