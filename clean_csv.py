#!/usr/bin/env python3
"""Clean a CSV file, remove duplicate rows, validate required fields, and write a report."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


def clean_csv(
    input_path: str | Path,
    output_path: str | Path,
    report_path: str | Path,
    *,
    required_columns: Iterable[str] = (),
    numeric_columns: Iterable[str] = (),
) -> dict[str, int]:
    """Clean *input_path* and return row-level processing counts.

    Values are whitespace-trimmed. Rows missing required values or containing
    non-numeric values in ``numeric_columns`` are excluded. Duplicate rows are
    counted after normalization and only the first occurrence is retained.
    """
    input_path, output_path, report_path = map(Path, (input_path, output_path, report_path))
    required = tuple(required_columns)
    numeric = tuple(numeric_columns)

    with input_path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no header row")
        headers = list(reader.fieldnames)
        missing_columns = [column for column in (*required, *numeric) if column not in headers]
        if missing_columns:
            raise ValueError(f"Columns not found in input: {', '.join(missing_columns)}")

        kept: list[dict[str, str]] = []
        seen: set[tuple[str, ...]] = set()
        duplicate_rows = invalid_rows = input_rows = 0
        for raw_row in reader:
            input_rows += 1
            row = {header: (raw_row.get(header) or "").strip() for header in headers}
            if any(not row[column] for column in required):
                invalid_rows += 1
                continue
            try:
                for column in numeric:
                    float(row[column])
            except (TypeError, ValueError):
                invalid_rows += 1
                continue
            key = tuple(row[header] for header in headers)
            if key in seen:
                duplicate_rows += 1
                continue
            seen.add(key)
            kept.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=headers)
        writer.writeheader()
        writer.writerows(kept)

    result = {
        "input_rows": input_rows,
        "output_rows": len(kept),
        "duplicate_rows": duplicate_rows,
        "invalid_rows": invalid_rows,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean and validate a CSV file.")
    parser.add_argument("input", type=Path, help="Input UTF-8 CSV")
    parser.add_argument("output", type=Path, help="Cleaned output CSV")
    parser.add_argument("--report", type=Path, default=Path("cleaning_report.json"))
    parser.add_argument("--required", nargs="*", default=[], help="Columns that must be non-empty")
    parser.add_argument("--numeric", nargs="*", default=[], help="Columns that must contain numbers")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = clean_csv(
            args.input,
            args.output,
            args.report,
            required_columns=args.required,
            numeric_columns=args.numeric,
        )
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
