import CertificateCompleteness
import CertificateBinding
open OrthemicCertificate
#check body_sound
#check check_sound
#check region_has_certificate
#check policy_has_certificate
#check semantic_iff_certificate
#print axioms bodyCheck_iff
#print axioms body_sound
#print axioms check_sound
#print axioms Component.exists_valid
#print axioms Witness.exists_valid
#print axioms region_has_certificate
#print axioms policy_has_certificate
#print axioms semantic_iff_certificate
#print axioms boundCheck_iff
#print axioms boundCheck_stale
set_option pp.explicit true in
#check semantic_iff_certificate
set_option pp.explicit true in
#check policy_has_certificate
