$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $PSScriptRoot
$PythonBin = if ($env:PYTHON) { $env:PYTHON } else { "python" }
Set-Location $RootDir
& $PythonBin experiments/run_statistics.py --output results/audit/statistics.json
& $PythonBin scripts/validate_release.py
& $PythonBin scripts/generate_current_paper_figures.py
Write-Host "Reproduction complete."
