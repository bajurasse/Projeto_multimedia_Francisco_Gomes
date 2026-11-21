# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

"Dashboard Multimédia" is a school project (Oficina de Multimédia, 2026/2027): a static site whose landing page links to three interactive widgets written in **Python that runs in the browser via PyScript** (release `2025.11.1`, loaded from `pyscript.net`). There is no build step, package manager, test suite or linter. All UI text and identifiers (functions, variables, DOM ids) are in **European Portuguese (pt-PT)**; keep new code and copy consistent with that.

## Running

Serve the folder over HTTP (PyScript does not work from `file://`), e.g.:

```
python -m http.server 8000
```

then open `http://localhost:8000/index.html`. The VS Code Live Preview extension is also configured (`.vscode/settings.json` → `/index.html`). Python errors appear in the browser console / PyScript error banner, not in a terminal.

## Architecture

- `index.html` — pure HTML hub (no PyScript), with cards linking to each widget page.
- `style.css` — one shared stylesheet for every page (widget pages reference it as `../style.css`). Styles for all widgets (galo board, quiz timer/explosion overlay, result modals, loading spinner) live here.
- Each widget is a folder with an HTML page + a Python script loaded via `<script type="py" src="./x.py">`:
  - `poesia/` — text/poem analyser (word counts, most frequent word, suggestion).
  - `galo/` — tic-tac-toe vs CPU (easy = random, medium = 50% win/block heuristic, hard = minimax) or local 2-player.
  - `quiz/` — multimedia quiz: 5 random questions from `banco_perguntas`, 10 s countdown per question.

### PyScript conventions used throughout

- Every widget page has a `#loading` overlay; the Python script removes it at import time (`document.getElementById("loading").remove()`), so this must stay at the top of each script.
- Event handlers are bound with `@when("click", "#element-id")`; the Python code is tightly coupled to DOM ids/classes in the matching HTML file — rename both together.
- Clicks on dynamic children (board cells, quiz options) are handled by a single delegated handler on the container using `event.target.closest(...)`.
- State is held in module-level globals mutated via `global`. Async work uses `asyncio` (`asyncio.sleep`, `asyncio.create_task`); the quiz timer uses a `ciclo_pergunta_atual` counter so stale countdown tasks exit when the question changes.
