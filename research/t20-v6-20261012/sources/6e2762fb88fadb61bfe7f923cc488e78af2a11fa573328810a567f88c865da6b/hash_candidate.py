#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
paths=sorted(set(root.glob('*.lean')) | set(root.glob('*.sh')) | set(root.glob('*.py')) |
             set((root/'tests').glob('*.lean')) | {root/'SOURCE_BINDING.json'})
print(json.dumps([{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                  'size':p.stat().st_size} for p in paths],indent=2))
