# Sample data metadata template

Use this template before promoting any candidate sample dataset to demo-ready status.

Do not commit large dataset files to git. Commit only metadata, retrieval instructions, and hashes.

## Dataset identity

```yaml
dataset_name:
dataset_version:
source_project:
source_url:
accessor_or_download_command:
retrieved_at:
retrieved_by:
```

## License and citation

```yaml
license:
license_source_url:
required_citation:
citation_source_url:
reuse_notes:
```

## Files

Record one entry per file used by the workflow.

```yaml
files:
  - role: topology
    path:
    format:
    size_bytes:
    sha256:
  - role: trajectory
    path:
    format:
    size_bytes:
    sha256:
```

If a hash is unavailable, record why:

```yaml
hash_unavailable_reason:
```

## Runtime suitability

```yaml
tested_platform:
python_version:
analysis_tool:
analysis_tool_version:
runtime_seconds:
memory_observed:
```

## Expected artifacts

```yaml
expected_artifacts:
  - metrics/rmsd.csv
  - metrics/rmsf.csv
  - metrics/rg.csv
  - report/report.md
  - run_manifest.json
```

## Claim boundary

Required text for reports using this dataset:

```text
This sample run demonstrates workflow mechanics and reproducibility metadata only. RMSD, RMSF, and radius-of-gyration outputs are descriptive trajectory metrics. They are not evidence of biological function, binding, drug efficacy, clinical meaning, or experimental validation.
```

## Review decision

```yaml
status: candidate
reviewer:
decision_date:
open_blockers:
  - license not recorded
  - citation not recorded
  - hashes not recorded
```
