# CLEAN Stage Issues Report (`CLEAN_ISSUES.md`)

> **Source:** `uclouvain`  
> **Generated deterministically from:** `data/clean/sources/uclouvain/validation.json`  
> **Total Issue Occurrences:** `36`  
> **Unique Affected Records:** `36`

```text
ISSUE SUMMARY — UCLOUVAIN / CLEAN
Mixed orthography preservation (UK/US): 6
Parenthetical or phrasal modifier syntax: 1
Vocabulary below A1/A2 exclusion threshold: 29
TOTAL DISTINCT ISSUES: 36
UNIQUE AFFECTED RECORDS: 36
```

---

## 1. Issue Summary by Error Category

| Error Category | Issue Occurrences | Unique Records | Primary Severity |
|---|---|---|---|
| `Mixed orthography preservation (UK/US)` | `6` | `6` | `info_notice` |
| `Parenthetical or phrasal modifier syntax` | `1` | `1` | `review_notice` |
| `Vocabulary below A1/A2 exclusion threshold` | `29` | `29` | `excluded` |
| **TOTAL DISTINCT ISSUES** | **`36`** | **`36`** | |

---

## 2. Itemized Issues Grouped by Error Category

### Category: Mixed orthography preservation (UK/US) (Count: 6)

- **Affected Vocabulary Entries:** `analyse` (#16), `characterise` (#38), `emphasize` (#91), `favour` (#114), `summarise` (#218), `favourable` (#283)

#### [MIXE-001] `#16` (`uclouvain_vocab_016`) — `analyse`

- **Problem Description:** Preserved supplied spelling 'analyse' (british_ise_or_our; counterpart: 'analyze').
- **Actual Observed Output:** `word='analyse' (british_ise_or_our)`
- **Expected Output:** `Supplied spelling 'analyse' preserved intact`
- **Root Cause:** Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.
- **Corrective Action:** Preserve supplied spelling in 'word'; do not mutate spelling convention.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "analyse"`
- **Resolution Status:** `preserved_supplied_orthography`

#### [MIXE-002] `#38` (`uclouvain_vocab_038`) — `characterise`

- **Problem Description:** Preserved supplied spelling 'characterise' (british_ise_or_our; counterpart: 'characterize').
- **Actual Observed Output:** `word='characterise' (british_ise_or_our)`
- **Expected Output:** `Supplied spelling 'characterise' preserved intact`
- **Root Cause:** Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.
- **Corrective Action:** Preserve supplied spelling in 'word'; do not mutate spelling convention.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "characterise"`
- **Resolution Status:** `preserved_supplied_orthography`

#### [MIXE-003] `#91` (`uclouvain_vocab_091`) — `emphasize`

- **Problem Description:** Preserved supplied spelling 'emphasize' (american_or_oxford_ize; counterpart: 'emphasise').
- **Actual Observed Output:** `word='emphasize' (american_or_oxford_ize)`
- **Expected Output:** `Supplied spelling 'emphasize' preserved intact`
- **Root Cause:** Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.
- **Corrective Action:** Preserve supplied spelling in 'word'; do not mutate spelling convention.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "emphasize"`
- **Resolution Status:** `preserved_supplied_orthography`

#### [MIXE-004] `#114` (`uclouvain_vocab_114`) — `favour`

- **Problem Description:** Preserved supplied spelling 'favour' (british_ise_or_our; counterpart: 'favor').
- **Actual Observed Output:** `word='favour' (british_ise_or_our)`
- **Expected Output:** `Supplied spelling 'favour' preserved intact`
- **Root Cause:** Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.
- **Corrective Action:** Preserve supplied spelling in 'word'; do not mutate spelling convention.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "favour"`
- **Resolution Status:** `preserved_supplied_orthography`

#### [MIXE-005] `#218` (`uclouvain_vocab_218`) — `summarise`

- **Problem Description:** Preserved supplied spelling 'summarise' (british_ise_or_our; counterpart: 'summarize').
- **Actual Observed Output:** `word='summarise' (british_ise_or_our)`
- **Expected Output:** `Supplied spelling 'summarise' preserved intact`
- **Root Cause:** Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.
- **Corrective Action:** Preserve supplied spelling in 'word'; do not mutate spelling convention.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "summarise"`
- **Resolution Status:** `preserved_supplied_orthography`

#### [MIXE-006] `#283` (`uclouvain_vocab_283`) — `favourable`

- **Problem Description:** Preserved supplied spelling 'favourable' (british_ise_or_our; counterpart: 'favorable').
- **Actual Observed Output:** `word='favourable' (british_ise_or_our)`
- **Expected Output:** `Supplied spelling 'favourable' preserved intact`
- **Root Cause:** Source list contains authentic mixed British (-ise/-our) and American (-ize) orthography.
- **Corrective Action:** Preserve supplied spelling in 'word'; do not mutate spelling convention.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "favourable"`
- **Resolution Status:** `preserved_supplied_orthography`

### Category: Parenthetical or phrasal modifier syntax (Count: 1)

- **Affected Vocabulary Entries:** `account (for)` (#2)

#### [PARE-001] `#2` (`uclouvain_vocab_002`) — `account (for)`

- **Problem Description:** Preserved original word 'account (for)' while separating base lemma 'account' and particle (for).
- **Actual Observed Output:** `word='account (for)', lemma='account', modifier='for'`
- **Expected Output:** `lemma='account', modifier=(for)`
- **Root Cause:** Source specifies required phrasal preposition in parentheses.
- **Corrective Action:** Preserve exact word in 'word', separate base lemma and particle non-destructively.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "account (for)"`
- **Resolution Status:** `separated_non_destructively`

### Category: Vocabulary below A1/A2 exclusion threshold (Count: 29)

- **Affected Vocabulary Entries:** `be` (#33), `become` (#34), `can` (#36), `choose` (#39), `fail` (#113), `follow` (#117), `show` (#207), `use` (#229), `write` (#232), `correct` (#262), `difficult` (#268), `early` (#271), `far` (#282), `great` (#292), `high` (#293) ... and 14 more

#### [VOCA-001] `#33` (`uclouvain_vocab_033`) — `be`

- **Problem Description:** Vocabulary entry 'be' is elementary A1 level (Elementary primary auxiliary and copular verb (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='be' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'be' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "be"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-002] `#34` (`uclouvain_vocab_034`) — `become`

- **Problem Description:** Vocabulary entry 'become' is elementary A1 level (Elementary linking verb (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='become' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'become' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "become"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-003] `#36` (`uclouvain_vocab_036`) — `can`

- **Problem Description:** Vocabulary entry 'can' is elementary A1 level (Elementary modal auxiliary verb (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='can' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'can' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "can"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-004] `#39` (`uclouvain_vocab_039`) — `choose`

- **Problem Description:** Vocabulary entry 'choose' is elementary A1 level (Basic high-frequency action verb (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='choose' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'choose' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "choose"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-005] `#113` (`uclouvain_vocab_113`) — `fail`

- **Problem Description:** Vocabulary entry 'fail' is elementary A2 level (Basic elementary verb (Cambridge EVP A2) (CEFR A2 benchmark)).
- **Actual Observed Output:** `word='fail' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A2) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A2).
- **Corrective Action:** Exclude 'fail' (A2) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "fail"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-006] `#117` (`uclouvain_vocab_117`) — `follow`

- **Problem Description:** Vocabulary entry 'follow' is elementary A2 level (Basic elementary motion/sequence verb (Cambridge EVP A2) (CEFR A2 benchmark)).
- **Actual Observed Output:** `word='follow' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A2) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A2).
- **Corrective Action:** Exclude 'follow' (A2) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "follow"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-007] `#207` (`uclouvain_vocab_207`) — `show`

- **Problem Description:** Vocabulary entry 'show' is elementary A1 level (Elementary transitive verb (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='show' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'show' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "show"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-008] `#229` (`uclouvain_vocab_229`) — `use`

- **Problem Description:** Vocabulary entry 'use' is elementary A1 level (Elementary high-frequency utility verb (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='use' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'use' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "use"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-009] `#232` (`uclouvain_vocab_232`) — `write`

- **Problem Description:** Vocabulary entry 'write' is elementary A1 level (Elementary literacy verb (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='write' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'write' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "write"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-010] `#262` (`uclouvain_vocab_262`) — `correct`

- **Problem Description:** Vocabulary entry 'correct' is elementary A1 level (Elementary evaluation adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='correct' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'correct' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "correct"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-011] `#268` (`uclouvain_vocab_268`) — `difficult`

- **Problem Description:** Vocabulary entry 'difficult' is elementary A1 level (Elementary difficulty descriptor (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='difficult' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'difficult' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "difficult"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-012] `#271` (`uclouvain_vocab_271`) — `early`

- **Problem Description:** Vocabulary entry 'early' is elementary A1 level (Elementary temporal adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='early' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'early' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "early"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-013] `#282` (`uclouvain_vocab_282`) — `far`

- **Problem Description:** Vocabulary entry 'far' is elementary A1 level (Elementary spatial distance adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='far' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'far' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "far"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-014] `#292` (`uclouvain_vocab_292`) — `great`

- **Problem Description:** Vocabulary entry 'great' is elementary A1 level (Elementary qualitative adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='great' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'great' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "great"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-015] `#293` (`uclouvain_vocab_293`) — `high`

- **Problem Description:** Vocabulary entry 'high' is elementary A1 level (Elementary spatial dimension adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='high' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'high' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "high"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-016] `#294` (`uclouvain_vocab_294`) — `human`

- **Problem Description:** Vocabulary entry 'human' is elementary A2 level (Basic biological descriptor (Cambridge EVP A2) (CEFR A2 benchmark)).
- **Actual Observed Output:** `word='human' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A2) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A2).
- **Corrective Action:** Exclude 'human' (A2) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "human"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-017] `#298` (`uclouvain_vocab_298`) — `important`

- **Problem Description:** Vocabulary entry 'important' is elementary A1 level (Basic high-frequency adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='important' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'important' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "important"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-018] `#308` (`uclouvain_vocab_308`) — `interesting`

- **Problem Description:** Vocabulary entry 'interesting' is elementary A1 level (Elementary descriptive adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='interesting' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'interesting' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "interesting"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-019] `#310` (`uclouvain_vocab_310`) — `large`

- **Problem Description:** Vocabulary entry 'large' is elementary A1 level (Elementary physical size descriptor (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='large' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'large' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "large"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-020] `#311` (`uclouvain_vocab_311`) — `late`

- **Problem Description:** Vocabulary entry 'late' is elementary A1 level (Elementary temporal descriptor (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='late' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'late' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "late"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-021] `#327` (`uclouvain_vocab_327`) — `natural`

- **Problem Description:** Vocabulary entry 'natural' is elementary A2 level (Basic elemental descriptor (Cambridge EVP A2) (CEFR A2 benchmark)).
- **Actual Observed Output:** `word='natural' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A2) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A2).
- **Corrective Action:** Exclude 'natural' (A2) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "natural"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-022] `#330` (`uclouvain_vocab_330`) — `new`

- **Problem Description:** Vocabulary entry 'new' is elementary A1 level (Elementary temporal/novelty adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='new' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'new' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "new"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-023] `#340` (`uclouvain_vocab_340`) — `past`

- **Problem Description:** Vocabulary entry 'past' is elementary A1 level (Elementary temporal descriptor (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='past' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'past' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "past"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-024] `#361` (`uclouvain_vocab_361`) — `real`

- **Problem Description:** Vocabulary entry 'real' is elementary A1 level (Elementary authenticity adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='real' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'real' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "real"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-025] `#378` (`uclouvain_vocab_378`) — `simple`

- **Problem Description:** Vocabulary entry 'simple' is elementary A1 level (Elementary complexity adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='simple' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'simple' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "simple"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-026] `#382` (`uclouvain_vocab_382`) — `special`

- **Problem Description:** Vocabulary entry 'special' is elementary A2 level (Basic qualitative adjective (Cambridge EVP A2) (CEFR A2 benchmark)).
- **Actual Observed Output:** `word='special' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A2) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A2).
- **Corrective Action:** Exclude 'special' (A2) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "special"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-027] `#397` (`uclouvain_vocab_397`) — `total`

- **Problem Description:** Vocabulary entry 'total' is elementary A2 level (Basic quantity descriptor (Cambridge EVP A2) (CEFR A2 benchmark)).
- **Actual Observed Output:** `word='total' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A2) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A2).
- **Corrective Action:** Exclude 'total' (A2) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "total"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-028] `#399` (`uclouvain_vocab_399`) — `true`

- **Problem Description:** Vocabulary entry 'true' is elementary A1 level (Elementary veracity adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='true' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'true' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "true"`
- **Resolution Status:** `excluded_by_rule`

#### [VOCA-029] `#405` (`uclouvain_vocab_405`) — `useful`

- **Problem Description:** Vocabulary entry 'useful' is elementary A1 level (Elementary functional utility adjective (Cambridge EVP A1) (CEFR A1 benchmark)).
- **Actual Observed Output:** `word='useful' (status=excluded)`
- **Expected Output:** `Marked as excluded (CEFR A1) with reason recorded`
- **Root Cause:** Source list includes basic elementary English vocabulary below B1/B2 academic target (A1).
- **Corrective Action:** Exclude 'useful' (A1) from eligible vocabulary dataset while preserving in source/RAW records.
- **Verification / Backtesting:** `.\.venv\Scripts\python.exe tools/vocabulary_review.py --source uclouvain --word "useful"`
- **Resolution Status:** `excluded_by_rule`
