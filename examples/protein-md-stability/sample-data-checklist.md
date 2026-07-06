# Sample data checklist

Candidate:

```text
MDAnalysisData adk_equilibrium
```

Upstream:

```text
https://github.com/MDAnalysis/MDAnalysisData
```

## Gate 1: source status

- [x] Source repository exists.
- [x] Source repository is not archived.
- [x] Source package describes stable external data URLs.
- [x] Source package describes checksum validation.
- [ ] Exact dataset license recorded from dataset metadata.
- [ ] Exact citation recorded from dataset metadata.

## Gate 2: technical suitability

- [ ] Topology file path available.
- [ ] Trajectory file path available.
- [ ] File sizes recorded.
- [ ] SHA256 hashes recorded after download.
- [ ] Analysis runs in less than 5 minutes on a laptop.
- [ ] Generated artifact filenames match `docs/mvp-acceptance-criteria.md`.

## Gate 3: scientific claim boundary

- [ ] Report states that RMSD, RMSF, and radius of gyration are descriptive metrics.
- [ ] Report avoids binding, efficacy, clinical, or drug-development claims.
- [ ] Report includes warnings about trajectory length and sampling limitations.

## Gate 4: release readiness

- [ ] Retrieval command documented.
- [ ] Cache directory documented.
- [ ] Upstream license and citations included in the report.
- [ ] Dataset provenance included in `run_manifest.json`.
- [ ] No large dataset files committed to git.

## Current decision

Use this dataset only after the unchecked items above are resolved. Until then, documentation may refer to it as a preferred candidate, not as a finalized bundled dataset.

Metadata should be recorded with:

- `examples/protein-md-stability/sample-data-metadata-template.md`
