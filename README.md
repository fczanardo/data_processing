# data_processing

Arturic Industries Quarter metrics.

## Overview

This project extracts and processes quarterly output metrics for Arturic Industries. It unpacks a compressed archive (`quarterly_output.tar.gz`) and makes the data available for downstream analysis.

## Project Structure

```
data_processing/
├── README.md
├── requirements.txt
└── app/
    ├── main.py          # Entry point — runs the extraction pipeline
    └── extraction.py    # Core logic for extracting the quarterly archive
```

## Requirements

- Python 3.10+
- pandas >= 3.0.2

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the data extraction from the project root:

```bash
python app/main.py
```

This will extract the contents of `../file/quarterly_output.tar.gz` into a local `./file/` directory.

## How It Works

1. `main.py` calls `extraction.extract_data()`.
2. `extract_data()` calls `extract_quarterly_output()`, which locates the archive at `../../file/quarterly_output.tar.gz` relative to the `app/` directory.
3. The archive is extracted to `./file/` (created automatically if it does not exist).

## Author

**Fabio Zanardo** — fczanardo@gmail.com
