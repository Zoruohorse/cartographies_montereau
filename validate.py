"""Contrôle d'intégrité et d'objectivité minimale de la cartographie Montereau."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
root=Path(__file__).resolve().parent
load=lambda name:json.loads((root/name).read_text(encoding='utf-8'))
a=load('data/actors.json');c=load('data/claims.json');e=load('data/evidence.json');r=load('data/relations.json');s=load('data/sources.json');syn=load('data/synthesis.json');m=load('data/meta.json');tax=load('config/taxonomy.json');co=load('data/content.json')

def unique(label,items):
 ids=[x['id'] for x in items]; assert len(ids)==len(set(ids)),f"{label}: doublons {[(k,v) for k,v in Counter(ids).items() if v>1]}"; return set(ids)
A=unique('acteurs',a);C=unique('positions',c);E=unique('preuves',e);R=unique('relations',r);S=unique('sources',s)
assert m['id']=='project_montereau' and m['id'] in A and m['last_updated']
assert all(x['categories'] and all(y in tax['categories'] for y in x['categories']) for x in a), 'Catégories invalides'
assert any(x['id']=='project_montereau' and x.get('display_in_cards') is False for x in a)
used=set()
for x in c:
 assert x['subject_id'] in A and x['project_id'] in A and x['claim_type']=='position',x['id']
 assert x['value'] in ('favorable','neutral','opposed') and x['certainty'] in tax['certainty_levels'],x['id']
 assert x['evidence_ids'] and set(x['evidence_ids'])<=E,x['id']; used.update(x['evidence_ids'])
for x in r:
 assert x['source_id'] in A and x['target_id'] in A and x['source_id']!=x['target_id'],x['id']
 assert x['type'] in tax['relation_types'] and x['certainty'] in tax['certainty_levels'],x['id']
 assert x['evidence_ids'] and set(x['evidence_ids'])<=E,x['id'];used.update(x['evidence_ids'])
for group in [syn['griefs'],syn['vigilance'],co['fact_sheet'],co['milestones']]:
 for x in group:
  assert x.get('evidence_ids') and set(x['evidence_ids'])<=E,'missing proof in synthesis/content'
  used.update(x['evidence_ids'])
assert used==E, f"Preuves non rattachées : {sorted(E-used)}"
source_index={x['id']:x for x in s}
for x in s:
 parsed=urlparse(x['url']); assert parsed.scheme in ('http','https') and parsed.netloc and 'news.google.com' not in parsed.netloc,x['id']
 assert x.get('title') and x.get('publisher') and x.get('consultation') in ('directly_consulted','supplied_xlsx_extract'),x['id']
for x in e:
 assert x['source_id'] in S and x['text'] and x['source_location'] and x['type'] in ('exact_quote','reported_summary'),x['id']
 assert x['source_status']=='qualified'
assert len([x for x in c if x['value']=='opposed'])==0, 'Opposition locale formelle non documentée'
assert len([x for x in a if x['id']=='project_montereau'])==1
print(f"VALIDATION OK — {len(a)} nœuds, {len(c)} positions, {len(r)} relations, {len(e)} preuves, {len(s)} sources URL, {len(syn['griefs'])} thèmes, {len(syn['vigilance'])} vigilances")
