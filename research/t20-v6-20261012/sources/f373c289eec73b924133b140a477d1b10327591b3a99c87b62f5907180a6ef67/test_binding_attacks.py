"""Adversarial JSON binding controls plus intentionally rejected Lean replays."""
import copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_diag',ROOT/'sources/diagnostic.py')
d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
header='import LiteralSourceQ\nset_option maxRecDepth 32768\nset_option maxHeartbeats 8000000\n'
source0=d.SOURCE['numerals'][0];source1=d.SOURCE['numerals'][1]
valid=d.diagnose(source0)['certificate']
assert d.check_certificate(valid,expected_input=source0)
assert not d.check_certificate(valid,expected_input=source1)
# Swapping the intended input under unchanged count/traces must fail replay.
wrong=copy.deepcopy(valid);wrong['input']=source1
assert not d.check_certificate(wrong,expected_input=source1)
text=d.lean_certificate(valid,'changed_input')
old='def changed_input_n : P01D.Poly := '+d.lean_poly(source0)
new='def changed_input_n : P01D.Poly := '+d.lean_poly(source1)
assert old in text
(ROOT/'ChangedInputMustFail.lean').write_text(header+text.replace(old,new,1))
# A compromised JSON Q can fool a diagnostic whose local Q binding was changed.
# Kernel replay still targets FullPER.Application.originalQ literally.
original_q=d.ORIGINAL_Q;original_digest=d.Q_DIGEST
d.ORIGINAL_Q=['atom',['i']];d.Q_DIGEST=d.digest(d.ORIGINAL_Q)
fake=d.diagnose(source0)['certificate']
assert d.check_certificate(fake,expected_input=source0)
(ROOT/'FakeQMustFail.lean').write_text(header+d.lean_certificate(fake,'fake_q'))
(ROOT/'validation/FAKE_Q_CERTIFICATE.json').write_text(json.dumps(fake,indent=2)+'\n')
d.ORIGINAL_Q=original_q;d.Q_DIGEST=original_digest
assert not d.check_certificate(fake,expected_input=source0)
# A valid open erasing input can certify conversion; it cannot silently certify scope zero.
open_n=['app',['app',['atom',['k']],source0],['var',42]]
open_cert=d.diagnose(open_n)['certificate']; emitted=d.lean_certificate(open_cert,'open_erasing')
assert 'open_erasing_source_instance' not in emitted
(ROOT/'OpenCertificate.lean').write_text(header+emitted)
# Preserve an explicitly inconclusive resource outcome for a too-deep source.
deep=source0
for _ in range(2000):deep=['app',['atom',['i']],deep]
assert d.diagnose(deep)['status']=='budget_exhausted'
# Keep nominal source size exhaustion observable, even when K erases the branch.
assert d.diagnose(source0,max_nodes=1)['status']=='budget_exhausted'
(ROOT/'validation/BINDING_ATTACKS.json').write_text(json.dumps({'python_checks':'PASS','fake_q_accepted_only_with_tampered_local_q':True,'fake_q_rejected_against_original_digest':True,'expected_input_mismatch_rejected':True,'open_source_instance_omitted':True,'deep_source_resource_exhaustion':'inconclusive','kernel_negative_replays':'recorded separately in BINDING_KERNEL_RESULTS.json'},indent=2)+'\n')
print('PASS Python binding controls; two intentionally false Lean replays and one valid open conversion generated.')
