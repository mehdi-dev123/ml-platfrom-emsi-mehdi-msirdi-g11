# Plateforme IA - Machine Learning

Application desktop interactive (Python + CustomTkinter) pour explorer six
familles d'algorithmes de Machine Learning. Chaque onglet genere des donnees
aleatoires, entraine un modele et affiche des visualisations matplotlib ainsi
que les metriques associees.

> Projet de fin d'annee (PFA) — EMSI
> Realise par **MSIRDI Mahdi** · Encadre par **EL MKHALET MOUNA**

## Fonctionnalites

| Onglet | Modele | Visualisation |
| --- | --- | --- |
| Regression | Regression lineaire multiple | Nuage de points + plan de regression 3D |
| Clustering 3D | K-Means | Clusters et centres en 3D, score silhouette |
| Random Forest | Classification | Importance des variables + predictions |
| Series temp. | ARIMA | Entrainement, test et prevision |
| Reseau neuronal | MLPRegressor | Ajustement + courbe de perte |
| Validation croisee | 4 modeles compares | Accuracy moyenne et evolution par fold |

Theme clair / sombre commutable et ecran de chargement progressif.

## Installation

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Lancer en mode developpement

```powershell
.\venv\Scripts\python.exe main.py
```

Ou double-cliquer sur `run_app.bat`.

## Generer l'executable Windows

```powershell
.\build_desktop.ps1
```

L'executable est cree dans `dist\Plateforme-IA-ML\Plateforme-IA-ML.exe`.

## Stack technique

Python · CustomTkinter · matplotlib · scikit-learn · statsmodels · numpy
