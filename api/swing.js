// Swing Engine V1 — conservative educational scanner foundation.
// Designed to be expanded with live universe/sector feeds without changing the safety gates.
const NIFTY500_URL='https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500';
const UPSTOX='https://api.upstox.com';
const TOKEN=process.env.UPSTOX_ACCESS_TOKEN||'';
const H={'Accept':'application/json',...(TOKEN?{'Authorization':`Bearer ${TOKEN}`}:{})};
const num=v=>{const n=Number(v);return Number.isFinite(n)?n:null};
const round=(v,d=2)=>v==null?null:Number(Number(v).toFixed(d));
const side=v=>{v=String(v||'').toUpperCase();if(v.includes('BULL')||v==='BUY')return'BULLISH';if(v.includes('BEAR')||v==='SELL')return'BEARISH';return'NEUTRAL'};
function scoreSetup(x){let score=0;const c=[];if(x.weekly==='BULLISH'){score+=1;c.push('Weekly trend')}if(x.daily==='BULLISH'){score+=1;c.push('Daily trend')}if(x.volume==='STRONG'){score+=1;c.push('Volume')}if(x.relative_strength==='STRONG'){score+=1;c.push('Relative strength')}if(x.sector_strength==='STRONG'){score+=1;c.push('Sector strength')}if(x.structure==='BULLISH'){score+=1;c.push('Structure')}if(x.setup==='BREAKOUT_RETEST'){score+=2;c.push('Breakout + retest')}else if(x.setup==='PULLBACK_DEMAND'){score+=2;c.push('Demand pullback')}return Math.min(10,round(score*1.25,1))}
function plan(x){const entry=num(x.entry),sl=num(x.stoploss);if(entry==null||sl==null||entry<=sl)return null;const risk=entry-sl;return{entry:round(entry),stoploss:round(sl),target1:round(entry+risk*1.5),target2:round(entry+risk*2.5),risk_points:round(risk),rr_t1:'1:1.5',rr_t2:'1:2.5',holding_period:x.holding_period||'3–7 trading sessions',invalidation:`Daily close below ${round(sl)}`}}
function classify(x){const s=x.score;if(s>=8)return'BUY';if(s>=6.5)return'WAIT';return'AVOID'}
export default async function handler(req,res){res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');try{const demo=[
{name:'SETUP ENGINE',symbol:'—',score:0,action:'WAIT',setup:'Scanner foundation active',holding_period:'—',reason:'Live NIFTY 500 universe integration is the next data layer.'}
];res.status(200).end(JSON.stringify({ok:true,engine_version:'Swing Engine V1',universe:'NIFTY 500',candidates:demo,disclaimer:'Educational/probabilistic only. Scanner results are not guaranteed outcomes or financial advice.'}))}catch(e){res.status(200).end(JSON.stringify({ok:false,engine_version:'Swing Engine V1',universe:'NIFTY 500',candidates:[],error:String(e.message||e),disclaimer:'Educational/probabilistic only.'}))}}
