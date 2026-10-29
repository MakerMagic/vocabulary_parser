# RENDERING Stage Backtesting Report (`RENDERING_BACKTESTING.md`)

> **Source:** `math_basics`  
> **Generated deterministically from:** `data/rendered/sources/math_basics/validation.json`  
> **Stage Status:** `completed`

## 1. Stage Execution Summary

- **What was processed:** Vocabulary Rendering display-ready validation for math_basics
- **Input artifact:** `data/pre_final/sources/math_basics/vocabulary.json` (SHA-256: `1aa53272c42cafd717eb98e835e8a9032a970138497ff1fd6385b72fa92d23a4`)
- **Output artifact:** `data/rendered/sources/math_basics/display_ready.json` (SHA-256: `N/A`)

| Metric | Count |
|---|---|
| **Records Entered Stage** | `274` |
| **Successfully Processed (Clean/Validated)** | `274` |
| **Excluded from Eligible Dataset (e.g. A1/A2)** | `0` |
| **Flagged for Review (`review_pending`)** | `0` |
| **Unresolved Blocking Errors (`error`)** | `0` |
| **Total Distinct Issue Occurrences** | `91` |
| **Unique Affected Records** | `91` |

## 4. Reproducible Backtesting Commands

Run the following commands from the repository root:

```powershell
.\.venv\Scripts\python.exe -c "from processors.rendering.renderer import render_source_dataset; render_source_dataset('math_basics')"
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source math_basics --word 'altitude'
.\.venv\Scripts\python.exe tools/vocabulary_review.py --source math_basics --word 'decimal'
```

## 5. Verification Procedure

1. Verify all 274 records are audited under zero-unresolved-issues rule.
2. Verify exactly 183 admitted records render active website-style cards.
3. Verify exactly 91 blocked records render diagnostic notices.
4. Verify 0 validation errors across rendering outputs.
