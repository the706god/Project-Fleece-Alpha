# Project: Fleece Alpha 🐑

**The "Crate Motor" SLM build (Text Edition)** — a small, self-contained AI model equipped with **Mimir OCR** that you run **completely offline, on your own machine**. No internet needed after the first setup.

**Core model:** Qwen 2.5 Coder 3B Instruct (`Q4_K_M` GGUF)
**Ingestion & Memory Stack:** **Mimir OCR** (3-Pass Progressive Optical Sieve with Coordinate Delta-Masking + Two-Tier Vectorless Memory)

---

## What "local agent" means here

Fleece Alpha is a **tool for offloading work from frontier (cloud) agents so it can live locally**. You give it a task or a degraded legacy PDF/scan, Mimir OCR extracts and grounds every text block to normalized `[x0, y0, x1, y1]` coordinates without calling a server, and the model serves answers while keeping its own living notes.

- **No internet required.** Everything runs locally.
- **No cloud API keys.** No `OPENAI_API_KEY`, no AWS Textract, no Google Document AI.
- **No vector databases, embeddings, or chunking.** Retrieval is by direct file search over plain markdown via **Mimir OCR**.
- **Self-contained.** Everything the project needs sits in one folder.

---

## What's inside the crate

1. **GGUF SLM core (`engine/llm_engine.py`)** — the local model, pre-configured for Apple Silicon (Metal), NVIDIA (CUDA), or CPU fallback.
2. **Mimir OCR (`sieve_ocr.py` & `memory/`)**
   - **3-Pass Progressive Optical Sieve with Coordinate Delta-Masking (`engine/sieve_ocr.py`):**
     - **Pass 1 (OS-Native OCR):** Apple Vision / Windows OCR clears ~85% of clean text in `<150ms/page`.
     - **Coordinate Delta-Masking:** Locks in `>= 0.85` confidence blocks and crops only `< 0.85` bounding boxes (`12px` margin at `200 DPI`).
     - **Pass 2 (Targeted `RapidOCR` ONNX):** Runs on delta-masked sub-crops (~12%: faded print, stamps, tables) and projects coordinates back to full-page `[0.0000, 1.0000]` space.
     - **Pass 3 (In-Process Local VLM via `MiniCPM-V 2.6`):** Escalates stubborn cursive/marginalia crops (~3%) at `temperature=0.0` with Gate 3 quarantine (`needs_human_review = True` if `< 0.85` or `[?]`).
   - **Tier 1 — Mimir Living Dossier (`DOSSIER.md`):** a fast-path cache. Frequently asked questions and answers are served instantly without rescanning documents.
   - **Tier 2 — Mimir Vectorless PageIndex (`PAGE_INDEX.json`):** a plain table-of-contents tree over the markdown knowledge files. Zero embeddings, zero chunking.
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

### 2. Run Mimir OCR Benchmark or Launch Shell

```bash
python test_sieve_ocr.py
./run.sh
```

### 3. Use inside the interactive shell

- `!ocr /path/to/document.pdf` — ingest a PDF or image via the Mimir 3-Pass Progressive Optical Sieve.
- `!dossier` — view the Mimir living dossier.
- `!toc` — view the Mimir table-of-contents index.
- `!budget` — check context token usage.
- `!reset` — clear conversation turns, keep the model and memory.

### 4. Run as a Python crate motor

```python
from fleece import FleeceCrateMotor

motor = FleeceCrateMotor()
motor.ingest_document("legacy_record.pdf")
response = motor.execute("Summarize the itemized charges and cite coordinates.")
print(response)
```
