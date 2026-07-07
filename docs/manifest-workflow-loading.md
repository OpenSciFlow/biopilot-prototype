# Manifest and workflow loading

BioPilot should load OpenSciFlow protocol artifacts before planning execution.

The first implementation is intentionally read-only:

- read the demo request JSON;
- resolve the declared workflow template path;
- resolve declared plugin manifest paths;
- parse YAML summaries;
- compare declared names and schema versions with loaded files;
- report missing or invalid artifacts;
- do not render or execute scientific commands.

## Script

Use:

```powershell
python scripts\resolve_demo_artifacts.py
```

In the local development workspace, the default workspace root is the parent directory of `biopilot-prototype`, which allows paths such as:

```text
workflow-templates/protein/md-stability-analysis.yaml
plugin-manifest/examples/mdanalysis-trajectory-analysis/opensciflow.yaml
```

To require all artifacts to exist:

```powershell
python scripts\resolve_demo_artifacts.py --strict
```

To write a checked summary:

```powershell
python scripts\resolve_demo_artifacts.py --write examples\protein-md-stability\artifact-resolution.local.json
```

## Why this stays review-only

Loading a manifest or workflow template is not execution approval.

BioPilot should still block execution until readiness evidence, input hashes, sample-data license/citation metadata, reviewed command templates, and user approval are present.
