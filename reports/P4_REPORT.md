# P4: Congressional disclosures, from source documents to a usable table

Sean Ryan · sryan3 · DSA 405 (002) · Fall 2026

## 1. Data motivation

I wanted to make House and Senate transaction disclosures searchable and traceable to their original records. P2 supplied the cleaning and audit foundation. P3 built independent acquisition, parsing, and a verified House–Senate integration. P4 brings those parts together with the finished disclosure-search table used by my data portfolio.

Working with the actual data narrowed the analytical question: which reported ticker–calendar-month combinations appear in the two captured sources during 2025? The result is a comparison of archive coverage, not a claim about all congressional trading, suspicious behavior, or investment returns.

## 2. Sources, provenance and terms

The House Clerk produces the official PTR PDFs and filing index. The inherited collection contains 515 House PDFs. The Senate produces electronic HTML reports and paper disclosures. The preserved Senate index contains 680 reports, including 583 electronic reports and 97 deferred paper reports. The code reads the archived material locally. It does not newly accept an access agreement or bypass access controls.

Original report URLs, filing IDs, raw checksums, source commits, and parsing code remain in the repository. See PROVENANCE.md and provenance/source_commits.json. These are publicly disclosed official records, but public access is not a blanket license to use them for any purpose. The Senate notice restricts unlawful use, commercial use outside news/media dissemination, credit screening, and fundraising solicitation. No permissive third-party software or data license is invented here. Inherited code retains its attribution and notices. Use is limited to noncommercial coursework and public-records explanation.

P4 also freezes the two CSVs that feed the portfolio table on November 8, 2026. Their local source versions, hashes, dates, and row counts are in provenance/portfolio_snapshot.json. They are derived exports, not original government CSV releases. A clone includes them and needs no sibling portfolio checkout.

## 3. Final data dictionary and metadata

DATA_DICTIONARY.md describes the final analytical transactions, ticker-month join, and portfolio completion view. The analytical transaction grain is one retained report item, preserving chamber, filing and row identity. The join grain is one ticker per calendar month. The portfolio view preserves the source snapshot rows and exposes source links for inspection.

The final completion table and the 2025 analysis have different scopes. Their counts must not be compared as if they used the same population. In particular the P3 Senate archive reparses 5,069 source items, while the separately copied portfolio Senate snapshot has 4,930 rows. P4 keeps those versions separate instead of silently replacing one with the other.

## 4. Cleaning narrative

House PDFs are parsed with the inherited PyMuPDF geometry-based implementation. It finds tables, identifies cell rectangles, and reads embedded text inside the appropriate regions. This helps distinguish an asset description from a date or amount in the adjacent column. Ticker and amount rules run after extraction. The source wording remains available, and recorded review decisions are replayed only when their original evidence still matches.

One documented review kept January 13, 2025 as a transaction date because January 17 belonged to the option description. Another retained two similar-looking transactions because the source listed different unit quantities. Similar asset/date/amount brackets therefore do not justify automatic deletion. The review log changes two amount cells without deleting report rows.

Senate HTML is read with Beautiful Soup after checking the expected table headers. Dates, owners, asset names, tickers, types, amounts, and source links map into the shared schema. The comparable analysis keeps 2025 transaction dates, the stated stock/ticker scope, and usable ticker labels. Excluded items remain in excluded_rows.csv. Amount brackets remain brackets, and missing amounts remain missing.

**Handwritten and image-only records were not solved in this project.** No claim is made that geometry reads handwriting. House scanned or handwritten material can produce no extracted rows or incomplete rows. Senate paper reports are deferred. The site can show a source image while still having no usable structured extraction from it.

## 5. Integration and verification

The chambers contain different people, so I do not join on legislator names. Raw transaction rows can also repeat the same ticker-month, so joining them directly would multiply records. I first aggregate each chamber to unique ticker-month keys, then use a one-to-one outer join. Unmatched chamber values stay missing rather than being replaced with observed zeroes.

The notebook checks expected union size, key uniqueness, preservation of unmatched keys, both chambers' count conservation, nonmissing keys, valid months, positive integer counts, and expected overlap. It verifies 1,105 raw-file hashes and preserves deliberate missing-table and duplicate-key failure demonstrations. A full House rebuild is available with scripts/house.py --rebuild.

## 6. Findings

The captured 2025 comparison contains **6,394 House report rows and 518 Senate report rows**. Their summaries produce **3,760 ticker-month keys**: **160 in both sources**, **3,410 House-only**, and **190 Senate-only**. Only **4.3%** of the union appears in both archives. An inner join would discard 3,600 keys, hiding much of the available coverage.

This is useful evidence about the captured records and the importance of the join design. It is not evidence that House members actually trade more than Senators, or that unmatched tickers were not traded in the other chamber. Different collection windows, excluded formats, and unresolved records limit that interpretation.

The completion table contains **26,732 House rows and 4,930 Senate rows**, or **31,662 source-snapshot rows**. Its contribution is practical: a reader can search, filter, sort, and open the underlying disclosure. These broader portfolio rows do not replace or expand the validated 2025 analysis. The final web view labels that distinction.

### Date checks in the final portfolio display

The imported portfolio snapshots retain **4 rows with dates requiring source review**: malformed dates, dates after the November 8 capture date, or years before the expected public-reporting period. Examples include 3031 and 2220. The completion table marks these records, preserves their original date text and source links, and places them after plausible dates in the default display. No guessed corrections or deletions are made. The review queue is `data/processed/portfolio_date_review.csv`. These display-snapshot issues do not enter the separately filtered 2025 analytical join.

## 7. What is missing and why it matters

| Exclusion or uncertainty | Consequence |
|---|---|
| Handwritten/scanned House records and unreadable cells | Parsed counts can underrepresent filers using those formats. A file with no rows is not proof of no transactions. |
| 97 Senate paper reports | Electronic-report users are represented more fully than paper filers. |
| Unequal source collection windows | Cross-chamber row counts cannot measure the relative amount of actual trading. |
| Unresolved tickers and excluded asset categories | The analytical overlap describes only the chosen ticker-bearing scope. |
| Amendments and potentially repeated economic events | Report items are not a fully deduplicated count of trades. |
| Amount ranges and household ownership | Exact dollar totals and personal holdings cannot be inferred. Spouse/joint transactions remain distinct source information. |
| Portfolio snapshots differ from the preserved P3 inputs | A final display refresh does not retroactively validate a different analytical population. |

One question this project cannot answer is whether a filer used privileged information. That would require additional evidence and a different research design.

## 8. AI use log and reflection

ChatGPT helped develop code, explain methods, draft documentation, and identify checks. I directed the work, inspected source examples, and selected which methods to keep. This P4 draft and its suggested self-scores still need my final review before submission.

**My biggest lesson was not to let AI spend indefinitely going in circles on old ideas that I had already seen fail.** I had to interrupt that repetition, inspect the document's structure, and explore libraries and methods better suited to it. The productive change was treating the PDF as a positioned document: use table and rectangle geometry rather than repeatedly guessing from a loose stream of text.

The checked implementation uses PyMuPDF's page.find_tables(), fitz.Rect, and page.get_text(..., clip=rect). It is fair to describe the rectangle finder as a library-based PDF geometry approach. That does not prove why the model repeated suggestions internally, and a library is not automatically correct. I still needed source checks, documented exceptions, and failure handling. It also did not make handwritten records readable.

The error in the AI-assisted process was persisting with unsuccessful strategies rather than changing methods when the evidence required it. My correction was to set a stop-and-reassess point, inspect a representative original, test a concrete alternative, and keep only changes supported by the source. The preserved date and duplicate-review examples show why plausible output alone is insufficient. This account is my retrospective reflection, not a controlled benchmark of competing models or libraries.

## 9. Reproducibility

Repository: https://github.com/Strokeofluck/congressional-disclosures-p4

Install requirements.txt with Python 3.12, then run scripts/p4_synthesis.py. Use scripts/house.py --rebuild to force parsing from all primary PDFs. Run the tests and execute the P4 notebook with scripts/execute_p4_notebook.py. The README gives the complete order. Source archives, pinned parser, review decisions, analytical outputs, and final portfolio snapshots are bundled. No GitHub or API credential belongs in the notebook or repository.

The website supports the report and executed notebook. Moodle still requires the repository URL, notebook, written report, and self-scored rubric. P4 is due November 20 at 11:59 PM Eastern. No Moodle submission is performed by building this repository.
