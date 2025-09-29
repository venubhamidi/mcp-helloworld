from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PRODUCTS = [{
    "id": 1,
    "name": "MacBook Pro",
    "category": "electronics",
    "price": 2399,
    "in_stock": True
}, {
    "id": 2,
    "name": "Gaming Chair",
    "category": "furniture",
    "price": 450,
    "in_stock": False
}, {
    "id": 3,
    "name": "Wireless Mouse",
    "category": "electronics",
    "price": 85,
    "in_stock": True
}, {
    "id": 4,
    "name": "Standing Desk",
    "category": "furniture",
    "price": 599,
    "in_stock": True
}, {
    "id": 5,
    "name": "iPhone 15",
    "category": "electronics",
    "price": 999,
    "in_stock": False
}, {
    "id": 6,
    "name": "Coffee Table",
    "category": "furniture",
    "price": 249,
    "in_stock": True
}, {
    "id": 7,
    "name": "Gaming Laptop",
    "category": "electronics",
    "price": 1599,
    "in_stock": False
}, {
    "id": 9,
    "name": "Macbook Pro Laptop",
    "category": "electronics",
    "price": 2500,
    "in_stock": True
}, {
    "id": 8,
    "name": "Office Lamp",
    "category": "furniture",
    "price": 89,
    "in_stock": False
}]


def filter_products_v1(query, category):
    """V1 filtering - basic query and category only"""
    results = PRODUCTS

    if query:
        results = [p for p in results if query.lower() in p['name'].lower()]

    if category:
        results = [
            p for p in results if p['category'].lower() == category.lower()
        ]

    # V1 API doesn't include inventory information - remove in_stock field
    results = [
        {k: v for k, v in product.items() if k != 'in_stock'}
        for product in results
    ]

    return results


def filter_products_v2(query, category, price_range):
    """V2 filtering - adds price range filtering"""
    results = filter_products_v1(query, category)

    # NEW in V2: Price range filtering
    if price_range:
        min_price = price_range.get('min') if price_range.get('min') is not None else 0
        max_price = price_range.get('max') if price_range.get('max') is not None else float('inf')
        results = [p for p in results if min_price <= p['price'] <= max_price]

    return results


def filter_products_v3(query, category, in_stock):
    """V3 filtering - adds inventory filtering"""
    # Start with raw products (including in_stock field)
    results = PRODUCTS

    # Apply basic filters
    if query:
        results = [p for p in results if query.lower() in p['name'].lower()]

    if category:
        results = [
            p for p in results if p['category'].lower() == category.lower()
        ]

    # NEW in V3: Inventory filtering
    if in_stock is not None:
        results = [p for p in results if p['in_stock'] == in_stock]

    return results


# ============= V1 API ENDPOINTS =============
@app.route('/v1/products/search', methods=['POST'])
def search_products_v1():
    """V1 search - query + category only"""
    data = request.get_json() or {}
    query = data.get('query', '')
    category = data.get('category', '')

    results = filter_products_v1(query, category)

    return jsonify({
        "products": results,
        "version": "v1",
        "total": len(results),
        "search_params": {
            "query": query,
            "category": category
        },
        "message": "V1 API - Basic search (query + category)"
    })


# ============= V2 API ENDPOINTS =============
@app.route('/v2/products/search', methods=['POST'])
def search_products_v2():
    """V2 search - query + category + price_range"""
    data = request.get_json() or {}
    query = data.get('query', '')
    category = data.get('category', '')
    
    # Support both formats: direct min_price/max_price or nested price_range
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    price_range = data.get('price_range', {})
    
    # If direct min_price/max_price are provided, use those
    if min_price is not None or max_price is not None:
        price_range = {
            'min': min_price,
            'max': max_price
        }

    results = filter_products_v2(query, category, price_range)

    return jsonify({
        "products":
        results,
        "version":
        "v2",
        "total":
        len(results),
        "search_params": {
            "query": query,
            "category": category,
            "price_range": price_range
        },
        "message":
        "V2 API - Enhanced search (query + category + price_range)"
    })


# ============= V3 API ENDPOINTS =============
@app.route('/v3/products/search', methods=['POST'])
def search_products_v3():
    """V3 search - query + category + in_stock"""
    data = request.get_json() or {}
    query = data.get('query', '')
    category = data.get('category', '')
    in_stock = data.get('in_stock')

    results = filter_products_v3(query, category, in_stock)

    return jsonify({
        "products": results,
        "version": "v3",
        "total": len(results),
        "search_params": {
            "query": query,
            "category": category,
            "in_stock": in_stock
        },
        "message": "V3 API - Inventory search (query + category + in_stock)"
    })


@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message":
        "MCP Demo API - Live Code Change Demo",
        "available_endpoints": {
            "v1": "/v1/products/search (query + category)",
            "v2": "/v2/products/search (query + category + price_range)",
            "v3": "/v3/products/search (query + category + in_stock)"
        },
        "demo_flow": [
            "1. Start MCP server pointing to v1",
            "2. Test basic search capabilities",
            "3. Live change MCP server to point to v2",
            "4. Use Tool Refresh in Claude Desktop",
            "5. Show new price_range capability"
        ]
    })


if __name__ == '__main__':
    print("MCP Demo API starting...")
    print("V1 endpoint: /v1/products/search")
    print("V2 endpoint: /v2/products/search") 
    print("V3 endpoint: /v3/products/search")
    app.run(host='0.0.0.0', port=5000, debug=True)
