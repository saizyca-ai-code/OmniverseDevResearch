# GitHub Setup Checklist

1. Connect the intended GitHub account through the supported integration.
2. Grant access to this artifact repository first; expand scope only when needed.
3. Prefer read-only access for research-only work. Enable write access only for needed and supported operations.
4. Verify access with a harmless read before any write.
5. Prefer feature branches and pull requests over direct pushes to main.

## Repository settings
- Keep main as the default branch.
- Configure branch protection or a ruleset for main.
- Require the Research quality workflow to pass before merge.
- Disable force pushes and branch deletion on main.
- Enable secret scanning and push protection if available.
- Add CODEOWNERS if ownership becomes shared.

A URL in project instructions does not grant access by itself. Direct operations require a connected integration with appropriate repository selection and permissions. Never store personal access tokens in the repository or chat instructions.
