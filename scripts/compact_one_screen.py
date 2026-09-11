from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = r'''
/* SNIPER ONE-SCREEN MODE */
@media (max-width:600px){
  body{background:#eef3f8}
  .app{max-width:540px;min-height:100vh;padding-bottom:70px}
  .top{padding:10px 14px 9px}.brand{font-size:18px}.sub{font-size:9px}.pill{padding:5px 8px;margin-top:6px}
  .grid{padding:8px;gap:7px}.card{border-radius:12px;padding:9px}.label{font-size:9px}.value{font-size:17px;margin-top:2px}
  .section{padding:2px 9px}.section h2{font-size:13px;margin:8px 2px 6px}
  .verdict{padding:11px;border-radius:14px}.big{font-size:27px}.score{margin:7px 0;height:6px}.row{padding:7px;border-radius:9px}
  .status,.age{padding:7px;margin-top:5px;font-size:10px}.button{padding:9px;margin-top:6px}
  /* ONE-SCREEN: hide secondary sections below the cockpit on mobile. */
  .app > .section:nth-of-type(n+4){display:none}
  .one-screen-details{display:block!important}
  .nav{height:58px}.nav b{font-size:15px}.nav span{font-size:8px}
}
.one-screen-details{margin-top:7px}
.os-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.os-chip{background:#f3f7fb;border:1px solid #dce5ef;border-radius:9px;padding:7px 5px;text-align:center;font-size:9px}
.os-chip b{display:block;font-size:11px;margin-top:2px}
.os-plan{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:7px}
.os-plan div{background:#fff;border:1px solid #dce5ef;border-radius:9px;padding:7px;text-align:center}
.os-plan span{display:block;font-size:8px;color:#718198}.os-plan b{font-size:12px}
.os-reason{margin-top:7px;padding:7px 9px;border-radius:9px;background:#fff;border:1px solid #dce5ef;font-size:9px;line-height:1.35}
'''

marker = '</style>'
if 'SNIPER ONE-SCREEN MODE' not in s:
    s = s.replace(marker, css + '\n' + marker, 1)

needle = '<div class="status" id="status">'
if 'id="oneScreenDetails"' not in s:
    insert = '''<div class="one-screen-details" id="oneScreenDetails">
<div class="os-grid">
<div class="os-chip"><span>NIFTY</span><b id="osNifty">—</b></div>
<div class="os-chip"><span>SENSEX</span><b id="osSensex">—</b></div>
<div class="os-chip"><span>OPTIONS</span><b id="osOptions">—</b></div>
<div class="os-chip"><span>SMC</span><b id="osSmc">—</b></div>
<div class="os-chip"><span>LIQUIDITY</span><b id="osLiquidity">—</b></div>
<div class="os-chip"><span>NEWS</span><b id="osNews">—</b></div>
</div>
<div class="os-plan">
<div><span>ENTRY</span><b id="osEntry">—</b></div>
<div><span>STOP LOSS</span><b id="osStop">—</b></div>
<div><span>TARGET</span><b id="osTarget">—</b></div>
</div>
<div class="os-reason" id="osReason">🛡️ Waiting for live confirmation.</div>
</div>'''
    s = s.replace(needle, insert + '\n' + needle, 1)

if 'function loadOneScreen()' not in s:
    script = r'''<script>
(function(){
  const $=id=>document.getElementById(id);
  const text=(id,v)=>{const e=$(id);if(e)e.textContent=v==null||v===''?'—':String(v)};
  const side=v=>{v=String(v||'').toUpperCase();return v.includes('BULL')||v==='CALL'||v==='CE'?'BULLISH':v.includes('BEAR')||v==='PUT'||v==='PE'?'BEARISH':'MIXED'};
  async function get(u){const r=await fetch(u+(u.includes('?')?'&':'?')+'ts='+Date.now(),{cache:'no-store'});return r.json()}
  async function loadOneScreen(){
    try{
      const [live,plan,news]=await Promise.all([get('/api/live?action=engine'),get('/api/plan'),get('/api/news-intel')]);
      const n=live.nifty||{},s=live.sensex||{};
      text('osNifty',side(n.side||n.bias||live.nifty_bias));
      text('osSensex',side(s.side||s.bias||live.sensex_bias));
      text('osOptions',side(live.optionFactor||live.option_factor||live.options?.side||live.options?.bias));
      text('osSmc',side(live.smcFactor||live.smc_factor||live.smc?.side||live.smc?.bias));
      text('osLiquidity',live.liquidity?.label||live.liquidityFactor||live.liquidity_factor||'WAIT');
      text('osNews',side(news?.side||'NEUTRAL'));
      const pl=plan&&plan.plan?plan.plan:{};
      text('osEntry',pl.entry==null?'—':pl.entry);text('osStop',pl.stoploss==null?'—':pl.stoploss);text('osTarget',pl.target1==null?'—':pl.target1);
      text('osReason',plan?.reason||plan?.gate||'🛡️ Waiting for confirmation.');
    }catch(e){text('osReason','🛡️ Live confirmation unavailable — NO TRADE.')}
  }
  window.loadOneScreen=loadOneScreen;loadOneScreen();setInterval(loadOneScreen,30000);
})();
</script>'''
    s = s.replace('</body>', script + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('compact one-screen patch applied')
