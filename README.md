# ingest-memory-rag

Watches a folder and, whenever a `*.txt` or `*.md` file is **added or updated**,
ingests it into a [Qdrant](https://qdrant.tech/documentation/) vector database
through a [Haystack](https://docs.haystack.deepset.ai/docs/intro) indexing
pipeline. Re-ingesting a changed file replaces its previous chunks, so the store
never accumulates stale content.

File watching is cross-platform via [`watchdog`](https://github.com/gorakhargosh/watchdog):
inotify on Linux, FSEvents/kqueue on macOS, ReadDirectoryChangesW on Windows —
the same code runs unchanged everywhere.

## How it works

At a systems level there are two paths: a **write path** that keeps Qdrant in
sync with your files, and a **read path** that lets MCP clients query them.

```mermaid
flowchart LR
    subgraph host["Your machine"]
        raw[["./raw folder<br/>.txt / .md files"]]
        clients["MCP clients<br/>Claude Code / opencode / pi.dev"]
    end

    subgraph app["ingest-memory-rag"]
        watch["File watcher<br/>+ debounce"]
        ingest["Ingestion service<br/>chunk + embed"]
    end

    model["Embedding model<br/>all-MiniLM-L6-v2"]
    mcp["mcp-server-qdrant<br/>semantic search"]
    qdrant[("Qdrant<br/>vector database")]

    raw -->|add / update| watch
    watch --> ingest
    ingest <-->|vectors| model
    ingest -->|upsert chunks| qdrant

    clients -->|query| mcp
    mcp -->|search| qdrant
    qdrant -->|matches| mcp
    mcp -->|results| clients
```

Each chunk is tagged with `meta.source_file`; on update the engine deletes all
chunks with that `source_file` before writing the new ones, so the store never
accumulates stale content.

<details>
<summary>Detailed pipeline (code-level view)</summary>

```mermaid
flowchart TD
    A[".txt / .md file in ./raw"] --> B["watchdog event"]
    B --> C["debounce"]
    C --> D["IngestionEngine"]
    D --> E["convert<br/>TextFileToDocument / MarkdownToDocument"]
    E --> F["delete prior chunks<br/>(by meta.source_file)"]
    F --> G["DocumentSplitter"]
    G --> H["SentenceTransformersDocumentEmbedder"]
    H --> I["DocumentWriter"]
    I --> Q[("Qdrant")]
```

</details>

## Requirements

- Docker + Docker Compose — to run the full stack, **or**
- for local development: Python 3.11 or 3.12, [uv](https://docs.astral.sh/uv/), and a running Qdrant at `http://localhost:6333`

## Setup

### Run the full stack with Docker (recommended)

`docker compose up` starts the whole stack — Qdrant, the ingestion `app`, the
`mcp-qdrant` bridge, and the [LobeChat](https://github.com/lobehub/lobe-chat) UI
(<http://localhost:3210>). The app waits until Qdrant is healthy, then watches
the bind-mounted `./raw` folder.

```bash
docker compose up --build      # start qdrant + app + mcp-qdrant + lobe-chat
# ...then add or edit a .txt / .md file in ./raw on your host
docker compose down            # stop everything
```

- The app reaches Qdrant over the compose network (`QDRANT_URL=http://qdrant:6333`) — no code change, just env.
- `mcp-qdrant` serves the ingested collection over MCP so LobeChat can search it — see [MCP → LobeChat](#lobechat-chat-ui-via-docker-compose).
- `./raw` is bind-mounted into the container, and `WATCH_USE_POLLING=true` is set so
  host changes are detected across the mount (Docker Desktop does not deliver
  native FS events there).

### Run locally (development)

```bash
docker compose up -d qdrant    # just the database
uv sync --frozen               # install from the lockfile
uv run ingest-memory-rag       # watch ./raw, ingest into localhost:6333
```

Drop or edit a `.txt` / `.md` file in `./raw` and watch it get indexed. Inspect
the collection at <http://localhost:6333/dashboard>.

> The first run downloads the embedding model (`all-MiniLM-L6-v2`, ~90 MB).

## Configuration

All settings are read from the environment (see [`.env.example`](.env.example)):

| Variable | Default | Description |
| --- | --- | --- |
| `WATCH_FOLDER` | `./raw` | Folder to watch (created if missing) |
| `QDRANT_URL` | `http://localhost:6333` | Qdrant endpoint |
| `QDRANT_INDEX` | `Document` | Collection name |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Sentence-Transformers model |
| `EMBEDDING_DIM` | `384` | Vector size — **must match the model** |
| `SPLIT_BY` / `SPLIT_LENGTH` / `SPLIT_OVERLAP` | `word` / `200` / `30` | Chunking |
| `DEBOUNCE_SECONDS` | `1.0` | Coalesce rapid save events |
| `SCAN_ON_START` | `true` | Ingest existing matching files on startup |
| `QDRANT_RECREATE_INDEX` | `false` | Drop and recreate the collection at startup |
| `WATCH_USE_POLLING` | `false` | Poll instead of native FS events (needed for bind mounts on Docker Desktop) |

## Development

```bash
uv sync                 # install runtime + dev dependencies
uv run ruff check .     # lint
uv run ruff format .    # format
uv run mypy             # type-check
uv run pytest           # fast unit tests (no network / no Qdrant), ≥80% coverage
```

## MCP (query the ingested data)

Ingestion writes a Qdrant collection the official
[`mcp-server-qdrant`](https://github.com/qdrant/mcp-server-qdrant) can serve, so
MCP clients (Claude Code, opencode, pi.dev, LobeChat) can run semantic search
over your ingested files. With Qdrant running and data ingested, start the server
over SSE:

```bash
QDRANT_URL=http://localhost:6333 COLLECTION_NAME=Document \
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 \
FASTMCP_HOST=127.0.0.1 FASTMCP_PORT=8000 \
  uvx mcp-server-qdrant --transport sse
```

Remote clients (opencode, pi.dev) connect to that SSE endpoint
**`http://127.0.0.1:8000/sse`**; Claude Code instead runs the server locally over
stdio (below), so it needs no separate process and no authentication. Keep
`EMBEDDING_MODEL` as `all-MiniLM-L6-v2` (384-dim) so queries match the ingested
vectors.

### LobeChat (chat UI, via Docker Compose)

`docker compose up` also starts a [LobeChat](https://github.com/lobehub/lobe-chat)
web UI plus an `mcp-qdrant` bridge that serves your ingested collection over MCP
(**Streamable HTTP**) — no separate host process. Wiring them together lets you
*chat* with your ingested files. Qdrant is reached purely through MCP; LobeChat's
built-in knowledge base (PostgreSQL/pgvector) is intentionally not used here.

1. **Start the stack** and open the UI:

   ```bash
   docker compose up --build      # includes lobe-chat + mcp-qdrant
   ```

   Then browse to <http://localhost:3210>.

2. **Configure an LLM provider** — MCP tools need a model that supports
   tool/function calling. Either set a key before starting (the `lobe-chat`
   service reads it from your `.env`)…

   ```dotenv
   OPENAI_API_KEY=sk-...
   # or
   ANTHROPIC_API_KEY=sk-ant-...
   ```

   …or add one in the app under **Settings → AI Service Provider**.

3. **Add the Qdrant MCP plugin.** In LobeChat's plugin/tool store, add a custom
   MCP plugin with:

   - **Type:** `Streamable HTTP`
   - **URL:** `http://mcp-qdrant:8000/mcp`

   LobeChat connects to MCP servers **server-side**, from inside its container, so
   use the compose service name `mcp-qdrant` (not `localhost`). The bridge is also
   published on the host at `http://localhost:8000/mcp` for a LobeChat running
   outside this compose network.

4. **Verify.** Enable the plugin in a chat and ask something answerable only from
   your ingested files, e.g. *"Use qdrant-find to search my notes for agentic
   coding and summarise what you find."* LobeChat invokes the `qdrant-find` tool
   and answers from the ingested content.

### Claude Code

Use **stdio** locally — Claude Code launches the server itself, so there is no
separate process to run and no authentication (`mcp-server-qdrant` has none, so an
HTTP/SSE setup would stall on Claude Code's OAuth handshake):

```bash
claude mcp add qdrant \
  -e QDRANT_URL=http://localhost:6333 \
  -e COLLECTION_NAME=Document \
  -e EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 \
  -- uvx mcp-server-qdrant
```

Add `--scope project` to write a shared `.mcp.json`, or `--scope user` to enable it
in every project. The equivalent `.mcp.json` entry:

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "COLLECTION_NAME": "Document",
        "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
      }
    }
  }
}
```

Restart Claude Code (or reconnect via `/mcp`), confirm `qdrant` is connected and its
`qdrant-find` tool is listed, then ask Claude to search your ingested files.

> Only use SSE (`claude mcp add --transport sse qdrant http://127.0.0.1:8000/sse`)
> for a remote/shared server — and note it needs an auth layer, since Claude Code
> attempts OAuth for HTTP/SSE transports.

### opencode

Add the server to `opencode.json` (project root or `~/.config/opencode/opencode.json`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "qdrant": {
      "type": "remote",
      "url": "http://127.0.0.1:8000/sse",
      "enabled": true
    }
  }
}
```

opencode loads the server's `qdrant-find` tool at startup; ask it to search your
ingested files to confirm.

### pi.dev (Pi coding agent)

Pi has no built-in MCP support — enable it with a community adapter such as
[`pi-mcp`](https://github.com/0xKobold/pi-mcp). After installing the extension,
register the server in its config (for `pi-mcp`, `~/.0xkobold/mcp.json`):

```json
{
  "servers": [
    {
      "name": "qdrant",
      "transport": { "type": "sse", "url": "http://127.0.0.1:8000/sse" },
      "enabled": true,
      "autoReconnect": true
    }
  ]
}
```

In Pi, run `/mcp discover` (or `/mcp status`) to confirm the `qdrant-find` tool is
available, then ask it to search your ingested files. The exact config path and
format follow the adapter you choose.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
