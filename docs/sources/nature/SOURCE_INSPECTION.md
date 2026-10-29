# Nature Vocabulary Simplified — Source Inspection (`SOURCE_INSPECTION.md`)

> **Source ID:** `nature`  
> **Source Document:** [`acquisition/sources/nature/Nature_Vocabulary_Simplified.csv`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/nature/Nature_Vocabulary_Simplified.csv)  
> **SHA-256 Lock:** `215bdb89ad6910d4edeeddebf980523bd2ad55616c651cf908cbdf713d0809bc`  
> **Inspection Profile:** [`inspections/sources/nature/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/nature/profile.json)

---

## 1. Document Structure & Ingestion Findings

- **Format:** CSV with UTF-8 byte order mark (`utf-8-sig`).
- **Dimensions:** Exactly 170 lines (1 header row + 169 data rows).
- **Header Columns:**
  1. `Word` — Primary English lexical entry.
  2. `Part of Speech` — Grammatical classification (`Noun`, `Plural Noun`, `Adjective`, `Proper Noun`, `Noun (Abbreviation)`).
  3. `Russian Translation 1` — Primary Russian contextual translation alternative.
  4. `Russian Translation 2` — Secondary Russian contextual translation alternative.
  5. `English Explanation` — Flashcard-ready semantic definition in English.
  6. `Topic` — Nature domain categorization (7 scientific domains).

---

## 2. Statistical Breakdown

- **Total Entries:** 169 records.
- **Unique Headwords:** 169 (0 duplicate verbatim entries).
- **Part of Speech Distribution:**
  - `Noun`: 127
  - `Plural Noun`: 23
  - `Adjective`: 17
  - `Noun (Abbreviation)`: 1 (`DNA`)
  - `Proper Noun`: 1 (`Mars`)
- **Scientific Topic Distribution:**
  - `Earth & Geography`: 43
  - `Living Organisms`: 34
  - `Ecology & Environment`: 23
  - `Physics & Chemistry`: 20
  - `Plants & Ecosystems`: 20
  - `Climate & Weather`: 19
  - `Space & Astronomy`: 10

---

## 3. Linguistic & Lexical Nuances

1. **Singular / Plural Paired Variants in Source:**
   - `#52 Nutrients` (Plural Noun) vs. `#121 Nutrient` (Noun)
   - `#66 Resources` (Plural Noun) vs. `#115 Resource` (Noun)
   - `#70 Plastic` (Noun) vs. `#153 Plastics` (Plural Noun)
   - `#90 Volcanoes` (Plural Noun) vs. `#97 Volcano` (Noun)
   Both singular and plural forms are distinct records in the user-supplied CSV and will be preserved faithfully.
2. **Em-Dash in Russian Translation Phrases:**
   - `#108 Whales` alternative 2: `Морские млекопитающие — киты`
   - `#152 Flies` alternative 2: `Летающие насекомые — мухи`
   Validation regex accommodates unicode em-dash (`\u2014`).
3. **Flashcard Explanations:**
   - All 169 explanations exceed the minimum 15-character threshold.
   - `#165 Cone` contains `cone-shaped` which references the headword; non-circular phrasing is applied during enrichment.
4. **Elementary A1/A2 Exclusions:**
   - 11 A1 items (`Food`, `Sun`, `Light`, `Body`, `Plant`, `Animal`, `Fish`, `Star`, `Sugar`, `Fruit`, `Egg`) and 28 A2 items identified according to Cambridge EVP benchmarks and excluded from active flashcard study while preserving their complete records.
