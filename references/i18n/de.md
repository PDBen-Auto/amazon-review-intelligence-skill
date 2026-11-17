# Amazon-Rezensionen sammeln und auswerten

`amazon-review-scraper` · Deutsch

## Zweck und Einsatzbereich

Textrezensionen exakter ASINs sammeln oder analysieren, vorsichtig deduplizieren und nachvollziehbare Tabellen/Offlineberichte liefern.

## Umsetzungsgrundlage und Abhängigkeiten

Python 3.10+, openpyxl für XLSX, optional Pillow für Bilder. Woot ist optional, nur USA, mit exakter ASIN-/Offer-Zuordnung. Andere Märkte benötigen verfügbaren autorisierten Connector oder Browser.

## Eingaben

Sammlung: ASIN/URL und Marktplatz, optional Datum/Sterne/Anzahl. Analyse: vorhandenes JSON/CSV/XLSX/HTML. Ausgaben und Datenschutzrechte festlegen; vollständige Dateien nicht erneut sammeln.

## Ausgaben

Quell-/Statusdaten je ASIN, kanonisches JSON, benötigtes XLSX/CSV/Medien-URLs, Einzeldatei-HTML und optional VOC-Übergabe. Originaltext, Übersetzung und Zusammenfassung getrennt halten.

## Ablauf

1. Produkt/Markt klären
2. Woot exakt zuordnen oder erlaubte Alternative
3. Schnittstellen-Null/Seitenfehler nicht als vollständig leer werten
4. per ID oder Volltextbelegen zusammenführen
5. je Rezension ein Hauptproblem/-nutzen
6. Sekundärlabels nicht als exklusiven Nenner summieren
7. Ausgaben öffnen und Mengen abstimmen.

## Grenzen und Abbruchbedingungen

Bei CAPTCHA, Login oder Zugangssperre stoppen. Keine Cookies, Bestellungen oder Kontodaten. HTML/Formeln absichern. Rezensionen sind nicht Bewertungen, Stichproben keine Bevölkerungsfehlerquote. Feste translation_zh/summary_zh-Felder bleiben chinesisch.

## Beispielanfrage

Verwende `$amazon-review-scraper` — Vorhandene Halterrezensionen auswerten, Originale erhalten und auf Deutsch wiederkehrende Probleme samt Stichprobenlimits erklären; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Vollständige Spezifikation

[Skill-Einstieg und Detailreferenzen](../../SKILL.md).

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

