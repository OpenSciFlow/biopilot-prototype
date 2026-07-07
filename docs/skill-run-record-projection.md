# Skill Run-Record Projection

BioPilot uses a reference-app run manifest. OpenSciFlow Skill uses an agent-execution audit record.

The two records are related but not identical.

## Current Alignment Artifact

The machine-readable crosswalk currently lives in:

```text
OpenSciFlow/opensciflow-skill:data/run-record-crosswalk.biopilot-v0.1.json
```

The Skill-compatible projection fixture lives in:

```text
OpenSciFlow/opensciflow-skill:examples/biopilot-md-stability/skill-run-record.projection.json
```

## BioPilot Rule

BioPilot may emit a planned run manifest before execution.

It should not claim a completed Skill-compatible run record until the runner records:

- rendered commands;
- command source;
- return code;
- logs;
- tool versions;
- file hashes;
- license metadata;
- citations;
- limitations;
- warnings.

## Current Status

The first BioPilot sample remains review-only because MDAnalysis and MDAnalysisData are not installed in the current local readiness check.

