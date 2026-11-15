#!/usr/bin/env python3
"""Paired test-only robustness for 30 FOMC information needs.

Input main_predictions.jsonl: all 145 main query predictions (or at least the 30 test parents).
Input variant_predictions.jsonl: 30 test-only variant queries.
Outputs *exploratory* known-positive diagnostics unless human gold qrels are supplied.
"""
import json,math,csv,argparse,collections,random,statistics
from pathlib import Path
from fomcrag.metrics import select_budget
ROOT=Path(__file__).resolve().parent

def loadjsonl(p):
 with open(p,encoding='utf-8') as f:return [json.loads(s) for s in f if s.strip()]
def loadcsv(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def retrieved_pages(pred,k,convention):
 return select_budget(pred,k,convention)['pages']

def one_score(pages,r,k):
 known=[(i+1,r[p]) for i,p in enumerate(pages) if p in r and r[p]>0]
 first=1/known[0][0] if known else 0
 hit=int(bool(known))
 npositives=sum(x>0 for x in r.values())
 coverage=len(known)/npositives if npositives else 0
 idcg=sum((2**g-1)/math.log2(i+2) for i,g in enumerate(sorted([v for v in r.values() if v>0],reverse=True)[:k]))
 dcg=sum((2**r.get(p,0)-1)/math.log2(i+2) for i,p in enumerate(pages))
 return (hit,coverage,first,dcg/idcg if idcg else 0)

def main():
 p=argparse.ArgumentParser();p.add_argument('--main-predictions',required=True);p.add_argument('--variant-predictions',required=True);p.add_argument('--k',type=int,default=5);p.add_argument('--output');p.add_argument('--convention',choices=['page-coverage-from-chunk@k','unique-page@k'],required=True);a=p.parse_args()
 variants=loadjsonl(ROOT/'robustness_30_TEST_ONLY.jsonl')
 qr=collections.defaultdict(dict)
 for v in loadcsv(ROOT/'qrels_group_confirmed_PAGES.csv'):
  qr[v['question_id']][v['page_id']]=int(v['relevance_grade'])
 main={r['question_id']:r.get('retrieved',r.get('results',[])) for r in loadjsonl(a.main_predictions)}
 pred={r['question_id']:r.get('retrieved',r.get('results',[])) for r in loadjsonl(a.variant_predictions)}
 metricnames=[a.convention+'/'+m for m in ['known_hit@k','known_coverage@k','known_mrr@k','seed_ndcg@k']]
 rows=[]
 for v in variants:
  pid=v['parent_question_id'];vid=v['question_id']
  if pid not in main or vid not in pred:raise ValueError(f'Missing {pid} or {vid} predictions')
  src=qr[pid];b=one_score(retrieved_pages(main[pid],a.k,a.convention),src,a.k);z=one_score(retrieved_pages(pred[vid],a.k,a.convention),src,a.k)
  row={'parent_question_id':pid,'variant_id':vid}
  row.update({f'baseline_{m}':b[i] for i,m in enumerate(metricnames)})
  row.update({f'paraphrase_{m}':z[i] for i,m in enumerate(metricnames)})
  row.update({f'delta_{m}':z[i]-b[i] for i,m in enumerate(metricnames)})
  rows.append(row)
 rng=random.Random(1114)
 result={}
 for m in metricnames:
  diffs=[x[f'delta_{m}'] for x in rows]
  resamples=[sum(diffs[rng.randrange(len(diffs))] for _ in diffs)/len(diffs) for j in range(2000)]
  vals=sorted(resamples);result[m]={'mean_delta':round(sum(diffs)/len(diffs),4),'bootstrap_95pct_CI':[round(vals[49],4),round(vals[1949],4)]}
 result={'status':'GROUP_CONFIRMED_KNOWN_POSITIVE_DIAGNOSTIC_ONLY','test_pairs':len(rows),'k':a.k,'paired_deltas':result,'warning':'Not a gold standard; unknown relevance may bias all metric differences; no model performance claimed by this script alone.'}
 print(json.dumps(result,ensure_ascii=False,indent=2))
 if a.output:Path(a.output).write_text(json.dumps({'summary':result,'per_pair':rows},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
