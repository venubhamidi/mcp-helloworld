# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway will set the PORT environment variable)
EXPOSE 8000

# Run using FastMCP CLI (official recommended approach)
CMD ["sh", "-c", "fastmcp run main.py --transport http --host 0.0.0.0 --port ${PORT:-8000}"]
