# Minimal Runner Contract

BioPilot should start as a narrow local runner for one OpenSciFlow path, not as a general autonomous science system.

The first runner contract is:

```text
demo-run-request.json
-> workflow template validation
-> plugin manifest validation
-> readiness check
-> reviewed command rendering
-> user approval
-> execution or refusal
-> run_manifest.json
-> report
```

## Input Contract

The runner should accept a `BioPilot Demo Request` object with:

- task text;
- selected workflow template path;
- selected plugin manifest paths;
- input file records;
- run directory;
- execution mode;
- required readiness level;
- approval requirement;
- safety constraints.

See:

- `schema/biopilot-demo-request.schema.json`
- `examples/protein-md-stability/demo-run-request.json`

## Allowed First Workflow

The first runner should allow only:

```text
molecular-dynamics-stability-analysis
```

Unknown workflow names should be refused until they have explicit support.

## Refusal Before Execution

The runner should refuse before execution when:

- the demo request fails schema validation;
- the workflow template fails validation;
- a referenced plugin manifest fails validation;
- required inputs are missing;
- the selected manifest has lower readiness than `required_readiness`;
- citation, license, or limitation metadata is missing;
- command rendering would require arbitrary shell;
- user approval is required but absent.

## First Implementation Boundary

The first implementation may be review-only.

That is acceptable if it can:

- validate the request;
- validate the workflow and manifest references;
- report missing readiness evidence;
- emit a validated plan response;
- produce a planned run record;
- preserve citations, limitations, and non-claims.

## Current Planning Fixture

The current request is intentionally blocked for execution:

```text
examples/protein-md-stability/plan-response.blocked.json
```

Generate the same class of response with:

```text
python scripts/plan_demo_run.py
```
