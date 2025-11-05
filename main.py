#!/usr/bin/env python3
import json
import httpx
import os
from fastmcp import FastMCP

API_BASE_URL = "https://product-search-mcp-api.replit.app"

# Create FastMCP server instance
# CLI will automatically find this object named 'mcp'
mcp = FastMCP("Product Search MCP Server")

@mcp.tool()
async def search_products(query: str = "", category: str = "") -> str:
    """
    Search products by name and category.

    Args:
        query: Search query for product names
        category: Product category (electronics, furniture)

    Returns:
        JSON formatted search results
    """
    async with httpx.AsyncClient() as client:
        try:
            # V1 IMPLEMENTATION (START HERE)
            search_data = {
                "query": query,
                "category": category
            }
            response = await client.post(f"{API_BASE_URL}/v1/products/search",
                                       json=search_data)

            response.raise_for_status()
            data = response.json()
            return json.dumps(data, indent=2)

        except Exception as e:
            return f"Error: {str(e)}"

# V2 TOOL (UNCOMMENT DURING DEMO)
# @mcp.tool()
# async def product_search_price_range(query: str = "", category: str = "", price_min: float = None, price_max: float = None) -> str:
#     """
#     Search products by name, category, and price range.
#
#     Args:
#         query: Search query for product names
#         category: Product category (electronics, furniture)
#         price_min: Minimum price filter
#         price_max: Maximum price filter
#
#     Returns:
#         JSON formatted search results with price filtering
#     """
#     async with httpx.AsyncClient() as client:
#         try:
#             # V2 IMPLEMENTATION (CHANGE DURING DEMO)
#             search_data = {
#                 "query": query,
#                 "category": category,
#                 "price_range": {}
#             }
#
#             if price_min is not None or price_max is not None:
#                 search_data["price_range"] = {}
#                 if price_min is not None:
#                     search_data["price_range"]["min"] = price_min
#                 if price_max is not None:
#                     search_data["price_range"]["max"] = price_max
#
#             response = await client.post(f"{API_BASE_URL}/v2/products/search",
#                                        json=search_data)
#
#             response.raise_for_status()
#             data = response.json()
#             return json.dumps(data, indent=2)
#
#         except Exception as e:
#             return f"Error: {str(e)}"

# V3 TOOL (UNCOMMENT DURING DEMO)
# @mcp.tool()
# async def product_search_inventory(query: str = "", category: str = "", in_stock: bool = None) -> str:
#     """
#     Search products by name, category, and inventory status.

#     Args:
#         query: Search query for product names
#         category: Product category (electronics, furniture)
#         in_stock: Filter by inventory status (True for in stock, False for out of stock)

#     Returns:
#         JSON formatted search results with inventory filtering
#     """
#     async with httpx.AsyncClient() as client:
#         try:
#             # V3 IMPLEMENTATION (CHANGE DURING DEMO)
#             search_data = {
#                 "query": query,
#                 "category": category,
#                 "in_stock": in_stock
#             }

#             response = await client.post(f"{API_BASE_URL}/v3/products/search",
#                                        json=search_data)

#             response.raise_for_status()
#             data = response.json()
#             return json.dumps(data, indent=2)

#         except Exception as e:
#             return f"Error: {str(e)}"

# Optional: Keep for direct execution compatibility
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting MCP server on port {port}")
    mcp.run(transport="http", host="0.0.0.0", port=port)
