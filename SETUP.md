# Setup: Chapter 0, kept up to date

This file follows Chapter 0 of the book. When installers or versions change,
the newest fixes are added at the top of the *Latest notes* section.

## Latest notes

- 2027 (first edition): the book was checked with Python 3.13 and the package
  versions of `requirements.txt`.

## The steps

| Step | Check |
|---|---|
| 0.1 Check your computer: system, 3 GB free, administrator rights | |
| 0.2 Open a terminal | the prompt appears |
| 0.3 Install Python from python.org (Windows: tick *Add python.exe to PATH*; macOS: run *Install Certificates*) | `python --version` (Windows) or `python3 --version` shows 3.11 or later |
| 0.4 Install VS Code, then the Python and Jupyter extensions | `print("Hello")` runs in a notebook |
| 0.5 Download this repository to `C:\scraping` or `~/scraping` | the folder contains `run_site.py` |
| 0.6 `python -m venv .venv`, activate, `python -m pip install -r requirements.txt` | the prompt starts with `(.venv)` |
| 0.7 `python -m playwright install chromium`; Google Chrome for Selenium | `python chapters/ch00/examples/test_playwright.py` and `test_selenium.py` print a title |
| 0.8 `python run_site.py` in its own terminal | <http://localhost:8000> shows *Welcome to Practice Ground* |
| 0.9 `python check_setup.py` | last line: **All set: you are ready for Chapter 1** |

## Tell me what you see

| What you see | Cause and fix |
|---|---|
| `python is not recognized` (Windows) | Python not on PATH: rerun the installer, *Modify*, tick *Add Python to environment variables*; or turn off the Store aliases for `python.exe` (*Manage app execution aliases*). |
| `command not found: python` (macOS, Linux) | type `python3` |
| `pip is not recognized` | type `python -m pip` |
| *running scripts is disabled* (PowerShell) | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again |
| `CERTIFICATE_VERIFY_FAILED` | macOS: run *Install Certificates.command*; company network: install from home or use Codespaces |
| `No module named ...` | activate the virtual environment in this terminal |
| `Address already in use` | the site already runs elsewhere; close it or use `python run_site.py --port 8001` |
| *This site can't be reached* | start the site with `python run_site.py` |
| `Executable doesn't exist` (Playwright) | `python -m playwright install chromium` |
| `NoSuchDriverException` (Selenium) | install Google Chrome, or use Firefox |
| Selenium: Chrome crashes at start on Linux, in a container or as the root user | add `options.add_argument("--no-sandbox")` next to `--headless=new` |
| No administrator rights | use GitHub Codespaces (below) |

## No installation: GitHub Codespaces

1. On the repository page: **Code**, **Codespaces**, **Create codespace on main**.
2. Wait for *Setup finished* in the terminal (the file `.devcontainer/devcontainer.json`
   installs Python's packages, Playwright's Chromium and Google Chrome for Selenium).
3. `python run_site.py`; click *Open in Browser* to see the site.
4. Second terminal: `python check_setup.py`.
5. Stop the codespace when you finish (**Code**, **Codespaces**, **...**, **Stop codespace**).
