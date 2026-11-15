#!/usr/bin/env python3
"""Merge BM25/Dense/Hybrid retrieved chunks for independent graded relevance judgment.

Inputs: each JSONL row {"question_id":"FOMC_001","retrieved":[
  {"chunk_id":"...","text":"...","document":"...","page":1,"score":0.3}, ...]}

DO NOT automatically treat absent candidates as grade 0. This is a pool for review.
"""
import argparse,csv,json,collections,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent

def jsonl(p):
 with open(p,encoding='utf-8') as f:
  for line in f:
   if line.strip():yield json.loads(line)

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--bm25',required=True);p.add_argument('--dense',required=True);p.add_argument('--hybrid',required=True)
 p.add_argument('--topk',type=int,default=20);p.add_argument('--output',default=str(R/'POOL_CHUNKS_TO_ANNOTATE.csv'))
 a=p.parse_args()
 qids={q['question_id'] for q in jsonl(R/'queries_145.jsonl')}
 group=collections.defaultdict(dict)
 for model,path in [('BM25',a.bm25),('DENSE',a.dense),('HYBRID',a.hybrid)]:
  seen_questions=set()
  for obj in jsonl(path):
   qid=obj['question_id'];seen_questions.add(qid)
   if qid not in qids:continue
   for rank,hit in enumerate(obj.get('retrieved',obj.get('results',[]))[:a.topk],1):
    if not isinstance(hit,dict):raise ValueError('Retrieved results must include chunk_id, text, page, document')
    for key in ('chunk_id','text','document','page'):
     if hit.get(key) in (None,''):raise ValueError(f'{model} {qid} rank{rank}: missing {key}')
    chunk_id=str(hit['chunk_id']);key=(qid,chunk_id)
    if key not in group[qid]:
     group[qid][key]=dict(question_id=qid,chunk_id=chunk_id,document=Path(hit['document']).name,page=hit['page'],text=hit['text'],source_models=[],ranks=[],annotator_A='',annotator_B='',adjudicated_grade='',evidence_facts='',status='UNJUDGED')
    g=group[qid][key]
    if g['text']!=hit['text'] or g['document']!=Path(hit['document']).name:raise ValueError(f'Same chunk_id with different source/text; freeze corpus and chunking first: {chunk_id}')
    g['source_models'].append(model);g['ranks'].append(f'{model}:{rank}')
  if qids-seen_questions:print(f'WARNING {model}: missing {len(qids-seen_questions)} queries')
 output=[]
 for qid in sorted(group):
  for r in group[qid].values():
   r['source_models']=';'.join(r['source_models']);r['ranks']=';'.join(r['ranks']);output.append(r)
 with open(a.output,'w',newline='',encoding='utf-8-sig') as f:
  columns=['question_id','chunk_id','document','page','text','source_models','ranks','annotator_A','annotator_B','adjudicated_grade','evidence_facts','status'];w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(output)
 print('Questions pooled:',len(group),'Unique query-chunk candidates:',len(output),'Output:',a.output)
 print('These are UNJUDGED candidates, not automatically relevant or irrelevant.')
if __name__=='__main__':main()
