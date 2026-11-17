# Visualisation des ventes et recherche d’opportunités véhicules

`vehicle-sales-opportunity` · Français

## Objectif et périmètre

Visualiser les quantités existantes d’automobiles, motos, UTV, ATV et bateaux, comparer des fenêtres identiques et concevoir une recherche étayée.

## Fondements et dépendances

Données autorisées avec marché/période civile/métrique/unité ; Python 3.10+ standard et navigateur pour contrôle visuel. Cœur hors ligne sans compte/API. Validation : preuves produit/utilisateur/compatibilité/coût.

## Entrées

dataset JSON mensuel, périodes de référence appariées et nouveau répertoire obligatoires. Seuils/brief/preuves facultatifs. Conserver valeurs manquantes/assetType/metricKind ; ne pas répartir année/trimestre en mois égaux.

## Sorties

dashboard.html, analysis.json, opportunities.json, report.md, qa.json ; research-review.md rédigé séparément. Candidats et PASS arithmétique ne prouvent ni demande, ni compatibilité, ni ROI.

## Déroulement

1. Fixer question/marchés/unités/droits
2. ID stables, séparer CY/MY, ventes/parc, types et détail/gros/livraisons/immatriculations neuves
3. valider/générer
4. rapprocher hausse/baisse/base nulle/manquants sur mêmes cohortes complètes
5. examiner chaque hypothèse avec preuve/test minimal/arrêt
6. contrôler filtres/détails/exports ordinateur/mobile.

## Limites et conditions d’arrêt

Aucun achat de données ni publication automatique. Cas UTV :124 entrées,105 sources, cohortes historiques calculables US63/CA15/MX1 ; VIO total inconnu. Scénarios de cohortes ≠ ventes observées, intervalle de confiance ou borne basse. Canaux ATV étudiés mais ATV exclus du jeu UTV ; affinage millésimes/images non terminé.

## Exemple de demande

Utilise `$vehicle-sales-opportunity` — Comparer janvier–juin États-Unis/Canada/Mexique aux mêmes mois précédents ; +30% de ventes ne prouve pas +30% de demande d’accessoires ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Spécification complète

[Point d’entrée du Skill et références détaillées](../../SKILL.md).

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

