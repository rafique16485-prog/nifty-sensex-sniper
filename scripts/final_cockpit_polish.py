from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

CSS = r'''
<style id="final-cockpit-css">
@media(max-width:600px){
  body{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;background:#eef3f8!important;color:#10213b!important}
  .app{max-width:540px!important;background:#f7f9fc!important;padding-bottom:70px!important}
  .header{background:#071b3a!important;padding:12px 14px 11px!important;border-radius:0 0 18px 18px!important}
  .brand{font-size:21px!important;font-weight:900!important;letter-spacing:-.35px!important}
  .sub{font-size:10px!important}
  .live{font-size:10px!important;padding:7px 10px!important}
  .updated{font-size:10px!important}
  .grid{padding:8px 8px 5px!important;gap:7px!important}
  .card{min-height:116px!important;padding:11px 10px!important;border-radius:13px!important}
  .label{font-size:11px!important;font-weight:800!important}
  .value{font-size:23px!important;line-height:1.05!important}
  .chg{font-size:14px!important}
  .muted{font-size:10px!important}
  .search{grid-template-columns:minmax(0,1fr) 128px!important;gap:7px!important;padding:8px!important}
  .search input,.search button{height:52px!important;font-size:15px!important;border-radius:13px!important}
  .search input{padding:0 13px!important}
  .chips{gap:7px!important;padding:4px 8px 10px!important}
  .chip{font-size:12px!important;padding:9px 14px!important}
  .section{padding:2px 8px 9px!important}
  .verdict{padding:12px!important;border-radius:15px!important}
  .vtitle{font-size:15px!important}.confidence{font-size:10px!important}
  .big{font-size:34px!important;margin-top:11px!important}
  .vreason{font-size:13px!important;line-height:1.35!important}
  .vstat{padding:10px!important}.vstat small{font-size:11px!important}.vstat b{font-size:19px!important}
  .tabs{gap:7px!important;padding:5px 8px 9px!important}
  .tab{min-height:48px!important;font-size:12px!important;padding:9px 5px!important}
  .panel{margin:0 8px 10px!important;border-radius:14px!important}
  .panel-head{padding:12px!important}.panel-head b{font-size:14px!important}
  .news{grid-template-columns:72px minmax(0,1fr) 16px!important;padding:11px 0!important}
  .news-title{font-size:12px!important;line-height:1.3!important}.source,.news-time{font-size:10px!important}
  .intelline,.event-row{font-size:11px!important;line-height:1.45!important}
  .swing-wrap{padding:10px!important}.swing{min-width:172px!important;padding:10px!important}
  .swing b{font-size:13px!important}.price{font-size:19px!important}.pct{font-size:13px!important}
  .more{height:46px!important;margin:4px 8px 14px!important;width:calc(100% - 16px)!important;font-size:12px!important}
  .bottom{height:68px!important}.navbtn{font-size:11px!important}.navbtn b{font-size:23px!important}
  #stockResult{display:none}.result{font-size:12px!important}.rchip{font-size:11px!important;padding:9px!important}.rchip b{font-size:14px!important}
  #finalRefreshBtn{border:0;background:transparent;color:#fff;font-size:21px;line-height:1;cursor:pointer;padding:7px;touch-action:manipulation}
  #finalToast{position:fixed;left:50%;bottom:78px;transform:translateX(-50%);z-index:120;background:#071b3a;color:#fff;padding:9px 13px;border-radius:999px;font-size:11px;font-weight:800;display:none;box-shadow:0 5px 18px #10213b35}
  .final-modal-body{font-size:13px;line-height:1.5;color:#52647a}
  .final-modal-actions{display:grid;gap:8px;margin-top:10px}.final-modal-actions button{height:44px;border:1px solid #d7e2ed;border-radius:11px;background:#f5f8fb;font-weight:850;color:#10213b}
}
</style>
'''

JS = r'''
<script id="final-cockpit-js">
(function(){
  function toast(msg){let t=document.getElementById('finalToast');if(!t){t=document.createElement('div');t.id='finalToast';document.body.appendChild(t)}t.textContent=msg;t.style.display='block';clearTimeout(window.__ft);window.__ft=setTimeout(()=>t.style.display='none',1800)}
  function replaceButton(id){const old=document.getElementById(id);if(!old||old.dataset.finalWired==='1')return old;const b=old.cloneNode(true);old.replaceWith(b);b.dataset.finalWired='1';return b}
  function showPanel(name){
    const map={news:'newsPanel',smart:'smartPanel',swing:'swingV2',scanner:'scannerPanel'};
    Object.entries(map).forEach(([k,id])=>{const el=document.getElementById(id);if(el)el.style.display=k===name?'block':'none'});
    document.querySelectorAll('.tab[data-tab]').forEach(x=>x.classList.toggle('active',x.dataset.tab===name));
    const target=document.getElementById(map[name]);if(target)target.scrollIntoView({behavior:'smooth',block:'nearest'});
    if(name==='smart'&&window.loadSmart)window.loadSmart();
    if(name==='swing'&&window.loadSwing)window.loadSwing();
  }
  function wireTabs(){document.querySelectorAll('.tab[data-tab]').forEach(tab=>{if(tab.dataset.finalWired==='1')return;tab.dataset.finalWired='1';tab.addEventListener('click',e=>{e.preventDefault();showPanel(tab.dataset.tab)})})}
  function wireAnalyze(){
    const b=replaceButton('analyzeBtn'),input=document.getElementById('stockInput'),box=document.getElementById('stockResult');if(!b||!input||!box)return;
    b.addEventListener('click',async()=>{const symbol=input.value.trim().toUpperCase();if(symbol.length<2){input.focus();toast('Enter a stock symbol');return}b.disabled=true;b.textContent='Analyzing…';box.style.display='block';box.innerHTML='<div class="result"><b>🔎 Analyzing '+symbol+'…</b><div class="intelline">Checking NIFTY 500 membership, daily trend, volume, relative strength and SMC.</div></div>';
      try{const r=await fetch('/api/stock-analysis?symbol='+encodeURIComponent(symbol)+'&ts='+Date.now(),{cache:'no-store'}),d=await r.json();if(!d.ok||!d.result)throw Error(d.error||'Live analysis unavailable');const x=d.result;const cls=String(x.action||'WAIT').toLowerCase();box.innerHTML='<div class="result"><div class="panel-head"><b>🎯 '+x.symbol+' • Swing Analysis</b><span class="statuspill">'+x.action+'</span></div><div class="result-grid">'+[['Price',x.current_price],['Score',x.score+'/10'],['Lifecycle',x.lifecycle],['Setup',x.setup],['Trend',x.trend],['Volume',x.volume],['RS vs NIFTY',x.relative_strength_pct+'%'],['Holding',x.holding_period],['Entry',x.entry],['Stop Loss',x.stoploss],['Target 1',x.target1],['Target 2',x.target2],['R:R',x.rr],['SMC',x.smc?.status]].map(a=>'<div class="rchip"><span>'+a[0]+'</span><b>'+String(a[1]==null?'—':a[1])+'</b></div>').join('')+'</div><div class="intelline"><b>Why:</b> '+String(x.reason||'Confirmation based analysis.')+'</div><div class="intelline"><b>Invalidation:</b> '+String(x.invalidation||'Wait for confirmation')+'</div><div class="final-modal-actions"><button type="button" id="addWatchFinal">☆ Add to Watchlist</button></div></div>';const wb=document.getElementById('addWatchFinal');if(wb)wb.onclick=()=>{let a=[];try{a=JSON.parse(localStorage.getItem('sniperWatchlist')||'[]')}catch(_){}if(!a.includes(x.symbol))a.push(x.symbol);localStorage.setItem('sniperWatchlist',JSON.stringify(a));toast(x.symbol+' added to Watchlist')};
      }catch(e){box.innerHTML='<div class="result"><div class="error">⚠ '+String(e.message||e)+'</div><div class="intelline">No fallback guess is generated when live stock analysis is unavailable.</div></div>'}finally{b.disabled=false;b.textContent='🔎 Analyze'}});
    input.addEventListener('keydown',e=>{if(e.key==='Enter')b.click()});
  }
  function wireChips(){const examples={"Banking":'HDFCBANK',"IT":'INFY',"FMCG":'ITC',"Auto":'MARUTI'};document.querySelectorAll('.chip').forEach(c=>{if(c.dataset.finalWired==='1')return;c.dataset.finalWired='1';c.addEventListener('click',()=>{document.querySelectorAll('.chip').forEach(z=>z.classList.remove('active'));c.classList.add('active');const q=examples[c.textContent.trim()];if(q){const i=document.getElementById('stockInput');i.value=q;i.focus();toast('Ready to analyze '+q)}else if(c.textContent.includes('NIFTY 500'))toast('NIFTY 500 universe selected');else toast(c.textContent.trim()+' filter selected')})})}
  function wireNav(){document.querySelectorAll('#sniperNav [data-nav]').forEach(n=>{if(n.dataset.finalWired==='1')return;n.dataset.finalWired='1';n.addEventListener('click',e=>{e.preventDefault();document.querySelectorAll('#sniperNav [data-nav]').forEach(x=>x.classList.remove('active'));n.classList.add('active');const key=n.dataset.nav;if(key==='dashboard')window.scrollTo({top:0,behavior:'smooth'});else if(key==='scanner')showPanel('scanner');else if(key==='news')showPanel('news');else if(key==='watchlist'){let a=[];try{a=JSON.parse(localStorage.getItem('sniperWatchlist')||'[]')}catch(_){}openModal('Watchlist',a.length?a.map(x=>'• '+x).join('<br>'):'No stocks saved yet. Analyze a stock and add it to Watchlist.')}else if(key==='settings')openModal('Settings','Data source: Upstox server-side API<br>Refresh: automatic<br>Mode: Educational / probabilistic<br><br>API secrets are not shown in the browser.')})})}
  function openModal(title,html){const m=document.getElementById('modal');if(!m)return;document.getElementById('modalTitle').textContent=title;document.getElementById('modalBody').innerHTML='<div class="final-modal-body">'+html+'</div>';m.classList.add('open')}
  function wireExtras(){const b=replaceButton('moreDetailsBtn');if(b)b.addEventListener('click',()=>{const app=document.querySelector('.app');if(!app)return;const open=app.classList.toggle('details-open');b.textContent=open?'▴ LESS DETAILS':'▾ MORE DETAILS';toast(open?'More details opened':'Details collapsed')});const close=document.getElementById('closeModal');if(close&&close.dataset.finalWired!=='1'){close.dataset.finalWired='1';close.addEventListener('click',()=>document.getElementById('modal')?.classList.remove('open'))}document.getElementById('modal')?.addEventListener('click',e=>{if(e.target.id==='modal')e.currentTarget.classList.remove('open')});const bell=document.querySelector('.bell');if(bell&&bell.dataset.finalWired!=='1'){bell.dataset.finalWired='1';bell.addEventListener('click',()=>showPanel('news'))}const menu=document.querySelector('.menu');if(menu&&menu.dataset.finalWired!=='1'){menu.dataset.finalWired='1';menu.addEventListener('click',()=>openModal('NIFTY Sensex Sniper','Dashboard • Scanner • Watchlist • News • Settings<br><br>All sections are connected to the live analysis APIs where available.'))}}
  function addRefresh(){const u=document.getElementById('updated');if(!u||document.getElementById('finalRefreshBtn'))return;const b=document.createElement('button');b.id='finalRefreshBtn';b.type='button';b.textContent='↻';b.title='Refresh all data';u.parentNode.appendChild(b);b.onclick=async()=>{toast('Refreshing market intelligence…');if(window.loadLive)await window.loadLive();if(window.loadNews)await window.loadNews();if(window.loadSmart)await window.loadSmart();if(window.loadEvents)await window.loadEvents();if(window.loadSwing)await window.loadSwing();}};
  function boot(){wireTabs();wireAnalyze();wireChips();wireNav();wireExtras();addRefresh();if(!document.getElementById('finalCockpitBanner')){const x=document.createElement('div');x.id='finalCockpitBanner';x.style.display='none';document.body.appendChild(x)}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();setTimeout(boot,700);setTimeout(boot,1800);
  window.finalShowPanel=showPanel;
})();
</script>
'''

if 'id="final-cockpit-css"' not in s:
    s = s.replace('</head>', CSS + '</head>', 1)
if 'id="final-cockpit-js"' not in s:
    s = s.replace('</body>', JS + '</body>', 1)
p.write_text(s, encoding='utf-8')
print('final cockpit polish applied')
