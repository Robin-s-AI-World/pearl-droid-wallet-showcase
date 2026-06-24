// Netlify Function: log-acceptance
// Logs clickwrap acceptance events (IP, geo, timestamp) to Netlify function logs.
// TODO: When StackCP MySQL is provisioned, uncomment the MySQL persistence block
// and set environment variables: MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
// See README.md → Clickwrap Logging section for setup instructions.

// TODO: Install mysql2 as a dependency and uncomment the import:
// const mysql = require('mysql2/promise');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const headers = event.headers || {};
  const ip = headers['x-forwarded-for'] || headers['client-ip'] || 'unknown';
  const ipClean = ip.split(',')[0].trim();
  const country = headers['cf-ipcountry'] || headers['x-vercel-ip-country'] || 'unknown';
  const region = headers['x-vercel-ip-country-region'] || 'unknown';
  const userAgent = headers['user-agent'] || 'unknown';

  let body = {};
  try { body = JSON.parse(event.body || '{}'); } catch (e) {}

  const record = {
    accepted_at: new Date().toISOString(),
    ip_address: ipClean,
    country: country,
    region: region,
    user_agent: userAgent,
    app_version: body.version || 'unknown',
    accepted: true,
    download_url: body.url || null
  };

  // Log to Netlify function logs (viewable in Netlify dashboard → Functions → log-acceptance → Logs)
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

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ok: true })
  };
};
