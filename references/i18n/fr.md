# Collecte et analyse d’avis écrits Amazon

`amazon-review-scraper` · Français

## Objectif et périmètre

Collecter ou analyser les avis écrits d’ASIN exacts, dédupliquer prudemment et livrer des tableaux et rapports hors ligne traçables.

## Fondements et dépendances

Python 3.10+, openpyxl pour XLSX, Pillow facultatif pour images. Woot facultatif et réservé aux États-Unis avec correspondance exacte ASIN/offre ; autres marchés : connecteur ou navigateur autorisé disponible.

## Entrées

Collecte : ASIN/URL et marché, filtres date/étoiles/volume facultatifs. Analyse : JSON/CSV/XLSX/HTML fournis. Préciser livrables et droits ; ne pas recollecter des fichiers complets.

## Sorties

Sources/statuts par ASIN, JSON canonique, XLSX/CSV/URL médias demandés, HTML autonome et éventuel transfert VOC. Conserver séparément texte intégral, traduction et résumé.

## Déroulement

1. Identifier produit/marché
2. vérifier offre Woot ou repli autorisé
3. zéro d’interface/pages partielles ne prouvent pas un ensemble vide complet
4. fusionner par ID ou texte complet étayé
5. un problème/bénéfice principal par avis, étiquettes secondaires non exclusives
6. ouvrir et rapprocher les livrables.

## Limites et conditions d’arrêt

Arrêter sur CAPTCHA, connexion ou restriction. Ni cookies, commandes, données de compte. Protéger HTML/formules. Avis écrits ≠ notes, échantillon ≠ taux de défaut global. Les champs fixes translation_zh/summary_zh restent chinois.

## Exemple de demande

Utilise `$amazon-review-scraper` — Analyser les avis fournis d’un support, garder les originaux et expliquer en français les thèmes récurrents avec limites d’échantillon ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Spécification complète

[Point d’entrée du Skill et références détaillées](../../SKILL.md).

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

