#!/usr/bin/env python3
"""Local non-network preflight for Codex handoff. Never prints any secret values."""
from __future__ import annotations
import argparse,csv,hashlib,json,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BENCH=ROOT/'evaluation'/'benchmark'
PDF_ROOT=ROOT/'utils'/'TxtExtraction'/'TextsData'

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--hash-pdfs',action='store_true',help='Verify PDF SHA256 (reads 93 PDF files)');ap.add_argument('--json-report',default='',help='Optional local JSON output report path');args=ap.parse_args()
    problems=[];warnings=[];facts={}
    if (ROOT/'.env').exists():warnings.append('Local .env exists: do not commit or display its contents; inspect git status/history safely.')
    if not (ROOT/'.gitignore').exists():problems.append('Missing .gitignore')
    manifest=BENCH/'MANIFESTE_CORPUS_93.csv'
    doc_pages={}
    if not manifest.exists():problems.append('Missing benchmark corpus manifest')
    else:
        docs=read_csv(manifest);facts['manifest_pdfs']=len(docs)
        doc_pages={r.get('document'):int(r.get('pdf_pages') or 0) for r in docs}
        if len(docs)!=93:problems.append(f'Expected 93 manifest PDFs, got {len(docs)}')
        facts['manifest_pages']=sum(int(x.get('pdf_pages') or 0) for x in docs)
        if facts['manifest_pages']!=838:problems.append('Unexpected corpus page total (expected 838)')
        facts['manifest_years']=dict(sorted(collections.Counter(x.get('year') for x in docs).items()))
        seen=set();pdf_count=0
        for r in docs:
            name=r.get('document','')
            rel=r.get('relative_path','').replace('\\','/')
            path=PDF_ROOT/rel.removeprefix('TextsData/')
            if not path.exists() and name:
                alt=list(PDF_ROOT.rglob(name))
                if len(alt)==1:path=alt[0]
            if name in seen:problems.append(f'Duplicate basename in manifest: {name}')
            seen.add(name)
            if not path.is_file():problems.append(f'Missing source PDF: {name} at {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}');continue
            pdf_count+=1
            if args.hash_pdfs and r.get('pdf_sha256'):
                h=hashlib.sha256()
                with path.open('rb') as inp:
                    for part in iter(lambda:inp.read(1024*1024),b''):h.update(part)
                if h.hexdigest()!=r['pdf_sha256']:problems.append(f'PDF SHA mismatch: {name}')
        facts['found_pdfs']=pdf_count
    audit=BENCH/'evidence_source_audit_145.csv'
    if audit.exists():
        ev=read_csv(audit)
        facts['source_audit_rows']=len(ev)
        facts['source_evidence_count']=sum(x.get('source_presence_verified')=='YES' for x in ev)
        facts['source_evidence_excluded']=sum(x.get('candidate_status')=='EXCLUDE_SCOPE' for x in ev)
        if len(ev)!=296 or facts['source_evidence_count']!=294 or facts['source_evidence_excluded']!=2:problems.append('Expected 296 audited source rows = 294 retained + 2 excluded')
        for row in ev:
            fn=row.get('document','');pg=row.get('page','')
            if fn not in doc_pages:problems.append(f'Evidence references unknown PDF: {fn}');continue
            try:n=int(pg)
            except ValueError:problems.append(f'Invalid evidence page: {fn} page {pg}');continue
            if n<1 or n>doc_pages[fn]:problems.append(f'Evidence page out of range: {fn} page {n}')
        if any(str(x.get('source_presence_verified','')).upper() not in ('YES','NOT_APPLICABLE_EXCLUDED') for x in ev):warnings.append('One or more source citations need textual source verification')
    else:problems.append('Missing source evidence audit file')
    qrels=BENCH/'silver_qrels_PAGES.trec'
    if qrels.exists():
        seen_qrels=set();n_rows=0
        for ln,line in enumerate(qrels.read_text(encoding='utf8').splitlines(),1):
            if not line.strip():continue
            fields=line.split()
            if len(fields)!=4:problems.append(f'Invalid TREC qrels line {ln}');continue
            qid,_,pid,g=fields;n_rows+=1
            if (qid,pid) in seen_qrels:problems.append(f'Duplicate qrel: {qid}/{pid}')
            seen_qrels.add((qid,pid))
            if '#p' not in pid:problems.append(f'Invalid page_id in qrels: {pid}');continue
            filename,page=pid.rsplit('#p',1)
            if filename not in doc_pages:problems.append(f'Qrel references unknown PDF: {filename}');continue
            try:page=int(page)
            except ValueError:problems.append(f'Invalid qrel page in {pid}');continue
            if page<1 or page>doc_pages[filename]:problems.append(f'Qrel page out of bounds: {pid}')
            if g not in {'0','1','2'}:problems.append(f'Invalid relevance grade {g}')
        facts['silver_qrel_question_pages']=n_rows
        if n_rows!=279:problems.append(f'Expected 279 silver question-page labels, got {n_rows}')
    else:problems.append('Missing silver_qrels_PAGES.trec')
    q_file=BENCH/'queries_145.jsonl';questions=[]
    if not q_file.exists():problems.append('Missing queries_145.jsonl')
    else:
        with q_file.open(encoding='utf-8') as fh:
            for li,line in enumerate(fh,1):
                if not line.strip():continue
                try:questions.append(json.loads(line))
                except Exception as exc:problems.append(f'JSON error in queries line {li}: {type(exc).__name__}')
        facts['queries_count']=len(questions)
        if len(questions)!=145:problems.append(f'Expected 145 main queries, got {len(questions)}')
        ids=[q.get('question_id') for q in questions]
        if len(ids)!=len(set(ids)):problems.append('Duplicate query IDs')
        if qrels.exists():
            orphaned=sorted({qid for qid,pid in seen_qrels if qid not in set(ids)})
            if orphaned:problems.append(f'Qrels with unknown questions: {orphaned[:10]}')
        counts=collections.Counter(q.get('split') for q in questions);facts['query_splits']=dict(counts)
        if counts != {'dev':85,'validation':30,'test':30}:problems.append(f'Unexpected split counts {dict(counts)}')
        if any(not str(q.get('question','')).strip() for q in questions):problems.append('Empty question found')
    bpath=BENCH/'benchmark_fomc_evaluation_silver_145.json'
    if bpath.exists():
        try:
            obj=json.loads(bpath.read_text(encoding='utf-8'));facts['benchmark_questions']=len(obj['questions']);facts['benchmark_paraphrases']=len(obj['paraphrases_test']);facts['benchmark_unanswerable_candidates']=len(obj['unanswerable_candidates_not_verified'])
            if facts['benchmark_questions']!=145 or facts['benchmark_paraphrases']!=30 or facts['benchmark_unanswerable_candidates']!=10:problems.append('Unexpected benchmark component counts')
        except Exception as exc:problems.append('Invalid combined benchmark: '+str(exc))
    else:problems.append('Missing combined benchmark')
    variants=BENCH/'robustness_30_TEST_ONLY.jsonl'
    if variants.exists():
        vs=[json.loads(l) for l in variants.read_text(encoding='utf-8').splitlines() if l.strip()]
        if len(vs)!=30:problems.append('Expected 30 robustness queries')
        question_ids={q['question_id'] for q in questions}
        for v in vs:
            if v.get('parent_question_id') not in question_ids:problems.append('Invalid robustness parent: '+str(v.get('parent_question_id')))
            if v.get('split')!='test':problems.append('Robustness variant outside test: '+str(v.get('question_id')))
            parent=next((q for q in questions if q['question_id']==v.get('parent_question_id')),None)
            if parent and parent.get('split')!='test':problems.append('Robustness parent outside test')
        facts['variants_count']=len(vs)
    else:problems.append('Missing robustness JSONL')
    neg=BENCH/'unanswerable_10_NOT_GOLD.csv'
    if neg.exists():
        negs=read_csv(neg);facts['negative_candidates']=len(negs)
        if len(negs)!=10:problems.append('Unexpected count of unanswerables')
        if any((r.get('approved') or '').upper() in ('YES','TRUE') for r in negs):warnings.append('One or more negative candidates marked approved; verify actual human approval.')
    else:problems.append('Missing negative candidates file')
    if (ROOT/'.git').exists():facts['git_present']=True
    else:warnings.append('Git directory not detected in local workspace; initialize/connect repository if required.')
    facts['status']='PASS' if not problems else 'FAIL'
    print('CODEX PREFLIGHT',facts['status'],'— project root:',ROOT)
    for k,v in facts.items():print(' ',k,':',v)
    for w in warnings:print(' WARNING:',w)
    for e in problems:print(' ERROR:',e)
    if args.json_report:
        out=Path(args.json_report);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps({'facts':facts,'warnings':warnings,'errors':problems},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if not problems else 1
if __name__=='__main__':sys.exit(main())
