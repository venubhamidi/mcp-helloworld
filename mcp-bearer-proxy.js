#!/usr/bin/env node

/**
 * MCP Bearer Token Proxy
 * Bridges stdio (Claude Desktop) to HTTP MCP servers with Bearer token auth
 */

import { createInterface } from 'readline';
import { stdout, stderr, stdin } from 'process';

const MCP_URL = process.env.MCP_URL;
const MCP_TOKEN = process.env.MCP_TOKEN;

if (!MCP_URL) {
  stderr.write('Error: MCP_URL environment variable is required\n');
  process.exit(1);
}

if (!MCP_TOKEN) {
  stderr.write('Error: MCP_TOKEN environment variable is required\n');
  process.exit(1);
}

const DEBUG = process.env.MCP_DEBUG === 'true';

function debug(...args) {
  if (DEBUG) {
    stderr.write(`[MCP-PROXY] ${args.join(' ')}\n`);
  }
}

async function sendRequest(message) {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream',
    'Authorization': `Bearer ${MCP_TOKEN}`
  };

  debug(`Sending request to ${MCP_URL}:`, JSON.stringify(message));

  try {
    const response = await fetch(MCP_URL, {
      method: 'POST',
      headers,
      body: JSON.stringify(message)
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`HTTP ${response.status}: ${text}`);
    }

    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('text/event-stream')) {
      // Handle SSE response
      debug('Received SSE response');
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;

            try {
              const parsed = JSON.parse(data);
              debug('Received SSE event:', JSON.stringify(parsed));
              stdout.write(JSON.stringify(parsed) + '\n');
            } catch (e) {
              debug('Failed to parse SSE data:', data);
            }
          }
        }
      }
    } else {
      // Handle regular JSON response
      const data = await response.json();
      debug('Received JSON response:', JSON.stringify(data));
      stdout.write(JSON.stringify(data) + '\n');
    }
  } catch (error) {
    debug('Error:', error.message);

    // Send error response back to client
    const errorResponse = {
      jsonrpc: '2.0',
      id: message.id || null,
      error: {
        code: -32603,
        message: error.message
      }
    };
    stdout.write(JSON.stringify(errorResponse) + '\n');
  }
}

// Read JSON-RPC messages from stdin
const rl = createInterface({
  input: stdin,
  terminal: false,
  crlfDelay: Infinity
});

debug('MCP Bearer Proxy started');
debug(`Connecting to: ${MCP_URL}`);

let pendingRequests = 0;

rl.on('line', (line) => {
  if (!line.trim()) return;

  try {
    const message = JSON.parse(line);
    pendingRequests++;

    sendRequest(message).finally(() => {
      pendingRequests--;
      if (pendingRequests === 0 && rl.closed) {
        debug('All requests completed, shutting down');
        process.exit(0);
      }
    });
  } catch (error) {
    debug('Failed to parse input:', error.message);
  }
});

rl.on('close', () => {
  debug('Stdin closed');
  if (pendingRequests === 0) {
    debug('Proxy shutting down');
    process.exit(0);
  }
});

process.on('SIGINT', () => {
  debug('Received SIGINT, shutting down');
  process.exit(0);
});

process.on('SIGTERM', () => {
  debug('Received SIGTERM, shutting down');
  process.exit(0);
});
