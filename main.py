from fastmcp import FastMCP

# Create FastMCP server instance
# CLI will automatically find this object named 'mcp'
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

# Optional: Keep for direct execution compatibility
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting MCP server on port {port}")
    mcp.run(transport="http", host="0.0.0.0", port=port)
