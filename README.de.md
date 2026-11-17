# Absatzvisualisierung und Chancenforschung für Fahrzeuge

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

## Installation und Nutzung

Das Repository herunterladen oder klonen und das angegebene Skill-Verzeichnis mit seinen vorhandenen references, scripts, assets und weiteren Abhängigkeiten in das Skill-Verzeichnis des Hosts kopieren. Name und SKILL.md beibehalten. Ein Sprachwechsel erfordert keine weitere Installation. Installationsbefehle sind Optionen und kein Nachweis einer Installation oder Aktivierung.

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## Absatzvisualisierung und Chancenforschung für Fahrzeuge

`vehicle-sales-opportunity`

Vorhandene Mengen für Autos, Motorräder, UTV, ATV und Boote visualisieren, gleiche Zeitfenster vergleichen und belegte Chancenforschung planen.

Skill-Verzeichnis: `skills/vehicle-sales-opportunity`

**Umsetzungsgrundlage und Abhängigkeiten**

Erlaubter Datensatz mit Markt/Kalenderzeit/Indikator/Einheit; Python 3.10+ Standardbibliothek und Browser zur Sichtprüfung. Offlinekern braucht kein Konto/API; Validierung braucht Produkt-, Nutzer-, Passform- und Kostenbelege.

**Eingaben**

Monatliches dataset-JSON, passende Basisperioden und neuer Ausgabeordner erforderlich. Optional Schwellen, Forschungsbrief und Belege. Fehlwerte/assetType/metricKind erhalten; Jahres-/Quartalswerte nicht auf Monate verteilen.

**Ausgaben**

dashboard.html, analysis.json, opportunities.json, report.md, qa.json; research-review.md zusätzlich durch den Assistenten. Kandidaten und Rechen-PASS beweisen keine Nachfrage, Passform oder ROI.

[Ablauf · Grenzen und Abbruchbedingungen · Beispielanfrage](skills/vehicle-sales-opportunity/references/i18n/de.md)

> Verwende `$vehicle-sales-opportunity` — Januar–Juni in USA/Kanada/Mexiko mit denselben Vorjahresmonaten vergleichen; +30% Fahrzeugabsatz beweist nicht +30% Zubehörnachfrage; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.
