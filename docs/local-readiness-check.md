# Local readiness check

BioPilot should distinguish between:

- metadata that has been reviewed;
- a local environment that can run a dry run;
- a smoke test that produces artifacts;
- a full run that produces a validated run record.

The helper script:

```powershell
python scripts\check_local_readiness.py
```

prints a JSON report with:

- check timestamp;
- Python version and executable;
- OS and machine architecture;
- whether key packages are installed;
- package versions where available.

## Current use

Use this script before claiming a local environment is ready for:

- `mdanalysis-trajectory-analysis` R3 dry-run evidence;
- BioPilot `Protein MD Stability Report Lite`;
- sample-data retrieval with `MDAnalysisData`.

## Non-goals

The script does not install packages, download datasets, or execute scientific analysis.

It is an environment inspection step only.
