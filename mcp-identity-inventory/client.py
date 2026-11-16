# Connect to identity inventory server through MCP

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult


def show_result(title: str, result: CallToolResult) -> None:
    # Display text returned by an MCP tool

    print(f"\n---{title}---")
    print(f"Tool error: {bool(result.isError)}")

    for content in result.content:
        if content.type == "text":
            print(content.text)


async def main() -> None:
    # start the server, discover tools, and call them

    server_file = Path(__file__).resolve().with_name("server.py")

    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Available MCP tools:")
            for tool in tools.tools:
                print(f"{tool.name}")

            result = await session.call_tool("list_identities", {})
            show_result("All identities", result)

            result = await session.call_tool(
                "get_identity",
                {"identity_id": "user-001"},
            )

            show_result("One identity", result)

            result = await session.call_tool(
                "find_inactive_identities",
                {"days": 90},
            )

            show_result("Inactive identities", result)

            result = await session.call_tool(
                "get_identity",
                {"identity_id": "missing"},
            )

            show_result("Expected error: unknown identity", result)

    print("\nClient finished: server connection closed")


if __name__ == "__main__":
    asyncio.run(main())
