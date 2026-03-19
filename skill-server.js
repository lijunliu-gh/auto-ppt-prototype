const http = require('http');
const path = require('path');

const { resolvePath } = require('./deck-agent-core');
const { handleSkillRequest } = require('./agent-skill');

const port = Number.parseInt(process.env.PORT || '3010', 10);

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, { 'Content-Type': 'application/json; charset=utf-8' });
  response.end(JSON.stringify(payload, null, 2));
}

function readJsonBody(request) {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1024 * 1024) {
        reject(new Error('Request body too large.'));
      }
    });
    request.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(new Error(`Invalid JSON body: ${error.message}`));
      }
    });
    request.on('error', reject);
  });
}

function normalizeRequestPayload(payload) {
  const timestamp = Date.now();
  const action = payload.action === 'revise' ? 'revise' : 'create';
  const suffix = action === 'revise' ? 'http-revised' : 'http-generated';

  return {
    action,
    prompt: payload.prompt,
    mock: Boolean(payload.mock),
    research: Boolean(payload.research),
    contextFiles: Array.isArray(payload.contextFiles) ? payload.contextFiles : [],
    sources: Array.isArray(payload.sources) ? payload.sources : [],
    deckPath: payload.deckPath,
    outputJson: payload.outputJson || path.join('output', `${suffix}-${timestamp}.json`),
    outputPptx: payload.outputPptx || path.join('output', `${suffix}-${timestamp}.pptx`)
  };
}

const server = http.createServer(async (request, response) => {
  try {
    if (request.method === 'GET' && request.url === '/health') {
      sendJson(response, 200, { ok: true, service: 'auto-ppt-skill-server' });
      return;
    }

    if (request.method === 'POST' && request.url === '/skill') {
      const payload = await readJsonBody(request);
      const normalized = normalizeRequestPayload(payload);
      const result = await handleSkillRequest(normalized, null);
      sendJson(response, 200, result);
      return;
    }

    sendJson(response, 404, {
      ok: false,
      error: 'Not found',
      routes: {
        health: 'GET /health',
        skill: 'POST /skill'
      }
    });
  } catch (error) {
    sendJson(response, 500, {
      ok: false,
      error: error.message
    });
  }
});

server.listen(port, () => {
  console.log(`Skill server listening on http://127.0.0.1:${port}`);
  console.log(`Health: http://127.0.0.1:${port}/health`);
  console.log(`Skill endpoint: POST http://127.0.0.1:${port}/skill`);
});
