const DHAN_BASE = 'https://api.dhan.co/v2';

function json(res, status, body) {
  res.status(status).setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store');
  return res.end(JSON.stringify(body));
}

async function dhan(path, payload) {
  const token = process.env.DHAN_ACCESS_TOKEN;
  const clientId = process.env.DHAN_CLIENT_ID;
  if (!token || !clientId) throw new Error('Dhan credentials are not configured on Vercel.');
  const r = await fetch(`${DHAN_BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      'access-token': token,
      'client-id': clientId,
    },
    body: JSON.stringify(payload),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.errorMessage || data.message || `Dhan HTTP ${r.status}`);
  return data;
}

const IDS = {
  NIFTY: process.env.NIFTY_SECURITY_ID || '13',
  SENSEX: process.env.SENSEX_SECURITY_ID || '51',
};

function todayIST() {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Kolkata' }).format(new Date());
}

async function market() {
  const data = await dhan('/marketfeed/ltp', { IDX_I: [Number(IDS.NIFTY), Number(IDS.SENSEX)] });
  const idx = data?.data?.IDX_I || {};
  return {
    nifty: idx[IDS.NIFTY] || null,
    sensex: idx[IDS.SENSEX] || null,
    provider: 'DhanHQ',
    updatedAt: new Date().toISOString(),
  };
}

async function expiry(underlying) {
  const id = IDS[underlying];
  if (!id) throw new Error('Unknown underlying');
  const data = await dhan('/optionchain/expirylist', {
    UnderlyingScrip: Number(id),
    UnderlyingSeg: 'IDX_I',
  });
  return data?.data || [];
}

function summarizeChain(raw) {
  const oc = raw?.data?.oc || {};
  const rows = Object.entries(oc).map(([strike, x]) => ({
    strike: Number(strike),
    call: x.ce ? { ltp: x.ce.last_price, oi: x.ce.oi, prevOi: x.ce.previous_oi, volume: x.ce.volume, iv: x.ce.implied_volatility } : null,
    put: x.pe ? { ltp: x.pe.last_price, oi: x.pe.oi, prevOi: x.pe.previous_oi, volume: x.pe.volume, iv: x.pe.implied_volatility } : null,
  })).sort((a,b) => a.strike-b.strike);
  const spot = Number(raw?.data?.last_price || 0);
  const atm = rows.reduce((best, r) => !best || Math.abs(r.strike-spot) < Math.abs(best.strike-spot) ? r : best, null);
  const totalPutOI = rows.reduce((s,r) => s + (r.put?.oi || 0), 0);
  const totalCallOI = rows.reduce((s,r) => s + (r.call?.oi || 0), 0);
  return { spot, atm, pcr: totalCallOI ? totalPutOI / totalCallOI : null, rows: rows.slice(Math.max(0, rows.findIndex(r => r.strike === atm?.strike)-6), Math.max(0, rows.findIndex(r => r.strike === atm?.strike)+7)) };
}

async function optionchain(underlying, exp) {
  const exps = exp ? [exp] : await expiry(underlying);
  if (!exps.length) throw new Error('No active expiry returned by Dhan.');
  const raw = await dhan('/optionchain', {
    UnderlyingScrip: Number(IDS[underlying]),
    UnderlyingSeg: 'IDX_I',
    Expiry: exps[0],
  });
  return { expiry: exps[0], ...summarizeChain(raw) };
}

async function candles(underlying) {
  const id = IDS[underlying];
  const date = todayIST();
  const raw = await dhan('/charts/intraday', {
    securityId: String(id),
    exchangeSegment: 'IDX_I',
    instrument: 'INDEX',
    interval: '5',
    oi: false,
    fromDate: `${date} 09:15:00`,
    toDate: `${date} 15:30:00`,
  });
  const n = Math.min(raw?.close?.length || 0, 120);
  const bars = [];
  for (let i = Math.max(0, n - 78); i < n; i++) bars.push({
    ts: raw.timestamp?.[i], open: raw.open?.[i], high: raw.high?.[i], low: raw.low?.[i], close: raw.close?.[i], volume: raw.volume?.[i] || 0,
  });
  let pv=0, vol=0;
  bars.forEach(b => { const tp=(b.high+b.low+b.close)/3; pv += tp*(b.volume||0); vol += b.volume||0; });
  return { bars, vwap: vol ? pv/vol : null };
}

export default async function handler(req, res) {
  if (req.method !== 'GET') return json(res, 405, { error: 'GET only' });
  const action = req.query?.action || 'status';
  try {
    if (!process.env.DHAN_ACCESS_TOKEN || !process.env.DHAN_CLIENT_ID) {
      return json(res, 200, { live: false, provider: 'DhanHQ', error: 'Dhan credentials are not configured yet.' });
    }
    if (action === 'market') return json(res, 200, { live: true, ...(await market()) });
    if (action === 'expiry') return json(res, 200, { live: true, nifty: await expiry('NIFTY'), sensex: await expiry('SENSEX') });
    if (action === 'chain') {
      const underlying = String(req.query?.underlying || 'NIFTY').toUpperCase();
      return json(res, 200, { live: true, underlying, ...(await optionchain(underlying, req.query?.expiry)) });
    }
    if (action === 'candles') {
      const underlying = String(req.query?.underlying || 'NIFTY').toUpperCase();
      return json(res, 200, { live: true, underlying, ...(await candles(underlying)) });
    }
    return json(res, 200, { live: true, provider: 'DhanHQ', actions: ['market','expiry','chain','candles'] });
  } catch (e) {
    return json(res, 502, { live: false, provider: 'DhanHQ', error: e.message });
  }
}
