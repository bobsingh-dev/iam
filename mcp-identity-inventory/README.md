A small, read-only MCP server built with Python.

The server exposes tools for exploring fictional users, service
accounts, and AI agents. A Python client discovers and calls these
tools through the Model Context Protocol over stdio.

## Tools

| Tool | Purpose |
| --- | --- |
| list_identities() | List all identities |
| get_identity(identity_id) | Retrieve an identity's details |
| find_inactive_identities(days) | Find identities unused for at least a given number of days |

Each identity includes its ID, name, type, roles, permissions,
and last-used date.

## Stack

Python 3.12+, MCP Python SDK 1.x, Pydantic, pytest, Ruff, and mypy.

## Setup

From this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pip install --no-deps -e .
```

## Run the demo

```bash
python client.py
```

The client automatically starts the server, discovers its tools,
and calls all three tools.

It also requests an unknown identity to demonstrate error handling.
The error for that request is intentional.

No AI model or API key is required.

To start only the server:

```bash
python server.py
```

It waits for an MCP client over stdio. Press Ctrl+C to stop it.

## Tests and checks

```bash
python -m pytest -q
ruff check .
ruff format --check .
mypy server.py client.py test_server.py
```

Four basic tests cover listing identities, retrieving an identity,
an unknown identity ID, and an invalid inactivity threshold.

## Files

- server.py: MCP server, identity model, and tools.
- client.py: example MCP client.
- identities.json: fictional inventory.
- test_server.py: basic tests.
- pyproject.toml: project dependencies and tool settings.
- requirements.lock.txt: dependency versions captured during setup.

## Scope

This is a local learning project using fictional data.
Tools only read the inventory.

Listed roles and permissions describe the sample identities;
they do not enforce access to the server.

Inactivity is calculated using today's UTC date.
Authentication, cloud integrations, and an AI-powered client
are outside this project's scope.
