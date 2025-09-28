from fastmcp import FastMCP
import os

# Create FastMCP server instance
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

if __name__ == "__main__":
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting MCP server on port {port}")
    
    # Run the server with HTTP transport (recommended over SSE)
    # HTTP transport is the modern approach for remote MCP servers
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=port
    )
