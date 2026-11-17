# Absatzvisualisierung und Chancenforschung für Fahrzeuge

`vehicle-sales-opportunity` · Deutsch

## Zweck und Einsatzbereich

Vorhandene Mengen für Autos, Motorräder, UTV, ATV und Boote visualisieren, gleiche Zeitfenster vergleichen und belegte Chancenforschung planen.

## Umsetzungsgrundlage und Abhängigkeiten

Erlaubter Datensatz mit Markt/Kalenderzeit/Indikator/Einheit; Python 3.10+ Standardbibliothek und Browser zur Sichtprüfung. Offlinekern braucht kein Konto/API; Validierung braucht Produkt-, Nutzer-, Passform- und Kostenbelege.

## Eingaben

Monatliches dataset-JSON, passende Basisperioden und neuer Ausgabeordner erforderlich. Optional Schwellen, Forschungsbrief und Belege. Fehlwerte/assetType/metricKind erhalten; Jahres-/Quartalswerte nicht auf Monate verteilen.

## Ausgaben

dashboard.html, analysis.json, opportunities.json, report.md, qa.json; research-review.md zusätzlich durch den Assistenten. Kandidaten und Rechen-PASS beweisen keine Nachfrage, Passform oder ROI.

## Ablauf

1. Frage/Markt/Einheit/Rechte festlegen
2. stabile IDs, CY/MY, Absatz/Bestand, Typen und Einzelhandel/Großhandel/Auslieferung/Neuzulassung trennen
3. prüfen und erzeugen
4. Wachstum/Rückgang/Nullbasis/Lücken an identischen vollständigen Gruppen abgleichen
5. Hypothesen mit Beleg, kleinstem Test und Stopp prüfen
6. Desktop/Mobilfilter, Details und Export testen.

## Grenzen und Abbruchbedingungen

Kein automatischer Datenkauf oder Veröffentlichung. UTV-Fall:124 Katalogeinträge,105 Quellen, historisch berechenbare Gruppen US63/CA15/MX1; Gesamt-VIO unbekannt. Gruppenszenarien sind keine beobachteten Verkäufe, Konfidenzintervalle oder Untergrenzen. ATV-Kanäle untersucht, ATV nicht im UTV-Datensatz; Modelljahr-/Bildarbeit bleibt offen.

## Beispielanfrage

Verwende `$vehicle-sales-opportunity` — Januar–Juni in USA/Kanada/Mexiko mit denselben Vorjahresmonaten vergleichen; +30% Fahrzeugabsatz beweist nicht +30% Zubehörnachfrage; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Vollständige Spezifikation

[Skill-Einstieg und Detailreferenzen](../../SKILL.md).

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

