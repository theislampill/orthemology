import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'tools'))
import check_ir_instance_integrity as ir
root=Path(__file__).resolve().parent
value=json.loads(Path(sys.argv[1]).read_text())
schema=ir.load_json(root/'atomics/skill/references/diagnostics/diagnostic-ir.schema.json')
errors=ir.validate_instance('repair probe',value,schema,ir.load_catalogue(root),ir.load_compiled_modules(root))
print(json.dumps(errors,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
