import RecurrentSupport

noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal
open Orthemology.Tranche2.RecurrentSupport
namespace RecurrenceAudit

 theorem constant_recurrence (b a : Bool) : Recurs (fun _ => b) a ↔ b = a := by
  simp [Recurs]

 theorem constant_support (b : Bool) : recurrentSet (fun _ => b) = {b} := by
  ext a
  simp [mem_recurrentSet,constant_recurrence,eq_comm]

 theorem infinite_alphabet_no_recurrence (a : ℕ) : ¬ Recurs (fun n : ℕ => n) a := by
  intro h
  obtain ⟨n,hn,he⟩ := (frequently_atTop.mp h) (a+1)
  change n = a at he
  omega

def delayed (k n : ℕ) : Bool := if n < k then false else true

 theorem delayed_eventually_true (k : ℕ) : ∀ᶠ n in atTop, delayed k n = true := by
  apply eventually_atTop.mpr
  exact ⟨k,fun n hn => by simp [delayed,not_lt.mpr hn]⟩

 theorem delayed_support (k : ℕ) : recurrentSet (delayed k) = {true} := by
  have hs : recurrentSet (delayed k) ⊆ ({true} : Finset Bool) :=
    recurrentSet_subset_of_eventually_mem (delayed k) {true} ((delayed_eventually_true k).mono (fun n hn => by simp [hn]))
  apply Finset.Subset.antisymm hs
  obtain ⟨a,ha⟩ := recurrentSet_nonempty (delayed k)
  have ha' : a = true := by simpa using hs ha
  simpa [ha'] using ha

 theorem no_uniform_tail_time : ¬ ∃ N, ∀ k n, N ≤ n → delayed k n = true := by
  rintro ⟨N,hN⟩
  have h := hN (N+1) N le_rfl
  simp [delayed] at h

 theorem selected_support_is_nonempty (k : ℕ) : (recurrentSet (delayed k)).Nonempty :=
  recurrentSet_nonempty _

 theorem superset_tail_does_not_certify_all_actions :
    (∀ n : ℕ, (false : Bool) ∈ (Finset.univ : Finset Bool)) ∧
    ¬ (Finset.univ : Finset Bool) ⊆ ({false} : Finset Bool) := by
  constructor
  · simp
  · intro h
    have := h (Finset.mem_univ true)
    simp at this

local instance : MeasurableSpace Bool := ⊤
local instance : MeasurableSingletonClass Bool := ⟨fun _ => trivial⟩

def stream (ω : Bool) (_n : ℕ) : Bool := ω

theorem exact_false_event : exactRecurrentEvent stream {false} = {false} := by
  ext ω
  change recurrentSet (fun _ => ω) = {false} ↔ ω = false
  rw [constant_support]
  simp

theorem false_tail_event (N : ℕ) : tailEvent stream {false} N = {false} := by
  ext ω
  cases ω <;> simp [tailEvent,exact_false_event,stream]

theorem true_law_null_false_event :
    (Measure.dirac true) (exactRecurrentEvent stream {false}) = 0 := by
  rw [exact_false_event]
  simp

theorem false_law_positive_tail (N : ℕ) :
    (Measure.dirac false) (tailEvent stream {false} N) = 1 := by
  rw [false_tail_event]
  simp

theorem true_law_null_tail (N : ℕ) :
    (Measure.dirac true) (tailEvent stream {false} N) = 0 := by
  rw [false_tail_event]
  simp

theorem modelwise_success (θ : Bool) :
    ∀ᵐ ω ∂(Measure.dirac θ), ∀ᶠ n in atTop, stream ω n ∈ ({θ} : Finset Bool) := by
  simp [stream]

theorem no_common_nonempty_support :
    ¬ ∃ U : Finset Bool, U.Nonempty ∧ U ⊆ {false} ∧ U ⊆ {true} := by
  rintro ⟨U,⟨a,ha⟩,hf,ht⟩
  have hfalse : a = false := by simpa using hf ha
  have htrue : a = true := by simpa using ht ha
  cases hfalse.symm.trans htrue

theorem positive_transfer_is_substantive :
    ¬ (∀ θ η : Bool, ∀ U : Finset Bool, ∀ N : ℕ,
      0 < (Measure.dirac θ) (tailEvent stream U N) →
      0 < (Measure.dirac η) (tailEvent stream U N)) := by
  intro h
  have hn := h false true {false} 0 (by rw [false_law_positive_tail]; exact zero_lt_one)
  rw [true_law_null_tail] at hn
  exact (lt_irrefl 0 hn)

theorem zero_measure_has_no_positive_cell :
    ¬ ∃ U : Finset Bool, 0 < (0 : Measure Bool) (exactRecurrentEvent stream U) := by
  simp

theorem nonempty_event_can_be_null :
    (exactRecurrentEvent stream {false}).Nonempty ∧
      (Measure.dirac true) (exactRecurrentEvent stream {false}) = 0 := by
  rw [exact_false_event]
  simp

end RecurrenceAudit
