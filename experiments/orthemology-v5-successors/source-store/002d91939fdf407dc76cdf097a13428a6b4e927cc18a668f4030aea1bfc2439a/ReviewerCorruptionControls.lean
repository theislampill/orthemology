import BadStoreErasure

namespace SharedAlias.Progress.IndependentCorruptionReview
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
open BadStore
noncomputable section
open Classical

/-- The erasure relation cannot hide even one altered good actual-root store. -/
theorem changed_good_store_is_not_erased {m} {I : Interface m}
    (E : Environment I) (C : SharedAlias.State I) (i : Fin m) (z : RootState I)
    (good : Good E.labelConfig i) (changed : C.roots (E.rootOf i) ≠ z) :
    ¬ SameGoodState E C (SharedAlias.setRoot C (E.rootOf i) z) := by
  intro same
  have roots := same.roots i good
  apply changed
  simpa only [SharedAlias.setRoot, Function.update_self] using roots

/-- Even an otherwise legal acknowledgement is not an invisible store rewrite:
its genuine new label receipt changes a common coordinate. -/
theorem fresh_acknowledgement_is_not_erased {m} {I : Interface m}
    (E : Environment I) (C : SharedAlias.State I) (i : Fin m)
    (fresh : i ∉ C.acks) :
    ¬ SameGoodState E C (SharedAlias.acknowledge E C i) := by
  intro same
  have receipts := same.acks
  have present : i ∈ (SharedAlias.acknowledge E C i).acks := by
    simp only [acknowledge_receipts, Finset.mem_insert_self]
  rw [← receipts] at present
  exact fresh present

/-- Arbitrary bad-root contents cannot alter the unchanged gate Boolean, for
either value of the source's existing badOpen switch. -/
theorem arbitrary_bad_rewrite_preserves_exact_attempt {m}
    (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (i : Fin m) (z : RootState (interface m)) (bad : i ∈ E.labelConfig.faulty)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) :
    applied E C k who time badOpen =
      applied E (SharedAlias.setRoot C (E.rootOf i) z) k who time badOpen :=
  applied_congr (corrupt_preserves E C i z bad) k who time badOpen

/-- A nonempty corruption insertion cannot retain the original total-event
bound. This test charges all extra writes even though their effects erase. -/
theorem nonempty_insertions_exceed_core_length {m} {I : Interface m}
    (E : Environment I) (service actual : List (Event I)) (added : Nat)
    (weave : Weave E service actual added) (core : service.length = 259)
    (positive : 0 < added) : 259 < actual.length := by
  have count := weave_length weave
  omega

/-- Universal, not existential endpoint selection: every actual finite woven
trace of the source-derived fixed program has exactly one installation and no
repairs. No successful trace is a premise supplied by this theorem's caller. -/
theorem every_realized_fixture_has_exact_counters
    (E : Environment (interface 7)) (q : E.q = 5)
    (source0 : E.source 0 = Witness.Fixture.source 0)
    (badSync : Fin 7 → Bool) (bad : Nat → Replies 7) :
    ∃ specs service,
      compile Witness.actor Witness.action sevenPaths Witness.times bad = some specs ∧
      specs.length = 21 ∧ service.length = 259 ∧
      ∀ actual added final, Weave E service actual added →
        SharedAlias.Trace E (SharedAlias.initial E Witness.Fixture.before) actual final →
          final.plant = Witness.Fixture.installed ∧ actual.length = 259 + added ∧
          OperationalJoin.Typed.installCount actual = 1 ∧
          OperationalJoin.Typed.repairCount actual = 0 := by
  obtain ⟨specs, service, compiled, trials, length, _reference, every⟩ :=
    every_woven_installation_has_exact_effect E q source0 badSync bad
  refine ⟨specs, service, compiled, trials, length, ?_⟩
  intro actual added final weave realized
  obtain ⟨effect, count⟩ := every actual added final weave realized
  have reach : SharedAlias.Reachable E (SharedAlias.initial E Witness.Fixture.before) :=
    ⟨Witness.Fixture.before, [], .nil _⟩
  have counters := SharedAlias.Typed.trace_counters reach realized
  have installs := counters.1
  have repairs := counters.2.1
  rw [effect] at installs repairs
  change 4 = 3 + OperationalJoin.Typed.installCount actual at installs
  change 8 = 8 + OperationalJoin.Typed.repairCount actual at repairs
  exact ⟨effect, count, by omega, by omega⟩

end
end SharedAlias.Progress.IndependentCorruptionReview

#print axioms SharedAlias.Progress.IndependentCorruptionReview.changed_good_store_is_not_erased
#print axioms SharedAlias.Progress.IndependentCorruptionReview.fresh_acknowledgement_is_not_erased
#print axioms SharedAlias.Progress.IndependentCorruptionReview.arbitrary_bad_rewrite_preserves_exact_attempt
#print axioms SharedAlias.Progress.IndependentCorruptionReview.nonempty_insertions_exceed_core_length
#print axioms SharedAlias.Progress.IndependentCorruptionReview.every_realized_fixture_has_exact_counters
