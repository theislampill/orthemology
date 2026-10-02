import UniformComputabilityNumeric

namespace P02.Codec.UniformComputability
open P02.Codec

/-- Arithmetic reading under the actual bit-accumulator invariant. -/
def plainRead : List ℕ → ℕ → ℕ → List ℕ → Option ReadResult
  | [], _, _, _ => none
  | b::bs, acc, shift, used =>
      if b < 256 then
        let next := acc + 2^shift * (b%128)
        if b < 128 then some (next,(b::used).reverse,bs)
        else plainRead bs next (shift+7) (b::used)
      else none

theorem plainRead_eq (bs : List ℕ) (acc shift : ℕ) (used : List ℕ) (ha : acc < 2^shift) :
    plainRead bs acc shift used = readAccum bs acc shift used := by
  induction bs generalizing acc shift used with
  | nil => rfl
  | cons b bs ih =>
      simp only [plainRead, readAccum, payload_eq_mod, accumulator_or ha]
      split_ifs with hb ht
      · rfl
      · apply ih
        have hp : 2^(shift+7) = 2^shift*128 := by rw [pow_add]; norm_num
        have hm := Nat.mod_lt b (by omega : 0<128)
        have hz : 0 < 2^shift := by positivity
        rw [hp]
        nlinarith
      · rfl

abbrev UVWork := List ℕ × ℕ × ℕ × List ℕ
abbrev UVState := UVWork ⊕ Option ReadResult

def uvAdvance : UVState → UVState
  | .inr result => .inr result
  | .inl ([],_,_,_) => .inr none
  | .inl (b::bs,acc,shift,used) =>
      if b < 256 then
        let next := acc + 2^shift*(b%128)
        if b < 128 then .inr (some (next,(b::used).reverse,bs))
        else .inl (bs,next,shift+7,b::used)
      else .inr none

theorem uvAdvance_terminal (fuel : ℕ) (r : Option ReadResult) :
    uvAdvance^[fuel] (.inr r) = .inr r := by
  induction fuel with
  | zero => rfl
  | succ fuel ih => simpa [Function.iterate_succ_apply, uvAdvance] using ih

theorem uvAdvance_complete (bs : List ℕ) (acc shift : ℕ) (used : List ℕ) :
    uvAdvance^[bs.length+1] (.inl (bs,acc,shift,used)) = .inr (plainRead bs acc shift used) := by
  induction bs generalizing acc shift used with
  | nil => rfl
  | cons b bs ih =>
      simp only [List.length_cons, Function.iterate_succ_apply, uvAdvance, plainRead]
      split_ifs with hb ht
      · exact uvAdvance_terminal _ _
      · exact ih _ _ _
      · exact uvAdvance_terminal _ _

def uvFinish : UVState → Option ReadResult
  | .inl _ => none
  | .inr r => r

def plainInitialRead (bs : List ℕ) : Option ReadResult :=
  uvFinish (uvAdvance^[bs.length+1] (.inl (bs,0,0,[])))

theorem plainInitialRead_eq (bs : List ℕ) : plainInitialRead bs = readAccum bs 0 0 [] := by
  rw [plainInitialRead, uvAdvance_complete]
  exact plainRead_eq bs 0 0 [] (by norm_num)


abbrev UVConsWork := (ℕ × List ℕ) × ℕ × ℕ × List ℕ

def uvConsBranch (d : UVConsWork) : UVState :=
  let b := d.1.1
  let bs := d.1.2
  let acc := d.2.1
  let shift := d.2.2.1
  let used := d.2.2.2
  let next := acc + 2^shift*(b%128)
  if b < 256 then
    if b < 128 then .inr (some (next,(b::used).reverse,bs))
    else .inl (bs,next,shift+7,b::used)
  else .inr none

theorem uvConsBranch_primrec : Primrec uvConsBranch := by
  have hb : Primrec (fun d : UVConsWork => d.1.1) := Primrec.fst.comp Primrec.fst
  have hbs : Primrec (fun d : UVConsWork => d.1.2) := Primrec.snd.comp Primrec.fst
  have ha : Primrec (fun d : UVConsWork => d.2.1) := Primrec.fst.comp Primrec.snd
  have hs : Primrec (fun d : UVConsWork => d.2.2.1) := Primrec.fst.comp (Primrec.snd.comp Primrec.snd)
  have hu : Primrec (fun d : UVConsWork => d.2.2.2) := Primrec.snd.comp (Primrec.snd.comp Primrec.snd)
  have hp : Primrec (fun d : UVConsWork => 2^d.2.2.1) :=
    (Primrec₂.unpaired'.mp Nat.Primrec.pow).comp (Primrec.const 2) hs
  have hn := Primrec.nat_add.comp ha (Primrec.nat_mul.comp hp (Primrec.nat_mod.comp hb (Primrec.const 128)))
  have hc := Primrec.list_cons.comp hb hu
  exact Primrec.ite (Primrec.nat_lt.comp hb (Primrec.const 256))
    (Primrec.ite (Primrec.nat_lt.comp hb (Primrec.const 128))
      (Primrec.sumInr.comp (Primrec.option_some.comp (hn.pair ((Primrec.list_reverse.comp hc).pair hbs))))
      (Primrec.sumInl.comp (hbs.pair (hn.pair ((Primrec.nat_add.comp hs (Primrec.const 7)).pair hc)))))
    (Primrec.const (.inr none : UVState))

theorem uvAdvance_primrec : Primrec uvAdvance := by
  have hl : Primrec (fun w : UVWork => uvAdvance (.inl w)) := by
    have hc : Primrec₂ (fun (w : UVWork) (p : ℕ × List ℕ) => uvConsBranch (p,w.2)) :=
      (uvConsBranch_primrec.comp (Primrec.snd.pair (Primrec.snd.comp Primrec.fst))).to₂
    have hh := Primrec.list_casesOn (Primrec.fst : Primrec (fun w : UVWork => w.1))
      (Primrec.const (.inr none : UVState)) hc
    apply hh.of_eq
    intro w
    rcases w with ⟨bs,acc,shift,used⟩
    cases bs <;> rfl
  have hsum := Primrec.sumCasesOn (Primrec.id : Primrec (@id UVState))
    ((hl.comp Primrec.snd).to₂) ((Primrec.sumInr.comp Primrec.snd).to₂)
  apply hsum.of_eq
  intro s
  cases s <;> rfl

theorem uvFinish_primrec : Primrec uvFinish := by
  have h := Primrec.sumCasesOn (Primrec.id : Primrec (@id UVState))
    (Primrec.const (none : Option ReadResult)).to₂ Primrec.snd.to₂
  apply h.of_eq
  intro s
  cases s <;> rfl

theorem plainInitialRead_primrec : Primrec plainInitialRead := by
  have hi : Primrec (fun bs : List ℕ => (Sum.inl (bs,0,0,[]) : UVState)) :=
    Primrec.sumInl.comp (Primrec.id.pair (Primrec.const (0,0,[])))
  have hr := Primrec.nat_iterate (Primrec.succ.comp Primrec.list_length) hi
    ((uvAdvance_primrec.comp Primrec.snd).to₂)
  exact uvFinish_primrec.comp hr

theorem initialReadAccum_primrec : Primrec (fun bs => readAccum bs 0 0 []) :=
  plainInitialRead_primrec.of_eq plainInitialRead_eq

/-- Actual canonical reader effectivity, including malformed/truncated rejection. -/
theorem uvRead_primrec : Primrec uvRead := by
  have hs : Primrec₂ (fun (_ : List ℕ) (r : ReadResult) =>
      if r.2.1 = uv r.1 then some (r.1,r.2.2) else none) := by
    have hn : Primrec (fun p : List ℕ × ReadResult => p.2.1) := Primrec.fst.comp Primrec.snd
    have hu : Primrec (fun p : List ℕ × ReadResult => p.2.2.1) := Primrec.fst.comp (Primrec.snd.comp Primrec.snd)
    have hr : Primrec (fun p : List ℕ × ReadResult => p.2.2.2) := Primrec.snd.comp (Primrec.snd.comp Primrec.snd)
    exact (Primrec.ite (Primrec.eq.comp hu (uv_primrec.comp hn))
      (Primrec.option_some.comp (hn.pair hr)) (Primrec.const none)).to₂
  exact Primrec.option_bind initialReadAccum_primrec hs

end P02.Codec.UniformComputability
