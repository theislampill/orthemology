"""Regression for UTF-8 metadata in a genuinely non-UTF-8 Python subprocess.

This simulates the C locale on Linux; it is not a Windows execution claim.
"""
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UTF8MetadataPortability(unittest.TestCase):
    def test_metadata_readers_under_explicit_ascii_locale(self):
        if not sys.platform.startswith('linux'):
            self.skipTest('Strict C-locale simulation is specified for Linux.')
        script = '''import codecs, locale, sys, unittest
assert sys.flags.utf8_mode == 0, "UTF-8 mode was not disabled"
assert codecs.lookup(locale.getencoding()).name == "ascii", "Locale is not ASCII"
print("LOCALE=ascii;UTF8=0", flush=True)
suite = unittest.TestSuite()
for pattern in ("test_aggregate_certificates.py", "test_source_coverage.py", "test_arabic_source_scope.py", "test_minhaj_electronic_scope.py"):
    suite.addTests(unittest.defaultTestLoader.discover("checks", pattern=pattern))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
'''
        env = dict(os.environ, LC_ALL='C', LANG='C',
                   PYTHONCOERCECLOCALE='0', PYTHONUTF8='0')
        result = subprocess.run(
            [sys.executable, '-I', '-X', 'utf8=0', '-B', '-c', script],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding='utf-8', timeout=120,
        )
        self.assertIn('LOCALE=ascii;UTF8=0', result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
