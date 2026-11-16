# MCP Identity Inventory

A small, read-only Python MCP server for exploring fictional users,
service accounts, and AI agents.

## Planned tools

- list_identities(): list identities and their types.
- get_identity(identity_id): retrieve an identity's roles and permissions.
- find_inactive_identities(days): find identities unused for a given period.

## Setup

Requires Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pip install --no-deps -e .
