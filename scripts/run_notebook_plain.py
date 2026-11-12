"""Execute every code cell sequentially in a fresh Python process (not a Jupyter kernel)."""
from pathlib import Path
import json,io,contextlib,html,os
from render_markdown import render
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
p=ROOT/'notebooks/DSA405_002_FA26_P4_sryan3.ipynb'
n=json.loads(p.read_text(encoding='utf-8'));scope={'__name__':'__main__'};count=0;pages=[]
for i,c in enumerate(n['cells']):
    source=''.join(c['source'])
    if c['cell_type']=='markdown':pages.append(render(source));continue
    count+=1;buf=io.StringIO()
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):exec(compile(source,f'notebook-cell-{i}','exec'),scope)
    output=buf.getvalue();c['execution_count']=count;c['outputs']=[{'output_type':'stream','name':'stdout','text':output.splitlines(True)}]
    pages.append('<pre>'+html.escape(source)+'</pre><pre class="output">'+html.escape(output)+'</pre>')
    print('PASS cell',count,flush=True)
p.write_text(json.dumps(n,ensure_ascii=False,indent=1),encoding='utf-8')
(ROOT/'docs/P4-notebook.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>P4 executed computations</title><style>body{font:16px/1.6 system-ui;max-width:1050px;margin:40px auto;padding:20px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f8;padding:16px}.output{border-left:3px solid #216453}table{border-collapse:collapse}td{border:1px solid #ddd;padding:6px}</style><a href="index.html">Back to project</a><p>Every code cell executed in order in a fresh Python process. Jupyter-kernel verification is a separate check.</p>'+''.join(pages)+'</html>',encoding='utf-8')
print('Completed',count,'code cells in a fresh Python process.')
