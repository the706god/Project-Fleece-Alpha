# Project: Fleece Alpha 🐑

**The "Crate Motor" SLM build (Text Edition)** — a small, self-contained AI model you run **completely offline, on your own machine**. No internet needed after the first setup.

**Core model:** Qwen 2.5 Coder 3B Instruct (`Q4_K_M` GGUF)

---

## What "local agent" means here

Fleece Alpha is a **tool for offloading work from frontier (cloud) agents so it can live locally**. You give it a task, it stays in memory, serves answers, and keeps its own notes — all without calling anything to a server. It is designed to run on your machine with nothing installed except a Python environment and the model weights.

- **No internet required.** Everything runs locally.
- **No cloud API keys.** No `OPENAI_API_KEY`, no `ANTHROPIC_API_KEY`, no external calls.
- **No vector databases, embeddings, or chunking.** Retrieval is by direct file search over plain markdown.
- **Self-contained.** Everything the project needs sits in one folder.

---

## What's inside the crate

1. **GGUF SLM core (`engine/llm_engine.py`)** — the local model, pre-configured for Apple Silicon (Metal), NVIDIA (CUDA), or CPU fallback.
2. **Two-tier living memory (`memory/`)**
   - **Tier 1 — Living Dossier (`DOSSIER.md`):** a fast-path cache. Frequently asked questions and answers are served instantly without rescanning documents.
   - **Tier 2 — Vectorless PageIndex (`PAGE_INDEX.json`):** a plain-table of contents tree over the markdown knowledge files. Zero embeddings, zero chunking.
3. **Context safeguard (`memory/context_budget.py`)** — tracks token usage so the model never runs out of context. It offloads old conversation first and keeps ingested documents intact.
4. **Ingestion protocols (`ingestion/protocols.py`)** — three guarantees:
   - **Anti-Parsing:** raw text is never rewritten or reformatted.
   - **Anti-Chunking:** documents are treated as complete wholes.
   - **Anti-Truncating:** content is never cut off mid-sentence.

---

## Quickstart

### 1. Install the model (once)

```bash
python -m pip install -r requirements.txt
python setup_models.py
```

The first run downloads the model weights automatically if they are not present.

### 2. Run

```bash
./run.sh
```

### 3. Use inside the interactive shell

- `!dossier` — view the living dossier.
- `!toc` — view the table-of-contents index.
- `!budget` — check context token usage.
- `!reset` — clear conversation turns, keep the model and memory.

### 4. Run as a Python crate motor

```python
from fleece import FleeceCrateMotor

motor = FleeceCrateMotor()
motor.set_task("Review python files for performance bottlenecks")
response = motor.execute("What should we look for first?")
print(response)
```
