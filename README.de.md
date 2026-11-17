# Amazon-Rezensionen sammeln und auswerten

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

## Installation und Nutzung

Das Repository herunterladen oder klonen und das angegebene Skill-Verzeichnis mit seinen vorhandenen references, scripts, assets und weiteren Abhängigkeiten in das Skill-Verzeichnis des Hosts kopieren. Name und SKILL.md beibehalten. Ein Sprachwechsel erfordert keine weitere Installation. Installationsbefehle sind Optionen und kein Nachweis einer Installation oder Aktivierung.

```sh
git clone https://github.com/PDBen-Auto/amazon-review-intelligence-skill.git
```

## Amazon-Rezensionen sammeln und auswerten

`amazon-review-scraper`

Textrezensionen exakter ASINs sammeln oder analysieren, vorsichtig deduplizieren und nachvollziehbare Tabellen/Offlineberichte liefern.

Skill-Verzeichnis: `.`

**Umsetzungsgrundlage und Abhängigkeiten**

Python 3.10+, openpyxl für XLSX, optional Pillow für Bilder. Woot ist optional, nur USA, mit exakter ASIN-/Offer-Zuordnung. Andere Märkte benötigen verfügbaren autorisierten Connector oder Browser.

**Eingaben**

Sammlung: ASIN/URL und Marktplatz, optional Datum/Sterne/Anzahl. Analyse: vorhandenes JSON/CSV/XLSX/HTML. Ausgaben und Datenschutzrechte festlegen; vollständige Dateien nicht erneut sammeln.

**Ausgaben**

Quell-/Statusdaten je ASIN, kanonisches JSON, benötigtes XLSX/CSV/Medien-URLs, Einzeldatei-HTML und optional VOC-Übergabe. Originaltext, Übersetzung und Zusammenfassung getrennt halten.

[Ablauf · Grenzen und Abbruchbedingungen · Beispielanfrage](references/i18n/de.md)

> Verwende `$amazon-review-scraper` — Vorhandene Halterrezensionen auswerten, Originale erhalten und auf Deutsch wiederkehrende Probleme samt Stichprobenlimits erklären; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.
