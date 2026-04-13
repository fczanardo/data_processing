# data_processing

Arturic Industries Quarter metrics.

## Overview

This project extracts, transforms, and validates quarterly output metrics for Arturic Industries. It unpacks a compressed `.tar.gz` archive, parses data from multiple file formats (CSV, MDR, TXT), applies validation rules and column filters, writes the consolidated result to `output/result.txt`, and generates detailed error reports.

The architecture follows **Clean Architecture**, **SOLID** principles, and the **ETL Pipeline** design pattern.

## Project Structure

```
data_processing/
├── README.md
├── requirements.txt
├── output/                            # Generated output and error reports
└── app/
    ├── main.py                        # Entry point — configures logging and runs the pipeline
    ├── config.py                      # Loads and validates environment variables
    ├── exceptions.py                  # Custom domain exception hierarchy
    ├── domain/
    │   └── etl.py                     # Abstract interfaces: Extractor, Transformer, Loader, ETLPipeline
    ├── use_cases/
    │   └── run_pipeline.py            # Assembles and executes the ETL pipeline
    └── infrastructure/
        ├── extractor.py               # TarGzExtractor — extracts .tar.gz archives
        ├── parsers.py                 # SAParser (csv), MDRParser (mdr), WBParser (txt)
        ├── transformer.py             # QuarterlyDataTransformer — parses, validates and filters data
        └── loader.py                  # DataLoader — writes results and error reports to output/
```

## Architecture

### ETL Pipeline Pattern

The pipeline is composed of three abstract stages defined in `domain/etl.py`:

| Stage | Interface | Implementation |
|---|---|---|
| Extract | `Extractor` | `TarGzExtractor` |
| Transform | `Transformer` | `QuarterlyDataTransformer` |
| Load | `Loader` | `DataLoader` |

`ETLPipeline.run()` orchestrates: `extract()` → `transform()` → `load()`.

Each stage depends on an abstraction — following the **Dependency Inversion Principle**. Swapping an implementation (e.g. `TarGzExtractor` → `ZipExtractor`) requires only changing `run_pipeline.py`.

### Supported File Formats

| Extension | Parser | Description |
|---|---|---|
| `.csv` | `SAParser` | Comma-separated session data |
| `.mdr` | `MDRParser` | JSON-structured session entries |
| `.txt` | `WBParser` | Line-delimited metadata + entries |

All parsers normalize data into a standard schema: `SOURCE_FILE`, `SESSION`, `PROCESSOR`, `DEPARTMENT`, `TIMESTAMP`, `REF`, `BIN`, `VALUE`, `CATEGORY`.

### Validation Rules

| Column | Rule |
|---|---|
| `PROCESSOR` | Must be one of: `James.L`, `Nora.K`, `Arthur.B`, `Lena.P`, `Felix.G`, `Dr.Voss`, `Clara.M` |
| `DEPARTMENT` | Must be one of: `MDR`, `SA`, `WB` |
| `BIN` | Must be one of: `GR`, `BL`, `AX`, `SP` |
| `CATEGORY` | Must be one of: `alpha`, `beta`, `gamma`, `delta` |
| `VALUE` | Must be a positive number (zero and negative values rejected) |
| `TIMESTAMP` | Must fall within Q4 2025 (`2025-10-01` to `2025-12-31`) |

### Exception Hierarchy

```
DataProcessingError
├── ConfigurationError     # missing/invalid env var
├── ArchiveNotFoundError   # archive file not found
└── ExtractionError        # failure during extraction
```

### Output Files

All files are written to the `output/` directory:

| File | Content |
|---|---|
| `result.txt` | Final consolidated VALUE sum |
| `INVALID_parse_warnings.txt` | Files that failed to parse (malformed JSON, bad CSV lines, etc.) |
| `INVALID_values.txt` | Rows with non-numeric VALUE (e.g. `100.01A`) |
| `INVALID_filtered_out.txt` | Rows rejected by column validation rules |

## Requirements

- Python 3.10+
- pandas

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

| Variable | Required | Description | Example |
|---|---|---|---|
| `QUARTERLY_ARCHIVE_PATH` | **Yes** | Absolute path to the `.tar.gz` archive to extract | `/data/file/quarterly_output.tar.gz` |
| `EXTRACTION_DESTINATION` | **Yes** | Directory where files will be extracted and read from | `./temp/fileExtracted` |

Set them before running:

```bash
# Linux / macOS
export QUARTERLY_ARCHIVE_PATH="/path/to/quarterly_output.tar.gz"
export EXTRACTION_DESTINATION="./temp/fileExtracted"
```

```powershell
# Windows (PowerShell)
$env:QUARTERLY_ARCHIVE_PATH = "C:\path\to\quarterly_output.tar.gz"
$env:EXTRACTION_DESTINATION = ".\temp\fileExtracted"
```

When running via VS Code, these variables are pre-configured in `.vscode/launch.json`.

## Usage

Run the pipeline from the project root:

```bash
python app/main.py
```

## How It Works

1. `main.py` configures logging and calls `run_pipeline.execute()`.
2. `run_pipeline` assembles `ETLPipeline` with `TarGzExtractor`, `QuarterlyDataTransformer`, and `DataLoader`.
3. **Extract** — `TarGzExtractor` validates the archive exists and extracts it to `EXTRACTION_DESTINATION`.
4. **Transform** — `QuarterlyDataTransformer` reads all `.csv`, `.mdr`, and `.txt` files, normalises the `TIMESTAMP` column, detects non-numeric `VALUE` entries, and applies all column filters.
5. **Load** — `DataLoader` writes the consolidated sum to `output/result.txt` and saves error reports for parse warnings, invalid values, and filtered-out rows.

## Author

**Fabio Zanardo** — fczanardo@gmail.com

