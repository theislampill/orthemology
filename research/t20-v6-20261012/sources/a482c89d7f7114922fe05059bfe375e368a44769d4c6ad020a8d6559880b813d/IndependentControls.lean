import TypeInhabitationSearch
import Lean
namespace IndependentActualSourceReview
open Encodable JointCertificates ActualSourceEnumerability CertificateCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 4000000

theorem acceptedInputsCanonical {q c : Nat} (h : checkCanonical q c = true) :
    (∃ j : Claim, encode j = q) ∧ (∃ s : SerialCert, encode s = c) := by
  simp only [checkCanonical, Bool.and_eq_true] at h
  exact ⟨(valid_Claim _).mp h.1.1, (valid_SerialCert _).mp h.1.2⟩

theorem rejectEveryNoncanonicalClaim (q c : Nat) (hq : ¬ ∃ j : Claim, encode j = q) :
    checkCanonical q c = false := by
  cases h : checkCanonical q c
  · rfl
  · exact False.elim (hq (acceptedInputsCanonical h).1)

theorem rejectEveryNoncanonicalCertificate (q c : Nat) (hc : ¬ ∃ s : SerialCert, encode s = c) :
    checkCanonical q c = false := by
  cases h : checkCanonical q c
  · rfl
  · exact False.elim (hc (acceptedInputsCanonical h).2)

theorem acceptedListArity {cs : SerialCertList} {js : List Claim}
    (h : serialCheckList cs js = true) : (fromSerialList cs).length = js.length := by
  rw [serialCheckList_exact] at h
  simp only [coreList, Bool.and_eq_true, decide_eq_true_eq] at h
  have he := congrArg List.length h.1
  simpa only [List.length_map] using he

theorem emptyRejectsRemainder (j : Claim) (js : List Claim) :
    serialCheckList .nil (j :: js) = false := rfl

theorem nonemptyRejectsExhausted (c : SerialCert) (cs : SerialCertList) :
    serialCheckList (.cons c cs) [] = false := rfl

theorem repeatedClaimSwapIsHarmless (a b : SerialCert) (j : Claim) :
    serialCheckList (.cons a (.cons b .nil)) [j,j] =
      serialCheckList (.cons b (.cons a .nil)) [j,j] := by
  simp only [serialCheckList, Bool.and_true, Bool.true_and, Bool.and_comm]

def jEmpty : SerialCert := .node .CtxJ_nil .nil
def eEmpty : SerialCert := .node .CtxE_nil .nil

theorem pairedDistinctAccept :
    serialCheckList (.cons jEmpty (.cons eEmpty .nil)) [.ctxJ [], .ctxE []] = true := by
  decide

theorem pairedDistinctSwapReject :
    serialCheckList (.cons eEmpty (.cons jEmpty .nil)) [.ctxJ [], .ctxE []] = false := by
  decide

theorem numericPairedOrderReject :
    runList (encode ([.ctxJ [], .ctxE []] : List Claim))
      (encode (SerialCertList.cons eEmpty (.cons jEmpty .nil))) = false := by
  rw [runList_exact]
  exact pairedDistinctSwapReject

theorem acceptedRootHasActualSourceMeaning {q c : Nat} (h : checkCanonical q c = true) :
    ∃ j : Claim, encode j = q ∧ j.denote := checkCanonical_sound h

theorem returnedCertificateIsSound {q c : Nat} (h : c ∈ proofSearch q) : DerivableCode q :=
  checkCanonical_sound ((proofSearch_mem q c).mp h).1

theorem searchReturnsLeastAccepted (q c : Nat) (hc : c ∈ proofSearch q) :
    ∀ d, checkCanonical q d = true → c ≤ d := by
  intro d hd
  by_contra hn
  have hf := ((proofSearch_mem q c).mp hc).2 d (by omega)
  rw [hd] at hf
  contradiction

theorem malformedClaimNoSearch (q : Nat) (hq : ¬ ∃ j : Claim, encode j = q) :
    ¬ (proofSearch q).Dom := by
  intro h
  obtain ⟨j, hj, _⟩ := (proofSearch_dom q).mp h
  exact hq ⟨j,hj⟩

theorem acceptedInhabitantHasThreeCanonicalComponents {a w : Nat}
    (h : inhabitantCheck a w = true) :
    (∃ A : P01AC.Ty, encode A = a) ∧
    (∃ p : P01D.Poly, encode p = w.unpair.1) ∧
    (∃ c : SerialCert, encode c = w.unpair.2) := by
  simp only [inhabitantCheck, Bool.and_eq_true] at h
  exact ⟨(valid_ty _).mp h.1.1, (valid_poly _).mp h.1.2,
    (acceptedInputsCanonical h.2).2⟩

theorem suppliedTermDomain (p : P01D.Poly) (A : P01AC.Ty) :
    (proofSearch (encode (Claim.hasJ [] p A))).Dom ↔ JointCompletion.HasJ [] p A :=
  proofSearch_hasJ [] p A

theorem existentialTermDomain (A : P01AC.Ty) :
    (inhabitantSearch (encode A)).Dom ↔ ∃ p : P01D.Poly, JointCompletion.HasJ [] p A :=
  inhabitantSearch_exact A

theorem malformedTypeNoSearch (a : Nat) (ha : ¬ ∃ A : P01AC.Ty, encode A = a) :
    ¬ (inhabitantSearch a).Dom := by
  intro h
  obtain ⟨A, hA, _⟩ := (inhabitantSearch_dom a).mp h
  exact ha ⟨A,hA⟩

theorem inhabitantReturnsLeastPair (a w : Nat) : w ∈ inhabitantSearch a ↔
    inhabitantCheck a w = true ∧ ∀ v, v < w → inhabitantCheck a v = false := by
  simp [inhabitantSearch, Nat.mem_rfind]


def baseEmpty : DerivationCertificate := .node .CtxJ_nil []
def rawFormation : DerivationCertificate := .node (.FormJ_raw []) [baseEmpty]
def bottomFormation : DerivationCertificate := .node (.FormJ_bottom []) [baseEmpty]
def rawExtension : DerivationCertificate := .node (.CtxJ_ext [] .raw) [baseEmpty, rawFormation]
def nestedRawFormation : DerivationCertificate := .node (.FormJ_raw [.raw]) [rawExtension]
def arrowFormation : DerivationCertificate := .node (.FormJ_pi [] .raw .raw)
  [rawFormation, nestedRawFormation]
def finiteRule : Rule := .HasJ_finite (.arrow (.var 0) (.var 0)) [] .i [.raw, .bottom] (.i (.var 0))
def completeFinite : DerivationCertificate := .node finiteRule [rawFormation, bottomFormation, arrowFormation]
def omitOnlyUnusedImage : DerivationCertificate := .node finiteRule [rawFormation, arrowFormation]

local macro "finite_control" : tactic => `(tactic|
  (simp only [check, Certificate.checkRoot, Certificate.check_node,
    baseEmpty, rawFormation, bottomFormation, rawExtension, nestedRawFormation,
    arrowFormation, finiteRule, completeFinite, omitOnlyUnusedImage,
    Certificate.rule, List.map_cons, List.map_nil, List.all_cons, List.all_nil,
    Rule.checkSide, Rule.premises, Rule.conclusion, Bool.true_and, Bool.and_true,
    Bool.false_and, Bool.and_false, decide_true, decide_false] <;> decide))

theorem fullFiniteAccepts : checkCanonical (encode finiteRule.conclusion)
    (encodeCertificate completeFinite) = true := by
  rw [checkCanonical_encode]
  finite_control

theorem singleUnusedImageOmissionRejects : checkCanonical (encode finiteRule.conclusion)
    (encodeCertificate omitOnlyUnusedImage) = false := by
  rw [checkCanonical_encode]
  finite_control


def rawAtomCertificate : DerivationCertificate := .node (.HasJ_rawAtom [] .i) [rawFormation]

theorem concreteClosedInhabitantAccepted :
    inhabitantCheck (encode P01AC.Ty.raw)
      (Nat.pair (encode (P01D.Poly.atom .i)) (encodeCertificate rawAtomCertificate)) = true := by
  rw [inhabitantCheck_exact]
  unfold rawAtomCertificate
  finite_control

theorem typeZeroInvalid : certValid 3 0 = false := by
  have hz : ExactSyntaxValidity.shape (3, 0) = false := by decide
  have hv : ExactSyntaxValidity.valid 3 0 = false := by
    rw [ExactSyntaxValidity.valid, ExactSyntaxValidity.evaluate, hz]
    rfl
  rw [certValid, ExactSyntaxValidity.evaluate]
  simp [certShape, certChildren, hv]

theorem zeroInhabitationUndefined : ¬ (inhabitantSearch 0).Dom := by
  apply malformedTypeNoSearch
  intro h
  have ht := (valid_ty 0).mpr h
  rw [typeZeroInvalid] at ht
  contradiction

-- Small serial controls only. No execution of the unbounded searches.
#eval serialCheckList (.cons jEmpty (.cons eEmpty .nil)) [.ctxJ [], .ctxE []]
#eval serialCheckList (.cons eEmpty (.cons jEmpty .nil)) [.ctxJ [], .ctxE []]

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``acceptedInputsCanonical, ``rejectEveryNoncanonicalClaim,
      ``rejectEveryNoncanonicalCertificate, ``acceptedListArity,
      ``repeatedClaimSwapIsHarmless, ``pairedDistinctAccept, ``pairedDistinctSwapReject,
      ``numericPairedOrderReject, ``acceptedRootHasActualSourceMeaning,
      ``returnedCertificateIsSound, ``searchReturnsLeastAccepted, ``malformedClaimNoSearch,
      ``acceptedInhabitantHasThreeCanonicalComponents, ``suppliedTermDomain,
      ``existentialTermDomain, ``malformedTypeNoSearch, ``inhabitantReturnsLeastPair,
      ``fullFiniteAccepts, ``singleUnusedImageOmissionRejects,
      ``concreteClosedInhabitantAccepted, ``typeZeroInvalid, ``zeroInhabitationUndefined] do
    let (_, audit) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in audit.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom: {target}, {ax}"
    for name in audit.visited do
      if name.toString.startsWith "FullPER." || name.toString == "JointCompletion.fundamental" then
        throwError "Semantic oracle: {target}, {name}"
    logInfo m!"PASS independent control {target}"
end IndependentActualSourceReview
