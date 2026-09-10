const UPSTOX_V2 = 'https://api.upstox.com/v2';
const UPSTOX_V3 = 'https://api.upstox.com/v3';

const IDS = {
  NIFTY: process.env.UPSTOX_NIFTY_KEY || 'NSE_INDEX|Nifty 50',
  SENSEX: process.env.UPSTOX_SENSEX_KEY || 'BSE_INDEX|SENSEX',
  VIX: process.env.UPSTOX_VIX_KEY || 'NSE_INDEX|India VIX',
  RELIANCE: process.env.UPSTOX_RELIANCE_KEY || 'NSE_EQ|INE002A01018',
  HDFCBANK: process.env.UPSTOX_HDFCBANK_KEY || 'NSE_EQ|INE040A01034',
  ICICIBANK: process.env.UPSTOX_ICICIBANK_KEY || 'NSE_EQ|INE090A01021',
};

function json(res, status, body) {
  res.status(status).setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store');
  return res.end(JSON.stringify(body));
}

function authHeaders() {
  const token = process.env.UPSTOX_ACCESS_TOKEN;
  if (!token) throw new Error('Upstox access token is not configured on Vercel.');
  return { Accept: 'application/json', Authorization: `Bearer ${token}` };
}

async function upstox(base, path, params = {}) {
  const url = new URL(`${base}${path}`);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, String(v));
  });
  const r = await fetch(url, { headers: authHeaders(), cache: 'no-store' });
  const data = await r.json().catch(() => ({}));
  if (!r.ok || data.status === 'error') {
    const msg = data?.errors?.[0]?.message || data?.message || `Upstox HTTP ${r.status}`;
    throw new Error(msg);
  }
  return data;
}

function pickQuote(data, key) {
  const d = data?.data || {};
  return d[key] || d[key.replace('|', ':')] || Object.entries(d).find(([k]) => k.replace(':', '|') === key)?.[1] || null;
}

async function market() {
  const keys = [IDS.NIFTY, IDS.SENSEX, IDS.VIX].join(',');
  const data = await upstox(UPSTOX_V2, '/market-quote/ltp', { instrument_key: keys });
  return {
    nifty: pickQuote(data, IDS.NIFTY),
    sensex: pickQuote(data, IDS.SENSEX),
    vix: pickQuote(data, IDS.VIX),
    provider: 'Upstox',
    updatedAt: new Date().toISOString(),
  };
}

function normalizeStockQuote(q, key, name) {
  if (!q) return { name, instrument_key: key, available: false };
  const last = Number(q.last_price);
  const prev = q.cp == null ? null : Number(q.cp);
  const change = prev != null && Number.isFinite(last) ? last - prev : null;
  const changePct = prev ? (change / prev) * 100 : null;
  return {
    name,
    instrument_key: key,
    last_price: Number.isFinite(last) ? last : null,
    prev_close: prev,
    change: change != null && Number.isFinite(change) ? change : null,
    change_pct: changePct != null && Number.isFinite(changePct) ? changePct : null,
    volume: q.volume == null ? null : Number(q.volume),
    available: true,
  };
}

async function leaders() {
  const keys = [IDS.RELIANCE, IDS.HDFCBANK, IDS.ICICIBANK].join(',');
  const raw = await upstox(UPSTOX_V3, '/market-quote/ltp', { instrument_key: keys });
  return {
    reliance: normalizeStockQuote(pickQuote(raw, IDS.RELIANCE), IDS.RELIANCE, 'Reliance'),
    hdfcBank: normalizeStockQuote(pickQuote(raw, IDS.HDFCBANK), IDS.HDFCBANK, 'HDFC Bank'),
    iciciBank: normalizeStockQuote(pickQuote(raw, IDS.ICICIBANK), IDS.ICICIBANK, 'ICICI Bank'),
    updatedAt: new Date().toISOString(),
  };
}

function normalizeCandleRows(raw) {
  const candles = raw?.data?.candles || [];
  return candles.map(x => ({ ts: x[0], open: Number(x[1]), high: Number(x[2]), low: Number(x[3]), close: Number(x[4]), volume: Number(x[5] || 0) })).sort((a,b) => String(a.ts).localeCompare(String(b.ts)));
}

async function candles(underlying) {
  const key = IDS[underlying];
  if (!key) throw new Error('Unknown underlying');
  const raw = await upstox(UPSTOX_V3, `/historical-candle/intraday/${encodeURIComponent(key)}/minutes/5`);
  const bars = normalizeCandleRows(raw).slice(-78);
  let pv = 0, vol = 0;
  bars.forEach(b => { const tp = (b.high + b.low + b.close) / 3; pv += tp * (b.volume || 0); vol += b.volume || 0; });
  return { bars, vwap: vol ? pv / vol : null };
}

async function optionContracts(underlying, expiry = 'current_week') {
  const key = IDS[underlying];
  if (!key) throw new Error('Unknown underlying');
  // Fetch active contracts first, then select the nearest future expiry.
  const raw = await upstox(UPSTOX_V2, '/option/contract', { instrument_key: key });
  const contracts = Array.isArray(raw?.data) ? raw.data : [];
  const dates = [...new Set(contracts.map(x => x.expiry).filter(Boolean))].sort();
  const today = new Date().toISOString().slice(0, 10);
  const futureDates = dates.filter(d => d >= today);
  const selected = futureDates[0] || dates[0] || null;
  return { contracts, expiry: selected, expiryDates: dates };
}

function summarizeChain(raw, requestedExpiry) {
  const rows = Array.isArray(raw?.data) ? raw.data.map(x => ({
    strike: Number(x.strike_price),
    call: x.call_options ? { ltp: x.call_options.market_data?.ltp, oi: x.call_options.market_data?.oi, prevOi: x.call_options.market_data?.prev_oi, volume: x.call_options.market_data?.volume, iv: x.call_options.option_greeks?.iv } : null,
    put: x.put_options ? { ltp: x.put_options.market_data?.ltp, oi: x.put_options.market_data?.oi, prevOi: x.put_options.market_data?.prev_oi, volume: x.put_options.market_data?.volume, iv: x.put_options.option_greeks?.iv } : null,
    spot: Number(x.underlying_spot_price || 0),
    pcrAtStrike: x.pcr,
  })).sort((a,b) => a.strike-b.strike) : [];
  const spot = Number(rows.find(r => r.spot > 0)?.spot || 0);
  const atm = rows.reduce((best, r) => !best || Math.abs(r.strike - spot) < Math.abs(best.strike - spot) ? r : best, null);
  const callOI = rows.reduce((s,r) => s + Number(r.call?.oi || 0), 0);
  const putOI = rows.reduce((s,r) => s + Number(r.put?.oi || 0), 0);
  const idx = atm ? rows.findIndex(r => r.strike === atm.strike) : -1;
  return { expiry: requestedExpiry, spot, atm, pcr: callOI ? putOI / callOI : null, rows: idx >= 0 ? rows.slice(Math.max(0,idx-6),idx+7) : rows.slice(0,13) };
}

async function optionchain(underlying, requested) {
  const contractInfo = await optionContracts(underlying, requested || 'current_week');
  const expiry = contractInfo.expiry || requested || 'current_week';
  const raw = await upstox(UPSTOX_V2, '/option/chain', { instrument_key: IDS[underlying], expiry_date: expiry });
  const summary = summarizeChain(raw, expiry);
  if (!summary.rows.length) throw new Error(`Upstox returned no option-chain rows for ${underlying} ${expiry}.`);
  return { underlying, ...summary, expiryDates: contractInfo.expiryDates };
}

export default async function handler(req, res) {
  if (req.method !== 'GET') return json(res, 405, { error: 'GET only' });
  const action = req.query?.action || 'status';
  try {
    if (!process.env.UPSTOX_ACCESS_TOKEN) return json(res, 200, { live: false, provider: 'Upstox', error: 'Upstox access token is not configured yet.' });
    if (action === 'market') return json(res, 200, { live: true, ...(await market()) });
    if (action === 'leaders') return json(res, 200, { live: true, provider: 'Upstox', ...(await leaders()) });
    if (action === 'expiry') {
      const [nifty, sensex] = await Promise.all([optionContracts('NIFTY'), optionContracts('SENSEX')]);
      return json(res, 200, { live: true, provider: 'Upstox', nifty: nifty.expiryDates, sensex: sensex.expiryDates });
    }
    if (action === 'chain') {
      const underlying = String(req.query?.underlying || 'NIFTY').toUpperCase();
      return json(res, 200, { live: true, provider: 'Upstox', ...(await optionchain(underlying, req.query?.expiry)) });
    }
    if (action === 'candles') {
      const underlying = String(req.query?.underlying || 'NIFTY').toUpperCase();
      return json(res, 200, { live: true, provider: 'Upstox', underlying, ...(await candles(underlying)) });
    }
    return json(res, 200, { live: true, provider: 'Upstox', actions: ['market','leaders','expiry','chain','candles'] });
  } catch (e) {
    return json(res, 502, { live: false, provider: 'Upstox', error: e.message });
  }
}
