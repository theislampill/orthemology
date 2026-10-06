import CertificateBinding
import CertificateFixtures
open OrthemicCertificate OrthemicCertificate.Fixtures
private def packet : BoundBody 3 3 3 := ⟨reveal,revealedBody⟩
private def changedInput : Input 3 3 3 :=
  {reveal with interpretation := {reveal.interpretation with authority := "different declaration"}}
#guard boundCheck reveal packet {0,1,2} 0
#guard check changedInput revealedBody {0,1,2} 0
#guard !(boundCheck changedInput packet {0,1,2} 0)
#guard boundCheck changedInput ⟨changedInput,revealedBody⟩ {0,1,2} 0
