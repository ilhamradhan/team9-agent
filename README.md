# Team 9 HR agent prototype

This prototype runs two LangGraph steps. It searches the sample HR policies, then returns the matching text with a file-and-section citation. It uses a fixed answer template and does not call an LLM.

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

Search compares words in the question with each document section. It returns a match only when at least two words overlap, then cites that section. This simple method can miss synonyms or return a weak match. The answer uses a fixed template, not an LLM.

## Sample data

`data/hr/` contains fictional examples for local testing. They are not real policies, legal guidance, or employee records. Replace them with professor-approved documents before relying on answers.

## Scope

This is a local workflow prototype, not a deployed service or a Discord integration. It has no real employee-data access, authentication, ticketing, or production retrieval database. Keep secrets and real employee data out of Git.
