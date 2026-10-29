# Stage Issues Report: `math_basics`

> **Source ID:** `math_basics`  
> **Source File:** `acquisition/sources/math_basics/math_basics.txt`  
> **Preset:** `math_basics`  

---

## 1. Issue Categories & Counts

| Issue Category | Total Occurrences | Unique Affected Records | Affected Identifiers (Sample) | Root Cause | Status |
|---|---|---|---|---|---|
| **Duplicate Vocabulary Entry** | **91** | **91** (from 52 terms) | `math_vocab_026` (`addition`), `math_vocab_028` (`decimal`), `math_vocab_030` (`division`), `math_vocab_032` (`estimate`), `math_vocab_035` (`factor`), `math_vocab_037` (`fraction`), `math_vocab_038` (`integer`), etc. | Repeated inclusion across 12 distinct study sections in source text. | **Resolved** (preserved in RAW; excluded from final eligible output with `duplicate_master_id` pointer). |
| **Validation Contract Defects** | **0** | **0** | None | N/A | **Passed** |
| **Circular English Explanation** | **0** | **0** | None | Prevented via strict non-circularity definitions. | **Passed** |
| **Russian Translation Excess (>2)** | **0** | **0** | None | Enforced <=2 mathematical translations rule. | **Passed** |
| **Unmapped CEFR / Difficulty** | **0** | **0** | None | All 183 terms mapped to established CEFR tiers. | **Passed** |

---

## 2. Detailed Duplicate Accounting

1. **5 occurrences:** `decimal`, `equation`.
2. **4 occurrences:** `equivalent`, `factor`, `fraction`, `graph`, `integer`, `operation`, `quantity`, `quotient`, `rational`.
3. **3 occurrences:** `estimate`, `express`, `formula`, `irrational`, `negative`, `positive`, `product`, `property`, `value`.
4. **2 occurrences:** `absolute value`, `addition`, `area`, `coefficient`, `conversion`, `convert`, `coordinate`, `cube`, `digit`, `distance`, `division`, `exponent`, `expression`, `inequality`, `linear`, `magnitude`, `multiple`, `multiplication`, `percent`, `perimeter`, `plane`, `proportional`, `ratio`, `slope`, `square`, `subtraction`, `sum`, `table`, `unit`, `vertical`, `volume`.

**Total redundant occurrences excluded from eligible output:** 91.  
**Retained master entries:** 183.
