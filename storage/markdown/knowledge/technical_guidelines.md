# Technical Architecture Guidelines
date: 2026-10-09
tags: architecture, crate-motor, engineering

## Crate Motor Design Principles
A crate motor is a drop-in component that requires zero external setup.
The engine must be completely self-contained within its repo folder.
Hardware detection must occur dynamically without requiring manual flag tuning.

## Ingestion Protocol Specifications
The ingestion engine strictly adheres to three unbreakable protocols:
1. Anti-Parsing: Preserves raw markdown tables, syntax trees, and indentation.
2. Anti-Chunking: Never splits code blocks or paragraphs across arbitrary token limits.
3. Anti-Truncating: Never truncates prompts abruptly; utilizes head-and-tail compaction with explicit continuation notices.

## Context Budget Limits
The maximum working context is set to 16,384 tokens.
When memory usage exceeds 85% of capacity, the engine triggers automated offloading to the secondary markdown store.
Older dialogue turns are condensed into a rolling summary while immutable anchors remain preserved.
