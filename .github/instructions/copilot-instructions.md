---
applyTo: "**/*"
---

# GitHub Copilot Instructions - DataBank Development Standards

## Purpose
This file defines how GitHub Copilot should generate code for DataBank IMX development teams.
All generated code must align with internal standards for quality, maintainability, security, and consistency.

## Scope
This repository is the **Working With Data Formats** training tutorial. It has an Electron lesson runner (JavaScript), sample code in C#, Python, and JavaScript, and committed sample data. Follow the **Common Standards** section, plus the section for the language you are working in.

---

## Common Standards

### General Principles
- Prioritize **readability, maintainability, and clarity** over brevity.
- Follow **DataBank coding standards** at all times.
- Assume code will be **reviewed, tested, and deployed to client environments**.
- Avoid unsafe, experimental, or non-production-ready patterns.
- Do not introduce unnecessary dependencies or frameworks.
- Third-party packages **must** have licenses that allow closed-source commercial use.
- Prefer existing project patterns over introducing new architectural or library choices.

### Architecture and Design
- Prefer clear separation of concerns.
- Avoid tightly coupled designs.
- Design for reuse and extensibility.
- Keep controllers, endpoints, and entry points thin; place business logic in services or domain components.
- Match the structure and conventions already used by the repository unless the user explicitly requests a redesign.

### Error Handling and Security
- Validate all inputs.
- Avoid exposing sensitive information in exceptions, logs, API responses, or console output.
- Follow least-privilege principles.
- Do not generate insecure defaults, hardcoded secrets, or bypass validation/authentication/authorization checks.
- Exception and error messages must be clear, concise, grammatically correct, and end with a period.

### Comments and Documentation
- Write comments only when necessary.
- Use clear, concise US-English.
- Document complex logic, non-obvious decisions, and important operational behavior.
- Avoid comments that merely restate the code.

### Source Control and Workflow
- All code must be tracked in source control.
- Commit early and often.
- Use meaningful commit messages.
- Link commits to tasks, issues, bugs, or enhancements where appropriate.
- Use branches and pull requests for review; do not commit directly to protected mainline branches.

### Code Reviews and Quality Gates
- All code must be reviewed before merge or delivery.
- Address correctness, readability, performance, security, and maintainability.
- Where applicable, code must pass SonarQube or other required quality gates before merge.

### Testing and QA Expectations
- Follow a **test-driven mindset** where practical.
- Ensure new code is testable.
- Include unit tests and integration tests where appropriate.
- Consider edge cases, invalid inputs, failure scenarios, and regression risk.

### Prohibited Practices
- Do NOT generate hardcoded credentials, secrets, tokens, or connection strings.
- Do NOT introduce unapproved third-party libraries.
- Do NOT expose internal implementation details unnecessarily.
- Do NOT produce code that violates DataBank IP, security, or delivery policies.

---

## Python Project Instructions

Python packages are pinned in the root `requirements.txt`.

### General Style
- Write idiomatic, readable Python.
- Prefer explicit, maintainable code over compact or clever code.
- Use descriptive names for modules, classes, functions, variables, and parameters.
- Match the repository's existing layout and conventions.
- Follow the repository's formatting and linting setup when present.

### Structure
- Keep modules focused and cohesive.
- Keep functions and methods reasonably small and single-purpose.
- Place business logic outside of CLI handlers, route handlers, or task entry points when practical.
- Reuse existing utilities, services, and patterns before introducing new abstractions.

### Error Handling
- Raise specific exceptions instead of broad `Exception` where practical.
- Preserve original exception context when wrapping or translating errors.
- Keep user-facing error messages clear and safe.
- Avoid swallowing exceptions silently.

### Logging
- Use the repository's existing approved logging pattern.
- If the repository does not define a custom logging abstraction, use Python's standard `logging` module rather than `print` for operational logging.
- Use appropriate log levels.
- Never log secrets, credentials, tokens, or sensitive customer data.

### Documentation
- Add docstrings when the repository uses them consistently or when a function's behavior is not obvious.
- Keep inline comments minimal and purposeful.

### Testing
- Python unit tests **must** use **pytest**. JavaScript tests use `node:test`.
- Avoid introducing alternate Python test frameworks unless already required by the repository.
- Include coverage for normal flow, validation failures, edge cases, and exception paths as appropriate.

### Training Repository Notes
- This repository contains training content. Lesson files and sample code are teaching material. Some sample files are wrong on purpose
  (malformed, mis-encoded, or hostile data) so learners can see the failure. Do not "fix" them.
- The files in `samples/data` are generated and committed, including binary files. Do not edit them by hand.
- Follow the established conventions of the existing lessons and try-it-yourself files.
- Keep the three language versions of a lesson equivalent in behavior.

---

## JavaScript Project Instructions

- The lesson runner (`lesson-runner`) and samples (`samples`) are npm workspaces that target Node.js 24 or later.
- Match the existing module style: CommonJS in `lesson-runner`, ES modules in `samples`.
- Tests use the built-in `node:test` runner. Add new test files to the `test` script in `lesson-runner/package.json`.
- Do not add npm dependencies without license review. Commit `package-lock.json` changes with the `package.json` change.
- Keep renderer code free of Node access; use the preload bridge for anything privileged.

## C# Project Instructions

- Target the .NET 10 SDK. Use nullable reference types and the existing naming conventions.
- Sample packages come from NuGet; verify the license before adding one.

---

## Copilot Behavior Guidelines

When generating code, Copilot should:
- Follow all applicable rules in this document automatically.
- Prefer existing project patterns over new ones.
- Match surrounding code style closely.
- Avoid speculative implementations.
- Ask for clarification through comments or generated TODO notes only when requirements are genuinely unclear.

---

## Definition of Done

Generated code is acceptable only if it:
- Runs successfully without warnings in the target project context.
- Passes required static analysis and quality gates where applicable.
- Follows the Python standards in this file.
- Includes appropriate validation, error handling, and logging.
- Is readable, maintainable, and testable.
