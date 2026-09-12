from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

style='''<style id="reference-mobile-ui-css">
/* REFERENCE MOBILE UI — readable, dense, Upstox/Groww-inspired */
@media (max-width:600px){
  html,body{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
  body{font-size:14px!important;line-height:1.35!important;overflow-x:hidden!important}
  .app{width:100%!important;max-width:540px!important;margin:0 auto!important;padding-bottom:74px!important;background:#f6f8fb!important}
  .top{padding:12px 14px 10px!important;border-radius:0 0 16px 16px!important}
  .brand{font-size:20px!important;line-height:1.15!important;letter-spacing:-.35px!important}
  .sub{font-size:10px!important;line-height:1.3!important;margin-top:3px!important}
  .pill{font-size:10px!important;padding:6px 9px!important;margin-top:7px!important}
  .grid{padding:9px 8px 5px!important;gap:7px!important}
  .card{padding:10px!important;border-radius:12px!important}
  .label{font-size:10px!important;line-height:1.2!important}
  .value{font-size:20px!important;line-height:1.12!important;font-weight:900!important}
  .section{padding:3px 8px!important}
  .section h2{font-size:15px!important;line-height:1.25!important;margin:8px 2px 6px!important}
  .cue,.row,.level,.tip,.status,.age{font-size:12px!important;line-height:1.4!important;padding:8px!important}
  .cue b,.row b,.level b{font-size:13px!important}
  .verdict{padding:11px!important;border-radius:14px!important}
  .verdict .big{font-size:30px!important;line-height:1.05!important}
  .verdict .row{padding:8px!important}
  .verdict .row b{font-size:15px!important}
  .one-screen-details,.swing-v2,.intel-panel{font-size:12px!important;line-height:1.4!important}
  .swing-card{padding:9px 0!important}
  .swing-top{font-size:13px!important}
  .swing-meta{font-size:11px!important;line-height:1.45!important}
  .intel-title{font-size:13px!important;font-weight:900!important}
  .intel-panel{padding:10px!important;border-radius:12px!important}
  .intel-panel *{font-size:12px!important;line-height:1.4!important}
  .more-details,.button{font-size:12px!important;padding:10px!important;min-height:40px!important}
  .nav{height:64px!important}
  .nav b{font-size:19px!important}
  .nav span{font-size:10px!important;font-weight:700!important}
  .stock-search-wrap{margin:7px 8px 4px!important;display:grid!important;grid-template-columns:minmax(0,1fr) 104px!important;gap:7px!important;align-items:center!important}
  .stock-search-input{width:100%!important;height:46px!important;border:1px solid #d4dfeb!important;border-radius:12px!important;background:#fff!important;color:#10213b!important;font-size:14px!important;padding:0 13px!important;outline:none!important;box-shadow:0 2px 8px rgba(16,33,59,.06)!important}
  .stock-search-input:focus{border-color:#1676d2!important;box-shadow:0 0 0 3px rgba(22,118,210,.12)!important}
  .stock-search-btn{height:46px!important;border:0!important;border-radius:12px!important;background:#126bd6!important;color:#fff!important;font-size:14px!important;font-weight:900!important;cursor:pointer!important;touch-action:manipulation!important}
  .stock-search-btn:active{transform:scale(.98)!important}
  .stock-analysis-panel{margin:5px 8px 7px!important;background:#fff!important;border:1px solid #d9e3ee!important;border-radius:13px!important;padding:10px!important;box-shadow:0 3px 12px rgba(16,33,59,.06)!important}
  .stock-analysis-title{font-size:13px!important;font-weight:900!important;color:#10213b!important;margin-bottom:6px!important}
  .stock-analysis-body{font-size:12px!important;line-height:1.45!important;color:#40536b!important}
  .stock-analysis-body b{color:#10213b!important}
  .stock-analysis-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:6px!important;margin-top:7px!important}
  .stock-analysis-chip{background:#f5f8fb!important;border:1px solid #e0e7ef!important;border-radius:9px!important;padding:7px!important;font-size:11px!important}
  .stock-analysis-chip b{display:block!important;font-size:13px!important;margin-top:2px!important}
  .search-error{color:#c33a4e!important;background:#fff5f6!important;border:1px solid #f1ccd2!important;border-radius:8px!important;padding:8px!important}
}
@media (min-width:601px){
  .stock-search-wrap{margin:10px auto;max-width:700px;display:grid;grid-template-columns:1fr 120px;gap:8px}
  .stock-search-input{height:44px;padding:0 12px;font-size:14px;border:1px solid #d4dfeb;border-radius:10px}
  .stock-search-btn{height:44px;border:0;border-radius:10px;background:#126bd6;color:#fff;font-weight:900}
  .stock-analysis-panel{max-width:700px;margin:8px auto;background:#fff;border:1px solid #d9e3ee;border-radius:12px;padding:12px}
}
</style>'''
if 'id="reference-mobile-ui-css"' not in s:
    s=s.replace('</head>',style+'</head>',1)

search='''<div class="stock-search-wrap" id="stockSearchWrap">
  <input id="stockSearchInput" class="stock-search-input" type="search" inputmode="text" autocomplete="off" placeholder="🔎 Search stock: RELIANCE, TCS, HDFCBANK" aria-label="Search stock">
  <button id="stockAnalyzeBtn" class="stock-search-btn" type="button">🔎 Analyze</button>
</div>
<div class="stock-analysis-panel" id="stockAnalysisPanel" hidden>
  <div class="stock-analysis-title">📊 Stock Swing Analysis</div>
  <div class="stock-analysis-body" id="stockAnalysisBody">Enter a NIFTY 500 stock and tap Analyze.</div>
</div>'''
if 'id="stockSearchWrap"' not in s:
    # Put search immediately before the first major section so it stays near the top.
    marker='<div class="section"><h2>🎯 Sniper Verdict'
    if marker in s:
        s=s.replace(marker,search+'\n'+marker,1)
    else:
        marker='<main>'
        if marker in s:s=s.replace(marker,marker+'\n'+search,1)

script='''<script id="stock-search-v1">
(function(){
  const input=document.getElementById('stockSearchInput'),btn=document.getElementById('stockAnalyzeBtn'),panel=document.getElementById('stockAnalysisPanel'),body=document.getElementById('stockAnalysisBody');
  if(!input||!btn||!panel||!body||btn.dataset.wired==='1')return;
  btn.dataset.wired='1';
  const esc=v=>String(v==null?'—':v).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  function render(r){const cls=String(r.action||'WAIT').toLowerCase();panel.hidden=false;body.innerHTML=`<div><b>${esc(r.symbol)}</b> • <b class="${cls}">${esc(r.action)}</b> • Score <b>${esc(r.score)}/10</b></div><div class="stock-analysis-grid"><div class="stock-analysis-chip">Trend<b>${esc(r.trend)}</b></div><div class="stock-analysis-chip">Setup<b>${esc(r.setup)}</b></div><div class="stock-analysis-chip">Entry<b>${esc(r.entry)}</b></div><div class="stock-analysis-chip">SL<b>${esc(r.stoploss)}</b></div><div class="stock-analysis-chip">T1 / T2<b>${esc(r.target1)} / ${esc(r.target2)}</b></div><div class="stock-analysis-chip">Holding<b>${esc(r.holding_period)}</b></div></div><div style="margin-top:7px">RS ${esc(r.relative_strength_pct)}% • Volume ${esc(r.volume)} • SMC ${esc(r.smc?.status)} • ${esc(r.lifecycle)}</div><div style="margin-top:5px">${esc(r.reason)}</div>`}
  async function analyze(){const sym=input.value.trim().toUpperCase();if(!sym)return;panel.hidden=false;body.textContent='⏳ Analyzing live NIFTY 500 data…';btn.disabled=true;btn.textContent='Analyzing…';try{const r=await fetch('/api/stock-analysis?symbol='+encodeURIComponent(sym)+'&ts='+Date.now(),{cache:'no-store'});const d=await r.json();if(!d.ok||!d.result){body.innerHTML='<div class="search-error">⚠️ '+esc(d.error||'Live analysis unavailable. No fallback guess is generated.')+'</div>';return}render(d.result)}catch(e){body.innerHTML='<div class="search-error">⚠️ Live analysis unavailable. Please try again.</div>'}finally{btn.disabled=false;btn.textContent='🔎 Analyze'}}
  btn.addEventListener('click',function(e){e.preventDefault();analyze()});input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();analyze()}});
})();
</script>'''
if 'id="stock-search-v1"' not in s:s=s.replace('</body>',script+'</body>',1)
p.write_text(s,encoding='utf-8')
