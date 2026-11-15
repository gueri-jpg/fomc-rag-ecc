#!/usr/bin/env python3
"""No third-party dependencies. Inspect the Codex kit, statuses, splits and controlled qrels."""
import csv, json, collections, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'evaluation'/'benchmark'

def records(n):
    with (B/n).open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def jsonl(n):return [json.loads(x) for x in (B/n).read_text(encoding='utf-8').splitlines() if x.strip()]

def main():
    errors=[]
    needed=['AGENTS.md','CODEX_MASTER_PROMPT.md','README_COMMENCER_ICI.md','project_spec/CONSIGNES_OFFICIELLES.md',
            'project_spec/VALIDATION_BENCHMARK_ET_QRELS.md','prompts/01_PHASE_0_AUDIT.md','prompts/02_PHASE_1_CORPUS_EDA.md',
            'prompts/08_PHASE_7_STREAMLIT_LOCAL.md','evaluation/benchmark/validate_benchmark.py']
    for name in needed:
        if not (ROOT/name).is_file():errors.append(f'Missing {name}')
    qs=jsonl('queries_145.jsonl');ids={q['question_id'] for q in qs}
    if len(qs)!=145 or len(ids)!=145:errors.append('Expected 145 unique main queries')
    splits=collections.Counter(q.get('split') for q in qs)
    if splits!={'dev':85,'validation':30,'test':30}:errors.append(f'Wrong split {dict(splits)}')
    ev=jsonl('evidence_citations_145.jsonl')
    status=collections.Counter(e['candidate_status']=='EXCLUDE_SCOPE' for e in ev)
    if len(ev)!=296 or status[True]!=2:errors.append('Expected 296 evidence rows with 2 excluded')
    r=records('qrels_group_confirmed_PAGES.csv')
    pairs={(row['question_id'],row['page_id']) for row in r}
    if len(r)!=len(pairs)!=279:errors.append('Duplicate or missing 279 page qrels')
    if len(r)!=279 or len(pairs)!=279:errors.append(f'Expected 279 unique qrels, got {len(r)}/{len(pairs)}')
    grade_count=collections.Counter(row['relevance_grade'] for row in r)
    if grade_count!={'1':91,'2':188}:errors.append(f'Unexpected judged grades {dict(grade_count)}')
    if any(x['question_id'] not in ids for x in r):errors.append('Orphan qrel question')
    if any(x['validation_status']!='CONFIRMED_BY_GROUP_USER_REPORT' for x in r):errors.append('Unexpected validation status')
    qrel_lines=[x.split() for x in (B/'qrels_group_confirmed_PAGES.trec').read_text(encoding='utf-8').splitlines() if x.strip()]
    if len(qrel_lines)!=len(r) or {(a,c,d) for a,b,c,d in qrel_lines}!={(row['question_id'],row['page_id'],row['relevance_grade']) for row in r}:
        errors.append('TREC qrels are out of sync with CSV')
    variants=jsonl('robustness_30_TEST_ONLY.jsonl')
    test_ids={q['question_id'] for q in qs if q['split']=='test'}
    if len(variants)!=30 or {v['parent_question_id'] for v in variants}!=test_ids or any(v['split']!='test' for v in variants):
        errors.append('Variants must contain one TEST paraphrase per test query')
    neg=records('unanswerable_10_NOT_GOLD.csv')
    if len(neg)!=10 or any(str(n.get('approved','')).upper()=='YES' for n in neg):errors.append('10 unanswerable candidates must remain disabled')
    metadata=json.loads((B/'GROUP_VALIDATION_STATUS.json').read_text(encoding='utf-8'))
    if metadata.get('individual_annotation_files_received') is not False or metadata.get('can_claim_measured_inter_annotator_agreement') is not False:errors.append('Approval provenance should not fabricate annotator sheets')
    cfg=json.loads((ROOT/'configs/experiment_protocol.json').read_text(encoding='utf-8'))
    if cfg['deployment']['docker_required'] or not cfg['deployment']['streamlit_local_required']:errors.append('V2 must require local Streamlit, not Docker')
    if cfg['corpus']['automatic_year_filter']:errors.append('Automatic year filter must be false')
    if errors:
        for error in errors:print('FAIL:',error)
        raise SystemExit(1)
    print('PASS kit V2: 145 queries [85/30/30], 279 group-confirmed page qrels [188 grade2, 91 grade1], 294 source positives + 2 excluded, 30 TEST paraphrases, 10 disabled negative candidates.')
    print('PASS scope: all-year retrieval, Streamlit-local demo required, Docker/cloud optional.')
    print('CAVEAT: this does not verify gold exhaustiveness or independent annotator agreement.')

if __name__=='__main__':main()
