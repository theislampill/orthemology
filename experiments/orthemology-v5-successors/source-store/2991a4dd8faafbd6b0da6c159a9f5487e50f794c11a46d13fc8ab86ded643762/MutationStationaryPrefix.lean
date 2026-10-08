import NecessityControls
open HiddenChange HiddenChangeNecessityTests MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic HiddenParity.ResidualSeed
-- False retroactive mode1 support claim: same old prefix is positive only for a late switch.
example : PositivePrefix lateInput lateValid (some 0) 0 (Measure.dirac ()) latePolicy lateHistory := by
  rw [PositivePrefix,fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _)]
  norm_num [CompatibleSeeds,ActionCompatible,pairPolicy,currentState,erasePairSources,latePolicy,
    lateHistory,fixedPrefixLikelihood,fixedMode,lateInput,OrthemicCertificate.Input.row,Fin.prod_univ_succ]
