from __future__ import annotations

import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "opensciflow-run-record.schema.json"
EXAMPLES_DIR = ROOT / "examples"


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    files = sorted(EXAMPLES_DIR.glob("*/sample-run-manifest.json"))
    if not files:
        raise SystemExit("No sample run records found")

    errors: list[str] = []
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            jsonschema.validate(data, schema)
        except Exception as exc:  # noqa: BLE001 - report validation failures clearly.
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        raise SystemExit("\n".join(errors))

    print(f"Validated {len(files)} run records")


if __name__ == "__main__":
    main()
