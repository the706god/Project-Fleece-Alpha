# Project: Fleece Alpha 🐑
> **The 'Crate Motor' SLM Build (Text Edition)**  
> **Core Model:** Qwen 2.5 Coder 3B Instruct (`Q4_K_M` GGUF)

Project: Fleece Alpha is a pre-packaged, self-contained Small Language Model build designed to act as a **crate motor** for AI applications. Drop it into your workflow, assign your tasks, and run it locally without fighting environment configurations or context limits.

---

## ⚡ What's in the Crate

1. **GGUF SLM Core (`engine/llm_engine.py`)**
   - Pre-configured for `qwen2.5-coder-3b-instruct-q4_k_m.gguf` (located in `models/model.gguf`).
   - Automated hardware acceleration: Apple Silicon (Metal), NVIDIA (CUDA), or multi-threaded CPU fallback.
2. **Two-Tier Living Memory Architecture (`memory/`)**
   - **Tier 1 — Living Dossier (`DOSSIER.md`):** Instant fast-path cache (~150 tokens) modeled after legacy markdown memory. Frequently requested facts and answers are cached here and served immediately without document rescanning.
   - **Continuous Auto-Updating:** Whenever a deep query resolves information from documents, the Living Dossier is automatically updated with the new Q&A pair and exact file/anchor citations.
   - **Tier 2 — Vectorless PageIndex (`PAGE_INDEX.json`):** Hierarchical Table of Contents tree navigation over markdown knowledge files in `storage/markdown/knowledge/`. Zero vector databases, zero embeddings, zero chunking.
3. **Context Limitation Safeguard (`memory/context_budget.py`)**
   - Dynamic budget allocation prevents "out-of-context" model crashes.
   - Preserves immutable System Anchors and Task Objectives while maintaining a rolling context window.
   - Automatically compacts conversational dialogue first to preserve ingested document text unbroken.
4. **Ingestion Protocols (`ingestion/protocols.py`)**
   - **Anti-Parsing:** Ingests raw data without destructive regex stripping or breaking whitespace/indentation.
   - **Anti-Chunking:** AST and markdown-aware boundary splits. Never slices code blocks, functions, or tables in half.
   - **Anti-Truncating:** Guarantees input boundaries are preserved safely without mid-sentence clipping.

---

## 🚀 Quickstart

### 1. Model Setup (Automated on First Run)
When you launch the engine for the first time, it automatically detects and downloads the verified `Qwen 2.5 Coder 3B Instruct` weights directly into `models/model.gguf`.

You can also pre-download the weights manually at any time:
```bash
python setup_models.py
```

### 2. Run via Turnkey Launcher
```bash
./run.sh
```

### 2. Interactive CLI Commands
Once inside the interactive shell, you can use built-in management commands:
- `!dossier` — View the live contents of `DOSSIER.md`.
- `!toc` — Inspect the vectorless Table of Contents knowledge index.
- `!budget` — Check active context token utilization.
- `!reset` — Clear conversation turns while keeping model and memory intact.

### 3. Assign a Task Directly from CLI
```bash
./run.sh --task "Review python files for performance bottlenecks" --prompt "What should we look for first?"
```

### 4. Use as a Python Crate Motor
```python
from fleece import FleeceCrateMotor

motor = FleeceCrateMotor()
motor.set_task("Act as a strict code auditor")
response = motor.execute("Audit this SQL schema for anti-patterns")
print(response)
```
