# Sample data policy

This repository may include demo metadata and lightweight fixtures, but it must not commit large scientific datasets by default.

## Purpose

The first BioPilot demo needs a public, reproducible molecular-dynamics trajectory so contributors can test the workflow without private data, cloud uploads, or laboratory-specific files.

## Allowed sources

Preferred sample data sources must satisfy all of the following:

- Publicly reachable from a stable archive or maintained open-source data package.
- Explicit license or reuse terms are available.
- Required citations are known before the demo is published.
- File integrity can be checked with SHA256 or equivalent checksums.
- The dataset is small enough for a first-run demo on a laptop.
- The scientific context is suitable for descriptive workflow testing.

The current preferred candidate is `MDAnalysis/MDAnalysisData`, especially an adenylate kinase equilibrium trajectory such as `fetch_adk_equilibrium()`, subject to final citation and dataset license confirmation before bundling any direct download instructions.

## Disallowed sources

Do not use:

- proprietary or collaborator-only trajectories;
- patient-derived, clinical, or personally identifying data;
- unpublished simulation data without written permission;
- datasets without clear license or citation metadata;
- very large trajectories that make the first demo slow or fragile.

## Storage rule

The default repo should store only:

- dataset metadata;
- retrieval instructions;
- expected file hashes after retrieval;
- tiny synthetic fixtures when needed for tests.

Large files should remain outside git. If a future release needs archived demo inputs, publish them as a separate release asset or external dataset with explicit checksums and license text.

## Provenance fields

Every sample dataset used by the MVP must record:

- source URL or package name;
- exact accessor or download command;
- upstream license;
- required citation;
- retrieval date;
- file names;
- file sizes;
- SHA256 hashes;
- any preprocessing steps.

Use the metadata template before marking a dataset demo-ready:

```text
examples/protein-md-stability/sample-data-metadata-template.md
```

## Claim boundary

Sample-data results are workflow demonstrations only. They must not be presented as new biological findings, drug-discovery evidence, clinical evidence, or benchmark superiority claims.
