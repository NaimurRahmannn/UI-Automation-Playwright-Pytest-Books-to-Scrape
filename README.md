# Enterprise UI Automation Framework – Books to Scrape

A UI automation framework built with **Playwright** and **Pytest** that
validates the functionality, data consistency, UI elements, and navigation behavior of the
[Books to Scrape](https://books.toscrape.com/index.html) sandbox website. The framework runs
both locally and through GitHub Actions CI/CD, and produces both **HTML** and **Allure** test
reports.

**Live Allure report:** http://naimurrahmanlam.me/UI-Automation-Playwright-Pytest-Books-to-Scrape/

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation Guide](#installation-guide)
- [Environment Setup](#environment-setup)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Test Case Coverage](#test-case-coverage)
- [Report Generation Guide](#report-generation-guide)
  - [HTML Report Guide](#html-report-guide)
  - [Allure Report Guide](#allure-report-guide)
- [GitHub Actions Setup](#github-actions-setup)
- [Design Decisions](#design-decisions)
- [Known Limitations](#known-limitations)

---

## Project Overview

This project tests the main user-facing behavior of the Books to Scrape website. It separates page actions, helper methods, configuration, and test assertions so the tests stay clean and are easier to update when the website changes.

The suite covers five functional areas:

1. Homepage loads correctly with the expected URL, title, headings, and book list.
2. Randomly selected books open the correct details page.
3. Book title and price are consistent between the homepage and the details page.
4. All hyperlinks on the homepage return successful responses.
5. Product images render correctly with the required attributes across paginated pages.

---

## Features

- Page Object Model (POM) design with a shared `BasePage` for reusable behavior.
- Centralized configuration (URLs, sample sizes, timeouts) in a single `Config` class.
- Reliable synchronization using Playwright's auto-waiting and explicit waits — **no hardcoded sleeps**.
- Randomized test data (5 random books per run) for broader coverage.
- Broken-link checking via Playwright's request API for consistency with the browser context.
- Multi-page image validation that respects pagination and a configurable page cap.
- Dual reporting: pytest-html and Allure.
- GitHub Actions CI/CD that runs on every push and pull request and publishes the Allure
  report to GitHub Pages.
- Screenshots, videos, and traces captured for every test and uploaded as CI artifacts.

---

## Tech Stack

| Component         | Purpose                                  |
| ----------------- | ---------------------------------------- |
| Python 3.12       | Programming language                     |
| Playwright        | Browser automation                       |
| Pytest            | Test framework and runner                |
| pytest-playwright | Playwright fixtures for Pytest           |
| pytest-html       | Self-contained HTML report               |
| allure-pytest     | Allure results generation                |
| Allure CLI        | Renders Allure results into an HTML report |

---

## Installation Guide

### Prerequisites

- Python 3.12+
- Git
- (For viewing Allure locally) Java 17+ and the Allure command-line tool

### Steps

Clone the repository and enter the project directory:

```bash
git clone https://github.com/NaimurRahmannn/UI-Automation-Playwright-Pytest-Books-to-Scrape.git
cd UI-Automation-Playwright-Pytest-Books-to-Scrape
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

Install dependencies and browsers:

```bash
pip install -r requirements.txt
playwright install
# On Linux, also install the system libraries the browser needs:
playwright install-deps
```

---

## Environment Setup

No secrets or environment variables are required — the target site is public. All tunable
values live in `utils/config.py`:

| Setting                   | Default | Meaning                              |
| ------------------------- | ------- | ------------------------------------ |
| `BASE_URL`                | homepage URL | Target site entry point         |
| `EXPECTED_TITLE`          | page title  | Expected homepage `<title>`      |
| `RANDOM_BOOK_SAMPLE_SIZE` | 5       | Number of random books per test      |
| `MAX_IMAGE_PAGES`         | 5       | Max pages validated in image test    |
| `DEFAULT_TIMEOUT`         | 30000ms | Default element timeout              |
| `NAVIGATION_TIMEOUT`      | 30000ms | Default navigation timeout           |

---

## Running Tests

Run the entire suite (HTML and Allure results are generated automatically via `pytest.ini`):

```bash
pytest
```

Run a single test file:

```bash
pytest tests/test_homepage.py
```

Run tests by marker:

```bash
pytest -m homepage
pytest -m navigation
pytest -m consistency
pytest -m links
pytest -m images
```

Watch the browser while tests run:

```bash
pytest --headed
```

---

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── playwright.yml          # CI/CD pipeline
├── pages/                          # Page Object Model
│   ├── base_page.py                # Shared base class
│   ├── home_page.py                # Homepage interactions
│   └── book_details_page.py        # Details page interactions
├── tests/                          # Test cases
│   ├── test_homepage.py            # TC1
│   ├── test_book_navigation.py     # TC2
│   ├── test_data_consistency.py    # TC3
│   ├── test_broken_links.py        # TC4
│   └── test_product_images.py      # TC5
├── utils/
│   └── config.py                   # Central configuration
├── conftest.py                     # Pytest fixtures
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Dependencies
└── README.md
```

---

## Test Case Coverage

| ID  | Test Case                  | What it verifies                                                              |
| --- | -------------------------- | ---------------------------------------------------------------------------- |
| TC1 | Homepage Validation        | URL, title, all headings visible and non-empty, books section present and non-empty |
| TC2 | Random Book Navigation     | 5 random books open the correct details page; H1 matches; book info visible  |
| TC3 | Book Data Consistency      | Homepage title and price match the details page for 5 random books           |
| TC4 | Broken Link Validation     | All de-duplicated hyperlinks return HTTP 200                                  |
| TC5 | Product Image Validation   | Images visible with non-empty `src`/`alt` and `thumbnail` class, across pages |

---

## Report Generation Guide

Both report types are generated on every `pytest` run, configured in `pytest.ini`.

### HTML Report Guide

After running `pytest`, open the self-contained HTML report:

```bash
# Windows
start reports\html\report.html

# Linux
xdg-open reports/html/report.html
```

The report is self-contained (CSS/JS bundled inline) so it opens correctly anywhere,
including when downloaded from CI artifacts.

### Allure Report Guide

`pytest` writes raw Allure results to `reports/allure-results/`. To render them into a report,
the Allure CLI (which requires Java) is needed.

Quick local preview:

```bash
allure serve reports/allure-results
```

Generate a static report folder:

```bash
allure generate reports/allure-results --clean -o reports/allure-report
allure open reports/allure-report
```

The CI pipeline generates this same report automatically and publishes it to GitHub Pages
(see the live link at the top of this README), so a rendered Allure report is always available
without any local setup.

---

## GitHub Actions Setup

The workflow is defined in `.github/workflows/playwright.yml` and runs on every **push** and
**pull request**.

### Pipeline steps

1. Checkout the repository.
2. Set up Python 3.12.
3. Install Python dependencies.
4. Install Playwright browsers (with OS dependencies).
5. Create report directories.
6. Execute all tests.
7. Upload the HTML report as an artifact.
8. Upload the raw Allure results as an artifact.
9. Upload Playwright failure artifacts (screenshots, videos, traces) from `test-results/`.
10. Install the Allure CLI and generate the Allure HTML report.
11. Publish the Allure report to GitHub Pages.

### Enabling GitHub Pages (one-time)

In the repository: **Settings → Pages → Build and deployment → Source → GitHub Actions**.
After this is set, each pipeline run publishes the latest Allure report to the Pages URL.

---

## Design Decisions

**Page Object Model with a shared base class.**
Every page object inherits from `BasePage`, which holds the Playwright `page` instance and
common actions (navigation, title/URL getters). This removes duplicated logic and keeps each
page object focused on its own elements (OOP + DRY).

**Locators as named constants.**
Selectors are declared as class-level constants at the top of each page object, giving a single
source of truth. A site change requires editing one line rather than hunting through tests.

**Centralized configuration.**
URLs, sample sizes, and timeouts live in `utils/config.py` so no test hardcodes a value.

**No hardcoded waits.**
Synchronization relies on Playwright's built-in auto-waiting and explicit `wait_for(state=...)`
calls (for example, after pagination) instead of fixed `sleep` calls. This makes the suite both
faster and more reliable.

**Full title comparison via the `title` attribute.**
Homepage book titles are visually truncated (e.g. "A Light in the ..."), but the link's `title`
attribute holds the full title that the details-page `<h1>` displays. The navigation and
consistency tests read this attribute to compare titles accurately.

**Prices are normalized before comparison.**
Book prices are normalized before comparison by removing the currency symbol and converting the
value into a `Decimal`. This avoids false failures if the homepage and details page ever display
the same price with slightly different formatting, and uses `Decimal` rather than `float` to
avoid floating-point rounding issues with monetary values.

**Homepage validation separates "visible" from "non-empty".**
The homepage check splits two concerns into two tests: one asserts the book-list container
(`ol.row`) is visible, the other asserts the list is populated (`book count > 0`). Using a
specific container locator rather than a generic `section` means a failure points precisely at
which condition broke — a missing or hidden list versus an empty one.

**Broken-link checking uses Playwright's request API.**
Link validation uses `page.context.request.get(...)` rather than the Python `requests` library.
Initial attempts with `requests` failed in restricted network environments due to SSL
certificate verification errors and connection resets — not because the links were broken.
Using the browser context's own request client makes link checks consistent with the browser's
networking and avoids those environment-specific failures. `ignore_https_errors=True` is set
deliberately to tolerate certificate-handling differences between Python and the browser.

**Allure generated via the CLI in CI, not a Docker action.**
The pipeline installs the Allure CLI directly (with `setup-java`) and runs `allure generate`,
rather than relying on a Docker-based third-party action that proved unreliable to build on the
runner.

**Screenshots, videos, and traces captured on every run.**
Playwright is configured (via `--screenshot=on`, `--video=on`, and `--tracing=on` in
`pytest.ini`) to capture a screenshot, video, and trace for every test, whether it passes or
fails. These are written to `test-results/` and uploaded by CI as artifacts, giving a complete
visual record of every run rather than only failures.

---

## Known Limitations

**Random sampling.**
TC2 and TC3 select 5 random books per run, so each run exercises a different subset. This
broadens coverage over time but means a single run does not validate every book.

## Author

**[Naimur Rahman Lam](https://github.com/NaimurRahmannn)**