$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$python = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Venv introuvable. Creez d'abord le venv puis installez requirements.txt."
}

& $python -m pip install -r requirements.txt
& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --name "Plateforme-IA-ML" `
    --hidden-import matplotlib.backends.backend_tkagg `
    --add-data "assets;assets" `
    --collect-data customtkinter `
    --collect-data matplotlib `
    --collect-data statsmodels `
    --exclude-module pandas.tests `
    --exclude-module sklearn.tests `
    --exclude-module scipy.tests `
    --exclude-module matplotlib.tests `
    main.py

Write-Host ""
Write-Host "Application generee dans : dist\Plateforme-IA-ML\Plateforme-IA-ML.exe"
