# Read-only MCP server for a fictional identity inventory

from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, TypeAdapter

mcp = FastMCP("Identity Inventory")


DATA_FILE = Path(__file__).with_name("identities.json")


class Identity(BaseModel):
    # A Fictional Identity and its access information

    id: str
    name: str
    type: Literal["user", "service_account", "ai_agent"]
    roles: list[str]
    permissions: list[str]
    last_used: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


def load_identities() -> list[Identity]:
    # Read and validate the local inventory

    adapter = TypeAdapter(list[Identity])
    return adapter.validate_json(DATA_FILE.read_text(encoding="utf-8"))


@mcp.tool()
def list_identities() -> list[Identity]:
    # List all identities in the fictional inventory
    return load_identities()


@mcp.tool()
def get_identity(identity_id: str) -> Identity:
    # Get an identity's details using its exact id

    for identity in load_identities():
        if identity.id == identity_id:
            return identity

    raise ValueError(f"Identity not found: {identity_id}")


@mcp.tool()
def find_inactive_identities(days: int) -> list[Identity]:
    # Find identities unused for at least the given numbers of days

    if days < 1:
        raise ValueError("days must be at least 1")

    today = datetime.now(timezone.utc).date()
    inactive: list[Identity] = []

    for identity in load_identities():
        last_used = datetime.strptime(identity.last_used, "%Y-%m-%d").date()

        if (today - last_used).days >= days:
            inactive.append(identity)

    return inactive


if __name__ == "__main__":
    mcp.run(transport="stdio")
