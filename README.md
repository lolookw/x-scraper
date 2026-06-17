# X Scraper Portfolio Demo

This project is a small Selenium-based portfolio demo for collecting public X profile data from configured searches, filtering the results, and opening selected profiles for manual review. It is intended for learning and portfolio review, not bulk outreach or platform abuse.

## Quick path

1. Create a virtual environment and install dependencies.
2. Copy `config.example.json` to `config.json` and fill in local credentials.
3. Run the GUI with `python interface.py`, or run the scraper flow with `python main.py`.
4. Review generated output files locally; do not commit credentials or generated data.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Chrome must be installed because Selenium opens a Chrome browser session.

## Configuration

Copy the example file and edit the private copy only:

```bash
cp config.example.json config.json
```

| Field | Purpose |
|-------|---------|
| `username`, `mail`, `password` | Primary X login details used locally by Selenium. |
| `username2`, `mail2`, `password2` | Optional fallback account fields kept for compatibility with the original script. |
| `busquedas` | Search definitions with query text and scroll counts. |

`config.json` is ignored by Git because it contains secrets.

If real credentials were ever committed or pushed, rotate them before sharing
the repository and remove them from Git history if the project will be public.

## Usage

### GUI

```bash
python interface.py
```

The GUI saves `config.json`, executes `main.py`, and can launch `usuarios.py` for manual profile review.

### Scraper flow

```bash
python main.py
```

`main.py` logs in, collects public profile data for configured searches, writes local backups, and filters collected users. Direct-message automation remains out of the default path.

### Manual profile review

```bash
python usuarios.py
```

This opens filtered X profiles one at a time so a human can review each account manually.

## Outputs

Generated files are local-only and ignored by Git:

- `backups/` — raw and intermediate scrape backups.
- `users_list.txt` — collected user records.
- `ordered+filtered_users.txt` — filtered user records ordered by simple heuristic tiers.
- `checked_users_list.txt` — optional manually curated usernames.

## Ethics and limitations

Use this only with accounts and data you are allowed to access. Respect X terms, rate limits, robots/platform restrictions, and privacy expectations. The filtering logic is heuristic and can be wrong; manually verify any result before acting on it. Do not use this project for spam, harassment, credential collection, or evading platform controls.
