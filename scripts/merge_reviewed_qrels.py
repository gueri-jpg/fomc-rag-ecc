#!/usr/bin/env python3
"""Merge *actual* additional human judgments with 279 group-confirmed seed labels.

Never infer negative labels from unjudged pages; fail on conflicts, unknown queries or invalid page IDs.
The output is a consolidated labeled pool, NOT automatically certified exhaustive gold.
"""
import argparse,csv
from pathlib import Path
from fomcrag.pooling import merge_human_judgments
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
    pages={f"{r['document']}#p{p}" for r in read(B/'MANIFESTE_CORPUS_93.csv') for p in range(1,int(r['pdf_pages'])+1)}
    if opts.output.resolve() in {(B/n).resolve() for n in ('qrels_group_confirmed_PAGES.csv','qrels_group_confirmed_PAGES.trec')}:
        raise ValueError('Refuse to overwrite group-confirmed source judgments')
    merged=merge_human_judgments(known,read(opts.additional),all_queries,pages)
    added=len(merged)-len(known)
    known=merged
    opts.output.parent.mkdir(parents=True,exist_ok=True)
    with opts.output.open('w',encoding='utf-8') as f:
        for (q,p),grade in sorted(known.items()):f.write(f'{q} 0 {p} {grade}\n')
    print(f'EXPORTED {len(known)} qrels ({len(baseline)} accepted seed + {added} explicit new).')
    print('NOT GOLD CERTIFICATION: document pool coverage, page/chunk granularity and agreement separately.')

if __name__=='__main__':main()
