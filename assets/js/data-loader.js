const DIR = '../../';
export async function loadRepository(base=DIR){
  const files={meta:'data/meta.json',actors:'data/actors.json',claims:'data/claims.json',evidence:'data/evidence.json',relations:'data/relations.json',sources:'data/sources.json',content:'data/content.json',synthesis:'data/synthesis.json',taxonomy:'config/taxonomy.json'};
  const pairs=await Promise.all(Object.entries(files).map(async([key,path])=>{const resp=await fetch(base+path,{cache:'no-store'});if(!resp.ok)throw new Error(`Impossible de charger ${path} : ${resp.status}`);return[key,await resp.json()]}));
  const d=Object.fromEntries(pairs);
  d.actorById=new Map(d.actors.map(a=>[a.id,a]));d.evidenceById=new Map(d.evidence.map(e=>[e.id,e]));d.sourceById=new Map(d.sources.map(s=>[s.id,s]));d.claimByActor=new Map(d.claims.filter(c=>c.claim_type==='position').map(c=>[c.subject_id,c]));return d;
}
export function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
export function normal(v){return String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()}
export function srcHtml(d,sourceId,compact=false){const s=d.sourceById.get(sourceId);if(!s||!s.url)return '<span class="muted">Source indisponible</span>';const label=compact?s.publisher:(s.title||s.publisher);return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`}
export function evidenceHtml(d,ids=[]){if(!ids.length)return '<p class="muted">Aucune preuve qualifiée publiée pour cet objet.</p>';return ids.map(id=>{const e=d.evidenceById.get(id);if(!e)return `<div class="warning">Preuve ${esc(id)} non résolue</div>`;const s=d.sourceById.get(e.source_id);return `<article class="proof"><div class="proof-kind">${esc(e.type==='exact_quote'?'Citation littérale':'Résumé documentaire')} ${e.status?.includes('xlsx')?'<span class="tag">Extrait de corpus</span>':''}</div><p>${esc(e.text)}</p><div class="proof-foot">${srcHtml(d,e.source_id)}<span>${esc(s?.published_at||'Date non renseignée')}</span></div>${e.source_location?`<small class="muted">${esc(e.source_location)}</small>`:''}</article>`}).join('')}
export function actorClaim(d,id){return d.claimByActor.get(id)}
export function relationName(d,x){return d.taxonomy.relation_types[x.type]?.label||x.type}
export function stanceName(d,c){return c?d.taxonomy.stances[c.value]?.label||c.value:'Position non documentée'}
export function linkedEvidence(d,ids){return ids?.map(id=>d.evidenceById.get(id)).filter(Boolean)||[]}
