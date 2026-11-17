# Project: Fleece Alpha

The Crate Motor AI Build (Text Edition) — a fast, private AI model that runs completely on your own computer. Once set up, it requires zero internet connection and sends zero data to the cloud.

Core Model: Qwen 3.5 4B Instruct (Full Q8_0 Precision)
Memory & Acceleration: Native Metal TurboQuant (turbo4/turbo4) with 65,536-token context capacity
Document Stack: Mimir OCR (3-Pass Progressive Optical Sieve) + Two-Tier Vectorless Memory System

---

## Why Fleece Exists: Stop Using a Racecar to Haul Groceries

Frontier AI models like Claude, ChatGPT, and Gemini are like supercars. They are powerful, but they cost real money every single time you use them.

The biggest waste of money in AI today is not long conversations. It is having dozens of background agents running all day doing small, repetitive chores—formatting text, cleaning data, organizing files, and drafting routine notes. Doing that on cloud models burns through your daily message caps and racks up huge monthly API bills.

Project Fleece was created to solve that problem. It is your local crate motor. You offload high-volume text and data chores to your own computer for zero dollars per month, zero token bills, zero rate limits, and 100% privacy. You keep your expensive cloud models for the rare, massive tasks that actually need them.

---

## What Fleece Alpha Is Designed For

Fleece Alpha is the speed-first text engine of the Fleece suite. It is built to chew through high-volume text, scripts, lists, and numbers at blazing speed. 

While frontier cloud models make you wait in line, meter every word, and throttle your account when you send too many requests, Fleece Alpha runs right on your computer's chip. It responds instantly, follows strict formatting rules, and never gets tired.

### Updated Technical Specs

- Brain: Qwen 3.5 4B Instruct with full Q8_0 precision (no fuzzy math or lost accuracy).
- TurboQuant KV Cache: Uses advanced 4-bit memory packing (turbo4/turbo4). This cuts memory usage by nearly four times and unlocks a huge 65,536-token workspace on ordinary hardware.
- Memory Fallback Guard: If run on an older machine without TurboQuant, it smoothly steps down to standard q8_0 memory instead of crashing.
- Zero-Destruction Guarantee: Fleece follows three strict rules:
  1. Anti-Parsing: Raw text is never scrambled or changed.
  2. Anti-Chunking: Documents are kept whole, never chopped into loose paragraphs.
  3. Anti-Truncating: Information is never cut off mid-thought.

---

## How Fleece Remembers: Two-Tier Vectorless Memory

Most AI systems use complex "vector databases." They chop your files into little pieces, turn them into confusing math numbers, and lose track of page numbers. Fleece throws all of that out and replaces it with a clean, two-tier system:

- Tier 1 Memory (Fast Working Memory — The Living Dossier): This is your agent's notepad. It automatically records important facts, active tasks, and verified answers as work happens. When you ask a question it already answered, it gives you the answer instantly without re-reading the whole file.
- Tier 2 Memory (Book Index Navigation — The PageIndex Tree): Instead of guessing where information lives, Fleece builds an interactive table-of-contents tree. It knows exactly which page and line every fact came from, just like the index at the back of a textbook.
- Cold Backup (Secondary Markdown Store): Every document you ingest is safely backed up as plain, clean Markdown on your local drive.

---

## Bonus Feature: Mimir OCR

Most local AI projects drop a raw model in your lap and expect you to figure out file ingestion yourself. We packaged **Mimir OCR**—the proprietary OCR stack from our upcoming **MimirOS** release—directly into Fleece Alpha so you get a real, multi-purpose local AI tool right out of the box.

How you use it is completely up to you. Whether your workflow touches medical, legal, financial, administrative, or everyday files, Mimir OCR is built to read whatever documents and forms you feed it with fidelity and accuracy—offline and under your control.

Under the hood, it runs a 3-pass pipeline (OS-native reading first, RapidOCR on low-confidence boxes, and a sleeping Chandra-OCR-2 fallback only for tough scans) without chopping or cutting off your pages. Combined with Fleece Alpha's portable speed, you get real-world local AI and file reading on your machine anywhere in the world.

---

## Real-World Possibilities (Industry-Agnostic)

You do not need to be a programmer or a tech company to get massive value out of Fleece Alpha. Here is what it does right out of the box:

- Turning Messy Logs into Clean Tables: Feed in thousands of lines of raw system exports, customer notes, or equipment readings. Alpha formats them into clean, standardized spreadsheets in seconds.
- Drafting and Polishing Business Writing: Have an agent summarize lengthy email threads, polish project updates, or write clear operational steps without paying a cloud fee.
- Script and Code Automation: Write, check, and fix Python scripts, terminal commands, or database queries locally with zero risk of company code leaking to the public internet.
- Document Fact Checking: Ask specific questions about long manuals, warranty handbooks, or rulebooks. Alpha finds the exact sentence and page without guessing.

---

## Ideal System Specifications

### Mac (Apple Silicon)
- Best: Any Mac with M1 Pro, M2 Pro, M3 Pro, M4, or better (16 GB to 32 GB Unified Memory).
- Minimum: M1 / M2 / M3 Mac with 8 GB RAM.
- Operating System: macOS 13 (Ventura) or later.

### Windows PC
- Best: 8-core CPU (Intel i7/i9 12th gen+ or AMD Ryzen 7/9) with 16 GB to 32 GB RAM, and an NVIDIA GPU (RTX 3060, 4060, or better with 6 GB+ VRAM).
- Minimum: 4-core CPU with 16 GB system RAM (runs on CPU).
- Operating System: Windows 10 or 11 (64-bit).

### Linux
- Best: Modern x86_64 or ARM64 workstation with 16 GB to 32 GB RAM and an NVIDIA GPU (CUDA support).
- Minimum: 4-core modern CPU with 16 GB RAM.

---

## What to Expect for Response Speeds

- On Apple Silicon Mac (M1 Pro / M2 / M3): Blazing fast. You will see 45 to 65+ words per second. Answers appear almost immediately with zero network lag.
- On Windows / Linux with NVIDIA GPU: 40 to 60+ words per second.
- On Standard CPU Only (No GPU): 12 to 20 words per second (reads comfortably like someone typing in real time).
- Document Reading Speed (Mimir OCR): Less than 1 second per page for 85%+ of standard documents.

---

## Quickstart Guide

### 1. Set Up the Environment

```bash
python -m pip install -r requirements.txt
python setup_models.py
```

### 2. Test Document Reading or Start the Shell

```bash
# Run the built-in document reading test:
python test_sieve_ocr.py

# Launch the interactive terminal:
./run.sh
```

### 3. Useful Commands Inside the Shell

- `!audit /path/to/skill` — Check if an outside prompt or agent skill can run locally on Fleece.
- `!ocr /path/to/file.pdf` — Read a document and store it in permanent, unbroken memory.
- `!dossier` — Open your active working notepad.
- `!toc` — View the document table of contents.
- `!budget` — Check how much of your 65,536-token workspace is currently in use.
- `!reset` — Clear the conversation while keeping all loaded documents intact.

### 4. Use Inside Python Scripts

```python
from fleece import FleeceCrateMotor

# 1. Start the local engine
motor = FleeceCrateMotor()

# 2. Add a document
motor.ingest_document("operations_manual.pdf")

# 3. Ask your question
answer = motor.execute("What are the three steps required before shutting down power?")
print(answer)
```

---

## Auditing Outside Agents and Skills

Fleece Alpha includes a built-in auditor. It scans prompts and agent setups made for cloud services (like OpenAI, LangChain, or Claude) and tells you if they can run locally for free.

```bash
./audit_agent.py /path/to/my_skill/
```
