// test/run.test.js
//
// Checks the command for each language, and the toolchain check with a stand-in for the real commands.

'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { FILE_NAMES, commandFor, runEnvironment, prerequisiteProblem, isInstalled } = require('../core/run');
const { probe, probeAll, COMMANDS } = require('../core/toolchains');

test('each course language maps to its source file name', () => {
  assert.deepEqual(FILE_NAMES, { csharp: 'main.cs', python: 'main.py', javascript: 'main.js' });
});

test('each language runs its file with its own command', () => {
  const environment = { python: 'C:\\course\\.venv\\Scripts\\python.exe' };
  assert.deepEqual(commandFor('csharp', 'main.cs', environment), { command: 'dotnet', args: ['run', 'main.cs'] });
  assert.deepEqual(commandFor('python', 'main.py', environment), { command: environment.python, args: ['main.py'] });
  assert.deepEqual(commandFor('javascript', 'main.js', environment), { command: 'node', args: ['main.js'] });
});

test('an unknown language is refused', () => {
  assert.throws(() => commandFor('typescript', 'main.ts', {}), /no way to run typescript/);
});

test('every run gets TRAINING_DATA and CHAIN_DATA, and keeps the learner environment', () => {
  const course = fs.mkdtempSync(path.join(os.tmpdir(), 'course-'));
  const environment = runEnvironment(course);
  // Windows stores the PATH variable as "Path", so the whole environment is compared rather than one key.
  assert.deepEqual(environment, {
    ...process.env,
    TRAINING_DATA: path.join(course, 'samples', 'data'),
    CHAIN_DATA: path.join(course, 'samples', '.chain'),
  });
  assert.ok(fs.existsSync(path.join(course, 'samples', '.chain')));
});

test('a language whose command runs is available, with its first line of version output', async () => {
  const fakeRun = (command, args, options, callback) => callback(null, '10.0.100\nmore text\n', '');
  const result = await probe('csharp', fakeRun);
  assert.deepEqual(result, { available: true, version: '10.0.100' });
});

test('a language whose command is missing is unavailable', async () => {
  const fakeRun = (command, args, options, callback) => callback(new Error('not found'), '', '');
  const result = await probe('python', fakeRun);
  assert.deepEqual(result, { available: false, version: null });
});

test('probeAll checks every course language', async () => {
  const fakeRun = (command, args, options, callback) =>
    command === 'node' ? callback(new Error('missing'), '', '') : callback(null, 'v1\n', '');
  const result = await probeAll(fakeRun);
  assert.deepEqual(Object.keys(result).sort(), Object.keys(COMMANDS).sort());
  assert.equal(result.javascript.available, false);
  assert.equal(result.csharp.available, true);
  assert.equal(result.python.available, true);
});

// A course folder laid out the way the installs leave it: packages at the root, the manifest under samples/.
function courseWith(dependencies, installed) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'course-'));
  fs.mkdirSync(path.join(root, 'samples'), { recursive: true });
  fs.writeFileSync(path.join(root, 'samples', 'package.json'), JSON.stringify({ dependencies }));
  for (const name of installed) {
    const folder = path.join(root, 'node_modules', name);
    fs.mkdirSync(folder, { recursive: true });
    fs.writeFileSync(path.join(folder, 'package.json'), '{}');
  }
  return root;
}

test('a sample package installed at the repository root is found', () => {
  const root = courseWith({ 'csv-parse': '7.0.2' }, ['csv-parse']);
  try {
    assert.equal(isInstalled('csv-parse', path.join(root, 'samples')), true);
    assert.equal(prerequisiteProblem('javascript', root), null);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('a declared sample package that is not installed is reported by name', () => {
  const root = courseWith({ 'csv-parse': '7.0.2', 'js-yaml': '5.4.1' }, ['csv-parse']);
  try {
    const problem = prerequisiteProblem('javascript', root);
    assert.match(problem, /js-yaml/);
    assert.doesNotMatch(problem, /csv-parse/);
    assert.match(problem, /npm install in the training-data-formats folder/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('a package folder without a package.json does not count as installed', () => {
  const root = courseWith({ 'csv-parse': '7.0.2' }, []);
  try {
    fs.mkdirSync(path.join(root, 'node_modules', 'csv-parse'), { recursive: true });
    assert.equal(isInstalled('csv-parse', path.join(root, 'samples')), false);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
