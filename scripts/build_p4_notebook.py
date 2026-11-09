"""Continue the submitted P3 notebook with P4's final evidence and reflection."""
from pathlib import Path
import nbformat as nbf
from integration import ROOT

def main():
    n=nbf.read(ROOT/'notebooks/DSA405_002_FA26_P3_sryan3.ipynb',as_version=4)
    # Retain the full reproducible P3 computation, replacing its old grading section.
    end=next(i for i,c in enumerate(n.cells) if c.cell_type=='markdown' and c.source.startswith('## 8.'))
    n.cells=n.cells[:end]
    n.cells[0].source=n.cells[0].source.replace('# P3 · Acquisition & Integration','# P4 · Congressional disclosure synthesis').replace('This independent repository','This P4 repository continues P3 and')+'\n\nP4 adds the portfolio completion table, final dictionary, nine-section report, and the author’s reflection on switching from repeated unsuccessful strategies to PDF geometry. Portfolio snapshots remain separate from the validated 2025 inputs.'
    for c in n.cells:
        if c.cell_type=='code':c.outputs=[];c.execution_count=None
    n.cells += [nbf.v4.new_markdown_cell('''## 8. P4 completion and final snapshot provenance

The portfolio's final searchable table uses separate derived CSV snapshots. Load those exact files without changing the validated 2025 analysis above. This is a presentation deliverable with documented provenance, not a claim to regenerate the portfolio's full multi-year scrape from its original raw files.'''),nbf.v4.new_code_cell('''from p4_synthesis import build_completion, docs, update_site
summary = json.loads((ROOT / "data/processed/validation.json").read_text())
snapshots = build_completion()
docs(summary, snapshots)
update_site()
display(pd.DataFrame(snapshots).T[["rows", "transaction_date_min", "transaction_date_max"]])
final_table = pd.read_csv(ROOT / "docs/data/portfolio-completion.csv", dtype=str, keep_default_na=False)
assert len(final_table) == sum(s["rows"] for s in snapshots.values())
assert final_table.groupby("chamber").size().to_dict() == {k:v["rows"] for k,v in snapshots.items()}
assert final_table.source_url.str.startswith(("https://", "http://")).all()
display(final_table.head(10))
print("Final display rows:", len(final_table), "Separate validated 2025 rows:", len(house) + len(senate))
'''),nbf.v4.new_markdown_cell('''## 9. Who is missing

Handwritten and image-only House forms were not solved. The Senate archive defers 97 paper reports. These omissions can systematically underrepresent filers using those formats. Unequal collection windows and unusable tickers also prevent treating the table as a census. No parsed rows does not establish no trading. Household ownership, amendment records, and amount ranges limit claims about individual trades or exact totals.'''),nbf.v4.new_code_cell('''from IPython.display import Markdown
display(Markdown((ROOT / "AI_USE_LOG.md").read_text(encoding="utf-8")))
display(Markdown((ROOT / "SELF_ASSESSMENT.md").read_text(encoding="utf-8")))
'''),nbf.v4.new_markdown_cell('''## 10. Written report and handoff

The required report is `reports/P4_REPORT.md`. The updated data dictionary is `DATA_DICTIONARY.md`. The P3 inspector remains available at `docs/index.html`; its completion link opens the final portfolio-style table. Review the report, reflection, and suggested self-scores before Moodle submission.''')]
    nbf.validate(n);nbf.write(n,ROOT/'notebooks/DSA405_002_FA26_P4_sryan3.ipynb')
    print('Created P4 notebook with',len(n.cells),'cells')

if __name__=='__main__':main()
