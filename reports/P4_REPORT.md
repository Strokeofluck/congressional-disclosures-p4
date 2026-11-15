# From congressional disclosures to searchable records
**Sean Ryan | sryan3 | DSA 405 (002) | P4: Project Synthesis**

## 1. Data motivation
How can public disclosures reveal shared stock purchases? I chose this project to make congressional financial records traceable, searchable, and usable for reporting. Working with the actual forms showed that reliable extraction and cleaning had to come first. P4 brings that work together as searchable records linked to their original filings.

## 2. Sources, provenance and terms
I used 515 official U.S. House Clerk PTR PDFs downloaded in the P2 archive and 583 U.S. Senate eFD HTML reports archived by the prior scraper. The Senate index also lists 97 deferred paper reports. These are unequal collection snapshots, not a census. Filing IDs, original URLs, collection details and checksums are preserved in [PROVENANCE.md](https://github.com/Strokeofluck/congressional-disclosures-p4/blob/main/PROVENANCE.md). No blanket reuse license is assumed; Senate access terms restrict several uses, including commercial use except news/media dissemination. This project uses archived records for coursework.

## 3. Data dictionary and metadata
One analytical row is a retained report item, identified by chamber, filing and item number. Columns include filer, owner, transaction date, asset, ticker, transaction type, amount bounds and source URL. Amounts remain ranges; missing values remain unknown. The [final dictionary](https://github.com/Strokeofluck/congressional-disclosures-p4/blob/main/DATA_DICTIONARY.md) documents every output column and missingness. Broader portfolio exports are labeled separately from the 2025 analysis.

## 4. Data cleaning steps narrative
House members entered information differently, so a regex could not reliably tell where each field ended across all the reports. I used PyMuPDF to divide the PDF into rectangular cells and read each box separately, instead of using one large regex for the whole page. Table boundaries define the boxes; shading is an extra check. Small patterns clean individual fields. Senate HTML is read with Beautiful Soup after checking the table headers.

Some PDF text looked right on the page but came out as broken letters. In Greene PTR 20030924, some letters in “Filing Status: New” had character codes 546 too high. Subtracting 546 within the affected range restores the label. The parser can then save `New` in its own `filing_status` column, keeping it out of the `asset` and `ticker` columns. ABBV itself was already correct. Dates, tickers, and amount brackets are standardized, and exclusions and source-review decisions stay recorded.

## 5. Integration and verification
I harmonized both schemas and appended report items with chamber and source identities. For P3’s separate comparison, I summarized each chamber by ticker and month, then used a one-to-one outer join; unmatched values stay missing. I checked that no records were lost or multiplied, each summary had one row per ticker and month, keys were not missing or duplicated, dates stayed in 2025, and counts were positive whole numbers. The join preserved the counts from both chambers. All 1,105 raw-file checksums and 12 tests passed.

## 6. Findings
The reproducible 2025 sample retains **6,394 House and 518 Senate report rows**. The practical result is a searchable table with links back to filings. A separate, broader portfolio snapshot contains **31,662 rows**; four questionable dates remain flagged for source review. These counts describe captured records, not unique trades or relative trading volume across chambers.

The presentation also shows how structured records can support social network analysis. A separate frozen House-only purchase extract links filers to stocks they reported buying; AMZN connects 19 filers. That graph does not use the P3 House–Senate ticker-month join or the broader portfolio snapshot. Shared purchases show overlap without establishing coordination. Its separate methods and calculations are available in the [SNA project](https://github.com/Strokeofluck/congressional-stock-network-sna/blob/main/METHODS.md).

## 7. What is missing
Handwritten financial disclosure records were excluded because manually transcribing and cleaning them would have taken too much time for the scope of this project. Scanned or image-only House records also remain unresolved, and 97 Senate paper reports were deferred. These gaps can underrepresent filers who use those formats. Excluded assets and unresolved tickers narrow the analytical population. Unequal capture windows prevent direct chamber-volume comparisons. Amendments, household ownership and amount ranges prevent exact personal-spending totals. The data cannot establish whether someone used privileged information.

## 8. AI use log and reflection
ChatGPT assisted with code, explanations, checks and drafting. I inspected source examples and challenged misleading output. AI overemphasized a shared-key statistic unrelated to the House-only network; I questioned it and removed it from the presentation. Checking the proposed ABBV repair also showed the ticker was correct, so I used the genuinely broken filing-status label. I learned to verify examples and change methods when repeated regex suggestions failed.

## 9. Reproducibility
[Repository and README](https://github.com/Strokeofluck/congressional-disclosures-p4): clone, install `requirements.txt` with Python 3.12, then run `python scripts/unicode_example.py`, `python scripts/p4_synthesis.py` and `python -m unittest discover -s tests -v`. Open the P4 notebook and run all cells; view `docs/index.html`. All 12 code cells passed in a fresh Jupyter kernel on November 15, 2026, along with the pipeline build and 12 tests. Bundled raw inputs reproduce the 2025 pipeline; broader portfolio CSVs are frozen derived exports. Detailed evidence and the rubric accompany this report.
