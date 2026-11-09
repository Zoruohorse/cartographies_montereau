# Cartographie des acteurs — Montereau-Vallée-de-la-Seine

**Projet EDF–OpCore · Seine-et-Marne · Arrêté documentaire au 5 novembre 2026**

Deux interfaces statiques et interactives pour analyser les acteurs, positions, preuves et relations autour du projet de data center de l'ancienne centrale thermique EDF de Montereau.

> **Attention au périmètre :** le nom historique « Montereau » ne signifie pas que les bâtiments sont dans Montereau-Fault-Yonne. Le site industriel se trouve à **Vernou-la-Celle-sur-Seine** et **La Grande-Paroisse**.

## Accéder aux vues

- `apps/cards/` : fiches acteurs et positions, lien vers preuve cliquable, filtres, synthèse des enjeux, vigilances et sources, chronologie du projet.
- `apps/network/` : réseau à forces et liens courbes, navigation/zoom, drag & drop, filtres de typologies et de positions, panneau de détail acteur et lien avec les sources.
- `index.html` : page d'accueil et navigation entre les deux vues.

## Données initiales

- `data/actors.json` : acteurs, projets, institutions, médias et **points de vigilance** identifiés et qualifiés.
- `data/claims.json` : positions et incertitudes (favorable / neutral / opposed) avec références vers preuves.
- `data/evidence.json` : synthèses sourcées (non présentées comme des citations exactes) et emplacement documentaire.
- `data/relations.json` : **uniquement** des relations justifiables, avec type, certitude et preuves.
- `data/sources.json` : titres, éditeurs, dates et **URL canoniques** ; distinction entre source consultée directement et extrait issu du tableur.
- `data/content.json` : informations techniques, jalons, calendriers et réserves.
- `data/synthesis.json` : synthèses des enjeux / vigilances, preuves et liste des sources mobilisées.
- `config/taxonomy.json` : palette, catégories, positions et types de relations.

Les données sont initialisées à partir des **20 ressources** de `Montereau.xlsx` et de publications complémentaires publiques, dont le communiqué primaire EDF, le portail RTE, les déclarations des maires et les sites officiels des communes.

### Fiabilité et interdictions

1. La puissance du projet est décrite dans l'annonce de 2025 comme *plusieurs centaines de mégawatts*, sans transformer automatiquement les données de sites Fast Track en MW attribués à OpCore.
2. L'investissement d'**environ 4 Md€**, les **emplois projetés** et l'ouverture envisagée en **2027** sont des annonces prospectives, **non** des réalisations attestées au 5 novembre 2026.
3. Le dernier stade contractuel explicitement confirmé par les sources principales consultées est l'annonce de **négociations exclusives EDF–OpCore** en novembre 2025. Ne pas conclure qu'aucun acte n'a eu lieu depuis ; l'état actuel exige une vérification supplémentaire.
4. Les **positions de critiques nationales des data centers** ne sont pas représentées comme une opposition organisée à Montereau. Les acteurs et projets de **Fouju** ne sont pas fusionnés avec ceux de Montereau.
5. Les informations publiées à partir du texte du classeur, sans consultation intégrale du site d'origine, sont distinguées par `source.consultation`.
6. Les propositions de **récupération de chaleur**, de **transport fluvial** et de **campus de formation** ne sont pas assimilées à des contrats ou installations confirmés.

## Déploiement GitHub

Ce répertoire constitue le contenu **complet** d'un dépôt GitHub. Il n'exige ni Node.js, ni build, ni base de données, ni CDN.

1. Créez un dépôt public nommé, par exemple, **`cartographies_montereau`** sur le compte GitHub concerné.
2. Importez tous les fichiers et dossiers **à la racine** (pas l'archive ZIP en tant que seul fichier).
3. Dans **Settings → Pages**, sélectionnez `Deploy from a branch`, la branche `main`, le dossier `/ (root)`.
4. Ouvrez `https://<compte>.github.io/cartographies_montereau/` ; les deux vues se trouvent à `/apps/cards/` et `/apps/network/`.

Utilisation en ligne de commande si le dépôt vide a été créé :

```bash
git init
git add .
git commit -m "Initialiser la cartographie Montereau EDF–OpCore avec preuves"
git branch -M main
git remote add origin https://github.com/<compte>/cartographies_montereau.git
git push -u origin main
```

## Validation et test local

```bash
python3 validate.py
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000/`. Les requêtes `fetch()` sont bloquées en ouverture directe `file://` : il faut un serveur local ou GitHub Pages.

## Provenance et mise à jour

Date d'arrêté : **5 novembre 2026**. Les sources et analyses des exclusions sont documentées dans `docs/RESSOURCES_LOT.md` et `docs/RAPPORT_INITIAL.md`.

**Publication** : le présent projet est un dépôt **préparé**, pas un dépôt distant créé automatiquement. La connexion GitHub utilisée ne dispose pas d'action de création de dépôt neuf. Aucun autre dépôt existant n'a été modifié.


## Actualisation du 9 novembre 2026 : cinq onglets

**Évolution contractuelle majeure** : EDF indique dans sa présentation publique du 29 mai 2026 (diapositive 5, Institut Paris Region) qu'un **bail avec OpCore a été signé début mai 2026**. Il ne s'agit pas d'une autorisation, ni d'un début de travaux ou raccordement déjà réalisé. Pièces : `source_0023`, `evidence_0045`.

La synthèse comporte neuf thèmes, avec références cliquables et preuves dépliables. La chronologie compte 11 jalons et sept repères techniques, en distinguant historique, annonces et projet 2027.

Un cinquième onglet **Évolution des acteurs** contient les modes **Nouveaux / Cumulés / Par position** : 20 fiches, 18 acteurs datés (dont RTE daté au mois seulement) et deux parlementaires sans date de publication sûre de l'interview, conservés hors graphique. Parmi les 18 datés : 17 favorables, un neutre, aucun opposant documenté. Cela ne mesure pas l'opinion réelle de la population et ne retrace pas les changements de positions historiques.

Références nouvelles : présentation EDF du 29 mai 2026 ; bulletin municipal Montereau 7 sur 7 du 29 avril 2026 ; article Évasion FM du 5 mars déjà présent. Les positions et les relations initiales sont conservées. Audit : `data/evolution-audit-20261109.json`.
