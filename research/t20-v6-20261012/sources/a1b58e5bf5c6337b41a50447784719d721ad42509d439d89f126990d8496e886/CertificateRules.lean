/- Finite rule payloads generated from the actual frozen constructor types.
The generated code itself is kernel checked; no source proof is a payload. -/
import CertificateFramework
import AuxiliaryCertificates
namespace JointCertificates
open P01AC P01D OrthemologyV2 OrthemologyV3
set_option maxRecDepth 16384
set_option maxHeartbeats 16000000
set_option linter.unusedVariables false

inductive Rule where
  | CtxJ_ctxBase (Γ : P01AC.Tel)
  | CtxJ_nil 
  | CtxJ_ext (Γ : P01AC.Tel) (A : P01AC.Ty)
  | FormJ_formBase (Γ : P01AC.Tel) (A : P01AC.Ty)
  | FormJ_param (Γ : P01AC.Tel) (n : Nat)
  | FormJ_bottom (Γ : P01AC.Tel)
  | FormJ_all (Γ : P01AC.Tel) (B : P01AC.Ty)
  | FormJ_raw (Γ : P01AC.Tel)
  | FormJ_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty)
  | FormJ_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty)
  | FormJ_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly)
  | HasJ_hasBase (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty)
  | HasJ_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert)
  | HasJ_i (Γ : P01AC.Tel) (A : P01AC.Ty)
  | HasJ_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty)
  | HasJ_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty)
  | HasJ_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert)
  | HasJ_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly)
  | HasJ_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly)
  | HasJ_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term)
  | HasJ_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly)
  | HasJ_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly)
  | HasJ_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly)
  | HasJ_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly)
  | HasJ_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly)
  | HasJ_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly)
  | HasJ_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert)
  | HasJ_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly)
  | HasJ_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly)
  | HasJ_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert)
  | HasJ_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly)
  | HasJ_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly)
  | HasJ_sigmaElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (P : P01AC.Ty) (d : P01D.Poly) (z : P01D.Poly)
  | HasJ_natInduction (Γ : P01AC.Tel) (P : P01AC.Ty) (p : P01D.Poly) (s : P01D.Poly)
  | CtxE_nil 
  | CtxE_ext (Γ : P01AC.Tel) (A : P01AC.Ty)
  | FormE_param (Γ : P01AC.Tel) (n : Nat)
  | FormE_bottom (Γ : P01AC.Tel)
  | FormE_all (Γ : P01AC.Tel) (B : P01AC.Ty)
  | FormE_raw (Γ : P01AC.Tel)
  | FormE_pi (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty)
  | FormE_sigma (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty)
  | FormE_identity (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly)
  | HasE_var (Γ : P01AC.Tel) (A : P01AC.Ty) (n : Nat) (aux0 : AuxiliaryCertificates.LookupCert)
  | HasE_i (Γ : P01AC.Tel) (A : P01AC.Ty)
  | HasE_k (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty)
  | HasE_s (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (C : P01AC.Ty)
  | HasE_finite (C : OrthemologyV2.TypeCode) (Γ : P01AC.Tel) (t : OrthemologyV2.Term) (τ : List P01AC.Ty) (aux0 : AuxiliaryCertificates.FiniteCert)
  | HasE_allIntro (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly)
  | HasE_allElim (Γ : P01AC.Tel) (B : P01AC.Ty) (A : P01AC.Ty) (p : P01D.Poly)
  | HasE_rawAtom (Γ : P01AC.Tel) (t : OrthemologyV2.Term)
  | HasE_rawApp (Γ : P01AC.Tel) (f : P01D.Poly) (a : P01D.Poly)
  | HasE_piIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (b : P01D.Poly)
  | HasE_piElim (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (f : P01D.Poly)
  | HasE_sigmaIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (a : P01D.Poly) (b : P01D.Poly)
  | HasE_sigmaFst (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly)
  | HasE_sigmaSnd (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (z : P01D.Poly)
  | HasE_identityIntro (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert)
  | HasE_proofErase (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (y : P01D.Poly) (p : P01D.Poly)
  | HasE_j (Γ : P01AC.Tel) (A : P01AC.Ty) (x : P01D.Poly) (B : P01AC.Ty) (y : P01D.Poly) (e : P01D.Poly) (d : P01D.Poly)
  | HasE_conv (Γ : P01AC.Tel) (A : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (aux0 : AuxiliaryCertificates.PolyCert)
  | HasE_piExt (Γ : P01AC.Tel) (A : P01AC.Ty) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly)
  | HasE_allExt (Γ : P01AC.Tel) (B : P01AC.Ty) (p : P01D.Poly) (q : P01D.Poly) (h : P01D.Poly)

def Rule.conclusion : Rule → Claim
  | .CtxJ_ctxBase Γ => Claim.ctxJ Γ
  | .CtxJ_nil  => Claim.ctxJ []
  | .CtxJ_ext Γ A => Claim.ctxJ (A :: Γ)
  | .FormJ_formBase Γ A => Claim.formJ Γ A
  | .FormJ_param Γ n => Claim.formJ Γ (P01AC.Ty.param n)
  | .FormJ_bottom Γ => Claim.formJ Γ P01AC.Ty.bottom
  | .FormJ_all Γ B => Claim.formJ Γ B.all
  | .FormJ_raw Γ => Claim.formJ Γ P01AC.Ty.raw
  | .FormJ_pi Γ A B => Claim.formJ Γ (A.pi B)
  | .FormJ_sigma Γ A B => Claim.formJ Γ (A.sigma B)
  | .FormJ_identity Γ A p q => Claim.formJ Γ (A.identity p q)
  | .HasJ_hasBase Γ p A => Claim.hasJ Γ p A
  | .HasJ_var Γ A n aux0 => Claim.hasJ Γ (P01D.Poly.var n) A
  | .HasJ_i Γ A => Claim.hasJ Γ (P01D.Poly.atom OrthemologyV2.Term.i) (P01AC.arr A A)
  | .HasJ_k Γ A B => Claim.hasJ Γ (P01D.Poly.atom OrthemologyV2.Term.k) (P01AC.arr A (P01AC.arr B A))
  | .HasJ_s Γ A B C => Claim.hasJ Γ (P01D.Poly.atom OrthemologyV2.Term.s) (P01AC.arr (P01AC.arr A (P01AC.arr B C)) (P01AC.arr (P01AC.arr A B) (P01AC.arr A C)))
  | .HasJ_finite C Γ t τ aux0 => Claim.hasJ Γ (P01D.Poly.atom t) (P01AC.tsubst (P01AC.typeImages τ) (P01AC.fin C))
  | .HasJ_allIntro Γ B p => Claim.hasJ Γ p B.all
  | .HasJ_allElim Γ B A p => Claim.hasJ Γ p (P01AC.tinst B A)
  | .HasJ_rawAtom Γ t => Claim.hasJ Γ (P01D.Poly.atom t) P01AC.Ty.raw
  | .HasJ_rawApp Γ f a => Claim.hasJ Γ (f.app a) P01AC.Ty.raw
  | .HasJ_piIntro Γ A B b => Claim.hasJ Γ (P01D.abstract b) (A.pi B)
  | .HasJ_piElim Γ A B a f => Claim.hasJ Γ (f.app a) (P01AC.inst B a)
  | .HasJ_sigmaIntro Γ A B a b => Claim.hasJ Γ (P01D.pairPoly a b) (A.sigma B)
  | .HasJ_sigmaFst Γ A B z => Claim.hasJ Γ (P01D.fstPoly z) A
  | .HasJ_sigmaSnd Γ A B z => Claim.hasJ Γ (P01D.sndPoly z) (P01AC.inst B (P01D.fstPoly z))
  | .HasJ_identityIntro Γ A p q aux0 => Claim.hasJ Γ (P01D.Poly.atom OrthemologyV2.Term.i) (A.identity p q)
  | .HasJ_proofErase Γ A x y p => Claim.hasJ Γ p P01AC.Ty.raw
  | .HasJ_j Γ A x B y e d => Claim.hasJ Γ (P01D.jPoly d y e) (P01AC.motiveAt B y e)
  | .HasJ_conv Γ A p q aux0 => Claim.hasJ Γ q A
  | .HasJ_piExt Γ A B p q h => Claim.hasJ Γ (P01D.Poly.atom OrthemologyV2.Term.i) ((A.pi B).identity p q)
  | .HasJ_allExt Γ B p q h => Claim.hasJ Γ (P01D.Poly.atom OrthemologyV2.Term.i) (B.all.identity p q)
  | .HasJ_sigmaElim Γ A B P d z => Claim.hasJ Γ (SigmaCompletion.branchAt d (P01D.fstPoly z) (P01D.sndPoly z)) (P01AC.inst P z)
  | .HasJ_natInduction Γ P p s => Claim.hasJ Γ (RigidityInitiality.sectionPoly p s) (P01AC.EffectiveCompleteness.N.pi P)
  | .CtxE_nil  => Claim.ctxE []
  | .CtxE_ext Γ A => Claim.ctxE (A :: Γ)
  | .FormE_param Γ n => Claim.formE Γ (P01AC.Ty.param n)
  | .FormE_bottom Γ => Claim.formE Γ P01AC.Ty.bottom
  | .FormE_all Γ B => Claim.formE Γ B.all
  | .FormE_raw Γ => Claim.formE Γ P01AC.Ty.raw
  | .FormE_pi Γ A B => Claim.formE Γ (A.pi B)
  | .FormE_sigma Γ A B => Claim.formE Γ (A.sigma B)
  | .FormE_identity Γ A p q => Claim.formE Γ (A.identity p q)
  | .HasE_var Γ A n aux0 => Claim.hasE Γ (P01D.Poly.var n) A
  | .HasE_i Γ A => Claim.hasE Γ (P01D.Poly.atom OrthemologyV2.Term.i) (P01AC.arr A A)
  | .HasE_k Γ A B => Claim.hasE Γ (P01D.Poly.atom OrthemologyV2.Term.k) (P01AC.arr A (P01AC.arr B A))
  | .HasE_s Γ A B C => Claim.hasE Γ (P01D.Poly.atom OrthemologyV2.Term.s) (P01AC.arr (P01AC.arr A (P01AC.arr B C)) (P01AC.arr (P01AC.arr A B) (P01AC.arr A C)))
  | .HasE_finite C Γ t τ aux0 => Claim.hasE Γ (P01D.Poly.atom t) (P01AC.tsubst (P01AC.typeImages τ) (P01AC.fin C))
  | .HasE_allIntro Γ B p => Claim.hasE Γ p B.all
  | .HasE_allElim Γ B A p => Claim.hasE Γ p (P01AC.tinst B A)
  | .HasE_rawAtom Γ t => Claim.hasE Γ (P01D.Poly.atom t) P01AC.Ty.raw
  | .HasE_rawApp Γ f a => Claim.hasE Γ (f.app a) P01AC.Ty.raw
  | .HasE_piIntro Γ A B b => Claim.hasE Γ (P01D.abstract b) (A.pi B)
  | .HasE_piElim Γ A B a f => Claim.hasE Γ (f.app a) (P01AC.inst B a)
  | .HasE_sigmaIntro Γ A B a b => Claim.hasE Γ (P01D.pairPoly a b) (A.sigma B)
  | .HasE_sigmaFst Γ A B z => Claim.hasE Γ (P01D.fstPoly z) A
  | .HasE_sigmaSnd Γ A B z => Claim.hasE Γ (P01D.sndPoly z) (P01AC.inst B (P01D.fstPoly z))
  | .HasE_identityIntro Γ A p q aux0 => Claim.hasE Γ (P01D.Poly.atom OrthemologyV2.Term.i) (A.identity p q)
  | .HasE_proofErase Γ A x y p => Claim.hasE Γ p P01AC.Ty.raw
  | .HasE_j Γ A x B y e d => Claim.hasE Γ (P01D.jPoly d y e) (P01AC.motiveAt B y e)
  | .HasE_conv Γ A p q aux0 => Claim.hasE Γ q A
  | .HasE_piExt Γ A B p q h => Claim.hasE Γ (P01D.Poly.atom OrthemologyV2.Term.i) ((A.pi B).identity p q)
  | .HasE_allExt Γ B p q h => Claim.hasE Γ (P01D.Poly.atom OrthemologyV2.Term.i) (B.all.identity p q)

def Rule.premises : Rule → List Claim
  | .CtxJ_ctxBase Γ => [Claim.ctxE Γ]
  | .CtxJ_nil  => []
  | .CtxJ_ext Γ A => [Claim.ctxJ Γ, Claim.formJ Γ A]
  | .FormJ_formBase Γ A => [Claim.formE Γ A]
  | .FormJ_param Γ n => [Claim.ctxJ Γ]
  | .FormJ_bottom Γ => [Claim.ctxJ Γ]
  | .FormJ_all Γ B => [Claim.ctxJ Γ, Claim.formJ (P01AC.twkTel Γ) B]
  | .FormJ_raw Γ => [Claim.ctxJ Γ]
  | .FormJ_pi Γ A B => [Claim.formJ Γ A, Claim.formJ (A :: Γ) B]
  | .FormJ_sigma Γ A B => [Claim.formJ Γ A, Claim.formJ (A :: Γ) B]
  | .FormJ_identity Γ A p q => [Claim.formJ Γ A, Claim.hasJ Γ p A, Claim.hasJ Γ q A]
  | .HasJ_hasBase Γ p A => [Claim.hasE Γ p A]
  | .HasJ_var Γ A n aux0 => [Claim.formJ Γ A]
  | .HasJ_i Γ A => [Claim.formJ Γ A, Claim.formJ Γ (P01AC.arr A A)]
  | .HasJ_k Γ A B => [Claim.formJ Γ A, Claim.formJ Γ B, Claim.formJ Γ (P01AC.arr A (P01AC.arr B A))]
  | .HasJ_s Γ A B C => [Claim.formJ Γ A, Claim.formJ Γ B, Claim.formJ Γ C, Claim.formJ Γ (P01AC.arr (P01AC.arr A (P01AC.arr B C)) (P01AC.arr (P01AC.arr A B) (P01AC.arr A C)))]
  | .HasJ_finite C Γ t τ aux0 => (List.ofFn (fun i : Fin τ.length => Claim.formJ Γ (P01AC.typeImages τ i.val))) ++ [Claim.formJ Γ (P01AC.tsubst (P01AC.typeImages τ) (P01AC.fin C))]
  | .HasJ_allIntro Γ B p => [Claim.formJ Γ B.all, Claim.hasJ (P01AC.twkTel Γ) p B]
  | .HasJ_allElim Γ B A p => [Claim.formJ Γ B.all, Claim.formJ Γ A, Claim.formJ Γ (P01AC.tinst B A), Claim.hasJ Γ p B.all]
  | .HasJ_rawAtom Γ t => [Claim.formJ Γ P01AC.Ty.raw]
  | .HasJ_rawApp Γ f a => [Claim.formJ Γ P01AC.Ty.raw, Claim.hasJ Γ f P01AC.Ty.raw, Claim.hasJ Γ a P01AC.Ty.raw]
  | .HasJ_piIntro Γ A B b => [Claim.formJ Γ (A.pi B), Claim.hasJ (A :: Γ) b B]
  | .HasJ_piElim Γ A B a f => [Claim.formJ Γ (A.pi B), Claim.formJ Γ (P01AC.inst B a), Claim.hasJ Γ f (A.pi B), Claim.hasJ Γ a A]
  | .HasJ_sigmaIntro Γ A B a b => [Claim.formJ Γ (A.sigma B), Claim.formJ Γ (P01AC.inst B a), Claim.hasJ Γ a A, Claim.hasJ Γ b (P01AC.inst B a)]
  | .HasJ_sigmaFst Γ A B z => [Claim.formJ Γ A, Claim.formJ Γ (A.sigma B), Claim.hasJ Γ z (A.sigma B)]
  | .HasJ_sigmaSnd Γ A B z => [Claim.formJ Γ (A.sigma B), Claim.formJ Γ (P01AC.inst B (P01D.fstPoly z)), Claim.hasJ Γ z (A.sigma B)]
  | .HasJ_identityIntro Γ A p q aux0 => [Claim.formJ Γ (A.identity p q), Claim.hasJ Γ p A, Claim.hasJ Γ q A]
  | .HasJ_proofErase Γ A x y p => [Claim.formJ Γ P01AC.Ty.raw, Claim.formJ Γ (A.identity x y), Claim.hasJ Γ p (A.identity x y)]
  | .HasJ_j Γ A x B y e d => [Claim.formJ Γ A, Claim.formJ (P01AC.theta Γ A x) B, Claim.formJ Γ (A.identity x y), Claim.formJ Γ (P01AC.motiveAt B x (P01D.Poly.atom OrthemologyV2.Term.i)), Claim.formJ Γ (P01AC.motiveAt B y e), Claim.hasJ Γ x A, Claim.hasJ Γ y A, Claim.hasJ Γ e (A.identity x y), Claim.hasJ Γ d (P01AC.motiveAt B x (P01D.Poly.atom OrthemologyV2.Term.i))]
  | .HasJ_conv Γ A p q aux0 => [Claim.formJ Γ A, Claim.hasJ Γ p A]
  | .HasJ_piExt Γ A B p q h => [Claim.formJ Γ A, Claim.formJ (A :: Γ) B, Claim.formJ Γ (A.pi B), Claim.hasJ Γ p (A.pi B), Claim.hasJ Γ q (A.pi B), Claim.formJ (A :: Γ) (B.identity ((P01D.pren Nat.succ p).app (P01D.Poly.var 0)) ((P01D.pren Nat.succ q).app (P01D.Poly.var 0))), Claim.formJ Γ (A.pi (B.identity ((P01D.pren Nat.succ p).app (P01D.Poly.var 0)) ((P01D.pren Nat.succ q).app (P01D.Poly.var 0)))), Claim.hasJ Γ h (A.pi (B.identity ((P01D.pren Nat.succ p).app (P01D.Poly.var 0)) ((P01D.pren Nat.succ q).app (P01D.Poly.var 0)))), Claim.formJ Γ ((A.pi B).identity p q)]
  | .HasJ_allExt Γ B p q h => [Claim.formJ (P01AC.twkTel Γ) B, Claim.formJ Γ B.all, Claim.hasJ Γ p B.all, Claim.hasJ Γ q B.all, Claim.formJ (P01AC.twkTel Γ) (B.identity p q), Claim.hasJ (P01AC.twkTel Γ) h (B.identity p q), Claim.formJ Γ (B.all.identity p q)]
  | .HasJ_sigmaElim Γ A B P d z => [Claim.ctxJ Γ, Claim.formJ Γ A, Claim.formJ (A :: Γ) B, Claim.formJ (A.sigma B :: Γ) P, Claim.hasJ (B :: A :: Γ) d (SigmaCompletion.branchType P), Claim.hasJ Γ z (A.sigma B)]
  | .HasJ_natInduction Γ P p s => [Claim.ctxJ Γ, Claim.formJ (P01AC.EffectiveCompleteness.N :: Γ) P, Claim.hasJ Γ p (P01AC.inst P SourceRigidity.zero), Claim.hasJ Γ s (RigidityInitiality.dependentStepType P)]
  | .CtxE_nil  => []
  | .CtxE_ext Γ A => [Claim.ctxE Γ, Claim.formE Γ A]
  | .FormE_param Γ n => [Claim.ctxE Γ]
  | .FormE_bottom Γ => [Claim.ctxE Γ]
  | .FormE_all Γ B => [Claim.ctxE Γ, Claim.formE (P01AC.twkTel Γ) B]
  | .FormE_raw Γ => [Claim.ctxE Γ]
  | .FormE_pi Γ A B => [Claim.formE Γ A, Claim.formE (A :: Γ) B]
  | .FormE_sigma Γ A B => [Claim.formE Γ A, Claim.formE (A :: Γ) B]
  | .FormE_identity Γ A p q => [Claim.formE Γ A, Claim.hasE Γ p A, Claim.hasE Γ q A]
  | .HasE_var Γ A n aux0 => [Claim.formE Γ A]
  | .HasE_i Γ A => [Claim.formE Γ A, Claim.formE Γ (P01AC.arr A A)]
  | .HasE_k Γ A B => [Claim.formE Γ A, Claim.formE Γ B, Claim.formE Γ (P01AC.arr A (P01AC.arr B A))]
  | .HasE_s Γ A B C => [Claim.formE Γ A, Claim.formE Γ B, Claim.formE Γ C, Claim.formE Γ (P01AC.arr (P01AC.arr A (P01AC.arr B C)) (P01AC.arr (P01AC.arr A B) (P01AC.arr A C)))]
  | .HasE_finite C Γ t τ aux0 => (List.ofFn (fun i : Fin τ.length => Claim.formE Γ (P01AC.typeImages τ i.val))) ++ [Claim.formE Γ (P01AC.tsubst (P01AC.typeImages τ) (P01AC.fin C))]
  | .HasE_allIntro Γ B p => [Claim.formE Γ B.all, Claim.hasE (P01AC.twkTel Γ) p B]
  | .HasE_allElim Γ B A p => [Claim.formE Γ B.all, Claim.formE Γ A, Claim.formE Γ (P01AC.tinst B A), Claim.hasE Γ p B.all]
  | .HasE_rawAtom Γ t => [Claim.formE Γ P01AC.Ty.raw]
  | .HasE_rawApp Γ f a => [Claim.formE Γ P01AC.Ty.raw, Claim.hasE Γ f P01AC.Ty.raw, Claim.hasE Γ a P01AC.Ty.raw]
  | .HasE_piIntro Γ A B b => [Claim.formE Γ (A.pi B), Claim.hasE (A :: Γ) b B]
  | .HasE_piElim Γ A B a f => [Claim.formE Γ (A.pi B), Claim.formE Γ (P01AC.inst B a), Claim.hasE Γ f (A.pi B), Claim.hasE Γ a A]
  | .HasE_sigmaIntro Γ A B a b => [Claim.formE Γ (A.sigma B), Claim.formE Γ (P01AC.inst B a), Claim.hasE Γ a A, Claim.hasE Γ b (P01AC.inst B a)]
  | .HasE_sigmaFst Γ A B z => [Claim.formE Γ A, Claim.formE Γ (A.sigma B), Claim.hasE Γ z (A.sigma B)]
  | .HasE_sigmaSnd Γ A B z => [Claim.formE Γ (A.sigma B), Claim.formE Γ (P01AC.inst B (P01D.fstPoly z)), Claim.hasE Γ z (A.sigma B)]
  | .HasE_identityIntro Γ A p q aux0 => [Claim.formE Γ (A.identity p q), Claim.hasE Γ p A, Claim.hasE Γ q A]
  | .HasE_proofErase Γ A x y p => [Claim.formE Γ P01AC.Ty.raw, Claim.formE Γ (A.identity x y), Claim.hasE Γ p (A.identity x y)]
  | .HasE_j Γ A x B y e d => [Claim.formE Γ A, Claim.formE (P01AC.theta Γ A x) B, Claim.formE Γ (A.identity x y), Claim.formE Γ (P01AC.motiveAt B x (P01D.Poly.atom OrthemologyV2.Term.i)), Claim.formE Γ (P01AC.motiveAt B y e), Claim.hasE Γ x A, Claim.hasE Γ y A, Claim.hasE Γ e (A.identity x y), Claim.hasE Γ d (P01AC.motiveAt B x (P01D.Poly.atom OrthemologyV2.Term.i))]
  | .HasE_conv Γ A p q aux0 => [Claim.formE Γ A, Claim.hasE Γ p A]
  | .HasE_piExt Γ A B p q h => [Claim.formE Γ A, Claim.formE (A :: Γ) B, Claim.formE Γ (A.pi B), Claim.hasE Γ p (A.pi B), Claim.hasE Γ q (A.pi B), Claim.formE (A :: Γ) (B.identity ((P01D.pren Nat.succ p).app (P01D.Poly.var 0)) ((P01D.pren Nat.succ q).app (P01D.Poly.var 0))), Claim.formE Γ (A.pi (B.identity ((P01D.pren Nat.succ p).app (P01D.Poly.var 0)) ((P01D.pren Nat.succ q).app (P01D.Poly.var 0)))), Claim.hasE Γ h (A.pi (B.identity ((P01D.pren Nat.succ p).app (P01D.Poly.var 0)) ((P01D.pren Nat.succ q).app (P01D.Poly.var 0)))), Claim.formE Γ ((A.pi B).identity p q)]
  | .HasE_allExt Γ B p q h => [Claim.formE (P01AC.twkTel Γ) B, Claim.formE Γ B.all, Claim.hasE Γ p B.all, Claim.hasE Γ q B.all, Claim.formE (P01AC.twkTel Γ) (B.identity p q), Claim.hasE (P01AC.twkTel Γ) h (B.identity p q), Claim.formE Γ (B.all.identity p q)]

def Rule.checkSide : Rule → Bool
  | .CtxJ_ctxBase Γ => decide (True)
  | .CtxJ_nil  => decide (True)
  | .CtxJ_ext Γ A => decide (True)
  | .FormJ_formBase Γ A => decide (True)
  | .FormJ_param Γ n => decide (True)
  | .FormJ_bottom Γ => decide (True)
  | .FormJ_all Γ B => decide (True)
  | .FormJ_raw Γ => decide (True)
  | .FormJ_pi Γ A B => decide (True)
  | .FormJ_sigma Γ A B => decide (True)
  | .FormJ_identity Γ A p q => decide (True)
  | .HasJ_hasBase Γ p A => decide (True)
  | .HasJ_var Γ A n aux0 => decide ((AuxiliaryCertificates.checkLookup aux0 Γ n A = true) ∧ True)
  | .HasJ_i Γ A => decide (True)
  | .HasJ_k Γ A B => decide (True)
  | .HasJ_s Γ A B C => decide (True)
  | .HasJ_finite C Γ t τ aux0 => decide ((P01AC.finSupport C ≤ τ.length) ∧ (AuxiliaryCertificates.checkFinite aux0 t C = true) ∧ True)
  | .HasJ_allIntro Γ B p => decide (True)
  | .HasJ_allElim Γ B A p => decide (True)
  | .HasJ_rawAtom Γ t => decide (True)
  | .HasJ_rawApp Γ f a => decide (True)
  | .HasJ_piIntro Γ A B b => decide ((P01AC.Scoped (List.length Γ) (P01D.abstract b)) ∧ True)
  | .HasJ_piElim Γ A B a f => decide (True)
  | .HasJ_sigmaIntro Γ A B a b => decide (True)
  | .HasJ_sigmaFst Γ A B z => decide (True)
  | .HasJ_sigmaSnd Γ A B z => decide (True)
  | .HasJ_identityIntro Γ A p q aux0 => decide ((AuxiliaryCertificates.checkPoly aux0 p q = true) ∧ True)
  | .HasJ_proofErase Γ A x y p => decide (True)
  | .HasJ_j Γ A x B y e d => decide (True)
  | .HasJ_conv Γ A p q aux0 => decide ((AuxiliaryCertificates.checkPoly aux0 p q = true) ∧ (P01AC.Scoped (List.length Γ) q) ∧ True)
  | .HasJ_piExt Γ A B p q h => decide ((P01AC.Scoped (List.length Γ) p) ∧ (P01AC.Scoped (List.length Γ) q) ∧ (P01AC.Scoped (List.length Γ) h) ∧ (P01AC.TyScoped (List.length Γ) A) ∧ (P01AC.TyScoped (List.length Γ + 1) B) ∧ True)
  | .HasJ_allExt Γ B p q h => decide ((P01AC.Scoped (List.length Γ) p) ∧ (P01AC.Scoped (List.length Γ) q) ∧ (P01AC.Scoped (List.length Γ) h) ∧ (P01AC.TyScoped (List.length Γ) B) ∧ True)
  | .HasJ_sigmaElim Γ A B P d z => decide (True)
  | .HasJ_natInduction Γ P p s => decide (True)
  | .CtxE_nil  => decide (True)
  | .CtxE_ext Γ A => decide (True)
  | .FormE_param Γ n => decide (True)
  | .FormE_bottom Γ => decide (True)
  | .FormE_all Γ B => decide (True)
  | .FormE_raw Γ => decide (True)
  | .FormE_pi Γ A B => decide (True)
  | .FormE_sigma Γ A B => decide (True)
  | .FormE_identity Γ A p q => decide (True)
  | .HasE_var Γ A n aux0 => decide ((AuxiliaryCertificates.checkLookup aux0 Γ n A = true) ∧ True)
  | .HasE_i Γ A => decide (True)
  | .HasE_k Γ A B => decide (True)
  | .HasE_s Γ A B C => decide (True)
  | .HasE_finite C Γ t τ aux0 => decide ((P01AC.finSupport C ≤ τ.length) ∧ (AuxiliaryCertificates.checkFinite aux0 t C = true) ∧ True)
  | .HasE_allIntro Γ B p => decide (True)
  | .HasE_allElim Γ B A p => decide (True)
  | .HasE_rawAtom Γ t => decide (True)
  | .HasE_rawApp Γ f a => decide (True)
  | .HasE_piIntro Γ A B b => decide ((P01AC.Scoped (List.length Γ) (P01D.abstract b)) ∧ True)
  | .HasE_piElim Γ A B a f => decide (True)
  | .HasE_sigmaIntro Γ A B a b => decide (True)
  | .HasE_sigmaFst Γ A B z => decide (True)
  | .HasE_sigmaSnd Γ A B z => decide (True)
  | .HasE_identityIntro Γ A p q aux0 => decide ((AuxiliaryCertificates.checkPoly aux0 p q = true) ∧ True)
  | .HasE_proofErase Γ A x y p => decide (True)
  | .HasE_j Γ A x B y e d => decide (True)
  | .HasE_conv Γ A p q aux0 => decide ((AuxiliaryCertificates.checkPoly aux0 p q = true) ∧ (P01AC.Scoped (List.length Γ) q) ∧ True)
  | .HasE_piExt Γ A B p q h => decide ((P01AC.Scoped (List.length Γ) p) ∧ (P01AC.Scoped (List.length Γ) q) ∧ (P01AC.Scoped (List.length Γ) h) ∧ (P01AC.TyScoped (List.length Γ) A) ∧ (P01AC.TyScoped (List.length Γ + 1) B) ∧ True)
  | .HasE_allExt Γ B p q h => decide ((P01AC.Scoped (List.length Γ) p) ∧ (P01AC.Scoped (List.length Γ) q) ∧ (P01AC.Scoped (List.length Γ) h) ∧ (P01AC.TyScoped (List.length Γ) B) ∧ True)

theorem Rule.sound (r : Rule) (hs : r.checkSide = true)
    (hp : All Claim.denote r.premises) : r.conclusion.denote := by
  cases r with
  | CtxJ_ctxBase Γ =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.CtxJ.ctxBase Γ h0
  | CtxJ_nil  =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      exact @JointCompletion.CtxJ.nil 
  | CtxJ_ext Γ A =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.CtxJ.ext Γ A h0 h1
  | FormJ_formBase Γ A =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.FormJ.formBase Γ A h0
  | FormJ_param Γ n =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.FormJ.param Γ n h0
  | FormJ_bottom Γ =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.FormJ.bottom Γ h0
  | FormJ_all Γ B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.FormJ.all Γ B h0 h1
  | FormJ_raw Γ =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.FormJ.raw Γ h0
  | FormJ_pi Γ A B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.FormJ.pi Γ A B h0 h1
  | FormJ_sigma Γ A B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.FormJ.sigma Γ A B h0 h1
  | FormJ_identity Γ A p q =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.FormJ.identity Γ A p q h0 h1 h2
  | HasJ_hasBase Γ p A =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.HasJ.hasBase Γ p A h0
  | HasJ_var Γ A n aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.HasJ.var Γ A n h0 (AuxiliaryCertificates.checkLookup_sound s0)
  | HasJ_i Γ A =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.HasJ.i Γ A h0 h1
  | HasJ_k Γ A B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.HasJ.k Γ A B h0 h1 h2
  | HasJ_s Γ A B C =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @JointCompletion.HasJ.s Γ A B C h0 h1 h2 h3
  | HasJ_finite C Γ t τ aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, _⟩
      simp only [Rule.premises, all_append, all_ofFn, All, Claim.denote] at hp
      rcases hp with ⟨hfamily, ⟨h0, _⟩⟩
      exact @JointCompletion.HasJ.finite C Γ t τ s0 (fun n hn => hfamily ⟨n,hn⟩) h0 (AuxiliaryCertificates.checkFinite_sound s1)
  | HasJ_allIntro Γ B p =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.HasJ.allIntro Γ B p h0 h1
  | HasJ_allElim Γ B A p =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @JointCompletion.HasJ.allElim Γ B A p h0 h1 h2 h3
  | HasJ_rawAtom Γ t =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @JointCompletion.HasJ.rawAtom Γ t h0
  | HasJ_rawApp Γ f a =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.HasJ.rawApp Γ f a h0 h1 h2
  | HasJ_piIntro Γ A B b =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.HasJ.piIntro Γ A B b h0 h1 s0
  | HasJ_piElim Γ A B a f =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @JointCompletion.HasJ.piElim Γ A B a f h0 h1 h2 h3
  | HasJ_sigmaIntro Γ A B a b =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @JointCompletion.HasJ.sigmaIntro Γ A B a b h0 h1 h2 h3
  | HasJ_sigmaFst Γ A B z =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.HasJ.sigmaFst Γ A B z h0 h1 h2
  | HasJ_sigmaSnd Γ A B z =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.HasJ.sigmaSnd Γ A B z h0 h1 h2
  | HasJ_identityIntro Γ A p q aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.HasJ.identityIntro Γ A p q h0 h1 h2 (AuxiliaryCertificates.checkPoly_sound s0)
  | HasJ_proofErase Γ A x y p =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @JointCompletion.HasJ.proofErase Γ A x y p h0 h1 h2
  | HasJ_j Γ A x B y e d =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, _⟩
      exact @JointCompletion.HasJ.j Γ A x B y e d h0 h1 h2 h3 h4 h5 h6 h7 h8
  | HasJ_conv Γ A p q aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @JointCompletion.HasJ.conv Γ A p q h0 h1 (AuxiliaryCertificates.checkPoly_sound s0) s1
  | HasJ_piExt Γ A B p q h =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, s2, s3, s4, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, _⟩
      exact @JointCompletion.HasJ.piExt Γ A B p q h h0 h1 h2 h3 h4 h5 h6 h7 h8 s0 s1 s2 s3 s4
  | HasJ_allExt Γ B p q h =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, s2, s3, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, h6, _⟩
      exact @JointCompletion.HasJ.allExt Γ B p q h h0 h1 h2 h3 h4 h5 h6 s0 s1 s2 s3
  | HasJ_sigmaElim Γ A B P d z =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, _⟩
      exact @JointCompletion.HasJ.sigmaElim Γ A B P d z h0 h1 h2 h3 h4 h5
  | HasJ_natInduction Γ P p s =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @JointCompletion.HasJ.natInduction Γ P p s h0 h1 h2 h3
  | CtxE_nil  =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      exact @P01AC.ExtensionalRepair.CtxE.nil 
  | CtxE_ext Γ A =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.CtxE.ext Γ A h0 h1
  | FormE_param Γ n =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @P01AC.ExtensionalRepair.FormE.param Γ n h0
  | FormE_bottom Γ =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @P01AC.ExtensionalRepair.FormE.bottom Γ h0
  | FormE_all Γ B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.FormE.all Γ B h0 h1
  | FormE_raw Γ =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @P01AC.ExtensionalRepair.FormE.raw Γ h0
  | FormE_pi Γ A B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.FormE.pi Γ A B h0 h1
  | FormE_sigma Γ A B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.FormE.sigma Γ A B h0 h1
  | FormE_identity Γ A p q =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.FormE.identity Γ A p q h0 h1 h2
  | HasE_var Γ A n aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @P01AC.ExtensionalRepair.HasE.var Γ A n h0 (AuxiliaryCertificates.checkLookup_sound s0)
  | HasE_i Γ A =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.HasE.i Γ A h0 h1
  | HasE_k Γ A B =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.HasE.k Γ A B h0 h1 h2
  | HasE_s Γ A B C =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @P01AC.ExtensionalRepair.HasE.s Γ A B C h0 h1 h2 h3
  | HasE_finite C Γ t τ aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, _⟩
      simp only [Rule.premises, all_append, all_ofFn, All, Claim.denote] at hp
      rcases hp with ⟨hfamily, ⟨h0, _⟩⟩
      exact @P01AC.ExtensionalRepair.HasE.finite C Γ t τ s0 (fun n hn => hfamily ⟨n,hn⟩) h0 (AuxiliaryCertificates.checkFinite_sound s1)
  | HasE_allIntro Γ B p =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.HasE.allIntro Γ B p h0 h1
  | HasE_allElim Γ B A p =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @P01AC.ExtensionalRepair.HasE.allElim Γ B A p h0 h1 h2 h3
  | HasE_rawAtom Γ t =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, _⟩
      exact @P01AC.ExtensionalRepair.HasE.rawAtom Γ t h0
  | HasE_rawApp Γ f a =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.HasE.rawApp Γ f a h0 h1 h2
  | HasE_piIntro Γ A B b =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.HasE.piIntro Γ A B b h0 h1 s0
  | HasE_piElim Γ A B a f =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @P01AC.ExtensionalRepair.HasE.piElim Γ A B a f h0 h1 h2 h3
  | HasE_sigmaIntro Γ A B a b =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, _⟩
      exact @P01AC.ExtensionalRepair.HasE.sigmaIntro Γ A B a b h0 h1 h2 h3
  | HasE_sigmaFst Γ A B z =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.HasE.sigmaFst Γ A B z h0 h1 h2
  | HasE_sigmaSnd Γ A B z =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.HasE.sigmaSnd Γ A B z h0 h1 h2
  | HasE_identityIntro Γ A p q aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.HasE.identityIntro Γ A p q h0 h1 h2 (AuxiliaryCertificates.checkPoly_sound s0)
  | HasE_proofErase Γ A x y p =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, _⟩
      exact @P01AC.ExtensionalRepair.HasE.proofErase Γ A x y p h0 h1 h2
  | HasE_j Γ A x B y e d =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, _⟩
      exact @P01AC.ExtensionalRepair.HasE.j Γ A x B y e d h0 h1 h2 h3 h4 h5 h6 h7 h8
  | HasE_conv Γ A p q aux0 =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, _⟩
      exact @P01AC.ExtensionalRepair.HasE.conv Γ A p q h0 h1 (AuxiliaryCertificates.checkPoly_sound s0) s1
  | HasE_piExt Γ A B p q h =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, s2, s3, s4, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, _⟩
      exact @P01AC.ExtensionalRepair.HasE.piExt Γ A B p q h h0 h1 h2 h3 h4 h5 h6 h7 h8 s0 s1 s2 s3 s4
  | HasE_allExt Γ B p q h =>
      simp only [Rule.checkSide, decide_eq_true_eq] at hs
      rcases hs with ⟨s0, s1, s2, s3, _⟩
      simp only [Rule.premises, All, Claim.denote] at hp
      rcases hp with ⟨h0, h1, h2, h3, h4, h5, h6, _⟩
      exact @P01AC.ExtensionalRepair.HasE.allExt Γ B p q h h0 h1 h2 h3 h4 h5 h6 s0 s1 s2 s3

abbrev DerivationCertificate := Certificate Rule

def check (c : DerivationCertificate) (j : Claim) : Bool :=
  Certificate.checkRoot Rule.conclusion Rule.premises Rule.checkSide c j

theorem check_sound {c : DerivationCertificate} {j : Claim} (h : check c j = true) : j.denote :=
  Certificate.checkRoot_sound _ _ _ Rule.sound c j h

abbrev Proved := Certificate.Proved Rule.conclusion Rule.premises Rule.checkSide

theorem proved_rule (r : Rule) (hs : r.checkSide = true) (hp : All Proved r.premises) :
    Proved r.conclusion := Certificate.proved_rule _ _ _ r hs hp

#print axioms Rule.sound
#print axioms check_sound
end JointCertificates
