/- Finite reduction certificates and the refusal-preserving proof-replay boundary.
   Python is NOT assumed to be a proof kernel. New source, UNCOMPILED at 4.19.0. -/
import P01ContextualJ
namespace P01Certificate
open OrthemologyV2 OrthemologyV3

inductive Direction where
  | left | right
  deriving DecidableEq, Repr
abbrev Address := List Direction

def root (t : Term) : Option {u : Term // Step t u} := match t with
  | .app .i x => some ⟨x,.i x⟩
  | .app (.app .k x) y => some ⟨x,.k x y⟩
  | .app (.app (.app .s f) g) x => some ⟨.app (.app f x) (.app g x),.s f g x⟩
  | _ => none

def stepAt : (t : Term) → Address → Option {u : Term // Step t u}
  | t, [] => root t
  | .app f x, .left::rest => match stepAt f rest with
      | none => none
      | some g => some ⟨.app g.val x,.left g.property x⟩
  | .app f x, .right::rest => match stepAt x rest with
      | none => none
      | some y => some ⟨.app f y.val,.right f y.property⟩
  | _, _ => none

def replay : (t : Term) → List Address → Option {u : Term // Red t u}
  | t, [] => some ⟨t,.refl t⟩
  | t, a::rest => match stepAt t a with
      | none => none
      | some u => match replay u.val rest with
          | none => none
          | some v => some ⟨v.val,.tail u.property v.property⟩

def checkJoin (t u : Term) (l r : List Address) : Option (PLift (Conv t u)) :=
  match replay t l, replay u r with
  | some n, some m =>
      if h : n.val = m.val then
        some ⟨.trans (P01Source.red_conv n.property)
          (.symm (P01Source.red_conv (h.symm ▸ m.property)))⟩
      else none
  | _, _ => none

theorem replay_sound (t : Term) (p : List Address)
    (u : {u : Term // Red t u}) (_h : replay t p = some u) : Red t u.val := u.property

theorem join_sound (t u : Term) (l r : List Address)
    (p : Conv t u) (_h : checkJoin t u l r = some ⟨p⟩) : Conv t u := p

/-- A closed source type/term commitment carried alongside the actual canonical
    Checked object. These equalities are kernel obligations, not JSON booleans. -/
structure FiniteEnvelope (t : Term) (A : TypeCode) where
  checked : OrthemologyV3.Checked
  term_binding : checked.term = t
  type_binding : checked.ty = A

theorem finite_envelope_sound {t A} (e : FiniteEnvelope t A) : FiniteDerives t A := by
  have h := e.checked.valid
  rw [e.term_binding,e.type_binding] at h
  exact h

theorem finite_envelope_SN {t A} (e : FiniteEnvelope t A) : P01Candidates.SN t :=
  P01Candidates.finite_SN (finite_envelope_sound e)

/-- The new dependent target is a different interface from canonical Cert.
    It binds the actual tracked program and the exact intrinsic contextual type.
    A frontend label cannot manufacture this object. -/
structure DependentEnvelope (Γ : P01D.Context) (A : P01D.Ty Γ) (p : P01D.Poly) where
  checked : P01D.Tm Γ A
  code_binding : checked.code = p

theorem dependent_envelope_sound {Γ A p} (e : DependentEnvelope Γ A p)
    {γ δ} (h : Γ.eqv γ δ) :
    (A.obj γ).rel (P01D.eval p (Γ.environment γ)) (P01D.eval p (Γ.environment δ)) := by
  have he := e.checked.valid h
  rw [e.code_binding] at he
  exact he

/-- Stage distinction: no kernel object is produced by merely labelling a JSON
    result ACCEPTED. The replay stage returns either refusal or real evidence. -/
inductive ReplayResult (Γ : P01D.Context) (A : P01D.Ty Γ) (p : P01D.Poly) where
  | refused : String → ReplayResult Γ A p
  | accepted : DependentEnvelope Γ A p → ReplayResult Γ A p

def acceptedProof {Γ A p} : ReplayResult Γ A p → Option (DependentEnvelope Γ A p)
  | .refused _ => none
  | .accepted e => some e

theorem refusal_preserved {Γ A p} (reason : String) :
    acceptedProof (ReplayResult.refused (Γ:=Γ) (A:=A) (p:=p) reason) = none := rfl

theorem accepted_replay_sound {Γ A p} (r : ReplayResult Γ A p)
    (e : DependentEnvelope Γ A p) (_h : acceptedProof r = some e)
    {γ δ} (hγ : Γ.eqv γ δ) :
    (A.obj γ).rel (P01D.eval p (Γ.environment γ)) (P01D.eval p (Γ.environment δ)) :=
  dependent_envelope_sound e hγ

/-- The exact canonical TypeCode image inside the new dependent type vocabulary.
    Resource refusal and this syntax obstruction concern TOTALITY/completeness,
    not a counterexample to the soundness of already-replayed proof objects. -/
inductive TypeShape where
  | var : Nat → TypeShape
  | bottom : TypeShape
  | pi : TypeShape → TypeShape → TypeShape
  | all : TypeShape → TypeShape
  | sigma : TypeShape → TypeShape → TypeShape
  | identity : TypeShape → TypeShape
  deriving DecidableEq

def image : TypeCode → TypeShape
  | .var n => .var n
  | .bottom => .bottom
  | .arrow A B => .pi (image A) (image B)
  | .all B => .all (image B)

theorem identity_not_in_exact_target_image (A : TypeShape) :
    ¬ ∃ T : TypeCode, image T = .identity A := by
  rintro ⟨T,h⟩; cases T <;> cases h

theorem sigma_not_in_exact_target_image (A B : TypeShape) :
    ¬ ∃ T : TypeCode, image T = .sigma A B := by
  rintro ⟨T,h⟩; cases T <;> cases h
end P01Certificate
