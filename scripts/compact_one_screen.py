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
  .more-details{display:block;width:100%;margin-top:5px;padding:7px 9px;border:1px solid #315a87;border-radius:8px;background:#fff;color:#0b2a52;font-weight:900;font-size:9px;text-align:center;cursor:pointer;touch-action:manipulation}
  .app>.section:nth-of-type(n+4){display:none!important}
  .app.details-open>.section:nth-of-type(n+4){display:block!important}
  .verdict>.status,.verdict>.age,.verdict>.button{display:none!important}
  .nav{height:52px}.nav b{font-size:14px}.nav span{font-size:7px}
}
'''

if 'SNIPER TRUE ONE-SCREEN COCKPIT' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

needle = '<div class="status" id="status">'
button = '<button class="more-details" id="moreDetailsBtn" type="button">▾ MORE DETAILS</button>'
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
''' + button + '\n</div>'
    s = s.replace(needle, insert + '\n' + needle, 1)
elif 'id="moreDetailsBtn"' not in s:
    marker = '<div class="os-reason" id="osReason">🛡️ Waiting for live confirmation.</div>'
    s = s.replace(marker, marker + '\n' + button, 1)

# Always ensure the mobile reveal rule exists AFTER the mobile hide rule.
reveal_marker = '/* MORE DETAILS REVEAL FIX */'
reveal_css = '''
/* MORE DETAILS REVEAL FIX */
@media (max-width:600px){
  .app.details-open > .section:nth-of-type(n+4){display:block!important}
}
'''
if reveal_marker not in s:
    s = s.replace('</style>', reveal_css + '\n</style>', 1)

# Always ensure the click handler exists. Older versions could already contain
# loadOneScreen(), which prevented the previous idempotent block from adding it.
handler_marker = '/* MORE DETAILS CLICK FIX */'
handler = r'''<script>
/* MORE DETAILS CLICK FIX */
(function(){
  function wireMoreDetails(){
    const app=document.querySelector('.app');
    const btn=document.getElementById('moreDetailsBtn');
    if(!app||!btn||btn.dataset.wired==='1')return;
    btn.dataset.wired='1';
    btn.addEventListener('click',function(ev){
      ev.preventDefault();
      const open=app.classList.toggle('details-open');
      btn.textContent=open?'▴ LESS DETAILS':'▾ MORE DETAILS';
      if(open){
        const first=app.querySelector('.section:nth-of-type(4)');
        if(first) first.scrollIntoView({behavior:'smooth',block:'start'});
      }
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wireMoreDetails);
  else wireMoreDetails();
  setTimeout(wireMoreDetails,500);
})();
</script>
'''
if handler_marker not in s:
    s = s.replace('</body>', handler + '</body>', 1)

s = '\n'.join(line.rstrip() for line in s.splitlines()) + '\n'
p.write_text(s, encoding='utf-8')
print('More Details click + reveal fix applied')
