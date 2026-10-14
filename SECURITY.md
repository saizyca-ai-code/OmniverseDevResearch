# Security and Sensitive Data

Do not store access tokens, passwords, private keys, personal data, internal-only source code, or proprietary material without explicit authorization.

If a secret is committed accidentally, revoke or rotate it immediately, notify the repository owner, remove it from the current tree, and assess whether Git history must be rewritten. Deleting a file from the latest commit does not make a leaked secret safe.

Use GitHub Actions secrets or an approved secret manager for CI credentials. Never echo secrets into logs.
