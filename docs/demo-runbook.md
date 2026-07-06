# MVP demo runbook

MVP:

> Protein MD Stability Report Lite

## Demo objective

Show that BioPilot can map a natural-language request to a reviewed workflow template, run a local trajectory-analysis plugin, collect reproducibility metadata, and render a report.

## Pre-demo checklist

- `workflow-templates` contains `molecular-dynamics-stability-analysis`.
- `plugin-manifest` contains a reviewed `mdanalysis-trajectory-analysis` example.
- The compliance stages in `docs/protocol-compliance-plan.md` are satisfied up to the requested demo level.
- A public sample dataset has passed `examples/protein-md-stability/sample-data-checklist.md`.
- Local environment has Python, MDAnalysis, NumPy, pandas, matplotlib, and Jinja2.
- The demo machine has no requirement to upload input files.

## Happy path

1. User enters:

   ```text
   Analyze this protein trajectory and report RMSD, RMSF, radius of gyration, warnings, and reproducibility metadata.
   ```

2. Planner selects:

   ```text
   molecular-dynamics-stability-analysis
   ```

3. Readiness check reports:

   ```text
   MDAnalysis: available
   plotting stack: available
   sample dataset: available
   output directory: writable
   ```

4. Runner creates:

   ```text
   runs/demo-md-stability-001/
   ```

5. Runner produces:

   ```text
   metrics/rmsd.csv
   metrics/rmsf.csv
   metrics/rg.csv
   plots/rmsd.png
   plots/rmsf.png
   plots/rg.png
   report/report.md
   report/report.html
   run_manifest.json
   logs/execution.log
   ```

6. Report contains:

   - methods;
   - input provenance;
   - plots;
   - warnings;
   - citations;
   - limitations;
   - reproducibility metadata.

## Failure cases to demonstrate

- Missing trajectory file: stop before execution and show a clear input error.
- Missing MDAnalysis: stop before execution and show install guidance without auto-installing arbitrary packages.
- Unknown task: refuse to invent a new workflow and ask the user to select a supported template.
- Large input: warn before execution and require explicit user confirmation.

## Acceptance evidence

The first public demo should attach:

- screenshot of the task entry and readiness check;
- screenshot or exported HTML report;
- `run_manifest.json`;
- `logs/execution.log`;
- checksums for input files and generated artifacts.

## Out of scope

- Full molecular-dynamics simulation.
- Model-based scientific hypothesis generation.
- Cloud execution.
- Automatic arbitrary package installation.
- Clinical or drug-development interpretation.
