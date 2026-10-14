# Evidence Policy

## Evidence labels
- A — direct: directly supported by a pinned source file, test, configuration, or official document.
- B — cross-checked: corroborated by independent relevant evidence, such as implementation plus tests.
- C — inference: plausible and evidence-informed but not directly established.
- U — unknown: insufficient evidence or inaccessible implementation.

These labels describe evidence basis, not statistical confidence.

## Validation states
Use explicit labels: source-inspected, static-checked, test-executed, runtime-verified, or not-verified. Never imply a stronger state than the work performed.

## Citation minimum
For material implementation claims, provide the upstream repository URL, pinned commit/tag, file path and symbol or line range, and a commit-pinned permalink where available. Include symbol names because line numbers can change.

## Conflicts
When documentation, tests, and implementation disagree, record the discrepancy and version rather than silently choosing one.
