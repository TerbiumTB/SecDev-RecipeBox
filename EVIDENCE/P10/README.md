# P10 - SAST & Secrets Evidence

This directory contains evidence from SAST (Static Application Security Testing) and secrets scanning.

## Files

- `semgrep.sarif` - SARIF format report from Semgrep SAST scan
- `gitleaks.json` - JSON report from Gitleaks secrets detection
- `sast_summary.md` - Summary of findings and actions taken

## Tools Used

- **Semgrep**: Static analysis with community rules (`p/ci`) and custom rules (`security/semgrep/rules.yml`)
- **Gitleaks**: Secrets detection with custom configuration (`security/.gitleaks.toml`)

## Workflow

The scans are automatically run via GitHub Actions workflow: `.github/workflows/ci-sast-secrets.yml`

## Last Scan

See `sast_summary.md` for details on the latest scan results.
