"""Build P4 from the preserved P3 outline using the standard notebook JSON format."""
from pathlib import Path
import json,uuid
ROOT=Path(__file__).resolve().parents[1]
def cell(kind,source):
    value={'cell_type':kind,'id':uuid.uuid4().hex[:8],'metadata':{},'source':source.splitlines(True)}
    if kind=='code':value.update(outputs=[],execution_count=None)
    return value
def main():
    n=json.loads((ROOT/'notebooks/DSA405_002_FA26_P3_sryan3.ipynb').read_text(encoding='utf-8'))
    end=next(i for i,c in enumerate(n['cells']) if c['cell_type']=='markdown' and ''.join(c['source']).startswith('## 8.'))
    n['cells']=n['cells'][:end]
    n['cells'][0]['source']=['# P4: Congressional disclosures, from source documents to searchable records\n','Sean Ryan | sryan3 | DSA 405 (002)\n','P3 supplies the acquisition, extraction and verified integration outline. P4 adds a real character repair, a documented portfolio snapshot, final report and reflection. The summary join is supporting technical evidence; it is not the House-only network.']
    for c in n['cells']:
        if c['cell_type']=='code':
            c.update(outputs=[],execution_count=None)
            text=''.join(c['source']).replace('complete P3 repository','complete P4 repository').replace('one P3 project ZIP','one P4 project ZIP')
            text=text.replace('from IPython.display import display, Code, HTML, SVG',"try:\n    from IPython.display import display, Code, HTML, SVG\nexcept ImportError:\n    from plain_display import display, Code, HTML, SVG")
            c['source']=text.splitlines(True)
    n['cells'] += [cell('markdown','## 8. Repair a real PDF character mapping\n\nThe PDF displays Filing Status: New correctly, but its embedded text mapping is broken. Recover the label and keep metadata separate from asset and ticker columns.'),cell('code','from unicode_example import main as demonstrate_unicode_repair\nexample=demonstrate_unicode_repair()\ndisplay(pd.DataFrame([{"Before":example["raw"],"After":example["cleaned"],"Saved field":example["destination_field"]}]))'),cell('markdown','## 9. Final portfolio snapshot\n\nThese bundled derived CSVs have a broader scope than the reproducible 2025 archive above. They are kept separate and their hashes are recorded.'),cell('code','from p4_synthesis import build_completion, docs, update_site\nsummary=json.loads((ROOT/"data/processed/validation.json").read_text())\nsnapshots=build_completion()\ndocs(summary,snapshots)\nupdate_site()\ndisplay(pd.DataFrame(snapshots).T)\nfinal_table=pd.read_csv(ROOT/"docs/data/portfolio-completion.csv",dtype=str,keep_default_na=False)\nassert len(final_table)==31662\nassert final_table.groupby("chamber").size().to_dict()=={"House":26732,"Senate":4930}\nassert final_table.source_url.str.startswith(("https://","http://")).all()\nprint("Final snapshot rows:",len(final_table))\nprint("Dates requiring source review:",final_table.date_quality.ne("").sum())'),cell('markdown','## 10. Interpretation, missingness and AI reflection\n\nThe written report contains all nine required sections. Handwritten/image-only House records remain unresolved; 97 Senate paper reports are deferred. No parsed rows is not proof of no transactions. Amendments and household ownership limit claims about unique trades and personal spending.'),cell('code','print((ROOT/"AI_USE_LOG.md").read_text(encoding="utf-8"))\nprint((ROOT/"SELF_ASSESSMENT.md").read_text(encoding="utf-8"))'),cell('markdown','## 11. Handoff\n\nSubmit the repository URL, this notebook, reports/P4_REPORT.md, and SELF_ASSESSMENT.md. Review the first-person reflection and suggested self-scores before submission. See REQUIREMENTS.md for the evidence map.')]
    (ROOT/'notebooks/DSA405_002_FA26_P4_sryan3.ipynb').write_text(json.dumps(n,ensure_ascii=False,indent=1),encoding='utf-8')
    print('Built P4 notebook:',len(n['cells']),'cells')
if __name__=='__main__':main()
