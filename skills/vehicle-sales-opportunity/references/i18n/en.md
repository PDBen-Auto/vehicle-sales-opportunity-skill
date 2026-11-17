# Vehicle sales visualization and opportunity research

`vehicle-sales-opportunity` · English

## Purpose and scope

Visualize existing quantity data for cars, motorcycles, UTV, ATV and boats, compare matched periods and design evidence-led opportunity research.

## Implementation Basis and Dependencies

Authorized dataset with market, calendar period, metric and units; Python 3.10+ standard library for scripts and browser for visual QA. Core offline execution needs no account/API. Additional research requires relevant product, user, fitment and cost evidence.

## Inputs

Required monthly dataset JSON, matched current/base month windows and a new output directory. Optional thresholds, research brief and supporting evidence. Preserve missing values, assetType and metricKind; annual/quarterly data cannot be evenly split into months.

## Outputs

dashboard.html, analysis.json, opportunities.json, report.md and qa.json; the assistant separately writes research-review.md. Candidate signals and arithmetic PASS do not validate demand, fitment or ROI.

## Workflow

1. Freeze question, markets, units and permissions.
2. Normalize stable series IDs without mixing CY/MY, sales/VIO, vehicle types or retail/wholesale/deliveries/registrations.
3. Run validation and build.
4. Reconcile growing, declining, zero-base and missing series using matched complete cohorts.
5. Review each research hypothesis with evidence, next test and stop condition.
6. Inspect desktop/mobile filters, drilldown and exports.

## Boundaries and stopping conditions

No automatic source purchase or publication. UTV case: 124 catalog items, 105 sources, historical computable US63/CA15/MX1 cohorts; total VIO unknown. Cohort scenarios are not observed sales, a confidence interval or lower bound. ATV channels exist but ATV is excluded from that UTV dataset; further model-year/image work remains open.

## Example request

Use `$vehicle-sales-opportunity` — Compare US/CA/MX January–June with the same months last year; +30% vehicle sales is a research signal, not proof of +30% accessory demand; respond in English and preserve evidence, unknowns and action boundaries.

## Complete specification

[Skill entrypoint and detailed references](../../SKILL.md).

Use the user's explicitly requested output language; otherwise follow the request language. Keep commands, skill IDs, JSON keys, enum values, units and source quotations unchanged. Separate translations from originals. Never infer country, currency or jurisdiction from language. Read the relevant detailed references in the complete specification and retain all existing validation and authorization gates.

Before delivery reconcile inputs, evidence, missing values, files and the original completion criteria. Mark unexecuted steps unverified; a successful script exit is not business validation.

## Language coverage and validation

This localized operating guide covers purpose, prerequisites, inputs, outputs, workflow, examples and boundaries; it is not a line-by-line translation of every reference. Detailed technical references, historical cases, script errors, example interfaces and images retain their original language. The assistant can explain them in the requested language. Structural, link and key-constraint checks are performed; native-speaker editorial review for each language is not claimed.

