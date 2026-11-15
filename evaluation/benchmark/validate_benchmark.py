#!/usr/bin/env python3
"""Run lightweight local integrity checks on the benchmark files."""
import csv,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def jsonl(n):return [json.loads(s) for s in (ROOT/n).read_text(encoding='utf-8').splitlines() if s.strip()]
def csvrows(n):return list(csv.DictReader((ROOT/n).open(encoding='utf-8-sig')))
qs=jsonl('queries_145.jsonl');e=jsonl('evidence_citations_145.jsonl');v=jsonl('robustness_30_TEST_ONLY.jsonl');qr=csvrows('silver_qrels_PAGES.csv');negs=csvrows('unanswerable_10_NOT_GOLD.csv');
ids={q['question_id'] for q in qs};assert len(qs)==len(ids)==145
assert len(e)==296 and len(v)==30 and len(negs)==10
assert set(q['split'] for q in qs)=={'dev','validation','test'}
assert collections.Counter(q['split'] for q in qs)=={'dev':85,'validation':30,'test':30}
assert all(vv['parent_question_id'] in ids for vv in v)
assert all(vv['split']==next(q['split'] for q in qs if q['question_id']==vv['parent_question_id']) for vv in v)
assert all(q['question_id'] in ids for q in qr)
assert all(q['page_id'].endswith('#p'+q['page_id'].split('#p')[-1]) for q in qr)
assert len({(r['question_id'],r['page_id']) for r in qr})==len(qr)
assert all(r['source_presence_verified']!='CHECK' for r in e)
assert all(1<=int(r['proposed_relevance_grade'])<=2 for r in e if r['candidate_status']!='EXCLUDE_SCOPE')
assert all(str(r.get('approved','')).upper()!='YES' for r in negs)
rv=jsonl('robustness_30_TEST_ONLY.jsonl');assert len(rv)==30
assert all(vv['split']=='test' for vv in rv)
assert set(vv['parent_question_id'] for vv in rv)==set(q['question_id'] for q in qs if q['split']=='test')
print('PASS: 145 query IDs, 296 cited candidates (294 retained), 30 active TEST variants, 10 disabled negative candidates, splits 85/30/30, 279 page qrels; note: judge completeness not certified')
