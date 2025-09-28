from fastmcp import FastMCP
import uvicorn
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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

# Create the FastAPI app
app = mcp.create_app()

# Add a simple root endpoint to verify the server is running
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Hello World MCP Server</title>
        </head>
        <body>
            <h1>Hello World MCP Server is Running! 🚀</h1>
            <p>This is a remote MCP server with SSE transport.</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><strong>/sse</strong> - MCP Server-Sent Events endpoint</li>
                <li><strong>/</strong> - This status page</li>
            </ul>
            <h2>Available Tools:</h2>
            <ul>
                <li><strong>hello_world</strong> - Takes a name parameter and returns a greeting</li>
            </ul>
            <p>Connect your MCP client to the <code>/sse</code> endpoint to use the tools.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting MCP server on port {port}")
    
    # Run the server with SSE transport
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
