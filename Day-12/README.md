# Telecom CDR & Billing Insights CLI Sample Project

This sample project implements the Telecom CDR & Billing Insights CLI described in the Python Core Capstone Workbook.

## Architecture

Package: `telecom_cli`

Modules:
- `telecom_cli/main.py` - CLI entry point and orchestration
- `telecom_cli/config.py` - rate table and default thresholds
- `telecom_cli/io_utils.py` - file loading, parsing, and report serialization
- `telecom_cli/models.py` - subscriber and CDR data models
- `telecom_cli/rating.py` - call rating logic
- `telecom_cli/fraud.py` - fraud detection rules
- `telecom_cli/reporting.py` - report assembly and console summary

## Usage

From the workspace root:

```powershell
python -m telecom_cli.main \
  --subscribers sample_data/subscribers.json \
  --cdrs sample_data/cdrs.csv \
  --output-report sample_data/report.json
```

Optional threshold override:

```powershell
python -m telecom_cli.main --subscribers sample_data/subscribers.json --cdrs sample_data/cdrs.csv --output-report sample_data/report.json --fraud-duration-threshold 3600
```

## Sample data

The `sample_data` folder includes example subscriber and CDR files.

## Notes

This sample follows the workbook expectations:
- separate modules for parsing, rating, fraud, reporting, and CLI orchestration
- logging for status and errors
- malformed rows are counted and do not crash the batch
- critical exit when malformed rows exceed 10%
- report output is JSON-indented and includes a console summary
