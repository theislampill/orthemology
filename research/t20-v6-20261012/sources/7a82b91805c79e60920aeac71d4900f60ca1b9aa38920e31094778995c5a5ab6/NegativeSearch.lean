import CertificateTerm
import PRSearchComputability

namespace PRNegativeSearch
open P01AC P01D P01AC.ExtensionalRepair
open P01AC.BooleanPrimitive PRConditionalRefutation FullPERTests
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Executable finite approximation: scan 0,...,fuel-1, preserving the first
    counterexample found. A none result makes no claim about later inputs. -/
def scan (f : PR 2) (e : Nat) : Nat → Option Nat
  | 0 => none
  | fuel+1 => match scan f e fuel with
    | some k => some k
    | none => if f.denote (inputs fuel e) = 0 then none else some fuel

theorem scan_spec (f : PR 2) (e fuel : Nat) :
    match scan f e fuel with
    | none => ∀ k, k < fuel → f.denote (inputs k e) = 0
    | some k => k < fuel ∧ f.denote (inputs k e) ≠ 0 ∧
        ∀ j, j < k → f.denote (inputs j e) = 0 := by
  induction fuel with
  | zero => simp [scan]
  | succ fuel ih =>
    simp only [scan]
    cases h : scan f e fuel with
    | none =>
      have hz : ∀ k, k < fuel → f.denote (inputs k e) = 0 := by simpa only [h] using ih
      by_cases hn : f.denote (inputs fuel e) = 0
      · simp only [hn, ↓reduceIte]
        intro k hk
        rcases Nat.lt_succ_iff_lt_or_eq.mp hk with hl | rfl
        · exact hz k hl
        · exact hn
      · simp only [hn, ↓reduceIte]
        exact ⟨Nat.lt_succ_self fuel,hn,hz⟩
    | some k =>
      have hk : k < fuel ∧ f.denote (inputs k e) ≠ 0 ∧
          ∀ j, j < k → f.denote (inputs j e) = 0 := by simpa only [h] using ih
      exact ⟨Nat.lt.step hk.1,hk.2⟩

theorem scan_none_iff (f : PR 2) (e fuel : Nat) :
    scan f e fuel = none ↔ ∀ k, k < fuel → f.denote (inputs k e) = 0 := by
  constructor
  · intro h
    simpa only [h] using scan_spec f e fuel
  · intro hz
    cases h : scan f e fuel with
    | none => rfl
    | some k =>
      have hk := scan_spec f e fuel
      rw [h] at hk
      exact False.elim (hk.2.1 (hz k hk.1))

/-- The executable approximants agree with the actual partial recursive search. -/
theorem scan_return_mem {f : PR 2} {e fuel k : Nat} (h : scan f e fuel = some k) :
    k ∈ f.nonzeroSearch e := by
  have hs := scan_spec f e fuel
  rw [h] at hs
  exact (f.mem_nonzeroSearch_iff e k).mpr hs.2

theorem search_mem_has_scan {f : PR 2} {e k : Nat} (h : k ∈ f.nonzeroSearch e) :
    scan f e (k+1) = some k := by
  cases hs : scan f e (k+1) with
  | none =>
    have hz := (scan_none_iff f e (k+1)).mp hs k (Nat.lt_succ_self k)
    exact False.elim (((f.mem_nonzeroSearch_iff e k).mp h).1 hz)
  | some j =>
    have hj := scan_return_mem hs
    have eq := Part.mem_unique hj h
    exact congrArg some eq

theorem search_dom_iff_invalid (f : PR 2) (e : Nat) :
    (f.nonzeroSearch e).Dom ↔ ¬ Holds (programType f e) := by
  exact (f.nonzeroSearch_dom_iff e).trans (invalid_iff_finite_counterexample f e).symm

theorem scan_terminates_iff_invalid (f : PR 2) (e : Nat) :
    (∃ fuel k, scan f e fuel = some k) ↔ ¬ Holds (programType f e) := by
  constructor
  · rintro ⟨fuel,k,h⟩
    exact (search_dom_iff_invalid f e).mp (scan_return_mem h).1
  · intro h
    obtain ⟨k,hk⟩ := Part.dom_iff_mem.mp ((search_dom_iff_invalid f e).mpr h)
    exact ⟨k+1,k,search_mem_has_scan hk⟩

/-- Actual source data returned by each successful finite scan. -/
def scanCertificate (f : PR 2) (e fuel : Nat) : Option (Nat × Poly) :=
  (scan f e fuel).map (fun k => (k,certificateTerm k))

/-- The partial procedure returns an index and the literal source proof term.
    Its typing is certified below, without a serialization of proof derivations. -/
def certificateSearch (f : PR 2) (e : Nat) : Part (Nat × Poly) :=
  (f.nonzeroSearch e).map (fun k => (k,certificateTerm k))

theorem certificateSearch_dom_iff (f : PR 2) (e : Nat) :
    (certificateSearch f e).Dom ↔ ¬ Holds (programType f e) :=
  search_dom_iff_invalid f e

theorem returned_source_certificate {f : PR 2} {e k : Nat} {q : Poly}
    (h : (k,q) ∈ certificateSearch f e) :
    q = certificateTerm k ∧ f.denote (inputs k e) ≠ 0 ∧
      HasE [] q (arr NoConfusion (arr (programType f e) .bottom)) := by
  obtain ⟨j,hj,heq⟩ := (Part.mem_map_iff _).mp h
  have hk : j = k := congrArg Prod.fst heq
  have hq : certificateTerm j = q := congrArg Prod.snd heq
  subst k
  subst q
  have bad := ((f.mem_nonzeroSearch_iff e j).mp hj).1
  exact ⟨rfl,bad,certificateTerm_has f e j bad⟩

theorem scanCertificate_sound {f : PR 2} {e fuel k : Nat} {q : Poly}
    (h : scanCertificate f e fuel = some (k,q)) :
    q = certificateTerm k ∧ HasE [] q (arr NoConfusion (arr (programType f e) .bottom)) := by
  cases hs : scan f e fuel with
  | none => simp [scanCertificate,hs] at h
  | some j =>
    simp only [scanCertificate,hs,Option.map_some,Option.some.injEq,Prod.mk.injEq] at h
    obtain ⟨rfl,rfl⟩ := h
    exact ⟨rfl,certificateTerm_has f e k (((f.mem_nonzeroSearch_iff e k).mp (scan_return_mem hs)).1)⟩

/-- Valid inputs do not terminate; finite-fuel none is not a validity proof. -/
theorem valid_search_undefined {f : PR 2} {e : Nat} (h : Holds (programType f e)) :
    ¬ (certificateSearch f e).Dom := by
  intro hd
  exact (certificateSearch_dom_iff f e).mp hd h

#print axioms scan_terminates_iff_invalid
#print axioms returned_source_certificate
#print axioms scanCertificate_sound
end PRNegativeSearch
