from pathlib import Path
import csv

from clean_csv import clean_csv


def test_clean_csv_trims_deduplicates_and_reports_invalid_rows(tmp_path: Path):
    source = tmp_path / "input.csv"
    output = tmp_path / "clean.csv"
    report = tmp_path / "report.json"
    source.write_text(
        "name,email,amount\n"
        " Alice , alice@example.com ,10\n"
        "Alice,alice@example.com,10\n"
        "Bob,bob@example.com,not-a-number\n"
        ",missing@example.com,5\n",
        encoding="utf-8",
    )

    result = clean_csv(source, output, report, required_columns=["name", "email"])

    assert result == {"input_rows": 4, "output_rows": 1, "duplicate_rows": 1, "invalid_rows": 2}
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [{"name": "Alice", "email": "alice@example.com", "amount": "10"}]

    report_text = report.read_text(encoding="utf-8")
    assert '"invalid_rows": 2' in report_text
