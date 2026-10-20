# conduit-demo

Public demo for the Nebius × NVIDIA hackathon: [Conduit](https://github.com/conduit-oss/conduit) (Apache-2.0) catching and fixing an OpenAI Python SDK break.

## What this shows

`main` pins `openai==0.28.1` and calls the legacy `openai.ChatCompletion.create(...)` API in `summarize.py`. Tests stub the **1.x** client surface (`OpenAI().chat.completions.create` → `.choices[0].message.content`), so they fail on the old code and pass only after a real migration.

Open a PR that bumps `openai` in `requirements.txt`. The Conduit Action runs `impact` → `apply`, posts one PR comment (impact table, apply status, diff), and pushes a verified fix commit to the PR branch. **Conduit never merges.**

## How the Action works

Workflow: [`.github/workflows/conduit.yml`](.github/workflows/conduit.yml)

1. Triggers on `pull_request` when requirements files change.
2. Installs Conduit from `git+https://github.com/conduit-oss/conduit.git#subdirectory=conduit`.
3. Reads the new `openai` pin from the PR’s `requirements.txt`.
4. Reads the base-branch `openai` pin as `--from` and the PR pin as `--to`, then runs `conduit impact --dep openai --from … --to … --json` and `conduit apply --impact … --write --test-cmd "python -m pytest -q"` with `CONDUIT_APPLY_MODEL=nvidia/nemotron-3-super-120b-a12b`.
5. Posts or updates a single PR comment; commits and pushes verified edits. Never merges.

## Secret

Add a repository secret named **`NEBIUS_API_KEY`** (Nebius Token Factory). If it is missing, the Action comments that fact and exits successfully. The key is never echoed.
