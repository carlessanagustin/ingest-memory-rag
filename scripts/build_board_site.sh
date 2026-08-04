#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

rm -rf _site
mkdir -p _site

backlog board export _site/board.md --force

uv run --with markdown python - _site/board.md _site/index.html <<'PY'
import sys, datetime, markdown

src, dst = sys.argv[1], sys.argv[2]
md_text = open(src, encoding="utf-8").read()
body = markdown.markdown(md_text, extensions=["tables"])
generated = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ingest-memory-rag — Kanban Board</title>
<style>
  :root {{
    color-scheme: light dark;
    --bg: #f5f6f8;
    --fg: #1b1f24;
    --card-bg: #ffffff;
    --border: #d8dce1;
    --header-bg: #eef1f5;
    --accent: #3b5bdb;
    --muted: #6b7280;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #14161a;
      --fg: #e6e8eb;
      --card-bg: #1d2025;
      --border: #33373d;
      --header-bg: #23262b;
      --accent: #7c9bff;
      --muted: #9aa1ab;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 2rem 1.5rem 3rem;
    background: var(--bg);
    color: var(--fg);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.5;
  }}
  header.page-header {{
    max-width: 1100px;
    margin: 0 auto 1.5rem;
  }}
  header.page-header h1 {{
    margin: 0 0 0.25rem;
    font-size: 1.6rem;
  }}
  header.page-header p {{
    margin: 0;
    color: var(--muted);
    font-size: 0.9rem;
  }}
  .board-wrap {{
    max-width: 1100px;
    margin: 0 auto;
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--card-bg);
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    min-width: 720px;
  }}
  thead th {{
    background: var(--header-bg);
    text-align: left;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    border-bottom: 2px solid var(--border);
    position: sticky;
    top: 0;
  }}
  tbody td {{
    vertical-align: top;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    border-right: 1px solid var(--border);
    font-size: 0.9rem;
    width: 33.33%;
  }}
  tbody td:last-child {{ border-right: none; }}
  tbody tr:last-child td {{ border-bottom: none; }}
  strong {{ color: var(--accent); }}
  em {{ color: var(--muted); font-style: italic; }}
  footer {{
    max-width: 1100px;
    margin: 1.5rem auto 0;
    color: var(--muted);
    font-size: 0.8rem;
  }}
</style>
</head>
<body>
<header class="page-header">
  <h1>ingest-memory-rag — Kanban Board</h1>
  <p>Generated on {generated}</p>
</header>
<div class="board-wrap">
{body}
</div>
<footer>Static export via <code>backlog board export</code> — rendered offline, no external resources.</footer>
</body>
</html>
"""

with open(dst, "w", encoding="utf-8") as f:
    f.write(html)
PY

rm -f _site/board.md

echo "Built _site/index.html"
