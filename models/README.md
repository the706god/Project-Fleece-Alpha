# Model Directory: Project Fleece Alpha

This folder holds the local AI model brain files for Project Fleece Alpha.

Once these files are downloaded to your computer, Fleece Alpha runs completely offline. It never sends your words, code, or documents to the internet.

---

## What Is in This Folder

1. Core Text Model (`model.gguf`)
   - Brain: Qwen 3.5 4B Instruct.
   - Precision: Full Q8_0 precision (high accuracy with no cut corners).
   - What It Does: Reads, writes, organizes data, and writes code.
   - Memory Speed: Uses TurboQuant 4-bit memory packing (turbo4/turbo4) to give you 65,536 tokens of working memory. If TurboQuant is not supported on your system, it automatically steps down to standard q8_0 memory so it never crashes.

2. Optical Sieve Specialists (Mimir OCR Pass 3)
   - Specialist Brain: `Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf`
   - Specialist Eyes: `Qwen2.5-VL-7B-Instruct-mmproj-F16.gguf`
   - What They Do: These files sleep until you feed Fleece a very blurry scan, messy stamp, or handwritten note that passes 1 and 2 cannot read with high confidence. Once finished, they go right back to sleep so your computer stays fast.

---

## How to Download and Verify the Models

You can download and verify all the necessary model files with one command from the project root folder:

```bash
python setup_models.py
```

This script checks whether the models are already on your computer. If they are missing or damaged, it downloads them automatically and tests their file size.

---

## Model Specifications

- Core Brain File: `model.gguf`
- Architecture: Qwen 3.5 (4 Billion Parameters)
- Quantization: Q8_0 (8-bit quantization)
- KV Cache Mode: turbo4/turbo4 (with automatic q8_0 fallback)
- Context Window: 65,536 tokens
- Default Source: Hugging Face (`unsloth/Qwen3.5-4B-GGUF`)
- OCR Fallback Model: `Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` + `Qwen2.5-VL-7B-Instruct-mmproj-F16.gguf`
