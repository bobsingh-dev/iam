# AI Agent Authorization Lab

A small Python project demonstrating authorization for MCP tools
called on a user's behalf.

## Goals

- Delegate user access through OAuth.
- Restrict MCP tools using scopes.
- Enforce authorization with OPA.
- Prevent access to another tenant's documents.
- Test allowed and denied requests.

## Tools

Python, MCP Python SDK, Keycloak, OPA, Docker Compose, and pytest.

A scripted MCP client makes tool calls without an AI API key.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
