from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'function refreshAll' not in s:
    s = subprocess.check_output(
        ['git', 'show', '2ddf2fa4186f6d27ce76d3cb2d508c639fa582ac:index.html'],
        text=True,
        encoding='utf-8'
    )

s = s.replace(
    ('One directional signal is not enough to claim agreement. ' * 3).strip(),
    'One directional signal is not enough to claim agreement.'
)
s = s.replace(
    'One directional signal is not enough to claim agreement. One directional signal is not enough to claim agreement.',
    'One directional signal is not enough to claim agreement.'
)

match = re.search(r'<section class="section"(?: id="sniperPlanV1Panel")?><h2>🎯 Sniper Trade Plan V1</h2>', s)
if match:
    start = match.start()
    end = s.find('<section class="section">', match.end())
    if end < 0:
        end = s.find('</main>', match.end())
    if end > start:
        section = '''<section class="section"><h2>🎯 Sniper Trade Plan V2</h2><div class="verdict"><div class="label">MULTI-GATE EXECUTION PLAN</div><div class="big yellow" id="planDecision">NO TRADE</div><div class="label" id="planReason">Waiting for confirmation</div><div class="rows"><div class="row"><span class="label">Confidence</span><b id="planConfidence">— / 10</b></div><div class="row"><span class="label">Agreement</span><b id="planAgreement">INSUFFICIENT</b></div></div><div class="why-grid" id="planGates"><div class="why-item"><span class="label">System</span><b>Waiting…</b></div></div><div class="rows" style="margin-top:10px"><div class="row"><span class="label">Entry</span><b id="planEntry">—</b></div><div class="row"><span class="label">Stop Loss</span><b id="planStop">—</b></div><div class="row"><span class="label">Target 1</span><b id="planTarget1">—</b></div><div class="row"><span class="label">Target 2</span><b id="planTarget2">—</b></div></div><div class="tip waitbox" id="planGateReason"><b>WAIT:</b> Live plan gates will populate here.</div><div class="age" id="planUpdated">Plan V2: waiting</div></div><div class="tip">ELI5: PASS = confirmed, WAIT = missing confirmation, BLOCK = hard stop. Every critical gate must confirm before an entry is shown.</div></section>'''
        s = s[:start] + section + s[end:]

for fn in ('loadPlanV1', 'loadPlan'):
    while True:
        pos = s.find('function ' + fn)
        if pos < 0:
            break
        script_start = s.rfind('<script', 0, pos)
        script_end = s.find('</script>', pos)
        if script_start >= 0 and script_end >= 0:
            s = s[:script_start] + s[script_end + len('</script>'):]
        else:
            break

if 'async function loadPlanV2()' not in s:
    loader = r'''<script>
async function loadPlanV2(){
 const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
 const esc=v=>String(v==null?'—':v).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));
 try{
  const r=await fetch('/api/plan?ts='+Date.now(),{cache:'no-store'}); const d=await r.json();
  if(!d.ok) throw Error(d.reason||'Plan unavailable');
  set('planDecision',d.decision||'NO TRADE'); set('planConfidence',(d.confidence??'—')+' / 10');
  set('planAgreement',d.agreement==null?'INSUFFICIENT':d.agreement+'%'); set('planReason',d.reason||'NO TRADE');
  set('planEntry',d.plan?.entry??'—'); set('planStop',d.plan?.stoploss??'—'); set('planTarget1',d.plan?.target1??'—'); set('planTarget2',d.plan?.target2??'—');
  const names={market_open:'Market Open',freshness:'Fresh Data',index_alignment:'NIFTY + SENSEX',structure:'BOS / CHoCH',liquidity:'Liquidity',smc_retest:'Retest',orderflow:'Options Flow',forecast:'Forecast',news_risk:'News Risk'};
  const html=Object.entries(d.gates||{}).map(([k,g])=>'<div class="why-item '+(g.status==='PASS'?'okbox':g.status==='BLOCK'?'dangerbox':'waitbox')+'"><span class="label">'+esc(names[k]||k)+'</span><b>'+esc(g.status)+'</b><span class="label">'+esc(g.reason)+'</span></div>').join('');
  const box=document.getElementById('planGates'); if(box) box.innerHTML=html||'<div class="why-item"><b>Waiting…</b></div>';
  const waiting=(d.gates_summary?.waiting||[]).length, blocked=(d.gates_summary?.blocked||[]).length;
  set('planGateReason',blocked?'BLOCK: '+d.gates_summary.blocked.join(', '):waiting?'WAIT: '+d.gates_summary.waiting.join(', '):'PASS: all critical gates confirmed.');
  set('planUpdated','Updated '+new Date().toLocaleTimeString()+' • Sniper Plan V2');
 }catch(e){set('planDecision','NO TRADE');set('planReason','Plan engine unavailable — conservative fallback.');set('planUpdated','Plan V2: unavailable')}
}
loadPlanV2(); setInterval(loadPlanV2,30000);
</script>'''
    s = s.replace('</body>', loader + '</body>')

p.write_text(s, encoding='utf-8')
