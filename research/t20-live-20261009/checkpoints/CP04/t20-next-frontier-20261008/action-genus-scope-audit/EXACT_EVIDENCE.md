# Bounded exact evidence

Inherited research excerpts; no new historical witness.

## model_header

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/ontology-type-control/OriginationTypeControl.lean
Range: 3–8

3: /-! Representation control only, not a metaphysical possibility proof or an
4: attribution of complete cessation to Ibn Taymiyya. G is one stated kind of
5: voluntary divine act. Objects are potential labels; E alone marks present
6: existence. Type and capacity are predicates, never extra object constructors.
7: The model permits a stronger all-emergent empty state but does not identify it
8: with the weaker G-empty statement. Modal accessibility and actual time differ. -/

## model_definitions

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/ontology-type-control/OriginationTypeControl.lean
Range: 11–56

11: inductive Obj where
12:   | ground | gAct (id : Nat) | effect (id : Nat) | other (id : Nat)
13:   deriving DecidableEq
14: structure World where
15:   serial : Nat
16:   gOn : Bool
17:   otherOn : Bool
18: 
19: def E (w : World) : Obj → Prop
20:   | .ground => True
21:   | .gAct n => n = w.serial ∧ w.gOn = true
22:   | .effect n => n = w.serial ∧ w.gOn = true
23:   | .other n => n = w.serial ∧ w.otherOn = true
24: 
25: def Emergent : Obj → Prop | .ground => False | _ => True
26: def GAct : Obj → Prop | .gAct _ => True | _ => False
27: def Created : Obj → Prop | .effect _ | .other _ => True | _ => False
28: def DivineAct (a g : Obj) : Prop := GAct a ∧ g = .ground
29: def Inheres (a g : Obj) : Prop := DivineAct a g
30: def Produces : Obj → Obj → Prop
31:   | .gAct n, .effect m => n = m
32:   | _, _ => False
33: -- Whole receipt belongs to the independent bearer level; intrinsic acts are
34: -- not thereby extraneously supplied. This is an interpretation, not a theorem
35: -- denying every possible constitutive or intrinsic dependence of acts on God.
36: def ExternalReceipt (_w : World) (x : Obj) : Prop := Created x
37: 
38: def Power (w : World) (g : Obj) : Prop := E w g ∧ g = .ground
39: -- G is represented by the predicate GAct, not by another member of Obj.
40: def EmptyG (w : World) : Prop := ¬ ∃ x, E w x ∧ GAct x
41: def EmptyEmergent (w : World) : Prop := ¬ ∃ x, E w x ∧ Emergent x
42: def Necessary (x : Obj) : Prop := ∀ w, E w x
43: -- serial orders eligible fresh labels. R is an explicitly chosen modal frame,
44: -- not evidence that the corresponding transition occurs on the actual path.
45: def R (w v : World) : Prop := w.serial < v.serial
46: def Diamond (w : World) (P : World → Prop) : Prop := ∃ v, R w v ∧ P v
47: def Box (w : World) (P : World → Prop) : Prop := ∀ v, R w v → P v
48: def FreshG (w v : World) : Prop := ∃ n,
49:   w.serial < n ∧ E v (.gAct n) ∧
50:   (∀ past : World, past.serial ≤ w.serial → ¬ E past (.gAct n))
51: def PossibleFreshG (w : World) : Prop := Diamond w (FreshG w)
52: def PossibleCreated (w : World) : Prop := Diamond w (fun v => ∃ x, E v x ∧ Created x)
53: def quiet (n : Nat) : World := ⟨n, false, false⟩
54: def active (n : Nat) : World := ⟨n, true, false⟩
55: -- Repeated activity uses new identities 1,3,5,...; no old token recurs.
56: def actual (t : Nat) : World := ⟨t, t % 2 == 1, false⟩

## modal_controls

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/ontology-type-control/OriginationTypeControl.lean
Range: 58–75

58: theorem empty_all (n : Nat) : EmptyEmergent (quiet n) ∧ EmptyG (quiet n) := by
59:   constructor <;> rintro ⟨x, hx, hg⟩ <;> cases x <;> simp_all [E, quiet, Emergent, GAct]
60: 
61: theorem fresh_possible (w : World) : PossibleFreshG w := by
62:   refine ⟨active (w.serial + 1), Nat.lt_succ_self _, w.serial + 1,
63:     Nat.lt_succ_self _, ⟨rfl, rfl⟩, ?_⟩
64:   intro past hp he
65:   have h := he.1
66:   have bad : w.serial + 1 ≤ w.serial := h ▸ hp
67:   exact (Nat.not_succ_le_self _) bad
68: 
69: -- Both the requested G-scoped formula and stronger all-emergent variant are
70: -- explicit. Neither asserts that the genus is populated at every world/time.
71: theorem empty_and_renewable (w : World) :
72:     Diamond w EmptyG ∧ Diamond w EmptyEmergent ∧ Box w PossibleFreshG := by
73:   exact ⟨⟨quiet (w.serial + 1), Nat.lt_succ_self _, (empty_all _).2⟩,
74:     ⟨quiet (w.serial + 1), Nat.lt_succ_self _, (empty_all _).1⟩,
75:     fun v _ => fresh_possible v⟩

## act_product_and_cessation

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/ontology-type-control/OriginationTypeControl.lean
Range: 100–141

100: -- A present new act and its product have different createdness. Emergence does
101: -- not logically imply createdness or external receipt in this signature.
102: theorem act_product_boundary :
103:     ¬ E (actual 0) (.gAct 1) ∧ E (actual 1) (.gAct 1) ∧
104:     Emergent (.gAct 1) ∧ DivineAct (.gAct 1) .ground ∧
105:     Produces (.gAct 1) (.effect 1) ∧ E (actual 1) (.effect 1) ∧
106:     Created (.effect 1) ∧ ¬ Created (.gAct 1) ∧
107:     ¬ ExternalReceipt (actual 1) (.gAct 1) ∧
108:     Inheres (.gAct 1) .ground ∧ E (actual 1) .ground := by
109:   simp [E, actual, Emergent, DivineAct, GAct, Produces, Created,
110:     ExternalReceipt, Inheres]
111: 
112: -- Every represented emergent token ceases after its single indexed occurrence,
113: -- including tokens of the auxiliary kind. This is stronger than merely showing
114: -- different labels on two sampled states, and is independent of gOn's pattern.
115: theorem each_token_ceases (t : Nat) (x : Obj)
116:     (present : E (actual t) x) (emergent : Emergent x) :
117:     ∃ u, t < u ∧ ∀ v, u ≤ v → ¬ E (actual v) x := by
118:   refine ⟨t + 1, Nat.lt_succ_self _, ?_⟩
119:   intro v hv he
120:   have lt : t < v := Nat.lt_of_lt_of_le (Nat.lt_succ_self _) hv
121:   cases x with
122:   | ground => exact emergent
123:   | gAct n => exact (Nat.ne_of_lt lt) (present.1.symm.trans he.1)
124:   | effect n => exact (Nat.ne_of_lt lt) (present.1.symm.trans he.1)
125:   | other n => exact (Nat.ne_of_lt lt) (present.1.symm.trans he.1)
126: 
127: theorem actual_gap_and_new_act :
128:     EmptyEmergent (actual 2) ∧ E (actual 3) (.gAct 3) ∧
129:     (.gAct 3 : Obj) ≠ .gAct 1 ∧ PossibleFreshG (actual 2) ∧
130:     ¬ (∀ t, ∃ x, E (actual t) x ∧ Emergent x) := by
131:   have gap : EmptyEmergent (actual 2) := (empty_all 2).1
132:   refine ⟨gap, by simp [E, actual], by decide, fresh_possible _, ?_⟩
133:   intro all
134:   exact gap (all 2)
135: 
136: -- G-empty is strictly weaker than all kinds empty: another emergent kind may
137: -- be present while G has no present token.
138: theorem scoped_absence_is_not_global : ∃ w, EmptyG w ∧ ¬ EmptyEmergent w := by
139:   refine ⟨⟨0, false, true⟩, ?_, ?_⟩
140:   · rintro ⟨x, hx, hg⟩
141:     cases x <;> simp_all [E, GAct]

## ontology_audit

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/ontology-type-control/AUDIT.md
Range: 1–61

1: # T20 bounded ontology/type audit
2: 
3: 7 October 2026, 16:15 UTC. Additive application-scope audit and representation control. Earlier source packets and historical reports remain unchanged. The 7 October 2026 14:34 UTC defeasible assessment is unchanged.
4: 
5: ## Result
6: 
7: No inspected conditional theorem derives creaturehood, external receipt, or ontological dependence merely from temporal novelty. The central risk is an **application-scope substitution**, not a defect in the conditional proof: modal non-necessity of a bearer considered in respect of its whole existence is not temporal novelty of a particular intrinsic act. Applying the bearer-level contingency/receipt premise to all emergent act tokens would add precisely the substantive premise under dispute.
8: 
9: The acquired Arabic material positively warrants distinguishing divine acts subsisting in their agent from their created products. It does not warrant silently attributing the stronger possibility of simultaneous cessation of every emergent kind to Ibn Taymiyya. The small new formal control is **executed and checked**, not merely written; it demonstrates compatibility and non-entailment within its stipulated signature only.
10: 
11: ## Fourfold control and vocabulary
12: 
13: Keep apart (1) the necessary bearer's essential power, will, and capacity; (2) the genus/type of voluntary activity and modal availability of fresh origination; (3) a successive particular voluntary act; and (4) its created effect. An emergent particular/event is not, by logic alone, a created emergent particular. Where the Arabic source warrants it, an uncreated voluntary divine act/occurrence belongs to the former category without becoming its own independently subsisting bearer. Inherence, ownership, or intrinsic dependence on its agent is not the same predicate as external reception or being a created product.
14: 
15: Thus ¬A(g,t₁) and A(g,t₂) alone entail neither Created(A) nor a newly externally supplied perfection of g. DivineAct(a,g), Produces(a,e), and Created(e) do not entail Created(a). Nor does essential capacity mean simultaneous exercise of every possible particular act. A conclusion about a necessarily “frozen” agent requires further premises about change, creation, and receipt; this audit neither establishes nor adopts it from the disputed implication.
16: 
17: ## Definition findings, with exact bindings
18: 
19: OTC-D1–OTC-D9 in DEFINITION_BINDINGS.json resolve every inspected definition and assessment to its exact prior public alias, with separate original/public identities and line coordinates.
20: 
21: 1. **Original-bearer bridge: scope obligation, conditional theorem intact.** OTC-D1 (OriginalBearerBridge.lean)16–25 separates B bearers, R intrinsic resources, and T targets. Lines41–43 transfer actual whole-bearer receipt to an intrinsic resource, not the converse; they do not identify temporally new resources with received resources. ReceiptRepresentation46–47 is an explicit representation premise. ContingencyNeed50–52 assumes whole receipt for an actually existent, modally nonnecessary B. Necessary is ∀w E(w,g), defined in SourceIdentityDerived.lean25; it is not “unchanging at every time.” ConstitutiveReception55–57 is a further premise. The preserved-bearer proof126–139 needs no temporal premise. Its interpretation must not insert every intrinsic act into B and then call the resulting receipt consequence a proof from origination. A B-admission/whole-existence applicability argument is required first.
22: 
23: 2. **Intrinsic-necessity audit already guards the distinction.** OTC-D3 (CNDModalScope.lean)3–5 distinguishes original production from whole-existence nonreceipt and token-state receipt. CND11–13 is world-local uniqueness of an entire original production in one respect. The modal role and overlap assumptions21–33 do substantive work. The switch control56–62 explicitly keeps power, production, and whole receipt distinct. Token-state control99–113 denies the move from received state to received whole existence. None defines temporal emergence or Created. The corresponding OTC-D4 appraisal at original lines 63 and 71 (public lines 59 and 67) already says an occasioned act is not production of its bearer's existence/power, and generic activity does not establish original provenance in every alternative. No theorem correction required.
24: 
25: 3. **Original-ground controls are deliberate object extensions.** OTC-D5 (GroundExtension.lean)21–45 adds a new Option.none object, assigns it all-world existence, and keeps holder/power separate from productive edges. Necessary182–183 quantifies E. GroundNecessitates242–244 is a stated grounding-specific implication, not a principle about every temporal or support relation. Original-holder323–335 exposes its independent power parameter; capable-ground350–359 does not infer actual production. This construction must not be reused to reify an enduring genus or possibility: it intentionally adds an object for a different question. ModalCapacityControl.lean18–30 gives actual-existence and productive tables separately. Its abbreviated modalAble omits E syntactically, but each displayed production edge has existent endpoints by those particular tables; it is not a generic warrant to omit E from future modal existentials. The new control writes E explicitly.
26: 
27: 4. **Anchored-source bridge is actual-field scoped.** OTC-D7 (AnchoredSourceBridge.lean)8–17 keeps sources, occurrences, and contributions distinct. ActualOccurrence is an uninterpreted predicate, not Created. Admissible28 says field members actually occur. Classification40–41 is a qualification-and-role premise, not a theorem that every new act is externally received or defective. CND52–56 concerns original provision of the same contribution; it says nothing about temporal origination. The predicates at65–71 concern an actual anchor and represented field. They supply no ∀t∃x persistence or de re eternal event.
28: 
29: 5. **Joint model: useful sort separation, incomplete for this new question.** OTC-D8 (JointFiniteInterpretation.lean)14–22 separates W, B, E, contributions, speech tokens, and exercises. Whole receipt37–50 and occurrence/exercise66–104 are distinct tables. J03/J04 at283–290 connect the selected created-effect bearers to received targets; they do not classify every intrinsic exercise as a received bearer. Its w₂ lacks the selected received beings and occurrences, while g and h remain. These are modal-index tables, not an actual temporal trajectory, and they do not establish fresh token identities or classify a universal genus. The model's existing two necessary bearers cannot be treated as a type and its instantiation. Its limited signature is no defect; the new control addresses the different question without altering it.
30: 
31: ## Contextual Arabic reading
32: 
33: SOURCE_BINDINGS.json records exact acquired-file spans, image identities, reading status, and limits. No new scan certification is claimed for electronic texts.
34: 
35: - **Safadiyya, SF-S001-L0070–L0085; L0266–L0276; SF-S002-L0519–L0534.** Post-completion contextual reread. S001-L0073 distinguishes unrestricted activity, a particular effect's production, and producing everything; L0077 distinguishes type from particular acts. L0082 distinguishes successive acts and products; L0084 says affirming the type does not establish one particular eternal act or product. L0273 expressly separates the divine act subsisting in him from the product separate from him, while treating creatures' acts as created and genuinely theirs. S002-L0521–L0527 discusses successive particular operations versus making original creative efficacy dependent on another creative efficacy. L0529–L0530 explicitly reports that divine attributes/acts subsisting in him are not his created products across the compared accounts, including the account of successive individual acts with an enduring type. L0531–L0533 then separates positions about particular “kun” utterances. The reported alternatives must not be combined into one undifferentiated doctrine. This directly supports the act/product category correction, not total cessation of all emergent kinds.
36: 
37: - **Sharḥ al-ʿAqīda al-Aṣbahāniyya, printed65–68,96–99,103–104; PDF165–168,196–199,203–204.** Direct reread of retained images, main prose and visible relevant apparatus. Pages65–68 distinguish external existential need from qualification and concomitance;96–99 distinguish mutual conditions from efficient causal dependence and an actually qualified self from an abstract bare existent. Pages103–104 distinguish each particular's necessity from the shared abstract description. These controls block deriving a second extramental necessary individual merely by naming a common type. They do not prove an empty-genus scenario or classify every voluntary act by themselves.
38: 
39: - **Darʾ, acquired electronic section014 lines102–124, within completed volume8 body.** Contextual reread. Lines102–109 distinguish essential qualifications/type from successive particulars and explicitly discuss one individual ceasing as another succeeds it. Lines120–124 challenge a circular blanket prohibition on new occurrences in the eternal bearer. The passage's succession claim must not be rewritten as the stronger simultaneous emptiness of all emergent kinds.
40: 
41: - **Darʾ, acquired section017 lines100–148, volume10 material.** NEW bounded targeted first reading for this audit, not a claimed reread or extension of completed volume8–9 study. Lines105–115 separate necessary existence, voluntary acts, and act/product accounts. Lines123–132 compare capacity for successive acts with inability to originate; lines136–146 distinguish an external thing's efficiently affecting God from things consequent on his own will and acts. The electronic wording at110 is not silently emended or presented as print-certified. These passages support the specific category distinctions, not the complete metaphysical adequacy of the new model.
42: 
43: ## Checked formal control and limits
44: 
45: OriginationTypeControl.lean imports only Init. E marks actual existence within a constant potential-label domain. Its object constructors are ground, indexed G-act, created effect, and another emergent kind; the type and Power are predicates, not extra individuals. Inheres ties the G-act to ground. The ground's existence and power are explicit interpretation inputs, never inferred from persistence of possibility.
46: 
47: The 152-line control checks:
48: 
49: - ◇EmptyG and □◇FreshG, plus a separately stated stronger ◇EmptyEmergent. An additional example makes G-empty true while another kind is present, so the two scopes are not equated.
50: - FreshG includes E(v,actₙ) and absence of that very identity at every earlier-indexed world. It is not recurrence of one old token. PossibleCreated likewise includes E(v,x) ∧ Created(x), avoiding existence by fixed predicate alone.
51: - Exactly one object is all-world necessary; no act, product, genus, or modal proposition is counted as another necessary object.
52: - Every emergent token occurring on the stipulated actual trajectory permanently ceases after its indexed occurrence. At actual time2 the whole emergent extension is simultaneously empty; at3 a distinct act exists. The formula ∀t∃x E(actual(t),x)∧Emergent(x) is explicitly refuted.
53: - A new present divine act inheres in its existing bearer, produces a present created effect, and is not Created or ExternalReceipt in this interpretation.
54: 
55: R is a chosen modal relation on indexed alternatives; actual is a separately chosen trajectory. No S5 result, possible-world metaphysical adequacy, empirical cosmology, complete source ontology, or historical total-cessation doctrine is proved. The interpretation's ExternalReceipt assignment is deliberately weak and is not a universal account of all ontological dependence. The logical type remains available even when its actual extension is empty; this is not a claim that an abstract type exists extramentally as an independent particular.
56: 
57: EXECUTION_RECEIPT.json preserves the historical author record of a fresh Lean4.19.0 trust0 run, exit0, seven selected axiom readbacks (at most propext and Quot.sound), no sorryAx/admissions, and two deliberately false strengthenings substantively rejected. The direct-dependency listing prints Init twice (implicit and explicit); there is one distinct direct imported module. first-check.log preserves initial local proof-development failures; final-check.log is the successful run. That recorded run replayed no inherited proof package and installed no broad dependencies. Preparing this source projection performs no scientific replay.
58: 
59: ## Disposition
60: 
61: The correction is adopted as an explicit application and terminology boundary. The inspected conditional theorems remain intact. The current assessment of at least one necessary being and defeasible common provision of the actual connected created order does not need revision on these findings. The stronger “frozen state” conclusion and historical total-cessation attribution remain unestablished by this audit.

## independent_review

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/ontology-type-control/review/REVIEW.md
Range: 19–58

19: ## Model and interpretation checks
20: 
21: 1. **Capacity, kind, act, effect remain distinct.** Lines11–38 use ground, gAct, effect and other labels. GAct and Power are predicates, not additional Obj constructors. DivineAct and Inheres tie an act to ground. The effect and act have distinct constructors and different Created classifications. This implements the requested distinction without making the activity kind or capacity a second independent necessary object.
22: 
23: 2. **Three seams must remain explicit.** ExternalReceipt is assigned exactly the Created extension at line36 in this particular interpretation; the review does not endorse that as a general identification. Emergent at line25 is a classification of labels, not a definition of temporal becoming; lines103–105 supply actual before/after novelty for the concrete witness. Power at line38 marks the existing ground and is not a causal or explanatory account of R. Ground, Power and the modal frame are stipulated inputs. Persistent possibility neither entails nor independently proves its ground here.
24: 
25: 3. **Every fresh witness has its represented owner.** FreshG supplies an actually existent gAct label. ReviewerProbes.fresh_act_has_explicit_owner checks, for every such witness, DivineAct, Inheres, Power of its existing ground, and noncreatedness. No author-source change is needed for this definitional consequence. It does not prove that power causes accessibility or independently establish voluntary agency.
26: 
27: 4. **Constant-domain existence is guarded.** Obj is a potential-label domain. EmptyG, EmptyEmergent, FreshG and PossibleCreated explicitly use E. A classified but absent effect does not populate an empty world. DivineAct, Inheres and Produces are themselves label-level relations; statements about their actual instantiation must retain E, as the displayed witness does.
28: 
29: 5. **G absence is not global absence.** Theorem empty_and_renewable states the G-empty possibility and all-emergent-empty possibility separately. scoped_absence_is_not_global gives an existent other-kind witness at a G-empty world. The stronger all-empty case is an intentional extra control, not a translation of the weaker G-scoped statement.
30: 
31: 6. **Freshness is genuine identity novelty within this frame.** FreshG requires an act with a greater identity index, existent at the accessible world, absent at every world whose serial is at most the starting index. It does not recycle an earlier token. fresh_possible constructs the successor witness for every world. The reviewer separately checked seriality, so the Box statement is not true merely because there are no accessible worlds.
32: 
33: 7. **Modal branches and the actual trajectory are different inputs.** R is strict increase of serial; actual is the selected odd/even trajectory. The reviewer checks that the same frame also admits an all-quiet selected trajectory while fresh modal alternatives remain available. Thus modal renewability does not force actual exercise. This is not an S5 frame, a past-eternal chronology, or an independently validated account of metaphysical possibility.
34: 
35: 8. **Cessation and actual gaps are real but bounded.** each_token_ceases proves permanent later absence for every emergent token that occurs on the selected actual trajectory. G-act and effect witnesses make this nonvacuous. The auxiliary other kind is always absent on that actual trajectory, so its actual cessation clause is vacuous; it is nevertheless inhabited in another represented world. actual_gap_and_new_act checks simultaneous emptiness at time2, a distinct act at time3, and failure of universal actual population. No theorem asserts that every time has a token.
36: 
37: 9. **Exactly one necessary object is model-local.** Necessary quantifies all represented worlds. Ground is stipulated to exist in each; the other constructors fail existence in quiet worlds. This proves uniqueness within the closed Obj signature, not numerical uniqueness of all actual necessary reality. Neither logical predicates nor modal propositions are counted as Obj individuals.
38: 
39: 10. **No universal dependence denial or frozen-state inference.** The actual witness separates novelty, created effect, noncreated act, and external receipt in the chosen assignment. Inherence is compatible with intrinsic or constitutive dependence on its owner. The result does not show that acts are independent grounds or exempt from every sense of dependence. Nor does the disputed implication by itself establish a necessarily frozen divine state. The audit correctly leaves those stronger conclusions unestablished.
40: 
41: ## Bearer-level application boundary
42: 
43: OriginalBearerBridge.lean16–25 distinguishes B bearers, R resources and T targets. SupportTransport41–43 goes from whole-bearer receipt to receipt of an intrinsic resource; it does not infer whole receipt from the resource's temporal novelty. ContingencyNeed50–52 is an explicit premise about an actually existent B individual that is not all-world necessary. ReceiptRepresentation46–47 and ConstitutiveReception55–57 are separate premises. SourceIdentityDerived.lean25 defines modal necessity as existence at every world, not temporal immutability. Its43–61 proofs are valid conditionals, and the composed witness proof preserves the same bearer.
44: 
45: The audit's other exact definition spans were read without execution. They preserve production/receipt distinctions, explicit ground-extension inputs, actual-field qualification, and separate bearer/event/exercise sorts. The finite joint model's two necessary bearers are not a genus and its instantiation. The new control is not claimed to satisfy that older joint model or an unrestricted receipt principle on all its own Obj labels. Substituting every intrinsic act for a B whole bearer would be an additional application claim, not a deduction from the older theorem.
46: 
47: ## Source correspondence
48: 
49: The reviewer independently read the exact electronic spans in SOURCE_BINDINGS.json and displayed all ten retained Asbahani page images. These are fresh bounded reviewer inspections of the same retained sources, not additional independent historical witnesses or new complete-volume studies.
50: 
51: - Safadiyya S001-L0070–0085 separates unrestricted activity, particular effects and succession; L0266–0276 explicitly separates divine act subsisting in its agent from the separate created product. S002-L0519–0534 retains the argumentative and reported alternatives. In particular, L0529–0530 supports the uncreated intrinsic-act/created-product distinction across the compared accounts. It does not certify total cessation of all emergent kinds.
52: - Asbahani printed65–68 and96–99 distinguish concomitance/qualification from external efficient need. Printed103–104 distinguishes a particular's necessity from an abstract common description. The text therefore supports the category controls; it does not prove the empty-kind model or introduce a second extramental individual merely by abstraction.
53: - Dar014 lines102–124 distinguishes essential qualifications/type and successive particulars, including one individual ceasing as another succeeds it. That succession is not simultaneous absence of every emergent kind.
54: - Dar017 lines100–148 supports distinctions involving voluntary acts, necessary existence, act/product accounts and external influence. Its status is a NEW bounded first reading of already acquired volume10 material, outside the completed volume8–9 reading. No whole-volume coverage, acquired-equals-read inference, new print certification or silent repair of the electronic wording at110 is credited.
55: 
56: The source passages warrant these category and attribution boundaries. They do not warrant the modal frame, selected all-empty state, selected actual trajectory, full ontology or actual numerical uniqueness. The audit's express limits preserve that separation.
57: 
58: The separate contextual receipt ACT_PRODUCT_CONTEXT.json was additionally integrity-checked: its aggregate source hash matches acquisition/lines.json, and all 13 paragraph content hashes match both that file and the retained body. It can be bound separately outside the author's seal. This adds no historical witness or scan credit and does not retroactively place it inside the author manifest.

## report

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/reports/REPORT_v2.md
Range: 81–93

81: ## Successive acts and created effects
82: 
83: A late type audit addresses the distinction between essential capacity, the genus of voluntary activity, a particular voluntary act and its created effect. Temporal novelty alone entails neither creaturehood nor external reception. A new exercise need not mean that its bearer acquired a missing essential perfection from outside. The source language is therefore rendered as successive particular voluntary acts, rather than indiscriminately as newly acquired qualities.
84: 
85: No invalid inference of that kind was found in the inspected conditional proofs. Their bearer-level contingency-as-need premise concerns modal non-necessity in respect of whole existence. Applying it to every temporally novel intrinsic act would add a substantive domain and receipt assumption. The existing source/occurrence/exercise sorts and the distinction between receiving a state and receiving whole existence must survive any application. The original-ground extension deliberately adds a reified object; it must not be used to turn a persistent type or possibility into another necessary individual.
86: 
87: A new Init-only representation control supplies an explicit existence predicate, indexed fresh act identities, a separate created-effect category and one stipulated necessary ground. It admits an empty extension of a stated act kind together with continued possible fresh activity. A separate stronger all-emergent-empty example and a counterexample to identifying these scopes are both present. On its stipulated actual trajectory, earlier tokens cease and a later distinct act occurs; no always-present-token formula is assumed. The model has one all-world necessary object, while its genus and capacity are predicates rather than extra object constructors.
88: 
89: The small source was freshly checked under official Lean 4.19.0 with trust zero; seven selected author readbacks and two deliberate rejected overclaims are recorded. Independent review adds its own fresh checks and probes at the recorded scope. These are new bounded controls, not a replay of the earlier proof packages. The modal relation and actual trajectory are chosen separately. Ground existence and the standing-power marker are explicit interpretation inputs; the latter does not independently explain or causally establish accessibility. ExternalReceipt is assigned a particular extension in this model, not identified universally with createdness. No full theory of voluntary agency, metaphysical possibility certificate or additional actual Necessary Being follows.
90: 
91: The contextual return to Safadiyya explicitly supports the distinction between intrinsic divine acts and created products, including the compared account of successive individual acts with an enduring type. The Darʾ passage on one individual replacing another does not establish simultaneous cessation of every emergent kind. The stronger absence control therefore remains a logical representation test, not an automatically attributed historical doctrine. Its new source checks, including a bounded first reading of previously acquired Darʾ volume10 material, are recorded outside the earlier reading index and retrospective zero-credit methodology ledger. The fourfold distinction also does not, by itself, prove that alternative premises force an eternally frozen agent; that conclusion requires further argument.
92: 
93: Evidence: [bounded type audit]\(../ontology-type-control/AUDIT.md), [exact model]\(../ontology-type-control/OriginationTypeControl.lean), [definition bindings]\(../ontology-type-control/DEFINITION_BINDINGS.json) and [dated source checks]\(../ontology-type-control/SOURCE_BINDINGS.json). The original mathematical companion remains unchanged; these late controls form a separately identified supplement.

## guide

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/reading/GUIDE_v2.md
Range: 23–29

23: ## Later act and effect distinction
24: 
25: The owner’s subsequent terminology control prompted a separately dated [ontology-type audit]\(../ontology-type-control/AUDIT.md). It distinguishes an emergent particular from a created particular, successive intrinsic divine acts from their created effects, and essential capacity from its temporally discriminated exercises. Safadiyya S002L0519–0534, especially 529–530, supplies explicit source support for the act/product distinction across the compared accounts. The record keeps reported positions and the author’s argument separate.
26: 
27: The new [source bindings]\(../ontology-type-control/SOURCE_BINDINGS.json) identify targeted returns to Safadiyya and the previously completed Darʾ volume 8 body, ten retained Asbahani image pages, and a bounded FIRST reading of previously acquired Darʾ volume 10 section 017. Earlier acquisition of section 017 had supplied boundary information, not reading credit for this new passage. These checks are a dated delta outside the sealed eight-study reading index and the retrospective methodology audit; their credit is neither erased nor backdated.
28: 
29: The associated checked model distinguishes an empty extension of one act kind from absence of all emergent kinds, while allowing a genuinely fresh possible token. It does not reify a persistent type or capacity as another necessary being. This controls a proposed representation; it does not establish the historical doctrine of total cessation or metaphysical possibility merely by providing a model. The earlier Darʾ succession passage explicitly discusses replacement of individuals, so its stated domain must be preserved. The 14:34 appraisal remains unchanged.

## source_locus

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/targeted-final-loci/causal-action/LOCUS_AUDIT.md
Range: 67–109

67: ## Audit B Divine action and emergence
68: 
69: ### Particular act versus enduring perfection
70: 
71: Classification: reveals an equivocation; strengthens.
72: 
73: SF-S001-L0073–0094 distinguishes producing everything, producing a particular thing, and activity in general. Eternal complete production of every particular conflicts with observed novelty. A beginning of a particular effect or particular act need not be a beginning of the agent's essential perfection. This is directly controlled in Adwa99–100. At L0103/Adwa107, the completion of each successive efficacy is explicitly not supplied from another: preceding acts conditioning later products are the agent's own acts.
74: 
75: Hence these must remain separate: temporal emergence; being a creature distinct from the agent; dependence on an external giver; acquisition of a formerly missing essential perfection. No automatic implication from the first to the other three has been established.
76: 
77: ### The rejected binary
78: 
79: Classification: reveals an equivocation; answers a counter-objection.
80: 
81: SF-S002-L0577–0603, controlled at Adwa368–374, exposes the assumption that everything is either an eternally fixed particular or a separated created thing. The third category is what subsists in the divine agent through power and will. It can be described as intrinsic by subsistence and voluntary by its relation to power and will. The author separately distinguishes act from effect and creation from the created product. His reports of competing schools are not all endorsements; the positive third-category resolution is explicit.
82: 
83: ### Global inactivity has an additional causal exclusion
84: 
85: Classification: new substantive premise relative to capacity-only reconstruction; strengthens; answers the globally inactive model against the fuller doctrine.
86: 
87: The clarified continuous /11 discussion culminates at Salim2:141–144, especially 2:142, electronically lines2254–2257 and SF-S003-L0079–0083. Adwa414/PDF421 independently controls it. A hypothesis stripping the agent of all successive voluntary matters even at a time could not subsequently yield a new event, since it would lack a sufficient causal change. The text then explicitly says those successive voluntary matters are inseparable. This is an argument from adequate causation, intrinsic successive agency, and absence of an independent external enabler. It is stronger than saying power remains available.
88: 
89: Compared with the separately completed Ibn ʿUthaymin Nisāʾ33 audit, both supply more than persistent ability: that later explanation appeals explicitly to the perfection of activity; this Ibn Taymiyya locus adds the causal impossibility of restarting from the stipulated total stripping. Their evidential roles should remain distinct. This comparison adds no second-hand primary-reading credit to this assessment.
90: 
91: The quantifier is activity generally. No particular act-kind is thereby shown to be active at every time. Nor does cessation of one utterance, one effect, or one kind amount to cessation of the genus. No-first-act, no interval of total inactivity, and no ultimate exhaustion are different propositions. The selected Salim2:142 argument expressly addresses total stripping at a time; translating that into a temporal formalism still requires defining times, intervals, event boundaries and the range of voluntary activity.
92: 
93: ### The /12 incipit and the modal boundary
94: 
95: Classification: strengthens; reveals an equivocation; answers the eternal-particular-act model.
96: 
97: “ونفس حقيقة الفعل المعين يمتنع قدمه” is directly bound to Salim2:145, electronic line2272 with footer2273, and Adwa416/PDF423. The following page, Salim2:146, is independently displayed on Shamela22874/477. The two source coordinates are not interchangeable.
98: 
99: Salim2:145–149 explains that a particular act is successive and voluntary, whereas a necessary attribute may belong essentially, either as a particular such as life or as a genus such as speech and willing. An eternal fixed particular act would erase the relevant distinction between acting and an invariant attribute. The objection that the essential power and will would themselves then need to be voluntarily caused generates a regress or prior circle in the very basis of agency. The text also distinguishes efficient causation from mere accompanying motion, as in hand and key.
100: 
101: At 2:172–173 the intrinsic-power argument establishes beginningless possibility, then possibility of beginningless activity. Do not silently change that modal conclusion into actual tokens at every time. Actual continuing activity is supported elsewhere by the stronger genus, perfection and causal claims just identified. The formal G-empty versus all-emergent-empty distinction remains useful, but it is not the full source ontology: it must not erase intrinsic acts, alter event-kind quantifiers, or equate occurrence with logical Created.
102: 
103: ## Bounded conclusion
104: 
105: The cooperation challenge is answered by the fuller source-premise package to the extent a proposed model claims to preserve that package. Whether its coalescence, unlimited independence, or causal-perfection bridges are independently defensible remains a philosophical question; no bare-logic theorem or complete Lean reconstruction is claimed here.
106: 
107: The action audit now has direct textual grounds for rejecting complete global inactivity under that stronger doctrine while preserving the difference between genus, kind, token and effect. It does not licence an inference from mere possibility to actuality or a blanket accusation that all voluntary cessation loses essential perfection.
108: 
109: Reading, source identification, and the requested electronic edition-page bindings are complete. Remaining limitations are witness-level: no acquired Salim scan, no full manuscript collation, no modern-science revalidation, and no independent verification of every historical attribution or polemical report.

## source_mapping

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/targeted-final-loci/causal-action/PAGE_CORRESPONDENCE.json
Range: 1–142

1: {
2:   "created_utc": "2026-10-07T18:20:00Z",
3:   "records": [
4:     {
5:       "locus": "Darʾ9:339–362",
6:       "status": "continuous text reread complete;bounded electronic page anchors verified",
7:       "read_base": "DAR9-IB L600–794",
8:       "requested_start": "9:339 starts L631 وهـذا في كل ما يقال...",
9:       "start_evidence": "Page-labelled Islamweb indexed primary extract at https://www.islamweb.net/ar/library/content/413/1768/?idfrom=&idto=&start= ;retrieval of complete object subsequently cache-missed. This is a weaker boundary witness than the directly displayed page362.",
10:       "direct_anchors": [
11:         {
12:           "label": "9:337",
13:           "url": "https://shamela.ws/book/21506/3617",
14:           "match": "L623–626"
15:         },
16:         {
17:           "label": "9:350",
18:           "url": "https://shamela.ws/book/21506/3630",
19:           "match": "L682 tail–686 prefix"
20:         },
21:         {
22:           "label": "9:362",
23:           "url": "https://shamela.ws/book/21506/3642",
24:           "match": "L747–750 and beginningL751"
25:         }
26:       ],
27:       "limit": "No complete print-page collation. The new reading extends before339 and beyond362; cite those extensions by local line until separately page-bound."
28:     },
29:     {
30:       "locus": "Majmuʿ20:175–178",
31:       "status": "page-labelled electronic locus verified;continuous continuation read through183",
32:       "direct_anchors": [
33:         {
34:           "label": "20:175",
35:           "url": "https://shamela.ws/book/7289/9999"
36:         },
37:         {
38:           "label": "20:176",
39:           "url": "https://shamela.ws/book/7289/10000"
40:         },
41:         {
42:           "label": "20:177",
43:           "url": "https://shamela.ws/book/7289/10001"
44:         }
45:       ],
46:       "additional_page_source": "MF-ISLAMWEB webL907–928,including visible178,179,180,181,182,183 markers",
47:       "limit": "Electronic page witness only; no print scan."
48:     },
49:     {
50:       "locus": "Safadiyya1:92–93 Salim",
51:       "status": "DIRECT_ELECTRONIC_EDITION_PAGE_BINDING_VERIFIED",
52:       "source": "https://islamhouse.com/read/ar/الصفدية-272837",
53:       "metadata_line": 15,
54:       "direct_boundaries": [
55:         {
56:           "page": "1:92",
57:           "web_text_lines": [
58:             423,
59:             423
60:           ],
61:           "footer_line": 424,
62:           "local": "SF-S001-L0134–0135"
63:         },
64:         {
65:           "page": "1:93",
66:           "web_text_lines": [
67:             427,
68:             427
69:           ],
70:           "footer_line": 428,
71:           "local": "SF-S001-L0136"
72:         },
73:         {
74:           "page": "1:94",
75:           "web_text_lines": [
76:             431,
77:             431
78:           ],
79:           "footer_line": 432,
80:           "local": "SF-S001-L0137–0140"
81:         },
82:         {
83:           "page": "1:95",
84:           "web_text_lines": [
85:             435,
86:             435
87:           ],
88:           "footer_line": 436,
89:           "local": "SF-S001-L0141–0142"
90:         }
91:       ],
92:       "continuous_read": "1:90–95 target context reread directly on the page-labelled primary text",
93:       "distinct_scan_control": "Adwa122–126/PDF129–133;particularly123–125 for the central argument",
94:       "qualification": "Footers label preceding text,not following text. Electronic binding is not a Salim scan certification."
95:     },
96:     {
97:       "locus": "Wikisource/11–/12 target incipit",
98:       "target": "ونفس حقيقة الفعل المعين يمتنع قدمه",
99:       "status": "DIRECT_ELECTRONIC_EDITION_PAGE_BINDING_VERIFIED",
100:       "local": "SF-S003-L0092",
101:       "direct_Salim": {
102:         "edition": "Muhammad Rashad Salim,Maktabat Ibn Taymiyya2nd1406",
103:         "page": "2:145",
104:         "url": "https://islamhouse.com/read/ar/الصفدية-272837",
105:         "text_line": 2272,
106:         "footer_line": 2273
107:       },
108:       "direct_scan": {
109:         "edition": "SF-ADWA",
110:         "printed_page": 416,
111:         "pdf_position": 423
112:       },
113:       "direct_Salim_next_page": {
114:         "page": "2:146",
115:         "url": "https://shamela.ws/book/22874/477",
116:         "web_lines": [
117:           50,
118:           55
119:         ],
120:         "local": "SF-S003-L0094–0097"
121:       },
122:       "stronger_global_inactivity_argument": {
123:         "page": "2:142",
124:         "url": "https://islamhouse.com/read/ar/الصفدية-272837",
125:         "web_body_lines": [
126:           2254,
127:           2256
128:         ],
129:         "footer_line": 2257,
130:         "local": "SF-S003-L0079–0082",
131:         "distinct_scan": "Adwa414/PDF421"
132:       },
133:       "larger_sections": {
134:         "wiki11": "begins within Salim2:111 at IslamHouseL2071/footer2072;ends within2:145 atL2271",
135:         "wiki12": "begins within2:145 atL2272;ends within2:181 atL2474/footer2476",
136:         "method": "Both full Wikisource sections read;exact beginning,join,and ending anchors matched to page-labelled primary text. Not full diplomatic collation of each electronic word."
137:       },
138:       "qualification": "No Salim scan claim;all prior direct-citation holds cleared at electronic level only."
139:     }
140:   ],
141:   "canonical_Salim_citation_holds": []
142: }

## historical_text_receipts

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/targeted-final-loci/causal-action/TEXT_READ_RECEIPTS.json
Range: 1–144

1: {
2:   "scope_rule": "Fresh2026-10-07 targeted rereading only. Earlier zero-credit methodology core and sealed historical reading claims remain unchanged. File acquisition,search hits and mechanical counts are not continuous-reading credit.",
3:   "receipts": [
4:     {
5:       "id": "dar9",
6:       "source_path_input_name": "dar-islamicbook-016.txt",
7:       "source_path_input_delivery": "Historical input identity only; this field does not promise the input body in the public selection.",
8:       "source_sha256": "04cc1092235e0d92312ed5146f1f89c1bea866546a6c567318a77be9cf1b0963",
9:       "range": [
10:         600,
11:         794
12:       ],
13:       "range_sha256": "2f179125a8bc0f3112c543b3c49b0419b192e4655328ed739beed811e887e2d3",
14:       "receipt_input_name": "dar9-L0600-L0794.txt",
15:       "receipt_input_delivery": "Historical input identity only; this field does not promise the input body in the public selection.",
16:       "scope": "new targeted direct continuous reread; no earlier period credit",
17:       "completed_utc": "2026-10-07T17:59:02.143079+00:00"
18:     },
19:     {
20:       "id": "saf1",
21:       "source_path_input_name": "001.txt",
22:       "source_path_input_delivery": "Historical input identity only; this field does not promise the input body in the public selection.",
23:       "source_sha256": "c22b439759b0aad722662db678c9f311184a76c7a0feb43ed359684e4bf3229e",
24:       "range": [
25:         69,
26:         149
27:       ],
28:       "range_sha256": "bb93fa16fd531df843646b86821bfc38373a18a82573526d98824fc11607c7f3",
29:       "receipt_input_name": "saf1-L0069-L0149.txt",
30:       "receipt_input_delivery": "Historical input identity only; this field does not promise the input body in the public selection.",
31:       "scope": "new targeted direct continuous reread; no earlier period credit",
32:       "completed_utc": "2026-10-07T17:59:02.145594+00:00"
33:     },
34:     {
35:       "id": "saf2",
36:       "source_path_input_name": "002.txt",
37:       "source_path_input_delivery": "Historical input identity only; this field does not promise the input body in the public selection.",
38:       "source_sha256": "5d3c623f5daebc8910fb8683d5ea1df8c6780942e9e976ec7da840aa1bf08bbe",
39:       "range": [
40:         574,
41:         636
42:       ],
43:       "range_sha256": "35facb0cd2bb02968252f567dbf9c4e361dff7959d08209ab4470b812e3b95e6",
44:       "receipt_input_name": "saf2-L0574-L0636.txt",
45:       "receipt_input_delivery": "Historical input identity only; this field does not promise the input body in the public selection.",
46:       "scope": "new targeted direct continuous reread; no earlier period credit",
47:       "completed_utc": "2026-10-07T17:59:02.147571+00:00"
48:     },
49:     {
50:       "id": "MF",
51:       "source": "MF-SHAMELA and MF-ISLAMWEB",
52:       "read_scope": "20:175–183 complete electronic continuous primary body,plus preceding opening paragraph at webL906;not all20:174",
53:       "source_url": "https://islamweb.net/ar/library/content/22/2032/فصل-العلتين-لا-تكونان-مستقلتين-بحكم-واحد-حال-الاجتماع",
54:       "web_line_range": [
55:         906,
56:         928
57:       ],
58:       "private_read_object_sha256": "8b767ddf0ca083c9469b01987f3c020eb08a1627e8fef0e3369f677572ec69a3",
59:       "read_at_utc": "2026-10-07T18:11:00Z",
60:       "credit": "new targeted reading only"
61:     },
62:     {
63:       "id": "SF-WIKI-11",
64:       "source": "SF-WIKI",
65:       "source_url": "https://ar.wikisource.org/wiki/الصفدية/11",
66:       "web_body_lines": [
67:         93,
68:         243
69:       ],
70:       "continuity": "All displayed body lines read in overlapping bounded windows;initial tool output ended early,so later ranges explicitly reopened;no missing body line",
71:       "private_read_object_sha256": "786e73b6cc9c92bf81faa0cbaf158acf2db8980db144bd4728c7925c2c73fd1c",
72:       "local_alignment": "SF-S002-L0695–0740 plusSF-S003-L0001–0091",
73:       "read_at_utc": "2026-10-07T18:11:00Z",
74:       "credit": "new contextual reread of previously studied work,no new historical witness"
75:     },
76:     {
77:       "id": "SF-WIKI-12",
78:       "source": "SF-WIKI",
79:       "source_url": "https://ar.wikisource.org/wiki/الصفدية/12",
80:       "web_body_lines": [
81:         93,
82:         277
83:       ],
84:       "continuity": "All displayed body lines read in overlapping bounded windows;initial tool output ended early,so later ranges explicitly reopened;no missing body line",
85:       "private_read_object_sha256": "043265a40cc7ce9b328fc4517d808802a9eb907432b06b348ea056e946d92386",
86:       "local_alignment": "SF-S003-L0092–0246",
87:       "read_at_utc": "2026-10-07T18:11:00Z",
88:       "credit": "new contextual reread of previously studied work,no new historical witness"
89:     },
90:     {
91:       "id": "SF-SALIM-FINAL-BINDING",
92:       "source_url": "https://islamhouse.com/read/ar/الصفدية-272837",
93:       "metadata_line": 15,
94:       "body_read_spans": [
95:         {
96:           "web_lines": [
97:             415,
98:             436
99:           ],
100:           "pages": "1:90–95"
101:         },
102:         {
103:           "web_lines": [
104:             2237,
105:             2301
106:           ],
107:           "pages": "2:139–150"
108:         },
109:         {
110:           "web_lines": [
111:             2400,
112:             2429
113:           ],
114:           "pages": "2:168–173"
115:         }
116:       ],
117:       "boundary_only_spans": [
118:         {
119:           "web_lines": [
120:             2071,
121:             2078
122:           ],
123:           "pages": "2:111–112"
124:         },
125:         {
126:           "web_lines": [
127:             2467,
128:             2481
129:           ],
130:           "pages": "2:180–181"
131:         }
132:       ],
133:       "read_at_utc": "2026-10-07T18:20:00Z",
134:       "qualification": "The stated body ranges were each displayed/read in full. Boundary probes add no whole-section second-edition reading credit. Page numbers are footers.",
135:       "private_source_response_sha256s": {
136:         "salim_meta.txt": "f8dc0cfa9509746112397791c725ec1fb62d5bcc6b8400a00cc0d4f6d86ef323",
137:         "salim92.txt": "4181ca727ffa8b7f4f631cf4246c08f150027bdb1c2f30eaeec1777ef11f28ff",
138:         "salim145.txt": "c678899c85be765b21567f8a22f648a5f69b9913e1e7d7dbd42d3740239f45c5",
139:         "salim_wiki_bounds.txt": "1ca7f657f3d307ca60fa4a120557a02c100356c4687b36b857e08364191f691d",
140:         "salim147_170.txt": "6ebe3e8cef4fa60487886f173455ced72ca0871d21c7e6b1c2945b8a6aca5bd2"
141:       }
142:     }
143:   ]
144: }

## uthaymin_locus

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/targeted-final-loci/uthaymin/LOCUS_AUDIT.md
Range: 11–108

11: ### U1. Nisāʾ 6, Q4:15: genus, kind, individual act
12: 
13: [Official source](https://old.binothaimeen.net/content/13876). Read continuous lines 322–341, with the preceding Q4:15–16 exposition also consulted. Core: 336–340. Section starts 00:35:06; next section 01:21:06.
14: 
15: Anchor: “جنس، ونوع، وفرد”.
16: 
17: From the verse’s divine making he moves to voluntary renewed action: genus is eternal, particular kinds can originate (enthronement after the throne), and individual occurrences recur. He expressly endorses past/future succession and denies that originated acts entail an originated subject.
18: 
19: Classification: **strengthening; exposes hidden equivocation; answers the blanket new-act→originated-agent objection**. This is not merely a capacity quotation. It does not independently establish uniqueness of an original source (audit A), nor prove that every kind is eternally instantiated. Audit B must distinguish an act’s beginning from its subject’s beginning. “Emergent→Created” cannot simply be imposed as the meaning of his terminology.
20: 
21: ### U2. Nisāʾ 26, Q4:87: speech and the created/originated distinction
22: 
23: [Official source](https://old.binothaimeen.net/content/13896). Read lines 307–399 continuously across overlapping retrievals, including the full speech objection/reply and subsequent Q&A. Core: 341–364, 392–399. Section 00:48:14–01:11:32.
24: 
25: Anchor: “الحادث قد يكون صفة وقد يكون مخلوقًا بائنًا”.
26: 
27: The underlying attribute of speech is essential; individual utterances occur successively. Scriptural reports following events supply examples. The objection that such occurrence makes God originated is expressly rejected. The Q&A distinguishes an occurring attribute from a separately created thing and an attribute from its bearer.
28: 
29: Classification: **strengthening; answers a counter-objection; exposes hidden equivocation**. This directly defeats using his word “originated” as synonymous with “created entity.” It supplies no derivation from a new utterance to externally received perfection. That proposed bridge remains substantive and unproved here. For audit A it is a vocabulary constraint, not an additional unity proof.
30: 
31: ### U3. Nisāʾ 33, Q4:114: the general-inactivity exclusion
32: 
33: [Official source](https://old.binothaimeen.net/content/13904). Read the continuous renewed Q4:114 discussion, lines 380–427; core 405–413. Section 00:53:48–01:24:28.
34: 
35: Anchor: “لأن الفعل كمال”.
36: 
37: He calls the genus essential while kinds/tokens arise voluntarily. He explicitly rejects an interval in which God was not acting, on a perfection premise, then challenges any first date when action supposedly became possible. He distinguishes divine pleasure from a separate reward-effect.
38: 
39: Classification: **new substantive premise relative to a capacity-only reconstruction; strengthening; answers the global-empty-extension countermodel against the fuller doctrine**. The quantifier concerns voluntary activity generally, not every kind. Ability alone does not entail exercise: his possibility challenge cannot replace the additional perfection premise. Consequently a globally empty extension preserves capacity but violates this fuller premise and is **not a countermodel to his stated doctrine**. Kind-specific nonperformance remains distinct. Audit A receives no independent uniqueness derivation.
40: 
41: ### U4. Shūrā 6: always active, will-governed, act distinct from effect
42: 
43: [Official source](https://old.binothaimeen.net/content/14192). Read continuous lines 228–247; core 234–236, a complete digression between exposition of Q42:17 and Q42:18. The encompassing section starts 00:00:03; Q42:18 starts 00:57:35.
44: 
45: Anchor: “لكن فعله تابع لمشيئته”.
46: 
47: He rejects initial inactivity and final exhaustion, endorses succession in both directions, and retains voluntary particular action. For unspecified pre-cosmic acts he argues from ability to possibility; he denies that succession makes individual creatures coeternal, distinguishing willing agent, act, and effect.
48: 
49: Classification: **strengthening and restatement of the genus/token distinction; answers the coeternal-effect objection**. Permission to act is weaker than proof of each token’s actuality; his broader always-active affirmation must be retained separately. Neither unrestricted global cessation nor the eternal actuality of every act-kind follows from the voluntary clause. Audit A is unaffected as a uniqueness proof. This is later explanatory control, including his defense of Ibn Taymiyya, not independent historical evidence for the latter’s wording.
50: 
51: ### U5. Ghāfir 2, Q40:6: succession belongs to speech itself
52: 
53: [Official source](https://old.binothaimeen.net/content/14157). Supplementary speech locus, not a substitute for the requested Nisāʾ/Shūrā works. Read the entire Q40:6 unit, lines 273–293. Core 283–287. Section 01:03:02–01:11:15.
54: 
55: Anchor: “الكلام يحدث نفس الكلام”.
56: 
57: The ordered letters provide a successive-utterance argument, while the underlying attribute remains eternal. He contrasts this with hearing: its heard object originates, whereas for speech he says the speech itself occurs. He then answers an objection about resemblance to created speech.
58: 
59: Classification: **strengthening; additional argument; exposes an act/object equivocation**. Audit B cannot reduce every divine-action occurrence to a new external object while leaving all intrinsic action unchanged. Conversely, the passage does not infer externally acquired perfection. It offers no additional exclusion of cooperative original sources for audit A.
60: 
61: ### U6. Māʾida 24, Q5:73: explanation of Q21:22 and Q23:91
62: 
63: [Official source](https://old.binothaimeen.net/content/13941). Read continuous lines 408–434, the complete unity argument; core 426–433. Section begins 01:19:01; exact argument timestamp unverified.
64: 
65: Anchor: “وكل إله يريد أن تكون الألوهية له”.
66: 
67: After Q21:22, he explains Q23:91 through separated creations, each deity’s exclusive claim, conflict, and domination. A travel party with two commanders illustrates disorder.
68: 
69: Classification: **restatement/strengthening; makes an extra conflict premise explicit; does not answer the cooperation countermodel in this bounded argument**. Intrinsically concordant co-producers are not separately tested. The step from plurality to conflict therefore cannot be recorded as a theorem from numerical plurality alone. This is a later control on exposition, not an independent historical witness for Ibn Taymiyya. No new action-ontology premise is established.
70: 
71: ## Separate audit conclusions
72: 
73: ### A. Plural original sources / cooperation
74: 
75: U6 warrants attributing an exclusive-rule/conflict argument to this later explanation. Its explanatory vividness is not, by itself, elimination of all cooperative countermodels. A modal proof needs to justify why two original agents could not possess intrinsic concordance, why a joint act implies ontological dependence, or why one sufficient source excludes another rather than merely making it explanatorily redundant. These are alternative substantive routes; this reading does not collapse them.
76: 
77: The action passages constrain permissible reconstructions but do not supply the missing cooperation proof. In particular, multiplying voluntary actors cannot be dismissed merely by relabeling their new acts as separately created entities or externally bestowed perfections.
78: 
79: ### B. Divine-action ontology
80: 
81: Keep the following variables separate:
82: 
83: 1. Essential capacity: an enduring ability to act.
84: 2. Genus: divine activity considered generally.
85: 3. Kind: e.g. a particular specified form of action.
86: 4. Token: a numerically particular voluntary occurrence.
87: 5. Effect: what an act produces, possibly existing separately.
88: 
89: Logical controls:
90: 
91: - Persistent ability alone does not imply an actual token at every time.
92: - A general always-active premise is stronger than persistent ability.
93: - An existential assertion of some activity at every relevant time is not a universal assertion that every kind occurs at every time.
94: - An empty extension for one kind is not an empty extension for activity as a whole.
95: - An act’s temporal novelty, the novelty of its bearer, the creation of a separate effect, and the acquisition of perfection from another are different predicates.
96: - Any bridge between those predicates needs a premise, not a terminological stipulation.
97: 
98: **Earlier formal control:** the global empty-extension test applies only to the reduced, capacity-only axiom set. U3 requires the fuller premise to be retained. The earlier withholding of a historical total-cessation attribution needs no forced revision.
99: 
100: No conclusion here claims every act-kind is always actual, a particular creature is eternal, every renewed act is a separately created thing, or a new act imports perfection from outside. No artificial resolution of tensions beyond the verified loci is offered.
101: 
102: ## Verification limits and stopping boundary
103: 
104: - The connected Tafsīr plugin’s 28-source registry was checked; it did not list Ibn ʿUthaymīn. It therefore supplies no receipt for these readings.
105: - Direct Q23:91 and Q21:22 URLs on tafsir.app were inaccessible through the retrieval tool. This is not evidence that the author never commented on those verses.
106: - A shell request to tafsir.app returned HTTP 403; no bypass was attempted.
107: - Relevant exact passages were subsequently acquired from the official author website. Search snippets served only discovery.
108: - No sealed package or repository source was edited. This report does not exercise closure authority over either audit.

## uthaymin_receipts

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/targeted-final-loci/uthaymin/READING_RECEIPTS.json
Range: 1–164

1: {
2:   "schema": "targeted-context-reading-receipts/1",
3:   "author": "محمد بن صالح العثيمين",
4:   "reading_date_utc": "2026-10-07",
5:   "session_start_utc": "2026-10-07T17:47:14Z",
6:   "reading_status": "new_targeted_reading",
7:   "prior_exact_receipt": null,
8:   "medium": "official_site_arabic_lecture_transcription",
9:   "publisher_site": "الموقع الرسمي لفضيلة الشيخ محمد بن صالح بن عثيمين",
10:   "edition": "Official old.binothaimeen.net web transcription; print edition not established",
11:   "print_edition_verified": false,
12:   "print_pages": null,
13:   "audio_listened": false,
14:   "timing_precision": "Website section boundaries only; not exact spoken-locus timestamps",
15:   "line_number_scope": "Rendered web-tool snapshot; line numbers can change with site layout",
16:   "receipts": [
17:     {
18:       "id": "U1",
19:       "work": "تفسير سورة النساء - 6",
20:       "verse": "4:15",
21:       "url": "https://old.binothaimeen.net/content/13876",
22:       "read_lines": [
23:         322,
24:         341
25:       ],
26:       "core_lines": [
27:         336,
28:         340
29:       ],
30:       "section_start": "00:35:06",
31:       "next_section_start": "01:21:06",
32:       "reading_status": "new_targeted_reading",
33:       "complete_relevant_argument_read": true,
34:       "print_page": null,
35:       "exact_spoken_locus_timestamp": null
36:     },
37:     {
38:       "id": "U2",
39:       "work": "تفسير سورة النساء - 26",
40:       "verse": "4:87",
41:       "url": "https://old.binothaimeen.net/content/13896",
42:       "read_lines": [
43:         307,
44:         399
45:       ],
46:       "core_lines": [
47:         [
48:           341,
49:           364
50:         ],
51:         [
52:           392,
53:           399
54:         ]
55:       ],
56:       "section_start": "00:48:14",
57:       "next_section_start": "01:11:32",
58:       "reading_status": "new_targeted_reading",
59:       "complete_relevant_argument_read": true,
60:       "print_page": null,
61:       "exact_spoken_locus_timestamp": null
62:     },
63:     {
64:       "id": "U3",
65:       "work": "تفسير سورة النساء - 33",
66:       "verse": "4:114",
67:       "url": "https://old.binothaimeen.net/content/13904",
68:       "read_lines": [
69:         380,
70:         427
71:       ],
72:       "core_lines": [
73:         405,
74:         413
75:       ],
76:       "section_start": "00:53:48",
77:       "next_section_start": "01:24:28",
78:       "reading_status": "new_targeted_reading",
79:       "complete_relevant_argument_read": true,
80:       "print_page": null,
81:       "exact_spoken_locus_timestamp": null
82:     },
83:     {
84:       "id": "U4",
85:       "work": "تفسير سورة الشورى - 6",
86:       "verse": "digression between 42:17 and 42:18",
87:       "url": "https://old.binothaimeen.net/content/14192",
88:       "read_lines": [
89:         228,
90:         247
91:       ],
92:       "core_lines": [
93:         234,
94:         236
95:       ],
96:       "section_start": "00:00:03",
97:       "next_section_start": "00:57:35",
98:       "reading_status": "new_targeted_reading",
99:       "complete_relevant_argument_read": true,
100:       "print_page": null,
101:       "exact_spoken_locus_timestamp": null
102:     },
103:     {
104:       "id": "U5",
105:       "work": "تفسير سورة غافر - 2",
106:       "verse": "40:6",
107:       "url": "https://old.binothaimeen.net/content/14157",
108:       "read_lines": [
109:         273,
110:         293
111:       ],
112:       "core_lines": [
113:         283,
114:         287
115:       ],
116:       "section_start": "01:03:02",
117:       "next_section_start": "01:11:15",
118:       "reading_status": "new_targeted_reading",
119:       "complete_relevant_argument_read": true,
120:       "print_page": null,
121:       "exact_spoken_locus_timestamp": null
122:     },
123:     {
124:       "id": "U6",
125:       "work": "تفسير سورة المائدة - 24",
126:       "verse": "5:73 explaining 21:22 and 23:91",
127:       "url": "https://old.binothaimeen.net/content/13941",
128:       "read_lines": [
129:         408,
130:         434
131:       ],
132:       "core_lines": [
133:         426,
134:         433
135:       ],
136:       "section_start": "01:19:01",
137:       "next_section_start": null,
138:       "reading_status": "new_targeted_reading",
139:       "complete_relevant_argument_read": true,
140:       "print_page": null,
141:       "exact_spoken_locus_timestamp": null
142:     }
143:   ],
144:   "failed_or_unavailable_routes": [
145:     {
146:       "source": "https://tafsir.app/ibn-uthaymeen/23/91",
147:       "result": "inaccessible via web tool",
148:       "inference_limit": "No negative existence claim"
149:     },
150:     {
151:       "source": "https://tafsir.app/ibn-uthaymeen/21/22",
152:       "result": "inaccessible via web tool",
153:       "inference_limit": "No negative existence claim"
154:     },
155:     {
156:       "source": "https://tafsir.app/ibn-uthaymeen/42/1",
157:       "result": "shell request HTTP 403; no bypass attempted"
158:     },
159:     {
160:       "source": "connected Tafsir plugin source registry",
161:       "result": "28 sources listed; Ibn Uthaymin absent"
162:     }
163:   ]
164: }

## final_context

Source: recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/final-context-audit/CONTEXT_SCOPE.md
Range: 25–45

25: For **T20-EMERGENCE-TYPE-CONTROL**, the new support is limited to application scope:
26: 
27: - The Ibn ʿUthaymīn audit and its [dated official-transcription receipts]\(../targeted-final-loci/uthaymin/READING_RECEIPTS.json), especially Nisāʾ lesson 33 at Q4:114 and Shūrā lesson 6.
28: - The causal-action audit, [text-read receipts]\(../targeted-final-loci/causal-action/TEXT_READ_RECEIPTS.json), [image-read receipts]\(../targeted-final-loci/causal-action/IMAGE_READ_RECEIPTS.json), and [edition/page correspondence]\(../targeted-final-loci/causal-action/PAGE_CORRESPONDENCE.json).
29: - The dated philosophical reassessment and premise edges, only where they distinguish essential capacity, general activity, particular kind, particular act-token, and created effect.
30: 
31: The formal conclusion and its original scientific anchors retain their checked interpretation. A global empty extension separates persistent capacity from actual activity under the reduced assumptions. It does not preserve the stronger always-active or anti-inactivity premises supported at the audited source scope. General activity is not eternal instantiation of every kind; a token's ending or one kind's absence is not total inactivity. A renewed intrinsic act is not, by definition, a created bearer or externally received perfection.
32: 
33: The exact general-inactivity controls are Ibn ʿUthaymīn's Nisāʾ lesson 33, Q4:114, official-transcription core lines 405–413, and Ibn Taymiyyah's al-Ṣafadiyya at Rashād Sālim 2:142, electronic lines 2254–2257. The latter is separately controlled by the Āḍwāʾ edition's printed page 414/PDF position 421. The later explanation appeals to perfection; the earlier causal argument excludes total stripping of successive voluntary matters followed by an unexplained restart. These are separate source arguments. The Sālim coordinate is an electronic edition-page binding, not a claim to have inspected a Sālim print scan.
34: 
35: ## Distinct evidential roles
36: 
37: 1. Passage and witness verification identifies actual read intervals, editions, apparatus, web transcription limits and page correspondences. Overlapping readers do not add another historical witness.
38: 2. Strongest argument reconstruction states the author's inferential branches and intended quantifiers, including the defended metaphysical bridges.
39: 3. Model-premise comparison inspects existing definitions and receipts without another Lean run. Its negative full-countermodel verdict is narrower than a general impossibility theorem.
40: 4. Philosophical warrant review evaluates the inferential burden and records qualified assent or withholding. It does not convert historical attribution into truth.
41: 5. Receiving integration must separately bind selected identities to the two existing owners. This source selection itself changes no result, status, suite, receipt, theorem or repository record.
42: 
43: ## Reading credit and delivery limits
44: 
45: The new reading is dated 7 October 2026. Receipts distinguish first reading, contextual return, text display, scan inspection and author-attributed review. Neither acquisition alone nor curation is credited as reading. No whole-volume reading, fresh manuscript collation, exact audio timestamp, public permission for a privately supplied PDF, additional scientific result, native science execution or Lean proof replay is implied.

## checkpoint_cooperation

Source: recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-resumption/cooperation/RESULT.md
Range: 23–29

23: The key primary passage is the retained Arabic Majmu 20:174–183, especially web L908, L912–913 and L917–921. L908 argues that a genuinely additional contributor changes the complete effect if the first contributor remains unchanged; ordinary solo/joint examples involve a changed productive state. L912–913 explicitly strengthens complete power and decisive willing into production through the agent alone. L917–921 gives the concentration/de re/perfection/dependence sequence, rather than merely saying that cooperation is bad.
24: 
25: Minhaj 2:180–183 supplies efficacy-as-perfection and the intrinsically necessary perfection argument. Its preceding 2:168–172 control distinguishes intrinsic concomitance from efficient origination. The experiment does not treat every matching state as a causal cycle, nor does it assume the disputed effect-to-intrinsic transfer.
26: 
27: The Safadiyya control distinguishes essential capacity, genus, act token and external product. The particular-act anchor remains Salim 2:145, and the additional global-inactivity argument remains 2:142. Neither is reinterpreted or weakened here. The present algebra has no temporal-global-activity model and claims no result about total divine cessation.
28: 
29: Exact files, hashes, ranges, page qualifications and premise bindings are in `SOURCE_BINDINGS.json` and `PREMISE_MATRIX.json`. Retained electronic Arabic was directly read; there was no new browsing, manuscript collation, scan campaign or whole-book reading.

## checkpoint_design

Source: recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-resumption/cooperation/DESIGN.md
Range: 1–13

1: # Fixed-target cooperation interpretation campaign
2: 
3: Started 2026-10-07 20:08:05 UTC. New research only in this directory; the delivered checkpoint and earlier formal/source files remain read-only.
4: 
5: ## Question and stopping rule
6: 
7: Attempt a materially stronger two-agent interpretation of the late B5/B6 cooperation arguments. Stop at a faithful preserving interpretation at explicitly stated scope, a conditional bridge whose extra antecedents are exposed, or a precise obstruction within the tried encoding family. A finite failure is never a proof that every future interpretation fails.
8: 
9: ## Frozen source constraints
10: 
11: The exact owner's computational objective and the late source argument, premise map, model audit, root reassessment and independent warrant review have been read. T17 P65–68, P74–81 and P108–112 govern eligible pure power and wise willing. Two rigid agents must keep their actual existence, essential nonreceipt, intrinsic capacity and willing. Capacity, intrinsic reason, will, act token, emitted productive contribution, external effect and entire original provenance are different types. Safadiyya's particular-act anchor remains Salim 2:145; the stronger total-inactivity argument remains 2:142. This experiment does not use global inactivity or alter those findings.
12: 
13: P2b, M1's effect-to-intrinsic transfer, B5's de re/perfection/receipt conclusion, B6's whole/exclusive-provision transition and B2's efficient-concurrence interpretation are targets, never silently included in their own antecedents.

## checkpoint_provision

Source: recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/provision-identity/RESULT.md
Range: 52–61

52: The source nonetheless asserts a much stronger total case: original powers are intrinsically possessed; efficient receipt cannot circle; their perfect efficacy cannot come from a peer; full determination should be wholly productive; independent domains cannot account for the connected actual creation. The direct relation does not certify all those claims by drawing an acyclic graph.
53: 
54: ### 1.5 Perfection and action controls remain in force
55: 
56: Minhaj 2:180–183 calls realized efficacy a perfection and argues that what is necessary by itself cannot acquire its intrinsic perfection externally. Majmu L916–921 connects inability to act independently to fuller possible power, then to self-completion and dependence. The exact disputed application remains whether differentiated joint outcome-completion is external receipt of such a perfection rather than an extrinsic relational role of already possessed activity.
57: 
58: Safadiyya retained L618–627 and Salim2:141–146 separate necessary genus of activity, particular intrinsic acts, and particular created effects. The particular-act anchor remains Salim2:145, while the global-inactivity argument is at2:142. No generic rule here says that any newly described relational participation state is a newly acquired constitutive perfection. No model here establishes the full temporal divine-action profile or permits global inactivity by deleting its agent from existence.
59: 
60: Dar9's continuously reread L600–794 supplies the broader context. L627–650 rejects two whole-alone producers while affirming genuinely differentiated cooperation among created causes. L640–644 distinguishes a subject's own act from a separate result requiring other created conditions. L710–750 then argues from independent original power to independent productive efficacy and distinguishes self-chosen alternatives from another agent's enabling. These controls make the argument stronger than a universal prohibition of causation by several factors. They also locate the actual issue in the transfer to original-source independence.
61: 

## checkpoint_background

Source: recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/origin-identity-bridge/RESULT.md
Range: 72–80

72: 
73: The new Python control instead compares:
74: 
75: - Actual: AB originates q; AB preserves q; AB preserves q.
76: - Probe: the **same AB episode** originates q; the same AB preservation occurs; A preserves that same q while B omits only its q-preserving exercise.
77: 
78: The immutable origin-event object and numerical bearer object are literally shared in the model. The first two stages' support records and scheduled exercise records are checked equal. A's stage-specific scheduled exercise records stay equal throughout. In the shutdown control, a later scheduled attempt has no successful preserving effect; no resurrection is credited. Both bearers exist at every stage, and fixed background activity is retained so that withholding B's q-directed exercise is not B's global inactivity. Background activity is declared context, not a new argument establishing its particular wisdom or a hidden contribution to q.
79: 
80: The unchanged retained recurrence supplies continued existence only if q existed previously and some sustaining exercise is active now. If all q-sustaining action ceases, q ceases; later activity does not resurrect it. Thus the probe does not treat q's continued existence as autonomous after origin. Its current support changes AB→A, while q's historical origin remains AB.

## continuation_warrant

Source: t20-continuation-20261008/efficacy-warrant/WARRANT_ASSESSMENT.md
Range: 96–102

96: ## 6. Particular volition and perfection: no illicit universalisation
97: 
98: The necessary-being argument cannot be applied by treating every contingent particular act-token or external end as an eternally necessary constituent of the bearer. The inherited Dar/Safadiyya/Asbahani readings positively distinguish the essential genus of wise activity from each particular exercise and its fitting conditions. Their finding is preserved; it was not reverified as a new full-source reading here.
99: 
100: Accordingly, the affirmative norm is conditional: when the particular original undertaking is complete, its original productive adequacy is unborrowed. It does not require every possible product to exist, every end to be timelessly realised, or every particular intrinsic volition to be a created effect. The rival cannot defeat that conditional norm merely by pointing out that particular acts are optional. Equally, the source defender cannot infer a prior deficient nature from the novelty of an attained end.
101: 
102: Calling original self-provision a perfection rather than a capacity does not resolve these quantifiers. The desired conclusion concerns the adequacy of the chosen exercise; the antecedent necessary-being argument concerns the relevant perfections of the bearer. The source's actual-efficacy argument is the bridge between those scopes.

## continuation_owner_summary

Source: t20-continuation-20261008/owner-review/Orthemology_T20_Updated_Owner_Review_Source_20261008.md
Range: 34–38

34: ## The affirmative argument
35: 
36: The source treats efficacy actually exercised as a possible perfection of the bearer. Minhaj 2:180 argues from conditioned efficacy to dependence of its subject; Majmu 20:174–184 treats harmonious cooperation, unchanged contributors and inseparable mixed effects. Dependence need not take the form of a new intrinsic entity donated by a peer. [S4]
37: 
38: The strongest affirmative claim is conditional: a completed original undertaking obtains its appropriate actual productive adequacy wholly through that bearer. If an independently original peer partly constitutes that adequacy, willing the partnership does not remove the need for foreign completion. Particular voluntary acts must still be distinguished from the necessary bearer and the essential genus of activity; no inference makes every particular act eternally necessary.
