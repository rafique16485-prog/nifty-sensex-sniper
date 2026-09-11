const LIVE='/api/live?action=engine';
const FORECAST='/api/forecast';
const NEWS='/api/news-intel';
function side(v){v=String(v==null?'':v).toUpperCase();return v.includes('BULL')||v==='CALL'||v==='CE'?'BULL':v.includes('BEAR')||v==='PUT'||v==='PE'?'BEAR':'NEUTRAL'}
function num(v){const n=Number(v);return Number.isFinite(n)?n:null}
function round(v,d=2){const p=10**d;return Math.round(v*p)/p}
function first(...v){return v.find(x=>x!==undefined&&x!==null&&x!=='')}
function bool(v){return v===true||v===1||String(v||'').toUpperCase()==='YES'||String(v||'').toUpperCase()==='TRUE'||String(v||'').toUpperCase()==='PASS'}
function atr(bars){const b=Array.isArray(bars)?bars.slice(-15):[];if(b.length<2)return null;let s=0,n=0;for(let i=1;i<b.length;i++){const x=b[i],p=b[i-1];const h=num(x.high),l=num(x.low),pc=num(p.close);if(h!=null&&l!=null&&pc!=null){s+=Math.max(h-l,Math.abs(h-pc),Math.abs(l-pc));n++}}return n?s/n:null}
function ageSeconds(ts){if(!ts)return Infinity;const t=new Date(ts).getTime();return Number.isFinite(t)?Math.max(0,(Date.now()-t)/1000):Infinity}
function smcSide(s){return side(first(s?.bias,s?.side,s?.direction,s?.market_bias,s?.trend))}
function optionsSide(l){return side(first(l?.options?.side,l?.options?.bias,l?.options?.direction,l?.option_side,l?.option_bias,l?.optionFactor,l?.option_factor,l?.option_flow?.side,l?.option_flow?.bias))}
function technicalSide(l){return side(first(l?.verdict,l?.bias,l?.direction,l?.side,l?.market_bias))}
function gate(status,reason){return{status,reason}}
async function getJson(base,req){const u=new URL(base,`https://${req.headers.host}`);u.searchParams.set('ts',Date.now());const r=await fetch(u,{headers:{Accept:'application/json'},cache:'no-store'});if(!r.ok)throw Error(`${base} HTTP ${r.status}`);return r.json()}
export default async function handler(req,res){res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');try{
const [live,forecast,news]=await Promise.all([getJson(LIVE,req),getJson(FORECAST,req),getJson(NEWS,req)]);
const n=live?.nifty||live?.NIFTY||{};const s=live?.sensex||live?.SENSEX||{};const last=num(first(n.last,n.last_price,n.price));const bars=Array.isArray(n.bars)?n.bars:[];const a=atr(bars);
const marketOpen=!!live.market_open;const freshAge=ageSeconds(live.data_timestamp);const fresh=freshAge<=300;
const tech=technicalSide(live);const nf=side(forecast?.nifty?.bias),sf=side(forecast?.sensex?.bias);const fc=nf===sf&&nf!=='NEUTRAL'?nf:'NEUTRAL';const ns=side(news?.side);const newsRisk=String(news?.risk||'UNKNOWN').toUpperCase();
const smcN=live?.smc?.nifty||live?.nifty?.smc||live?.smc||{};const smcS=live?.smc?.sensex||live?.sensex?.smc||{};
const smc=smcN||{};const smcDir=smcSide(smc);const retest=bool(first(smc.retest,smc.retest_confirmed));const retestLevel=num(first(smc.retest_level,smc.retestPrice,smc.trigger_level));
const bos=bool(first(smc.bos,smc.BOS,smc.bos_confirmed));const choch=bool(first(smc.choch,smc.CHoCH,smc.choch_confirmed));const sweep=bool(first(smc.liquidity_sweep,smc.sweep,smc.sweep_confirmed));const fvg=bool(first(smc.fvg,smc.FVG,smc.fvg_confirmed));const ob=bool(first(smc.order_block,smc.ob,smc.order_block_confirmed));
const liquidityEvent=first(live?.liquidity?.event,live?.liquidity?.status,live?.liquidity_event,live?.liquidityFactor,live?.liquidity_factor);const liquidityPass=!!liquidityEvent&&String(liquidityEvent).toUpperCase()!=='WAIT'&&String(liquidityEvent).toUpperCase()!=='NONE'&&String(liquidityEvent).toUpperCase()!=='—';
const opt=optionsSide(live);const optionsPass=opt!=='NEUTRAL';
const alignedNiftySensex=side(first(live?.nifty?.bias,live?.nifty_bias,live?.nifty_direction,live?.nifty_side))===side(first(live?.sensex?.bias,live?.sensex_bias,live?.sensex_direction,live?.sensex_side))&&side(first(live?.nifty?.bias,live?.nifty_bias,live?.nifty_direction,live?.nifty_side))!=='NEUTRAL';
const structurePass=bos||choch||smcDir!=='NEUTRAL';
const technicalDirectional=tech!=='NEUTRAL';
const forecastPass=fc==='NEUTRAL'||fc===tech;
const newsBlock=ns==='BEAR'&&newsRisk==='HIGH';
const gates={
market_open:gate(marketOpen?'PASS':'BLOCK',marketOpen?'Market is open.':'Market is closed.'),
freshness:gate(fresh?'PASS':'BLOCK',fresh?`Exchange snapshot ${round(freshAge,0)}s old.`:'Exchange snapshot is stale or missing.'),
index_alignment:gate(alignedNiftySensex?'PASS':'WAIT',alignedNiftySensex?'NIFTY and SENSEX directional bias aligned.':'NIFTY/SENSEX directional alignment is not confirmed.'),
structure:gate(structurePass?'PASS':'WAIT',structurePass?'BOS/CHoCH/SMC direction provides structure confirmation.':'BOS/CHoCH/SMC structure confirmation is missing.'),
liquidity:gate(liquidityPass?'PASS':'WAIT',liquidityPass?`Liquidity event: ${liquidityEvent}.`:'No confirmed liquidity sweep/event.'),
smc_retest:gate(retest?'PASS':'WAIT',retest?'Retest confirmed.':'Retest confirmation is missing — wait.'),
orderflow:gate(optionsPass?'PASS':'WAIT',optionsPass?`Options flow: ${opt}.`:'Options flow is neutral/unconfirmed.'),
forecast:gate(forecastPass?'PASS':'WAIT',forecastPass?(fc==='NEUTRAL'?'Forecast neutral; not used as directional trigger.':`Forecast agrees with ${tech}.`):`Forecast ${fc} conflicts with technical ${tech}.`),
news_risk:gate(newsBlock?'BLOCK':'PASS',newsBlock?'High-risk bearish news blocks the trade.':`News ${ns} • Risk ${newsRisk}.`)
};
const bull=[tech,fc,ns,smcDir,opt].filter(x=>x==='BULL').length;const bear=[tech,fc,ns,smcDir,opt].filter(x=>x==='BEAR').length;
let direction=bull>=3&&bull>bear?'CALL':bear>=3&&bear>bull?'PUT':'NO TRADE';
const hardBlocks=Object.values(gates).filter(g=>g.status==='BLOCK').length;
const coreWaits=['index_alignment','structure','liquidity','smc_retest','orderflow'].filter(k=>gates[k].status!=='PASS').length;
let decision=direction;if(hardBlocks||coreWaits>0||newsBlock||!technicalDirectional||!fresh||!marketOpen)decision='NO TRADE';
let confidence=Math.min(decision==='NO TRADE'?6.5:9.5,5+Math.max(bull,bear)*1.2-Math.min(bull,bear)*0.8+(coreWaits===0?1:0));
let entry=null,stop=null,target1=null,target2=null,riskPoints=null;const level=retestLevel;
if(decision!=='NO TRADE'&&last!=null){entry=last;const buffer=Math.max(a?0.35*a:0.002*last,2);if(decision==='CALL'){stop=level!=null&&level<entry?level-buffer:entry-buffer;riskPoints=entry-stop;target1=entry+1.5*riskPoints;target2=entry+2*riskPoints}else{stop=level!=null&&level>entry?level+buffer:entry+buffer;riskPoints=stop-entry;target1=entry-1.5*riskPoints;target2=entry-2*riskPoints}}
const passed=Object.entries(gates).filter(([,g])=>g.status==='PASS').map(([k])=>k);const waiting=Object.entries(gates).filter(([,g])=>g.status==='WAIT').map(([k])=>k);const blocked=Object.entries(gates).filter(([,g])=>g.status==='BLOCK').map(([k])=>k);
let reason;if(decision==='CALL')reason='CALL setup: all critical gates passed.';else if(decision==='PUT')reason='PUT setup: all critical gates passed.';else if(blocked.length)reason=`NO TRADE — blocked by ${blocked.join(', ')}.`;else if(waiting.length)reason=`NO TRADE — waiting for ${waiting.join(', ')}.`;else reason='NO TRADE — directional confirmation insufficient.';
res.status(200).end(JSON.stringify({ok:true,engine_version:'Sniper Plan V2',decision,confidence:round(confidence,1),agreement:(bull+bear)>=2?Math.round(Math.max(bull,bear)/(bull+bear)*100):null,signals:{technical:tech,forecast:fc,news:ns,news_risk:newsRisk,smc:smcDir,options:opt},gates,gates_summary:{passed,waiting,blocked},instrument:'NIFTY',price:last,atr:a,plan:{entry:entry==null?null:round(entry),stoploss:stop==null?null:round(stop),target1:target1==null?null:round(target1),target2:target2==null?null:round(target2),risk_points:riskPoints==null?null:round(riskPoints)},reason,gate:reason,disclaimer:'Educational/probabilistic only. Entry, stop and targets are heuristic levels, not guaranteed outcomes or financial advice.'}))
}catch(e){res.status(200).end(JSON.stringify({ok:false,engine_version:'Sniper Plan V2',decision:'NO TRADE',confidence:5,reason:'NO TRADE — Plan engine unavailable; conservative fallback.',gate:'NO TRADE — Plan engine unavailable; conservative fallback.',error:String(e.message||e),disclaimer:'Educational/probabilistic only.'}))}}
