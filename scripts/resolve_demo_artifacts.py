from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schema" / "biopilot-demo-request.schema.json"
RESOLUTION_SCHEMA = ROOT / "schema" / "biopilot-artifact-resolution.schema.json"
DEFAULT_REQUEST = ROOT / "examples" / "protein-md-stability" / "demo-run-request.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to a YAML object")
    return data


def safe_workspace_path(workspace_root: Path, declared_path: str) -> Path:
    root = workspace_root.resolve()
    target = (root / declared_path).resolve()
    target.relative_to(root)
    return target


def summarize_workflow(data: dict[str, Any]) -> dict[str, Any]:
    steps = data.get("steps", [])
    plugins = data.get("plugins", {})
    dag = data.get("dag", {})

    return {
        "inputs": len(data.get("inputs", [])),
        "outputs": len(data.get("outputs", [])),
        "steps": len(steps) if isinstance(steps, list) else 0,
        "dag_nodes": len(dag) if isinstance(dag, dict) else 0,
        "required_plugins": plugins.get("required", []) if isinstance(plugins, dict) else [],
        "optional_plugins": plugins.get("optional", []) if isinstance(plugins, dict) else [],
        "report_template": data.get("report_template"),
        "records_input_hashes": data.get("reproducibility", {}).get("record_inputs_hash"),
        "records_tool_versions": data.get("reproducibility", {}).get("record_tool_versions"),
        "records_commands": data.get("reproducibility", {}).get("record_commands")
    }


def summarize_manifest(data: dict[str, Any]) -> dict[str, Any]:
    execution = data.get("execution", {})
    local_execution = execution.get("local", {}) if isinstance(execution, dict) else {}
    slurm_execution = execution.get("slurm", {}) if isinstance(execution, dict) else {}
    model_weights = data.get("model_weights", {})
    validation = data.get("validation", {})

    return {
        "domain": data.get("domain", []),
        "task_types": data.get("task_types", []),
        "inputs": len(data.get("inputs", [])),
        "outputs": len(data.get("outputs", [])),
        "local_command_keys": sorted([
            key for key, value in local_execution.items()
            if "command" in key and isinstance(value, str)
        ]) if isinstance(local_execution, dict) else [],
        "slurm_supported": slurm_execution.get("supported") if isinstance(slurm_execution, dict) else None,
        "model_weights_required": model_weights.get("required") if isinstance(model_weights, dict) else None,
        "dry_run_command": validation.get("dry_run_command") if isinstance(validation, dict) else None,
        "citation": data.get("citation", {}).get("preferred") if isinstance(data.get("citation"), dict) else None,
        "license": data.get("license", {}) if isinstance(data.get("license"), dict) else {}
    }


def resolve_artifact(kind: str, declared: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    declared_name = declared["name"]
    declared_path = declared["path"]
    declared_schema = declared["schema_version"]
    warnings: list[str] = []

    artifact = {
        "kind": kind,
        "declared_name": declared_name,
        "declared_path": declared_path,
        "declared_schema_version": declared_schema,
        "status": "missing",
        "loaded_name": None,
        "loaded_schema_version": None,
        "summary": {},
        "warnings": warnings
    }

    try:
        path = safe_workspace_path(workspace_root, declared_path)
    except ValueError:
        artifact["status"] = "invalid"
        warnings.append("Declared path resolves outside the workspace root.")
        return artifact

    if not path.exists():
        warnings.append("Declared artifact path does not exist in the selected workspace root.")
        return artifact

    try:
        data = load_yaml(path)
    except Exception as exc:  # noqa: BLE001 - preserve parser reason in review output.
        artifact["status"] = "invalid"
        warnings.append(f"Could not parse YAML: {exc}")
        return artifact

    loaded_name = data.get("workflow_name") if kind == "workflow_template" else data.get("name")
    loaded_schema = data.get("schema_version")

    artifact["status"] = "loaded"
    artifact["loaded_name"] = loaded_name
    artifact["loaded_schema_version"] = loaded_schema
    artifact["summary"] = summarize_workflow(data) if kind == "workflow_template" else summarize_manifest(data)

    if loaded_name != declared_name:
        warnings.append(f"Declared name {declared_name!r} differs from loaded name {loaded_name!r}.")
    if loaded_schema != declared_schema:
        warnings.append(f"Declared schema {declared_schema!r} differs from loaded schema {loaded_schema!r}.")

    return artifact


def build_resolution(request: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    workflow = resolve_artifact("workflow_template", request["workflow_template"], workspace_root)
    plugins = [
        resolve_artifact("plugin_manifest", plugin, workspace_root)
        for plugin in request["plugin_manifests"]
    ]

    artifacts = [workflow, *plugins]
    missing = [
        artifact["declared_path"]
        for artifact in artifacts
        if artifact["status"] != "loaded"
    ]
    warnings = [
        f"{artifact['declared_path']}: {warning}"
        for artifact in artifacts
        for warning in artifact.get("warnings", [])
    ]

    if not missing:
        status = "resolved"
    elif len(missing) == len(artifacts):
        status = "missing"
    else:
        status = "partial"

    return {
        "request_id": request["request_id"],
        "workspace_root_policy": "Resolve request paths relative to a reviewed OpenSciFlow workspace root; default local development root is the parent directory of biopilot-prototype.",
        "status": status,
        "workflow_template": workflow,
        "plugin_manifests": plugins,
        "missing_artifacts": missing,
        "warnings": warnings
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", nargs="?", default=str(DEFAULT_REQUEST))
    parser.add_argument("--workspace-root", type=Path, default=ROOT.parent)
    parser.add_argument("--write", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    request_schema = load_json(REQUEST_SCHEMA)
    resolution_schema = load_json(RESOLUTION_SCHEMA)
    request = load_json(Path(args.request))
    jsonschema.validate(request, request_schema)

    resolution = build_resolution(request, args.workspace_root)
    jsonschema.validate(resolution, resolution_schema)

    if args.strict and resolution["status"] != "resolved":
        raise SystemExit("Artifact resolution did not resolve all declared artifacts")

    text = json.dumps(resolution, indent=2)
    if args.write:
        args.write.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
