# Visualisation des ventes et recherche d’opportunités véhicules

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

## Installation et utilisation

Télécharger ou cloner le dépôt, puis copier le répertoire du Skill indiqué, avec ses references, scripts, assets et autres dépendances existantes, dans le répertoire de Skills de l’hôte. Conserver son nom et SKILL.md. Changer la langue de documentation ne demande pas de nouvelle installation. Les commandes proposées ne prouvent ni installation ni activation.

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## Visualisation des ventes et recherche d’opportunités véhicules

`vehicle-sales-opportunity`

Visualiser les quantités existantes d’automobiles, motos, UTV, ATV et bateaux, comparer des fenêtres identiques et concevoir une recherche étayée.

Répertoire du Skill: `skills/vehicle-sales-opportunity`

**Fondements et dépendances**

Données autorisées avec marché/période civile/métrique/unité ; Python 3.10+ standard et navigateur pour contrôle visuel. Cœur hors ligne sans compte/API. Validation : preuves produit/utilisateur/compatibilité/coût.

**Entrées**

dataset JSON mensuel, périodes de référence appariées et nouveau répertoire obligatoires. Seuils/brief/preuves facultatifs. Conserver valeurs manquantes/assetType/metricKind ; ne pas répartir année/trimestre en mois égaux.

**Sorties**

dashboard.html, analysis.json, opportunities.json, report.md, qa.json ; research-review.md rédigé séparément. Candidats et PASS arithmétique ne prouvent ni demande, ni compatibilité, ni ROI.

[Déroulement · Limites et conditions d’arrêt · Exemple de demande](skills/vehicle-sales-opportunity/references/i18n/fr.md)

> Utilise `$vehicle-sales-opportunity` — Comparer janvier–juin États-Unis/Canada/Mexique aux mêmes mois précédents ; +30% de ventes ne prouve pas +30% de demande d’accessoires ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.
