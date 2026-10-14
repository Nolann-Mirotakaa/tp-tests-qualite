# Exercices de tests, couverture et qualit?

Projet du chapitre 2 : fonctions utilitaires, validateurs, moteur de tarification et API de commande avec Flask.

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Commandes

```powershell
python -m pytest -q
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
python -m flake8
python -m src.server
```

L'API utilise un stockage en m?moire, r?initialis? au red?marrage. Les routes et la configuration Flask sont s?par?es du d?marrage du serveur pour que les tests utilisent le client Flask sans ouvrir de port.
