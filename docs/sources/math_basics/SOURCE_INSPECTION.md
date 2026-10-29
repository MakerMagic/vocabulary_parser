# Source Inspection Report: `math_basics`

> **Source ID:** `math_basics`  
> **Source File:** [`acquisition/sources/math_basics/math_basics.txt`](file:///c:/Users/user/Desktop/vocabulary_parser/acquisition/sources/math_basics/math_basics.txt)  
> **Source SHA-256:** `eb6ea47dabd2e54b17a514781edb9b577145d865d9928495cc40ab8cbf09e698`  
> **Preset Assigned:** `math_basics`  
> **Profile JSON:** [`inspections/sources/math_basics/profile.json`](file:///c:/Users/user/Desktop/vocabulary_parser/inspections/sources/math_basics/profile.json)

---

## 1. Overview & Dataset Profile

The `math_basics.txt` dataset is a specialized collection of **274 mathematical vocabulary entries** designed for students preparing for NUET mathematics.

Unlike general English vocabulary, every entry must be understood, translated, and defined strictly within **mathematics and quantitative reasoning**.

---

## 2. Structural Findings & Deduplication Audit

1. **Total Lines / Records:** 274 non-empty lines.
2. **Unique Terms:** 183 distinct terms.
3. **Repeated / Duplicate Terms:** 52 terms appear multiple times across the 12 topical sub-lists:
   - `decimal`, `equation`: 5 occurrences each.
   - `factor`, `fraction`, `integer`, `operation`, `quotient`, `rational`, `quantity`, `equivalent`, `graph`: 4 occurrences each.
   - `estimate`, `negative`, `positive`, `product`, `express`, `irrational`, `value`, `formula`, `property`: 3 occurrences each.
   - 33 terms appear 2 times each.
   - **Total redundant duplicate instances:** 91.
4. **Deduplication Strategy:**
   - Raw source records are 100% preserved (all 274 line items retained in RAW with precise line coordinates).
   - In the Cleaned and Pre-Final outputs, the primary (first) occurrence of each term is retained as active and eligible (183 records).
   - The 91 duplicate occurrences are tagged with `status: "excluded"`, `exclusion_reason: "duplicate_term"`, `final_output_eligible: false`, and an auditable link to `duplicate_master_id`.
5. **Multiword Expressions:**
   - `absolute value` (line 25, line 124) is the only multiword expression; preserved as a compound unit.
6. **Cross-Preset Overlaps:**
   - 19 words overlap with `uclouvain` (`acute`, `base`, `compare`, `convert`, `derive`, `equal`, `equivalent`, `express`, `function`, `identical`, `linear`, `negative`, `opposite`, `parallel`, `perpendicular`, `positive`, `proof`, `relative`, `right`).
   - 4 words overlap with `new_words` (`equivalent`, `function`, `identical`, `positive`).
   - 2 words overlap with `nature` (`altitude`, `cone`).
   - In each case, `math_basics` requires strict mathematical interpretation (e.g., `altitude` = geometric height; `cone` = geometric solid; `derive` = deduce formula / differentiate; `function` = mathematical mapping).
