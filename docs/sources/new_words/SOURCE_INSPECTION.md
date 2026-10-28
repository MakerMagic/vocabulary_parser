# SOURCE_INSPECTION.md — `new_words` Source Dataset Inspection

> **Source ID:** `new_words`  
> **Source Document:** [`acquisition/sources/new_words/new_words.md`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/new_words/new_words.md)  
> **SHA-256 Lock:** `6aac09b4631462c239e49c6bbbbebf0a2d30ee88acddfbb16debb780ce163ec7`  
> **File Size:** `30,161` bytes  
> **Line Count:** `692` lines  

---

## 1. Structural Overview

The document is organized into **56 numbered semantic clusters** containing **159 structured lexical entries**. Each lexical entry contains:
- Headword or multiword expression (e.g. `- Impact`, `- Give rise to`, `- Be capable of`)
- `Part of Speech` (e.g. `Noun`, `Verb`, `Adjective`, `Adverb`, `Phrasal verb`, `Verb phrase`, `Adjective phrase`, `Quantifier phrase`, `Adverbial phrase`, `Determiner`)
- `Russian Translation` (contextual Russian translation with 1 or 2 comma-separated alternatives)
- `English Explanation` (concise contextual definition suitable for study cards)

---

## 2. Quantitative Distribution

| Metric | Count |
|---|---|
| **Total Semantic Clusters** | `56` |
| **Total Extracted Entries** | `159` |
| **Unique Headwords (case-insensitive)** | `157` |
| **Duplicate Headwords** | `2` (`negligible` at #72 & #94; `augment` at #99 & #112) |
| **Questions Group at End** | `0` questions found in `new_words.md` |

### Part of Speech Distribution

- **Adjective:** 69
- **Verb:** 49
- **Noun:** 16
- **Adverb:** 10
- **Adjective phrase:** 3
- **Quantifier phrase:** 3
- **Adverbial phrase:** 3
- **Phrasal verb:** 2
- **Determiner:** 2
- **Verb phrase:** 1
- **Verb (third-person singular):** 1

---

## 3. Key Observations & Invariants for Pipeline Stages

1. **Multiword Expressions:**
   Expressions like `Lead to`, `Give rise to`, `Be capable of`, `In many cases`, `In no case`, `Under no condition`, `Contingent on`, `Hinge on`, `Financially secure`, `A proportion of`, `A smaller amount of`, and `Myriad of` represent cohesive lexical units and must not be fractured into isolated words.
2. **Russian Translation Alternatives:**
   132 entries contain 2 comma-separated translation alternatives; 27 entries contain 1 alternative. 0 entries exceed 2 alternatives.
3. **Cross-Cluster Duplicates:**
   `negligible` occurs under Cluster 28 (`Small`) and Cluster 36 (`Unimportant`).
   `augment` occurs under Cluster 37 (`Increase`) and Cluster 41 (`Improve`).
   Both occurrences carry distinct nuance and explanation tailored to the cluster and must be preserved as distinct records with cross-referencing.
4. **General Questions & `Type: Essential`:**
   Inspected the entire source text for questions or question mark punctuation. 0 general questions exist at the end of `new_words.md`. The data schema is extended with the `type` field (`type: "Essential"` or `null`) so that whenever question groups are processed, they receive `Type: Essential` and are exempt from elementary exclusion.
