---
name: diagnose-stocks-first-principles
description: "Diagnose and investigate public stocks from first principles: ownership, business reality, cash generation, moat, management, valuation, incentives, and failure modes. Use when Codex is asked to analyze, diagnose, research, compare, or write an investment memo for A-shares, Hong Kong stocks, U.S. stocks, ADRs, listed equity securities, Chinese-language stock diagnosis requests, first-principles investing requests, buy-or-not questions, worth-researching questions, or source-backed risk reviews before acting."
---

# Diagnose Stocks First Principles

## Purpose

Use this skill to turn a ticker or company name into a current, source-backed stock diagnosis. Treat a share as partial ownership of a business, then reason from observable facts, economic constraints, and downside cases before forming a view.

This skill is for analysis and education, not personalized financial advice. Do not present certainty, guaranteed returns, or an unconditional buy/sell command. If the user asks a buy-or-not question, translate it into a conditional decision tree with assumptions, evidence gaps, and risks.

## Core Question

Answer this before any narrative:

> If I bought the whole company at today's market value, what durable cash flows would I likely receive, what could destroy them, and what price am I paying for that uncertainty?

## Workflow

1. **Normalize the security.**
   - Identify ticker, exchange, currency, company legal name, and share class.
   - If ambiguous, ask one concise question only when a wrong assumption would materially change the analysis.
   - State the analysis date, market data timestamp, and user-provided constraints such as cost basis, holding period, portfolio role, or risk tolerance.

2. **Build a source ledger before reasoning.**
   - Browse for current facts whenever price, filings, earnings, guidance, rates, regulation, or ownership may have changed.
   - Prefer official sources: company investor relations, annual reports, quarterly reports, SEC EDGAR, exchange filings, HKEXnews, CNINFO, Shanghai/Shenzhen/Beijing exchange disclosures, regulator releases, and official macro data.
   - Use secondary quote/news sources only for market snapshots or cross-checks, and label them as secondary.
   - Capture exact dates for each source. Separate fact, inference, and unknown.

3. **Reduce the company to first principles.**
   - Customer job: what real problem is solved, for whom, and why payment happens.
   - Unit economics: revenue driver, gross margin, variable cost, capital intensity, working capital need, and reinvestment runway.
   - Cash conversion: whether reported earnings become operating cash flow and free cash flow after capex, working capital, and stock-based compensation.
   - Financial quality: explain revenue mix, gross margin, operating margin, R&D, sales efficiency, debt, dilution, backlog conversion, and customer concentration when available.
   - Durability: why competitors cannot easily copy, undercut, regulate away, substitute, or outspend the business.
   - Competition: map direct competitors, substitutes, incumbent suppliers, customer procurement power, and the price/value wedge.
   - Capital allocation: whether management reinvests, pays dividends, repurchases shares, issues shares, borrows, or acquires with owner discipline.

4. **Value the security as a claim on future cash.**
   - Start with enterprise value or market cap, net cash/debt, share count, and dilution.
   - Use ranges and base rates, not single-point precision.
   - Build at least three scenarios: downside, base, and upside.
   - Each scenario must state revenue, gross margin, FCF margin, dilution/share count effect, terminal valuation method, and implied annualized return or valuation gap.
   - Tie valuation to cash flow quality, growth duration, reinvestment return, cyclicality, and balance-sheet risk.
   - Make explicit what must be true for the current price to be attractive, fair, or dangerous.
   - Read `references/scenario-valuation.md` when drafting a formal memo or when valuation is the main uncertainty.

5. **Invert the thesis.**
   - Write the bear case before the verdict.
   - Ask: what evidence would prove this diagnosis wrong, what hidden leverage exists, which accounting numbers may be low quality, and what incentive would make insiders or intermediaries overstate the story?
   - Identify the critical option or catalyst if one dominates the valuation, such as a new product, drug, factory, mine, license, turnaround, acquisition, or launch vehicle.
   - For that option, separate technical feasibility, customer demand, unit economics, capital need, timing, and competitive response.
   - Distinguish permanent impairment risk from temporary price volatility.

6. **Produce a decision-grade output.**
   - Lead with a short verdict: "investigate further", "watchlist only", "too hard", "quality but expensive", "cheap for a reason", or another plain label.
   - Include a source ledger, evidence map, first-principles diagnosis, scenario valuation, inversion, key monitoring items, and open questions.
   - For buy-or-not questions, give conditional action buckets such as "research further", "watchlist", "too hard", "quality but expensive", or "risk dominates" rather than a naked trade command.
   - If the user asks for a Markdown report, use `references/output-template.md`.
   - If a report is saved, run `scripts/audit_stock_memo.py <report.md>` and fix any failures before delivering.

## Required Evidence

Collect the items in `references/checklist.md` unless impossible. If an item is unavailable, mark it `Unknown` and explain why it matters.

Do not let a missing fact silently become an assumption.

## Output Standards

- Use exact dates for current market data, filings, earnings, guidance, dividends, buybacks, or regulatory events.
- Cite sources with links. Keep source summaries concise.
- Label facts, inferences, assumptions, and unknowns.
- Use a compact Evidence Map table for decision-critical facts, inferences, assumptions, and unknowns.
- Avoid precise price targets unless requested; prefer valuation ranges and scenario conditions.
- Avoid technical-analysis claims unless the user asks for trading context. If included, keep them secondary to business and risk analysis.
- When the user already owns the stock, add a "Holder Lens" section: cost basis, thesis drift, sell discipline, position sizing risk, tax/liquidity caveats if relevant, and what would trigger a reassessment.
- For comparisons, use the same first-principles dimensions across all tickers and avoid mixing stale and current data.

## Guardrails

- Do not rely on memory for latest facts. Browse or state that current verification was not possible.
- Do not confuse a good company with a good stock; valuation is part of the diagnosis.
- Do not confuse low multiples with cheapness; check business decline, cyclicality, leverage, governance, and cash conversion.
- Do not confuse high growth with value creation; check reinvestment returns, dilution, and terminal economics.
- Do not give personalized financial advice as if it were certain. Frame conclusions as analysis under stated assumptions.

## Optional Tools

- Read `references/checklist.md` for the full investigative checklist.
- Read `references/scenario-valuation.md` when the report needs a decision-grade valuation.
- Read `references/output-template.md` when drafting a saved Markdown memo.
- Run `scripts/audit_stock_memo.py` against saved Markdown reports to catch missing headings, sources, dates, and risk sections.
