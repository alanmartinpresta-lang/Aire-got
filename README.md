# AIRE Genesis 3 — Immersion

Version reconstruite pour l'expérience d'immersion d'un agent externe.

## Base

Le projet reprend la structure expérimentale AIRE/Genesis 3 disponible dans l'historique du projet, avec une architecture en couches U0-U6 et une interface volontairement minimale.

### U0 — World/Causal Kernel
Temps, cycles, seed déterministe, événements, transitions d'état.

### U1 — Existence/Ontology
Identité persistante, naissance, mort, renaissance, objets et mémoire expérimentale.

### U2 — Environment
Atmosphère simplifiée, eau, énergie environnementale, température, terrain et ressources.

### U3 — Matter/Chemistry
Ressources élémentaires, transformations et combinaisons expérimentales.

### U4 — Biology/State
État fonctionnel de l'agent, énergie, hydratation, santé et vieillissement de cycle.

### U5 — Ecology/Interaction
Disponibilité locale des ressources, dangers et conséquences des actions.

### U6 — Experiment/Agent Interface
Observation partielle, actions, journal, découvertes et mémoire persistante.

## Immersion

Le même agent expérimental conserve sa mémoire après une mort. Son état physique est réinitialisé à la renaissance.

Une expérience peut être lancée sur 50 vies ou davantage. AIRE ne contient aucune clé OpenAI et n'appelle pas un modèle externe : l'agent externe interagit avec l'API.

## Interface

Pas de carte ni d'inventaire affichés. L'interface présente uniquement :
- robot représentant l'agent ;
- Découvert ;
- État du personnage ;
- Expériences réalisées.

## Lancer

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Puis ouvrir http://localhost:8000.

## API

GET /api/health
POST /api/experiment/start?lives=50
GET /api/observation
POST /api/action
GET /api/state
GET /api/memory
GET /api/history
GET /api/experiments
GET /api/results

Exemple :
```json
{"action":"move","params":{"dx":1,"dy":0}}
```

AIRE est un environnement expérimental : les interprétations doivent être séparées des faits mesurés.
