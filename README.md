# AI Incident Collector

The model of an AI workflow that collects messages from different sources, examines them and creates a JSON output with scoring of relevance.

## How to use

1. Add your Anthropic API key to `.env`
2. Run `python workflow.py`

> **Note on `.env`:** normally I wouldn't commit `.env` to a repo, but this is a demo — it's committed so a reviewer can run everything right away. The key inside is a placeholder, not a real credential.

## Requirements

- anthropic
- python-dotenv

## Description

- **workflow.py** — the main file of the AI workflow. Adds the context for an AI model and the initial data about the incident from `config.py`.
  1. The model reads the alert message and extracts properties to filter the messages from different sources (Jira tickets, status pages, etc.)
  2. The script calls `collect()` from `info_collector.py`
  3. `info_collector` returns the JSON with mocked messages filtered by time
  4. The second call of the model, with an analyzing prompt, looks into the info collector's output
  5. The model returns a list of entities with scoring, sorted from high to low score depending on time, sense, and relevance to the incident
- **logs.json** — the log file
- **info_collector_output.mock.json** — the mocked output for the info collector
- **config.py** — contains variables that could be changed
