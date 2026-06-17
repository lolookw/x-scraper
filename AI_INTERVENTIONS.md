# AI Interventions

This repository includes AI-assisted polish work for portfolio presentation and safety hardening. The goal is to make the original learning project easier to review without turning it into a bulk-outreach or abuse tool.

## What changed

| Area | Intervention | Intent |
|------|--------------|--------|
| Safety | Replaced unsafe `eval` parsing with `ast.literal_eval`. | Preserve the saved record format without executing arbitrary code. |
| Secrets | Added `config.example.json` and `.gitignore` rules for local credentials and generated outputs. | Keep real secrets and scrape artifacts out of future commits. |
| Documentation | Added `README.md` with setup, usage, outputs, and ethics notes. | Help reviewers understand the project quickly. |
| Dependencies | Added `requirements.txt`. | Make local setup reproducible. |
| Maintainability | Added small docstrings, narrower exceptions, and safer driver cleanup. | Improve clarity while avoiding a large rewrite. |
| Execution | Updated the GUI to run scripts with the active Python interpreter. | Make virtual-environment usage more reliable. |

## Boundaries

The AI work intentionally avoided expanding direct-message automation. Existing DM-related code is not part of the default execution path and should remain secondary to manual, consent-aware review.

## Learning value

This polish pass demonstrates practical cleanup of an early Selenium project: safer parsing, credential hygiene, lightweight documentation, dependency capture, and review-friendly project framing.
