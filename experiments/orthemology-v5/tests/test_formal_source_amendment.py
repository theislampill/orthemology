"""Owner finite source/target boundary controls; no theorem proof credit."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
REGIONS = {'lean/EffectsAndDependence.lean': ['red_trans'], 'lean/BoundaryResults.lean': ['replace_free'], 'lean/AlmostSureBoundary.lean': ['no_atomless_full_intersection'], 'lean/OperationalKernel.lean': ['ticket_good', 'all_open_execute']}
EXPECTED_SURFACES = {'lean/EffectsAndDependence.lean': '4fee0679ef1b63781b5545212e5d949b4ddcd658371c2c860c400bbd2638fa51', 'lean/BoundaryResults.lean': 'c0beb83c0b401e71d6903edaf83b1c4a7e5abec727235e4154a2b17bab002e6a', 'lean/AlmostSureBoundary.lean': '7f1b338ac29d882cec83870a38d82409fdf727a49f967ce808f850a5e563be27', 'lean/OperationalKernel.lean': '240a1e020bb68f2a0276c67e1b27279b1aec77a40030bef37ae57bd84a561620'}
UNCHANGED = {'verify.py': '318c67e2f874a9e1e951fed9aed4a9ab0a1de55670e53c78c403810d6932b87e', 'formal_targets.json': '751c4bac319035dff1fda364e0bc3466efcd7b198889de4f50bf148afb448ab2', 'lean-toolchain': '55e97be96000b5e9e290c9e74482e5e317861499a5540353ce845471bded8cea', 'lean/NormalisationAndNumerals.lean': '13c3b0ba7aa7e57fd13bf1d61d28ef842755d5f5103ef9598d18cc885f4e2ca2', 'lean/HurkensBoundary.lean': '4c1d8a9d8a9a6ebec9f5e1a1ee41008b75fbfffeabbbd9ee489ea21982425a08', 'lean/InternalPolymorphism.lean': '7cf85525305944e343b50f63e9b593a0fdcab3c89303f2f32cdb37d92c70b1ee', 'lean/GeneratedExamples.lean': '0f8e551de28b6bdf549e0d2ecba0932bb2758b8ff57aaf5f1cf5956d7d88d8cd', 'lean/AuditSupport.lean': 'f3e08557b57a745bae547dc827755616cd6c6824bf1360441a72789036e1cd96', 'lean/RelationalFragment.lean': '12dfbed26b887067f2bbd2a75930d038558b3a5c715100d7c25d3cfee79a7fdb', 'lean/FiniteBridge.lean': 'f75306d1a29cd76385058ca1a819910b1f635a63369d807d484ab6db981a0042', 'tests/test_reference.py': '222b0289436211fb9a865e6a7f5ac6621d6683f4d5515fcc2821471bb5e08a53', 'tests/test_observation_revision.py': 'a881ade3622dc84944cfab2e354016910590f55b09e7235abf7def4a5ce23fcc', 'tests/test_ticket_collision.py': '6d4942620a8d6b9e5dcfbcc239334b7d5147ce2f986b169899fb389886f49b72', 'tests/test_legacy_mutation_integrity.py': 'face065505bc935c74ad2a06ce3ed1cfad5f00268a4b2d01dec4a60043c0c4e9', 'tests/test_guarded_sampler.py': 'f5b547fa9b986e7f0e4a45fd329b0e6907948cc3097eb4e45a48f735ffcbab85', 'tests/test_generated_examples.py': 'e55bc17380a07e2f53b578087e1dfb0988aedb33ad13891a8d166843de1429ae', 'tests/test_productive_observer.py': '7d4deafd2030f5933ab31655698ce4392a302c73d297f56b830bb56b1888db9b', 'tests/test_v4_regressions.py': '7e784a3e80587f3d74cb3476829fdff501ceaed67b6da6ed0b3470fce07f9e80', 'tests/test_proof_export.py': '65f8954be7d13500c8d1a93f15783eb2a58548ff4de23f84685a61af987a16a6', 'tests/test_revision_transport.py': '0e8e95cc3b45a8c15a3157e1bcf1b9bcc1e2301a0c57242749b64668d04ca2ae', 'tests/test_final_boundaries.py': 'a47cc9c4aee4976df928fa4d2c6b98afddaaeb8161470309fd12ed4b9c88c3c2', 'tests/test_v4_resources.py': 'ef20ad5442f1fcaef45e62031b228ebd39d17e9d4d3591ea4b6f67b4ce1b9fde', 'tests/test_extensions.py': 'd746a396c6bc86f1a1a4353cac954f449b50b5ab790b2a3ad1277db6d7621160', 'tests/test_operational.py': '3b6ed664d3e88352ceba2f33aa6e1c28607fff120624c6962c5170add4d2d0cd', 'tests/test_build_gate.py': '6566924496965164ad815bc7d9cf754bf835f19a314275e898e20a8563458093', 'tests/test_required_audit.py': '627ece3600e1b0e624b79a76884fd0c4137f148916001ae3e0b7903786208e4c', 'tests/test_reflective_sampler.py': 'efec28dcf92c12e4d08c2f2f88beba51ddc7383ca1c38b7e0bf8b824dda4684d'}

def protected_surface(text, declarations):
    for declaration in declarations:
        expression = r'(?ms)^theorem ' + re.escape(declaration) + r'\b(.*?)(?=^theorem |^def |^/--|^end |\Z)'
        found = list(re.finditer(expression, text))
        if len(found) != 1: raise ValueError('declaration occurrence changed')
        match = found[0]; chunk = match.group(0)
        signature, separator, proof = chunk.partition(':=')
        if not separator: raise ValueError('missing declaration definition')
        if declaration == 'no_atomless_full_intersection':
            signature = re.sub(r'\bomitPoint\b', 'omit', signature)
        text = text[:match.start()] + signature + ':= <OWNER-AUTHORISED-PROOF-REGION>\n\n' + text[match.end():]
    return text


class FormalSourceAmendmentTests(unittest.TestCase):
    def test_protected_signatures_and_outside_regions(self):
        for rel, declarations in REGIONS.items():
            value = protected_surface((SOURCE / rel).read_text(), declarations)
            self.assertEqual(hashlib.sha256(value.encode()).hexdigest(), EXPECTED_SURFACES[rel], rel)

    def test_unchanged_reference_population_and_formal_owners(self):
        for rel, expected in UNCHANGED.items():
            self.assertEqual(hashlib.sha256((SOURCE / rel).read_bytes()).hexdigest(), expected, rel)

    def test_scuuat_extension_is_only_identifier_quoting(self):
        text = (SOURCE / 'lean/OperationalBoundary.lean').read_text()
        self.assertEqual(text.count('«at»'), 5)
        original = text.replace('«at»', 'at')
        expected = 'd72ea2871daf63836f72bf87aba02877c3d4a7324ed53bb32b659a30bcb36027'
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), expected)
        for changed in [original.replace('at : O.State', 'at : Type', 1),
                        original.replace('returnedBeta :', 'changedBeta :', 1)]:
            self.assertNotEqual(hashlib.sha256(changed.encode()).hexdigest(), expected)

    def test_all_twelve_modules_and_145_targets_retained(self):
        contract = json.loads((SOURCE / 'formal_targets.json').read_text())
        self.assertEqual(len(contract['modules']), 12)
        self.assertEqual(len([n for row in contract['modules'] for n in row['targets']]), 145)
        self.assertEqual({x.stem for x in (SOURCE / 'lean').glob('*.lean')}, {x['name'] for x in contract['modules']})

    def test_signature_and_global_definition_tamper_detected(self):
        rel = 'lean/OperationalKernel.lean'; text = (SOURCE / rel).read_text()
        for bad in [text.replace('Good g (ticket g p)', 'True', 1), text.replace('def ticket ', 'def changedTicket ', 1)]:
            self.assertNotEqual(hashlib.sha256(protected_surface(bad, REGIONS[rel]).encode()).hexdigest(), EXPECTED_SURFACES[rel])


if __name__ == '__main__': unittest.main()
