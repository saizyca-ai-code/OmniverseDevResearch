# Precision Lighting Engine — PoC 0 L3/L4 package

**Package status:** Content-ready draft, pending GitHub PR review; no implementation or hardware test executed. Prepared 2026-10-16.

## Files
- [PRD](../../specs/OVR-PRD-0001-poc0.md) — requirements, scope and traceability
- [Technical Design](../../specs/OVR-DES-0001-poc0.md) — architecture and runtime discovery contracts
- [Implementation Handoff](../OVR-HOF-0001-poc0.md) — Coding Agent tasks, PR slices, authority
- [Acceptance](POC0-ACCEPTANCE.md) — P0-AC-01…09 and Gate 0 rules
- [Verification Plan](POC0-VERIFICATION-PLAN.md) — fixtures, test sequence, negative testing
- [Expected Manifest](expected-manifest.example.json) — example only, all results not-run
- [Handoff Reference](handoff-reference.example.yaml) — example pointer without publication SHA

## Publication and consumption

Before merging, verify ID uniqueness, metadata, version assertions, references and repository checks. The authoritative documents live here in the research repository. Once merged, the implementation repo locks the **actual merged Git SHA** in `handoff.lock.yaml`; it must not copy or synchronize these documents. See [Handoff Protocol v0.2](../../governance/research-to-implementation-handoff-protocol.md).

Do not treat these planning documents as successful Omniverse Kit/RTX runtime validation. Exact SDK commands, versions and hardware observations remain for the implementation agent to establish.
