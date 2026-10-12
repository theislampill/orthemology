import PrefixObserver
import SelectorPrimrec
import CodecIndexPrimrec

/-! Generic fixed-family finite-prefix realisation of unary tagged rows.
The suffix word is re-encoded with the original sentinel convention. No
universal primitive-recursive interpreter is used or asserted. -/

set_option maxHeartbeats 800000

namespace OrthemologyTagged.UnaryPrefix
open P02A2.ObserverCore P02A2.Q8Measure P02A2.PRProgram P02.Codec

/-- A finite scan followed by dropping the selector and its zero terminator. -/
def suffixWord (n word i : ℕ) : ℕ :=
  sentinel ((scannedBits n word).drop (i+1))

/-- The selected row either passes all its tail bits or runs the fixed family. -/
def rows (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a i : ℕ) : Cantor → Cantor :=
  if D i then id else output (F a)

/-- The input is always finite: exactly the supplied n+1-bit word is scanned.
Before and at a tag stop, the output copies the current source bit. -/
def prefixValue (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a n word : ℕ) : ℕ :=
  let i := selector n word
  if n ≤ i then word % 2
  else if D i then word % 2 else F a (n-i-1) word

theorem drop_prefix (x : Cantor) (i n : ℕ) (hin : i < n) :
    (List.ofFn (fun j : Fin (n+1) => x j.val)).drop (i+1) =
      List.ofFn (fun j : Fin (n-i-1+1) => tail i x j.val) := by
  apply List.ext_getElem
  · simp only [List.length_drop, List.length_ofFn]
    omega
  · intro j hj hk
    simp only [List.getElem_drop, List.getElem_ofFn]
    simp only [tail, dropBits]

theorem suffixWord_prefix (x : Cantor) (i n : ℕ) (hin : i < n) :
    suffixWord n (sentinel (List.ofFn (fun j : Fin (n+1) => x j.val))) i =
      sentinel (List.ofFn (fun j : Fin (n-i-1+1) => tail i x j.val)) := by
  rw [suffixWord, scannedBits_prefix, drop_prefix x i n hin]

theorem prefixValue_output (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a : ℕ) :
    output (prefixValue F D a) = tagged (rows F D a) := by
  funext x n
  rcases exists_tag_or_allTrue x with ⟨i,hx⟩ | rfl
  · rw [tagged_on _ hx]
    by_cases hni : n < i
    · rw [tag_before i _ hni]
      have hsel := selector_before_tag hx hni
      have hbit := ((tagEvent_spec i x).mp hx).1 n hni
      unfold output prefixValue
      rw [hsel, if_pos (Nat.le_succ n), Nat.mod_mod,
        P02A2.Q8Compiler.sentinel_prefix_last, hbit]
      rfl
    · have hin : i ≤ n := by omega
      have hsel := selector_on_tag hx hin
      by_cases he : n = i
      · subst n
        rw [tag_at]
        have hbit := ((tagEvent_spec i x).mp hx).2
        unfold output prefixValue
        rw [hsel, if_pos (le_refl i), Nat.mod_mod,
          P02A2.Q8Compiler.sentinel_prefix_last, hbit]
        rfl
      · have hit : i < n := by omega
        rw [tag_after i _ hit]
        have hidx : i+1+(n-i-1) = n := by omega
        unfold output prefixValue
        rw [hsel]
        simp only [show ¬ (n ≤ i) by omega, ↓reduceIte]
        cases hd : D i
        · simp only [hd, Bool.false_eq_true, ↓reduceIte, rows]
          rw [suffixWord_prefix x i n hit]
          rfl
        · simp only [hd, ↓reduceIte, rows, id_eq]
          rw [Nat.mod_mod, P02A2.Q8Compiler.sentinel_prefix_last]
          cases hb : x n <;> simp [hb, tail, dropBits, hidx]
  · rw [tagged_allTrue]
    unfold output prefixValue
    rw [selector_allTrue, if_pos (Nat.le_succ n), Nat.mod_mod,
      P02A2.Q8Compiler.sentinel_prefix_last]
    rfl

/-- Explicit inclusion of the measure-zero source in pointwise realisation. -/
theorem prefixValue_allTrue (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a : ℕ) :
    output (prefixValue F D a) allTrue = allTrue := by
  rw [prefixValue_output, tagged_allTrue]

/-- The zero terminator is emitted as zero, including when the tail row is identity. -/
theorem prefixValue_at_stop (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a i : ℕ)
    {x : Cantor} (hx : x ∈ tagEvent i) :
    output (prefixValue F D a) x i = false := by
  rw [prefixValue_output, tagged_on _ hx, tag_at]

private theorem sentinel_primrec : Primrec sentinel := by
  have hbit : Primrec (fun p : List Bool × ℕ × Bool => if p.2.2 then 1 else 0) := by
    apply (Primrec.cond (Primrec.snd.comp Primrec.snd) (Primrec.const 1) (Primrec.const 0)).of_eq
    intro p
    cases p.2.2 <;> rfl
  have hs : Primrec₂ (fun (_ : List Bool) (p : ℕ × Bool) =>
      2*p.1 + if p.2 then 1 else 0) :=
    (Primrec.nat_add.comp (Primrec.nat_mul.comp (Primrec.const 2)
      (Primrec.fst.comp Primrec.snd)) hbit).to₂
  exact Primrec.list_foldl Primrec.id (Primrec.const 1) hs

private theorem list_drop_primrec {A : Type} [Primcodable A] : Primrec₂ (@List.drop A) := by
  have h : Primrec (fun p : ℕ × List A => List.tail^[p.1] p.2) :=
    Primrec.nat_iterate Primrec.fst Primrec.snd ((Primrec.list_tail.comp Primrec.snd).to₂)
  apply h.to₂.of_eq
  intro n bs
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, List.tail_drop]

theorem suffixWord_primrec : Primrec₂ (fun p : ℕ × ℕ => suffixWord p.1 p.2) := by
  have hn : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.1) := Primrec.fst.comp Primrec.fst
  have hw : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.2) := Primrec.snd.comp Primrec.fst
  exact (sentinel_primrec.comp (list_drop_primrec.comp (Primrec.succ.comp Primrec.snd)
    (scannedBits_primrec.comp hn hw))).to₂

/-- PR closure is joint in a,n,word for each fixed family F and digit function D. -/
theorem prefixValue_primrec (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool)
    (hF : Primrec₂ (fun p : ℕ × ℕ => F p.1 p.2)) (hD : Primrec D) :
    Primrec₂ (fun p : ℕ × ℕ => prefixValue F D p.1 p.2) := by
  let Input := (ℕ × ℕ) × ℕ
  have ha : Primrec (fun p : Input => p.1.1) := Primrec.fst.comp Primrec.fst
  have hn : Primrec (fun p : Input => p.1.2) := Primrec.snd.comp Primrec.fst
  have hw : Primrec (fun p : Input => p.2) := Primrec.snd
  have hi := selector_primrec.comp hn hw
  have ht := Primrec.nat_sub.comp (Primrec.nat_sub.comp hn hi) (Primrec.const 1)
  have hs := suffixWord_primrec.comp (hn.pair hw) hi
  have hv := hF.comp (ha.pair ht) hs
  have hb := Primrec.nat_mod.comp hw (Primrec.const 2)
  exact (Primrec.ite (Primrec.nat_le.comp hn hi) hb
    (Primrec.ite (Primrec.eq.comp (hD.comp hi) (Primrec.const true)) hb hv)).to₂

def family (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (args : Fin 3 → ℕ) : ℕ :=
  prefixValue F D (args 0) (args 1) (args 2)

theorem family_primrec (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool)
    (hF : Primrec₂ (fun p : ℕ × ℕ => F p.1 p.2)) (hD : Primrec D) :
    Primrec (family F D) := by
  have h0 : Primrec (fun args : Fin 3 → ℕ => args 0) := Primrec.fin_app.comp Primrec.id (Primrec.const 0)
  have h1 : Primrec (fun args : Fin 3 → ℕ => args 1) := Primrec.fin_app.comp Primrec.id (Primrec.const 1)
  have h2 : Primrec (fun args : Fin 3 → ℕ => args 2) := Primrec.fin_app.comp Primrec.id (Primrec.const 2)
  exact (prefixValue_primrec F D hF hD).comp (h0.pair h1) h2

theorem exists_fixed_program (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool)
    (hF : Primrec₂ (fun p : ℕ × ℕ => F p.1 p.2)) (hD : Primrec D) :
    ∃ p : Program 3, ∀ a n word, denote p ![a,n,word] = prefixValue F D a n word := by
  obtain ⟨p,hp⟩ := P02A2.PRCoverage.exists_program_of_primrec (family F D)
    (family_primrec F D hF hD)
  exact ⟨p,fun a n word => hp ![a,n,word]⟩

theorem numeric_observer_eq (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (p : Program 3)
    (hp : ∀ a n word, denote p ![a,n,word] = prefixValue F D a n word) (a : ℕ) :
    output (evaluateIndex (parameterIndex p a)) = tagged (rows F D a) := by
  rw [← prefixValue_output]
  funext x n
  unfold output
  rw [parameterIndex_correct, hp, Nat.mod_mod]

/-- One fixed LOOP program and the concrete PR map of literal-specialized
numeric P02-L1 indices realise the complete pointwise unary tagged family. -/
theorem exists_primrec_numeric_family (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool)
    (hF : Primrec₂ (fun p : ℕ × ℕ => F p.1 p.2)) (hD : Primrec D) :
    ∃ p : Program 3, Primrec (parameterIndex p) ∧ ∀ a,
      output (evaluateIndex (parameterIndex p a)) = tagged (rows F D a) := by
  obtain ⟨p,hp⟩ := exists_fixed_program F D hF hD
  exact ⟨p,parameterIndex_primrec p,numeric_observer_eq F D p hp⟩

end OrthemologyTagged.UnaryPrefix

#print axioms OrthemologyTagged.UnaryPrefix.prefixValue_output
#print axioms OrthemologyTagged.UnaryPrefix.prefixValue_primrec
#print axioms OrthemologyTagged.UnaryPrefix.exists_primrec_numeric_family
