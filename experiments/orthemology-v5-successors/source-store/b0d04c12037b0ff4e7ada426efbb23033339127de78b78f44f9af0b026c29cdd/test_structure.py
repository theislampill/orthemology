"""Structural proof obligations; counts corroborate rather than prove complexity."""
import ast
from pathlib import Path
from unittest.mock import patch
from tests.support import BoundaryCase, ROOT, graph_model


class StructureTests(BoundaryCase):
    def test_mec_work_items_have_binary_partition_bound(self):
        api=self.module('mec')
        m=graph_model([[[0,'1/2','1/2'],[1,0,0]],[[1,0,0],[0,1,0]],[[0,0,1],[0,0,1]]])
        pairs=tuple((s,a) for s in range(3) for a in range(2))
        with patch.object(api,'_strongly_connected',wraps=api._strongly_connected) as count:
            api.maximal_components(m,0,pairs)
            self.assertEqual(count.call_count,5)
            self.assertLessEqual(count.call_count,2*m.n_states-1)

    def test_threshold_call_bounds_use_full_pair_carrier(self):
        api=self.module('efficient')
        m=graph_model([[[1],[1],[1]]],priorities=[[[2,4,6]],[[6,4,2]]])
        pairs=((0,0),(0,1),(0,2)); carrier=m.n_states*m.n_actions
        with patch.object(api,'maximal_components',wraps=api.maximal_components) as count:
            api.known_components(m,pairs)
            self.assertEqual(count.call_count,carrier)
        with patch.object(api,'maximal_components',wraps=api.maximal_components) as count:
            result=api.uncertain_components(m,0,pairs)
            self.assertEqual(count.call_count,carrier+carrier**2)
            self.assertLessEqual(len(result),m.n_states*(carrier+carrier**2))

    def test_no_forbidden_production_call_or_import_names(self):
        forbidden={'all_components','combinations','powerset'}
        for name in ('mec','efficient','negative'):
            tree=ast.parse((ROOT/(name+'.py')).read_text())
            identifiers={node.id for node in ast.walk(tree) if isinstance(node,ast.Name)}
            attributes={node.attr for node in ast.walk(tree) if isinstance(node,ast.Attribute)}
            self.assertFalse((identifiers|attributes)&forbidden,name)
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn(node.module,('synthesis','certificates','finite'),name)

    def test_dependency_adapter_exports_only_approved_reference_bindings(self):
        tree=ast.parse((ROOT/'dependencies.py').read_text())
        allowed={'_model':{'Model','validate_model','natural'},
                 '_finite':{'checked_pairs','checked_region','safe_known','safe_uncertain','used'},
                 '_certificates':{'Positive','Negative','Route','check_positive','record','sequence','canonical'},
                 '_synthesis':{'shortest_route'}}
        for node in ast.walk(tree):
            if isinstance(node,ast.Attribute) and isinstance(node.value,ast.Name) and node.value.id in allowed:
                self.assertIn(node.attr,allowed[node.value.id])

    def test_scc_and_mec_are_nonrecursive(self):
        tree=ast.parse((ROOT/'mec.py').read_text())
        for function in (node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)):
            self.assertFalse(any(isinstance(node,ast.Call) and isinstance(node.func,ast.Name)
                                 and node.func.id==function.name for node in ast.walk(function)))
