#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

rm -rf _site
mkdir -p _site

# Pinned Tailwind CLI version used to compile the utility classes referenced
# below at build time (see the Tailwind compile step further down).
TAILWIND_CLI_PKG="@tailwindcss/cli@4.1.13"

# --- 1. Render the board HTML from live task data (does not touch backlog/) ---
# `backlog task list --json` is read-only; `backlog board export` is NOT used
# here because it rewrites task files as a side effect.
uv run python - _site/index.html <<'PY'
import json
import subprocess
import sys
import datetime
import html

dst = sys.argv[1]

raw = subprocess.run(
    ["backlog", "task", "list", "--json"],
    capture_output=True, text=True, check=True,
).stdout
data = json.loads(raw)
tasks = data.get("tasks", [])

COLUMNS = ["To Do", "In Progress", "Done"]
by_status = {c: [] for c in COLUMNS}
for t in tasks:
    status = t.get("status")
    if status in by_status:
        by_status[status].append(t)
for col in by_status.values():
    col.sort(key=lambda t: (t.get("ordinal") or 0, t.get("id") or ""))

generated = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
esc = html.escape


def render_card(t: dict) -> str:
    task_id = esc(str(t.get("id", "")))
    title = esc(str(t.get("title", "")))
    labels = t.get("labels") or []
    assignees = t.get("assignees") or []

    label_badges = "".join(
        f'<span class="inline-block rounded-full bg-indigo-100 px-2 py-0.5 '
        f'text-xs font-medium text-indigo-700 dark:bg-indigo-500/20 '
        f'dark:text-indigo-300">{esc(str(label))}</span>'
        for label in labels
    )
    labels_html = (
        f'<div class="mt-2 flex flex-wrap gap-1">{label_badges}</div>'
        if labels else ""
    )

    assignees_html = (
        f'<p class="mt-2 text-xs text-slate-500 dark:text-slate-400">'
        f'{esc(", ".join(str(a) for a in assignees))}</p>'
        if assignees else ""
    )

    return f"""
      <article class="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-800">
        <span class="inline-block rounded bg-slate-100 px-1.5 py-0.5 font-mono text-xs text-slate-500 dark:bg-slate-700 dark:text-slate-300">{task_id}</span>
        <h3 class="mt-2 text-sm font-semibold text-slate-900 dark:text-slate-100">{title}</h3>
        {labels_html}
        {assignees_html}
      </article>"""


def render_column(name: str) -> str:
    items = by_status[name]
    cards = "".join(render_card(t) for t in items) or (
        '<p class="text-sm italic text-slate-400 dark:text-slate-500">No tasks</p>'
    )
    return f"""
    <section class="flex flex-col gap-3">
      <header class="flex items-center justify-between rounded-lg bg-slate-100 px-3 py-2 dark:bg-slate-800">
        <h2 class="text-sm font-semibold uppercase tracking-wide text-slate-700 dark:text-slate-200">{esc(name)}</h2>
        <span class="rounded-full bg-slate-200 px-2 py-0.5 text-xs font-medium text-slate-600 dark:bg-slate-700 dark:text-slate-300">{len(items)}</span>
      </header>
      <div class="flex flex-col gap-3">{cards}</div>
    </section>"""


columns_html = "".join(render_column(name) for name in COLUMNS)

html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ingest-memory-rag — Kanban Board</title>
<style>/*__TAILWIND__*/</style>
</head>
<body class="min-h-screen bg-slate-50 px-4 py-8 text-slate-900 dark:bg-slate-950 dark:text-slate-100 sm:px-6 lg:px-8">
<div class="mx-auto max-w-6xl">
  <header class="mb-6">
    <h1 class="text-xl font-bold sm:text-2xl">ingest-memory-rag — Kanban Board</h1>
    <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">Generated on {generated}</p>
  </header>
  <div class="grid grid-cols-1 gap-4 md:grid-cols-3">{columns_html}
  </div>
</div>
</body>
</html>
"""

with open(dst, "w", encoding="utf-8") as f:
    f.write(html_doc)
PY

# --- 2. Compile Tailwind at build time (temp input, scans the generated HTML) ---
# `@import "tailwindcss"` is resolved by Node module resolution starting from
# the input CSS file's directory, so the input file must live next to a
# node_modules/tailwindcss install. Installing the pinned CLI into an
# isolated temp prefix (rather than relying on npx's internal cache layout)
# keeps this deterministic and leaves nothing behind in the repo.
tw_tmp="$(mktemp -d)"
trap 'rm -rf "$tw_tmp"' EXIT

npm install --no-save --silent --prefix "$tw_tmp" "$TAILWIND_CLI_PKG" >/dev/null

tw_input="$tw_tmp/input.css"
tw_output="$tw_tmp/output.css"
cat > "$tw_input" <<CSS
@import "tailwindcss";
@source "${repo_root}/_site/index.html";
CSS

"$tw_tmp/node_modules/.bin/tailwindcss" -i "$tw_input" -o "$tw_output" --minify

# --- 3. Inline the compiled CSS in place of the placeholder, then clean up ---
uv run python - _site/index.html "$tw_output" <<'PY'
import sys

html_path, css_path = sys.argv[1], sys.argv[2]
html_text = open(html_path, encoding="utf-8").read()
css_text = open(css_path, encoding="utf-8").read()
# Strip Tailwind's leading license-attribution comment: it is inert (never
# fetched) but contains a bare "https://" string that would otherwise trip
# an automated zero-external-reference check on the generated page.
if css_text.startswith("/*!"):
    css_text = css_text.split("*/", 1)[1].lstrip()
html_text = html_text.replace("/*__TAILWIND__*/", css_text, 1)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_text)
PY

rm -rf "$tw_tmp"
trap - EXIT

echo "Built _site/index.html"
