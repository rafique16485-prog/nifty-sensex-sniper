from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = r'''
/* SNIPER TRUE ONE-SCREEN COCKPIT */
@media (max-width:600px){
  body{background:#eef3f8;overflow-x:hidden}
  .app{max-width:540px;min-height:100vh;padding-bottom:58px}
  .top{padding:7px 12px 6px}.brand{font-size:17px;line-height:1.05}.sub{font-size:8px;margin-top:2px}.pill{padding:4px 7px;margin-top:4px;font-size:9px}
  .grid{padding:6px;gap:5px}.card{border-radius:11px;padding:7px}.label{font-size:8px}.value{font-size:16px;margin-top:1px;line-height:1.05}
  .section{padding:1px 7px}.section h2{font-size:12px;margin:5px 2px 4px}
  .cues{gap:5px}.cue{padding:6px;border-radius:9px}.cue b{margin-top:2px;font-size:11px}
  .verdict{padding:8px;border-radius:12px}.big{font-size:25px;line-height:1}.score{margin:5px 0;height:5px}.rows{gap:5px}.row{padding:6px;border-radius:8px}.row b{font-size:12px}
  .one-screen-details{margin-top:5px!important;display:block!important}
  .os-grid{gap:4px}.os-chip{padding:5px 3px;border-radius:7px;font-size:8px;line-height:1.05}.os-chip b{font-size:10px;margin-top:1px}
  .os-plan{gap:4px;margin-top:5px}.os-plan div{padding:5px;border-radius:7px}.os-plan span{font-size:7px}.os-plan b{font-size:11px}
  .os-reason{margin-top:5px;padding:5px 7px;border-radius:7px;font-size:8px;line-height:1.2}
  /* Main cockpit contains only decision-critical information. */
  .verdict>.status,.verdict>.age,.verdict>.button{display:none!important}
  /* Secondary long-form sections stay available in the source but are hidden from the dashboard viewport. */
  .app>.section:nth-of-type(n+4){display:none!important}
  .nav{height:52px}.nav b{font-size:14px}.nav span{font-size:7px}
}
'''

if 'SNIPER TRUE ONE-SCREEN COCKPIT' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

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

# Keep the generated HTML clean so validation does not fail on whitespace-only changes.
s = '\n'.join(line.rstrip() for line in s.splitlines()) + '\n'
p.write_text(s, encoding='utf-8')
print('true one-screen cockpit patch applied')
