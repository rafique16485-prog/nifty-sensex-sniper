const feeds=[
  ['NIFTY / SENSEX','https://news.google.com/rss/search?q=NIFTY+SENSEX+India+stock+market&hl=en-IN&gl=IN&ceid=IN:en'],
  ['RBI / Economy','https://news.google.com/rss/search?q=RBI+India+inflation+economy&hl=en-IN&gl=IN&ceid=IN:en'],
  ['Global / Fed','https://news.google.com/rss/search?q=Federal+Reserve+oil+markets+India&hl=en-IN&gl=IN&ceid=IN:en']
];
function clean(s=''){return s.replace(/<[^>]*>/g,' ').replace(/&amp;/g,'&').replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/\s+/g,' ').trim()}
function parse(xml,category){return [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)].slice(0,5).map(m=>{const x=m[1],pick=t=>{const z=x.match(new RegExp(`<${t}>([\\s\\S]*?)<\\/${t}>`));return z?clean(z[1]):''};return{category,title:pick('title'),link:pick('link'),published:pick('pubDate')}}).filter(x=>x.title)}
module.exports=async(req,res)=>{res.setHeader('Content-Type','application/json');res.setHeader('Cache-Control','no-store');try{const out=[];for(const [category,url] of feeds){const r=await fetch(url,{cache:'no-store',headers:{'User-Agent':'NIFTY-Sensex-Sniper/1.0'}});if(r.ok)out.push(...parse(await r.text(),category))}out.sort((a,b)=>new Date(b.published)-new Date(a.published));res.status(200).end(JSON.stringify({ok:true,generated_at:new Date().toISOString(),sentiment:'CONTEXT ONLY',items:out.slice(0,12),disclaimer:'News is contextual information. It is not a standalone CALL/PUT trigger or financial advice.'}))}catch(e){res.status(500).end(JSON.stringify({ok:false,error:e.message}))}};
