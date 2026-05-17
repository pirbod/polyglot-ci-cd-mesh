# Supply-Chain Evidence

The local demo generates deterministic evidence with `scripts/generate_demo_data.py`. The production workflow uses SBOM generation, filesystem scanning, provenance attestation, and image signing evidence.

Default behavior is safe and local:

- SBOM report: `evidence/sbom-report.json`
- Scan report: `evidence/scan-report.json`
- Security evidence: `evidence/security-evidence.json`
- Release signing: simulated locally and ready to replace with real keyless signing in protected release jobs
