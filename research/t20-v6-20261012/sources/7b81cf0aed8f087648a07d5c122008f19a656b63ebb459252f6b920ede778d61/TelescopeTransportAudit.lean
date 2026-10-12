import TelescopeNatTransport
namespace TelescopeCodeValidity
#check encode_map_encode_tel
#check telNatDecode
#check primrec_telNatDecode
#check telNatDecode_encode
#print axioms encode_map_encode_tel
#print axioms primrec_telNatDecode
#print axioms telNatDecode_encode
example : telNatDecode (Encodable.encode ([] : P01AC.Tel)) = [] := telNatDecode_encode []
end TelescopeCodeValidity
