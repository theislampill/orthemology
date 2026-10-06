import CertificateSoundness

/-! Proof-side finite choice constructs actual submitted syntax. None of these
constructions occurs in the executable checker's dependency closure. -/
noncomputable section
namespace OrthemicCertificate
open HiddenParity HiddenParity.Stage HiddenParity.Necessity
variable {q n k : ℕ}

theorem Component.exists_valid {I : Input q n k} (hI : I.Valid)
    {B : Support q} {θ : Fin q} {A E : Finset (Pair n k)} {entry : Fin n}
    (hq : MarkovQualifying (I.kernel hI) Prod.fst B I.priority θ A E)
    (hentry : entry ∈ usedStates Prod.fst E) :
    ∃ c : Component n k, c.pairs = E ∧ c.Valid I B θ A entry := by
  classical
  obtain ⟨hEA,hno,hEC,hpar⟩ := hq
  obtain ⟨e,he⟩ := hEC.nonempty
  let root := e.1
  let U := usedStates Prod.fst E
  have hr : root ∈ U := Finset.mem_image.mpr ⟨e,he,rfl⟩
  have pathExists : ∀ s ∈ U, ∃ p : Path (Fin n) (Fin k), Path.Valid E (I.internal B) s root p := by
    intro s hs
    apply Path.exists_valid
    simpa only [Input.internal_kernel I hI B] using hEC.connected s hs root hr
  have reverseExists : ∀ s ∈ U, ∃ p : Path (Fin n) (Fin k), Path.Valid E (I.internal B) root s p := by
    intro s hs
    apply Path.exists_valid
    simpa only [Input.internal_kernel I hI B] using hEC.connected root hr s hs
  let toRoot (s : Fin n) : Path (Fin n) (Fin k) :=
    if hs : s ∈ U then Classical.choose (pathExists s hs) else ⟨s,[]⟩
  let fromRoot (s : Fin n) : Path (Fin n) (Fin k) :=
    if hs : s ∈ U then Classical.choose (reverseExists s hs) else ⟨root,[]⟩
  let links : List (Link n k) := U.toList.map (fun s => ⟨s,toRoot s,fromRoot s⟩)
  refine ⟨⟨E,root,links⟩,rfl,?_⟩
  refine ⟨hEC.nonempty,hEA,hr,hentry,?_,?_,?_,?_,?_⟩
  · simpa [links,List.map_map,Function.comp_def] using U.nodup_toList
  · simp [links,List.map_map,Function.comp_def,Component.used,U,usedStates]
  · intro l hl
    obtain ⟨s,hs,rfl⟩ := List.mem_map.mp hl
    have hsU : s ∈ U := Finset.mem_toList.mp hs
    constructor
    · simpa [toRoot,hsU] using Classical.choose_spec (pathExists s hsU)
    · simpa [fromRoot,hsU] using Classical.choose_spec (reverseExists s hsU)
  · intro f hf
    refine ⟨?_,?_,?_⟩
    · simpa only [Input.internal_kernel I hI B] using hEC.successors_nonempty f hf
    · simpa only [Input.internal_kernel I hI B] using hEC.closed f hf
    · intro y hy
      simpa only [Input.internal_kernel I hI B] using hno f hf y hy
  · intro σ hσ hm
    obtain ⟨d,⟨⟨f,hf,hfd⟩,hmin⟩,hev⟩ := hpar σ hσ (fun f hf => funext (hm f hf))
    exact ⟨f,hf,by simpa [hfd] using hev,by simpa [hfd] using hmin⟩

theorem Witness.exists_valid {I : Input q n k} (hI : I.Valid)
    {B : Support q} {θ : Fin q} {A : Finset (Pair n k)} {s : Fin n}
    (h : ReachableExit (I.kernel hI) B θ A s ∨
      ∃ t ∈ markovTargetStates (I.kernel hI) Prod.fst B I.priority θ A,
        Reach Prod.fst (internalSuccessors (I.kernel hI) B) A s t) :
    ∃ w : Witness n k, w.Valid I B A s θ := by
  classical
  rcases h with ⟨e,he,hp,y,hy,_,hc⟩ | ⟨t,ht,hp⟩
  · have hpr : Reach Prod.fst (I.internal B) A s e.1 := by simpa only [Input.internal_kernel I hI B] using hp
    obtain ⟨p,hp⟩ := Path.exists_valid hpr
    exact ⟨.exit p e y,hp,he,hy,by simpa using hc⟩
  · obtain ⟨E,hE,htE⟩ := (markovTargetStates_exact _ _ _ _ _ _ _).mp ht
    obtain ⟨c,_,hc⟩ := Component.exists_valid hI hE htE
    have hpr : Reach Prod.fst (I.internal B) A s t := by simpa only [Input.internal_kernel I hI B] using hp
    obtain ⟨p,hp⟩ := Path.exists_valid hpr
    exact ⟨.target p c t,hp,hc⟩

/-- Finite keyed obligations can be selected independently for every submitted
state/candidate key. No certificate-existence premise appears here. -/
theorem obligations_exist {I : Input q n k} (hI : I.Valid)
    (B : Support q) (W : Finset (Fin n)) (A : Finset (Pair n k))
    (hw : ∀ s ∈ W, ∀ θ ∈ B, ∃ w : Witness n k, w.Valid I B A s θ) :
    ∃ obs : List (Obligation q n k),
      (obs.map (fun o => (o.state,o.candidate))).Nodup ∧
      (obs.map (fun o => (o.state,o.candidate))).toFinset = W ×ˢ B ∧
      ∀ o ∈ obs, o.witness.Valid I B A o.state o.candidate := by
  classical
  letI : NeZero k := ⟨Nat.ne_of_gt hI.1.2.2.1⟩
  let keys := W ×ˢ B
  let witness (z : Fin n × Fin q) : Witness n k :=
    if hz : z ∈ keys then Classical.choose (hw z.1 (Finset.mem_product.mp hz).1 z.2 (Finset.mem_product.mp hz).2)
    else .exit ⟨z.1,[]⟩ (z.1,0) z.1
  let obs := keys.toList.map (fun z => (⟨z.1,z.2,witness z⟩ : Obligation q n k))
  refine ⟨obs,?_,?_,?_⟩
  · simpa [obs,List.map_map,Function.comp_def] using keys.nodup_toList
  · simp [obs,List.map_map,Function.comp_def,keys]
  · intro o ho
    obtain ⟨z,hz,rfl⟩ := List.mem_map.mp ho
    have hzkeys : z ∈ keys := Finset.mem_toList.mp hz
    simpa [witness,hzkeys] using Classical.choose_spec
      (hw z.1 (Finset.mem_product.mp hzkeys).1 z.2 (Finset.mem_product.mp hzkeys).2)

/-- A node's finite keyed syntax is constructed from the inherited fixed point. -/
theorem node_syntax_exists (I : Input q n k) (hI : I.Valid) (B : Support q) (hB : B.Nonempty) :
    ∃ N : Node q n k, N.support = B ∧
      N.states = winningRegion (I.kernel hI) I.menu I.priority B ∧
      N.pairs = regionAllowed (I.kernel hI) I.menu B
        (winningRegion (I.kernel hI) I.menu I.priority) N.states ∧
      N.KeysValid ∧ ∀ o ∈ N.obligations,
        o.witness.Valid I N.support N.pairs o.state o.candidate := by
  classical
  let W := winningRegion (I.kernel hI) I.menu I.priority B
  let A := regionAllowed (I.kernel hI) I.menu B (winningRegion (I.kernel hI) I.menu I.priority) W
  have hw : ∀ s ∈ W, ∀ θ ∈ B, ∃ w : Witness n k, w.Valid I B A s θ := by
    intro s hs θ hθ
    have hfixed := winningRegion_fixed (I.kernel hI) I.menu I.priority B hB
    have hstep : s ∈ regionStep (I.kernel hI) I.menu I.priority B
        (winningRegion (I.kernel hI) I.menu I.priority) W := by
      rw [hfixed]
      exact hs
    exact Witness.exists_valid hI (((mem_regionStep _ _ _ _ _ _ _).mp hstep).2 θ hθ)
  obtain ⟨obs,hnd,hkeys,hobs⟩ := obligations_exist hI B W A hw
  exact ⟨⟨B,W,A,obs⟩,rfl,rfl,rfl,⟨hnd,hkeys⟩,hobs⟩

/-- Completeness constructs an actual finite AST from winning regions. The
powerset here is proof-side finite selection and is absent from checking. -/
theorem region_has_certificate (I : Input q n k) (hI : I.Valid)
    (B₀ : Support q) (s₀ : Fin n)
    (hs₀ : s₀ ∈ winningRegion (I.kernel hI) I.menu I.priority B₀) :
    ∃ c : Body q n k, check I c B₀ s₀ = true := by
  classical
  letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
  let P := I.kernel hI
  let G := winningRegion P I.menu I.priority
  let supports := B₀.powerset.filter (fun B => B.Nonempty ∧ (G B).Nonempty)
  have hsupport : ∀ B ∈ supports, B.Nonempty := fun B hB => (Finset.mem_filter.mp hB).2.1
  let select (B : Support q) : Node q n k :=
    if hB : B.Nonempty then Classical.choose (node_syntax_exists I hI B hB)
    else ⟨B,∅,∅,[]⟩
  have select_spec : ∀ B ∈ supports, (select B).support = B ∧
      (select B).states = G B ∧
      (select B).pairs = regionAllowed P I.menu B G (select B).states ∧
      (select B).KeysValid ∧ ∀ o ∈ (select B).obligations,
        o.witness.Valid I (select B).support (select B).pairs o.state o.candidate := by
    intro B hB
    simpa only [select, dif_pos (hsupport B hB)] using
      Classical.choose_spec (node_syntax_exists I hI B (hsupport B hB))
  let c : Body q n k := (sortSupports supports).map select
  have cmem : ∀ B ∈ supports, select B ∈ c := by
    intro B hB
    exact List.mem_map.mpr ⟨B,(mem_sortSupports supports B).mpr hB,rfl⟩
  have ckeys : c.map Node.support = sortSupports supports := by
    change ((sortSupports supports).map select).map Node.support = sortSupports supports
    rw [List.map_map]
    conv_rhs => rw [← List.map_id (sortSupports supports)]
    apply List.map_congr_left
    intro B hB
    exact (select_spec B ((mem_sortSupports supports B).mp hB)).1
  have valid : BodyValid I c := by
    refine ⟨hI,?_,?_⟩
    · exact ⟨ckeys ▸ sortSupports_pairwise supports, ckeys ▸ sortSupports_nodup supports⟩
    · intro N hN
      obtain ⟨B,hB,rfl⟩ := List.mem_map.mp hN
      have hBs : B ∈ supports := (mem_sortSupports supports B).mp hB
      obtain ⟨hNB,hW,hA,hkeys,hobs⟩ := select_spec B hBs
      refine ⟨hNB.symm ▸ hsupport B hBs,hkeys,?_,hobs⟩
      intro e he
      rw [hA] at he
      obtain ⟨hsource,hmenu,hchild⟩ := (mem_regionAllowed _ _ _ _ _ _).mp he
      refine ⟨hsource,by simpa only [hNB] using hmenu,?_⟩
      intro y hy
      have hsemantic : (liveUpdate P B e y).Nonempty := by simpa [hNB] using hy
      have hc := hchild y hsemantic
      by_cases heq : I.live (select B).support e y = (select B).support
      · have heq' : liveUpdate P B e y = B := by simpa [hNB] using heq
        simpa only [heq,heq',if_true] using hc
      · have heq' : liveUpdate P B e y ≠ B := by simpa [hNB] using heq
        simp only [heq,if_false,heq'] at hc ⊢
        let C := I.live (select B).support e y
        have hCB : C ⊆ B := by simpa only [C,hNB] using (Finset.filter_subset (fun σ => 0 < I.row σ e y) B)
        have hC0 : C ⊆ B₀ := hCB.trans (Finset.mem_powerset.mp (Finset.mem_filter.mp hBs).1)
        have hyG : y ∈ G C := by simpa only [C,hNB,Input.live_kernel I hI B] using hc
        have hCs : C ∈ supports := Finset.mem_filter.mpr
          ⟨Finset.mem_powerset.mpr hC0,hy,⟨y,hyG⟩⟩
        have hCspec := select_spec C hCs
        refine ⟨Finset.ssubset_iff_subset_ne.mpr ⟨?_,heq⟩,
          select C,cmem C hCs,hCspec.1,?_⟩
        · exact Finset.filter_subset _ _
        · rw [hCspec.2.1]
          exact hyG
  have hB₀ : B₀.Nonempty := HiddenParity.Sufficiency.winningRegion_mem_support_nonempty
    P I.menu I.priority B₀ s₀ hs₀
  have hB₀s : B₀ ∈ supports := Finset.mem_filter.mpr
    ⟨Finset.mem_powerset.mpr (Finset.Subset.refl _),hB₀,⟨s₀,hs₀⟩⟩
  have hroot := select_spec B₀ hB₀s
  refine ⟨c,(check_iff I c B₀ s₀).mpr ⟨valid,hB₀,select B₀,cmem B₀ hB₀s,hroot.1,?_⟩⟩
  rw [hroot.2.1]
  exact hs₀

/-- Any admitted measurable-seed common policy supplies finite accepted syntax. -/
theorem policy_has_certificate [NeZero n] {R : Type*} [MeasurableSpace R]
    (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n) (d : Pair n k)
    (w : WinningPolicy (R := R) (I.kernel hI) I.menu I.priority d B s) :
    ∃ c : Body q n k, check I c B s = true :=
  region_has_certificate I hI B s (winning_policy_mem_winningRegion _ _ _ _ _ _ w)

/-- The independently checked syntax presents exactly the inherited deterministic
common-policy existence predicate. It is not a new winning-region theorem. -/
theorem semantic_iff_certificate [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (s : Fin n) (d : Pair n k) :
    SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority d B s ↔
      ∃ c : Body q n k, check I c B s = true := by
  constructor
  · rintro ⟨w⟩
    exact policy_has_certificate I hI B s d w
  · rintro ⟨c,hc⟩
    exact check_sound hc d
end OrthemicCertificate
