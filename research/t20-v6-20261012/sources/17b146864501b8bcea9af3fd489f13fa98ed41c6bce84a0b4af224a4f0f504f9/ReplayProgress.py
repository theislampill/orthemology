# Diagnostic helper only; does not modify candidate sources.
from pathlib import Path
r=Path(__file__).resolve().parent.parent
for typ in ['StepCert','RedCert','FiniteCert','PolyCert','LookupCert','Claim','Rule','SerialCert','SerialCertList']:
 print(typ, (r/'validation'/(typ+'ImageRule.olean')).exists(), (r/'validation'/(typ+'Bounds.olean')).exists())
