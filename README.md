# CSV Clean & Report Kit

Small, local-first Python utility for turning a messy CSV into a clean, deduplicated file plus a machine-readable processing report.

## What it does

- Trims whitespace from every field.
- Drops rows missing required columns.
- Validates selected numeric columns.
- Removes duplicate rows after normalization.
- Writes a UTF-8 cleaned CSV.
- Writes a JSON report with input, output, duplicate, and invalid row counts.
- Uses only Python's standard library; no subscription or API required.

## Run

```bash
python clean_csv.py input.csv output.csv \
  --report cleaning_report.json \
  --required name email \
  --numeric amount
```

Arguments:

- `input.csv`: source file.
- `output.csv`: cleaned result.
- `--report`: JSON report path; defaults to `cleaning_report.json`.
- `--required`: columns that must not be empty.
- `--numeric`: columns that must contain valid numbers.

## Example result

The included `sample_input.csv` contains four data rows: one normalized duplicate and two invalid rows. Running the command above produces one retained row and this report:

```json
{
  "input_rows": 4,
  "output_rows": 1,
  "duplicate_rows": 1,
  "invalid_rows": 2
}
```

## Service offer built from this MVP

**Offer:** "Saya membersihkan dan merapikan file Excel/CSV Anda menjadi file siap pakai, lengkap dengan laporan baris invalid dan duplikat."

**Starter — Rp150.000**

- 1 file, up to 5,000 rows
- trim, duplicate removal, required-field checks
- cleaned CSV/XLSX output
- 1 revision
- delivery target: 24 hours after receiving the file and rules

**Standard — Rp350.000**

- up to 3 files or 25,000 rows total
- custom validation rules and numeric/date checks
- cleaned output plus JSON/Excel summary
- 2 revisions

**Automation — Rp750.000+**

- reusable Python script configured for the client's recurring file format
- README and sample input/output
- error report and local run instructions
- exact quote after a small sample is reviewed

These prices are hypotheses for market testing, not guaranteed market rates.

## Portfolio / contact

This repository is a working sample, not a claim of prior client work. For a small cleanup or repeatable automation request, share a redacted sample, expected columns, approximate row count, and desired output format through my freelance profile.

## Safe scope

Do not handle passwords, payment data, private credentials, or restricted personal data unless the client has a lawful and secure transfer process. Do not promise perfect accuracy before inspecting a sample.
