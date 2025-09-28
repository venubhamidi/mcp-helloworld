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

# Add a health check endpoint for Railway
@mcp.custom_route("/", methods=["GET"])
async def root(request):
    from starlette.responses import JSONResponse
    return JSONResponse({
        "status": "healthy",
        "message": "Hello World MCP Server is running!",
        "endpoints": {
            "mcp": "/mcp",
            "health": "/"
        }
    })

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    from starlette.responses import JSONResponse
    return JSONResponse({
        "status": "healthy",
        "tools": ["hello_world"]
    })

if __name__ == "__main__":
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting MCP server on port {port}")
    
    # Run the server with HTTP transport
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=port,
        path="/mcp"  # Explicitly set the MCP endpoint path
    )
