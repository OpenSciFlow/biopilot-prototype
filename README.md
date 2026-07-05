# BioPilot Prototype

Reference prototype for local-first protein-computing workflows using OpenSciFlow manifests and workflow templates.

## Current status

Early prototype scaffold. This repository should demonstrate the first OpenSciFlow reference workflow:

> Protein MD Stability Report Lite

## MVP demo

Input:

- protein topology/structure file;
- trajectory file;
- optional ligand identifier.

Output:

- RMSD/RMSF/Rg metrics;
- plots;
- run logs;
- artifact list;
- reproducibility manifest;
- Markdown/HTML report.

## Intentionally out of scope

- General autonomous science.
- Full plugin marketplace.
- Automatic arbitrary package installation.
- Clinical or drug-development decision support.

