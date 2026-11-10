"""Utility script to verify and inspect all registered MCP tools and schemas."""

import asyncio
import json
import sys
from os.path import abspath
sys.path.insert(0, abspath("src"))

from financial_tools.server import mcp_server


async def inspect_server():
    print("=" * 60)
    print(" FINANCIAL-AGENT-TOOLS MCP SERVER TOOL INVENTORY")
    print("=" * 60)

    tools = await mcp_server.list_tools()
    print(f"\nTotal Registered Tools: {len(tools)}\n")

    for idx, tool in enumerate(tools, 1):
        print(f"[{idx}] Tool: {tool.name}")
        print(f"    Description: {tool.description.strip()}")
        if hasattr(tool, "inputSchema") and tool.inputSchema:
            print(f"    Input Schema: {json.dumps(tool.inputSchema, indent=6)}")
        print("-" * 60)

    print("\nAll MCP tools successfully inspected and registered!")


if __name__ == "__main__":
    asyncio.run(inspect_server())
