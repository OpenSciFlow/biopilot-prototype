from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schema" / "biopilot-demo-request.schema.json"
RESPONSE_SCHEMA = ROOT / "schema" / "biopilot-plan-response.schema.json"
DEFAULT_REQUEST = ROOT / "examples" / "protein-md-stability" / "demo-run-request.json"

READINESS_ORDER = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def readiness_blocked(actual: str, required: str) -> bool:
    return READINESS_ORDER.get(actual, -1) < READINESS_ORDER.get(required, 999)


def build_response(request: dict) -> dict:
    missing: list[str] = []
    checks: list[dict] = []
    selected_plugins: list[dict] = []

    required_readiness = request["required_readiness"]
    for plugin in request["plugin_manifests"]:
        readiness = plugin.get("readiness", "R0")
        if readiness_blocked(readiness, required_readiness):
            selected_plugins.append({
                "name": plugin["name"],
                "readiness": readiness,
                "status": "blocked",
                "reason": f"Required readiness is {required_readiness}, but the current manifest is only {readiness}."
            })
            checks.append({
                "check": "required_readiness",
                "status": "blocked",
                "detail": f"{plugin['name']} is {readiness}; request requires {required_readiness}."
            })
            missing.append(f"passing {plugin['name']} dry-run evidence")
        else:
            selected_plugins.append({
                "name": plugin["name"],
                "readiness": readiness,
                "status": "ready"
            })
            checks.append({
                "check": "required_readiness",
                "status": "pass",
                "detail": f"{plugin['name']} meets {required_readiness}."
            })

    for input_file in request["input_files"]:
        if input_file.get("required") and "sha256" not in input_file:
            checks.append({
                "check": "input_hashes",
                "status": "blocked",
                "detail": f"{input_file['name']} has no sha256: {input_file.get('hash_unavailable_reason', 'not specified')}"
            })
            missing.append(f"{input_file['name']} file hash")

    if request["execution_mode"] == "review-only":
        checks.append({
            "check": "execution_mode",
            "status": "warning",
            "detail": "Request is review-only; no execution should be attempted."
        })

    deduped_missing = list(dict.fromkeys(missing))
    status = "blocked" if deduped_missing else "planned"

    return {
        "request_id": request["request_id"],
        "status": status,
        "execution_mode": request["execution_mode"],
        "selected_workflow": request["workflow_template"],
        "selected_plugins": selected_plugins,
        "readiness_checks": checks,
        "missing_requirements": deduped_missing,
        "approval_required": request["approval_required"],
        "proposed_run_directory": request["run_directory"],
        "run_manifest_path": f"{request['run_directory']}/run_manifest.json",
        "warnings": [
            "Review-only planning response; no execution was attempted.",
            "Do not claim execution readiness until all missing requirements are resolved."
        ],
        "next_actions": [
            "Resolve missing readiness evidence before dry-run or execution.",
            "Record sample-data license, citation, size, and hashes before publishing demo artifacts.",
            "Regenerate the plan response after metadata is updated."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", nargs="?", default=str(DEFAULT_REQUEST))
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()

    request_schema = load_json(REQUEST_SCHEMA)
    response_schema = load_json(RESPONSE_SCHEMA)
    request = load_json(Path(args.request))
    jsonschema.validate(request, request_schema)

    response = build_response(request)
    jsonschema.validate(response, response_schema)
    text = json.dumps(response, indent=2)

    if args.write:
        args.write.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()

