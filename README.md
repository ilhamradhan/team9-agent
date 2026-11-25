# Team 9 HR agent prototype

This LangGraph app searches sample HR policies and sends a matching section to DeepSeek for a short answer. The app attaches the source citation after generation. If retrieval finds no match, it returns a fixed fallback without calling the model.

## Setup

Requires Python 3.11 or newer and `uv`.

```sh
uv sync --extra dev
cp .env.example .env
```

Add your DeepSeek API key to `.env` as `DEEPSEEK_API_KEY=...`. The file is ignored by Git.

## Run

```sh
uv run pytest
uv run team9-agent "How many paid days off do I get for my wedding?"
```

Use `--mock` to test retrieval without calling DeepSeek:

```sh
uv run team9-agent --mock "How many paid days off do I get for my wedding?"
```

## Workflow

```text
Question -> keyword retrieval -> DeepSeek answer -> source citation
                   └-> no match: fixed fallback, no model request
```

Search compares question words with each document section and requires at least two matches. It can miss synonyms or return a weak match. The citation comes from the retrieved file and section, not from the model.

## Sample data and limits

`data/hr/` contains fictional examples for local testing. They do not describe a real employer or provide legal guidance. Replace them with professor-approved documents before relying on answers.

This is a local prototype, not a deployed service or Discord integration. It has no authentication, ticketing, personal employee data, or production retrieval database. Questions and retrieved policy text are sent to DeepSeek for matched queries. Do not use confidential HR data in this prototype.
