# </> Code Similarity Checker

A tool that detects structural similarity between two source code files — resistant to variable renaming, reformatting, and comment changes. Built to demonstrate real plagiarism-detection techniques, not a wrapper around an existing library.

## How it works

1. **Tokenization** — source code is broken into normalized tokens. Variable and function names become `VAR`, numbers become `NUM`, strings become `STR`, while keywords (`if`, `for`, `def`...) and operators are preserved. This means two functions that are logically identical but use different variable names produce identical token sequences.

2. **K-gram shingling** — the token sequence is split into overlapping windows of `k` tokens (default k=5), each hashed into a single integer. This captures partial matches, not just whole-file identity.

3. **Winnowing** — implements the winnowing algorithm (Schleimer, Wilkerson & Aiken, 2003) to select a representative subset of hashes from each sliding window, guaranteeing any shared region of a minimum length is detected while discarding redundant hashes. This is the same family of technique used by real plagiarism detectors like MOSS.

4. **Similarity scoring** — Jaccard similarity (intersection over union) between the two fingerprint sets gives a fair 0-100% score.

5. **Line mapping** — every match is traced back to its original source line numbers, so the frontend can highlight exactly which lines overlap.

## Tech stack
**Backend:** Python, FastAPI
**Frontend:** HTML, CSS, vanilla JavaScript (dark, diff-viewer style UI)
**Core logic:** custom tokenizer, hashing, and winnowing algorithm — no external similarity libraries used

## Run locally
1. Clone the repo
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload --port 8000`
5. Open `frontend/index.html` in a browser

## API
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /compare | Upload two files, returns similarity score, fingerprints, and matched line numbers |

## Known limitations
- Tokenizer currently targets Python syntax specifically
- No support yet for detecting reordered code blocks (only contiguous k-gram matches)
- Designed for pairwise comparison; not yet optimized for many-to-many batch checking

## Future improvements
- Support additional languages (Java, JavaScript)
- Batch comparison across many files (e.g., a whole class's submissions)
- Adjustable k and window-size sliders in the UI

---
Built by Aaryan Subedi