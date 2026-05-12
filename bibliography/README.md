# blueSteel Bibliography

This subproject contains the literature database for the broader `blueSteel` repository.

The bibliography focuses on steelhead ecology, marine migration, climate impacts, telemetry, kelts, habitat use, conservation biology, and related salmonid research.

---

# Purpose

This directory serves as:

- a curated literature review
- a searchable scientific knowledge base
- a citation archive
- a structured metadata repository
- a foundation for future synthesis and analysis

The long-term goal is to integrate:
- papers
- summaries
- thematic metadata
- figures
- analyses
- code references
- ecological concepts

into a single reproducible research workflow.

---

# Directory Structure

```text
bibliography/
├── README.md
├── bibliography.md
├── index.html
├── papers/
├── metadata/
│   └── papers.yaml
├── templates/
│   └── bibliography-entry.md
└── exports/
```

---

# Core Files

## bibliography.md

Primary human-readable bibliography.

Contains:
- formatted citations
- methods/findings summaries
- thematic tags
- PDF links

This is the canonical editable bibliography source.

---

## index.html

Browser-renderable version of the bibliography.

Generated from `bibliography.md`.

Useful for:
- browsing
- sharing
- quick searching
- local reading

---

## papers/

Contains PDF source papers.

Naming convention:

```text
Author_Year_Journal.pdf
```

Example:

```text
Courtney_2025_Animal_Biotelemetry.pdf
```

Avoid spaces when possible.

---

## metadata/papers.yaml

Structured metadata for all bibliography entries.

Contains:
- citation keys
- themes
- methods
- geography
- DOI
- keywords
- modeling approaches

This file enables future:
- automated indexing
- search
- synthesis
- visualization
- literature graphing
- AI retrieval workflows

---

# Bibliography Entry Format

Each entry should include:

1. Citation key
2. Full citation
3. DOI link
4. Summary paragraph
5. PDF link
6. Optional thematic tags

---

# Writing Style

Summaries should:

- emphasize methods and findings
- distinguish evidence from speculation
- remain concise and technical
- avoid hype language
- prioritize ecological interpretation

Important recurring themes include:

- marine survival
- telemetry
- thermal ecology
- kelts
- repeat spawning
- climate impacts
- marine competition
- migration ecology
- ocean distribution
- survival modeling
- conservation biology

---

# Workflow

## Adding a New Paper

1. Add PDF to:

```text
papers/
```

2. Create/update bibliography entry in:

```text
bibliography.md
```

3. Add metadata record to:

```text
metadata/papers.yaml
```

4. Regenerate:

```text
index.html
```

5. Commit changes.

---

# Recommended Git Workflow

Example commits:

```bash
git commit -m "Add Gulf of Alaska telemetry paper"
```

Avoid vague commits like:

```bash
git commit -m "update"
```

---

# AI-Assisted Workflow

This repository is designed to work well with:
- GitHub Copilot
- ChatGPT
- VS Code
- future AI-assisted literature tools

Copilot may assist with:
- formatting
- metadata extraction
- markdown editing
- repo organization
- HTML generation

Scientific interpretation and synthesis should always be reviewed by a human.

---

# Future Development

Planned future capabilities may include:

- BibTeX export
- DOI auto-resolution
- thematic indices
- Quarto integration
- Obsidian integration
- citation graphs
- interactive visualizations
- synthesis notebooks
- automated literature review generation
- cross-linking between code and literature

---

# Source of Truth

GitHub repository state is authoritative.

Generated drafts or local artifacts should not be considered canonical until committed and pushed.
