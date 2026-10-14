# Research Methodology

## Define the question
Write a falsifiable question, scope, non-goals, and expected deliverable before investigating source.

## Discover sources
Prefer version-matched source code and tests, official documentation, release notes/issues/pull requests/examples, then community discussion clearly labeled as secondary evidence.

## Pin versions
For each relevant upstream repository, record its URL and full commit SHA or exact tag. A default branch name alone is not a durable version pin.

## Trace implementation
Follow entry points through callers, callees, configuration, data structures, dependency boundaries, and cleanup paths. Tests clarify intended behavior but do not automatically prove runtime behavior.

## Validate
Use source inspection, static checks, unit/integration tests, or runtime reproduction as appropriate. Record what actually happened. Source-only review must not be labeled runtime-verified.

## Publish
Use the appropriate template, cite claims near the claim, run repository checks, update indexes, and list unresolved questions.
