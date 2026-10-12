import TypedObservations

/- A separate cross-typing discriminator. The identical pair and selector
polynomials are typed once through Sigma and once through Church-encoded Pi. -/
namespace CrossTypedObserver
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral inputNumeral_has app_has)
open P01AC.BooleanPrimitive (closed_has N_subst)
open P01AC.ExtensionalRepair.InternalGraph (pair_first)
set_option maxRecDepth 8192

def Selector (B : Ty) := arr B (arr B B)
def ChurchPair (B : Ty) := arr (Selector B) B
def Product (B : Ty) := Ty.sigma B (wk B)
def seed (a : Poly) := pairPoly a a
def step (b : Poly) := Poly.app (.atom .k) (pairPoly b b)
def run (n a b : Poly) := Poly.app (.app n (step b)) (seed a)
def observe (n a b : Poly) := fstPoly (run n a b)

theorem selector_form {Γ B} (hB : Form Γ B) : Form Γ (Selector B) :=
  form_arr hB (form_arr hB hB)
theorem churchPair_form {Γ B} (hB : Form Γ B) : Form Γ (ChurchPair B) :=
  form_arr (selector_form hB) hB

theorem product_form {Γ B} (hB : Form Γ B) : Form Γ (Product B) :=
  .sigma hB (form_wk hB (form_ctx hB) hB)

theorem constant_has {Γ A B b} (hA : Form Γ A) (hb : Has Γ b B) :
    Has Γ (.app (.atom .k) b) (arr A B) := by
  have hB := has_form hb
  have hAB := form_arr hA hB
  exact app_has (form_arr hB hAB) hAB (.k hB hA (form_arr hB hAB)) hb

theorem s_apply_has {Γ A B C f g}
    (hA : Form Γ A) (hB : Form Γ B) (hC : Form Γ C)
    (hf : Has Γ f (arr A (arr B C))) (hg : Has Γ g (arr A B)) :
    Has Γ (.app (.app (.atom .s) f) g) (arr A C) := by
  have hF := form_arr hA (form_arr hB hC)
  have hG := form_arr hA hB
  have hO := form_arr hA hC
  have hs := Has.s hA hB hC (form_arr hF (form_arr hG hO))
  exact app_has (form_arr hG hO) hO
    (app_has (form_arr hF (form_arr hG hO)) (form_arr hG hO) hs hf) hg

/-- The ACTUAL pairPoly SKI encoding has the Church-pair type as well. -/
theorem pair_church_has {Γ B a b} (ha : Has Γ a B) (hb : Has Γ b B) :
    Has Γ (pairPoly a b) (ChurchPair B) := by
  have hB := has_form ha
  have hE := selector_form hB
  have hBB := form_arr hB hB
  have hi : Has Γ (.atom .i) (arr (Selector B) (Selector B)) :=
    .i hE (form_arr hE hE)
  have inner := s_apply_has hE hB hBB hi (constant_has hE ha)
  exact s_apply_has hE hB hB inner (constant_has hE hb)

theorem pair_product_has {Γ B a b} (ha : Has Γ a B) (hb : Has Γ b B) :
    Has Γ (pairPoly a b) (Product B) := by
  apply Has.sigmaIntro (product_form (has_form ha))
  · simpa only [inst_wk] using has_form hb
  · exact ha
  · simpa only [inst_wk] using hb

theorem run_at {Γ C n a b} (hn : Has Γ n N)
    (hs : Has Γ (seed a) C) (hb : Has Γ (pairPoly b b) C) :
    Has Γ (run n a b) C := by
  have hC := has_form hs
  have hCC := form_arr hC hC
  have hi := TypedStructuredObserver.church_instance hC hn
  exact app_has hCC hC (app_has (form_arr hCC hCC) hCC hi (constant_has hC hb)) hs

/-- Sigma route: projection is literally application to K. -/
theorem observe_via_sigma {Γ B n a b}
    (hn : Has Γ n N) (ha : Has Γ a B) (hb : Has Γ b B) :
    Has Γ (observe n a b) B :=
  .sigmaFst (has_form ha) (product_form (has_form ha))
    (run_at hn (pair_product_has ha ha) (pair_product_has hb hb))

/-- Pi route: the same literal application to K, now typed as a selector. -/
theorem observe_via_church {Γ B n a b}
    (hn : Has Γ n N) (ha : Has Γ a B) (hb : Has Γ b B) :
    Has Γ (observe n a b) B := by
  have hB := has_form ha
  have hk : Has Γ (.atom .k) (Selector B) := .k hB hB (selector_form hB)
  exact app_has (churchPair_form hB) hB
    (run_at hn (pair_church_has ha ha) (pair_church_has hb hb)) hk

/-- The result judgement and polynomial coincide without conversion,
isomorphism transport, or a naturality assumption. -/
theorem same_endpoint_identity {Γ B n a b}
    (hn : Has Γ n N) (ha : Has Γ a B) (hb : Has Γ b B) :
    HasE Γ (.atom .i) (.identity B (observe n a b) (observe n a b)) := by
  have hs := has_inclusion (observe_via_sigma hn ha hb)
  have hc := has_inclusion (observe_via_church hn ha hb)
  exact .identityIntro (.identity (form_inclusion (has_form ha)) hs hc) hs hc (.refl _)

theorem zero_observation (a b : Poly) :
    P01DF.PolyConv (observe (inputNumeral 0) a b) a :=
  (P01DF.PolyConv.app (TypedStructuredObserver.numeral_zero_apply (step b) (seed a))
    (.refl _)).trans (pair_first a a)

theorem one_observation (a b : Poly) :
    P01DF.PolyConv (observe (inputNumeral 1) a b) b :=
  (P01DF.PolyConv.app (TypedStructuredObserver.numeral_one_apply (step b) (seed a))
    (.refl _)).trans
      ((P01DF.PolyConv.app (.k (pairPoly b b) (seed a)) (.refl _)).trans (pair_first b b))

theorem zero_source_identity {Γ B a b} (ha : Has Γ a B) (hb : Has Γ b B) :
    HasE Γ (.atom .i) (.identity B (observe (inputNumeral 0) a b) a) := by
  have hn := closed_has (inputNumeral_has 0) N_subst (form_ctx (has_form ha))
  have ho := has_inclusion (observe_via_sigma hn ha hb)
  have ha' := has_inclusion ha
  exact .identityIntro (.identity (form_inclusion (has_form ha)) ho ha') ho ha'
    (Intensional.Plus.polyConv_inclusion (zero_observation a b))

theorem one_source_identity {Γ B a b} (ha : Has Γ a B) (hb : Has Γ b B) :
    HasE Γ (.atom .i) (.identity B (observe (inputNumeral 1) a b) b) := by
  have hn := closed_has (inputNumeral_has 1) N_subst (form_ctx (has_form ha))
  have ho := has_inclusion (observe_via_church hn ha hb)
  have hb' := has_inclusion hb
  exact .identityIntro (.identity (form_inclusion (has_form hb)) ho hb') ho hb'
    (Intensional.Plus.polyConv_inclusion (one_observation a b))

universe u

def sigmaObservation {D : Type u}
    (n : ((D × D) → (D × D)) → (D × D) → (D × D)) (a b : D) : D :=
  (n (fun _ => (b,b)) (a,a)).1

def churchObservation {D : Type u}
    (n : (((D → D → D) → D) → ((D → D → D) → D)) →
      ((D → D → D) → D) → ((D → D → D) → D)) (a b : D) : D :=
  n (fun _ k => k b b) (fun k => k a a) (fun x _ => x)

/-- Conditional semantic consequence of the two source derivations.
`coherence` is equality of the values of ONE judgement, computed according to
Sigma's projection rule versus Pi's application/SKI rules. It is not assumed
for arbitrary maps, pairs of types, or Church carriers. -/
theorem no_shape_split {D : Type u}
    (ns : ((D × D) → (D × D)) → (D × D) → (D × D))
    (nc : (((D → D → D) → D) → ((D → D → D) → D)) →
      ((D → D → D) → D) → ((D → D → D) → D))
    (a b : D) (hne : a ≠ b)
    (coherence : sigmaObservation ns a b = churchObservation nc a b)
    (sigma_zero : ∀ step seed, ns step seed = seed)
    (church_one : ∀ step seed, nc step seed = step seed) : False := by
  apply hne
  simpa only [sigmaObservation, churchObservation, sigma_zero, church_one] using coherence

theorem no_reverse_shape_split {D : Type u}
    (ns : ((D × D) → (D × D)) → (D × D) → (D × D))
    (nc : (((D → D → D) → D) → ((D → D → D) → D)) →
      ((D → D → D) → D) → ((D → D → D) → D))
    (a b : D) (hne : a ≠ b)
    (coherence : sigmaObservation ns a b = churchObservation nc a b)
    (sigma_one : ∀ step seed, ns step seed = step seed)
    (church_zero : ∀ step seed, nc step seed = seed) : False := by
  apply hne.symm
  simpa only [sigmaObservation, churchObservation, sigma_one, church_zero] using coherence


/-- The two carrier syntaxes have distinct outer constructors. -/
theorem carriers_syntactically_distinct (B : Ty) : Product B ≠ ChurchPair B := by
  intro h
  cases h

def ProbeContext : Tel := [.param 0, .param 0, N]

theorem probe_context : Ctx ProbeContext := by
  have cn : Ctx [N] := .ext .nil (EffectiveCompleteness.N_form .nil)
  have cb : Ctx [.param 0,N] := .ext cn (.param cn)
  exact .ext cb (.param cb)

theorem probe_same_endpoint : HasE ProbeContext (.atom .i)
    (.identity (.param 0) (observe (.var 2) (.var 0) (.var 1))
      (observe (.var 2) (.var 0) (.var 1))) :=
  same_endpoint_identity
    (.var (EffectiveCompleteness.N_form probe_context) (.succ (.succ .zero)))
    (.var (.param probe_context) .zero) (.var (.param probe_context) (.succ .zero))

/-- Matching zero or matching one observations survive; the test does not
reject coherent fixed-count choices. -/
theorem matching_zero {D : Type u} (a b : D) :
    sigmaObservation (fun _ seed => seed) a b =
      churchObservation (fun _ seed => seed) a b := rfl

theorem matching_one {D : Type u} (a b : D) :
    sigmaObservation (fun step seed => step seed) a b =
      churchObservation (fun step seed => step seed) a b := rfl

theorem explicit_shape_split :
    Subsingleton Unit ∧
    sigmaObservation (fun step seed => step seed) false true = true ∧
    churchObservation (fun _ seed => seed) false true = false ∧
    sigmaObservation (fun step seed => step seed) false true ≠
      churchObservation (fun _ seed => seed) false true := by
  exact ⟨inferInstance, rfl, rfl, by decide⟩

#print axioms probe_same_endpoint
#print axioms explicit_shape_split

#print axioms pair_church_has
#print axioms observe_via_sigma
#print axioms observe_via_church
#print axioms same_endpoint_identity
#print axioms zero_source_identity
#print axioms one_source_identity
#print axioms no_shape_split
#print axioms no_reverse_shape_split
end CrossTypedObserver
