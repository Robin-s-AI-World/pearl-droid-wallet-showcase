// Vercel Serverless Function: log-acceptance
// Logs clickwrap acceptance events (IP, geo, timestamp) to Vercel runtime logs.
// TODO: When StackCP MySQL is provisioned, uncomment the MySQL persistence block
// and set environment variables: MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
// See README.md → Clickwrap Logging section for setup instructions.

// TODO: Install mysql2 as a dependency and uncomment the import:
// const mysql = require('mysql2/promise');

export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const headers = req.headers || {};
  const ip = headers['x-forwarded-for'] || headers['x-real-ip'] || 'unknown';
  const ipClean = ip.split(',')[0].trim();
  const country = headers['x-vercel-ip-country'] || 'unknown';
  const region = headers['x-vercel-ip-country-region'] || 'unknown';
  const userAgent = headers['user-agent'] || 'unknown';

  const body = req.body || {};
  const version = body.version || 'unknown';

  const record = {
    accepted_at: new Date().toISOString(),
    ip_address: ipClean,
    country: country,
    region: region,
    user_agent: userAgent,
    app_version: version,
    accepted: true,
    download_url: body.url || null
  };

  // Log to Vercel runtime logs (viewable in Vercel dashboard → Project → Logs)
  console.log('[clickwrap-acceptance]', JSON.stringify(record));

  // TODO: Persist to StackCP MySQL when provisioned.
  // Uncomment and configure the block below once the database is ready:
  //
  // const conn = await mysql.createConnection({
  //   host: process.env.MYSQL_HOST,
  //   port: parseInt(process.env.MYSQL_PORT || '3306'),
  //   user: process.env.MYSQL_USER,
  //   password: process.env.MYSQL_PASSWORD,
  //   database: process.env.MYSQL_DATABASE
  // });
  // await conn.execute(
  //   'INSERT INTO clickwrap_acceptances (accepted_at, ip_address, country, region, user_agent, app_version, accepted) VALUES (?, ?, ?, ?, ?, ?, ?)',
  //   [record.accepted_at, record.ip_address, record.country, record.region, record.user_agent, record.app_version, record.accepted]
  // );
  // await conn.end();

  res.status(200).json({ ok: true });
}
