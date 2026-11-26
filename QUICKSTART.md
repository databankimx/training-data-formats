# Quick start

This guide gets the Working With Data Formats runner open. The runner is a desktop window, so the tutorial needs no server, no browser, and no accounts. The samples run on your machine in C#, Python, and JavaScript, and the runner shows each one next to its lesson.

The tutorial lives at [databankimx/training-data-formats](https://github.com/databankimx/training-data-formats). Clone it into `C:\Development\training\training-data-formats`, or let the setup script do that for you.

## Quick setup with the script

`setup.ps1` does the whole setup. You can run it from anywhere. If it isn't inside the repository, it clones the repository into `C:\Development\training\training-data-formats` and runs the cloned copy. It then:

- checks for Git, and installs it with winget if it's missing
- checks for Node.js 24 or later, and installs the LTS release with winget if it's missing
- checks for Python 3.12 or later, and installs it with winget if it's missing
- checks for the .NET 10 SDK, which runs the C# samples, and installs it with winget if it's missing
- checks for Visual Studio Code, and installs it with winget if it's missing
- checks for the C++ Build Tools only if Electron's download fails, and installs them then
- creates the Python virtual environment in `.venv` at the repository root, and installs `requirements.txt` into it
- installs every npm package in one step, from `package.json` and `package-lock.json` at the repository root, and makes sure the Electron binary is present

It's safe to run more than once. Anything already in place is skipped.

Open PowerShell, and run:

```pwsh
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

The `-ExecutionPolicy Bypass` part lets this one script run. It doesn't change any setting on your machine.

The C++ Build Tools are installed only if Electron's download fails. They are about 4 to 5 GB and can take several minutes, and they need an **Administrator** PowerShell. If you aren't an administrator, the script stops at that step and says so. Open PowerShell as Administrator, and run the script again.

If you only want to check your setup, without installing anything, add `-SkipInstall`:

```pwsh
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1 -SkipInstall
```

To run the runner's tests as well, add `-RunTests`. They aren't run by default.

When the script finishes, it prints a summary and the command to start the runner. Every line should say `ok`.

Installing uses winget. If winget isn't available, install **App Installer** from the Microsoft Store first. Company policy can block installs, in which case the script stops and you'll need IT.

## Manual setup

If you'd rather not run the script, these are the same steps by hand. Run them from the repository root, `C:\Development\training\training-data-formats`, in PowerShell.

1. Install the tools:
   - Node.js 24 or later, from [nodejs.org](https://nodejs.org)
   - Python 3.12 or later, from [python.org](https://www.python.org)
   - The .NET 10 SDK, from [dotnet.microsoft.com](https://dotnet.microsoft.com)
   - Visual Studio Code, from [code.visualstudio.com](https://code.visualstudio.com)
   - The Visual Studio Build Tools with the C++ workload, only if Electron's download fails later
2. Install the npm packages. This one command installs the runner's packages and the samples' packages together:

   ```pwsh
   npm install
   ```

3. Create the Python virtual environment and install the Python packages:

   ```pwsh
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   The `pyarrow` package is about 50 MB, so this step can take several minutes the first time.

If `npm install` reports that the Electron binary is missing, run `npm install` again, with the Build Tools installed.

## Start the runner

```pwsh
cd C:\Development\training\training-data-formats\lesson-runner
npm start
```

Run `npm start` from the `lesson-runner` folder. The repository's root folder has a `package.json` for the installs, but the runner starts from `lesson-runner`.

The runner reopens the lesson you were on last. The first time, it opens on the first lesson. Close the window normally to stop it.

## Editing in VS Code

You can open the repository folder in VS Code, and edit the lessons and samples there. To run the Python samples from VS Code with the packages you installed, choose the `.venv` interpreter: open a Python file, then choose **Python: Select Interpreter**, and pick the one in `.venv`. The runner doesn't need VS Code, and it uses `.venv` by itself.

## How the lessons work

- The **sidebar** lists the chapters. Open a part, then choose a chapter, and the steps of that chapter appear below it. Use **Next** and **Previous** to move through the course in order.
- Read each lesson in the **Lesson** tab. Examples show the code in each language, and you choose the language once for every example.
- Samples in a lesson can be edited and run in place. Press **Run** under the sample to see its output.
- Homework and exercises use the **Source** tab. Press **Run** (F5) to run your code, or **Check** (Ctrl+F5) to compare its output with the expected result.
- **Show solutions (spoiler)** opens the solutions for a homework item. Try the homework first. Once you've opened the solutions, the gate stays open the next time you visit the step, and the solutions are hidden again until you choose to show them.
- **Reset** puts back the starter code of a homework item.
- **Open** next to a sample data file opens it in the program your computer uses for that file type. Tick **open as text** to open it in your text editor instead.
- Press Ctrl and move the mouse wheel to change the size of the lesson text.
- Ctrl+Left and Ctrl+Right move to the previous and next lesson, unless the cursor is in an editor.

The chapter called **Appendix** has a cheat sheet, a format guide, and a glossary. It has no exercises.

## Your progress

The runner saves your progress as you go, in a file outside the repository, so it's never committed:

```
%APPDATA%\training-data-formats-runner\progress.json
```

The saved progress includes the lessons you've visited, your quiz answers, the spoilers you've opened, the solutions you've revealed, and the last lesson you opened.

To clear it, press **Ctrl+Alt+Shift+Backspace** in the runner. The lesson on screen is redrawn with nothing saved, and the next start opens the first lesson.

Your homework edits last only while you're on that step. To keep your work, copy it into a file in your own folder.

Sample runs are written to `samples\.runs` and the conversion chain to `samples\.chain`. Both folders are created by the runner and are ignored by Git.

## Troubleshooting

- **Setup says Git is missing and winget is not available.** Install **App Installer** from the Microsoft Store, or install Git from [git-scm.com](https://git-scm.com), then run the script again.
- **Setup says Node.js, Python, or the .NET SDK is too old.** Install the current release from the link above, open a new PowerShell window, and run the script again.
- **Setup says the C++ Build Tools need an Administrator.** Open PowerShell as Administrator, then run the script again.
- **Setup says `npm install` failed.** Check your network access to the npm registry, then run the script again. Don't delete `package-lock.json` to get past the error.
- **Setup says the Electron binary still won't download.** Check your network access to github.com, and that the C++ Build Tools are installed. Then run the script again.
- **`npm install` shows deprecation warnings.** They come from `exceljs`'s dependencies, and they're notices about old packages, not vulnerabilities. The `uuid` package is pinned to 11.1.1 by an override in `package.json` to clear an advisory, so don't remove the override.
- **The first C# run prints a long .NET welcome message and waits.** This happens once, the first time the .NET SDK runs on your computer. Press Escape to stop it, then run the file again. After that, C# runs as expected.
- **A C# sample fails the first time with a package error.** The C# samples download their NuGet packages on the first run, so that run needs internet access. Run it again once you're online.
- **`pip install -r requirements.txt` fails.** Check your network access to the Python package index. If the failure is in `pyarrow`, run the install again, because its download is large.
- **`npm start` fails with "package.json not found".** You're in the repository's root folder. Change to `lesson-runner` first.
- **The runner says the course could not be loaded, or lists a chapter as missing.** A chapter folder is missing from `parts.json`, or a listed chapter has no folder. Tell the tutorial's owner what the message says.
