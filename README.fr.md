# Collecte et analyse d’avis écrits Amazon

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

## Installation et utilisation

Télécharger ou cloner le dépôt, puis copier le répertoire du Skill indiqué, avec ses references, scripts, assets et autres dépendances existantes, dans le répertoire de Skills de l’hôte. Conserver son nom et SKILL.md. Changer la langue de documentation ne demande pas de nouvelle installation. Les commandes proposées ne prouvent ni installation ni activation.

```sh
git clone https://github.com/PDBen-Auto/amazon-review-intelligence-skill.git
```

## Collecte et analyse d’avis écrits Amazon

`amazon-review-scraper`

Collecter ou analyser les avis écrits d’ASIN exacts, dédupliquer prudemment et livrer des tableaux et rapports hors ligne traçables.

Répertoire du Skill: `.`

**Fondements et dépendances**

Python 3.10+, openpyxl pour XLSX, Pillow facultatif pour images. Woot facultatif et réservé aux États-Unis avec correspondance exacte ASIN/offre ; autres marchés : connecteur ou navigateur autorisé disponible.

**Entrées**

Collecte : ASIN/URL et marché, filtres date/étoiles/volume facultatifs. Analyse : JSON/CSV/XLSX/HTML fournis. Préciser livrables et droits ; ne pas recollecter des fichiers complets.

**Sorties**

Sources/statuts par ASIN, JSON canonique, XLSX/CSV/URL médias demandés, HTML autonome et éventuel transfert VOC. Conserver séparément texte intégral, traduction et résumé.

[Déroulement · Limites et conditions d’arrêt · Exemple de demande](references/i18n/fr.md)

> Utilise `$amazon-review-scraper` — Analyser les avis fournis d’un support, garder les originaux et expliquer en français les thèmes récurrents avec limites d’échantillon ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.
