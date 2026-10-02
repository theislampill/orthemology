import SourceChecker
namespace P03Source
open OrthemologyV2 OrthemologyV3

theorem certSteps_commute (n : Nat) (c : Cert) :
    certSteps n (.step c) = .step (certSteps n c) := by
  induction n with
  | zero => rfl
  | succ n ih => simp [certSteps, ih]

theorem check_step_matches {d : Nat} {c : Cert} {v : Checked} {u : Term}
    (hc : check d c = some v) (hs : sourceHeadStep v.term = some u) :
    ∃ w, check d (.step c) = some w ∧ w.term = u ∧ w.ty = v.ty := by
  have hm : (certifiedHeadStep v.term).map Subtype.val = some u :=
    (sourceHeadStep_eq v.term).trans hs
  cases hh : certifiedHeadStep v.term with
  | none => simp [hh] at hm
  | some next =>
      simp only [hh, Option.map, Option.some.injEq] at hm
      subst u
      refine ⟨⟨next.val, v.ty, .reduce v.valid (Red.one next.property)⟩, ?_, rfl, rfl⟩
      simp [check, hc, hh]

theorem trace_tail_matches (trace : List Term) {d : Nat} {c : Cert} {v : Checked}
    (hc : check d c = some v) {u : Term}
    (ht : sourceTraceTail v.term trace = some u) :
    ∃ w, check d (certSteps trace.length c) = some w ∧ w.term = u ∧ w.ty = v.ty := by
  induction trace generalizing c v with
  | nil =>
      simp only [sourceTraceTail, Option.some.injEq] at ht
      exact ⟨v, hc, ht, rfl⟩
  | cons next rest ih =>
      simp only [sourceTraceTail] at ht
      split at ht
      next hs =>
        obtain ⟨w, hw, hterm, htype⟩ := check_step_matches hc hs
        have hnext : sourceTraceTail w.term rest = some u := by rw [hterm]; exact ht
        obtain ⟨last, hlast, hout, hty⟩ := ih hw hnext
        refine ⟨last, ?_, hout, hty.trans htype⟩
        simpa only [List.length_cons, certSteps, certSteps_commute] using hlast
      next hfail => contradiction

theorem trace_matches {trace : List Term} {d : Nat} {c : Cert} {v : Checked}
    (hc : check d c = some v) {u : Term} (ht : sourceTrace v.term trace = some u) :
    ∃ w, check d (certSteps (trace.length-1) c) = some w ∧ w.term = u ∧ w.ty = v.ty := by
  cases trace with
  | nil => contradiction
  | cons first rest =>
      simp only [sourceTrace] at ht
      split at ht
      next he =>
        simpa using trace_tail_matches rest hc ht
      next hne => contradiction

/-- Main induction: it uses the independent source evaluator's successful
branches, never uses target acceptance to define the source result. -/
theorem source_core_export_square (p : SourceProof) (d : Nat) (output : Term × TypeCode)
    (h : sourceCheckCore d p = some output) : Agrees d p output := by
  induction p generalizing d output with
  | i A =>
      simp only [sourceCheckCore, sourceScoped_eq] at h
      split at h
      next hs =>
        cases h
        exact ⟨⟨.i, .arrow A A, .i A⟩, by simp [encode, check, hs], rfl⟩
      next hn => contradiction
  | k A B =>
      simp only [sourceCheckCore, sourceScoped_eq] at h
      split at h
      next hs =>
        cases h
        exact ⟨⟨.k, .arrow A (.arrow B A), .k A B⟩, by simp [encode, check, hs], rfl⟩
      next hn => contradiction
  | s A B C =>
      simp only [sourceCheckCore, sourceScoped_eq] at h
      split at h
      next hs =>
        cases h
        exact ⟨⟨.s, .arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C)), .s A B C⟩,
          by simp [encode, check, hs], rfl⟩
      next hn => contradiction
  | app p q ihp ihq =>
      simp only [sourceCheckCore] at h
      cases hp : sourceCheckCore d p with
      | none => simp [hp] at h
      | some fp =>
          rcases fp with ⟨f, FT⟩
          cases hq : sourceCheckCore d q with
          | none => simp [hp, hq] at h
          | some xp =>
              rcases xp with ⟨x, XT⟩
              cases FT with
              | var n => simp [hp, hq] at h
              | bottom => simp [hp, hq] at h
              | all B => simp [hp, hq] at h
              | arrow A B =>
                  simp only [hp, hq] at h
                  split at h
                  next he =>
                    subst XT
                    cases h
                    obtain ⟨fv, hfv, efv⟩ := ihp d (f, .arrow A B) hp
                    obtain ⟨xv, hxv, exv⟩ := ihq d (x, A) hq
                    have eft : fv.term = f := congrArg Prod.fst efv
                    have efa : fv.ty = .arrow A B := congrArg Prod.snd efv
                    have ext : xv.term = x := congrArg Prod.fst exv
                    have exa : xv.ty = A := congrArg Prod.snd exv
                    refine ⟨⟨.app f x, B, ?_⟩, ?_, rfl⟩
                    · exact .app (eft ▸ efa ▸ fv.valid) (ext ▸ exa ▸ xv.valid)
                    · cases fv; cases xv; simp_all [checkedView, encode, check]
                  next hn => contradiction
  | allI p ih =>
      simp only [sourceCheckCore] at h
      cases hp : sourceCheckCore (d+1) p with
      | none => simp [hp] at h
      | some pair =>
          rcases pair with ⟨t, A⟩
          simp only [hp, Option.some.injEq] at h
          subst output
          obtain ⟨v, hv, ev⟩ := ih (d+1) (t, A) hp
          have et : v.term = t := congrArg Prod.fst ev
          have ea : v.ty = A := congrArg Prod.snd ev
          refine ⟨⟨t, .all A, .allI (et ▸ ea ▸ v.valid)⟩, ?_, rfl⟩
          simp [encode, check, hv, et, ea]
  | allE p A ih =>
      simp only [sourceCheckCore] at h
      split at h
      next hscope =>
        cases hp : sourceCheckCore d p with
        | none => simp [hp] at h
        | some pair =>
            rcases pair with ⟨t, PT⟩
            cases PT with
            | var n => simp [hp] at h
            | bottom => simp [hp] at h
            | arrow B C => simp [hp] at h
            | all B =>
                simp only [hp] at h
                split at h
                next houtscope =>
                  cases h
                  obtain ⟨v, hv, ev⟩ := ih d (t, .all B) hp
                  have et : v.term = t := congrArg Prod.fst ev
                  have ea : v.ty = .all B := congrArg Prod.snd ev
                  have hsc : wellScoped d A = true := by simpa only [sourceScoped_eq] using hscope
                  refine ⟨⟨t, instantiateType B A, .allE (et ▸ ea ▸ v.valid) A⟩, ?_, ?_⟩
                  · cases v; simp_all [checkedView, encode, check]
                  · simp [checkedView, sourceInstantiate_eq]
                next hno => contradiction
      next hnoscope => contradiction
  | reduce p trace ih =>
      simp only [sourceCheckCore] at h
      cases hp : sourceCheckCore d p with
      | none => simp [hp] at h
      | some pair =>
          rcases pair with ⟨t, A⟩
          simp only [hp] at h
          cases ht : sourceTrace t trace with
          | none => simp [ht] at h
          | some u =>
              simp only [ht, Option.map, Option.some.injEq] at h
              subst output
              obtain ⟨v, hv, ev⟩ := ih d (t, A) hp
              have et : v.term = t := congrArg Prod.fst ev
              have ea : v.ty = A := congrArg Prod.snd ev
              obtain ⟨w, hw, wt, wa⟩ := trace_matches hv (by rw [et]; exact ht)
              exact ⟨w, hw, by simp [checkedView, wt, wa, ea]⟩

#print axioms source_core_export_square
end P03Source
