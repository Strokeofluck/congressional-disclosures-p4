"""Build monthly bipartite activity snapshots from the validated analytical rows."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_network():
    months = [f'2025-{m:02}' for m in range(1, 13)]
    counts = {month: Counter() for month in months}
    nodes = {}
    with (ROOT / 'data/processed/combined_transactions.csv').open(encoding='utf-8-sig', newline='') as source:
        for row in csv.DictReader(source):
            month = row['month']
            if month not in counts or not row['ticker'] or not row['politician']:
                continue
            filer = 'f:' + row['chamber'] + ':' + row['politician']
            ticker = 't:' + row['ticker']
            nodes[filer] = dict(id=filer, label=row['politician'], kind=row['chamber'])
            nodes[ticker] = dict(id=ticker, label=row['ticker'], kind='Ticker')
            counts[month][(filer, ticker)] += 1
    result = dict(nodes=sorted(nodes.values(), key=lambda n: n['id']), frames=[
        dict(month=month, edges=[dict(source=a, target=b, rows=n)
                                for (a, b), n in sorted(counts[month].items())])
        for month in months])
    (ROOT / 'docs/data/network.js').write_text('window.P4NETWORK=' + json.dumps(result) + ';\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    build_network()
