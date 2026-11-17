# Vehicle sales visualization and opportunity research

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Use the user's explicitly requested output language; otherwise follow the request language. Keep commands, skill IDs, JSON keys, enum values, units and source quotations unchanged. Separate translations from originals. Never infer country, currency or jurisdiction from language. Read the relevant detailed references in the complete specification and retain all existing validation and authorization gates.

## Installation and use

Download or clone the repository and copy the indicated skill directory, including its existing references, scripts, assets and other dependencies, into your host's skill directory. Keep its name and SKILL.md. Changing the documentation language does not require another installation. Commands are installation options, not evidence of installation or activation.

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## Vehicle sales visualization and opportunity research

`vehicle-sales-opportunity`

Visualize existing quantity data for cars, motorcycles, UTV, ATV and boats, compare matched periods and design evidence-led opportunity research.

Skill directory: `skills/vehicle-sales-opportunity`

**Implementation Basis and Dependencies**

Authorized dataset with market, calendar period, metric and units; Python 3.10+ standard library for scripts and browser for visual QA. Core offline execution needs no account/API. Additional research requires relevant product, user, fitment and cost evidence.

**Inputs**

Required monthly dataset JSON, matched current/base month windows and a new output directory. Optional thresholds, research brief and supporting evidence. Preserve missing values, assetType and metricKind; annual/quarterly data cannot be evenly split into months.

**Outputs**

dashboard.html, analysis.json, opportunities.json, report.md and qa.json; the assistant separately writes research-review.md. Candidate signals and arithmetic PASS do not validate demand, fitment or ROI.

[Workflow · Boundaries and stopping conditions · Example request](skills/vehicle-sales-opportunity/references/i18n/en.md)

> Use `$vehicle-sales-opportunity` — Compare US/CA/MX January–June with the same months last year; +30% vehicle sales is a research signal, not proof of +30% accessory demand; respond in English and preserve evidence, unknowns and action boundaries.

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## Language coverage and validation

This localized operating guide covers purpose, prerequisites, inputs, outputs, workflow, examples and boundaries; it is not a line-by-line translation of every reference. Detailed technical references, historical cases, script errors, example interfaces and images retain their original language. The assistant can explain them in the requested language. Structural, link and key-constraint checks are performed; native-speaker editorial review for each language is not claimed.

Before delivery reconcile inputs, evidence, missing values, files and the original completion criteria. Mark unexecuted steps unverified; a successful script exit is not business validation.
