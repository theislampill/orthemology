import HiddenChangeFinite

/-! Explicit submitted finite evidence. Soundness and completeness below concern
only the finite greatest region. They do not assert stochastic policy existence. -/
namespace HiddenChange
open HiddenParity OrthemicCertificate.Path
variable {n k : ℕ}

structure KnownObligation (n k : ℕ) where
  source : State n
  route : PhysicalPath n k
  component : PairSet n k
  deriving DecidableEq
inductive UncertainWitness (n k : ℕ) where
  | component (route : PhysicalPath n k) (pairs : PairSet n k)
  | reveal (route : PhysicalPath n k) (action : Action k) (receipt : State n)
  deriving DecidableEq
structure UncertainObligation (n k : ℕ) where
  source : State n
  candidate : Mode
  witness : UncertainWitness n k
  deriving DecidableEq
structure PositiveBody (n k : ℕ) where
  K : Region n
  W : Region n
  D1 : PairSet n k
  D : PairSet n k
  known : List (KnownObligation n k)
  uncertain : List (UncertainObligation n k)
  deriving DecidableEq
structure NegativeBody (n : ℕ) where
  knownTrace : List (Region n)
  uncertainTrace : List (Region n)
  deriving DecidableEq

def KnownObligation.Valid (I : Input n k) (D : PairSet n k) (o : KnownObligation n k) : Prop :=
  o.component ⊆ D ∧ KnownGood I o.component ∧
  OrthemicCertificate.Path.Valid D (succ I 1) o.source o.route.endpoint o.route ∧
  o.route.endpoint ∈ usedStates Prod.fst o.component
instance (I : Input n k) (D : PairSet n k) (o : KnownObligation n k) :
    Decidable (o.Valid I D) := by unfold KnownObligation.Valid; infer_instance

def UncertainObligation.Valid (I : Input n k) (K : Region n)
    (D : PairSet n k) (o : UncertainObligation n k) : Prop :=
  match o.witness with
  | .component route E => E ⊆ D ∧ UncertainGood I o.candidate E ∧
      OrthemicCertificate.Path.Valid D (internalSucc I o.candidate) o.source route.endpoint route ∧
      route.endpoint ∈ usedStates Prod.fst E
  | .reveal route a y =>
      OrthemicCertificate.Path.Valid D (internalSucc I o.candidate) o.source route.endpoint route ∧
      (route.endpoint, a) ∈ D ∧ y ∈ K ∧
      0 < I.row o.candidate (route.endpoint, a) y ∧ I.row 0 (route.endpoint, a) y = 0
instance (I : Input n k) (K : Region n) (D : PairSet n k) (o : UncertainObligation n k) :
    Decidable (o.Valid I K D) := by
  unfold UncertainObligation.Valid
  split <;> infer_instance

def uncertainKey (o : UncertainObligation n k) : State n × Mode := (o.source, o.candidate)

def BodyValid (I : Input n k) (c : PositiveBody n k) : Prop :=
  c.D1 ⊆ knownAllowed I c.K ∧ c.D ⊆ uncertainAllowed I c.K c.W ∧
  (c.known.map KnownObligation.source).Nodup ∧
  (c.known.map KnownObligation.source).toFinset = c.K ∧
  (c.uncertain.map uncertainKey).Nodup ∧
  (c.uncertain.map uncertainKey).toFinset = c.W ×ˢ Finset.univ ∧
  (∀ o ∈ c.known, o.Valid I c.D1) ∧
  (∀ o ∈ c.uncertain, o.Valid I c.K c.D)
instance (I : Input n k) (c : PositiveBody n k) : Decidable (BodyValid I c) := by
  unfold BodyValid; infer_instance

def positiveCheck (I : Input n k) (s : State n) (c : PositiveBody n k) : Bool :=
  if I.inputCheck then decide ((∀ t, (commonMenu I t).Nonempty) ∧ BodyValid I c ∧ s ∈ c.W)
  else false

@[simp] theorem positiveCheck_iff (I : Input n k) (s : State n) (c : PositiveBody n k) :
    positiveCheck I s c = true ↔ Admissible I ∧ BodyValid I c ∧ s ∈ c.W := by
  by_cases h : I.inputCheck = true
  · have hv := OrthemicCertificate.Input.inputCheck_iff I |>.mp h
    simp [positiveCheck, h, Admissible, hv]
  · have hv : ¬ I.Valid := fun hv => h ((OrthemicCertificate.Input.inputCheck_iff I).mpr hv)
    simp [positiveCheck, h, Admissible, hv]

theorem KnownObligation.progress (I : Input n k) (D : PairSet n k)
    (o : KnownObligation n k) (h : o.Valid I D) : KnownProgress I D o.source :=
  ⟨o.component, Finset.mem_powerset.mpr h.1, h.2.1, o.route.endpoint, h.2.2.2,
    OrthemicCertificate.Path.valid_sound h.2.2.1⟩
theorem UncertainObligation.progress (I : Input n k) (K : Region n) (D : PairSet n k)
    (o : UncertainObligation n k) (h : o.Valid I K D) : UncertainProgress I K D o.candidate o.source := by
  rcases o with ⟨s, θ, w⟩
  cases w with
  | component route E =>
      exact Or.inl ⟨E, Finset.mem_powerset.mpr h.1, h.2.1, route.endpoint, h.2.2.2,
        OrthemicCertificate.Path.valid_sound h.2.2.1⟩
  | reveal route a y =>
      exact Or.inr ⟨(route.endpoint,a), h.2.1, y, h.2.2.1,
        OrthemicCertificate.Path.valid_sound h.1, h.2.2.2.1, h.2.2.2.2⟩

theorem body_known_postfixed (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) : c.K ⊆ F1 I c.K := by
  intro s hs
  have hkey : s ∈ (c.known.map KnownObligation.source).toFinset := hc.2.2.2.1.symm ▸ hs
  obtain ⟨o, ho, hos⟩ := List.mem_map.mp (List.mem_toFinset.mp hkey)
  apply (mem_F1 I c.K s).mpr
  refine ⟨hs, ?_⟩
  rw [← hos]
  exact knownProgress_mono I hc.1 (o.progress I c.D1 (hc.2.2.2.2.2.2.1 o ho))

theorem body_uncertain_postfixed (I : Input n k) (c : PositiveBody n k)
    (hc : BodyValid I c) : c.W ⊆ F I (knownRegion I) c.W := by
  have hK := knownRegion_greatest I c.K (body_known_postfixed I c hc)
  intro s hs
  apply (mem_F I (knownRegion I) c.W s).mpr
  refine ⟨hs, ?_⟩
  intro θ
  have hkey : (s,θ) ∈ (c.uncertain.map uncertainKey).toFinset := by
    rw [hc.2.2.2.2.2.1]
    exact Finset.mem_product.mpr ⟨hs, Finset.mem_univ _⟩
  obtain ⟨o, ho, hos⟩ := List.mem_map.mp (List.mem_toFinset.mp hkey)
  have hsrc := congrArg Prod.fst hos
  have hcan := congrArg Prod.snd hos
  change o.source = s at hsrc
  change o.candidate = θ at hcan
  rw [← hsrc, ← hcan]
  exact uncertainProgress_mono I hK
    (hc.2.1.trans (uncertainAllowed_mono I hK (Finset.Subset.refl _)))
    (o.progress I c.K c.D (hc.2.2.2.2.2.2.2 o ho))

theorem positiveCheck_sound (I : Input n k) (s : State n) (c : PositiveBody n k)
    (hc : positiveCheck I s c = true) : s ∈ uncertainRegion I := by
  rcases (positiveCheck_iff I s c).mp hc with ⟨_, hb, hs⟩
  exact uncertainRegion_greatest I c.W (body_uncertain_postfixed I c hb) hs

/-- A finite family of local existential witnesses reifies into a duplicate-free
submitted list with exact key coverage; no semantic success field is introduced. -/
theorem exists_keyed_list {Key Value : Type*} [DecidableEq Key]
    (K : Finset Key) (key : Value → Key) (valid : Value → Prop)
    (h : ∀ s ∈ K, ∃ v, key v = s ∧ valid v) :
    ∃ xs : List Value, (xs.map key).Nodup ∧ (xs.map key).toFinset = K ∧
      ∀ v ∈ xs, valid v := by
  classical
  induction K using Finset.induction_on with
  | empty => exact ⟨[], by simp, by simp, by simp⟩
  | @insert a K ha ih =>
      obtain ⟨v, hv, hvalid⟩ := h a (Finset.mem_insert_self _ _)
      obtain ⟨xs, hn, hkeys, hxs⟩ := ih (fun s hs => h s (Finset.mem_insert_of_mem hs))
      refine ⟨v :: xs, ?_, ?_, ?_⟩
      · simp only [List.map_cons, List.nodup_cons, hv]
        refine ⟨?_, hn⟩
        intro hamem
        exact ha (hkeys ▸ List.mem_toFinset.mpr hamem)
      · simp [hv, hkeys]
      · intro w hw
        rcases List.mem_cons.mp hw with rfl | hw
        · exact hvalid
        · exact hxs w hw

theorem exists_known_obligation (I : Input n k) (D : PairSet n k) (s : State n)
    (h : KnownProgress I D s) : ∃ o : KnownObligation n k, o.source = s ∧ o.Valid I D := by
  rcases h with ⟨E, hE, hg, t, ht, hr⟩
  obtain ⟨p, hp⟩ := OrthemicCertificate.Path.exists_valid hr
  refine ⟨⟨s,p,E⟩, rfl, Finset.mem_powerset.mp hE, hg, ?_, ?_⟩
  · exact ⟨hp.1, rfl, hp.2.2⟩
  · exact hp.2.1.symm ▸ ht

theorem exists_uncertain_obligation (I : Input n k) (K : Region n) (D : PairSet n k)
    (s : State n) (θ : Mode) (h : UncertainProgress I K D θ s) :
    ∃ o : UncertainObligation n k, uncertainKey o = (s,θ) ∧ o.Valid I K D := by
  rcases h with ⟨E,hE,hg,t,ht,hr⟩ | ⟨e,he,y,hy,hr,hp,hz⟩
  · obtain ⟨p, hp⟩ := OrthemicCertificate.Path.exists_valid hr
    refine ⟨⟨s,θ,.component p E⟩, rfl, Finset.mem_powerset.mp hE, hg, ?_, ?_⟩
    · exact ⟨hp.1, rfl, hp.2.2⟩
    · exact hp.2.1.symm ▸ ht
  · obtain ⟨p, hpath⟩ := OrthemicCertificate.Path.exists_valid hr
    have heq : (p.endpoint,e.2) = e := by rw [hpath.2.1]
    refine ⟨⟨s,θ,.reveal p e.2 y⟩, rfl, ?_, ?_, hy, ?_, ?_⟩
    · exact ⟨hpath.1, rfl, hpath.2.2⟩
    · simpa only [heq] using he
    · simpa only [heq] using hp
    · simpa only [heq] using hz

theorem exists_region_body (I : Input n k) :
    ∃ c : PositiveBody n k, BodyValid I c ∧ c.W = uncertainRegion I := by
  let K := knownRegion I
  let W := uncertainRegion I
  let D1 := knownAllowed I K
  let D := uncertainAllowed I K W
  have hk : ∀ s ∈ K, ∃ o : KnownObligation n k, o.source = s ∧ o.Valid I D1 := by
    intro s hs
    apply exists_known_obligation
    exact ((mem_F1 I K s).mp ((knownRegion_fixed I).symm ▸ hs)).2
  have hw : ∀ st ∈ W ×ˢ (Finset.univ : Finset Mode),
      ∃ o : UncertainObligation n k, uncertainKey o = st ∧ o.Valid I K D := by
    intro st hst
    rcases st with ⟨s,θ⟩
    apply exists_uncertain_obligation
    exact ((mem_F I K W s).mp ((uncertainRegion_fixed I).symm ▸
      (Finset.mem_product.mp hst).1)).2 θ
  obtain ⟨known, hkn, hkk, hkv⟩ := exists_keyed_list K KnownObligation.source
    (fun o => o.Valid I D1) hk
  obtain ⟨uncertain, hun, huk, huv⟩ := exists_keyed_list (W ×ˢ Finset.univ) uncertainKey
    (fun o => o.Valid I K D) hw
  exact ⟨⟨K,W,D1,D,known,uncertain⟩,
    ⟨Finset.Subset.refl _, Finset.Subset.refl _, hkn, hkk, hun, huk, hkv, huv⟩, rfl⟩

theorem positiveCheck_iff_region (I : Input n k) (hI : Admissible I) (s : State n) :
    (∃ c, positiveCheck I s c = true) ↔ s ∈ uncertainRegion I := by
  constructor
  · rintro ⟨c,hc⟩; exact positiveCheck_sound I s c hc
  · intro hs
    obtain ⟨c,hc,hw⟩ := exists_region_body I
    exact ⟨c,(positiveCheck_iff I s c).mpr ⟨hI,hc,hw.symm ▸ hs⟩⟩

/-- The complete descending trace starts at the full carrier, recomputes every
step, and explicitly repeats its terminal fixed point. The n+2 bound counts the
initial element and the repeated terminal, not just strict decreases. -/
def ValidTrace (op : Region n → Region n) (xs : List (Region n)) : Prop :=
  xs.head? = some Finset.univ ∧ xs.Chain' (fun U V => V = op U) ∧
  xs.length ≤ n + 2 ∧ ∃ pre W, xs = pre ++ [W,W]

private theorem repeated_iff (xs : List (Region n)) :
    (∃ pre W, xs = pre ++ [W,W]) ↔
    ∃ W ∈ xs, xs = xs.dropLast.dropLast ++ [W,W] := by
  constructor
  · rintro ⟨pre,W,rfl⟩
    exact ⟨W, by simp, by simp [List.dropLast_append]⟩
  · rintro ⟨W,_,h⟩
    exact ⟨_,W,h⟩

instance (op : Region n → Region n) (xs : List (Region n)) : Decidable (ValidTrace op xs) := by
  letI : Decidable (∃ pre W, xs = pre ++ [W,W]) :=
    decidable_of_iff (∃ W ∈ xs, xs = xs.dropLast.dropLast ++ [W,W]) (repeated_iff xs).symm
  unfold ValidTrace
  infer_instance

def traceTerminal (xs : List (Region n)) : Region n := xs.getLast?.getD ∅

private theorem terminal_of_repeated (pre : List (Region n)) (W : Region n) :
    traceTerminal (pre ++ [W,W]) = W := by simp [traceTerminal, List.getLast?_append]

private theorem postfixed_chain (op : Region n → Region n) (hMono : Monotone op)
    {V W : Region n} {xs : List (Region n)} (hV : V ⊆ op V) (hVW : V ⊆ W)
    (hc : xs.Chain (fun U T => T = op U) W) : ∀ T ∈ xs, V ⊆ T := by
  induction hc with
  | nil => intro T ht; exact False.elim (List.not_mem_nil ht)
  | @cons W U xs hstep hrest ih =>
      have hVU : V ⊆ U := hstep ▸ hV.trans (hMono hVW)
      intro T hT
      rcases List.mem_cons.mp hT with rfl | hT
      · exact hVU
      · exact ih hVU T hT

/-- Every postfixed set survives every submitted recomputed trace element. -/
theorem postfixed_subset_traceTerminal (op : Region n → Region n) (hMono : Monotone op)
    {V : Region n} (hV : V ⊆ op V) (xs : List (Region n)) (hx : ValidTrace op xs) :
    V ⊆ traceTerminal xs := by
  obtain ⟨pre,W,hrep⟩ := hx.2.2.2
  have ht : traceTerminal xs = W := hrep ▸ terminal_of_repeated pre W
  have hmem : W ∈ xs := by rw [hrep]; simp
  cases xs with
  | nil => exact False.elim (List.not_mem_nil hmem)
  | cons U rest =>
      have hU : U = Finset.univ := by simpa using hx.1
      have hVU : V ⊆ U := hU ▸ Finset.subset_univ V
      rw [ht]
      rcases List.mem_cons.mp hmem with rfl | hm
      · exact hVU
      · exact postfixed_chain op hMono hV hVU hx.2.1 W hm

/-- Requiring a repeated terminal really verifies fixedness. -/
theorem traceTerminal_fixed (op : Region n → Region n) (xs : List (Region n))
    (hx : ValidTrace op xs) : op (traceTerminal xs) = traceTerminal xs := by
  obtain ⟨pre,W,hrep⟩ := hx.2.2.2
  have hc := hx.2.1
  rw [hrep] at hc
  have hlast : W = op W := (List.chain'_cons.mp hc.right_of_append).1
  rw [hrep, terminal_of_repeated]
  exact hlast.symm

/-- The full trace certifies the greatest finite postfixed point, whereas
merely checking an arbitrary fixed point would be insufficient. -/
theorem traceTerminal_eq_descend (op : Region n → Region n) (hMono : Monotone op)
    (hContract : ∀ W, op W ⊆ W) (xs : List (Region n)) (hx : ValidTrace op xs) :
    traceTerminal xs = HiddenParity.Necessity.descend op n Finset.univ := by
  have ht := traceTerminal_fixed op xs hx
  have hd := HiddenParity.Necessity.descend_stable op hContract n Finset.univ (by simp)
  apply Finset.Subset.antisymm
  · exact HiddenParity.Necessity.postfixed_subset_descend op hMono
      (by rw [ht]) (Finset.subset_univ _) n
  · exact postfixed_subset_traceTerminal op hMono (by rw [hd]) xs hx

/-- Explicit finite recomputation, retaining all rounds and the terminal repeat. -/
def iterateTrace (op : Region n → Region n) : ℕ → Region n → List (Region n)
  | 0, W => [W]
  | m+1, W => W :: iterateTrace op m (op W)

@[simp] theorem iterateTrace_length (op : Region n → Region n) (m : ℕ) (W : Region n) :
    (iterateTrace op m W).length = m+1 := by
  induction m generalizing W with
  | zero => rfl
  | succ m ih => simp [iterateTrace, ih]
@[simp] theorem iterateTrace_head (op : Region n → Region n) (m : ℕ) (W : Region n) :
    (iterateTrace op m W).head? = some W := by cases m <;> rfl

theorem iterateTrace_chain (op : Region n → Region n) (m : ℕ) (W : Region n) :
    (iterateTrace op m W).Chain' (fun U V => V = op U) := by
  induction m generalizing W with
  | zero => simp [iterateTrace]
  | succ m ih =>
      rw [iterateTrace, List.chain'_cons']
      exact ⟨by simp, ih _⟩

theorem iterateTrace_repeated (op : Region n → Region n) (m : ℕ) (W : Region n)
    (h : op (HiddenParity.Necessity.descend op m W) = HiddenParity.Necessity.descend op m W) :
    ∃ pre, iterateTrace op (m+1) W = pre ++
      [HiddenParity.Necessity.descend op m W, HiddenParity.Necessity.descend op m W] := by
  induction m generalizing W with
  | zero => exact ⟨[], by simpa [iterateTrace, HiddenParity.Necessity.descend] using h⟩
  | succ m ih =>
      obtain ⟨pre,hpre⟩ := ih (op W) h
      exact ⟨W::pre, by simpa only [iterateTrace, List.cons_append, HiddenParity.Necessity.descend] using congrArg (W :: ·) hpre⟩

theorem iterateTrace_valid (op : Region n → Region n) (hContract : ∀ W, op W ⊆ W) :
    ValidTrace op (iterateTrace op (n+1) Finset.univ) := by
  refine ⟨iterateTrace_head _ _ _, iterateTrace_chain _ _ _, by simp, ?_⟩
  obtain ⟨pre,hpre⟩ := iterateTrace_repeated op n Finset.univ
    (HiddenParity.Necessity.descend_stable op hContract n Finset.univ (by simp))
  exact ⟨pre,_,hpre⟩

def NegativeValid (I : Input n k) (s : State n) (c : NegativeBody n) : Prop :=
  ValidTrace (F1 I) c.knownTrace ∧
  ValidTrace (F I (traceTerminal c.knownTrace)) c.uncertainTrace ∧
  s ∉ traceTerminal c.uncertainTrace
instance (I : Input n k) (s : State n) (c : NegativeBody n) : Decidable (NegativeValid I s c) := by
  unfold NegativeValid; infer_instance

def negativeCheck (I : Input n k) (s : State n) (c : NegativeBody n) : Bool :=
  if I.inputCheck then decide ((∀ t, (commonMenu I t).Nonempty) ∧ NegativeValid I s c) else false
@[simp] theorem negativeCheck_iff (I : Input n k) (s : State n) (c : NegativeBody n) :
    negativeCheck I s c = true ↔ Admissible I ∧ NegativeValid I s c := by
  by_cases h : I.inputCheck = true
  · have hv := (OrthemicCertificate.Input.inputCheck_iff I).mp h
    simp [negativeCheck, h, Admissible, hv]
  · have hv : ¬ I.Valid := fun hv => h ((OrthemicCertificate.Input.inputCheck_iff I).mpr hv)
    simp [negativeCheck, h, Admissible, hv]

theorem negativeCheck_sound (I : Input n k) (s : State n) (c : NegativeBody n)
    (hc : negativeCheck I s c = true) : s ∉ uncertainRegion I := by
  have hv := ((negativeCheck_iff I s c).mp hc).2
  have hk : traceTerminal c.knownTrace = knownRegion I :=
    traceTerminal_eq_descend (F1 I) (F1_mono I) (F1_subset I) _ hv.1
  have hw := hv.2.1
  rw [hk] at hw
  have he : traceTerminal c.uncertainTrace = uncertainRegion I :=
    traceTerminal_eq_descend (F I (knownRegion I)) (F_mono I _) (F_subset I _) _ hw
  exact he ▸ hv.2.2

def canonicalNegative (I : Input n k) : NegativeBody n :=
  ⟨iterateTrace (F1 I) (n+1) Finset.univ,
    iterateTrace (F I (knownRegion I)) (n+1) Finset.univ⟩

theorem canonicalNegative_accepts (I : Input n k) (hI : Admissible I) (s : State n)
    (hs : s ∉ uncertainRegion I) : negativeCheck I s (canonicalNegative I) = true := by
  have hk := iterateTrace_valid (F1 I) (F1_subset I)
  have heK : traceTerminal (iterateTrace (F1 I) (n+1) Finset.univ) = knownRegion I :=
    traceTerminal_eq_descend (F1 I) (F1_mono I) (F1_subset I) _ hk
  have hw := iterateTrace_valid (F I (knownRegion I)) (F_subset I _)
  have heW : traceTerminal (iterateTrace (F I (knownRegion I)) (n+1) Finset.univ) = uncertainRegion I :=
    traceTerminal_eq_descend (F I (knownRegion I)) (F_mono I _) (F_subset I _) _ hw
  apply (negativeCheck_iff I s _).mpr
  refine ⟨hI, hk, ?_, ?_⟩
  · simpa only [canonicalNegative, heK] using hw
  · exact heW.symm ▸ hs

theorem negativeCheck_iff_region (I : Input n k) (hI : Admissible I) (s : State n) :
    (∃ c, negativeCheck I s c = true) ↔ s ∉ uncertainRegion I := by
  constructor
  · rintro ⟨c,hc⟩; exact negativeCheck_sound I s c hc
  · intro hs; exact ⟨canonicalNegative I, canonicalNegative_accepts I hI s hs⟩
end HiddenChange
