import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
schema=json.loads(Path(sys.argv[1]).read_text())
value=json.loads(Path(sys.argv[2]).read_text())
Draft202012Validator.check_schema(schema)
errors=[{"path":list(e.absolute_path),"schema_path":list(e.absolute_schema_path),"message":e.message} for e in Draft202012Validator(schema).iter_errors(value)]
print(json.dumps(errors,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
