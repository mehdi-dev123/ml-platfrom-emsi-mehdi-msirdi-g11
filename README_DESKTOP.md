# Plateforme IA - Machine Learning

Application desktop Python avec CustomTkinter pour visualiser 6 algorithmes :
regression lineaire, clustering K-Means 3D, Random Forest, ARIMA, reseau de neurones
et validation croisee.

## Lancer en mode developpement

```powershell
.\venv\Scripts\python.exe main.py
```

Ou double-cliquer sur `run_app.bat`.

## Generer l'application Windows

```powershell
.\build_desktop.ps1
```

L'executable sera cree dans :

```text
dist\Plateforme-IA-ML\Plateforme-IA-ML.exe
```

Important : avec ce projet, utilisez toujours `venv\Scripts\python.exe -m pip ...`
pour installer les bibliotheques.
