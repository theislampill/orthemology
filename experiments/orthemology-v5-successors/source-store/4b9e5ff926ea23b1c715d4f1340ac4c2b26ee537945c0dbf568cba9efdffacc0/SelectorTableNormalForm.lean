import FiniteRadixNormalForm
import LiteralSelectorFamily
set_option autoImplicit false

/-! Additive classification of the unchanged exact finite-selector Certificate.
No selector is evaluated and no arbitrary orientation is adopted. -/
namespace Orthemology.Ninth.SelectorExtraction
open HiddenParity HiddenParity.Sufficiency
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FiniteSelectorSource
open Orthemology.Eighth.SemanticControls
open Orthemology.Eighth.SemanticControls.LiteralAssessment

/-- All sixteen table cells are represented once by the semantic indices. -/
theorem cell_index_roundtrip (i : Fin 16) :
    cellIndex (cellSupport i) (cellFirst i) (cellSecond i) = i := by
  exact (by decide : ∀ i : Fin 16, cellIndex (cellSupport i) (cellFirst i) (cellSecond i) = i) i

/-- All four support cells are represented once. -/
theorem support_index_roundtrip (i : Fin 4) : supportCode (supportAt i) = i.val := by
  exact (by decide : ∀ i : Fin 4, supportCode (supportAt i) = i.val) i

theorem bit_encoding_injective : Function.Injective bitNat := by
  intro a b h
  cases a <;> cases b <;> simp_all [bitNat]

theorem target_encoding_injective : Function.Injective targetCode := by
  exact (by decide : ∀ E F : Finset (Bool × Bool), targetCode E = targetCode F → E = F)

/-- The absent target and the present empty target have different codes. -/
theorem retained_encoding_injective : Function.Injective retainedCode := by
  exact (by decide : ∀ E F : Option (Finset (Bool × Bool)), retainedCode E = retainedCode F → E = F)

/-- Five-bit target payloads 17--31 cannot satisfy the exact Certificate cell. -/
theorem retained_encoding_le_sixteen (E : Option (Finset (Bool × Bool))) : retainedCode E ≤ 16 := by
  exact (by decide : ∀ E : Option (Finset (Bool × Bool)), retainedCode E ≤ 16) E

theorem absent_present_empty_distinct :
    retainedCode none = 0 ∧ retainedCode (some ∅) = 1 := by decide

/-- Only high, unused digits are removed. The operation itself is executable. -/
def normalizeData (d : Data) : Data :=
  ⟨d.cycleTable % 2^16, d.targetTable % 2^80, d.stageTable % 2^16⟩

def SameCells (d e : Data) : Prop :=
  (∀ B f r, cycleDigit d B f r = cycleDigit e B f r) ∧
  (∀ B c s, targetDigit d B c s = targetDigit e B c s) ∧
  (∀ B, stageDigit d B = stageDigit e B)

theorem cycleDigit_as_radix (d : Data) (B : Finset Bool) (f r : Bool) :
    cycleDigit d B f r = d.cycleTable / 2 ^ (cellIndex B f r).val % 2 := rfl

theorem targetDigit_as_radix (d : Data) (B : Finset Bool) (c s : Bool) :
    targetDigit d B c s = d.targetTable / 32 ^ (cellIndex B c s).val % 32 := by
  unfold targetDigit cellIndex
  rw [pow_mul]
  rfl

theorem stageDigit_as_radix (d : Data) (B : Finset Bool) :
    stageDigit d B = d.stageTable / 16 ^ supportCode B % 16 := by
  unfold stageDigit
  rw [pow_mul]
  rfl

theorem normalized_cycleDigit (d : Data) (B : Finset Bool) (f r : Bool) :
    cycleDigit (normalizeData d) B f r = cycleDigit d B f r := by
  rw [cycleDigit_as_radix, cycleDigit_as_radix]
  exact digit_mod_pow d.cycleTable 2 16 (cellIndex B f r).val (cellIndex B f r).isLt

theorem normalized_targetDigit (d : Data) (B : Finset Bool) (c s : Bool) :
    targetDigit (normalizeData d) B c s = targetDigit d B c s := by
  rw [targetDigit_as_radix, targetDigit_as_radix]
  change (d.targetTable % 2^80) / 32 ^ (cellIndex B c s).val % 32 = _
  rw [show (2:ℕ)^80 = 32^16 by decide]
  exact digit_mod_pow d.targetTable 32 16 (cellIndex B c s).val (cellIndex B c s).isLt

theorem normalized_stageDigit (d : Data) (B : Finset Bool) :
    stageDigit (normalizeData d) B = stageDigit d B := by
  rw [stageDigit_as_radix, stageDigit_as_radix]
  change (d.stageTable % 2^16) / 16 ^ supportCode B % 16 = _
  rw [show (2:ℕ)^16 = 16^4 by decide]
  exact digit_mod_pow d.stageTable 16 4 (supportCode B) (supportCode_lt B)

theorem normalize_sameCells (d : Data) : SameCells (normalizeData d) d :=
  ⟨normalized_cycleDigit d, normalized_targetDigit d, normalized_stageDigit d⟩

/-- Equality of every original certificate cell is exactly residue equality. -/
theorem sameCells_iff_normalize_eq (d e : Data) : SameCells d e ↔ normalizeData d = normalizeData e := by
  constructor
  · rintro ⟨hc,ht,hs⟩
    have ec : d.cycleTable % 2^16 = e.cycleTable % 2^16 := by
      apply (residue_eq_iff_digits _ _ 2 16).mpr
      intro i hi
      have h := hc (cellSupport ⟨i,hi⟩) (cellFirst ⟨i,hi⟩) (cellSecond ⟨i,hi⟩)
      simpa only [cycleDigit_as_radix, cell_index_roundtrip] using h
    have et : d.targetTable % 32^16 = e.targetTable % 32^16 := by
      apply (residue_eq_iff_digits _ _ 32 16).mpr
      intro i hi
      have h := ht (cellSupport ⟨i,hi⟩) (cellFirst ⟨i,hi⟩) (cellSecond ⟨i,hi⟩)
      simpa only [targetDigit_as_radix, cell_index_roundtrip] using h
    have es : d.stageTable % 16^4 = e.stageTable % 16^4 := by
      apply (residue_eq_iff_digits _ _ 16 4).mpr
      intro i hi
      simpa only [stageDigit_as_radix, support_index_roundtrip] using hs (supportAt ⟨i,hi⟩)
    change Data.mk _ _ _ = Data.mk _ _ _
    rw [ec, show (2:ℕ)^80 = 32^16 by decide, et, show (2:ℕ)^16 = 16^4 by decide, es]
  · intro h
    constructor
    · intro B f r
      rw [← normalized_cycleDigit d, ← normalized_cycleDigit e, h]
    constructor
    · intro B c s
      rw [← normalized_targetDigit d, ← normalized_targetDigit e, h]
    · intro B
      rw [← normalized_stageDigit d, ← normalized_stageDigit e, h]

theorem certificate_iff_of_sameCells (d e : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (h : SameCells d e) : Certificate d P menu priority ↔ Certificate e P menu priority := by
  constructor
  · intro hd
    exact ⟨fun B f r => (h.1 B f r).symm.trans (hd.cycle_eq B f r),
      fun B c s => (h.2.1 B c s).symm.trans (hd.target_eq B c s),
      fun B => (h.2.2 B).symm.trans (hd.stage_eq B)⟩
  · intro he
    exact ⟨fun B f r => (h.1 B f r).trans (he.cycle_eq B f r),
      fun B c s => (h.2.1 B c s).trans (he.target_eq B c s),
      fun B => (h.2.2 B).trans (he.stage_eq B)⟩

/-- Normalization preserves exactly the unchanged Certificate, for every kernel. -/
theorem normalized_certificate_iff (d : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ) :
    Certificate (normalizeData d) P menu priority ↔ Certificate d P menu priority :=
  certificate_iff_of_sameCells _ _ _ _ _ (normalize_sameCells d)

theorem normalized_literal (o : Bool) : normalizeData (literalData o) = literalData o := by
  cases o <;> decide

/-- A literal certificate is exactly a determination of the retained orientation. -/
theorem literal_certificate_iff (o : Bool) :
    Certificate (literalData o) fixtureKernel sparseMenu actionPriority ↔ initialCandidate = o := by
  constructor
  · intro hc
    have h := hc.cycle_eq Finset.univ false false
    rw [literal_cycle_digits] at h
    have he : expectedCycle o Finset.univ false false = o := by
      cases o <;> decide
    rw [he] at h
    exact (bit_encoding_injective h).symm
  · exact literal_certificate o

/-- All exact certified encodings have one bounded normal form. The orientation
remains opaque; no branch is chosen computationally by this theorem. -/
theorem certificate_iff_exact_normalForm (d : Data) :
    Certificate d fixtureKernel sparseMenu actionPriority ↔
      normalizeData d = literalData initialCandidate := by
  have hl := literal_certificate initialCandidate rfl
  constructor
  · intro hd
    have hs : SameCells d (literalData initialCandidate) :=
      ⟨fun B f r => (hd.cycle_eq B f r).trans (hl.cycle_eq B f r).symm,
       fun B c s => (hd.target_eq B c s).trans (hl.target_eq B c s).symm,
       fun B => (hd.stage_eq B).trans (hl.stage_eq B).symm⟩
    simpa only [normalized_literal] using (sameCells_iff_normalize_eq _ _).mp hs
  · intro hn
    apply (normalized_certificate_iff d fixtureKernel sparseMenu actionPriority).mp
    rw [hn]
    exact hl

/-- Exhaustivity is strengthened to exclusive exhaustivity. -/
theorem exactly_one_literal_certificate :
    (Certificate (literalData false) fixtureKernel sparseMenu actionPriority ∨
      Certificate (literalData true) fixtureKernel sparseMenu actionPriority) ∧
    ¬(Certificate (literalData false) fixtureKernel sparseMenu actionPriority ∧
      Certificate (literalData true) fixtureKernel sparseMenu actionPriority) := by
  refine ⟨explicit_two_table_certificate, ?_⟩
  rintro ⟨hf,ht⟩
  have h := (literal_certificate_iff false).mp hf
  have h' := (literal_certificate_iff true).mp ht
  rw [h] at h'
  contradiction


/-- A finite supplied certificate carries exactly one computably readable orientation bit. -/
def recoveredOrientation (d : Data) : Bool :=
  decide (cycleDigit d Finset.univ false false = 1)

theorem recoveredOrientation_exact (d : Data)
    (hc : Certificate d fixtureKernel sparseMenu actionPriority) :
    recoveredOrientation d = initialCandidate := by
  unfold recoveredOrientation
  rw [hc.cycle_eq]
  change decide (bitNat initialCandidate = 1) = initialCandidate
  cases initialCandidate <;> rfl

/-- Canonicalization computes a literal record from supplied finite data. Its
proof never chooses or evaluates the retained noncomputable enumeration. -/
theorem normalized_eq_recovered_literal (d : Data)
    (hc : Certificate d fixtureKernel sparseMenu actionPriority) :
    normalizeData d = literalData (recoveredOrientation d) := by
  rw [recoveredOrientation_exact d hc]
  exact (certificate_iff_exact_normalForm d).mp hc

/-- The readable orientation reconstitutes a fully certified literal record. -/
theorem recovered_literal_certificate (d : Data)
    (hc : Certificate d fixtureKernel sparseMenu actionPriority) :
    Certificate (literalData (recoveredOrientation d)) fixtureKernel sparseMenu actionPriority := by
  apply (literal_certificate_iff _).mpr
  exact (recoveredOrientation_exact d hc).symm

/-- Bounded means no unused high digits remain; it makes no assertion about
whether the low digits are valid certificate payloads. -/
def BoundedData (d : Data) : Prop :=
  d.cycleTable < 2^16 ∧ d.targetTable < 2^80 ∧ d.stageTable < 2^16

theorem normalizeData_bounded (d : Data) : BoundedData (normalizeData d) := by
  exact ⟨Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide), Nat.mod_lt _ (by decide)⟩

theorem normalizeData_of_bounded (d : Data) (h : BoundedData d) : normalizeData d = d := by
  rcases d with ⟨c,t,s⟩
  rcases h with ⟨hc,ht,hs⟩
  change Data.mk (c % 2^16) (t % 2^80) (s % 2^16) = Data.mk c t s
  rw [Nat.mod_eq_of_lt hc, Nat.mod_eq_of_lt ht, Nat.mod_eq_of_lt hs]

theorem normalizeData_idempotent (d : Data) : normalizeData (normalizeData d) = normalizeData d :=
  normalizeData_of_bounded _ (normalizeData_bounded d)

/-- There is a unique bounded certificate, while its actual Boolean orientation
is deliberately left unevaluated. -/
theorem bounded_certificate_iff (d : Data) (h : BoundedData d) :
    Certificate d fixtureKernel sparseMenu actionPriority ↔ d = literalData initialCandidate := by
  simpa only [normalizeData_of_bounded d h] using certificate_iff_exact_normalForm d

/-- Executable addition of unused high digits gives all noncanonical encodings. -/
def addHighDigits (d : Data) (c t s : ℕ) : Data :=
  ⟨d.cycleTable + 2^16*c, d.targetTable + 2^80*t, d.stageTable + 2^16*s⟩

theorem addHighDigits_normalize (d : Data) (c t s : ℕ) :
    normalizeData (addHighDigits d c t s) = normalizeData d := by
  simp [normalizeData, addHighDigits, Nat.add_mod, Nat.mul_mod]

theorem certificate_addHighDigits_iff (d : Data) (c t s : ℕ)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ) :
    Certificate (addHighDigits d c t s) P menu priority ↔ Certificate d P menu priority :=
  certificate_iff_of_sameCells _ _ _ _ _
    ((sameCells_iff_normalize_eq _ _).mpr (addHighDigits_normalize d c t s))

/-- Full numeral identity is not forced: ignored high digits give distinct
certified records. This does not undermine the bounded normal-form theorem. -/
theorem certified_records_not_unique :
    ∃ d e : Data, d ≠ e ∧ Certificate d fixtureKernel sparseMenu actionPriority ∧
      Certificate e fixtureKernel sparseMenu actionPriority := by
  let d := literalData initialCandidate
  refine ⟨d, addHighDigits d 1 0 0, ?_, literal_certificate initialCandidate rfl, ?_⟩
  · intro h
    have hc := congrArg Data.cycleTable h
    change d.cycleTable = d.cycleTable + 2^16*1 at hc
    omega
  · exact (certificate_addHighDigits_iff d 1 0 0 _ _ _).mpr
      (literal_certificate initialCandidate rfl)


/-- Euclidean division computes the discarded high-digit parameters. -/
theorem data_eq_normalized_plus_high (d : Data) :
    d = addHighDigits (normalizeData d)
      (d.cycleTable / 2^16) (d.targetTable / 2^80) (d.stageTable / 2^16) := by
  rcases d with ⟨c,t,s⟩
  change Data.mk c t s = Data.mk (c % 2^16 + 2^16*(c/2^16))
    (t % 2^80 + 2^80*(t/2^80)) (s % 2^16 + 2^16*(s/2^16))
  rw [Nat.mod_add_div, Nat.mod_add_div, Nat.mod_add_div]

/-- Complete parametrization of all unbounded certified table records. -/
theorem certificate_iff_literal_plus_high (d : Data) :
    Certificate d fixtureKernel sparseMenu actionPriority ↔
      ∃ c t s : ℕ, d = addHighDigits (literalData initialCandidate) c t s := by
  constructor
  · intro hc
    refine ⟨d.cycleTable / 2^16, d.targetTable / 2^80, d.stageTable / 2^16, ?_⟩
    have h := data_eq_normalized_plus_high d
    rw [(certificate_iff_exact_normalForm d).mp hc] at h
    exact h
  · rintro ⟨c,t,s,rfl⟩
    exact (certificate_addHighDigits_iff _ c t s _ _ _).mpr
      (literal_certificate initialCandidate rfl)


/-- For any original kernel/menu/priority, exact certificates determine the
same used-width data, even when the target choices are nonunique in principle. -/
theorem certified_normalForms_unique (d e : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hd : Certificate d P menu priority) (he : Certificate e P menu priority) :
    normalizeData d = normalizeData e := by
  apply (sameCells_iff_normalize_eq d e).mp
  exact ⟨fun B f r => (hd.cycle_eq B f r).trans (he.cycle_eq B f r).symm,
    fun B c s => (hd.target_eq B c s).trans (he.target_eq B c s).symm,
    fun B => (hd.stage_eq B).trans (he.stage_eq B).symm⟩

/-- Unique bounded existence is classical when the retained selectors are;
this theorem supplies no native extractor from an arbitrary kernel. -/
theorem existsUnique_bounded_certificate
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ) :
    ∃! d : Data, BoundedData d ∧ Certificate d P menu priority := by
  let d := normalizeData (certifiedData P menu priority)
  have hd : Certificate d P menu priority :=
    (normalized_certificate_iff _ P menu priority).mpr (certifiedData_certificate P menu priority)
  refine ⟨d, ⟨normalizeData_bounded _, hd⟩, ?_⟩
  intro e he
  have h := certified_normalForms_unique e d P menu priority he.2 hd
  rw [normalizeData_of_bounded e he.1, normalizeData_idempotent] at h
  exact h


/-- A proof-carrying executable normalization API. Its runtime value is only
modular truncation of supplied data; no retained choice is executed. -/
def normalizeCertified (d : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate d P menu priority) :
    { e : Data // BoundedData e ∧ Certificate e P menu priority } :=
  ⟨normalizeData d, normalizeData_bounded d,
    (normalized_certificate_iff d P menu priority).mpr hc⟩

theorem normalizeCertified_value (d : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate d P menu priority) :
    (normalizeCertified d P menu priority hc).val = normalizeData d := rfl

/-- Given supplied certified sparse-fixture data, produce the corresponding
literal record with the unchanged original certificate. This is conditional
extraction, not a closed evaluation of the retained orientation. -/
def extractCertifiedLiteral (d : Data)
    (hc : Certificate d fixtureKernel sparseMenu actionPriority) :
    { e : Data // Certificate e fixtureKernel sparseMenu actionPriority } :=
  ⟨literalData (recoveredOrientation d), recovered_literal_certificate d hc⟩

theorem extractCertifiedLiteral_value (d : Data)
    (hc : Certificate d fixtureKernel sparseMenu actionPriority) :
    (extractCertifiedLiteral d hc).val = normalizeData d :=
  (normalized_eq_recovered_literal d hc).symm


/-- High-bit equivalence is restricted to semantic finite cells. A raw support
argument 4 is outside supportCode's image and can observe bit 16. This is a tiny
selector-component proof, not evaluation of the complete policy denotation. -/
theorem malformed_cycle_input_distinguishes_high_bits (o : Bool) :
    P02A2.PRProgram.denote (cycleProgram (literalData o)) ![4,0,0] = 0 ∧
    P02A2.PRProgram.denote (cycleProgram (addHighDigits (literalData o) 1 0 0)) ![4,0,0] = 1 := by
  cases o <;> decide

/-- The malformed-input distinction coexists with equality of all exact finite
certificate cells. It does not contradict certificate-preserving normalization. -/
theorem sameCells_but_malformed_input_differs (o : Bool) :
    SameCells (literalData o) (addHighDigits (literalData o) 1 0 0) ∧
    P02A2.PRProgram.denote (cycleProgram (literalData o)) ![4,0,0] ≠
      P02A2.PRProgram.denote (cycleProgram (addHighDigits (literalData o) 1 0 0)) ![4,0,0] := by
  constructor
  · apply (sameCells_iff_normalize_eq _ _).mpr
    exact (addHighDigits_normalize _ 1 0 0).symm
  · rw [(malformed_cycle_input_distinguishes_high_bits o).1,
      (malformed_cycle_input_distinguishes_high_bits o).2]
    decide

end Orthemology.Ninth.SelectorExtraction
