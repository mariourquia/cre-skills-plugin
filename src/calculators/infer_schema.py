#!/usr/bin/env python3
"""
Document-to-Database: Schema Inference
======================================
Infers a column schema (type, nullability, detected unit, per-column
confidence) and a grain guess from an unknown tabular token stream -- the
``doc_type: auto`` path, used when an extracted table arrives without a known
shape. Deterministic: type inference is by value sampling with fixed rules
(integer / numeric / date / period / boolean / text), never a heuristic that
varies run to run.

Pure calculate_infer_schema(dict)->dict; selectors in --json.

Used by: document-to-database

Usage:
    python3 src/calculators/infer_schema.py --json '{
        "rows": [{"unit":"101","rent":"1,700.00","start":"2024-01-01","occupied":true},
                 {"unit":"102","rent":"1800","start":"2024-03-01","occupied":false}]
    }'

Output: JSON {columns, row_count, grain, overall_confidence}.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PERIOD_RE = re.compile(r"^\d{4}-\d{2}$")
_MONEY_RE = re.compile(r"^\(?-?\$?[\d,]+(\.\d+)?\)?$")


def calculate_infer_schema(inputs: dict) -> dict:
    rows = inputs.get("rows") or inputs.get("lines") or inputs.get("tokens") or []
    if not isinstance(rows, list) or not rows:
        return {"error": "provide a non-empty 'rows' (or 'lines'/'tokens') array of objects"}

    # Stable column order: first-seen across rows.
    col_order: list = []
    for r in rows:
        if isinstance(r, dict):
            for k in r.keys():
                if k not in col_order:
                    col_order.append(k)

    columns = []
    conf_sum = 0.0
    for col in col_order:
        values = [r.get(col) for r in rows if isinstance(r, dict)]
        present = [v for v in values if v not in (None, "")]
        nullable = len(present) < len(values)
        col_type, unit, conf = _infer_column(present)
        conf_sum += conf
        columns.append({
            "name": col,
            "type": col_type,
            "nullable": nullable,
            "unit": unit,
            "populated": len(present),
            "total": len(values),
            "confidence": round(conf, 4),
        })

    overall = round(conf_sum / len(col_order), 4) if col_order else 0.0
    return {
        "columns": columns,
        "row_count": len(rows),
        "grain": "one row per record (flat tabular grain)",
        "overall_confidence": overall,
    }


def _infer_column(values: list) -> tuple:
    """Return (type, unit, confidence). Confidence = fraction of values
    consistent with the dominant inferred type."""
    if not values:
        return ("text", None, 0.4)

    n = len(values)
    counts = {"boolean": 0, "period": 0, "date": 0, "integer": 0, "numeric": 0, "money": 0, "text": 0}
    for v in values:
        counts[_value_kind(v)] += 1

    # Resolve to a column type with precedence and unit detection.
    if counts["boolean"] == n:
        return ("boolean", None, 1.0)
    if counts["period"] == n:
        return ("period", "YYYY-MM", 1.0)
    if counts["date"] == n:
        return ("date", None, 1.0)
    money = counts["money"]
    numeric = counts["numeric"] + counts["integer"] + money
    if money >= 1 and numeric == n:
        return ("numeric", "usd", round(numeric / n, 4))
    if counts["integer"] == n:
        return ("integer", None, 1.0)
    if numeric == n:
        return ("numeric", None, round(numeric / n, 4))
    # mixed -> text, confidence = share that are plain text
    return ("text", None, round(counts["text"] / n, 4) if counts["text"] else 0.5)


def _value_kind(v: Any) -> str:
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "numeric"
    s = str(v).strip()
    if s.lower() in ("true", "false", "yes", "no", "y", "n"):
        return "boolean"
    if _PERIOD_RE.match(s):
        return "period"
    if _DATE_RE.match(s):
        return "date"
    if "$" in s or ("," in s and _MONEY_RE.match(s)) or (s.startswith("(") and s.endswith(")")):
        return "money" if _MONEY_RE.match(s) else "text"
    try:
        f = float(s)
        return "integer" if f == int(f) and "." not in s else "numeric"
    except (TypeError, ValueError):
        return "text"


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Schema Inference")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_infer_schema(inputs), indent=2))


if __name__ == "__main__":
    main()
