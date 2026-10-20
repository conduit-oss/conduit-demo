# conduit-demo

Public demo for the Nebius × NVIDIA hackathon: [Conduit](https://github.com/conduit-oss/conduit) (Apache-2.0) catching and fixing SDK breaks.

## What this shows

Two tiny apps on `main`:

- `summarize.py` — pinned `openai==0.28.1`, legacy `ChatCompletion.create`
- `complete.py` — pinned `anthropic==0.125.0`, legacy `client.completions.create` (removed in anthropic 1.0, Aug 2026)

Each test stubs **only the new client surface**, so tests fail before a real migration and pass after.

Open a PR that bumps one pin in `requirements.txt`. The Conduit Action diffs pins vs the base branch, runs `impact` → `apply` for each changed dependency, posts one PR comment, and pushes a verified fix commit. **Conduit never merges.**

## How the Action works

Workflow: [`.github/workflows/conduit.yml`](.github/workflows/conduit.yml)

1. Triggers on `pull_request` when requirements files change.
2. Installs Conduit from `git+https://github.com/conduit-oss/conduit.git#subdirectory=conduit`.
3. Detects which `pkg==version` pins changed vs the base branch (not hard-coded to one package).
4. For each changed pin, runs `conduit impact --dep <pkg> --from <base> --to <pr> --json`, merges the reports, then `conduit apply --impact … --write --test-cmd "python -m pytest -q"` with `CONDUIT_APPLY_MODEL=nvidia/nemotron-3-super-120b-a12b`.
5. Posts or updates a single PR comment; commits and pushes verified edits. Never merges.

## Secret

Add a repository secret named **`NEBIUS_API_KEY`** (Nebius Token Factory). If it is missing, the Action comments that fact and exits successfully. The key is never echoed.
