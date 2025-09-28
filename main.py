from fastmcp import FastMCP

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
    # Run the server
    mcp.run()
