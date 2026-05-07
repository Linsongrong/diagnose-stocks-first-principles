#!/usr/bin/env python3
"""Audit a first-principles stock memo for required report scaffolding."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "## Verdict",
    "## Source Ledger",
    "## Evidence Map",
    "## Security Identity",
    "## Business First Principles",
    "## Economics And Cash Conversion",
    "## Moat And Competition",
    "## Management And Capital Allocation",
    "## Valuation Logic",
    "## Scenario Valuation",
    "## Critical Option Or Catalyst",
    "## Inversion And Failure Modes",
    "## Monitoring Checklist",
    "## Bottom Line",
    "## Important Caveat",
]

DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
LINK_RE = re.compile(r"https?://|]\(")
UNKNOWN_RE = re.compile(r"\bUnknown\b", re.IGNORECASE)
RISK_RE = re.compile(r"\b(risk|failure|bear case|impair|downside|wrong|unknown)\b", re.IGNORECASE)
ADVICE_CAVEAT_RE = re.compile(
    r"\bnot personalized financial advice\b|\bnot financial advice\b",
    re.IGNORECASE,
)
FACT_LABEL_RE = re.compile(r"\b(fact|inference|assumption|unknown)\b", re.IGNORECASE)
SOURCE_TYPE_RE = re.compile(r"\b(primary|secondary)\b", re.IGNORECASE)
SCENARIO_RE = re.compile(r"\b(downside|base|upside)\b", re.IGNORECASE)
EVIDENCE_LABEL_RE = re.compile(r"\b(fact|inference|assumption|unknown)\b", re.IGNORECASE)
SCENARIO_COLUMNS = [
    "scenario",
    "revenue",
    "gross margin",
    "fcf margin",
    "dilution",
    "terminal",
    "implied return",
    "key assumptions",
]
FINANCIAL_QUALITY_RE = re.compile(
    r"\b(stock-based compensation|sbc|dilution|share count|backlog|customer concentration|segment)\b",
    re.IGNORECASE,
)
PROHIBITED_CERTAINTY_RE = re.compile(
    r"\b(guaranteed|risk-free|cannot lose|can't lose|sure thing|must buy|must sell)\b",
    re.IGNORECASE,
)


def section_between(text: str, heading: str) -> str:
    if heading not in text:
        return ""
    section = text.split(heading, 1)[1]
    return section.split("\n## ", 1)[0]


def audit_text(text: str) -> list[str]:
    failures: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"Missing required heading: {heading}")

    if len(DATE_RE.findall(text)) < 2:
        failures.append("Expected at least two explicit YYYY-MM-DD dates.")

    if len(LINK_RE.findall(text)) < 2:
        failures.append("Expected at least two source links.")

    if not RISK_RE.search(text):
        failures.append("Expected explicit risk, failure-mode, or bear-case language.")

    if not ADVICE_CAVEAT_RE.search(text):
        failures.append("Expected a non-personalized-financial-advice caveat.")

    if not FACT_LABEL_RE.search(text):
        failures.append("Expected labels such as fact, inference, assumption, or unknown.")

    if PROHIBITED_CERTAINTY_RE.search(text):
        failures.append("Avoid guaranteed-return or unconditional trade-command language.")

    if "Analysis date:" not in text:
        failures.append("Missing analysis date line.")

    if "Market data timestamp:" not in text:
        failures.append("Missing market data timestamp line.")

    if "## Source Ledger" in text:
        source_section = section_between(text, "## Source Ledger")
        if "|" not in source_section:
            failures.append("Source Ledger should use a Markdown table.")
        if not DATE_RE.search(source_section):
            failures.append("Source Ledger should include dated sources.")
        if not SOURCE_TYPE_RE.search(source_section):
            failures.append("Source Ledger should label sources as Primary or Secondary.")
        if len(LINK_RE.findall(source_section)) < 2:
            failures.append("Source Ledger should include at least two source links.")

    if "## Evidence Map" in text:
        evidence_section = section_between(text, "## Evidence Map")
        if "|" not in evidence_section:
            failures.append("Evidence Map should use a Markdown table.")
        labels = set(label.lower() for label in EVIDENCE_LABEL_RE.findall(evidence_section))
        missing_labels = {"fact", "inference", "assumption", "unknown"} - labels
        if missing_labels:
            failures.append(
                "Evidence Map should include Fact, Inference, Assumption, and Unknown labels."
            )

    if "## Economics And Cash Conversion" in text:
        economics_section = section_between(text, "## Economics And Cash Conversion")
        if not FINANCIAL_QUALITY_RE.search(economics_section):
            failures.append(
                "Economics section should discuss dilution/SBC, segment quality, backlog, or customer concentration."
            )

    if "## Valuation Logic" in text:
        valuation_section = section_between(text, "## Valuation Logic")
        if len(SCENARIO_RE.findall(valuation_section)) < 3:
            failures.append("Valuation Logic should include downside, base, and upside scenarios.")

    if "## Scenario Valuation" in text:
        scenario_section = section_between(text, "## Scenario Valuation")
        lower_scenario = scenario_section.lower()
        if "|" not in scenario_section:
            failures.append("Scenario Valuation should use a Markdown table.")
        missing_columns = [column for column in SCENARIO_COLUMNS if column not in lower_scenario]
        if missing_columns:
            failures.append(
                "Scenario Valuation table is missing required column(s): "
                + ", ".join(missing_columns)
            )
        scenario_names = set(name.lower() for name in SCENARIO_RE.findall(scenario_section))
        if {"downside", "base", "upside"} - scenario_names:
            failures.append("Scenario Valuation should include Downside, Base, and Upside rows.")

    if "## Critical Option Or Catalyst" in text:
        option_section = section_between(text, "## Critical Option Or Catalyst")
        if len(option_section.strip()) < 80:
            failures.append("Critical Option Or Catalyst section is too thin.")

    if "## Inversion And Failure Modes" in text:
        inversion_section = section_between(text, "## Inversion And Failure Modes")
        if len(inversion_section.strip()) < 80:
            failures.append("Inversion And Failure Modes section is too thin.")

    if UNKNOWN_RE.search(text) and not re.search(r"\b(why|because|matter|unavailable)\b", text, re.IGNORECASE):
        failures.append("Unknowns should explain why they matter or why they are unavailable.")

    return failures


def run_self_test() -> int:
    valid = """# First-Principles Stock Diagnosis: Example Co (EXM.US)

Analysis date: 2026-05-07
Market data timestamp: 2026-05-07 15:30 America/New_York

## Verdict

Watchlist only. Fact: current cash conversion is not yet strong enough.

## Source Ledger

| Date | Source | Type | Key Fact |
| --- | --- | --- | --- |
| 2026-05-01 | [Annual report](https://example.com/annual) | Primary | Revenue grew. |
| 2026-05-07 | [Quote](https://example.com/quote) | Secondary | Price snapshot. |

## Evidence Map

| Label | Item | Implication | Confidence |
| --- | --- | --- | --- |
| Fact | Revenue grew in 2026-05-01 filing. | Demand is improving. | High |
| Inference | Switching costs may support retention. | Moat may be real. | Medium |
| Assumption | FCF margin can reach 12%. | Valuation depends on this. | Medium |
| Unknown | Customer retention matters because it could disprove the thesis. | Monitor cohorts. | Low |

## Security Identity
Common stock.

## Business First Principles
Customer job, revenue engine, and reinvestment need are stated.

## Economics And Cash Conversion
Operating cash flow and free cash flow are compared. Stock-based compensation, dilution, segment quality, backlog conversion, and customer concentration are reviewed.

## Moat And Competition
Switching costs are the alleged moat.

## Management And Capital Allocation
Management has repurchased shares and issued debt.

## Valuation Logic
Downside, base, and upside scenarios are linked to assumptions.

## Scenario Valuation

| Scenario | Revenue | Gross Margin | FCF Margin | Dilution / Share Count | Terminal Method | Implied Return / Gap | Key Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Downside | $800M | 35% | 2% | 5% dilution | EV/revenue | Negative gap | Growth slows. |
| Base | $1.2B | 42% | 8% | 3% dilution | FCF yield | Mid return | Retention holds. |
| Upside | $1.8B | 48% | 12% | 1% dilution | FCF yield | Strong return | Moat strengthens. |

## Critical Option Or Catalyst
The critical catalyst is a new product launch. Technical feasibility, demand evidence, unit economics, capital required, timing risk, competitive response, and probability-changing evidence are discussed.

## Inversion And Failure Modes
The bear case is that growth slows, margins compress, and the company refinances debt on worse terms. Unknown customer retention matters because it could disprove the switching-cost thesis and permanently impair value.

## Monitoring Checklist
- Cash conversion
- Share count

## Bottom Line
The diagnosis depends on cash conversion improving.

## Important Caveat
This memo is analytical support, not personalized financial advice.
"""

    invalid = """# Memo

## Verdict
Buy.
"""

    dangerous = valid.replace(
        "Watchlist only. Fact: current cash conversion is not yet strong enough.",
        "This is guaranteed and investors must buy. Fact: current cash conversion is not yet strong enough.",
    )

    weak_valuation = valid.replace(
        "Downside, base, and upside scenarios are linked to assumptions.",
        "Only the base scenario is described.",
    )

    weak_scenario_table = valid.replace(
        "| Scenario | Revenue | Gross Margin | FCF Margin | Dilution / Share Count | Terminal Method | Implied Return / Gap | Key Assumptions |",
        "| Scenario | Revenue | Terminal Method | Key Assumptions |",
    )

    valid_failures = audit_text(valid)
    invalid_failures = audit_text(invalid)
    dangerous_failures = audit_text(dangerous)
    weak_valuation_failures = audit_text(weak_valuation)
    weak_scenario_table_failures = audit_text(weak_scenario_table)

    if valid_failures:
        print("Self-test valid memo failed:", file=sys.stderr)
        for failure in valid_failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    if not invalid_failures:
        print("Self-test invalid memo unexpectedly passed.", file=sys.stderr)
        return 1

    if not any("guaranteed" in failure or "trade-command" in failure for failure in dangerous_failures):
        print("Self-test dangerous memo did not trigger certainty guardrail.", file=sys.stderr)
        return 1

    if not any("downside, base, and upside" in failure for failure in weak_valuation_failures):
        print("Self-test weak valuation memo did not trigger scenario guardrail.", file=sys.stderr)
        return 1

    if not any("Scenario Valuation table is missing" in failure for failure in weak_scenario_table_failures):
        print("Self-test weak scenario table did not trigger required-column guardrail.", file=sys.stderr)
        return 1

    print("Self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a first-principles stock memo.")
    parser.add_argument("memo", nargs="?", help="Path to a Markdown memo.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in tests.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.memo:
        parser.error("memo is required unless --self-test is provided")

    path = Path(args.memo)
    text = path.read_text(encoding="utf-8")
    failures = audit_text(text)

    if failures:
        print("Audit failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
