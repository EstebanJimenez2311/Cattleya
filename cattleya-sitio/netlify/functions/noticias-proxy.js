/**
 * Netlify Function: noticias-proxy (DEPRECATED)
 * Ruta: /.netlify/functions/noticias-proxy?url=ENCODED_URL
 *
 * ⚠️ DEPRECATED: Esta función ya no se usa.
 * Ahora el backend Django maneja la importación de RSS directamente.
 * El frontend se conecta a la API de Django: http://127.0.0.1:8000/api/noticias/
 *
 * Esta función se mantiene solo como referencia histórica.
 * Para producción, usar el backend Django con CORS habilitado.
 */

const https = require('https');
const http = require('http');

const ALLOWED_DOMAINS = [
  'elespectador.com',
  'elheraldo.co',
  'caracol.com.co',
  'eltiempo.com',
  'semana.com',
  'infobae.com',
  'rcnradio.com',
  'bluradio.com',
  'wradio.com.co',
  'lafm.com.co'
];

function isAllowedDomain(url) {
  try {
    const { hostname } = new URL(url);
    return ALLOWED_DOMAINS.some((domain) => hostname.endsWith(domain));
  } catch {
    return false;
  }
}

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(
      url,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; CattleyaBot/1.0; +https://cattleya.netlify.app)',
          Accept: 'application/rss+xml, application/xml, text/xml, */*'
        },
        timeout: 8000
      },
      (res) => {
        // Seguir redirecciones manualmente (hasta 3)
        if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
          return fetchUrl(res.headers.location).then(resolve).catch(reject);
        }

        if (res.statusCode < 200 || res.statusCode >= 300) {
          return reject(new Error(`HTTP ${res.statusCode}`));
        }

        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
        res.on('error', reject);
      }
    );

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Cache-Control': 'public, max-age=1800' // cache 30 min en el edge
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers, body: '' };
  }

  if (event.httpMethod !== 'GET') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  const rawUrl = event.queryStringParameters && event.queryStringParameters.url;

  if (!rawUrl) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'Parametro ?url requerido' })
    };
  }

  let targetUrl;
  try {
    targetUrl = decodeURIComponent(rawUrl);
    new URL(targetUrl); // valida que sea una URL valida
  } catch {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'URL invalida' })
    };
  }

  if (!isAllowedDomain(targetUrl)) {
    return {
      statusCode: 403,
      headers,
      body: JSON.stringify({ error: 'Dominio no permitido', url: targetUrl })
    };
  }

  try {
    const content = await fetchUrl(targetUrl);
    return {
      statusCode: 200,
      headers: { ...headers, 'Content-Type': 'application/xml; charset=utf-8' },
      body: content
    };
  } catch (err) {
    return {
      statusCode: 502,
      headers,
      body: JSON.stringify({ error: 'No se pudo obtener el feed', detail: err.message })
    };
  }
};
