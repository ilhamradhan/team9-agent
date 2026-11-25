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
uv run team9-agent "What is the policy for payroll corrections?"
uv run team9-agent --employee-id TEST-001 "How many vacation days do I have left?"
```

Use `--mock` to test HR-document retrieval without calling DeepSeek:

```sh
uv run team9-agent --mock "How many paid days off do I get for my wedding?"
```

## Workflow

```text
Question -> classify
              ├-> personal: look up demo employee ID -> return leave balance
              └-> general: keyword retrieval -> DeepSeek answer -> source citation
                                  └-> no match: fixed fallback, no model request
```

Search compares question words with each document section and requires at least two matches. It can miss synonyms or return a weak match. HR-document citations come from the retrieved file and section, not from the model.

## Sample data and limits

`data/hr/` contains fictional policy examples. `data/demo/demo_employees.json` contains one fictional employee record, `TEST-001`. Neither file describes a real employer or person. Replace them with professor-approved documents and test records before relying on answers.

The employee ID check only selects a record from the demo JSON. It does not authenticate a person. This is a local prototype, not a deployed service or Discord integration. It has no authentication, ticketing, real employee-data access, or production retrieval database. Questions and retrieved HR policy text are sent to DeepSeek for matched general questions. Do not use confidential HR data in this prototype.
