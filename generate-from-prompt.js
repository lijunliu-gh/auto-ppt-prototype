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

const defaultJsonOutput = path.join(rootDir, 'output', 'generated-deck.json');
const defaultPptxOutput = path.join(rootDir, 'output', 'generated-deck.pptx');

function fail(message) {
  console.error(`Error: ${message}`);
  process.exit(1);
}

function printHelp() {
  console.log(`Usage:
  node generate-from-prompt.js --prompt "Create a 10-slide investor deck for..."

Options:
  --prompt <text>         Presentation request in natural language
  --prompt-file <path>    Read the request from a text file
  --out-json <path>       Where to save the generated deck JSON
  --out-pptx <path>       Where to save the generated PPTX file
  --context-file <path>   Extra context material to include in planning (repeatable)
  --source <value>        Source file path or URL to include in planning (repeatable)
  --research              Attempt optional web research when TAVILY_API_KEY is configured
  --mock                  Skip model calls and use a local heuristic planner
  --help                  Show this help message
`);
}

function parseArgs(argv) {
  const args = {
    prompt: '',
    outputJson: defaultJsonOutput,
    outputPptx: defaultPptxOutput,
    mock: false,
    research: false,
    contextFiles: [],
    sources: []
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    switch (token) {
      case '--prompt':
        args.prompt = argv[index + 1] || '';
        index += 1;
        break;
      case '--prompt-file':
        args.prompt = readTextFile(resolvePath(argv[index + 1] || ''));
        index += 1;
        break;
      case '--out-json':
        args.outputJson = resolvePath(argv[index + 1] || defaultJsonOutput);
        index += 1;
        break;
      case '--out-pptx':
        args.outputPptx = resolvePath(argv[index + 1] || defaultPptxOutput);
        index += 1;
        break;
      case '--context-file':
        args.contextFiles.push(resolvePath(argv[index + 1] || ''));
        index += 1;
        break;
      case '--source':
        args.sources.push(argv[index + 1] || '');
        index += 1;
        break;
      case '--research':
        args.research = true;
        break;
      case '--mock':
        args.mock = true;
        break;
      case '--help':
        printHelp();
        process.exit(0);
        break;
      default:
        if (!token.startsWith('--') && !args.prompt) {
          args.prompt = token;
        }
        break;
    }
  }

  if (!args.prompt || !args.prompt.trim()) {
    fail('A presentation prompt is required. Use --prompt "..." or --prompt-file path.');
  }

  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const contextTexts = args.contextFiles.map((filePath) => readTextFile(filePath));
  const sourceData = await loadSourceContexts(args.sources, { baseDir: rootDir });
  const deck = await executePlanningFlow({
    prompt: args.prompt,
    contextTexts: contextTexts.concat(sourceData.contextTexts),
    loadedSources: sourceData.loadedSources,
    researchEnabled: args.research,
    mock: args.mock,
    mode: 'create'
  });

  ensureParentDir(args.outputJson);
  fs.writeFileSync(args.outputJson, JSON.stringify(deck, null, 2));
  await buildDeck(deck, args.outputPptx);
  console.log(`Deck JSON saved to: ${args.outputJson}`);
  if (sourceData.loadedSources.length > 0) {
    console.log(`Loaded sources: ${sourceData.loadedSources.length}`);
  }
}

main().catch((error) => fail(error.message));
