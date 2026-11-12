"""Reproduce the real Greene PTR character-mapping error, without importing the full parser."""
from pathlib import Path
import json
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
def main():
    source=ROOT/'data/raw/2025_pdfs/20030924.pdf'
    with pymupdf.open(source) as pdf:
        text=pdf[0].get_text()
    raw=next(line for line in text.splitlines() if line.endswith(': New') and any(0x283<=ord(c)<=0x29c for c in line))
    cleaned=''.join(chr(ord(c)-0x222) if 0x283<=ord(c)<=0x29c else c for c in raw)
    assert cleaned=='Filing Status: New'
    assert 'AbbVie Inc. Common Stock (ABBV)' in text
    result={'filing_id':'20030924','page':1,'source':str(source.relative_to(ROOT)).replace(chr(92),'/'),'original_url':'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/20030924.pdf','raw':raw,'cleaned':cleaned,'offset_decimal':546,'offset_hex':'0x0222','affected_range':'U+0283-U+029C','ticker_already_correct':'ABBV','destination_field':'filing_status','destination_value':'New'}
    (ROOT/'data/processed/unicode_example.json').write_text(json.dumps(result,ensure_ascii=True,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2))
    return result
if __name__=='__main__': main()
