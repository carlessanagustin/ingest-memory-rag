# Serving the ingested data over MCP

The app writes its Qdrant collection in the layout the **official**
[`mcp-server-qdrant`](https://github.com/qdrant/mcp-server-qdrant) reads, so you
can expose semantic search over your ingested `.txt`/`.md` files to any MCP
client — no custom server required.

## How compatibility works

`mcp-server-qdrant` embeds queries with **fastembed** and searches a **named**
vector. To match it, ingestion stores each chunk as:

- vector name **`fast-all-minilm-l6-v2`** (384-dim, cosine)
- payload **`{"document": <chunk text>, "metadata": {...}}`**
- embeddings from **fastembed `sentence-transformers/all-MiniLM-L6-v2`**

Because store and query use the same fastembed model, retrieval aligns. The MCP
server's `EMBEDDING_MODEL` **must** stay `sentence-transformers/all-MiniLM-L6-v2`
(384-dim) — a different model or dimension breaks search.

## Prerequisites

1. Qdrant running locally: `docker compose up -d qdrant` (REST at `http://localhost:6333`).
2. Ingested data: run the app (`make run` or `docker compose up`) and drop
   `.txt`/`.md` files into `./raw`. Confirm the `Document` collection has points
   at <http://localhost:6333/dashboard>.

## Run the official MCP server (HTTP/SSE)

```bash
QDRANT_URL=http://localhost:6333 \
COLLECTION_NAME=Document \
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 \
FASTMCP_HOST=127.0.0.1 FASTMCP_PORT=8000 \
  uvx mcp-server-qdrant --transport sse
```

The SSE endpoint is then available at **`http://127.0.0.1:8000/sse`**. It exposes
a `qdrant-find` tool that MCP clients call to search the ingested data.

Sanity check (should return `200` and an `text/event-stream` response):

```bash
curl -sf -m 3 -D - http://127.0.0.1:8000/sse -o /dev/null | head -1
```

## Connect a client

Point your MCP client at `http://127.0.0.1:8000/sse`:

- **Claude Code** — see [TASK-10]
- **opencode** — see [TASK-11]
- **pi.dev (Pi)** — see [TASK-12]

(Per-client configuration is documented in their respective tasks.)
