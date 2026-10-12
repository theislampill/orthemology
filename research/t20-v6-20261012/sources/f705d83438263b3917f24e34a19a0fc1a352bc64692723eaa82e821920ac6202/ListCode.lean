import FiniteExact
import TermTypeSubstitution
import EncodedCertificatePayloads
#check Encodable.encode_list_cons
#check Encodable.encode_list_nil
#check Encodable.encode_list
#print Encodable.encodeList
set_option pp.all true in
#synth Encodable (List P01AC.Ty)
