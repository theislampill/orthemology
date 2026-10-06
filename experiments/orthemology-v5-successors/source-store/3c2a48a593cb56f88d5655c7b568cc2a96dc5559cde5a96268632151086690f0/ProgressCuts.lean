import ReductionBasics

namespace PolicySynthesis
open EffectiveRenewal
open Nat.Partrec (Code)
open Encodable Denumerable

/-! Generic numerical cut operations. The zero cut is a stated hypothesis in
semantic lemmas, not a totality condition on a computation. -/
def lastCut (cut : Nat → Bool) (i : Nat) : Nat :=
  Nat.findGreatest (fun b => cut b = true) i

theorem lastCut_le (cut : Nat → Bool) (i : Nat) : lastCut cut i ≤ i :=
  Nat.findGreatest_le _

theorem lastCut_isCut (cut : Nat → Bool) (h0 : cut 0 = true) (i : Nat) :
    cut (lastCut cut i) = true :=
  Nat.findGreatest_spec (P := fun b => cut b = true) (Nat.zero_le i) h0

theorem le_lastCut {cut : Nat → Bool} {b i : Nat} (hbi : b ≤ i) (hb : cut b = true) :
    b ≤ lastCut cut i := Nat.le_findGreatest hbi hb

theorem no_cut_after_lastCut (cut : Nat → Bool) {b i : Nat}
    (hb : lastCut cut i < b) (hbi : b ≤ i) : cut b ≠ true :=
  Nat.findGreatest_is_greatest hb hbi

theorem lastCut_eq_of_bounds {cut : Nat → Bool} {b i : Nat} (hb : cut b = true)
    (hbi : b ≤ i) (hn : ∀ c, b < c → c ≤ i → cut c ≠ true) : lastCut cut i = b := by
  apply Nat.findGreatest_eq_iff.mpr
  exact ⟨hbi, fun _ => hb, fun {c} hbc hci => hn c hbc hci⟩

theorem lastCut_mono (cut : Nat → Bool) : Monotone (lastCut cut) :=
  fun _ _ h => Nat.findGreatest_mono_right _ h

theorem lastCut_same_interval {cut : Nat → Bool} (h0 : cut 0 = true)
    {i j : Nat} (hlo : lastCut cut i ≤ j) (hhi : j ≤ i) :
    lastCut cut j = lastCut cut i := by
  apply lastCut_eq_of_bounds (lastCut_isCut cut h0 i) hlo
  intro c hc hcj
  exact no_cut_after_lastCut cut hc (hcj.trans hhi)

@[simp] theorem lastCut_zero (cut : Nat → Bool) : lastCut cut 0 = 0 := rfl

theorem lastCut_succ (cut : Nat → Bool) (i : Nat) :
    lastCut cut (i + 1) = if cut (i + 1) = true then i + 1 else lastCut cut i := rfl

theorem lastCut_eventually_constant {cut : Nat → Bool} (h0 : cut 0 = true)
    {N : Nat} (hN : ∀ c, N < c → cut c ≠ true) :
    ∃ b, cut b = true ∧ ∀ i, b ≤ i → lastCut cut i = b := by
  refine ⟨lastCut cut N, lastCut_isCut cut h0 N, ?_⟩
  intro i hi
  apply lastCut_eq_of_bounds (lastCut_isCut cut h0 N) hi
  intro c hc hci
  by_cases hcN : c ≤ N
  · exact no_cut_after_lastCut cut hc hcN
  · exact hN c (by omega)

theorem lastCut_primrec {α : Type} [Primcodable α] {cut : α → Nat → Bool}
    (hc : Primrec₂ cut) : Primrec₂ fun a i => lastCut (cut a) i := by
  exact Primrec.nat_findGreatest Primrec.snd
    (Primrec.eq.comp (hc.comp (Primrec.fst.comp Primrec.fst) Primrec.snd)
      (Primrec.const true)).to₂

/-! One fixed universal bounded-halting matrix. No code-totality promise. -/
def evalSeen (q : Nat × Nat) (s y : Nat) : Bool :=
  (Code.evaln s (ofNat Code q.1) (Nat.pair q.2 y)).isSome

def rowTotal (p x : Nat) : Prop :=
  ∀ y, (Code.eval (ofNat Code p) (Nat.pair x y)).Dom

theorem evalSeen_primrec :
    Primrec fun a : ((Nat × Nat) × Nat) × Nat => evalSeen a.1.1 a.1.2 a.2 := by
  exact Primrec.option_isSome.comp (Code.evaln_prim.comp
    (((Primrec.snd.comp Primrec.fst).pair
      ((Primrec.ofNat Code).comp (Primrec.fst.comp (Primrec.fst.comp Primrec.fst)))).pair
      (Primrec₂.natPair.comp (Primrec.snd.comp (Primrec.fst.comp Primrec.fst)) Primrec.snd)))

theorem evalSeen_mono {q : Nat × Nat} {s t y : Nat} (hst : s ≤ t)
    (hs : evalSeen q s y = true) : evalSeen q t y = true := by
  unfold evalSeen at hs ⊢
  rcases Option.isSome_iff_exists.mp hs with ⟨v, hv⟩
  exact Option.isSome_iff_exists.mpr ⟨v, Code.evaln_mono hst hv⟩

theorem rowTotal_iff_seen (p x : Nat) :
    rowTotal p x ↔ ∀ y, ∃ s, evalSeen (p,x) s y = true := by
  constructor
  · intro h y
    obtain ⟨v, hv⟩ := Part.dom_iff_mem.mp (h y)
    obtain ⟨s, hs⟩ := Code.evaln_complete.mp hv
    exact ⟨s, Option.isSome_iff_exists.mpr ⟨v, hs⟩⟩
  · intro h y
    obtain ⟨s, hs⟩ := h y
    obtain ⟨v, hv⟩ := Option.isSome_iff_exists.mp hs
    exact (Code.evaln_sound hv).1

def progress (q : Nat × Nat) (s : Nat) : Nat :=
  Nat.findGreatest (fun k => allBelow (evalSeen q s) k = true) s

theorem progress_le (q : Nat × Nat) (s : Nat) : progress q s ≤ s :=
  Nat.findGreatest_le _

theorem progress_seen (q : Nat × Nat) (s : Nat) :
    ∀ y < progress q s, evalSeen q s y = true := by
  apply (allBelow_iff _ _).mp
  exact Nat.findGreatest_spec (P := fun k => allBelow (evalSeen q s) k = true)
    (Nat.zero_le s) (by simp)

theorem le_progress {q : Nat × Nat} {k s : Nat} (hks : k ≤ s)
    (h : ∀ y < k, evalSeen q s y = true) : k ≤ progress q s :=
  Nat.le_findGreatest hks ((allBelow_iff _ _).mpr h)

theorem progress_mono (q : Nat × Nat) : Monotone (progress q) := by
  intro s t hst
  apply le_progress ((progress_le q s).trans hst)
  intro y hy
  exact evalSeen_mono hst (progress_seen q s y hy)

theorem progress_primrec : Primrec₂ progress := by
  have hg : Primrec fun a : ((Nat × Nat) × Nat) × Nat =>
      allBelow (evalSeen a.1.1 a.1.2) a.2 :=
    allBelow_primrec
      (evalSeen_primrec.comp ((Primrec.fst.comp Primrec.fst).pair Primrec.snd)).to₂ Primrec.snd
  exact Primrec.nat_findGreatest Primrec.snd
    (Primrec.eq.comp hg (Primrec.const true)).to₂

theorem rowTotal_unbounded_progress {p x : Nat} (h : rowTotal p x) :
    ∀ k, ∃ s, k ≤ progress (p,x) s := by
  have hseen := (rowTotal_iff_seen p x).mp h
  have hfinite : ∀ k, ∃ s, k ≤ s ∧ ∀ y < k, evalSeen (p,x) s y = true := by
    intro k
    induction k with
    | zero => exact ⟨0, le_rfl, by simp⟩
    | succ k ih =>
      obtain ⟨s, hks, hs⟩ := ih
      obtain ⟨t, ht⟩ := hseen k
      refine ⟨max (max s t) (k+1), Nat.le_max_right _ _, ?_⟩
      intro y hy
      by_cases hyk : y < k
      · exact evalSeen_mono ((Nat.le_max_left s t).trans (Nat.le_max_left _ _)) (hs y hyk)
      · have : y = k := by omega
        subst y
        exact evalSeen_mono ((Nat.le_max_right s t).trans (Nat.le_max_left _ _)) ht
  intro k
  obtain ⟨s, hks, hs⟩ := hfinite k
  exact ⟨s, le_progress hks hs⟩

theorem unbounded_progress_rowTotal {p x : Nat}
    (h : ∀ k, ∃ s, k ≤ progress (p,x) s) : rowTotal p x := by
  apply (rowTotal_iff_seen p x).mpr
  intro y
  obtain ⟨s, hs⟩ := h (y+1)
  exact ⟨s, progress_seen (p,x) s y hs⟩

def progressCut (q : Nat × Nat) (s : Nat) : Bool :=
  decide (s = 0 ∨ progress q (s-1) < progress q s)

@[simp] theorem progressCut_zero (q : Nat × Nat) : progressCut q 0 = true := by
  simp [progressCut]

theorem progressCut_pos {q : Nat × Nat} {s : Nat} (hs : 0 < s) :
    progressCut q s = true ↔ progress q (s-1) < progress q s := by
  simp [progressCut, Nat.ne_of_gt hs]

theorem progressCut_primrec : Primrec₂ progressCut := by
  exact (PrimrecPred.or (Primrec.eq.comp Primrec.snd (Primrec.const 0))
    (Primrec.nat_lt.comp
      (progress_primrec.comp Primrec.fst (Primrec.nat_sub.comp Primrec.snd (Primrec.const 1)))
      progress_primrec))

private theorem bounded_mono_stabilizes {f : Nat → Nat} (hm : Monotone f)
    {c : Nat} (hc : ∀ n, f n ≤ c) : ∃ N, ∀ n, N ≤ n → f n = f N := by
  induction c with
  | zero => exact ⟨0, fun n _ => by have := hc n; have := hc 0; omega⟩
  | succ c ih =>
    by_cases h : ∀ n, f n ≤ c
    · exact ih h
    · push_neg at h
      obtain ⟨N, hN⟩ := h
      refine ⟨N, ?_⟩
      intro n hn
      have := hm hn
      have := hc n
      have := hc N
      omega

theorem rowTotal_iff_unbounded_cuts (p x : Nat) :
    rowTotal p x ↔ ∀ N, ∃ c, N < c ∧ progressCut (p,x) c = true := by
  classical
  constructor
  · intro ht N
    by_contra h
    push_neg at h
    have heq : ∀ n, N ≤ n → progress (p,x) n = progress (p,x) N := by
      intro n hn
      induction n, hn using Nat.le_induction with
      | base => rfl
      | succ n hn ih =>
        have hc := h (n+1) (by omega)
        have hlt : ¬ progress (p,x) n < progress (p,x) (n+1) := by
          simpa [progressCut] using hc
        have hm := progress_mono (p,x) (Nat.le_succ n)
        simp only [Nat.succ_eq_add_one] at *
        omega
    obtain ⟨s, hs⟩ := rowTotal_unbounded_progress ht (progress (p,x) N + 1)
    by_cases hNs : N ≤ s
    · have := heq s hNs; omega
    · have := progress_mono (p,x) (show s ≤ N by omega); omega
  · intro h
    by_contra ht
    have hbound : ∃ k, ∀ s, progress (p,x) s ≤ k := by
      by_contra hn
      push_neg at hn
      apply ht
      exact unbounded_progress_rowTotal (fun k => by obtain ⟨s, hs⟩ := hn k; exact ⟨s, hs.le⟩)
    obtain ⟨k, hk⟩ := hbound
    obtain ⟨N, hN⟩ := bounded_mono_stabilizes (progress_mono (p,x)) hk
    obtain ⟨c, hcN, hc⟩ := h (N+1)
    have hlt := (progressCut_pos (by omega : 0 < c)).mp hc
    have h1 := hN c (by omega)
    have h2 := hN (c-1) (by omega)
    omega

theorem not_rowTotal_eventually_lastCut {p x : Nat} (h : ¬ rowTotal p x) :
    ∃ b, progressCut (p,x) b = true ∧
      ∀ i, b ≤ i → lastCut (progressCut (p,x)) i = b := by
  classical
  have hn : ¬ ∀ N, ∃ c, N < c ∧ progressCut (p,x) c = true := by
    intro hn
    exact h ((rowTotal_iff_unbounded_cuts p x).mpr hn)
  push_neg at hn
  obtain ⟨N, hN⟩ := hn
  exact lastCut_eventually_constant (progressCut_zero _) hN

end PolicySynthesis
