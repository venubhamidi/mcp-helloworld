#!/usr/bin/env python3
"""
Simple FastMCP Hello World Server for Railway
"""
from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Hello World MCP Server")

@mcp.tool()
def hello_world(name: str) -> str:
    """
    A simple hello world tool that greets a person by name.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A greeting message
    """
    return f"Hello World {name}"

# This script can be run with fastmcp CLI or directly
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting Hello World MCP Server on port {port}")
    print(f"MCP endpoint will be at: http://0.0.0.0:{port}/mcp")
    
    # Simple run command
    mcp.run(transport="http", host="0.0.0.0", port=port)
