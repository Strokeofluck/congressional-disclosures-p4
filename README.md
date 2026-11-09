# P4 · Congressional disclosure synthesis

Sean Ryan · sryan3 · DSA 405 (002) · Fall 2026

P4 continues my P2/P3 House–Senate disclosure project. It combines an independently reproducible extraction and integration pipeline with the final searchable table from my data portfolio. The validated 2025 analysis finds 160 shared ticker-month keys among 3,760 total. The broader portfolio completion snapshots remain separately labeled.

## Open the project

- `docs/index.html`: P3-style source/code inspector, plus the final table and P4 report
- `docs/network.html`: monthly filer–ticker animation; rebuild with `python scripts/build_network.py`
- `docs/completion.html`: finished searchable disclosure table
- `reports/P4_REPORT.md`: required nine-section written report
- `notebooks/DSA405_002_FA26_P4_sryan3.ipynb`: executed course notebook
- `SELF_ASSESSMENT.md`: suggested rubric for Sean to confirm
- `DATA_DICTIONARY.md`, `PROVENANCE.md`, `AI_USE_LOG.md`: final documentation

## Run from a fresh clone

Use Python 3.12. Install `requirements.txt` in a virtual environment.

```sh
python -m pip install -r requirements.txt
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
