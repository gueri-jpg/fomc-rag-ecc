#!/usr/bin/env python3
"""Assemble judged qrels from TWO annotators plus optional adjudication.

Only explicit adjudicated or mutually agreed 0/1/2 labels are exported.
Never infer 0 from lack of annotation. Does NOT certify exhaustive relevance.
"""
import argparse,csv,collections
from pathlib import Path
R=Path(__file__).resolve().parent

def parse(v):
 v=str(v).strip()
 if not v:return None
 if v not in {'0','1','2'}:raise ValueError(f'Invalid grade {v!r}')
 return int(v)
def main():
 p=argparse.ArgumentParser();p.add_argument('--annotations',default=str(R/'qrels_double_annotation_TEMPLATE.csv'));p.add_argument('--pooling',default=str(R/'POOLING_TO_REVIEW_1740.csv'));p.add_argument('--output',default=str(R/'validated_qrels.csv'));a=p.parse_args()
 entries=[]
 for source in [a.annotations,a.pooling]:
  with open(source,encoding='utf-8-sig',newline='') as f:entries.extend(list(csv.DictReader(f)))
 resolved=collections.defaultdict(list);disagreements=[];missing=[]
 for r in entries:
  A=parse(r.get('annotation_A',r.get('grade_annotator_A','')))
  B=parse(r.get('annotation_B',r.get('grade_annotator_B','')))
  final=parse(r.get('adjudicated_grade',r.get('final_grade','')))
  if final is not None:
   if A is None or B is None:missing.append(r);continue
   g=final
  elif A is not None and B is not None:
   if A!=B:disagreements.append(r);continue
   g=A
  else:missing.append(r);continue
  resolved[(r['question_id'],r['page_id'])].append(g)
 with open(a.output,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['question_id','page_id','final_grade']);w.writeheader()
  for (q,p),vals in sorted(resolved.items()):
   if len(set(vals))>1:raise ValueError(f'Disagreeing labels for duplicate {q} {p}: {vals}')
   w.writerow({'question_id':q,'page_id':p,'final_grade':vals[0]})
 print(f'Resolved unique page qrels: {len(resolved)}; missing labels {len(missing)}; unresolved disagreements {len(disagreements)}')
 print('NOTE: This file is NOT certified gold until cross-year pooling, independent review, and adjudication are documented.')
if __name__=='__main__':main()
