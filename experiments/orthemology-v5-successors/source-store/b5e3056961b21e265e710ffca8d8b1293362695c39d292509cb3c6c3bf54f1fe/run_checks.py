"""Portable standard-library checks; synthetic inputs and supplied aggregates only."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    ['-I', '-B', '-m', 'unittest', 'discover', '-s', 'calculation', '-p', 'test_*.py', '-v'],
    ['-I', '-B', '-m', 'unittest', 'discover', '-s', 'tail', '-p', 'test_*.py', '-v'],
    ['-I', '-B', '-m', 'unittest', 'discover', '-s', 'checks', '-p', 'test_*.py', '-v'],
    ['-I', '-B', 'synthetic/check_orbits.py'],
]

def main():
    for args in COMMANDS:
        print('CHECK: python ' + ' '.join(args), flush=True)
        result = subprocess.run([sys.executable] + args, cwd=ROOT)
        if result.returncode:
            return result.returncode
    print('PASS: synthetic, aggregate-certificate and metadata checks. Raw dataset was not replayed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
