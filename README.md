# data_processing

Arturic Industries Quarter metrics.

## Overview

This project extracts and processes quarterly output metrics for Arturic Industries. It unpacks a compressed archive (`quarterly_output.tar.gz`) and makes the data available for downstream analysis.

The architecture follows **Clean Architecture**, **SOLID** principles, and the **ETL Pipeline** design pattern.

## Project Structure

```
data_processing/
├── README.md
├── requirements.txt
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
        ├── transformer.py             # QuarterlyDataTransformer — transforms extracted data
        └── loader.py                  # DataLoader — loads transformed data to destination
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

Each stage depends on an abstraction (interface), not a concrete class — following the **Dependency Inversion Principle**. To swap implementations (e.g. replace `TarGzExtractor` with a `ZipExtractor`), only `run_pipeline.py` needs to change.

### Exception Hierarchy

```
DataProcessingError
├── ConfigurationError     # missing/invalid env var
├── ArchiveNotFoundError   # archive file not found
└── ExtractionError        # failure during extraction
```

### Logging

Logging is configured in `main.py` at `INFO` level. A success message is emitted after extraction:

```
INFO - Extraction completed successfully: /path/to/archive.tar.gz → /path/to/destination
```

## Requirements

- Python 3.10+
- pandas >= 3.0.2

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

| Variable | Required | Description | Example |
|---|---|---|---|
| `QUARTERLY_ARCHIVE_PATH` | **Yes** | Absolute path to the `.tar.gz` archive to extract | `/data/file/quarterly_output.tar.gz` |
| `EXTRACTION_DESTINATION` | No | Directory where files will be extracted (default: `./file`) | `./temp/fileExtracted` |

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

Run the data extraction from the project root:

```bash
python app/main.py
```

## How It Works

1. `main.py` configures logging and calls `run_pipeline.execute()`.
2. `run_pipeline` assembles the `ETLPipeline` with concrete implementations from `infrastructure/`.
3. `ETLPipeline.run()` calls `TarGzExtractor.extract()` — validates the archive exists, extracts it to the destination, and logs success.
4. `QuarterlyDataTransformer.transform()` processes the extracted files. // TODO
5. `DataLoader.load()` persists the result. // TODO

## Author

**Fabio Zanardo** — fczanardo@gmail.com

