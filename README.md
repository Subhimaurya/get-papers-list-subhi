
# get-papers-list

A simple command-line tool to fetch research papers from PubMed authored by individuals affiliated with pharmaceutical or biotech companies.

## Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Clone this repository or unzip the downloaded ZIP
3. Run `poetry install` inside the project folder

## Usage

```bash
poetry run get-papers-list "cancer therapy"
poetry run get-papers-list "diabetes" -f output.csv
poetry run get-papers-list "covid vaccine" -d
```

## Notes

I assume non-academic affiliations are those **not** containing words like "university", "institute", "lab", "hospital", etc.

## 📦 Published on TestPyPI

👉 [View on TestPyPI](https://test.pypi.org/project/get-papers-list-subhi/)

---

## 🚀 Installation

You can install this tool directly from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple get-papers-list-subhi
