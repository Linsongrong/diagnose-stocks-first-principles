# Markdown Stock Memo Template

Use this template when the user asks for a saved report or formal memo. Keep the structure stable so `scripts/audit_stock_memo.py` can check it.

```markdown
# First-Principles Stock Diagnosis: <Company> (<Ticker.Exchange>)

Analysis date: <YYYY-MM-DD>
Market data timestamp: <YYYY-MM-DD HH:MM timezone>
Currency: <currency>
User context: <cost basis, holding period, portfolio role, or "not provided">

## Verdict

<One plain classification plus 3-5 lines of reasoning.>

## Source Ledger

| Date | Source | Type | Key Fact |
| --- | --- | --- | --- |
| <YYYY-MM-DD> | [Company filing](https://...) | Primary | <fact> |

## Evidence Map

| Label | Item | Implication | Confidence |
| --- | --- | --- | --- |
| Fact | <verified fact> | <why it matters> | High |
| Inference | <reasoned conclusion> | <what it implies> | Medium |
| Assumption | <model assumption> | <what breaks if wrong> | Medium |
| Unknown | <missing evidence> | <why it matters> | Low |

## Security Identity

- Ticker / exchange:
- Share class:
- Market cap:
- Enterprise value:
- Net cash/debt:
- Shares outstanding and dilution notes:

## Business First Principles

- Customer job:
- Revenue engine:
- Unit economics:
- Reinvestment need:
- Key constraint:

## Economics And Cash Conversion

- Revenue and margin trend:
- Operating cash flow:
- Free cash flow:
- Working capital:
- Stock-based compensation and dilution:
- Segment quality / backlog conversion:
- Customer concentration:
- ROIC or proxy:
- Accounting quality:

## Moat And Competition

- Moat source:
- Evidence:
- Direct competitors:
- Substitutes:
- Price/value wedge:
- Competitive attack path:
- Durability:

## Management And Capital Allocation

- Incentives:
- Reinvestment:
- Dividends / buybacks / issuance:
- Governance concerns:

## Valuation Logic

- Current valuation:
- What must be true:
- Margin of safety:

## Scenario Valuation

| Scenario | Revenue | Gross Margin | FCF Margin | Dilution / Share Count | Terminal Method | Implied Return / Gap | Key Assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Downside | <amount> | <%> | <%> | <effect> | <multiple/DCF/asset value> | <annualized return or valuation gap> | <assumptions> |
| Base | <amount> | <%> | <%> | <effect> | <multiple/DCF/asset value> | <annualized return or valuation gap> | <assumptions> |
| Upside | <amount> | <%> | <%> | <effect> | <multiple/DCF/asset value> | <annualized return or valuation gap> | <assumptions> |

## Critical Option Or Catalyst

- Option/catalyst:
- Technical feasibility:
- Demand evidence:
- Unit economics:
- Capital required:
- Timing risk:
- Competitive response:
- Evidence that changes probability:

## Inversion And Failure Modes

- Bear case:
- Permanent impairment risks:
- Evidence that would disprove the thesis:
- Unknowns:

## Holder Lens

<Only include when the user already owns the stock. Otherwise write "Not applicable.">

## Monitoring Checklist

- <Metric, event, or filing to watch>
- <Metric, event, or filing to watch>
- <Metric, event, or filing to watch>

## Bottom Line

<Concise conclusion under stated assumptions.>

## Important Caveat

This memo is analytical support, not personalized financial advice. Verify current filings, prices, taxes, liquidity, and suitability before acting.
```
