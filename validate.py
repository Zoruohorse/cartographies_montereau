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


# Extension 2026-11-09 — sources du bail EDF–OpCore et nouvel onglet d’évolution.
from datetime import date
from urllib.parse import urlsplit
import re
timeline=load('data/timeline.json')
timeline_ids=unique('premières apparitions',timeline)
assert len(timeline)==20 and len({x['actor_id'] for x in timeline})==20
assert tax['timeline']['event_type']=='first_documented_appearance'
timeline_cats={x['id'] for x in tax['timeline']['categories']}
timeline_stances={x['id'] for x in tax['timeline']['stances']}
by_claim={x['subject_id']:x['value'] for x in c}
sources={x['id']:x for x in s}
ev_by_id={x['id']:x for x in e}
dated=undated=0
for x in timeline:
 assert x['actor_id'] in A and x['category'] in timeline_cats and x['stance'] in timeline_stances,x['id']
 assert x['stance']==by_claim.get(x['actor_id'],'unknown'),x['id']
 assert x['scope'] in ('direct','context'),x['id']
 assert x.get('source_ids') and x.get('evidence_ids'),x['id']
 assert all(k in E for k in x['evidence_ids']),x['id']
 for sid in x['source_ids']:
  assert sid in sources and urlsplit(sources[sid]['url']).scheme=='https',x['id']
 if x['status']=='confirmed':
  dated+=1
  val=x['date']
  if x['date_precision']=='month':
   assert re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])',val),x['id']
   moment=date.fromisoformat(val+'-01')
  else:
   assert x['date_precision']=='day',x['id']
   moment=date.fromisoformat(val)
  assert moment<=date(2026,11,9),x['id']
 else:
  undated+=1
  assert x['status']=='undated' and x['date'] is None and x['date_precision']=='unknown',x['id']

assert dated==18 and undated==2, 'Données de datation à requalifier'
assert sum(x['stance']=='favorable' for x in timeline if x['status']=='confirmed')==17
assert sum(x['stance']=='opposed' for x in timeline if x['status']=='confirmed')==0
for group in (syn['griefs'],syn['vigilance'],co['milestones'],co['fact_sheet']):
 for x in group:
  assert x['evidence_ids'],x.get('title',x.get('label'))
  for id in x['evidence_ids']:
   assert id in ev_by_id, id
   assert sources[ev_by_id[id]['source_id']]['url'].startswith('https://'),id

assert sources['source_0023']['publisher']=='EDF / Institut Paris Region'
bail=[x for x in co['milestones'] if x['status']=='contractual_reported']
assert len(bail)==1 and bail[0]['date']=='2026-05' and 'evidence_0045' in bail[0]['evidence_ids']
assert any(x['id']=='evidence_0045' and x['source_id']=='source_0023' for x in e)
for x in co['milestones']:
 if x['period_precision']=='year':assert re.fullmatch(r'\d{4}',x['date']),x['title']
 elif x['period_precision']=='month':assert re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])',x['date']),x['title']
 else:date.fromisoformat(x['date'])

page=(root/'apps/cards/index.html').read_text(encoding='utf-8')
for tab in ('carto','griefs','watch','timeline','evolution'):
 assert f'data-tab="{tab}"' in page and f'id="tab-{tab}"' in page,tab
assert len(re.findall(r'data-tab="[^"]+"',page))==5
assert (root/'assets/js/evolution.js').is_file() and (root/'assets/css/evolution.css').is_file()
evo_js=(root/'assets/js/evolution.js').read_text(encoding='utf-8')
for mode in ('new','cumulative','stance'):
 assert f'data-mode="{mode}"' in evo_js,mode
assert "timeline:'data/timeline.json'" in (root/'assets/js/data-loader.js').read_text(encoding='utf-8')
print(f'EXTENSION OK — {dated} acteurs datables, {undated} non datés, {len(co["milestones"])} jalons, {len(syn["griefs"])} thèmes, bail EDF sourcé et 5 onglets.')
