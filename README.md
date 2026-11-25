# Team 9 HR agent prototype

A small LangGraph workflow that retrieves a matching section from fictional HR documents and returns it with a source citation. The answer step is deterministic for now. It does not call an LLM.

## Run

Requires Python 3.11 or newer and `uv`.

```sh
uv sync --extra dev
uv run pytest
uv run team9-agent "How many paid days off do I get for my wedding?"
```

Try an unsupported topic to see the fallback:

```sh
uv run team9-agent "What is the policy for payroll corrections?"
```

## Workflow

```text
Question -> retrieve matching document section -> return answer with source
                                      └-> no match: say the documents do not cover it
```

The prototype uses simple keyword overlap because the sample corpus is tiny. It cites the filename and section, and abstains when it cannot find a sufficiently strong match. Replace the deterministic answer step with a model only after the team chooses an inference provider.

## Sample data

`data/hr/` contains fictional examples for local testing. They are not real policies, legal guidance, or employee records. Replace them with professor-approved documents before relying on answers.

## Scope

This is a local workflow prototype, not a deployed service or a Discord integration. It has no real employee-data access, authentication, ticketing, or production retrieval database. Keep secrets and real employee data out of Git.
