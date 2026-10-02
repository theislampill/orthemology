/- A new, explicitly modeled source-AST evaluator, not a proof of CPython or
JSON. It independently evaluates all seven reference.py certificate rules.
The Cert encoder is a separate function and is never called by sourceCheckCore.
Ordinary grammar/type/trace refusals remain none; resource policies are layered
separately and cannot turn a refusal into an accepted certificate. -/
import SourceHeadStep
namespace P03Source
open OrthemologyV2 OrthemologyV3

inductive SourceProof where
  | i : TypeCode → SourceProof
  | k : TypeCode → TypeCode → SourceProof
  | s : TypeCode → TypeCode → TypeCode → SourceProof
  | app : SourceProof → SourceProof → SourceProof
  | allI : SourceProof → SourceProof
  | allE : SourceProof → TypeCode → SourceProof
  | reduce : SourceProof → List Term → SourceProof
  deriving Repr

/-- Validate every supplied transition; the retained output is the last term. -/
def sourceTraceTail (current : Term) : List Term → Option Term
  | [] => some current
  | next :: rest =>
      if sourceHeadStep current = some next then sourceTraceTail next rest else none

def sourceTrace (start : Term) : List Term → Option Term
  | [] => none
  | first :: rest => if first = start then sourceTraceTail start rest else none

/-- Direct constructor equations, independently returning plain term/type data.
This function never calls check, certifiedHeadStep, or encode. -/
def sourceCheckCore (d : Nat) : SourceProof → Option (Term × TypeCode)
  | .i A => if sourceScoped d A then some (.i, .arrow A A) else none
  | .k A B => if sourceScoped d A && sourceScoped d B then
      some (.k, .arrow A (.arrow B A)) else none
  | .s A B C => if sourceScoped d A && sourceScoped d B && sourceScoped d C then
      some (.s, .arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C))) else none
  | .app p q =>
      match sourceCheckCore d p, sourceCheckCore d q with
      | some (f, .arrow A B), some (x, X) => if A = X then some (.app f x, B) else none
      | _, _ => none
  | .allI p => match sourceCheckCore (d+1) p with
      | some (t, B) => some (t, .all B)
      | none => none
  | .allE p A =>
      if sourceScoped d A then
        match sourceCheckCore d p with
        | some (t, .all B) =>
            let result := sourceSubstitute B A 0
            if sourceScoped d result then some (t, result) else none
        | _ => none
      else none
  | .reduce p trace =>
      match sourceCheckCore d p with
      | some (t, A) => (sourceTrace t trace).map (fun u => (u, A))
      | none => none

/-- Exactly the exporter's repeated Cert.step expansion, before elaboration. -/
def certSteps : Nat → Cert → Cert
  | 0, c => c
  | n+1, c => .step (certSteps n c)

def encode : SourceProof → Cert
  | .i A => .i A
  | .k A B => .k A B
  | .s A B C => .s A B C
  | .app p q => .app (encode p) (encode q)
  | .allI p => .allI (encode p)
  | .allE p A => .allE (encode p) A
  | .reduce p trace => certSteps (trace.length-1) (encode p)

def checkedView (v : Checked) : Term × TypeCode := (v.term, v.ty)

/-- Successful source output is matched in acceptance, erased term and type.
This is not the converse: erasing a malformed explicit trace can discard the
reason that the source checker correctly refused it. -/
def Agrees (d : Nat) (p : SourceProof) (output : Term × TypeCode) : Prop :=
  ∃ v, check d (encode p) = some v ∧ checkedView v = output

end P03Source
