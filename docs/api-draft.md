# API draft

This is a minimal API sketch for the Protein MD Stability Report Lite demo.

## Health

```text
GET /api/health
```

## Tools

```text
GET /api/tools/status
```

Returns local tool readiness:

```json
{
  "tools": [
    { "name": "mdanalysis", "status": "ready", "version": "2.x" },
    { "name": "gromacs", "status": "optional-missing" }
  ]
}
```

## Parse task

```text
POST /api/tasks/parse
```

Request:

```json
{
  "task_text": "Analyze this protein trajectory and report stability."
}
```

Response:

```json
{
  "task_type": "molecular-dynamics-stability-analysis",
  "workflow_id": "molecular-dynamics-stability-analysis",
  "confidence": "rule-match"
}
```

## Create run

```text
POST /api/runs
```

Request:

```json
{
  "task_text": "Analyze this protein trajectory and report stability.",
  "workflow_id": "molecular-dynamics-stability-analysis",
  "inputs": {
    "topology": "local:///data/demo/topology.pdb",
    "trajectory": "local:///data/demo/traj.xtc"
  },
  "execution_target": "local-agent"
}
```

## Run status

```text
GET /api/runs/{run_id}
GET /api/runs/{run_id}/logs
GET /api/runs/{run_id}/artifacts
GET /api/reports/{run_id}
```

