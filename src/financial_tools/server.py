"""Main entry point for Modular Financial MCP Server."""

import sys
from financial_tools.shared.types import FastMCP

from financial_tools.crypto.tools import register_crypto_tools
from financial_tools.shared.logging import logger
from financial_tools.stocks.tools import register_stock_tools


def create_mcp_server() -> FastMCP:
    """Instantiates and registers all domain tools on the FastMCP server."""
    server = FastMCP(
        name="financial-agent-tools",
        instructions=(
            "Modular Financial Tools MCP Server providing: "
            "(1) Stock quotes, history, and technical analysis (supporting US and Indonesian IDX tickers like BBCA.JK), and "
            "(2) Cryptocurrency quotes, history, and volatility metrics (BTC, ETH, etc.)."
        ),
    )

    # Register independent financial domains
    register_stock_tools(server)
    register_crypto_tools(server)

    return server


mcp_server = create_mcp_server()


def main():
    """Runs the MCP server over stdio transport."""
    logger.info("Starting financial-agent-tools MCP Server over stdio transport...")
    # FastMCP/MCPServer run method over stdio
    mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
