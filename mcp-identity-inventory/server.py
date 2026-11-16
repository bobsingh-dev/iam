# Read-only MCP server for a fictional identity inventory

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Identity Inventory")


if __name__ == "__main__":
    mcp.run(transport="stdio")



