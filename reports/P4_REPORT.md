# From congressional disclosures to searchable records
**Sean Ryan | sryan3 | DSA 405 (002) | P4: Project Synthesis**

## 1. Data motivation
How can congressional financial disclosures become searchable records that readers can trace to the original filing? I chose this project for public-interest reporting. Working with inconsistent forms shifted my focus from comparing stock choices to reliable extraction, cleaning, and source access.

## 2. Sources, provenance and terms
I used 515 official U.S. House Clerk PTR PDFs downloaded in the P2 archive and 583 U.S. Senate eFD HTML reports archived by the prior scraper. The Senate index also lists 97 deferred paper reports. These are unequal collection snapshots, not a census. Filing IDs, original URLs, collection details and checksums are preserved in [PROVENANCE.md](https://github.com/Strokeofluck/congressional-disclosures-p4/blob/main/PROVENANCE.md). No blanket reuse license is assumed; Senate access terms restrict several uses, including commercial use except news/media dissemination. This project uses archived records for coursework.

## 3. Data dictionary and metadata
One analytical row is a retained report item, identified by chamber, filing and item number. Columns include filer, owner, transaction date, asset, ticker, transaction type, amount bounds and source URL. Amounts remain ranges; missing values remain unknown. The [final dictionary](https://github.com/Strokeofluck/congressional-disclosures-p4/blob/main/DATA_DICTIONARY.md) documents every output column and missingness. Broader portfolio exports are labeled separately from the 2025 analysis.

## 4. Data cleaning steps narrative
I replaced unreliable whole-page regex parsing with PyMuPDF table geometry: identify rectangular cells and read each separately. Small patterns then clean individual fields. Senate tables use Beautiful Soup with checked headers. In Greene PTR 20030924, broken character codes garbled “Filing Status: New.” Subtracting 546 only within the affected range restores the label, allowing “New” to be stored in `filing_status`, outside `asset` and `ticker`. ABBV itself was already correct. Dates, tickers and amount brackets are standardized; exclusions and source-review decisions remain recorded rather than silently discarded.

## 5. Integration and verification
I harmonized both schemas and appended report items with chamber and source identities. For P3’s separate comparison, I summarized each chamber by ticker and month, then used a one-to-one outer join; unmatched values stay missing. Checks cover unique/nonmissing keys, valid months, positive integer counts and preservation of each chamber’s counts. All 1,105 raw-file checksums and 12 tests passed.

## 6. Findings
The reproducible 2025 sample retains **6,394 House and 518 Senate report rows**. The practical result is a searchable table with links back to filings. A separate, broader portfolio snapshot contains **31,662 rows**; four questionable dates remain flagged for source review. These counts describe captured records, not unique trades or relative trading volume across chambers.

## 7. What is missing
Unreadable/scanned House records and 97 Senate paper reports can underrepresent filers using those formats. Excluded assets and unresolved tickers narrow the analytical population. Unequal capture windows prevent direct chamber-volume comparisons. Amendments, household ownership and amount ranges prevent exact personal-spending totals. The data cannot establish whether someone used privileged information.

## 8. AI use log and reflection
ChatGPT assisted with code, explanations, checks and drafting. I inspected source examples and challenged misleading output. AI overemphasized a shared-key statistic unrelated to the House-only network; I questioned it and removed it from the presentation. Checking the proposed ABBV repair also showed the ticker was correct, so I used the genuinely broken filing-status label. I learned to verify examples and change methods when repeated regex suggestions failed.

## 9. Reproducibility
[Repository and README](https://github.com/Strokeofluck/congressional-disclosures-p4): clone, install `requirements.txt` with Python 3.12, then run `python scripts/unicode_example.py`, `python scripts/p4_synthesis.py` and `python -m unittest discover -s tests -v`. Open the P4 notebook and run all cells; view `docs/index.html`. All 12 code cells passed in a fresh Python process; a separate Jupyter-kernel rerun remains unverified here. Bundled raw inputs reproduce the 2025 pipeline; broader portfolio CSVs are frozen derived exports. Detailed evidence and the rubric accompany this report.
