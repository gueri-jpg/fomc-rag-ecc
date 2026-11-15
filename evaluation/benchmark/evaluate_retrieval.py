#!/usr/bin/env python3
"""Evaluate FOMC retrieval with explicit NON-EXHAUSTIVE SILVER vs expert-validated GOLD separation.

Example:
  python evaluate_retrieval.py --predictions predictions.jsonl --mode silver --split test

Predictions JSONL (ranked best first):
  {"question_id":"FOMC_001","retrieved":[{"page_id":"monetary20210127a1.pdf#p1"}, ...]}

A chunk-level retrieval must carry source page metadata. We report page-level proxy retrieval,
NOT evidence-span/chunk metrics. Duplicate pages get credited only once.
"""
import argparse,collections,csv,json,math,sys
from pathlib import Path
from fomcrag.metrics import CONVENTIONS, select_budget

ROOT=Path(__file__).resolve().parent

def readjsonl(path):
 with open(path,encoding='utf-8') as f:
  for s in f:
   if s.strip():yield json.loads(s)
def rowscsv(path):
 with open(path,encoding='utf-8-sig',newline='') as f:yield from csv.DictReader(f)
def unique_pages(results,k):
 """Legacy helper: UNIQUE-PAGE@k, potentially consuming more than k chunks."""
 if k<1:raise ValueError('k must be >=1')
 out=[];seen=set()
 for result in results:
  pid=result if isinstance(result,str) else result.get('page_id')
  if not pid and isinstance(result,dict):
   if result.get('document') and result.get('page'):pid=f"{Path(result['document']).name}#p{int(result['page'])}"
  if not pid:raise ValueError('Each retrieved hit must contain page_id or (document, page).')
  if pid not in seen:out.append(pid);seen.add(pid)
  if len(out)>=k:break
 return out

def check_gold_manifest(path):
 if not path or not Path(path).exists():raise ValueError('GOLD evaluation requires a validated completion manifest supplied via --gold-manifest.')
 obj=json.loads(Path(path).read_text(encoding='utf-8'))
 if not (obj.get('two_annotators_completed') is True and obj.get('cross_year_pooling_completed') is True and obj.get('adjudication_completed') is True):
  raise ValueError('Gold manifest is incomplete. Do not report official nDCG/Recall as finalized yet.')

def grade_map(mode,path):
 d=collections.defaultdict(dict)
 for r in rowscsv(path):
  q=r['question_id'];page=r['page_id']
  val=r.get('relevance_grade',r.get('grade_provisional','')) if mode=='silver' else r.get('final_grade',r.get('adjudicated_grade',''))
  if val is None or str(val).strip()=='':continue
  v=int(float(val));assert 0<=v<=2
  d[q][page]=max(d[q].get(page,0),v)
 return d

def main():
 ap=argparse.ArgumentParser(description='FOMC: page-level retrieval evaluation (initial silver / validated gold).')
 ap.add_argument('--predictions',required=True)
 ap.add_argument('--mode',choices=['silver','gold'],default='silver')
 ap.add_argument('--split',choices=['dev','validation','test','all'],default='test')
 ap.add_argument('--k',type=int,default=5)
 ap.add_argument('--convention',choices=CONVENTIONS,required=True,help='Explicit budget; chunk@k requires chunk judgments not supplied by this page evaluator.')
 ap.add_argument('--qrels')
 ap.add_argument('--gold-manifest')
 ap.add_argument('--output')
 a=ap.parse_args()
 if a.k<1:ap.error('--k must be >=1')
 if a.convention=='chunk@k':ap.error('Page qrels cannot score chunk@k. Supply independently judged chunk qrels to a chunk evaluator.')
 if a.mode=='gold':check_gold_manifest(a.gold_manifest)
 rels=grade_map(a.mode,a.qrels or ROOT/('qrels_group_confirmed_PAGES.csv' if a.mode=='silver' else 'validated_qrels.csv'))
 questions=list(readjsonl(ROOT/'queries_145.jsonl'))
 targets={q['question_id']:q for q in questions if a.split=='all' or q['split']==a.split}
 if not targets:raise ValueError('No target questions')
 preds={r.get('question_id'):r.get('retrieved',r.get('results',[])) for r in readjsonl(a.predictions)}
 missing=set(targets)-set(preds)
 if missing:raise ValueError(f'Missing predictions for {len(missing)} questions, examples: {sorted(missing)[:8]}')
 details=[]
 for qid in targets:
  budget=select_budget(preds[qid],a.k,a.convention)
  returned=budget['pages'];lab=rels.get(qid,{})
  if not any(v>0 for v in lab.values()):raise ValueError(f'No positive reference pages for {qid}.')
  if a.mode=='gold' and any(p not in lab for p in returned):
   raise ValueError(f'Gold evaluation refused: unjudged returned page(s) for {qid}; pool and judge all systems first.')
  grades=[lab.get(x) for x in returned]
  positives=sum(1 for v in lab.values() if v>0)
  hits=[(i,v) for i,v in enumerate(grades,1) if v is not None and v>0]
  hit=bool(hits)
  n_known_hits=len(hits)
  rrate=n_known_hits/positives
  mrr=1/hits[0][0] if hit else 0
  # nDCG is exploratory in silver: unjudged pages are treated as zero *for computation only*;
  # not an inferred negative label, nor an unbiased estimator of true nDCG.
  gains=[(2**(v or 0)-1)/math.log2(i+1) for i,v in enumerate(grades,1)]
  ideal=sorted([v for v in lab.values() if v>0],reverse=True)[:a.k]
  idcg=sum((2**v-1)/math.log2(i+2) for i,v in enumerate(ideal))
  ndcg=sum(gains)/idcg if idcg else 0
  details.append(dict(question_id=qid,split=targets[qid]['split'],convention=a.convention,consumed_chunks=budget['consumed_chunks'],known_positive_hit_at_k=int(hit),known_positive_coverage_at_k=rrate,first_known_positive_rr=mrr,seed_ndcg_at_k=ndcg,known_positive_pages=n_known_hits,known_positive_pages_in_qrels=positives,judged_returned_pages=sum(v is not None for v in grades),unjudged_returned_pages=sum(v is None for v in grades),retrieved_unique_pages=len(returned),retrieved_page_ids=';'.join(returned)))
 agg={k:sum(float(d[k]) for d in details)/len(details) for k in ('known_positive_hit_at_k','known_positive_coverage_at_k','first_known_positive_rr','seed_ndcg_at_k','unjudged_returned_pages')}
 result={'mode':a.mode,'split':a.split,'k':a.k,'convention':a.convention,'questions':len(details),'metrics':{a.convention+'/'+key:value for key,value in agg.items()},'qualification':('GROUP_CONFIRMED_KNOWN_POSITIVE_QRELS_NON_EXHAUSTIVE; NOT UNBIASED FULL RECALL/PRECISION/NDCG' if a.mode=='silver' else 'GOLD_PAGE_LEVEL_METRICS_REVIEWED_POOL'), 'unit':'source PDF pages under explicit chunk/page budget', 'consumed_chunks':sum(d['consumed_chunks'] for d in details)}
 print(json.dumps(result,ensure_ascii=False,indent=2))
 if a.output:
  with open(a.output,'w',encoding='utf-8') as f:json.dump({'summary':result,'per_question':details},f,ensure_ascii=False,indent=2)
if __name__=='__main__':main()
