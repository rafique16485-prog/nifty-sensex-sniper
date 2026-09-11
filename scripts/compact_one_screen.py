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

# Professional mobile cockpit layer: overrides the older visual layer without touching API logic.
pro_marker = '/* SNIPER PRO MOBILE COCKPIT V1 */'
pro_css = r'''
/* SNIPER PRO MOBILE COCKPIT V1 */
@media (max-width:600px){
  html,body{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;color:#10213b;-webkit-font-smoothing:antialiased}
  body{background:#eef3f8!important}
  .app{background:#f7f9fc!important;max-width:540px!important}
  .top{background:#071b3a!important;color:#fff!important;padding:10px 12px 9px!important;border-radius:0 0 14px 14px;box-shadow:0 3px 14px rgba(7,27,58,.16)!important}
  .brand{font-family:Inter,system-ui,sans-serif!important;font-size:17px!important;font-weight:900!important;letter-spacing:-.25px}
  .sub{color:#b9c9dc!important;font-size:8px!important}
  .pill{background:#12345e!important;border:1px solid rgba(255,255,255,.12);font-size:8px!important;padding:4px 7px!important}
  .pill.live{background:#073e31!important;color:#5ff0ba!important}
  .grid{padding:7px 7px 4px!important;gap:6px!important}
  .card{border:1px solid #d8e2ed!important;border-radius:11px!important;padding:8px!important;box-shadow:0 3px 10px rgba(16,33,59,.05)!important}
  .label{font-size:8px!important;color:#728198!important;letter-spacing:.25px}
  .value{font-size:17px!important;font-weight:900!important;color:#10213b!important}
  .section{padding:2px 7px!important}
  .section h2{font-family:Inter,system-ui,sans-serif!important;font-size:12px!important;font-weight:850!important;color:#10213b!important;letter-spacing:-.1px}
  .cue{background:#fff!important;border:1px solid #dce5ef!important;border-radius:9px!important;padding:6px 7px!important;box-shadow:0 2px 8px rgba(16,33,59,.035)}
  .cue b{font-size:10px!important;color:#10213b}
  .verdict{background:#fff!important;border:1px solid #cbdbea!important;border-left:4px solid #0b2a52!important;border-radius:12px!important;padding:9px!important;box-shadow:0 4px 14px rgba(16,33,59,.07)!important}
  .verdict .big{font-size:25px!important;font-weight:950!important;letter-spacing:-.4px}
  .verdict .score{height:6px!important;background:#e4ebf2!important;border-radius:8px!important}
  .verdict .rows{grid-template-columns:1fr 1fr!important;gap:5px!important}
  .verdict .row{background:#f7f9fc!important;border:1px solid #e1e8ef!important;border-radius:8px!important;padding:6px!important}
  .verdict .row b{font-size:11px!important}
  .one-screen-details{margin-top:5px!important}
  .os-chip{background:#f6f9fc!important;border:1px solid #dbe4ed!important;border-radius:7px!important;padding:5px 3px!important}
  .os-chip span,.os-plan span{color:#7a899b!important;font-size:7px!important;font-weight:800;letter-spacing:.25px}
  .os-chip b,.os-plan b{color:#10213b!important;font-size:10px!important;font-weight:900!important}
  .os-plan div{background:#fff!important;border:1px solid #dbe4ed!important;border-radius:7px!important;padding:5px!important}
  .os-reason{background:#f7f9fc!important;border:1px solid #dbe4ed!important;border-left:3px solid #bd8610!important;border-radius:7px!important;color:#40536b!important}
  .more-details{background:#071b3a!important;color:#fff!important;border-color:#071b3a!important;border-radius:8px!important;font-size:9px!important;padding:7px!important;box-shadow:0 2px 7px rgba(7,27,58,.18)}
  .more-details:active{transform:scale(.99)}
  .nav{height:52px!important;background:rgba(255,255,255,.98)!important;border-top:1px solid #dbe4ed!important;box-shadow:0 -4px 16px rgba(16,33,59,.08)!important}
  .nav b{color:#0b2a52!important;font-size:14px!important}.nav span{font-size:7px!important;color:#73839a!important}.nav .active span,.nav .active b{color:#087dca!important}
}
'''
if pro_marker not in s:
    s = s.replace('</style>', pro_css + '\n</style>', 1)

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

# Always ensure the click handler exists.
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
print('Professional mobile cockpit layer applied')
