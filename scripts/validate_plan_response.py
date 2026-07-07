from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "biopilot-plan-response.schema.json"
DEFAULT_RESPONSE = ROOT / "examples" / "protein-md-stability" / "plan-response.blocked.json"


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RESPONSE
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    data = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    print(f"Validated BioPilot plan response: {path}")


if __name__ == "__main__":
    main()

