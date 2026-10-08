import FiniteEnumeration
import PositiveFormula
import IndexedCoverage
import CertificateCompleteness

/-! A terminating signed certificate service for the unchanged Ninth checker.
The controller program coupling is intentionally a separate final module; these
negative results do not claim the direct submitted-body actual-law endpoint. -/
namespace OrthemicCertificate.Signed
open HiddenParity HiddenParity.Stage HiddenParity.Necessity
variable {q n k : Nat}

/-- Literal structured binding includes every input/interpretation field and the
exact support/start query. There is one locally checked refutation per AST index. -/
structure Negative (q n k : Nat) where
  input : Input q n k
  support : Support q
  start : Fin n
  entries : List (Nat × Refutation)
  deriving DecidableEq

def localReject (I : Input q n k) (B : Support q) (s : Fin n)
    (c : Body q n k) (r : Refutation) : Bool :=
  rejectCheck Atom.eval (positiveFormula I c B s) r

def negativeCheck (I : Input q n k) (B : Support q) (s : Fin n)
    (d : Negative q n k) : Bool :=
  I.inputCheck && decide B.Nonempty && I.sameInput d.input &&
    decide (B = d.support ∧ s = d.start) &&
    indexedCheck (localReject I B s) 0 (astDomain q n k) d.entries

@[simp] theorem negativeCheck_iff (I : Input q n k) (B : Support q) (s : Fin n)
    (d : Negative q n k) : negativeCheck I B s d = true ↔
      I.Valid ∧ B.Nonempty ∧ I = d.input ∧ B = d.support ∧ s = d.start ∧
      indexedCheck (localReject I B s) 0 (astDomain q n k) d.entries = true := by
  simp [negativeCheck, and_assoc]

theorem negativeCheck_binding {I : Input q n k} {B : Support q} {s : Fin n}
    {d : Negative q n k} (h : negativeCheck I B s d = true) :
    d.input = I ∧ d.support = B ∧ d.start = s := by
  have hs := (negativeCheck_iff I B s d).mp h
  exact ⟨hs.2.2.1.symm, hs.2.2.2.1.symm, hs.2.2.2.2.1.symm⟩

theorem negativeCheck_exact_indices {I : Input q n k} {B : Support q} {s : Fin n}
    {d : Negative q n k} (h : negativeCheck I B s d = true) :
    d.entries.map Prod.fst = List.range' 0 (astDomain q n k).length :=
  indexedCheck_indices _ _ _ _ ((negativeCheck_iff I B s d).mp h).2.2.2.2.2

theorem localReject_sound {I : Input q n k} {B : Support q} {s : Fin n}
    {c : Body q n k} {r : Refutation} (h : localReject I B s c r = true) :
    check I c B s = false := by
  have hf := refutation_sound Atom.eval (positiveFormula I c B s) r h
  rwa [positiveFormula_eval] at hf

/-- Every possible accepted AST is ruled out, not only a normalised family of
canonical witnesses. This is where full accepted-body coverage is essential. -/
theorem negativeCheck_excludes_certificate {I : Input q n k} {B : Support q} {s : Fin n}
    {d : Negative q n k} (h : negativeCheck I B s d = true) :
    ¬ ∃ c : Body q n k, check I c B s = true := by
  rintro ⟨c,hc⟩
  have hm := accepted_mem_astDomain hc
  obtain ⟨r,hr⟩ := indexedCheck_sound _ _ _ _
    ((negativeCheck_iff I B s d).mp h).2.2.2.2.2 c hm
  have hf := localReject_sound hr
  simp [hc] at hf

/-- Canonical full negative transcript. Generation invokes only finite formula
arithmetic and recursive rejection construction, never semantic winning. -/
def negativeCandidate (I : Input q n k) (B : Support q) (s : Fin n) : Negative q n k :=
  ⟨I,B,s,indexedCandidate Atom.eval (fun c => positiveFormula I c B s) 0 (astDomain q n k)⟩

theorem negativeCandidate_correct (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n)
    (h : ¬ ∃ c : Body q n k, check I c B s = true) :
    negativeCheck I B s (negativeCandidate I B s) = true := by
  apply (negativeCheck_iff I B s _).mpr
  refine ⟨hI,hB,rfl,rfl,rfl,?_⟩
  apply indexedCandidate_correct
  intro c _
  rw [positiveFormula_eval]
  cases he : check I c B s with
  | false => rfl
  | true => exact False.elim (h ⟨c,he⟩)

/-- New complete negative presentation, relative to Ninth's inherited semantic
iff. No credit is claimed for the inherited semantic characterization. -/
theorem negativeCheck_iff_not_semantic [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (defaultPair : Pair n k) :
    (∃ d, negativeCheck I B s d = true) ↔
      ¬ SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority defaultPair B s := by
  rw [semantic_iff_certificate I hI B s defaultPair]
  constructor
  · rintro ⟨d,hd⟩
    exact negativeCheck_excludes_certificate hd
  · intro hn
    exact ⟨negativeCandidate I B s,negativeCandidate_correct I hI B hB s hn⟩

/-- Exclusion is for every measurable private-seed policy, not merely the image
of the new deterministic compiler. The bridge is inherited Ninth necessity. -/
theorem negativeCheck_excludes_policy [NeZero n] {R : Type*} [MeasurableSpace R]
    (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n) (defaultPair : Pair n k)
    (d : Negative q n k) (hd : negativeCheck I B s d = true)
    (w : WinningPolicy (R := R) (I.kernel hI) I.menu I.priority defaultPair B s) : False :=
  negativeCheck_excludes_certificate hd (policy_has_certificate I hI B s defaultPair w)

inductive SignedResult (q n k : Nat) where
  | invalidInput
  | emptySupport
  | positive (body : Body q n k)
  | negative (certificate : Negative q n k)
  deriving DecidableEq

/-- Finite structurally terminating search over the explicit AST domain. The
positive body is returned literally, with no canonicalisation or solver oracle.
The potentially astronomical computation carries no complexity claim. -/
def solve (I : Input q n k) (B : Support q) (s : Fin n) : SignedResult q n k :=
  if I.inputCheck then
    if B.Nonempty then
      match (astDomain q n k).find? (fun c => check I c B s) with
      | some c => .positive c
      | none => .negative (negativeCandidate I B s)
    else .emptySupport
  else .invalidInput

def SignedResult.Correct (I : Input q n k) (B : Support q) (s : Fin n) :
    SignedResult q n k → Prop
  | .invalidInput => ¬I.Valid
  | .emptySupport => I.Valid ∧ ¬B.Nonempty
  | .positive c => check I c B s = true
  | .negative d => negativeCheck I B s d = true

theorem solve_correct (I : Input q n k) (B : Support q) (s : Fin n) :
    (solve I B s).Correct I B s := by
  unfold solve
  split
  next hI =>
    have hIv : I.Valid := (Input.inputCheck_iff I).mp hI
    split
    next hB =>
      split
      next c hc =>
        change check I c B s = true
        exact List.find?_some (p := fun c => check I c B s) hc
      next hn =>
        apply negativeCandidate_correct I hIv B hB s
        rintro ⟨c,hc⟩
        have hf := List.find?_eq_none.mp hn c (accepted_mem_astDomain hc)
        exact hf hc
    next hB => exact ⟨hIv,hB⟩
  next hI =>
    intro hIv
    exact hI ((Input.inputCheck_iff I).mpr hIv)

/-- On a valid nonempty query, the service can return neither invalid case. -/
theorem solve_valid_outcome (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) :
    (∃ c, solve I B s = .positive c ∧ check I c B s = true) ∨
    (∃ d, solve I B s = .negative d ∧ negativeCheck I B s d = true) := by
  have hc := solve_correct I B s
  cases he : solve I B s with
  | invalidInput =>
    simp only [he,SignedResult.Correct] at hc
    exact False.elim (hc hI)
  | emptySupport =>
    simp only [he,SignedResult.Correct] at hc
    exact False.elim (hc.2 hB)
  | positive c =>
    simp only [he,SignedResult.Correct] at hc
    exact Or.inl ⟨c,rfl,hc⟩
  | negative d =>
    simp only [he,SignedResult.Correct] at hc
    exact Or.inr ⟨d,rfl,hc⟩

/-- Exact sign semantics for the terminating search, on the declared valid
nonempty query class. Positive semantic existence is inherited from Ninth. -/
theorem solve_positive_iff_semantic [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (defaultPair : Pair n k) :
    (∃ c, solve I B s = .positive c) ↔
      SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority defaultPair B s := by
  constructor
  · rintro ⟨c,hc⟩
    have hs := solve_correct I B s
    have hp : check I c B s = true := by simpa [hc,SignedResult.Correct] using hs
    exact (semantic_iff_certificate I hI B s defaultPair).mpr ⟨c,hp⟩
  · intro hw
    rcases solve_valid_outcome I hI B hB s with ⟨c,hc,_⟩ | ⟨d,hd,hcheck⟩
    · exact ⟨c,hc⟩
    · exact False.elim (((negativeCheck_iff_not_semantic I hI B hB s defaultPair).mp
        ⟨d,hcheck⟩) hw)

theorem solve_negative_iff_not_semantic [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (defaultPair : Pair n k) :
    (∃ d, solve I B s = .negative d) ↔
      ¬ SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority defaultPair B s := by
  constructor
  · rintro ⟨d,hd⟩
    have hs := solve_correct I B s
    have hn : negativeCheck I B s d = true := by simpa [hd,SignedResult.Correct] using hs
    exact (negativeCheck_iff_not_semantic I hI B hB s defaultPair).mp ⟨d,hn⟩
  · intro hn
    rcases solve_valid_outcome I hI B hB s with ⟨c,hc,hcheck⟩ | ⟨d,hd,_⟩
    · exact False.elim (hn ((semantic_iff_certificate I hI B s defaultPair).mpr ⟨c,hcheck⟩))
    · exact ⟨d,hd⟩

end OrthemicCertificate.Signed
