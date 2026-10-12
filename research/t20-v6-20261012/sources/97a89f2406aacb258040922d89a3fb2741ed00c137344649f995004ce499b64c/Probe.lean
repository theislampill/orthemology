import AuxiliaryCodeCore
namespace AuxiliaryCodeComputability
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity
open AuxiliaryCertificates OrthemologyV2 P01D
set_option maxRecDepth 8192
set_option maxHeartbeats 200000

@[simp] theorem encode_step_i (x : Term) : encode (.i x : StepCert) = pack 0 [leaf (encode x)] := rfl

@[simp] theorem encode_step_k (x y : Term) : encode (.k x y : StepCert) = pack 1 [leaf (encode x), leaf (encode y)] := rfl

@[simp] theorem encode_step_s (f g x : Term) : encode (.s f g x : StepCert) = pack 2 [leaf (encode f), leaf (encode g), leaf (encode x)] := rfl

@[simp] theorem encode_step_left (f g x : Term) (c : StepCert) : encode (.left f g x c : StepCert) = pack 3 [leaf (encode f), leaf (encode g), leaf (encode x), encode c] := rfl

@[simp] theorem encode_step_right (f x y : Term) (c : StepCert) : encode (.right f x y c : StepCert) = pack 4 [leaf (encode f), leaf (encode x), leaf (encode y), encode c] := rfl

end AuxiliaryCodeComputability
