# Nature Stage Issues & Resolution Log (`STAGE_ISSUES.md`)

> **Source ID:** `nature`  
> **Source Document:** [`acquisition/sources/nature/Nature_Vocabulary_Simplified.csv`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/nature/Nature_Vocabulary_Simplified.csv)

---

## Issue Summary Across Executed Stages

| Stage | Issue Category | Total Occurrences | Unique Records | Status |
|---|---|---|---|---|
| **Acquisition** | UTF-8 Byte Order Mark (`\ufeff`) | 1 | 1 file | Resolved via `utf-8-sig` decoding |
| **Cleaning** | Elementary A1/A2 Exclusions | 27 | 27 | Excluded from final output (`final_output_eligible: false`) |
| **Cleaning** | A2 Exclusion Overrides (Approved Restorations) | 12 | 12 | Restored to eligible final dataset (`final_output_eligible: true`, Easy) |
| **Enrichment** | Redundant Second Russian Translations Pruned | 131 | 131 | Pruned to 1 precise translation (e.g. `whales → киты`) |
| **Enrichment** | Circular Headword Lemma in Explanation (`#165 Cone`) | 1 | 1 | Resolved via non-circular flashcard definition |
| **Validation** | Blocking Contract Errors | 0 | 0 | Clean pass |

---

## Itemized Categorized Reports

### Category: A2 Exclusion Overrides / Restored Words (12 records)
- **Count:** 12 records.
- **Affected IDs:**
  - `nature_vocab_029 Wind` (`ветер`)
  - `nature_vocab_047 Oil` (`нефть`)
  - `nature_vocab_074 Lake` (`озеро`)
  - `nature_vocab_083 Salt` (`соль`)
  - `nature_vocab_108 Whales` (`киты`)
  - `nature_vocab_109 Stomach` (`желудок`)
  - `nature_vocab_110 Seed` (`семя`)
  - `nature_vocab_124 Bone` (`кость`)
  - `nature_vocab_127 Farming` (`сельское хозяйство; земледелие`)
  - `nature_vocab_129 Roots` (`корни`)
  - `nature_vocab_152 Flies` (`мухи`)
  - `nature_vocab_167 Bugs` (`насекомые; жучки`)
- **Actual Problem:** Words were previously excluded under broad A1/A2 filtering.
- **Root Cause:** Over-exclusion of fundamental domain-relevant nature terms.
- **Corrective Action:** Added `NATURE_A2_EXCLUSION_OVERRIDES` in `processors/normalization/cleaner_nature.py` restoring all 12 words to active curriculum status with `difficulty: "Easy"`, `preset: "nature"`, and `final_output_eligible: true`.
- **Status:** Resolved / Enforced.
- **Reproduction:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source nature --word "Whales"`

### Category: Redundant Second Russian Translations (131 records pruned)
- **Count:** 131 records pruned.
- **Actual Problem:** 131 entries contained redundant descriptive paraphrases or dictionary definitions in `Russian Translation 2` (e.g., `whales` had `морские млекопитающие — киты`, `flies` had `летающие насекомые — мухи`, `wind` had `поток воздуха`).
- **Root Cause:** Source dataset author provided textbook definitions or expansions rather than distinct lexical synonyms.
- **Corrective Action:** Enforced single precise translation rule for entries lacking a distinct, genuinely useful lexical alternative in `processors/enrichment/enricher_nature.py`. Exactly 38 entries with complementary meanings retain 2 alternatives; 131 entries now carry 1 precise translation.
- **Status:** Resolved.
- **Reproduction:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source nature --word "Whales"`

### Category: Remaining Elementary CEFR A1/A2 Exclusions (27 records)
- **Count:** 27 records.
- **Affected IDs:**
  - 11 A1 records: `nature_vocab_003 Light`, `nature_vocab_004 Food`, `nature_vocab_006 Sun`, `nature_vocab_010 Body`, `nature_vocab_016 Plant`, `nature_vocab_027 Animal`, `nature_vocab_032 Fish`, `nature_vocab_061 Star`, `nature_vocab_078 Sugar`, `nature_vocab_099 Fruit`, `nature_vocab_104 Egg`.
  - 16 A2 records: `nature_vocab_002 Earth`, `nature_vocab_009 Space`, `nature_vocab_013 Moon`, `nature_vocab_019 Planet`, `nature_vocab_021 Ice`, `nature_vocab_025 Natural`, `nature_vocab_035 Rocks`, `nature_vocab_037 Ground`, `nature_vocab_043 Field`, `nature_vocab_044 Brain`, `nature_vocab_060 Forest`, `nature_vocab_063 Skin`, `nature_vocab_070 Plastic`, `nature_vocab_085 Clouds`, `nature_vocab_096 Desert`, `nature_vocab_153 Plastics`.
- **Actual Problem:** Basic high-frequency words familiar to introductory English learners.
- **Corrective Action:** Excluded from active flashcards (`final_output_eligible: false`) while preserved in all intermediate datasets.
- **Status:** Enforced.
- **Reproduction:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source nature --word "Food"`

### Category: Circular Headword Lemma in Explanation (1 record)
- **Count:** 1 record (`nature_vocab_165 Cone`).
- **Actual Problem:** Source explanation was `"The cone-shaped part of a volcano built from lava and ash."` which circularly contained `cone`.
- **Corrective Action:** Rephrased in enrichment stage to: `"A steep, sloping triangular mound around a volcano vent built from erupted lava and ash."`
- **Status:** Resolved.
