# Run record spec

Each BioPilot run should produce a `run_manifest.json`.

## Required top-level fields

| Field | Purpose |
|---|---|
| `run_id` | Stable run identifier |
| `created_at` | ISO timestamp |
| `task_text` | Original natural-language task |
| `workflow` | Workflow template name and version |
| `plugins` | Plugin manifests used |
| `inputs` | Input file paths and hashes |
| `steps` | Ordered execution steps |
| `environment` | Tool versions and package/container info |
| `artifacts` | Registered output files and hashes |
| `citations` | Tool/model citations |
| `limitations` | Scientific and technical caveats |

## Step fields

Each step should record:

- `step_id`;
- `status`;
- `command`;
- `started_at`;
- `completed_at`;
- `exit_code`;
- `log_path`;
- `artifacts`.

## Hashing policy

- Use SHA-256 for small/medium files.
- For huge trajectories, record path, size, modification time, and optional hash if feasible.
- Never silently skip input metadata; if a hash is unavailable, record why.

## Security policy

- Commands must come from reviewed plugin manifests or fixed workflow code.
- LLM-generated shell commands are not allowed.
- Resolved paths must stay inside approved work directories.

