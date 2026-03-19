const { spawnSync } = require('child_process');

const commands = [
  ['npm', ['run', 'smoke:generate']],
  ['npm', ['run', 'smoke:source']],
  ['npm', ['run', 'smoke:revise']],
  ['npm', ['run', 'smoke:skill']]
];

for (const [command, args] of commands) {
  const result = spawnSync(command, args, {
    stdio: 'inherit',
    shell: process.platform === 'win32'
  });

  if (typeof result.status === 'number' && result.status !== 0) {
    process.exit(result.status);
  }

  if (result.error) {
    console.error(result.error.message);
    process.exit(1);
  }
}