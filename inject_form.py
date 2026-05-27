#!/usr/bin/env python3
"""Injects multi-step consultation form into all 6 style HTML files."""
import os, re

FORM_CSS = """
<style id="cf-styles">
/* ── Multi-step Consultation Form ─────────────────────────────────────── */
#consult-overlay {
  position: fixed; inset: 0;
  background: rgba(10,8,20,.65);
  z-index: 9999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 16px;
}
#consult-overlay.open { display: flex; }
.cf-card {
  background: #fff;
  border-radius: 16px;
  width: min(520px, calc(100vw - 32px));
  max-height: 88vh;
  overflow-y: auto;
  box-shadow: 0 24px 80px rgba(0,0,0,.35);
  position: relative;
  font-family: inherit;
}
.cf-progress-track {
  height: 4px;
  background: #F3F4F6;
  border-radius: 16px 16px 0 0;
  overflow: hidden;
}
.cf-progress-fill {
  height: 100%;
  background: var(--accent, #7B4F9E);
  width: 0%;
  transition: width .4s cubic-bezier(.4,0,.2,1);
}
.cf-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px 0;
}
.cf-step-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent, #7B4F9E);
  letter-spacing: .08em;
  text-transform: uppercase;
}
.cf-close {
  background: none; border: none;
  font-size: 18px; cursor: pointer;
  color: #9CA3AF; padding: 4px 8px;
  border-radius: 6px; line-height: 1;
}
.cf-close:hover { color: #374151; background: #F3F4F6; }
.cf-steps-wrap { padding: 20px 24px 8px; }
.cf-step { display: none; }
.cf-step.cf-active {
  display: block;
  animation: cfSlideIn .28s ease;
}
@keyframes cfSlideIn {
  from { opacity: 0; transform: translateX(14px); }
  to   { opacity: 1; transform: translateX(0); }
}
.cf-question {
  font-size: clamp(17px,2.2vw,22px);
  font-weight: 800;
  color: #1A1525;
  margin: 0 0 18px;
  line-height: 1.3;
}
/* Card options (2-col grid) */
.cf-options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 6px;
}
.cf-option-card {
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  padding: 13px 14px;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  text-align: left;
  background: #fff;
  transition: border-color .15s, background .15s;
  width: 100%;
  font-family: inherit;
}
.cf-option-card:hover  { border-color: var(--accent, #7B4F9E); background: #FAF8FC; }
.cf-option-card.cf-sel { border-color: var(--accent, #7B4F9E); background: var(--accent-lt, #EDE5F5); }
.cf-opt-icon  { font-size: 20px; flex-shrink: 0; margin-top: 1px; }
.cf-opt-label { font-size: 13px; font-weight: 700; color: #1A1525; line-height: 1.2; display: block; }
.cf-opt-sub   { font-size: 11px; color: #6B7280; margin-top: 2px; display: block; }
/* Radio list */
.cf-radio-list  { display: flex; flex-direction: column; gap: 10px; margin-bottom: 6px; }
.cf-radio-item {
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  padding: 13px 16px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  transition: border-color .15s, background .15s;
  width: 100%;
  font-family: inherit;
  text-align: left;
}
.cf-radio-item:hover  { border-color: var(--accent, #7B4F9E); background: #FAF8FC; }
.cf-radio-item.cf-sel { border-color: var(--accent, #7B4F9E); background: var(--accent-lt, #EDE5F5); color: #1A1525; }
.cf-radio-dot {
  width: 18px; height: 18px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  transition: border-color .15s, background .15s;
}
.cf-radio-item.cf-sel .cf-radio-dot {
  border-color: var(--accent, #7B4F9E);
  background: var(--accent, #7B4F9E);
}
.cf-radio-item.cf-sel .cf-radio-dot::after {
  content: '';
  width: 6px; height: 6px;
  background: #fff; border-radius: 50%;
}
/* Text fields */
.cf-fields { display: flex; flex-direction: column; gap: 14px; margin-bottom: 6px; }
.cf-field-wrap { display: flex; flex-direction: column; gap: 5px; }
.cf-field-label { font-size: 13px; font-weight: 600; color: #374151; }
.cf-field-input {
  height: 46px;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  padding: 0 14px;
  font-size: 15px;
  color: #1A1525;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  font-family: inherit;
  background: #fff;
  transition: border-color .15s, box-shadow .15s;
}
.cf-field-input:focus {
  border-color: var(--accent, #7B4F9E);
  box-shadow: 0 0 0 3px rgba(123,79,158,.1);
}
/* Confirmation */
.cf-confirm { text-align: center; padding: 16px 0 12px; }
.cf-confirm-icon  { font-size: 52px; margin-bottom: 16px; }
.cf-confirm-title { font-size: 22px; font-weight: 800; color: #1A1525; margin-bottom: 10px; }
.cf-confirm-body  { font-size: 15px; color: #6B7280; line-height: 1.65; }
/* Nav bar */
.cf-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px 22px;
  border-top: 1px solid #F3F4F6;
}
.cf-btn-back {
  background: none; border: none;
  font-size: 14px; font-weight: 600;
  color: #6B7280; cursor: pointer;
  padding: 10px 0; font-family: inherit;
}
.cf-btn-back:hover { color: #374151; }
.cf-btn-next {
  background: var(--accent, #7B4F9E);
  color: #fff; border: none;
  border-radius: 100px;
  padding: 12px 26px;
  font-size: 14px; font-weight: 800;
  cursor: pointer;
  font-family: inherit;
  transition: opacity .15s;
  letter-spacing: .02em;
}
.cf-btn-next:hover    { opacity: .88; }
.cf-btn-next:disabled { opacity: .4; cursor: not-allowed; }
@media(max-width:480px){
  .cf-options-grid { grid-template-columns: 1fr; }
  .cf-card { border-radius: 12px; }
  .cf-steps-wrap { padding: 16px 16px 6px; }
  .cf-nav { padding: 12px 16px 18px; }
  .cf-header { padding: 16px 16px 0; }
}
</style>
"""

FORM_HTML = """
<!-- ── Multi-step Consultation Form Modal ──────────────────────────────── -->
<div id="consult-overlay" onclick="if(event.target===this)cfClose()">
  <div class="cf-card" role="dialog" aria-modal="true" aria-label="Schedule a Consultation">
    <div class="cf-progress-track">
      <div id="cf-prog" class="cf-progress-fill"></div>
    </div>
    <div class="cf-header">
      <span id="cf-lbl" class="cf-step-label">Step 1 of 5</span>
      <button class="cf-close" onclick="cfClose()" aria-label="Close">&#10005;</button>
    </div>
    <div id="cf-wrap" class="cf-steps-wrap"></div>
    <div class="cf-nav">
      <button id="cf-back" class="cf-btn-back" onclick="cfBack()" style="visibility:hidden">&#8592; Back</button>
      <button id="cf-next" class="cf-btn-next" onclick="cfNext()" disabled>Continue &#8594;</button>
    </div>
  </div>
</div>
"""

FORM_JS = """
<script>
// ── CONFIG: swap these per client ─────────────────────────────────────────
var CF_STEPS = [
  { id:'reason', type:'cards', q:'What brings you in?',
    opts:[
      {ic:'&#129504;', lb:'Individual Therapy',   sb:'Personal growth & healing'},
      {ic:'&#128145;', lb:'Couples Therapy',       sb:'Relationship support'},
      {ic:'&#128260;', lb:'Trauma & EMDR',         sb:'Processing past experiences'},
      {ic:'&#127807;', lb:'Anxiety & Depression',  sb:'Managing daily struggles'},
      {ic:'&#128138;', lb:'Substance Abuse',       sb:'Recovery & sobriety support'},
      {ic:'&#10024;',  lb:'Not sure yet',          sb:"I'd like to explore options"},
    ]},
  { id:'history', type:'radio', q:'Have you been to therapy before?',
    opts:[
      {lb:'Yes, regularly'},
      {lb:"Yes, but it's been a while"},
      {lb:'No — this would be my first time'},
    ]},
  { id:'feeling', type:'radio', q:'How are you feeling about starting?',
    opts:[
      {lb:'Nervous but ready'},
      {lb:'Hopeful and motivated'},
      {lb:'Overwhelmed — I need guidance'},
      {lb:'Just exploring for now'},
    ]},
  { id:'avail', type:'cards', q:'When are you typically available?',
    opts:[
      {ic:'&#127749;', lb:'Mornings',   sb:'Before noon'},
      {ic:'&#9728;&#65039;',  lb:'Afternoons', sb:'12pm – 5pm'},
      {ic:'&#127750;', lb:'Evenings',   sb:'After 5pm'},
      {ic:'&#128197;', lb:'Flexible',   sb:'Any time works'},
    ]},
  { id:'contact', type:'fields', q:'How should Lauren reach you?',
    fields:[
      {n:'name',  lb:'Your name',         t:'text',  req:true},
      {n:'email', lb:'Email address',     t:'email', req:true},
      {n:'phone', lb:'Phone (optional)',  t:'tel',   req:false},
    ]},
];
var CF_DONE = {
  ic:'&#127807;',
  tt:"You're all set!",
  bd:'Lauren will reach out within 24 hours to schedule your free consultation. You can also call directly at <a href="tel:4048778806" style="color:var(--accent,#7B4F9E);font-weight:700">404-877-8806</a>.'
};
// ──────────────────────────────────────────────────────────────────────────

var cfIdx = 0, cfAns = {};

function cfOpen(){ cfIdx=0; cfBuild(); cfPaint(); document.getElementById('consult-overlay').classList.add('open'); document.body.style.overflow='hidden'; }
function cfClose(){ document.getElementById('consult-overlay').classList.remove('open'); document.body.style.overflow=''; }

function cfBuild(){
  var w = document.getElementById('cf-wrap'); w.innerHTML='';
  CF_STEPS.forEach(function(s,i){
    var d=document.createElement('div');
    d.className='cf-step'+(i===0?' cf-active':'');
    d.id='cf-s'+i; d.innerHTML=cfStepHTML(s,i); w.appendChild(d);
  });
  var c=document.createElement('div');
  c.className='cf-step'; c.id='cf-sdone';
  c.innerHTML='<div class="cf-confirm"><div class="cf-confirm-icon">'+CF_DONE.ic+'</div><div class="cf-confirm-title">'+CF_DONE.tt+'</div><div class="cf-confirm-body">'+CF_DONE.bd+'</div></div>';
  w.appendChild(c);
}

function cfStepHTML(s,i){
  var h='<p class="cf-question">'+s.q+'</p>';
  if(s.type==='cards'){
    h+='<div class="cf-options-grid">';
    s.opts.forEach(function(o,j){
      var sel=cfAns[s.id]===j?' cf-sel':'';
      h+='<button class="cf-option-card'+sel+'" onclick="cfPick('+i+','+j+')" type="button"><span class="cf-opt-icon">'+o.ic+'</span><span><span class="cf-opt-label">'+o.lb+'</span>'+(o.sb?'<span class="cf-opt-sub">'+o.sb+'</span>':'')+'</span></button>';
    });
    h+='</div>';
  } else if(s.type==='radio'){
    h+='<div class="cf-radio-list">';
    s.opts.forEach(function(o,j){
      var sel=cfAns[s.id]===j?' cf-sel':'';
      h+='<button class="cf-radio-item'+sel+'" onclick="cfPick('+i+','+j+')" type="button"><span class="cf-radio-dot"></span>'+o.lb+'</button>';
    });
    h+='</div>';
  } else if(s.type==='fields'){
    h+='<div class="cf-fields">';
    s.fields.forEach(function(f,j){
      var v=(cfAns[s.id]&&cfAns[s.id][f.n])||'';
      h+='<div class="cf-field-wrap"><label class="cf-field-label">'+f.lb+(f.req?'':' <span style="color:#9CA3AF;font-weight:400">(optional)</span>')+'</label><input class="cf-field-input" type="'+f.t+'" placeholder="'+f.lb+'" value="'+v+'" oninput="cfFieldIn('+i+','+j+',this.value)" /></div>';
    });
    h+='</div>';
  }
  return h;
}

function cfPick(si,oi){
  var s=CF_STEPS[si]; cfAns[s.id]=oi;
  document.querySelectorAll('#cf-s'+si+' .cf-option-card, #cf-s'+si+' .cf-radio-item').forEach(function(el,i){ el.classList.toggle('cf-sel',i===oi); });
  cfPaint();
  if(s.type!=='fields') setTimeout(cfNext,320);
}

function cfFieldIn(si,fi,v){
  var s=CF_STEPS[si];
  if(!cfAns[s.id]) cfAns[s.id]={};
  cfAns[s.id][s.fields[fi].n]=v;
  cfPaint();
}

function cfNext(){
  var nb=document.getElementById('cf-next'); if(nb.disabled) return;
  var cur=document.getElementById(cfIdx<CF_STEPS.length?'cf-s'+cfIdx:'cf-sdone');
  if(cur) cur.classList.remove('cf-active');
  cfIdx++;
  var nxt=document.getElementById(cfIdx<CF_STEPS.length?'cf-s'+cfIdx:'cf-sdone');
  if(nxt) nxt.classList.add('cf-active');
  cfPaint();
}

function cfBack(){
  if(cfIdx===0) return;
  var cur=document.getElementById(cfIdx<CF_STEPS.length?'cf-s'+cfIdx:'cf-sdone');
  if(cur) cur.classList.remove('cf-active');
  cfIdx--;
  document.getElementById('cf-s'+cfIdx).classList.add('cf-active');
  cfPaint();
}

function cfPaint(){
  var tot=CF_STEPS.length, done=cfIdx>=tot;
  document.getElementById('cf-prog').style.width=(done?100:Math.round(cfIdx/tot*100))+'%';
  document.getElementById('cf-lbl').textContent=done?'Complete!':'Step '+(cfIdx+1)+' of '+tot;
  var bb=document.getElementById('cf-back'), nb=document.getElementById('cf-next');
  bb.style.visibility=(cfIdx>0&&!done)?'visible':'hidden';
  if(done){ nb.textContent='Close'; nb.disabled=false; nb.onclick=cfClose; return; }
  nb.textContent=(cfIdx===tot-1)?'Submit →':'Continue →';
  nb.onclick=cfNext;
  var s=CF_STEPS[cfIdx], ok=false;
  if(s.type==='fields'){
    var req=s.fields.filter(function(f){return f.req;});
    ok=req.every(function(f){return cfAns[s.id]&&cfAns[s.id][f.n]&&cfAns[s.id][f.n].trim();});
  } else { ok=cfAns[s.id]!==undefined; }
  nb.disabled=!ok;
}

// Auto-bind to any CTA whose text includes these keywords (excluding footer/nav)
document.addEventListener('DOMContentLoaded',function(){
  var words=['schedule','book a','consult','first step','get started','begin your'];
  document.querySelectorAll('a,button').forEach(function(el){
    var txt=el.textContent.toLowerCase().trim();
    var inFooter=!!el.closest('footer'), inNav=!!el.closest('nav');
    if(!inFooter && !inNav && words.some(function(w){return txt.indexOf(w)>-1;})){
      el.addEventListener('click',function(e){e.preventDefault();cfOpen();});
    }
  });
});
</script>
"""

INJECT = FORM_CSS + FORM_HTML + FORM_JS

styles = ['style-1','style-2','style-3','style-4','style-5','style-6','style-7','style-8','style-9']
base   = '/tmp/laur-deroc'

for s in styles:
    path = f'{base}/{s}/index.html'
    with open(path,'r') as f: html = f.read()

    # Ensure --accent-lt is defined if missing (fallback for styles that don't define it)
    if '--accent-lt' not in html:
        html = html.replace(':root {', ':root {\n  --accent-lt: #EDE5F5;', 1)

    # Inject before </body>
    if '</body>' in html:
        html = html.replace('</body>', INJECT + '\n</body>', 1)
    else:
        html += INJECT

    with open(path,'w') as f: f.write(html)
    size = os.path.getsize(path)
    print(f'  {s}: form injected ({size:,} bytes)')

print('\nAll 6 files updated.')
