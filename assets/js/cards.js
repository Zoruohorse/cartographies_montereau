import{loadRepository,esc,norm,actorClaim,evidenceHtml}from'./data-loader.js';const d=await loadRepository();const categories=document.getElementById('categories'),stances=document.getElementById('stances'),count=document.getElementById('count'),grid=document.getElementById('grid'),search=document.getElementById('search'),reset=document.getElementById('reset'),detail=document.getElementById('detail'),dialog=document.getElementById('dialog');let cat='all',stance='all',q='';document.getElementById('title').textContent=d.meta.title;document.getElementById('subtitle').textContent=d.meta.subtitle;document.getElementById('notice').textContent=d.meta.data_notice;const stanceColor=s=>d.taxonomy.stances[s]?.color||'#64748b';function filters(){categories.innerHTML=Object.entries(d.taxonomy.categories).map(([k,v])=>`<button class="filter ${cat===k?'active':''}" data-cat="${k}"><span>${esc(v.label)}</span><b>${k==='all'?d.actors.filter(a=>a.display_in_cards!==false).length:d.actors.filter(a=>a.display_in_cards!==false&&a.categories.includes(k)).length}</b></button>`).join('');stances.innerHTML=Object.entries(d.taxonomy.stances).map(([k,v])=>`<button class="filter ${stance===k?'active':''}" data-stance="${k}"><span>${esc(v.label)}</span><b>${k==='all'?d.claims.length:d.claims.filter(c=>c.value===k).length}</b></button>`).join('')}function render(){const list=d.actors.filter(a=>a.display_in_cards!==false).filter(a=>{const c=actorClaim(d,a.id);const text=norm([a.name,a.description,c?.summary,...(c?.evidence_ids||[]).map(id=>d.evidenceById.get(id)?.text)].join(' '));return(cat==='all'||a.categories.includes(cat))&&(stance==='all'||c?.value===stance)&&(!q||text.includes(q))});count.textContent=`${list.length} acteurs affichés sur ${d.actors.filter(a=>a.display_in_cards!==false).length}`;grid.innerHTML=list.map(a=>{const c=actorClaim(d,a.id);return `<article class="card" data-id="${a.id}" style="--stance:${stanceColor(c?.value)}"><h3>${esc(a.name)}</h3><div class="role">${esc(a.description)}</div><p class="position">${esc(c?.summary||'Position non renseignée')}</p><div class="footer"><span class="badge">${esc(d.taxonomy.stances[c?.value]?.label||'Non qualifié')}</span><span>Certitude : ${esc(d.taxonomy.certainty_levels[c?.certainty]?.label||'Non qualifiée')}</span></div></article>`}).join('')}function open(id){const a=d.actorById.get(id),c=actorClaim(d,id);const rel=d.relations.filter(r=>r.source_id===id||r.target_id===id);detail.innerHTML=`<h2>${esc(a.name)}</h2><p class="role">${esc(a.description)}</p><h3>Position</h3><p>${esc(c?.summary||'Non renseignée')}</p><p><b>Certitude :</b> ${esc(d.taxonomy.certainty_levels[c?.certainty]?.label||'Non qualifiée')}</p><h3>Preuves et sources</h3>${evidenceHtml(d,c?.evidence_ids)}<h3>Relations documentables</h3>${rel.length?rel.map(r=>{const other=d.actorById.get(r.source_id===id?r.target_id:r.source_id);return `<div class="relation"><button data-open="${other?.id}">${esc(other?.name||'Acteur inconnu')}</button><div><b>${esc(d.taxonomy.relation_types[r.type]?.label||r.type)}</b></div><p>${esc(r.summary)}</p><small>Certitude : ${esc(d.taxonomy.certainty_levels[r.certainty]?.label||r.certainty)} · ${r.evidence_ids.length} preuve(s)</small></div>`}).join(''):'<p class="muted">Aucune relation.</p>'}`;if(!dialog.open)dialog.showModal()}document.addEventListener('click',e=>{const c=e.target.closest('[data-cat]'),s=e.target.closest('[data-stance]'),card=e.target.closest('.card'),op=e.target.closest('[data-open]');if(c){cat=c.dataset.cat;filters();render()}if(s){stance=s.dataset.stance;filters();render()}if(card)open(card.dataset.id);if(op)open(op.dataset.open)});search.addEventListener('input',e=>{q=norm(e.target.value);render()});reset.onclick=()=>{cat='all';stance='all';q='';search.value='';filters();render()};document.querySelector('.close').onclick=()=>dialog.close();filters();render();


/* Cartes et filtres identiques au modèle Escaudain ;
   affichage adapté des sources et de la chronologie Montereau. */
const synthesis=d.synthesis;
function citationLinks(ids=[]){
  const found=new Map();
  for(const id of ids){
    const ev=d.evidenceById.get(id);
    const source=ev?d.sourceById.get(ev.source_id):null;
    if(source&&source.url)found.set(source.id,source);
  }
  return Array.from(found.values()).map(s=>'<a href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer" title="'+esc(s.title)+'">'+esc(s.publisher||s.title)+'</a>').join(' · ');
}
function supporting(ids=[]){
  const links=citationLinks(ids);
  return links?'<div class="source-citations">Sources : '+links+'</div>':'';
}
function setTab(key){
  document.querySelectorAll('[data-tab]').forEach(btn=>{
    const active=btn.dataset.tab===key;
    btn.classList.toggle('active',active);
    btn.setAttribute('aria-selected',String(active));
  });
  document.querySelectorAll('.tab-pane').forEach(p=>p.classList.toggle('active',p.id==='tab-'+key));
}
document.querySelectorAll('[data-tab]').forEach(btn=>btn.addEventListener('click',()=>setTab(btn.dataset.tab)));
document.getElementById('griefGrid').innerHTML=synthesis.griefs.length
  ?synthesis.griefs.map(g=>'<article class="griefCard"><h2>'+esc(g.title)+'</h2><p>'+esc(g.text)+'</p>'+supporting(g.evidence_ids)+'</article>').join('')
  :'<p class="muted">Aucun enjeu documenté.</p>';
document.getElementById('vigilance').innerHTML=synthesis.vigilance.map(v=>'<li><strong>'+esc(v.title)+'</strong><p>'+esc(v.text)+'</p>'+supporting(v.evidence_ids)+'</li>').join('');
document.getElementById('sources').innerHTML=d.sources.filter(s=>s.url).map(s=>'<li><a href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer">'+esc(s.publisher)+' — '+esc(s.title)+'</a> <small class="muted">('+esc(s.published_at||'date non précisée')+' ; '+(s.consultation==='directly_consulted'?'consultée directement':'référence du corpus')+')</small></li>').join('');
const period=m=>m.period_precision==='year'?m.date.slice(0,4):m.period_precision==='month'?m.date.slice(0,7):m.date;
document.getElementById('timelineGrid').innerHTML=d.content.milestones.map(m=>'<article class="griefCard '+(m.status==='forecast'?'chrono-forecast':'')+'"><div class="chrono-date">'+esc(period(m))+' · '+(m.status==='forecast'?'PRÉVISION':'DOCUMENTÉ')+'</div><h2>'+esc(m.title)+'</h2><p>'+esc(m.details)+'</p>'+supporting(m.evidence_ids)+'</article>').join('');
document.getElementById('factGrid').innerHTML=d.content.fact_sheet.map(f=>'<article class="griefCard"><h2>'+esc(f.label)+'</h2><p><strong>'+esc(f.value)+'</strong></p><p class="muted">'+esc(f.qualifier)+'</p>'+supporting(f.evidence_ids)+'</article>').join('');
