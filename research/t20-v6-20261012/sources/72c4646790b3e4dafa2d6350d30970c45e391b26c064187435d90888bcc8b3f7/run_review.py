"""Replay this bounded review in the same pinned prerequisite workspace.
No baseline rebuild, protected repository write, or integration occurs.
"""
from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
for script in ['verify_inputs.py','verify_source_coverage.py']:
    subprocess.run([sys.executable,str(R/script)],check=True)
subprocess.run([sys.executable,str(R/'replay.py'),
    'HasEStructuralBase','HasEStructuralRename','HasEClosedWeakening',
    'ClosedChurchIdentity','EffectiveChurchIdentity','IdentityControls',
    'ClosedChurchReviewControls','ExtensionInputControls','DependencyAudit'],check=True)
