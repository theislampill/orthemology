#!/usr/bin/env python3
"""Generate concrete certificates from the literal Lean export; never type labels."""
import json
from pathlib import Path
import diagnostic as d
ROOT = Path(__file__).resolve().parent
cases = [('numeral_' + str(k), n) for k,n in enumerate(d.SOURCE['numerals'])]
cases += [('packed_3', ['atom', d.pack_closed(d.SOURCE['numerals'][3])]),
          ('wrapped_4', ['app', ['atom', ['i']], d.SOURCE['numerals'][4]]),
          ('erasing_omega_2', ['app', ['app', ['atom', ['k']], d.SOURCE['numerals'][2]], ['atom', d.SOURCE['omega']]])]
text = ('import LiteralSourceQ\nset_option maxRecDepth 32768\n'
        'set_option maxHeartbeats 0\nnamespace ConcreteScalarCertificates\n'
        'theorem exact_q_export : (' + d.lean_poly(d.ORIGINAL_Q) + ' : P01D.Poly) = FullPER.Application.originalQ := ScalarCertificates.originalQ_expanded.symm\n')
summaries=[]
for name,n in cases:
    result = d.diagnose(n,max_nodes=5000000)
    assert result['status'] == 'certified_conversion', result
    cert=result['certificate']
    (ROOT/'validation'/f'{name}.json').write_text(json.dumps(cert,indent=2)+'\n')
    text+=d.lean_certificate(cert,name)+'\n'
    if name.startswith('numeral_'):
        text+=f'theorem {name}_input_binding : {name}_n = P01AC.EffectiveCompleteness.inputNumeral {name[8:]} := by\n  simp [{name}_n, P01AC.EffectiveCompleteness.inputNumeral, P01AC.EffectiveCompleteness.iterationPoly, P01D.abstract, P01D.freeZero, P01D.drop, P01D.pren, P01D.psub]\n'
    if name=='erasing_omega_2':
        text+='theorem erased_input_binding : erasing_omega_2_n = ScalarCertificates.erasingOmegaNumeral 2 := by\n  simp [erasing_omega_2_n, ScalarCertificates.erasingOmegaNumeral, P01AC.EffectiveCompleteness.inputNumeral, P01AC.EffectiveCompleteness.iterationPoly, P01D.abstract, P01D.freeZero, P01D.drop, P01D.pren, P01D.psub, OrthemologyV3.omega, OrthemologyV3.duplicator]\n'
    summaries.append({'case':name,'count':cert['count'],'steps':[cert[k]['steps'] for k in ['left','right']],
                      'complete_development_rounds':result['complete_development_rounds']})
text+='end ConcreteScalarCertificates\n'
(ROOT/'ConcreteScalarCertificates.lean').write_text(text)
(ROOT/'validation'/'CONCRETE_SUMMARY.json').write_text(json.dumps(summaries,indent=2)+'\n')
print(json.dumps(summaries,indent=2))

# A scopedness-negative control still permits concrete source conversion.
open_input = ['app', ['app', ['atom', ['k']], d.SOURCE['numerals'][0]], ['var', 42]]
open_result = d.diagnose(open_input)
open_output = 'import LiteralSourceQ\nset_option maxRecDepth 32768\nset_option maxHeartbeats 8000000\n' + d.lean_certificate(open_result['certificate'], 'open_erased')
assert '_source_instance' not in open_output
(ROOT/'OpenCertificateControl.lean').write_text(open_output)
