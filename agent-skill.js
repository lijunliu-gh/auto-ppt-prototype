const fs = require('fs');
const path = require('path');

const { buildDeck } = require('./generate-ppt');
const { loadSourceContexts } = require('./source-loader');
const {
  rootDir,
  resolvePath,
  readTextFile,
  ensureParentDir,
  executePlanningFlow
} = require('./deck-agent-core');

const defaultRequestPath = path.join(rootDir, 'sample-agent-request.json');
const defaultResponsePath = path.join(rootDir, 'output', 'agent-response.json');

function fail(message) {
  console.error(`Error: ${message}`);
  process.exit(1);
}

function printHelp() {
  console.log(`Usage:
  node agent-skill.js --request sample-agent-request.json

Options:
  --request <path>        JSON request payload for the skill
  --response <path>       Where to save the JSON response payload
  --help                  Show this help message
`);
}

function parseArgs(argv) {
  const args = {
    requestPath: defaultRequestPath,
    responsePath: defaultResponsePath
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    switch (token) {
      case '--request':
        args.requestPath = resolvePath(argv[index + 1] || defaultRequestPath);
        index += 1;
        break;
      case '--response':
        args.responsePath = resolvePath(argv[index + 1] || defaultResponsePath);
        index += 1;
        break;
      case '--help':
        printHelp();
        process.exit(0);
        break;
      default:
        break;
    }
  }

  return args;
}

function loadRequest(filePath) {
  const payload = JSON.parse(readTextFile(filePath));
  if (!payload || typeof payload !== 'object') {
    fail('Request payload must be a JSON object.');
  }
  if (!payload.action || !['create', 'revise'].includes(payload.action)) {
    fail('Request payload action must be either "create" or "revise".');
  }
  if (!payload.prompt || typeof payload.prompt !== 'string') {
    fail('Request payload prompt is required.');
  }
  return {
    ...payload,
    _baseDir: path.dirname(filePath)
  };
}

function resolveFromBase(baseDir, filePath) {
  return path.isAbsolute(filePath) ? filePath : path.resolve(baseDir, filePath);
}

async function handleSkillRequest(request, responsePath) {
  const requestBaseDir = request._baseDir || rootDir;
  const contextTexts = Array.isArray(request.contextFiles)
    ? request.contextFiles.map((filePath) => readTextFile(resolveFromBase(requestBaseDir, filePath)))
    : [];
  const sourceData = await loadSourceContexts(Array.isArray(request.sources) ? request.sources : [], {
    baseDir: requestBaseDir
  });

  const existingDeck = request.action === 'revise' && request.deckPath
    ? JSON.parse(readTextFile(resolveFromBase(requestBaseDir, request.deckPath)))
    : null;

  const deck = await executePlanningFlow({
    prompt: request.prompt,
    contextTexts: contextTexts.concat(sourceData.contextTexts),
    loadedSources: sourceData.loadedSources,
    researchEnabled: Boolean(request.research),
    mock: Boolean(request.mock),
    mode: request.action,
    existingDeck
  });

  const outputJson = resolveFromBase(requestBaseDir, request.outputJson || (request.action === 'revise' ? 'output/agent-revised-deck.json' : 'output/agent-generated-deck.json'));
  const outputPptx = resolveFromBase(requestBaseDir, request.outputPptx || (request.action === 'revise' ? 'output/agent-revised-deck.pptx' : 'output/agent-generated-deck.pptx'));
  ensureParentDir(outputJson);
  fs.writeFileSync(outputJson, JSON.stringify(deck, null, 2));
  await buildDeck(deck, outputPptx);

  const response = {
    ok: true,
    action: request.action,
    prompt: request.prompt,
    deckJsonPath: outputJson,
    pptxPath: outputPptx,
    slideCount: deck.slideCount,
    assumptions: deck.assumptions,
    sourcesUsed: sourceData.loadedSources.map((source) => ({
      label: source.label,
      type: source.type,
      location: source.location,
      trustLevel: source.trustLevel,
      priority: source.priority
    }))
  };

  if (responsePath) {
    ensureParentDir(responsePath);
    fs.writeFileSync(responsePath, JSON.stringify(response, null, 2));
    console.log(`Skill response saved to: ${responsePath}`);
  }

  return response;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const request = loadRequest(args.requestPath);
  await handleSkillRequest(request, args.responsePath);
}

module.exports = {
  handleSkillRequest,
  loadRequest
};

if (require.main === module) {
  main().catch((error) => fail(error.message));
}
