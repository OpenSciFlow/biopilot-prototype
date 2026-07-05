# MVP acceptance criteria

MVP name:

> Protein MD Stability Report Lite

## User story

A researcher provides a protein topology/structure file and an existing trajectory. They describe the task in natural language. BioPilot selects a fixed OpenSciFlow workflow template, checks local tools, runs trajectory analysis, streams logs, collects artifacts, and generates a report with reproducibility metadata.

## Must work

- The launcher accepts a natural-language task.
- The task maps to `molecular-dynamics-stability-analysis`.
- Tool readiness shows at least:
  - MDAnalysis or MDTraj;
  - optional GROMACS;
  - Python plotting stack.
- The run creates a stable run directory.
- Logs are captured.
- Artifacts are registered.
- The report includes:
  - input summary;
  - methods;
  - RMSD/RMSF/Rg plots;
  - warnings;
  - citations;
  - limitations;
  - reproducibility metadata.

## Expected artifacts

```text
runs/{run_id}/
  inputs_manifest.json
  run_manifest.json
  logs/execution.log
  metrics/rmsd.csv
  metrics/rmsf.csv
  metrics/rg.csv
  plots/rmsd.png
  plots/rmsf.png
  plots/rg.png
  report/report.md
  report/report.html
```

## Definition of done

- One sample trajectory can be analyzed end to end.
- The same input produces the same artifact filenames.
- The run manifest records input hashes, commands, tool versions, and timestamps.
- The report avoids claiming biological binding, drug efficacy, or clinical meaning.

## Explicit non-goals

- No full MD simulation in the first demo.
- No automatic arbitrary package installation.
- No cloud upload by default.
- No general autonomous science planning.
- No clinical or drug-development decision support.

