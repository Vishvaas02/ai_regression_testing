# LLM Test Framework

Provider-agnostic regression testing for LLM applications.

LLM Test Framework helps QA engineers and developers catch regressions caused by
prompt edits, model switches, retrieval changes, parameter tuning, or application
logic changes. It is designed to feel like lightweight, pytest-style testing for
LLM responses without locking teams into one model vendor.

## What it tests

- Correctness: required phrases, exact answers, regexes, JSON fields, and fuzzy similarity.
- Safety: simple unsafe-output pattern checks for MVP guardrails.
- Latency: maximum response time per case.
- Consistency: repeated calls should stay similar enough.
- Provider independence: test any app that can be wrapped as a command or Python function.

## Install locally

```bash
python3 -m pip install -e .
```

## Run the example

```bash
llmtest run examples/regression_suite.json \
  --command "python3 examples/fake_llm_app.py" \
  --json-report report.json \
  --junit-report junit.xml
```

You can also run without installing:

```bash
python3 -m llm_test_framework.cli run examples/regression_suite.json \
  --command "python3 examples/fake_llm_app.py"
```

## Test suite format

Suites are JSON files:

```json
{
  "name": "Checkout assistant regression",
  "defaults": {
    "repeats": 1
  },
  "cases": [
    {
      "id": "refund-policy",
      "tags": ["correctness", "policy"],
      "prompt": "What is the refund window?",
      "assertions": [
        {"type": "contains", "text": "30 days"},
        {"type": "max_latency_ms", "value": 2000},
        {"type": "safe_response"}
      ]
    }
  ]
}
```

## Assertion types

| Type | Purpose |
| --- | --- |
| `contains` | Response must include text. |
| `not_contains` | Response must not include text. |
| `regex` | Response must match a regular expression. |
| `equals` | Response must equal configured text, with whitespace normalization by default. |
| `json_field_equals` | Response must be JSON and a dotted field must equal a value. |
| `similar_to` | Response must be similar to expected text using a deterministic string similarity score. |
| `max_latency_ms` | First response latency must be below a limit. |
| `safe_response` | Response must avoid MVP unsafe-output patterns. |
| `consistent` | Repeated responses must remain similar. Set `repeats` to at least `2`. |

## Provider adapters

### Command provider

Use this when your LLM app can be called from the shell. The command receives
JSON on stdin:

```json
{"prompt": "question", "variables": {"locale": "en-US"}}
```

It may print plain text or JSON with a `text` field:

```json
{"text": "The refund window is 30 days.", "model": "local-fake"}
```

### Python provider

Use this when your app exposes a callable:

```python
def answer(prompt: str, variables: dict) -> str:
    return "The refund window is 30 days."
```

Run it with:

```bash
llmtest run suite.json --python-provider "my_app.qa:answer"
```

## Exit codes

- `0`: all selected tests passed.
- `1`: at least one selected test failed.
- `2`: suite, provider, or CLI configuration error.

## Roadmap

- Native pytest plugin.
- Snapshot/baseline comparison workflows.
- Pluggable evaluator registry.
- First-party OpenAI, Anthropic, local model, and HTTP adapters.
- Richer safety and hallucination evaluators.
