#!/usr/bin/env python3
"""Merge *actual* additional human judgments with 279 group-confirmed seed labels.

Never infer negative labels from unjudged pages; fail on conflicts, unknown queries or invalid page IDs.
The output is a consolidated labeled pool, NOT automatically certified exhaustive gold.
"""
import argparse,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'evaluation'/'benchmark'

def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--additional',type=Path,required=True,help='CSV with question_id,page_id,relevance_grade,review_status=HUMAN_REVIEWED')
    a.add_argument('--output',type=Path,default=ROOT/'evaluation'/'benchmark'/'qrels_consolidated_PAGES.trec')
    opts=a.parse_args()
    baseline=read(B/'qrels_group_confirmed_PAGES.csv')
    known={(r['question_id'],r['page_id']):int(r['relevance_grade']) for r in baseline}
    all_queries={row['question_id'] for row in read(B/'questions_metadata_145.csv')}
    added=0
    for r in read(opts.additional):
        required=['question_id','page_id','relevance_grade','review_status']
        if any(not r.get(x) for x in required):raise ValueError('Incomplete explicit human review row')
        if r['review_status']!='HUMAN_REVIEWED':raise ValueError('New label must have HUMAN_REVIEWED status')
        q,p=r['question_id'],r['page_id']
        if q not in all_queries:raise ValueError(f'Unknown question {q}')
        if '#p' not in p:raise ValueError(f'Bad page ID {p}')
        v=int(r['relevance_grade'])
        if v not in (0,1,2):raise ValueError(f'Invalid grade {v}')
        key=(q,p)
        if key in known and known[key]!=v:raise ValueError(f'Grade conflict for {key}: {known[key]} vs {v}')
        if key not in known:added+=1
        known[key]=v
    opts.output.parent.mkdir(parents=True,exist_ok=True)
    with opts.output.open('w',encoding='utf-8') as f:
        for (q,p),grade in sorted(known.items()):f.write(f'{q} 0 {p} {grade}\n')
    print(f'EXPORTED {len(known)} qrels ({len(baseline)} accepted seed + {added} explicit new).')
    print('NOT GOLD CERTIFICATION: document pool coverage, page/chunk granularity and agreement separately.')

if __name__=='__main__':main()
