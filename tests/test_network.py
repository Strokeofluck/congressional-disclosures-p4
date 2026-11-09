"""Check that animation snapshots preserve analytical activity and identity."""
import csv
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_network import build_network


class NetworkTests(unittest.TestCase):
    def test_monthly_edges_reconcile_to_source(self):
        result = build_network()
        self.assertEqual([f['month'] for f in result['frames']], [f'2025-{m:02}' for m in range(1, 13)])
        expected = Counter()
        with (ROOT / 'data/processed/combined_transactions.csv').open(encoding='utf-8-sig', newline='') as source:
            rows = list(csv.DictReader(source))
        for row in rows:
            expected[(row['month'], 'f:' + row['chamber'] + ':' + row['politician'], 't:' + row['ticker'])] += 1
        actual = Counter({(f['month'], e['source'], e['target']): e['rows'] for f in result['frames'] for e in f['edges']})
        self.assertEqual(actual, expected)
        self.assertEqual(sum(actual.values()), 6912)
        ids = {n['id'] for n in result['nodes']}
        self.assertEqual(len(ids), len(result['nodes']))
        self.assertTrue(all(a in ids and b in ids for _, a, b in actual))


if __name__ == '__main__':
    unittest.main()
