/- Deliberate rejected interface use. This is not a logical independence proof. -/
import EffectivePartialObserver
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity

example {p q : Poly} (hq : Has [] q C) :
    EndpointValid p q ↔ CanonicalTests p q :=
  endpoint_valid_iff_canonical_tests (p := p) (q := q) hq hq
