// core/run.js
//
// Works out how to run a step's code for each language. The runner writes the learner's code to a file with the
// name given here, then starts the command this module returns.
//
// Python and JavaScript use the tutorial's own environment, which setup.ps1 creates. Python runs with the interpreter
// in the tutorial's .venv. JavaScript runs under samples/. The npm packages are installed once, at the repository root,
// and Node finds them by walking up from the file's folder.

'use strict';

const fs = require('node:fs');
const path = require('node:path');

const FILE_NAMES = {
  csharp: 'main.cs',
  python: 'main.py',
  javascript: 'main.js',
};

// The Python interpreter inside the tutorial's environment, as setup.ps1 creates it.
function environmentFor(courseRoot) {
  return { python: path.join(courseRoot, '.venv', 'Scripts', 'python.exe') };
}

// The environment every run gets: the learner's own environment, plus TRAINING_DATA, which points at the sample data.
// Samples read their input files from there, so the same paths work in the runner, in the lesson, and on the
// learner's own machine. CHAIN_DATA points at the scratch folder the conversion chain passes files through. It is
// created if it does not exist, so the first step of the chain can always write.
function runEnvironment(courseRoot) {
  const chain = path.join(courseRoot, 'samples', '.chain');
  fs.mkdirSync(chain, { recursive: true });
  return { ...process.env, TRAINING_DATA: path.join(courseRoot, 'samples', 'data'), CHAIN_DATA: chain };
}

// The folder a run happens in. JavaScript runs under samples/.runs, so that Node finds the packages installed at the
// repository root. C# and Python run in the user data folder.
function runFolderFor(language, lessonId, courseRoot, userDataDir) {
  const name = lessonId.replace(/[^A-Za-z0-9-]+/g, '_');
  if (language === 'javascript') return path.join(courseRoot, 'samples', '.runs', name);
  return path.join(userDataDir, 'runs', name);
}

// True when a package is installed in this folder or in one above it, the way Node looks for packages.
function isInstalled(name, folder) {
  let dir = folder;
  for (;;) {
    if (fs.existsSync(path.join(dir, 'node_modules', name, 'package.json'))) return true;
    const parent = path.dirname(dir);
    if (parent === dir) return false;
    dir = parent;
  }
}

// What must be in place before a language can run, or null when it is ready. The message says what to do.
function prerequisiteProblem(language, courseRoot) {
  if (language === 'python' && !fs.existsSync(environmentFor(courseRoot).python)) {
    return 'The tutorial Python environment is missing. Run setup.ps1 in the training-data-formats folder.';
  }
  if (language === 'javascript') {
    const manifest = path.join(courseRoot, 'samples', 'package.json');
    if (!fs.existsSync(manifest)) {
      return 'The JavaScript sample setup is missing. Run setup.ps1 in the training-data-formats folder.';
    }
    // Packages are needed only when the manifest declares some. Each declared package must be installed, not just the folder.
    const declared = Object.keys(JSON.parse(fs.readFileSync(manifest, 'utf8')).dependencies || {});
    const missing = declared.filter((name) => !isInstalled(name, path.join(courseRoot, 'samples')));
    if (missing.length > 0) {
      return 'The JavaScript sample packages are missing (' + missing.join(', ') + '). Run npm install in the training-data-formats folder, or setup.ps1.';
    }
  }
  return null;
}

// The command to run one file. For C#, `dotnet run` runs a single source file directly (.NET 10 SDK).
function commandFor(language, file, environment) {
  switch (language) {
    case 'csharp':
      return { command: 'dotnet', args: ['run', file] };
    case 'python':
      return { command: environment.python, args: [file] };
    case 'javascript':
      return { command: 'node', args: [file] };
    default:
      throw new Error(`The runner has no way to run ${language}.`);
  }
}

module.exports = { FILE_NAMES, commandFor, environmentFor, runEnvironment, runFolderFor, prerequisiteProblem, isInstalled };
