# Quick start

This guide gets the Working With Data Formats runner open. The runner is a desktop window, so the tutorial needs no server, no browser, and no accounts. The samples run on your machine in C#, Python, and JavaScript, and the runner shows each one next to its lesson.

The tutorial lives at [databankimx/training-data-formats](https://github.com/databankimx/training-data-formats). Clone it into `C:\Development\training\training-data-formats`, or let the setup script do that for you.

## Quick setup with the script

### What gets installed

By default, the setup installs:

* Git
* PowerShell 7
* Node.js 24 or newer
* Python 3.12
* .NET SDK 10
* VS Code, with the extensions ms-dotnettools.csharp, ms-dotnettools.csdevkit, ms-python.python
* Notepad++

The C++ Build Tools aren't installed up front. The script installs them only if Electron's binary can't download.

The setup then runs these steps: Python virtual environment; npm packages; Runner tests. At the end it opens the repository in VS Code and starts the lesson runner window (Electron).

### Getting started

There are three methods available to set up this tutorial. They are currently Windows-only.

#### Full Automation (if you don't have Git currently set up)

This process will install Git and copy the repository to a subfolder of `C:\Development\training` and install all necessary software and extensions for the tutorial's lesson runner.

1. Obtain the tutorial's GitHub slug name, which is `training-data-formats`
2. Open PowerShell using "Run as Administrator"
3. Run the script below

```pwsh
# Obtain the load tutorial script
irm https://raw.githubusercontent.com/databankimx/training-shared-template/main/load-tutorial.ps1 -OutFile "$env:TEMP\load-tutorial.ps1"

# Perform automated setup
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\load-tutorial.ps1" -RepoUrl https://github.com/databankimx/training-data-formats.git
```

#### Automated Setup from Local Repo (assumes you already have Git installed and set up)

In this process, you pull the existing repository and then run its setup script, which installs all necessary software and extensions for the tutorial's lesson runner.

1. Obtain the tutorial's GitHub slug name, which is `training-data-formats`
2. Open PowerShell using "Run as Administrator"
3. If you will use the default base directory `C:\Development\training`, run the following:

```pwsh
# Create the base folder if it doesn't exist yet
New-Item -ItemType Directory -Force -Path C:\Development\training | Out-Null
```

4. Clone the repository. If you're using a different base directory, replace `C:\Development\training` with your path:

```pwsh
# Go there and clone the tutorial
cd C:\Development\training
git clone https://github.com/databankimx/training-data-formats.git
cd training-data-formats
```

5. If desired, edit the setup configuration, which determines what software is installed automatically (see "Change what gets installed" below)

```pwsh
# Optional: edit setup.json before installations
notepad setup.json
```

6. Save the configuration if you edited it, then run the setup script

##### If using the default base path, run this:

```pwsh
# Run the setup
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

##### If using a different base path, replace `<BASE_DIR>` with your path and run this:

```pwsh
# Run the setup
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1 -BaseDirectory <BASE_DIR>
```

#### Manual Setup from Local Repo

If you want to do everything manually, you can pull the repository and set up software on your own.

1. Obtain the tutorial's GitHub slug name, which is `training-data-formats`
2. Run the script below

```pwsh
git clone https://github.com/databankimx/training-data-formats.git
```

3. Review README.md and QUICKSTART.md in the repository for instructions for manual setup.

### Switches and notes

* `-SkipInstall` checks what's installed and installs nothing.
* `-NoLaunch` runs the setup but doesn't open VS Code or start the runner.
* Installing uses winget. If winget isn't available, install **App Installer** from the Microsoft Store first. Company policy can block installs, in which case the script stops and you'll need IT.
* If an install needs administrator rights, the script stops before installing anything and asks you to run it again from an Administrator PowerShell window.

### Change what gets installed

The settings are in `setup.json`, in the repository folder. Open it in any text editor:

* Set an install's `"install"` to `true` to include it, or `false` to skip it.
* `"pinned"` sets the version. `"extensions"` lists the VS Code extensions to add.
* Save the file, then run `setup.ps1` again. It skips what's already installed.

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
