from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from tests.support import BoundaryCase, ROOT, REFERENCE

class DependencyTests(BoundaryCase):
    def test_pins_match_frozen_sources(self):
        api=self.module('dependencies')
        self.assertEqual(set(api.verify_dependencies()), {'model','finite','certificates','synthesis','controller'})
        self.assertEqual(api.validate_model.__module__, 'model')
        self.assertEqual(api.shortest_route.__module__, 'synthesis')

    def test_dependency_tampering_fails_closed_before_import(self):
        self.module('dependencies')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/'efficient-v1').mkdir(); (root/'reference-v1').mkdir()
            shutil.copy2(ROOT/'dependencies.py',root/'efficient-v1'/'dependencies.py')
            for name in ('model','finite','certificates','synthesis','controller'):
                shutil.copy2(REFERENCE/(name+'.py'),root/'reference-v1'/(name+'.py'))
            with (root/'reference-v1'/'model.py').open('a') as out: out.write('\n# changed\n')
            run=subprocess.run([sys.executable,'-B','-c','import dependencies'],cwd=root/'efficient-v1',capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertIn('frozen reference hash mismatch: model.py',run.stderr)
