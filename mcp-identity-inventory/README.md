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

## Inventory and tools

The server reads fictional records from identities.json.
Each record includes an ID, name, identity type, roles, permissions,
and last-used date.

Available tools:

- list_identities(): return all inventory records.
- get_identity(identity_id): return one record or report an unknown ID.
- find_inactive_identities(days): return records unused for at least
  that many days, calculated using today's UTC date.

The tools only read data. Listed identity permissions are sample
inventory data, not authorization rules enforced by this server.

Lesson 2 complete: sample inventory and all three tools implemented.
