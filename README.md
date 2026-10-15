# Automation Exercise Hybrid QA Framework

Python automation for Automation Exercise using requests, Selenium, pytest, API clients, and page objects. Hybrid tests create an account through the API, exercise checkout in the browser, and delete the account through fixture cleanup.

## Setup

Install Python 3.13 and Google Chrome, then run from the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead. Selenium Manager resolves the browser driver; internet access is required for driver downloads and the practice site. Firefox is also supported if installed.

## Run tests

```bash
python -m pytest tests/api -v
python -m pytest tests/ui -v
python -m pytest tests/e2e -v
python -m pytest -v
```

You can select suites with `-m api`, `-m ui`, or `-m e2e`. Browsers run headlessly by default. Use `--headed` to see the browser, or `--browser firefox` to select Firefox.

The default target is `https://automationexercise.com`. Override it through the `AUTOMATION_EXERCISE_BASE_URL` environment variable. Tests generate unique account data and clean up API-created accounts. These are live integration tests, so website availability and network connectivity affect results.

## Reports and screenshots

Every run writes a self-contained HTML report to `reports/report.html`; open it in a browser. Failed browser tests capture PNG files in `screenshots/` and embed them in the HTML report. Capture runs before browser cleanup for setup or test failures when a browser is available; browser startup failures and teardown failures may have no screenshot. Screenshot capture errors produce a warning without hiding the original test failure.

Each run replaces the default report. To keep a separate report:

```bash
python -m pytest tests/api --html=reports/api.html --junitxml=reports/api.xml
```

Generated reports, screenshots, and local environment files are ignored by Git.

## GitHub Actions

`.github/workflows/tests.yml` runs on pushes and pull requests to `main`, and can be started manually from the Actions tab. Two independent jobs run API tests and headless Chrome UI/hybrid tests using Python 3.13. Each uploads HTML/JUnit reports and available screenshots, including after test failures, and retains artifacts for 14 days.

Push this project to a GitHub repository with a `main` branch. Open **Actions → Automation tests**, select a run, and download `api-test-results` or `browser-test-results` under **Artifacts**. Extract the download and open `reports/report.html`. A failing pytest command keeps its job failed even though the upload step still runs.

The workflow needs no account secrets: tests create temporary accounts through the public practice API. A hosted workflow run is needed to confirm behavior on GitHub's runners.

## Project layout

- `api/`: shared HTTP client and user/product API wrappers.
- `pages/`: Selenium page objects and shared element waits.
- `tests/api/`: API contract and account lifecycle tests.
- `tests/ui/`: browser behavior tests.
- `tests/e2e/`: hybrid purchase workflow.
- `utils/`: configuration and generated test data.
- `conftest.py`: browser/API fixtures, cleanup, and failure screenshots.
