import EffectiveRenewalBoundary
import RuntimeAudit

namespace IndependentBoundaryChecks
open EffectiveRenewal EffectiveRenewal.Contract EffectiveRenewal.Pruning

-- Total finite snapshots with pauses; extraction needs no advance waiting bound.
def pausedSnapshots (t : Nat) : Word := prefixWord (fun _ => false) (t / 3)
example : Computable pausedSnapshots :=
  (prefixWord_computable _ (Computable.const false)).comp
    (Primrec.nat_div.comp Primrec.id (Primrec.const 3)).to_comp
example : Committed pausedSnapshots := by
  intro s t hst
  exact prefixWord_committed _ _ _ (Nat.div_le_div_right hst)
example : UnboundedOutput pausedSnapshots := by
  intro n
  refine ⟨n * 3, ?_⟩
  simp [pausedSnapshots]

-- A range-exact enumerator may emit nothing for arbitrarily many initial ticks,
-- repeat words, and use an index unrelated to the emitted word's length.
def delayedEnum (delay : Nat) (n : Nat) : Option Word :=
  if n < delay then none else some (prefixWord (fun _ => false) ((n - delay) / 3))
theorem delayedEnum_primrec (delay : Nat) : Primrec (delayedEnum delay) := by
  have hz : Primrec (prefixWord (fun _ => false)) :=
    Primrec.list_map Primrec.list_range (Primrec.const false).to₂
  have hi : Primrec fun n : Nat => (n - delay) / 3 :=
    Primrec.nat_div.comp (Primrec.nat_sub.comp Primrec.id (Primrec.const delay)) (Primrec.const 3)
  exact Primrec.ite (Primrec.nat_lt.comp Primrec.id (Primrec.const delay))
    (Primrec.const none) (Primrec.option_some.comp (hz.comp hi))

theorem delayedEnum_exact (delay : Nat) (s : Word) :
    pathPrefixes (fun _ => false) s ↔ ∃ n, delayedEnum delay n = some s := by
  constructor
  · intro h
    refine ⟨delay + s.length * 3, ?_⟩
    simp only [delayedEnum, show ¬ delay + s.length * 3 < delay by omega, if_false]
    simp only [Nat.add_sub_cancel_left, Nat.mul_div_cancel _ (by decide : 0 < 3)]
    exact congrArg some h.symm
  · rintro ⟨n, hn⟩
    unfold delayedEnum at hn
    split at hn
    · contradiction
    · have hs := Option.some.inj hn
      subst s
      simp [pathPrefixes]

def delayedRun (delay n : Nat) : Word :=
  (enumRun (delayedEnum delay) n).get
    ((enumRun_good (pathPrefixes (fun _ => false)) (delayedEnum delay)
      (delayedEnum_exact delay) (pathPrefixes_rooted_pruned _) n).choose_spec.1.1)

example (c : Config) (b : Bool) : request true b (terminate c) = terminate c := by
  simp [request, terminate]
example (c : Config) (b : Bool) (h : treeCheck (c.1 ++ [b]) = false) :
    request true b c = c := by
  simp [request, h]
example (c : Config) (b : Bool) (k : Nat) (hk : k ≤ c.1.length) :
    ¬ operativeSupport (migrate c b) (.instanceToken k) := all_older_tokens_excluded c b k hk

-- Audit the observation search as well as the frozen runtime root set.
#audit_renewal_runtime EffectiveRenewal.observedBit
#audit_renewal_runtime EffectiveRenewal.Pruning.nextChild
#eval delayedRun 100 6
#eval finiteProcess 5 [] (false, true)
#eval finiteProcess 0 [true] (false, true)
end IndependentBoundaryChecks
