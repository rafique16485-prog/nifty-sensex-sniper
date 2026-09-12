from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
if 'id="swingScannerPanel"' not in s:
    panel='''<section class="section" id="swingScannerPanel"><h2>📈 Swing Scanner</h2><div class="verdict"><div class="big" id="swingState">WAIT</div><div class="os-reason" id="swingReason">🛡️ Scanning NIFTY 500 for confirmed setups.</div><div id="swingList"></div></div></section>'''
    s=s.replace('</main>',panel+'\n</main>',1)
script='''<script>\n(function(){\nasync function loadSwing(){const box=document.getElementById('swingList'),state=document.getElementById('swingState'),reason=document.getElementById('swingReason');if(!box||!state||!reason)return;try{const r=await fetch('/api/swing?ts='+Date.now(),{cache:'no-store'});const d=await r.json();state.textContent=d.ok?'SWING SCANNER':'NO TRADE';reason.textContent=d.ok?(d.candidates?.[0]?.reason||'Waiting for confirmed setup.'):'🛡️ Swing engine unavailable.';box.innerHTML=(d.candidates||[]).map(x=>`<div class="mini"><span><b>${x.symbol||'—'}</b><br>${x.setup||''}</span><span><b>${x.action||'WAIT'}</b><br>${x.score||0}/10</span></div>`).join('')}catch(e){state.textContent='NO TRADE';reason.textContent='🛡️ Swing confirmation unavailable.'}}\nwindow.loadSwing=loadSwing;loadSwing();setInterval(loadSwing,60000);\n})();\n</script>'''
    if 'function loadSwing()' not in s:s=s.replace('</body>',script+'</body>',1)
p.write_text(s,encoding='utf-8')
