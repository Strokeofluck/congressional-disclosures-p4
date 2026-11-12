"""Carry P3 forward with a final portfolio-table snapshot and P4 documentation."""
from pathlib import Path
import csv,hashlib,html,json,re,shutil
from datetime import date
import pandas as pd
from integration import build,ROOT

def fingerprint(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def build_completion():
    folder=ROOT/'data/portfolio'
    records=[];manifest={}
    for chamber,name in [('House','house_ptr_transactions_web.csv'),('Senate','senate_ptr_transactions_electronic.csv')]:
        p=folder/name;df=pd.read_csv(p,dtype=str,keep_default_na=False)
        manifest[chamber]={'file':'data/portfolio/'+name,'sha256':fingerprint(p),'rows':len(df),'transaction_date_min':df.transaction_date.min(),'transaction_date_max':df.transaction_date.max()}
        for row in df.to_dict('records'):
            records.append({'chamber':chamber,'filing_id':row.get('filing_id',row.get('report_id','')),
              'politician':row.get('politician',row.get('filer_name','')),'transaction_date':row['transaction_date'],
              'owner':row.get('owner',''),'ticker':row.get('ticker_v8_2_cleaned',row.get('ticker','')),
              'asset':row.get('asset_v8_2_cleaned',row.get('asset_name','')),
              'type':row['transaction_type'],'amount':row.get('amount_category',row.get('amount','')),
              'review':row.get('review_level',row.get('verification_status','')),
              'source_url':row.get('original_pdf_url',row.get('report_url',''))})
    assert len(records)==sum(x['rows'] for x in manifest.values())
    for row in records:
        try:
            parsed=date.fromisoformat(row['transaction_date'])
            row['date_quality']='Date needs source review' if parsed>date(2026,11,8) or parsed.year<2012 else ''
        except ValueError:
            row['date_quality']='Date needs source review'
    date_flags=sum(bool(row['date_quality']) for row in records)
    pd.DataFrame([r for r in records if r['date_quality']]).to_csv(ROOT/'data/processed/portfolio_date_review.csv',index=False)
    (ROOT/'provenance/portfolio_snapshot.json').write_text(json.dumps({'captured':'2026-11-08','commits':{'portfolio':'f8bd2ae483aa02429a9fbe65bf6d597ba9a8fd33','house':'725db272d62a1e8f32c6a9de071cf4776675b2a4','senate':'62f075a1e7dcbbb95865a62319de6aac2a6ce8f9'},'sources':manifest},indent=2),encoding='utf-8')
    out=ROOT/'docs/data';out.mkdir(exist_ok=True)
    pd.DataFrame(records).to_csv(out/'portfolio-completion.csv',index=False)
    (out/'portfolio-completion.js').write_text('window.P4ROWS='+json.dumps(records,ensure_ascii=True)+';window.P4_DATE_FLAGS='+str(date_flags)+';',encoding='utf-8')
    print('Portfolio date anomalies preserved for source review:',date_flags)
    return manifest

def docs(summary,manifest):
    report='''# P4: Congressional disclosures, from source documents to a usable table

Sean Ryan · sryan3 · DSA 405 (002) · Fall 2026

## 1. Data motivation

I wanted to make House and Senate transaction disclosures searchable and traceable to their original records. P2 supplied the cleaning and audit foundation. P3 built independent acquisition, parsing, and a verified House–Senate integration. P4 brings those parts together with the finished disclosure-search table used by my data portfolio.

Working with the actual data narrowed the question to: how can differently structured public disclosures become searchable, consistently labeled records that readers can trace back to a filing? The practical result is a source-linked table and inspector. A ticker-month comparison is retained as a P3 integration exercise, not the central research finding or an input to the House-only network.

## 2. Sources, provenance and terms

The House Clerk produces the official PTR PDFs and filing index. The inherited collection contains 515 House PDFs. The Senate produces electronic HTML reports and paper disclosures. The preserved Senate index contains 680 reports, including 583 electronic reports and 97 deferred paper reports. The code reads the archived material locally. It does not newly accept an access agreement or bypass access controls.

Original report URLs, filing IDs, raw checksums, source commits, and parsing code remain in the repository. See PROVENANCE.md and provenance/source_commits.json. These are publicly disclosed official records, but public access is not a blanket license to use them for any purpose. The Senate notice restricts unlawful use, commercial use outside news/media dissemination, credit screening, and fundraising solicitation. No permissive third-party software or data license is invented here. Inherited code retains its attribution and notices. Use is limited to noncommercial coursework and public-records explanation.

P4 also freezes the two CSVs that feed the portfolio table on November 8, 2026. Their local source versions, hashes, dates, and row counts are in provenance/portfolio_snapshot.json. They are derived exports, not original government CSV releases. A clone includes them and needs no sibling portfolio checkout.

## 3. Final data dictionary and metadata

DATA_DICTIONARY.md describes the final analytical transactions, ticker-month join, and portfolio completion view. The analytical transaction grain is one retained report item, preserving chamber, filing and row identity. The join grain is one ticker per calendar month. The portfolio view preserves the source snapshot rows and exposes source links for inspection.

The final completion table and the 2025 analysis have different scopes. Their counts must not be compared as if they used the same population. In particular the P3 Senate archive reparses 5,069 source items, while the separately copied portfolio Senate snapshot has 4,930 rows. P4 keeps those versions separate instead of silently replacing one with the other.

## 4. Cleaning narrative

House PDFs are parsed with the inherited PyMuPDF geometry-based implementation. It finds tables, identifies cell rectangles, and reads embedded text inside the appropriate regions. This helps distinguish an asset description from a date or amount in the adjacent column. Ticker and amount rules run after extraction. The source wording remains available, and recorded review decisions are replayed only when their original evidence still matches.

A real character-mapping error appears in Greene PTR 20030924. The PDF displays `Filing Status: New`, but PyMuPDF extracts the label with incorrect Unicode characters. `normalize_house_pdf_text` repairs only characters in U+0283 through U+029C by subtracting hexadecimal `0x0222` (546) from each code point. For example, U+0283 (`sha`, code 643) becomes `a` (code 97). ABBV itself extracts correctly. Recovering the label lets the parser store `New` separately as `filing_status`, rather than leave that metadata inside an asset description. This is related to Week 4's mojibake lesson, although the PDF font mapping differs from the lab's UTF-8/Latin-1 mismatch. See `scripts/unicode_example.py` and `data/processed/unicode_example.json` for the actual before-and-after text.

One documented review kept January 13, 2025 as a transaction date because January 17 belonged to the option description. Another retained two similar-looking transactions because the source listed different unit quantities. Similar asset/date/amount brackets therefore do not justify automatic deletion. The review log changes two amount cells without deleting report rows.

Senate HTML is read with Beautiful Soup after checking the expected table headers. Dates, owners, asset names, tickers, types, amounts, and source links map into the shared schema. The comparable analysis keeps 2025 transaction dates, the stated stock/ticker scope, and usable ticker labels. Excluded items remain in excluded_rows.csv. Amount brackets remain brackets, and missing amounts remain missing.

**Handwritten and image-only records were not solved in this project.** No claim is made that geometry reads handwriting. House scanned or handwritten material can produce no extracted rows or incomplete rows. Senate paper reports are deferred. The site can show a source image while still having no usable structured extraction from it.

## 5. Integration and verification

The chambers contain different people, so I do not join on legislator names. Raw transaction rows can also repeat the same ticker-month, so joining them directly would multiply records. I first aggregate each chamber to unique ticker-month keys, then use a one-to-one outer join. Unmatched chamber values stay missing rather than being replaced with observed zeroes.

The notebook checks expected union size, key uniqueness, preservation of unmatched keys, both chambers' count conservation, nonmissing keys, valid months, positive integer counts, and expected overlap. It verifies 1,105 raw-file hashes and preserves deliberate missing-table and duplicate-key failure demonstrations. A full House rebuild is available with scripts/house.py --rebuild.

## 6. Findings

The main outcome is a searchable, source-linked record collection, with separate fields for the asset, ticker, dates, amounts, and filing metadata. The captured 2025 pipeline retains **6,394 House report rows and 518 Senate report rows**.

**Supporting integration exercise, carried forward from P3.** Their summaries produce **3,760 ticker-month keys**: **160 in both sources**, **3,410 House-only**, and **190 Senate-only**. Only **4.3%** of the union appears in both archives. An inner join would discard 3,600 keys, hiding much of the available coverage.

This overlap is a description of the two captured archives, not a duplication problem, a repair, or an input to the House-only network. It is retained to document and reproduce the required P3 join. It is not evidence that House members actually trade more than Senators, or that unmatched tickers were not traded in the other chamber. Different collection windows, excluded formats, and unresolved records limit that interpretation.

The completion table contains **26,732 House rows and 4,930 Senate rows**, or **31,662 source-snapshot rows**. Its contribution is practical: a reader can search, filter, sort, and open the underlying disclosure. These broader portfolio rows do not replace or expand the validated 2025 analysis. The final web view labels that distinction.

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

A concrete AI mistake during presentation preparation was treating 160 shared ticker-month keys as a main finding without explaining its relevance. I questioned what it meant and whether it fed the network. Checking the pipeline showed it only described the P3 summary join; the House-only network was separate. I removed that statistic from the presentation and kept it here only as supporting integration documentation. I also asked to verify a proposed ABBV character-repair example: inspecting the PDF text showed ABBV was already correct, so the example uses the genuinely broken filing-status label instead.

## 9. Reproducibility

Repository: https://github.com/Strokeofluck/congressional-disclosures-p4

Install requirements.txt with Python 3.12, then run scripts/p4_synthesis.py. Use scripts/house.py --rebuild to force parsing from all primary PDFs. Run the tests and execute the P4 notebook with scripts/execute_p4_notebook.py. The README gives the complete order. Source archives, pinned parser, review decisions, analytical outputs, and final portfolio snapshots are bundled. No GitHub or API credential belongs in the notebook or repository.

The website supports the report and executed notebook. Moodle still requires the repository URL, notebook, written report, and self-scored rubric. P4 is due November 20 at 11:59 PM Eastern. No Moodle submission is performed by building this repository.
'''
    anomalies=pd.read_csv(ROOT/'data/processed/portfolio_date_review.csv',dtype=str,keep_default_na=False)
    report=report.replace('## 7. What is missing and why it matters',f'''### Date checks in the final portfolio display

The imported portfolio snapshots retain **{len(anomalies)} rows with dates requiring source review**: malformed dates, dates after the November 8 capture date, or years before the expected public-reporting period. Examples include 3031 and 2220. The completion table marks these records, preserves their original date text and source links, and places them after plausible dates in the default display. No guessed corrections or deletions are made. The review queue is `data/processed/portfolio_date_review.csv`. These display-snapshot issues do not enter the separately filtered 2025 analytical join.

## 7. What is missing and why it matters''')
    (ROOT/'reports/P4_REPORT.md').write_text(report,encoding='utf-8')
    # Markdown render is generated from the same required report.
    from render_markdown import render as markdown2html_mistune
    body=markdown2html_mistune(report)
    (ROOT/'docs/P4-report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>P4 final report</title><style>body{font:18px/1.65 system-ui;max-width:1000px;margin:40px auto;padding:0 24px;color:#222}a{color:#2780e3}table{border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #ddd;text-align:left}h2{margin-top:2em}</style><a href="index.html">Return to source inspector</a>'+body+'</html>',encoding='utf-8')
    frames={'analytical transaction':pd.read_csv(ROOT/'data/processed/combined_transactions.csv',dtype=str,keep_default_na=False),'ticker-month join':pd.read_csv(ROOT/'data/processed/combined_ticker_month.csv',dtype=str,keep_default_na=False),'portfolio completion':pd.read_csv(ROOT/'docs/data/portfolio-completion.csv',dtype=str,keep_default_na=False)}
    dictionary=['# Final data dictionary','Generated from final table schemas. Empty strings in source CSVs remain unknown/missing. Dates use ISO format. Report rows preserve amendments and do not represent uniquely deduplicated economic events.']
    meanings={'date_quality':'Source date anomaly flag, not a corrected date','transaction_id':'Chamber-prefixed source report/item identifier','chamber':'House or Senate','filing_id':'Original report identifier','row_number':'Report item number','politician':'Disclosure filer display name','filing_date':'Report filing date when available','transaction_date':'Reported transaction date','owner':'Reported household ownership','ticker':'Normalized reported ticker, not a permanent security ID','month':'Transaction calendar month, YYYY-MM','asset_name':'Reported asset description','asset':'Reported asset description','asset_type':'Source asset classification','transaction_type':'Source purchase/sale/exchange classification','type':'Source purchase/sale/exchange classification','amount_raw':'Original disclosed amount bracket','amount':'Original disclosed amount bracket','amount_min':'Lower bound, not an exact value','amount_max':'Upper bound, may be missing/open-ended','source_url':'Original disclosure link','source_format':'PDF or archived HTML','comment':'Source comment','review_flag':'Inherited extraction review flag','ticker_status':'Ticker-resolution status','action':'Harmonized transaction category','exclusion_reason':'Scope exclusion reason, empty for included rows','_merge':'Join provenance: both, left_only, right_only','review':'Source-specific review/verification label; not a calibrated probability'}
    for name,df in frames.items():
        dictionary+=['\n## '+name,'| Field | Meaning | Missing/empty rows |','|---|---|---:|']
        for c in df:
            meaning=meanings.get(c,'Per-chamber aggregate: '+c.replace('_',' ')+'. Missing means no observation in that chamber, not observed zero.')
            dictionary.append(f'| `{c}` | {meaning} | {int(df[c].eq("").sum())} |')
    (ROOT/'DATA_DICTIONARY.md').write_text('\n'.join(dictionary),encoding='utf-8')
    (ROOT/'AI_USE_LOG.md').write_text('# AI use and reflection\n\n'+report.split('## 8. AI use log and reflection\n\n')[1].split('\n## 9.')[0],encoding='utf-8')
    (ROOT/'SELF_ASSESSMENT.md').write_text('''# P4 suggested self-scored rubric

Sean Ryan should confirm these scores after reviewing the final report and notebook. These are suggestions, not an instructor grade. Scale 0–4 is carried forward from the course rubric convention.

| Criterion | Weight | Suggested score | Evidence |
|---|---:|---:|---|
| Findings and interpretation | 2 | 4 | Report §6 and executed notebook counts, cautious cross-chamber interpretation |
| Narrative coherence | 2 | 4 | Question, raw sources, cleaning, verified join, final table |
| Who is missing | 2 | 4 | Report §7 gives specific exclusions and consequences |
| AI use log and reflection | 2 | 3 | User's retrospective account, checked geometry implementation, practical change in workflow; no fabricated experiment log |
| Technical ambition | 2 | 3 | Independent PDF extraction, strict HTML parser, geometry source inspector, verified integration; tier-gated final score remains instructor-dependent |
| Repository and reproducibility | 2 | 4 | Bundled inputs, pinned packages, rebuild command, fresh-kernel notebook and tests |
| Documentation carried forward | 1 | 4 | Updated dictionary, provenance, review records and missingness |

Suggested total: 48/52. Technical ambition is tier-gated and this score is not a promise of a grade. Final author review is required. Do not submit this suggestion as a confirmed self-score without reviewing it.
''',encoding='utf-8')
    readme='''# P4 · Congressional disclosure synthesis

Sean Ryan · sryan3 · DSA 405 (002) · Fall 2026

P4 continues my P2/P3 House–Senate disclosure project. It combines an independently reproducible extraction and integration pipeline with the final searchable table from my data portfolio. The validated 2025 pipeline preserves 6,394 House and 518 Senate in-scope report rows. Source-linked search and inspection are the main outputs. The broader portfolio completion snapshots remain separately labeled.

## Open the project

- `docs/index.html`: P3-style source/code inspector, plus the final table and P4 report
- `docs/completion.html`: finished searchable disclosure table
- `reports/P4_REPORT.md`: required nine-section written report
- `notebooks/DSA405_002_FA26_P4_sryan3.ipynb`: executed course notebook
- `SELF_ASSESSMENT.md`: suggested rubric for Sean to confirm
- `DATA_DICTIONARY.md`, `PROVENANCE.md`, `AI_USE_LOG.md`: final documentation

## Run from a fresh clone

Use Python 3.12. Install `requirements.txt` in a virtual environment.

```sh
python -m pip install -r requirements.txt
python scripts/unicode_example.py
python scripts/p4_synthesis.py
python -m unittest discover -s tests -v
python scripts/build_p4_notebook.py
python scripts/execute_p4_notebook.py
python -m http.server 8765
```

Open `http://localhost:8765/docs/`. The final table and inspector also support local-file viewing. A forced raw House rebuild is `python scripts/house.py --rebuild`; the normal build verifies its immutable recipe and output before using a cache. All raw inputs and portfolio CSV snapshots are bundled. No sibling repo, credentials, live Senate agreement, or current scrape is needed.

## Layout and provenance

`data/raw/` preserves P3's official source archive. `data/review/` contains reviewed decisions. `vendor/` holds the pinned House parser. `scripts/` contains extraction, integration, tests/build helpers. `data/processed/` holds analytical outputs. `data/portfolio/` contains the two derived snapshots feeding the completion table. `docs/` contains the portable website, figures, and readable notebook. `reports/` contains the final written report.

See `provenance/source_commits.json` for inherited P2/P3 origins and `provenance/portfolio_snapshot.json` for November 8 snapshot hashes and source commits. Sources are the official House Clerk PTR PDFs and archived Senate eFD HTML. Public records and inherited software do not receive an invented blanket license here. Respect Senate use restrictions and upstream software notices.

## Scope and submission

We did not solve handwritten or image-only disclosures. Senate paper reports are deferred. Missing parsed rows are not proof of no transactions. Unequal collection coverage prevents trading-volume comparisons. Report items include amendments, amounts remain ranges, and the broader portfolio snapshots are not substituted into the 2025 join.

Moodle requires the repository URL, notebook, report, and self-scored rubric. Due November 20, 2026, 11:59 PM Eastern. This repository build does not submit to Moodle. Review the reflection and suggested self-scores before submission.
'''
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    provenance=ROOT/'PROVENANCE.md';txt=provenance.read_text(encoding='utf-8')
    marker='\n## P4 completion snapshots\n'
    txt=txt.split(marker)[0]+marker+'\nP4 continues the submitted P3 implementation preserved locally as the October 31, 2026 project copy. The unchanged P3 raw manifest, source commits, parser hashes and review records remain authoritative for its 2025 integration. The final portfolio CSV snapshots are distinct derived artifacts. Their hashes and source commits are recorded in `provenance/portfolio_snapshot.json`. They are not inputs to the validated 2025 join. P4 does not claim to reproduce the full multi-year portfolio scrape from its original raw records; the final table is a documented frozen export.\n'
    provenance.write_text(txt,encoding='utf-8')

def update_site():
    shutil.copy2(ROOT/'templates/p4-home.html',ROOT/'docs/index.html')


def main():
    summary=build();manifest=build_completion();docs(summary,manifest);update_site()
    print('P4 synthesis built. Portfolio rows:',{k:v['rows'] for k,v in manifest.items()})

if __name__=='__main__':main()
